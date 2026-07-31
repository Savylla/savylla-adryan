"""Debug: captura HTML do seletor de playlists na pagina de edicao do YouTube Studio."""
import sys, os, time, subprocess, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555
VIDEO_ID = "dxdNxe9Zzg4"  # Primeiro video Mercado Pago

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

# Start Chrome
chrome_path = find_chrome()
custom_data_dir = os.path.join(os.path.expanduser("~"), "chrome_selenium_data")
os.makedirs(custom_data_dir, exist_ok=True)

print("[BROWSER] Fechando Chrome existente...")
try:
    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True, timeout=10)
    time.sleep(3)
except Exception:
    pass

chrome_cmd = [
    chrome_path,
    f"--remote-debugging-port={CHROME_DEBUG_PORT}",
    f"--user-data-dir={custom_data_dir}",
    "--disable-blink-features=AutomationControlled",
    "--no-first-run", "--no-default-browser-check", "--log-level=3",
]
print(f"[BROWSER] Iniciando Chrome (porta {CHROME_DEBUG_PORT})...")
subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(10)

options = Options()
options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")
driver = webdriver.Chrome(options=options)

# Navigate to video edit page
url = f"https://studio.youtube.com/video/{VIDEO_ID}/edit"
print(f"[NAV] Abrindo {url}")
driver.get(url)
time.sleep(8)

# Check page title
title = driver.title
print(f"[PAGE] Title: {title}")
print(f"[PAGE] URL: {driver.current_url}")

# Check if we're on the edit page
page_check = driver.execute_script("""
    var results = {};
    results.hasMetadataEditor = !!document.querySelector('ytcp-video-metadata-editor');
    results.hasDetails = !!document.querySelector('#details');
    results.hasMentionTextbox = !!document.querySelector('ytcp-mention-textbox');
    results.hasVideoTitle = !!document.querySelector('#title-textarea, ytcp-mention-textbox #textbox');

    // Look for anything playlist-related
    var allElements = document.querySelectorAll('*');
    var playlistElements = [];
    for (var el of allElements) {
        var tag = el.tagName.toLowerCase();
        var cls = el.className || '';
        var id = el.id || '';
        var aria = el.getAttribute('aria-label') || '';
        var txt = (el.textContent || '').trim().substring(0, 50);

        if (tag.includes('playlist') || cls.toString().includes('playlist') ||
            id.includes('playlist') || aria.toLowerCase().includes('playlist') ||
            (txt.toLowerCase().includes('playlist') && el.children.length < 3)) {
            playlistElements.push({
                tag: tag,
                id: id,
                class: cls.toString().substring(0, 80),
                aria: aria,
                text: txt,
                visible: el.offsetParent !== null,
                tagName: el.tagName
            });
        }
    }
    results.playlistElements = playlistElements;
    return results;
""")
print(f"\n[DEBUG] Page state:")
print(f"  hasMetadataEditor: {page_check.get('hasMetadataEditor')}")
print(f"  hasDetails: {page_check.get('hasDetails')}")
print(f"  hasMentionTextbox: {page_check.get('hasMentionTextbox')}")
print(f"  hasVideoTitle: {page_check.get('hasVideoTitle')}")

print(f"\n[DEBUG] Playlist-related elements ({len(page_check.get('playlistElements', []))}):")
for el in page_check.get('playlistElements', []):
    vis = "VISIBLE" if el.get('visible') else "hidden"
    print(f"  <{el['tag']} id='{el['id']}' class='{el['class'][:50]}' aria='{el['aria']}' [{vis}]> {el['text'][:40]}")

# Try clicking various playlist selectors
print("\n[DEBUG] Tentando abrir seletor de playlists...")
click_results = driver.execute_script("""
    var results = [];

    // Method 1: ytcp-video-metadata-playlists
    var vmp = document.querySelector('ytcp-video-metadata-playlists');
    results.push({method: 'ytcp-video-metadata-playlists', found: !!vmp, visible: vmp ? vmp.offsetParent !== null : false});

    // Method 2: dropdown trigger with playlist text
    var triggers = document.querySelectorAll('ytcp-text-dropdown-trigger, ytcp-dropdown-trigger');
    for (var t of triggers) {
        var txt = (t.textContent || '').toLowerCase();
        var aria = (t.getAttribute('aria-label') || '').toLowerCase();
        results.push({
            method: 'dropdown-trigger',
            text: (t.textContent || '').trim().substring(0, 60),
            aria: t.getAttribute('aria-label') || '',
            visible: t.offsetParent !== null,
            hasPlaylist: txt.includes('playlist') || aria.includes('playlist')
        });
    }

    // Method 3: Any clickable element with "playlist" text
    var btns = document.querySelectorAll('button, ytcp-button, [role="button"]');
    for (var b of btns) {
        var txt = (b.textContent || '').toLowerCase();
        var aria = (b.getAttribute('aria-label') || '').toLowerCase();
        if (txt.includes('playlist') || aria.includes('playlist')) {
            results.push({
                method: 'button',
                tag: b.tagName,
                text: (b.textContent || '').trim().substring(0, 60),
                aria: b.getAttribute('aria-label') || '',
                visible: b.offsetParent !== null
            });
        }
    }

    return results;
""")

print(f"\n[DEBUG] Click targets found ({len(click_results)}):")
for r in click_results:
    print(f"  {json.dumps(r, ensure_ascii=False)}")

# Now try to click the playlist element
print("\n[DEBUG] Clicando no elemento de playlist...")
click_result = driver.execute_script("""
    // Try all known methods
    var vmp = document.querySelector('ytcp-video-metadata-playlists');
    if (vmp) {
        // Find clickable child
        var trigger = vmp.querySelector('ytcp-text-dropdown-trigger, ytcp-dropdown-trigger, button, [role="button"]');
        if (trigger) { trigger.click(); return 'clicked_vmp_trigger: ' + trigger.tagName; }
        vmp.click();
        return 'clicked_vmp';
    }

    // Try all dropdown triggers
    var triggers = document.querySelectorAll('ytcp-text-dropdown-trigger');
    for (var t of triggers) {
        var txt = (t.textContent || '').toLowerCase();
        var aria = (t.getAttribute('aria-label') || '').toLowerCase();
        if (txt.includes('playlist') || aria.includes('playlist')) {
            t.click();
            return 'clicked_trigger: ' + (t.textContent || '').trim().substring(0, 40);
        }
    }

    return 'nothing_found';
""")
print(f"  Result: {click_result}")
time.sleep(3)

# Check if dialog appeared
dialog_check = driver.execute_script("""
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return {found: false};
    return {
        found: true,
        visible: dialog.offsetParent !== null,
        display: getComputedStyle(dialog).display,
        height: dialog.offsetHeight,
        innerHTML_length: dialog.innerHTML.length
    };
""")
print(f"\n[DEBUG] Playlist dialog: {json.dumps(dialog_check, ensure_ascii=False)}")

# Take screenshot
driver.save_screenshot("debug_edit_playlist.png")
print("\n[OK] Screenshot salvo: debug_edit_playlist.png")

print("\n[DONE] Debug completo.")
