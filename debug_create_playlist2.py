"""Debug: inspect the NEW playlist creation dialog."""
import sys, os, time, subprocess, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555
VIDEO_ID = "euSotih5hqs"

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

print("[BROWSER] Fechando Chrome...")
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

# Navigate and open playlist dialog
driver.get(f"https://studio.youtube.com/video/{VIDEO_ID}/edit")
time.sleep(8)
print(f"[PAGE] {driver.title}")

# Open playlist dialog
driver.execute_script("""
    var trigger = document.querySelector('ytcp-dropdown-trigger[aria-label*="playlist"]');
    if (trigger) trigger.click();
""")
time.sleep(3)

# Click "Nova playlist"
driver.execute_script("""
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return;
    var btn = dialog.querySelector('.new-playlist-button button');
    if (btn) btn.click();
""")
time.sleep(2)

# Click menu item
driver.execute_script("""
    var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
    if (item) item.click();
""")
time.sleep(5)

# NOW: inspect the NEW dialog that appeared (outside ytcp-playlist-dialog)
print("\n[INSPECT] Procurando novo dialog de criacao...")

# Find ALL dialogs on the page
dialogs_info = driver.execute_script("""
    var results = [];
    var allDialogs = document.querySelectorAll('ytcp-dialog, tp-yt-paper-dialog, [role="dialog"], dialog, .dialog');
    for (var d of allDialogs) {
        results.push({
            tag: d.tagName,
            id: d.id,
            class: (d.className || '').toString().substring(0, 80),
            visible: d.offsetParent !== null || getComputedStyle(d).display !== 'none',
            height: d.offsetHeight,
            innerHTML_length: d.innerHTML.length,
            hasTitle: !!(d.querySelector('h1, h2, .header, .title')),
            headerText: (function() {
                var h = d.querySelector('h1, h2, .header, .dialog-title, yt-formatted-string.header');
                return h ? h.textContent.trim().substring(0, 50) : '';
            })()
        });
    }
    return results;
""")
print(f"  Dialogs encontrados: {len(dialogs_info)}")
for d in dialogs_info:
    print(f"  {json.dumps(d, ensure_ascii=False)}")

# Find the "Criar uma nova playlist" dialog specifically
print("\n[INSPECT] Procurando campos do dialog de criacao...")
fields = driver.execute_script("""
    // Find the dialog with "Criar uma nova playlist" or "Create a new playlist"
    var allDialogs = document.querySelectorAll('ytcp-dialog, tp-yt-paper-dialog, [role="dialog"]');
    var createDialog = null;
    for (var d of allDialogs) {
        var txt = (d.textContent || '').toLowerCase();
        if (txt.includes('criar uma nova playlist') || txt.includes('create a new playlist') ||
            txt.includes('título (obrigatório)') || txt.includes('title (required)')) {
            createDialog = d;
            break;
        }
    }
    if (!createDialog) return {error: 'dialog_not_found'};

    var result = {found: true, tag: createDialog.tagName, id: createDialog.id};

    // Find all input-like elements
    result.inputs = [];
    var inputs = createDialog.querySelectorAll('input, textarea, div[contenteditable="true"], [contenteditable=""], [contenteditable="plaintext-only"]');
    for (var el of inputs) {
        result.inputs.push({
            tag: el.tagName,
            type: el.type || '',
            id: el.id,
            name: el.name || '',
            class: (el.className || '').toString().substring(0, 60),
            placeholder: el.placeholder || el.getAttribute('aria-label') || '',
            visible: el.offsetParent !== null,
            height: el.offsetHeight,
            contentEditable: el.contentEditable || ''
        });
    }

    // Find all buttons
    result.buttons = [];
    var btns = createDialog.querySelectorAll('button, ytcp-button');
    for (var b of btns) {
        var txt = (b.textContent || '').trim();
        if (txt.length > 0 && txt.length < 30) {
            result.buttons.push({
                tag: b.tagName,
                text: txt,
                id: b.id,
                disabled: b.hasAttribute('disabled'),
                ariaDisabled: b.getAttribute('aria-disabled'),
                visible: b.offsetParent !== null
            });
        }
    }

    // Find dropdowns (visibility)
    result.dropdowns = [];
    var dds = createDialog.querySelectorAll('select, ytcp-dropdown-trigger, tp-yt-paper-dropdown-menu');
    for (var dd of dds) {
        result.dropdowns.push({
            tag: dd.tagName,
            id: dd.id,
            text: (dd.textContent || '').trim().substring(0, 30),
            visible: dd.offsetParent !== null
        });
    }

    return result;
""")
print(json.dumps(fields, indent=2, ensure_ascii=False))

# Try to type in the title field
if fields.get('inputs'):
    print("\n[TYPE] Tentando preencher titulo...")
    for i, inp in enumerate(fields['inputs']):
        if inp.get('visible') and inp.get('tag') in ('INPUT', 'TEXTAREA') and inp.get('id') != 'search-input':
            print(f"  Usando input #{i}: {inp}")

            # Focus and type
            typed = driver.execute_script(f"""
                var dialog = null;
                var allDialogs = document.querySelectorAll('ytcp-dialog, tp-yt-paper-dialog, [role="dialog"]');
                for (var d of allDialogs) {{
                    if ((d.textContent || '').toLowerCase().includes('criar uma nova playlist') ||
                        (d.textContent || '').toLowerCase().includes('título (obrigatório)')) {{
                        dialog = d;
                        break;
                    }}
                }}
                if (!dialog) return 'no_dialog';
                var inputs = dialog.querySelectorAll('input, textarea');
                var idx = 0;
                for (var el of inputs) {{
                    if (el.offsetParent !== null && el.id !== 'search-input') {{
                        if (idx === {i - len([x for x in fields['inputs'][:i] if x.get('tag') in ('DIV',)])}) {{
                            el.focus();
                            el.click();
                            el.value = 'Portfolio - Netshoes';
                            el.dispatchEvent(new Event('input', {{bubbles: true}}));
                            el.dispatchEvent(new Event('change', {{bubbles: true}}));
                            return 'typed: ' + el.tagName + '#' + el.id;
                        }}
                        idx++;
                    }}
                }}
                return 'no_match';
            """)
            print(f"  Result: {typed}")
            time.sleep(1)

            # Also try send_keys
            try:
                active = driver.switch_to.active_element
                active.clear()
                active.send_keys("Portfolio - Netshoes")
                print(f"  send_keys: OK")
            except Exception as e:
                print(f"  send_keys: {e}")

            time.sleep(2)
            driver.save_screenshot("debug_after_title_typed.png")
            print("  Screenshot: debug_after_title_typed.png")

            # Check Criar button
            criar = driver.execute_script("""
                var allDialogs = document.querySelectorAll('ytcp-dialog, tp-yt-paper-dialog, [role="dialog"]');
                for (var d of allDialogs) {
                    if (!(d.textContent || '').toLowerCase().includes('criar uma nova playlist')) continue;
                    var btns = d.querySelectorAll('button, ytcp-button');
                    for (var b of btns) {
                        var txt = (b.textContent || '').trim().toLowerCase();
                        if (txt === 'criar' || txt === 'create') {
                            return {
                                text: b.textContent.trim(),
                                disabled: b.hasAttribute('disabled'),
                                ariaDisabled: b.getAttribute('aria-disabled')
                            };
                        }
                    }
                }
                return 'not_found';
            """)
            print(f"  Criar button after typing: {criar}")
            break

print("\n[DONE]")
