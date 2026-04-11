#!/usr/bin/env python3
"""
Fix: Add 29 Raia videos to 'Portfolio - Raia' playlist.
Titles/descriptions are already correct - only playlist is missing.
"""

import json
import time
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_PROFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_selenium_data")

def start_chrome():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True, timeout=5)
        time.sleep(2)
    except Exception:
        pass

    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE}")
    options.add_argument("--profile-directory=Savylla Adryan")
    options.add_argument("--remote-debugging-port=9556")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def create_playlist_if_needed(driver, playlist_name):
    """Create playlist from YouTube Studio playlists page."""
    driver.get("https://studio.youtube.com/channel/playlists")
    time.sleep(5)

    # Check if playlist already exists
    exists = driver.execute_script("""
        var items = document.querySelectorAll('ytcp-playlist-title a, .playlist-title, [class*="playlist"] a');
        for (var item of items) {
            if ((item.textContent || '').trim().includes(arguments[0])) return true;
        }
        return false;
    """, playlist_name)

    if exists:
        print(f"  [OK] Playlist '{playlist_name}' ja existe")
        return True

    print(f"  [INFO] Playlist '{playlist_name}' nao encontrada, sera criada no primeiro video")
    return False


def add_video_to_playlist(driver, video_id, playlist_name, is_first=False):
    """Navigate to video edit page and add to playlist."""
    driver.get(f"https://studio.youtube.com/video/{video_id}/edit")
    time.sleep(5)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#textbox[contenteditable='true']"))
        )
    except Exception:
        print(f"  [ERRO] Pagina de edicao nao carregou")
        return False

    # Open playlist dialog
    opened = driver.execute_script("""
        var comp = document.querySelector('ytcp-video-metadata-playlists');
        if (comp) {
            var trigger = comp.querySelector('ytcp-text-dropdown-trigger, [role="button"]');
            if (trigger) { trigger.click(); return 'clicked'; }
            comp.click();
            return 'clicked_comp';
        }
        return 'not_found';
    """)

    if 'clicked' not in str(opened):
        print(f"  [ERRO] Componente de playlist nao encontrado")
        return False

    time.sleep(3)

    # Scroll to load all playlists
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var ironList = dialog.querySelector('tp-yt-iron-list');
        if (ironList) {
            for (var s = 0; s <= ironList.scrollHeight; s += 32) { ironList.scrollTop = s; }
            ironList.scrollTop = 0;
        }
    """)
    time.sleep(1)

    # Try to select existing playlist
    result = driver.execute_script("""
        var target = arguments[0];
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return 'no_dialog';
        var labels = dialog.querySelectorAll('label');
        for (var l of labels) {
            if ((l.textContent || '').trim().includes(target)) {
                var cb = l.closest('ytcp-checkbox-group');
                if (cb) {
                    var div = cb.querySelector('div[role="checkbox"]');
                    if (div && div.getAttribute('aria-checked') === 'true') return 'already_checked';
                }
                l.click();
                return 'selected';
            }
        }
        return 'not_found';
    """, playlist_name)

    if result == 'not_found' and is_first:
        print(f"  [PLAYLIST] Criando '{playlist_name}'...")

        # Click new playlist dropdown
        driver.execute_script("""
            var dialog = document.querySelector('ytcp-playlist-dialog');
            if (!dialog) return;
            var dropBtn = dialog.querySelector('.new-playlist-button button');
            if (dropBtn) dropBtn.click();
        """)
        time.sleep(2)

        # Click "Nova playlist"
        driver.execute_script("""
            var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
            if (item) item.click();
        """)
        time.sleep(5)

        # Try to find and fill title with retries
        for retry in range(8):
            focused = driver.execute_script("""
                var pd = document.querySelector('ytcp-playlist-dialog');
                if (!pd) return 'no_pd';
                var selectors = [
                    '#create-playlist-form #textbox',
                    '#create-playlist-form div[contenteditable]',
                    'ytcp-playlist-creation #textbox',
                    'ytcp-playlist-creation div[contenteditable]',
                    'div[aria-label*="tulo"]',
                    'div[aria-label*="itle"]',
                    'div[aria-label*="Título"]',
                    'div[aria-label*="Title"]',
                    'div[aria-label*="playlist"]',
                    'ytcp-form-input-container div[contenteditable]',
                    '.input-container div[contenteditable]'
                ];
                for (var s of selectors) {
                    var el = pd.querySelector(s);
                    if (el && el.offsetParent !== null) {
                        el.focus(); el.click(); el.textContent = '';
                        return 'focused:' + s;
                    }
                }
                // Try any visible dialog
                var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
                for (var d of dialogs) {
                    if (d.offsetHeight > 50 && getComputedStyle(d).display !== 'none') {
                        var tb = d.querySelector('#textbox[contenteditable], div[contenteditable="true"], div[role="textbox"]');
                        if (tb && tb.offsetParent !== null) {
                            tb.focus(); tb.click(); tb.textContent = '';
                            return 'focused_dialog';
                        }
                    }
                }
                // Any #textbox inside playlist area
                var allTb = pd.querySelectorAll('#textbox, div[contenteditable="true"]');
                for (var el of allTb) {
                    if (el.offsetParent !== null && el.offsetHeight > 0 && el.offsetHeight < 100) {
                        el.focus(); el.click(); el.textContent = '';
                        return 'focused_last';
                    }
                }
                return 'not_found';
            """)
            print(f"  [RETRY {retry+1}/8] Focus: {focused}")
            if 'focused' in str(focused):
                break
            time.sleep(2)

        if 'focused' in str(focused):
            # Type playlist name
            driver.execute_script("""
                var el = document.activeElement;
                if (el && el.contentEditable === 'true') {
                    el.textContent = '';
                    el.innerText = arguments[0];
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                }
            """, playlist_name)
            try:
                active = driver.switch_to.active_element
                active.send_keys(Keys.END)
            except Exception:
                pass
            time.sleep(2)

            # Click "Criar"
            created = driver.execute_script("""
                var pd = document.querySelector('ytcp-playlist-dialog');
                if (!pd) return 'no_pd';
                var btns = pd.querySelectorAll('ytcp-button, button');
                for (var b of btns) {
                    var txt = (b.textContent || '').trim().toLowerCase();
                    if (txt === 'criar' || txt === 'create') {
                        if (!b.hasAttribute('disabled') && b.getAttribute('aria-disabled') !== 'true') {
                            b.click(); return 'created';
                        }
                        return 'disabled';
                    }
                }
                // Try in paper dialogs
                var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
                for (var d of dialogs) {
                    if (d.offsetHeight > 50 && getComputedStyle(d).display !== 'none') {
                        var btns2 = d.querySelectorAll('ytcp-button, button');
                        for (var b of btns2) {
                            var txt = (b.textContent || '').trim().toLowerCase();
                            if (txt === 'criar' || txt === 'create') {
                                if (!b.hasAttribute('disabled')) { b.click(); return 'created'; }
                            }
                        }
                    }
                }
                return 'no_btn';
            """)
            time.sleep(4)
            print(f"  [PLAYLIST] Create: {created}")
            result = 'created' if created == 'created' else 'failed'
        else:
            print(f"  [ERRO] Nao conseguiu focar no titulo da playlist")
            result = 'failed'

    print(f"  [PLAYLIST] Result: {result}")

    # Close playlist dialog
    time.sleep(1)
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (dialog) {
            var els = dialog.querySelectorAll('ytcp-button, button, div');
            for (var el of els) {
                var txt = (el.textContent || '').trim().toLowerCase();
                if (txt === 'concluir' || txt === 'done') { el.click(); return; }
            }
        }
    """)
    time.sleep(2)

    # Save
    save = driver.execute_script("""
        var btns = document.querySelectorAll('#save-button ytcp-button, #save-button button');
        for (var b of btns) {
            if (b.offsetParent !== null) {
                if (!b.hasAttribute('disabled') && b.getAttribute('aria-disabled') !== 'true') {
                    b.click(); return 'saved';
                }
                return 'no_changes';
            }
        }
        var allBtns = document.querySelectorAll('ytcp-button');
        for (var b of allBtns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if ((txt === 'salvar' || txt === 'save') && b.offsetParent !== null) {
                if (!b.hasAttribute('disabled')) { b.click(); return 'saved'; }
            }
        }
        return 'no_btn';
    """)
    print(f"  [SAVE] {save}")
    time.sleep(3)
    return result in ('selected', 'already_checked', 'created')


def main():
    print("=" * 60)
    print("  FIX RAIA PLAYLIST - Adicionar 29 videos")
    print("=" * 60)

    with open("fix_old_uploads.json", "r", encoding="utf-8") as f:
        fixes = json.load(f)

    playlist_name = "Portfolio - Raia"
    videos = [f for f in fixes if f["playlist"] == playlist_name]
    print(f"\n[INFO] {len(videos)} videos para adicionar a '{playlist_name}'")

    input("\nPressione ENTER para iniciar...")

    driver = start_chrome()
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    try:
        channel = driver.execute_script("""
            var el = document.querySelector('#channel-title, .channel-name');
            return el ? el.textContent.trim() : null;
        """)
        if channel:
            print(f"[CANAL] {channel}")
    except Exception:
        pass

    print("[OK] YouTube Studio carregado!\n")

    success = 0
    for i, v in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] {v['id']}")
        ok = add_video_to_playlist(driver, v["id"], playlist_name, is_first=(i == 1))
        if ok:
            success += 1
        time.sleep(2)

    print(f"\n{'=' * 60}")
    print(f"  CONCLUIDO! {success}/{len(videos)} videos adicionados a playlist")
    print(f"{'=' * 60}")
    driver.quit()


if __name__ == "__main__":
    main()
