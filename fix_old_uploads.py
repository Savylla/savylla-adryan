#!/usr/bin/env python3
"""
Fix videos uploaded in the previous session with broken title/description/playlist.
Uses same Selenium/Chrome approach as the main uploader.
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
FIX_DATA_FILE = "fix_old_uploads.json"

def start_chrome(port=9556):
    """Start Chrome with user profile on a different port than the uploader."""
    # Kill any Chrome on this port first
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True, timeout=5)
        time.sleep(2)
    except Exception:
        pass

    options = Options()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE}")
    options.add_argument("--profile-directory=Savylla Adryan")
    options.add_argument(f"--remote-debugging-port={port}")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def fix_video_title_desc(driver, video_id, title, description):
    """Navigate to video edit page and fix title + description."""
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(5)

    # Wait for edit page to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#textbox[contenteditable='true']"))
        )
    except Exception:
        print(f"  [ERRO] Pagina de edicao nao carregou para {video_id}")
        return False

    textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox[contenteditable='true']")
    if not textboxes:
        textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox")

    if not textboxes:
        print(f"  [ERRO] Nenhum campo de texto encontrado")
        return False

    # Fix title
    title_box = textboxes[0]
    driver.execute_script("""
        var el = arguments[0];
        var title = arguments[1];
        el.focus();
        el.click();
        // Select all and clear
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        // Type new title
        document.execCommand('insertText', false, title);
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
    """, title_box, title[:100])
    time.sleep(1)
    print(f"  [OK] Titulo: {title[:60]}...")

    # Fix description
    if len(textboxes) > 1:
        desc_box = textboxes[1]
        driver.execute_script("""
            var el = arguments[0];
            var desc = arguments[1];
            el.focus();
            el.click();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, desc);
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, desc_box, description)
        time.sleep(1)
        print(f"  [OK] Descricao atualizada")

    # Click Save button
    time.sleep(2)
    save_result = driver.execute_script("""
        var btns = document.querySelectorAll('#save-button ytcp-button, #save-button button, button#save');
        for (var b of btns) {
            if (b.offsetParent !== null) {
                var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                if (!disabled) {
                    b.click();
                    return 'saved';
                }
                return 'disabled';
            }
        }
        // Fallback: any visible save button
        var allBtns = document.querySelectorAll('ytcp-button');
        for (var b of allBtns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if ((txt === 'salvar' || txt === 'save') && b.offsetParent !== null) {
                var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                if (!disabled) {
                    b.click();
                    return 'saved_fallback';
                }
            }
        }
        return 'no_save_btn';
    """)
    print(f"  [SAVE] {save_result}")
    time.sleep(3)

    return save_result in ('saved', 'saved_fallback')


def add_to_playlist(driver, video_id, playlist_name):
    """Add video to playlist from the edit page."""
    # Make sure we're on the edit page
    if f"/video/{video_id}/edit" not in driver.current_url:
        driver.get(f"https://studio.youtube.com/video/{video_id}/edit")
        time.sleep(5)

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
        print(f"  [PLAYLIST] Nao encontrou componente de playlist")
        return False

    time.sleep(3)

    # Scroll iron-list to load all playlists
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var ironList = dialog.querySelector('tp-yt-iron-list');
        if (ironList) {
            for (var scrollPos = 0; scrollPos <= ironList.scrollHeight; scrollPos += 32) {
                ironList.scrollTop = scrollPos;
            }
            ironList.scrollTop = 0;
        }
    """)
    time.sleep(1)

    # Try to select existing playlist
    playlist_result = driver.execute_script("""
        var targetName = arguments[0];
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return 'no_dialog';

        var groups = dialog.querySelectorAll('ytcp-checkbox-group');
        for (var group of groups) {
            var nameSpan = group.querySelector('span.checkbox-label, span.label, span.label-text');
            var txt = nameSpan ? nameSpan.textContent.trim() : '';
            if (!txt) {
                var lbl = group.querySelector('label');
                txt = lbl ? lbl.textContent.trim() : '';
            }

            if (txt.includes(targetName)) {
                var cbDiv = group.querySelector('div[role="checkbox"]');
                var isChecked = cbDiv && cbDiv.getAttribute('aria-checked') === 'true';
                if (isChecked) return 'already_checked';

                var label = group.querySelector('label.ytcp-checkbox-label, label');
                if (label) { label.click(); return 'clicked_label'; }
                group.click();
                return 'clicked_group';
            }
        }

        // Fallback: search all labels
        var labels = dialog.querySelectorAll('label.ytcp-checkbox-label');
        for (var label of labels) {
            var txt = (label.textContent || '').trim();
            if (txt.includes(targetName)) {
                label.click();
                return 'clicked_fallback_label';
            }
        }

        return 'not_found';
    """, playlist_name)

    print(f"  [PLAYLIST] Select: {playlist_result}")

    # If not found, create it
    if playlist_result == 'not_found':
        print(f"  [PLAYLIST] Criando '{playlist_name}'...")

        # Click dropdown button
        driver.execute_script("""
            var dialog = document.querySelector('ytcp-playlist-dialog');
            if (!dialog) return;
            var dropBtn = dialog.querySelector('.new-playlist-button button');
            if (dropBtn) dropBtn.click();
        """)
        time.sleep(2)

        # Click "Nova playlist" menu item
        clicked_item = driver.execute_script("""
            var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
            if (item) { item.click(); return 'clicked'; }
            return 'not_found';
        """)
        time.sleep(4)

        if clicked_item == 'clicked':
            # Focus title textbox
            focused = driver.execute_script("""
                var playlistDialog = document.querySelector('ytcp-playlist-dialog');
                if (playlistDialog) {
                    var titleBox = playlistDialog.querySelector('#create-playlist-form #textbox, #create-playlist-form div[contenteditable]');
                    if (!titleBox) {
                        titleBox = playlistDialog.querySelector('div[aria-label*="tulo"], div[aria-label*="itle"], div[aria-label*="Título"], div[aria-label*="Title"]');
                    }
                    if (!titleBox) {
                        titleBox = playlistDialog.querySelector('.input-container div[contenteditable], ytcp-form-input-container div[contenteditable]');
                    }
                    if (titleBox) {
                        titleBox.focus();
                        titleBox.click();
                        titleBox.textContent = '';
                        return 'focused';
                    }
                }
                var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
                for (var d of dialogs) {
                    if (d.offsetHeight > 50 && getComputedStyle(d).display !== 'none') {
                        var titleBox = d.querySelector('div[aria-label*="tulo"], div[aria-label*="itle"]');
                        if (!titleBox) {
                            titleBox = d.querySelector('#textbox[contenteditable], div[contenteditable="true"], div[role="textbox"]');
                        }
                        if (titleBox) {
                            titleBox.focus();
                            titleBox.click();
                            titleBox.textContent = '';
                            return 'focused';
                        }
                    }
                }
                return 'no_creation_dialog';
            """)

            if focused in ('focused', 'focused_fallback'):
                # Type playlist name via JS
                time.sleep(0.5)
                driver.execute_script("""
                    var el = document.activeElement;
                    if (el && el.contentEditable === 'true') {
                        el.textContent = '';
                        el.innerText = arguments[0];
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                        el.dispatchEvent(new Event('change', {bubbles: true}));
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
                    var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
                    for (var d of dialogs) {
                        if (d.offsetHeight > 50 && getComputedStyle(d).display !== 'none') {
                            var btns = d.querySelectorAll('ytcp-button, button');
                            for (var b of btns) {
                                var txt = (b.textContent || '').trim().toLowerCase();
                                if (txt === 'criar' || txt === 'create') {
                                    var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                                    if (!disabled) { b.click(); return 'created'; }
                                    return 'criar_disabled';
                                }
                            }
                        }
                    }
                    return 'no_dialog';
                """)
                time.sleep(3)
                print(f"  [PLAYLIST] Create: {created}")
            else:
                print(f"  [PLAYLIST] Nao focou no titulo: {focused}")

    elif 'clicked' in str(playlist_result):
        print(f"  [OK] Playlist selecionada: {playlist_name}")
    elif playlist_result == 'already_checked':
        print(f"  [OK] Playlist ja marcada: {playlist_name}")

    # Close playlist dialog - "Concluir" / "Done"
    time.sleep(2)
    close_result = driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (dialog) {
            var allElements = dialog.querySelectorAll('ytcp-button, button, div');
            for (var el of allElements) {
                var txt = (el.textContent || '').trim().toLowerCase();
                if (txt === 'concluir' || txt === 'done') {
                    el.click();
                    return 'closed: ' + txt;
                }
            }
        }
        return 'no_close_btn';
    """)
    print(f"  [PLAYLIST] Dialog: {close_result}")
    time.sleep(2)

    # Save changes
    save_result = driver.execute_script("""
        var btns = document.querySelectorAll('#save-button ytcp-button, #save-button button');
        for (var b of btns) {
            if (b.offsetParent !== null) {
                var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                if (!disabled) {
                    b.click();
                    return 'saved';
                }
                return 'no_changes';
            }
        }
        return 'no_save_btn';
    """)
    print(f"  [SAVE] {save_result}")
    time.sleep(3)

    return True


def main():
    print("=" * 60)
    print("  FIX OLD UPLOADS - Corrigir titulo/desc/playlist")
    print("=" * 60)
    print()
    print("  IMPORTANTE: Feche TODAS as janelas do Chrome antes!")
    print()

    # Load fix data
    if not os.path.exists(FIX_DATA_FILE):
        print(f"[ERRO] Arquivo {FIX_DATA_FILE} nao encontrado!")
        return

    with open(FIX_DATA_FILE, "r", encoding="utf-8") as f:
        fixes = json.load(f)

    print(f"[INFO] {len(fixes)} videos para corrigir\n")

    input("Pressione ENTER para iniciar (Chrome vai abrir)...")

    driver = start_chrome()

    # Navigate to YouTube Studio
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    # Verify login
    try:
        channel = driver.execute_script("""
            var el = document.querySelector('#channel-title, .channel-name, ytcp-channel-selector');
            return el ? el.textContent.trim() : null;
        """)
        if channel:
            print(f"[CANAL] Nome: {channel}")
    except Exception:
        pass

    print("[OK] YouTube Studio carregado!\n")

    for i, fix in enumerate(fixes, 1):
        vid = fix["id"]
        title = fix["title"]
        desc = fix["desc"]
        playlist = fix["playlist"]

        print(f"\n[{i}/{len(fixes)}] Corrigindo {vid}")
        print(f"  Titulo: {title[:60]}...")
        print(f"  Playlist: {playlist}")

        # Fix title and description
        success = fix_video_title_desc(driver, vid, title, desc)
        if not success:
            print(f"  [AVISO] Falha ao salvar titulo/desc - tentando playlist mesmo assim")

        time.sleep(3)

        # Add to playlist
        add_to_playlist(driver, vid, playlist)

        time.sleep(3)
        print(f"  [DONE] Video {vid} corrigido!")

    print(f"\n{'=' * 60}")
    print(f"  CONCLUIDO! {len(fixes)} videos corrigidos.")
    print(f"{'=' * 60}")

    driver.quit()


if __name__ == "__main__":
    main()
