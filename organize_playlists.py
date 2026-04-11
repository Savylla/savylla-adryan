"""
Organiza videos ja enviados em playlists por cliente no YouTube Studio.
Usa Selenium + _needs_playlist.json (26 Drogasil + 46 Raia).
Seletores baseados na estrutura real do YouTube Studio.

Estrutura do dialog de playlists:
  ytcp-playlist-dialog
    ytcp-checkbox-group (1 por playlist)
      label.ytcp-checkbox-label
        ytcp-checkbox-lit
          div[role="checkbox"][aria-checked="true/false"]
        span.checkbox-label  (texto: "Portfolio - Drogasil")

  Botao save: ytcp-button#save (NAO #save-button)
"""

import json
import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

NEEDS_PLAYLIST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_needs_playlist.json")
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "playlist_organize_progress.json")

PLAYLIST_NAMES = {
    "Drogasil": "Portfolio - Drogasil",
    "Raia": "Portfolio - Raia",
}


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"done": [], "failed": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


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


def setup_driver():
    """Kill Chrome, start manually with user profile, connect via debugger (same as uploader)."""
    chrome_path = find_chrome()
    if not chrome_path:
        raise RuntimeError("Chrome nao encontrado!")

    # Use same data dir as the uploader (home dir - has YouTube login cookies)
    custom_data_dir = os.path.join(os.path.expanduser("~"), "chrome_selenium_data")
    os.makedirs(custom_data_dir, exist_ok=True)

    print("[BROWSER] Fechando Chrome existente...")
    subprocess.Popen(['taskkill', '/F', '/IM', 'chrome.exe'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.Popen(['taskkill', '/F', '/IM', 'chromedriver.exe'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)

    for f in ['SingletonLock', 'SingletonSocket', 'SingletonCookie']:
        try:
            os.remove(os.path.join(custom_data_dir, f))
        except Exception:
            pass

    # Start Chrome manually (same approach as youtube_compilation_uploader.py)
    chrome_cmd = [
        chrome_path,
        f"--remote-debugging-port={CHROME_DEBUG_PORT}",
        f"--user-data-dir={custom_data_dir}",
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
        "--log-level=3",
    ]
    print(f"[BROWSER] Iniciando Chrome (porta {CHROME_DEBUG_PORT})...")
    subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10)

    # Connect Selenium to the already-running Chrome
    opts = Options()
    opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")

    driver = None
    for attempt in range(5):
        try:
            driver = webdriver.Chrome(options=opts)
            try:
                driver.maximize_window()
            except Exception:
                pass
            break
        except Exception as e:
            if attempt < 4:
                print(f"  [RETRY] Tentativa {attempt + 1}/5 - aguardando Chrome...")
                time.sleep(5)
            else:
                raise e

    return driver


def wait_for_login(driver):
    """Navigate to Studio and wait for login if needed."""
    driver.get('https://studio.youtube.com')
    time.sleep(5)

    if 'accounts.google' in driver.current_url:
        print('[LOGIN] Faca login no Chrome! (max 5 min)')
        for _ in range(150):
            time.sleep(2)
            try:
                if 'studio.youtube.com' in driver.current_url and 'accounts.google' not in driver.current_url:
                    print('[OK] Login detectado!')
                    break
            except Exception:
                pass
        time.sleep(3)

    if 'studio.youtube.com' not in driver.current_url or 'accounts.google' in driver.current_url:
        print('[ERRO] Login falhou.')
        driver.quit()
        exit(1)

    print(f'[OK] Studio carregado: {driver.current_url}')


def create_playlist_in_dialog(driver, playlist_name):
    """Create a new playlist via ytcp-playlist-creation-dialog.

    Flow:
    1. Click dropdown button (.new-playlist-button)
    2. Click menu item (test-id="new_playlist")
    3. A separate creation dialog opens with contenteditable divs
    4. Type name in div[aria-label*="título"]
    5. Click "Criar"
    """
    print(f'    Criando playlist "{playlist_name}"...')

    # Step 1: Click dropdown button
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var dropBtn = dialog.querySelector('.new-playlist-button button');
        if (dropBtn) dropBtn.click();
    """)
    time.sleep(2)

    # Step 2: Click "Nova playlist" menu item
    clicked_item = driver.execute_script("""
        var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
        if (item) { item.click(); return 'clicked'; }
        // Fallback: look for any menu item with "nova playlist" / "new playlist" text
        var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], [role="option"]');
        for (var i of items) {
            var txt = (i.textContent || '').toLowerCase();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                i.click();
                return 'clicked_fallback';
            }
        }
        return 'not_found';
    """)
    print(f'    Menu item: {clicked_item}')
    if clicked_item == 'not_found':
        return False

    time.sleep(5)

    # Step 3: Find the creation form and focus the title textbox
    focused = driver.execute_script("""
        // Search in ytcp-playlist-dialog first (primary), then tp-yt-paper-dialog (fallback)
        var containers = [];
        var pd = document.querySelector('ytcp-playlist-dialog');
        if (pd) containers.push(pd);
        var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
        for (var d of dialogs) {
            if (d.offsetHeight > 50 && getComputedStyle(d).display !== 'none') {
                containers.push(d);
            }
        }
        for (var d of containers) {
            var selectors = [
                '#create-playlist-form #textbox',
                '#create-playlist-form div[contenteditable]',
                'ytcp-playlist-creation div[contenteditable]',
                'ytcp-playlist-creation #textbox',
                'div[aria-label*="tulo"]',
                'div[aria-label*="itle"]',
                'div[aria-label*="playlist"]',
                'ytcp-form-input-container div[contenteditable]',
                '.input-container div[contenteditable]',
                'div[contenteditable]',
                'div[role="textbox"]'
            ];
            for (var sel of selectors) {
                var el = d.querySelector(sel);
                if (el && el.offsetParent !== null) {
                    el.focus();
                    el.click();
                    el.textContent = '';
                    return 'focused:' + sel;
                }
            }
        }
        return 'no_creation_dialog';
    """)
    print(f'    Title focus: {focused}')

    if 'focused' not in str(focused):
        return False

    # Step 4: Type playlist name via keyboard
    time.sleep(0.5)
    active = driver.switch_to.active_element
    active.send_keys(Keys.CONTROL + "a")
    active.send_keys(Keys.DELETE)
    active.send_keys(playlist_name)
    print(f'    Typed: "{playlist_name}"')
    time.sleep(2)

    # Step 5: Click "Criar" in the creation dialog
    created = driver.execute_script("""
        // Search in ytcp-playlist-dialog first (primary), then tp-yt-paper-dialog (fallback)
        var containers = [];
        var pd = document.querySelector('ytcp-playlist-dialog');
        if (pd) containers.push(pd);
        var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
        for (var d of dialogs) {
            if (d.offsetHeight > 50 && getComputedStyle(d).display !== 'none') {
                containers.push(d);
            }
        }
        for (var d of containers) {
            var btns = d.querySelectorAll('ytcp-button, button, #create-playlist-button');
            for (var b of btns) {
                var txt = (b.textContent || '').trim().toLowerCase();
                if (txt === 'criar' || txt === 'create') {
                    var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                    if (!disabled) { b.click(); return 'created'; }
                    return 'criar_disabled';
                }
            }
        }
        return 'no_criar_btn';
    """)
    print(f'    Create: {created}')
    time.sleep(5)

    return created == 'created'


def add_video_to_playlist(driver, video_id, playlist_name, progress):
    """Navigate to video edit page and add it to the correct playlist."""

    if video_id in progress["done"]:
        print(f'  [SKIP] {video_id} - ja feito')
        return True

    url = f'https://studio.youtube.com/video/{video_id}/edit'
    print(f'\n  Abrindo {url}')
    driver.get(url)
    time.sleep(6)

    # Check page loaded
    page_ok = driver.execute_script("""
        return document.querySelector('ytcp-video-metadata-playlists') !== null;
    """)
    if not page_ok:
        driver.execute_script('window.scrollTo(0, 500)')
        time.sleep(2)
        page_ok = driver.execute_script("""
            return document.querySelector('ytcp-video-metadata-playlists') !== null;
        """)
    if not page_ok:
        print(f'  [SKIP] Pagina nao carregou')
        progress["failed"].append({"id": video_id, "error": "page_not_loaded"})
        save_progress(progress)
        return False

    # Check if already in playlist
    already = driver.execute_script("""
        var comp = document.querySelector('ytcp-video-metadata-playlists');
        if (comp) {
            var txt = comp.textContent || '';
            return txt.includes(arguments[0]);
        }
        return false;
    """, playlist_name)
    if already:
        print(f'  [OK] Ja esta na playlist')
        progress["done"].append(video_id)
        save_progress(progress)
        return True

    # Open playlist dialog
    driver.execute_script("""
        var comp = document.querySelector('ytcp-video-metadata-playlists');
        if (comp) {
            var trigger = comp.querySelector('ytcp-text-dropdown-trigger, [role="button"]');
            if (trigger) trigger.click();
            else comp.click();
        }
    """)
    time.sleep(3)

    # Scroll iron-list to load all playlists (virtual scrolling only renders visible items)
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var ironList = dialog.querySelector('tp-yt-iron-list');
        if (ironList) {
            // Scroll to bottom to force rendering all items
            ironList.scrollTop = ironList.scrollHeight;
        }
    """)
    time.sleep(1)
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var ironList = dialog.querySelector('tp-yt-iron-list');
        if (ironList) {
            // Scroll back to top
            ironList.scrollTop = 0;
        }
    """)
    time.sleep(1)

    # Try to select existing playlist
    selected = driver.execute_script("""
        var targetName = arguments[0];
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return 'no_dialog';

        // First, try scrolling through iron-list to find the playlist
        var ironList = dialog.querySelector('tp-yt-iron-list');
        if (ironList) {
            // Scroll incrementally to render all items
            for (var scrollPos = 0; scrollPos <= ironList.scrollHeight; scrollPos += 32) {
                ironList.scrollTop = scrollPos;
            }
            ironList.scrollTop = 0; // Reset
        }

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
    print(f'    Select: {selected}')

    # Verify checkbox
    if 'clicked' in selected:
        time.sleep(1)
        verify = driver.execute_script("""
            var targetName = arguments[0];
            var dialog = document.querySelector('ytcp-playlist-dialog');
            if (!dialog) return 'no_dialog';
            var groups = dialog.querySelectorAll('ytcp-checkbox-group');
            for (var group of groups) {
                var nameSpan = group.querySelector('span.checkbox-label, span.label');
                var txt = nameSpan ? nameSpan.textContent.trim() : '';
                if (txt.includes(targetName)) {
                    var cbDiv = group.querySelector('div[role="checkbox"]');
                    var checked = cbDiv ? cbDiv.getAttribute('aria-checked') : 'no_div';
                    return 'aria-checked=' + checked;
                }
            }
            return 'playlist_not_found';
        """, playlist_name)
        print(f'    Verify: {verify}')

    # If playlist not found, create it
    if selected == 'not_found':
        created = create_playlist_in_dialog(driver, playlist_name)
        if not created:
            # Close dialog and skip
            driver.execute_script("""
                var dialog = document.querySelector('ytcp-playlist-dialog');
                if (dialog) {
                    var btns = dialog.querySelectorAll('ytcp-button, button');
                    for (var b of btns) {
                        var txt = (b.textContent || '').trim().toLowerCase();
                        if (txt === 'concluir' || txt === 'done' || txt === 'cancelar' || txt === 'cancel') {
                            b.click(); return;
                        }
                    }
                }
            """)
            time.sleep(1)
            progress["failed"].append({"id": video_id, "error": "create_playlist_failed"})
            save_progress(progress)
            return False

    # Close playlist dialog - "Concluir" / "Done"
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var allElements = dialog.querySelectorAll('ytcp-button, button, div');
        for (var el of allElements) {
            var txt = (el.textContent || '').trim().toLowerCase();
            if (txt === 'concluir' || txt === 'done') {
                el.click();
                return;
            }
        }
    """)
    time.sleep(2)

    # Save - correct selector: #save (not #save-button)
    saved = 'no_change'
    for attempt in range(3):
        saved = driver.execute_script("""
            var saveBtn = document.querySelector('ytcp-button#save');
            if (!saveBtn) saveBtn = document.querySelector('#save');
            if (!saveBtn) saveBtn = document.querySelector('#save-button');

            if (!saveBtn) {
                var btns = document.querySelectorAll('ytcp-button');
                for (var b of btns) {
                    var txt = (b.textContent || '').trim().toLowerCase();
                    if (txt === 'salvar' || txt === 'save') {
                        saveBtn = b; break;
                    }
                }
            }

            if (!saveBtn) return 'no_save_btn';

            var disabled = saveBtn.hasAttribute('disabled');
            var ariaDisabled = saveBtn.getAttribute('aria-disabled');

            if (!disabled && ariaDisabled !== 'true') {
                saveBtn.click();
                return 'saved';
            }
            return 'disabled|aria=' + ariaDisabled;
        """)
        print(f'    Save [{attempt+1}]: {saved}')
        if saved == 'saved':
            break
        time.sleep(2)

    time.sleep(3)

    if saved == 'saved' or selected == 'already_checked':
        progress["done"].append(video_id)
        save_progress(progress)
        return True
    else:
        progress["failed"].append({"id": video_id, "error": f"save={saved}, select={selected}"})
        save_progress(progress)
        return False


def main():
    with open(NEEDS_PLAYLIST_FILE, "r", encoding="utf-8") as f:
        needs_playlist = json.load(f)

    progress = load_progress()

    total = sum(len(v) for v in needs_playlist.values())
    done_count = len(progress["done"])
    print(f"Total: {total} videos | Ja feitos: {done_count} | Restantes: {total - done_count}")

    if total - done_count == 0:
        print("Todos os videos ja foram organizados!")
        return

    driver = setup_driver()
    wait_for_login(driver)

    success = 0
    errors = 0

    for client, video_ids in needs_playlist.items():
        playlist_name = PLAYLIST_NAMES.get(client, f"Portfolio - {client}")
        remaining = [v for v in video_ids if v not in progress["done"]]

        if not remaining:
            print(f'\n=== {client}: Todos {len(video_ids)} videos ja feitos ===')
            continue

        print(f'\n{"="*60}')
        print(f'  {playlist_name} ({len(remaining)} videos restantes)')
        print(f'{"="*60}')

        for i, video_id in enumerate(remaining):
            print(f'\n[{i+1}/{len(remaining)}] {video_id}')
            result = add_video_to_playlist(driver, video_id, playlist_name, progress)

            if result:
                success += 1
            else:
                errors += 1

            time.sleep(1)

    print(f'\n{"="*60}')
    print(f'  CONCLUIDO!')
    print(f'  Sucesso: {success}')
    print(f'  Falhas: {errors}')
    print(f'  Total no progresso: {len(progress["done"])} feitos')
    print(f'{"="*60}')

    driver.quit()


if __name__ == "__main__":
    main()
