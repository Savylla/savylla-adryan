"""
Debug: captura estado do dialogo de criacao de playlist passo a passo.
Conecta ao Chrome ja aberto (porta 9555).
"""
import json
import os
import sys
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555

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

# Start fresh Chrome
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

# Use first Uber video
VIDEO_ID = "ZT8eawnV8p4"
PLAYLIST_NAME = "Portfolio - Uber"

print(f"[1] Navegando para video {VIDEO_ID}...")
driver.get(f"https://studio.youtube.com/video/{VIDEO_ID}/edit")
time.sleep(8)
print(f"    Titulo: {driver.title}")

# Step 2: Open playlist dialog
print("[2] Abrindo dialogo de playlists...")
opened = driver.execute_script("""
    var trigger = document.querySelector('ytcp-dropdown-trigger[aria-label*="playlist" i]');
    if (trigger) { trigger.click(); return 'clicked_aria'; }
    var vmp = document.querySelector('ytcp-video-metadata-playlists');
    if (vmp) {
        var inner = vmp.querySelector('ytcp-dropdown-trigger, button');
        if (inner) { inner.click(); return 'clicked_vmp'; }
    }
    return 'not_found';
""")
print(f"    Resultado: {opened}")
time.sleep(4)

# Step 3: Dump the playlist dialog state
print("[3] Estado do dialogo de playlists...")
dialog_state = driver.execute_script("""
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return {exists: false};

    var result = {
        exists: true,
        height: dialog.offsetHeight,
        visible: dialog.offsetParent !== null || getComputedStyle(dialog).display !== 'none'
    };

    // List all playlists visible
    var groups = dialog.querySelectorAll('ytcp-checkbox-group');
    result.playlists = [];
    for (var g of groups) {
        var span = g.querySelector('span.checkbox-label, span.label, span.label-text, label');
        result.playlists.push(span ? span.textContent.trim() : '(no label)');
    }

    // List all buttons
    result.buttons = [];
    var btns = dialog.querySelectorAll('button, ytcp-button, tp-yt-paper-button, a');
    for (var b of btns) {
        var txt = (b.textContent || '').trim();
        if (txt && txt.length < 50) {
            result.buttons.push({
                tag: b.tagName,
                text: txt,
                class: (b.className||'').toString().substring(0,50),
                id: b.id,
                visible: b.offsetParent !== null
            });
        }
    }

    return result;
""")
print(f"    {json.dumps(dialog_state, indent=2, ensure_ascii=False)}")
driver.save_screenshot("debug_v3_step3_dialog.png")

# Step 4: Click "Nova playlist" button
print("[4] Clicando 'Nova playlist'...")
click1 = driver.execute_script("""
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return 'no_dialog';

    // Try the new-playlist-button
    var npBtn = dialog.querySelector('#new-playlist-button, .new-playlist-button');
    if (npBtn) {
        var inner = npBtn.querySelector('button') || npBtn;
        inner.click();
        return 'clicked_np_button:' + inner.tagName + ':' + (inner.textContent||'').trim().substring(0,30);
    }

    // Try by text
    var btns = dialog.querySelectorAll('button, ytcp-button, tp-yt-paper-button, a, div[role="button"]');
    for (var b of btns) {
        var txt = (b.textContent || '').trim().toLowerCase();
        if (txt.includes('nova playlist') || txt.includes('new playlist')) {
            b.click();
            return 'clicked_text:' + b.tagName + ':' + txt.substring(0,30);
        }
    }

    // List what we found for debugging
    var found = [];
    btns = dialog.querySelectorAll('button, ytcp-button, a, div[role="button"]');
    for (var b of btns) {
        var txt = (b.textContent || '').trim();
        if (txt && txt.length < 50) found.push(b.tagName + ':' + txt);
    }
    return 'not_found:' + found.join(' | ');
""")
print(f"    Resultado: {click1}")
time.sleep(3)
driver.save_screenshot("debug_v3_step4_after_nova.png")

# Step 5: Check for dropdown menu item
print("[5] Verificando menu dropdown...")
menu_result = driver.execute_script("""
    // Check for paper items (dropdown menu)
    var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
    if (item) { item.click(); return 'clicked_test_id'; }

    var items = document.querySelectorAll('tp-yt-paper-item, tp-yt-paper-listbox tp-yt-paper-item, [role="menuitem"], [role="option"]');
    var found = [];
    for (var i of items) {
        var txt = (i.textContent || '').trim();
        if (txt && txt.length < 50) found.push(txt);
        if (txt.toLowerCase().includes('nova playlist') || txt.toLowerCase().includes('new playlist')) {
            i.click();
            return 'clicked_menu:' + txt;
        }
    }
    return 'not_found: items=[' + found.join(', ') + ']';
""")
print(f"    Resultado: {menu_result}")
time.sleep(8)
driver.save_screenshot("debug_v3_step5_after_menu.png")

# Step 6: Inspect ALL dialogs on the page now
print("[6] Inspecionando todos os dialogs...")
all_dialogs = driver.execute_script("""
    var results = [];
    var selectors = [
        'ytcp-playlist-creation-dialog',
        'ytcp-dialog',
        'tp-yt-paper-dialog',
        '[role="dialog"]',
        '[aria-modal="true"]',
        'dialog'
    ];
    var seen = new Set();

    for (var sel of selectors) {
        var els = document.querySelectorAll(sel);
        for (var el of els) {
            var key = el.tagName + '#' + el.id;
            if (seen.has(key)) continue;
            seen.add(key);

            var info = {
                selector: sel,
                tag: el.tagName,
                id: el.id,
                height: el.offsetHeight,
                width: el.offsetWidth,
                display: getComputedStyle(el).display,
                textSnippet: (el.textContent || '').trim().substring(0, 100)
            };

            // Check for input fields
            var inputs = el.querySelectorAll('input, textarea, [contenteditable="true"], [contenteditable=""], [contenteditable="plaintext-only"]');
            info.inputCount = inputs.length;
            info.inputs = [];
            for (var inp of inputs) {
                info.inputs.push({
                    tag: inp.tagName,
                    type: inp.type || '',
                    id: inp.id,
                    contentEditable: inp.contentEditable,
                    height: inp.offsetHeight,
                    visible: inp.offsetParent !== null,
                    placeholder: inp.placeholder || inp.getAttribute('aria-label') || ''
                });
            }

            results.push(info);
        }
    }
    return results;
""")

for d in all_dialogs:
    print(f"    {json.dumps(d, indent=4, ensure_ascii=False)}")

# Step 7: Full HTML dump of creation dialog area
print("[7] Dump HTML do dialog de criacao...")
html_dump = driver.execute_script("""
    // Try the specific creation dialog
    var cd = document.querySelector('ytcp-playlist-creation-dialog');
    if (cd && cd.offsetHeight > 0) return 'CREATION_DIALOG: ' + cd.outerHTML.substring(0, 10000);

    // Try any visible dialog that appeared recently
    var dialogs = document.querySelectorAll('ytcp-dialog, tp-yt-paper-dialog, [role="dialog"]');
    var best = null;
    for (var d of dialogs) {
        if (d.offsetHeight > 100) {
            var txt = (d.textContent || '').toLowerCase();
            if (txt.includes('playlist') || txt.includes('título') || txt.includes('title')) {
                if (!best || d.offsetHeight > best.offsetHeight) best = d;
            }
        }
    }
    if (best) return 'FOUND_DIALOG: ' + best.outerHTML.substring(0, 10000);

    return 'NO_CREATION_DIALOG';
""")

with open("debug_v3_html_dump.txt", "w", encoding="utf-8") as f:
    f.write(html_dump)
print(f"    Salvo em debug_v3_html_dump.txt ({len(html_dump)} chars)")
print(f"    Preview: {html_dump[:200]}")

print("\n[DONE] Screenshots salvos:")
print("  - debug_v3_step3_dialog.png")
print("  - debug_v3_step4_after_nova.png")
print("  - debug_v3_step5_after_menu.png")
print("  - debug_v3_html_dump.txt")
