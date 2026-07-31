"""
Debug: captura HTML do dialogo de criacao de playlist no YouTube Studio.
Abre um video, abre o dialogo de playlist, clica em "Nova playlist" e captura o HTML.
"""
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555

def connect_to_chrome():
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")
    driver = webdriver.Chrome(options=options)
    return driver


def main():
    # Read a video ID that needs a NEW playlist (Uber)
    with open("youtube_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Pick first Uber video
    video_id = data["Uber"][0]["video_id"]
    print(f"[DEBUG] Video: {video_id}")

    driver = connect_to_chrome()

    # Go to video edit page
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    print("[DEBUG] Aguardando pagina carregar...")
    time.sleep(8)

    # Step 1: Open playlist dialog
    print("[DEBUG] Abrindo dialogo de playlists...")
    driver.execute_script("""
        // Try clicking the playlist section to open dialog
        var plBtn = document.querySelector('ytcp-video-metadata-playlists button');
        if (plBtn) { plBtn.click(); return; }
        var plSection = document.querySelector('ytcp-video-metadata-playlists');
        if (plSection) { plSection.click(); return; }
        // Fallback: look for dropdown with playlist text
        var allBtns = document.querySelectorAll('ytcp-text-dropdown-trigger, button');
        for (var b of allBtns) {
            var txt = (b.textContent || '').toLowerCase();
            if (txt.includes('playlist') || txt.includes('selecionar')) {
                b.click(); return;
            }
        }
    """)
    time.sleep(5)

    # Capture playlist dialog HTML
    html1 = driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (dialog) return dialog.outerHTML.substring(0, 5000);
        // Try other selectors
        var dialogs = document.querySelectorAll('tp-yt-paper-dialog[aria-modal="true"], ytcp-dialog');
        for (var d of dialogs) {
            if (d.offsetHeight > 100) return d.outerHTML.substring(0, 5000);
        }
        return 'NO_PLAYLIST_DIALOG_FOUND';
    """)

    with open("debug_step1_playlist_dialog.txt", "w", encoding="utf-8") as f:
        f.write(html1)
    print(f"[DEBUG] Step 1 salvo (playlist dialog): {len(html1)} chars")

    # Step 2: Click "Nova playlist" button
    print("[DEBUG] Clicando em 'Nova playlist'...")
    click_result = driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return 'no_dialog';

        // Try dedicated button
        var dropBtn = dialog.querySelector('.new-playlist-button button, #new-playlist-button button');
        if (dropBtn) { dropBtn.click(); return 'clicked_button'; }

        // Try any button with text
        var btns = dialog.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').toLowerCase();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                b.click(); return 'clicked_text:' + b.tagName + ':' + b.className;
            }
        }

        // List all buttons for debug
        var allBtns = [];
        btns = dialog.querySelectorAll('button, ytcp-button, tp-yt-paper-button');
        for (var b of btns) {
            allBtns.push(b.tagName + '|' + b.className.substring(0,50) + '|' + (b.textContent||'').trim().substring(0,40));
        }
        return 'not_found:' + allBtns.join(' ;; ');
    """)
    print(f"[DEBUG] Nova playlist click: {click_result}")
    time.sleep(3)

    # Step 3: Click menu item if dropdown appeared
    menu_result = driver.execute_script("""
        var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
        if (item) { item.click(); return 'clicked_test_id'; }
        var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], [role="option"]');
        var found = [];
        for (var i of items) {
            var txt = (i.textContent || '').toLowerCase().trim();
            found.push(txt.substring(0, 50));
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                i.click(); return 'clicked_menu:' + txt.substring(0, 50);
            }
        }
        return 'menu_not_found:' + found.join(' ;; ');
    """)
    print(f"[DEBUG] Menu item: {menu_result}")
    time.sleep(8)

    # Step 4: Capture the creation dialog HTML
    html2 = driver.execute_script("""
        // Check for creation dialog
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (cd) return 'CREATION_DIALOG:\\n' + cd.outerHTML.substring(0, 8000);

        // Check all visible dialogs
        var result = '';
        var allDialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog, [role="dialog"]');
        for (var d of allDialogs) {
            if (d.offsetHeight > 50) {
                result += '\\nDIALOG(' + d.tagName + ' h=' + d.offsetHeight + '):\\n' + d.outerHTML.substring(0, 5000) + '\\n---\\n';
            }
        }
        if (!result) {
            // Broader search - any overlay/modal
            var overlays = document.querySelectorAll('[aria-modal="true"], .overlay, .dialog');
            for (var o of overlays) {
                if (o.offsetHeight > 50) {
                    result += '\\nOVERLAY(' + o.tagName + '):\\n' + o.outerHTML.substring(0, 3000) + '\\n---\\n';
                }
            }
        }
        return result || 'NO_CREATION_DIALOG_FOUND';
    """)

    with open("debug_step2_creation_dialog.txt", "w", encoding="utf-8") as f:
        f.write(html2)
    print(f"[DEBUG] Step 2 salvo (creation dialog): {len(html2)} chars")

    # Also check for contenteditable elements
    editables = driver.execute_script("""
        var results = [];
        var els = document.querySelectorAll('[contenteditable="true"], [contenteditable=""], input[type="text"], textarea');
        for (var e of els) {
            if (e.offsetHeight > 0) {
                results.push({
                    tag: e.tagName,
                    id: e.id,
                    cls: (e.className || '').toString().substring(0, 80),
                    parent: e.parentElement ? e.parentElement.tagName + '.' + (e.parentElement.className || '').toString().substring(0, 40) : '',
                    h: e.offsetHeight,
                    w: e.offsetWidth,
                    contentEditable: e.contentEditable,
                    visible: e.offsetParent !== null
                });
            }
        }
        return JSON.stringify(results, null, 2);
    """)

    with open("debug_step3_editables.txt", "w", encoding="utf-8") as f:
        f.write(editables)
    print(f"[DEBUG] Step 3 salvo (editables): {len(editables)} chars")

    # Screenshot
    driver.save_screenshot("debug_creation_dialog.png")
    print("[DEBUG] Screenshot salvo: debug_creation_dialog.png")

    print("\n[DONE] Arquivos de debug salvos. Analise:")
    print("  - debug_step1_playlist_dialog.txt")
    print("  - debug_step2_creation_dialog.txt")
    print("  - debug_step3_editables.txt")
    print("  - debug_creation_dialog.png")


if __name__ == "__main__":
    main()
