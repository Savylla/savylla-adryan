"""Debug: tenta criar playlist e captura estado de cada etapa."""
import sys, os, time, subprocess, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555
VIDEO_ID = "euSotih5hqs"  # Netshoes video (needs new playlist)

def find_chrome():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\Application\chrome.exe",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

chrome_path = find_chrome()
custom_data_dir = os.path.join(os.path.expanduser("~"), "chrome_selenium_data")

print("[BROWSER] Fechando Chrome existente...")
try:
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True, timeout=10)
    time.sleep(3)
except Exception:
    pass

subprocess.Popen([
    chrome_path, f"--remote-debugging-port={CHROME_DEBUG_PORT}",
    f"--user-data-dir={custom_data_dir}",
    "--disable-blink-features=AutomationControlled",
    "--no-first-run", "--no-default-browser-check", "--log-level=3",
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(10)

options = Options()
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")
driver = webdriver.Chrome(options=options)

# Navigate
url = f"https://studio.youtube.com/video/{VIDEO_ID}/edit"
print(f"[NAV] {url}")
driver.get(url)
time.sleep(8)
print(f"[PAGE] {driver.title}")

# Open playlist dialog
print("\n[1] Abrindo dialog de playlist...")
driver.execute_script("""
    var trigger = document.querySelector('ytcp-dropdown-trigger[aria-label*="playlist"], ytcp-dropdown-trigger[aria-label*="Playlist"]');
    if (trigger) trigger.click();
""")
time.sleep(3)

# Verify dialog
dialog_ok = driver.execute_script("""
    var d = document.querySelector('ytcp-playlist-dialog');
    return d ? d.innerHTML.length : 0;
""")
print(f"[2] Dialog innerHTML length: {dialog_ok}")

# Click "Nova playlist" button
print("\n[3] Clicando 'Nova playlist'...")
btn_result = driver.execute_script("""
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return 'no_dialog';
    var dropBtn = dialog.querySelector('.new-playlist-button button, #new-playlist-button button');
    if (dropBtn) { dropBtn.click(); return 'clicked_drop: ' + dropBtn.textContent.trim().substring(0, 30); }
    var btns = dialog.querySelectorAll('button, ytcp-button');
    for (var b of btns) {
        var txt = (b.textContent || '').toLowerCase();
        if (txt.includes('nova playlist') || txt.includes('new playlist')) {
            b.click();
            return 'clicked_text: ' + b.textContent.trim().substring(0, 30);
        }
    }
    return 'not_found';
""")
print(f"  Result: {btn_result}")
time.sleep(2)

# Click menu item
print("\n[4] Clicando item 'Nova playlist' no menu...")
item_result = driver.execute_script("""
    var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
    if (item) { item.click(); return 'clicked'; }
    var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], [role="option"]');
    for (var i of items) {
        var txt = (i.textContent || '').toLowerCase();
        if (txt.includes('nova playlist') || txt.includes('new playlist')) {
            i.click();
            return 'clicked: ' + i.textContent.trim().substring(0, 30);
        }
    }
    return 'not_found';
""")
print(f"  Result: {item_result}")
time.sleep(8)

# Screenshot after clicking
driver.save_screenshot("debug_after_nova_playlist.png")
print("[5] Screenshot: debug_after_nova_playlist.png")

# Inspect what appeared
print("\n[6] Inspecionando formulario de criacao...")
form_state = driver.execute_script("""
    var pd = document.querySelector('ytcp-playlist-dialog');
    if (!pd) return {error: 'no_dialog'};

    var result = {};

    // Check for creation form
    result.hasCreateForm = !!pd.querySelector('#create-playlist-form');
    result.hasPlaylistCreation = !!pd.querySelector('ytcp-playlist-creation');

    // Find ALL contenteditable elements
    var editables = pd.querySelectorAll('div[contenteditable], [contenteditable="true"], [contenteditable=""]');
    result.editables = [];
    for (var el of editables) {
        result.editables.push({
            tag: el.tagName,
            id: el.id,
            class: (el.className || '').toString().substring(0, 50),
            contentEditable: el.contentEditable,
            visible: el.offsetParent !== null,
            height: el.offsetHeight,
            width: el.offsetWidth,
            text: el.textContent.substring(0, 20),
            ariaLabel: el.getAttribute('aria-label') || ''
        });
    }

    // Find textareas and inputs
    var inputs = pd.querySelectorAll('textarea, input[type="text"]');
    result.inputs = [];
    for (var el of inputs) {
        result.inputs.push({
            tag: el.tagName,
            id: el.id,
            visible: el.offsetParent !== null,
            value: el.value.substring(0, 20)
        });
    }

    // Find "Criar" button state
    var btns = pd.querySelectorAll('ytcp-button, button');
    result.buttons = [];
    for (var b of btns) {
        var txt = (b.textContent || '').trim().toLowerCase();
        if (txt === 'criar' || txt === 'create' || txt === 'concluir' || txt === 'done' || txt.includes('nova')) {
            result.buttons.push({
                tag: b.tagName,
                text: (b.textContent || '').trim().substring(0, 20),
                disabled: b.hasAttribute('disabled'),
                ariaDisabled: b.getAttribute('aria-disabled'),
                visible: b.offsetParent !== null
            });
        }
    }

    return result;
""")
print(json.dumps(form_state, indent=2, ensure_ascii=False))

# Try to focus and type
print("\n[7] Tentando focar e digitar no textbox...")
if form_state.get('editables'):
    for i, ed in enumerate(form_state['editables']):
        if ed.get('visible') and ed.get('height', 0) > 0:
            print(f"  Tentando editable #{i}: {ed}")

            # Focus via JS
            focus_result = driver.execute_script(f"""
                var pd = document.querySelector('ytcp-playlist-dialog');
                var all = pd.querySelectorAll('div[contenteditable], [contenteditable="true"], [contenteditable=""]');
                var el = all[{i}];
                if (el) {{
                    el.focus();
                    el.click();
                    el.textContent = '';
                    return 'focused: ' + el.tagName + ' editable=' + el.contentEditable;
                }}
                return 'not_found';
            """)
            print(f"  Focus: {focus_result}")
            time.sleep(0.5)

            # Type via send_keys
            try:
                active = driver.switch_to.active_element
                active_info = driver.execute_script("""
                    var el = document.activeElement;
                    return {
                        tag: el.tagName,
                        id: el.id,
                        contentEditable: el.contentEditable,
                        class: (el.className || '').toString().substring(0, 50)
                    };
                """)
                print(f"  Active element: {active_info}")
                active.send_keys("Portfolio - Netshoes")
                time.sleep(1)
            except Exception as e:
                print(f"  send_keys error: {e}")

            # Check what was typed
            typed = driver.execute_script(f"""
                var pd = document.querySelector('ytcp-playlist-dialog');
                var all = pd.querySelectorAll('div[contenteditable], [contenteditable="true"], [contenteditable=""]');
                var el = all[{i}];
                return el ? el.textContent : 'N/A';
            """)
            print(f"  Text after typing: '{typed}'")

            # Also try execCommand
            driver.execute_script("""
                var el = document.activeElement;
                if (el && (el.contentEditable === 'true' || el.contentEditable === '')) {
                    if (!(el.textContent || '').trim()) {
                        el.focus();
                        document.execCommand('selectAll', false, null);
                        document.execCommand('insertText', false, 'Portfolio - Netshoes');
                    }
                }
            """)
            time.sleep(1)

            typed2 = driver.execute_script(f"""
                var pd = document.querySelector('ytcp-playlist-dialog');
                var all = pd.querySelectorAll('div[contenteditable], [contenteditable="true"], [contenteditable=""]');
                var el = all[{i}];
                return el ? el.textContent : 'N/A';
            """)
            print(f"  Text after execCommand: '{typed2}'")

            # Dispatch events
            driver.execute_script("""
                var el = document.activeElement;
                if (el) {
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    el.dispatchEvent(new InputEvent('input', {bubbles: true, data: 'x', inputType: 'insertText'}));
                }
            """)
            time.sleep(2)

            # Check Criar button state now
            criar_state = driver.execute_script("""
                var pd = document.querySelector('ytcp-playlist-dialog');
                var btns = pd.querySelectorAll('ytcp-button, button');
                for (var b of btns) {
                    var txt = (b.textContent || '').trim().toLowerCase();
                    if (txt === 'criar' || txt === 'create') {
                        return {
                            text: b.textContent.trim(),
                            disabled: b.hasAttribute('disabled'),
                            ariaDisabled: b.getAttribute('aria-disabled'),
                            className: (b.className || '').toString().substring(0, 60)
                        };
                    }
                }
                return 'not_found';
            """)
            print(f"  Criar button: {criar_state}")

            driver.save_screenshot("debug_after_typing.png")
            print("  Screenshot: debug_after_typing.png")
            break
else:
    print("  Nenhum editable visivel encontrado!")

print("\n[DONE]")
