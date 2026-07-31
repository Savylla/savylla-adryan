"""
=============================================================
FIX PLAYLISTS - Organiza videos sem playlist
=============================================================
Lê youtube_results.json e adiciona cada video à playlist
correta ("Portfolio - {Cliente}") via YouTube Studio.

USO: python fix_playlists.py
=============================================================
"""

import json
import os
import sys
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Force flush on every print for real-time output in background mode
import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

RESULTS_FILE = "youtube_results.json"
PROGRESS_FILE = "fix_playlists_progress.json"
CHROME_DEBUG_PORT = 9555

# Clientes que JA tinham playlist (enviados em sessoes anteriores)
SKIP_CLIENTS = [
    'Devassas', 'Força da Terra', 'Projetos IA', 'Allfluence',
    'Drogasil', 'Raia', 'Philips', 'Intimus', 'Veloe', 'Garagem Coletiva'
]


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


def create_driver():
    chrome_path = find_chrome()
    if not chrome_path:
        raise RuntimeError("Chrome nao encontrado!")

    custom_data_dir = os.path.join(os.path.expanduser("~"), "chrome_selenium_data")
    os.makedirs(custom_data_dir, exist_ok=True)

    print("[BROWSER] Fechando Chrome existente...")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"],
                       capture_output=True, timeout=10)
        time.sleep(3)
    except Exception:
        pass

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

    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")

    driver = None
    for attempt in range(5):
        try:
            driver = webdriver.Chrome(options=options)
            try:
                driver.maximize_window()
            except Exception:
                pass
            break
        except Exception as e:
            if attempt < 4:
                print(f"  [RETRY] Tentativa {attempt + 1}/5...")
                time.sleep(5)
            else:
                raise e

    return driver


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"fixed": []}


def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def add_video_to_playlist(driver, video_id, playlist_name):
    """Navigate to video edit page and add it to the correct playlist."""

    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(5)

    # Wait for page to load
    for _ in range(10):
        ready = driver.execute_script("""
            return document.querySelector('ytcp-video-metadata-editor') !== null
                || document.querySelector('#details') !== null
                || document.querySelector('ytcp-mention-textbox') !== null;
        """)
        if ready:
            break
        time.sleep(2)

    # Check if page loaded
    title_check = driver.execute_script("""
        var t = document.querySelector('ytcp-mention-textbox #textbox, #title-textarea #textbox');
        return t ? t.textContent.trim().substring(0, 30) : 'not_found';
    """)
    if title_check == 'not_found':
        return 'page_not_loaded'

    # Click "Show more" / "Mostrar mais" to expand all fields if needed
    driver.execute_script("""
        var btns = document.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt.includes('mostrar mais') || txt.includes('show more')) {
                b.click();
                break;
            }
        }
    """)
    time.sleep(2)

    # Find and click the playlist section - use the inner trigger, not the wrapper
    opened = driver.execute_script("""
        // Best: click the dropdown trigger with aria-label "Selecionar playlists"
        var trigger = document.querySelector('ytcp-dropdown-trigger[aria-label*="playlist"], ytcp-dropdown-trigger[aria-label*="Playlist"]');
        if (trigger && trigger.offsetParent !== null) {
            trigger.click();
            return 'clicked_aria_trigger';
        }

        // Fallback: find trigger inside ytcp-video-metadata-playlists
        var vmp = document.querySelector('ytcp-video-metadata-playlists');
        if (vmp) {
            var inner = vmp.querySelector('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, button');
            if (inner) { inner.click(); return 'clicked_vmp_inner'; }
            vmp.click();
            return 'clicked_vmp';
        }

        // Last fallback: any dropdown trigger with playlist-related aria
        var triggers = document.querySelectorAll('ytcp-text-dropdown-trigger, ytcp-dropdown-trigger');
        for (var t of triggers) {
            var aria = (t.getAttribute('aria-label') || '').toLowerCase();
            if (aria.includes('playlist')) {
                t.click();
                return 'clicked_trigger_fallback';
            }
        }
        return 'not_found';
    """)

    if 'not_found' in str(opened):
        return 'no_playlist_selector'

    time.sleep(3)

    # Wait for playlist dialog to appear (check innerHTML, not height - dialog uses flex layout)
    dialog_ready = False
    for wait_try in range(8):
        dialog_ready = driver.execute_script("""
            var dialog = document.querySelector('ytcp-playlist-dialog');
            if (!dialog) return false;
            return dialog.innerHTML.length > 100;
        """)
        if dialog_ready:
            break
        time.sleep(1)

    if not dialog_ready:
        return 'no_dialog'

    # Scroll the playlist list to load all items
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

    # Try to find and check the playlist
    select_result = driver.execute_script("""
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
                if (label) { label.click(); return 'checked'; }
                group.click();
                return 'checked_group';
            }
        }

        // Fallback: search all labels
        var labels = dialog.querySelectorAll('label.ytcp-checkbox-label');
        for (var label of labels) {
            var txt = (label.textContent || '').trim();
            if (txt.includes(targetName)) {
                label.click();
                return 'checked_fallback';
            }
        }

        return 'not_found';
    """, playlist_name)

    if select_result == 'already_checked':
        # Close dialog and return
        close_playlist_dialog(driver)
        return 'already_in_playlist'

    if 'checked' in str(select_result):
        # Playlist found and checked - close dialog
        time.sleep(1)
        close_playlist_dialog(driver)
        time.sleep(1)
        # Save changes
        save_video(driver)
        return 'added_existing'

    # Playlist not found - need to create it
    if select_result == 'not_found':
        create_result = create_playlist_in_dialog(driver, playlist_name)
        if create_result == 'created':
            time.sleep(2)
            close_playlist_dialog(driver)
            time.sleep(1)
            save_video(driver)
            return 'created_and_added'
        else:
            close_playlist_dialog(driver)
            return f'create_failed:{create_result}'

    close_playlist_dialog(driver)
    return f'unexpected:{select_result}'


def create_playlist_in_dialog(driver, playlist_name):
    """Create a new playlist. YouTube Studio now opens ytcp-playlist-creation-dialog (separate dialog)."""

    # Step 1: Click "Nova playlist" button
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var dropBtn = dialog.querySelector('.new-playlist-button button, #new-playlist-button button');
        if (dropBtn) { dropBtn.click(); return; }
        var btns = dialog.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').toLowerCase();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) { b.click(); return; }
        }
    """)
    time.sleep(2)

    # Step 2: Click menu item
    clicked_item = driver.execute_script("""
        var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
        if (item) { item.click(); return 'clicked'; }
        var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], [role="option"]');
        for (var i of items) {
            var txt = (i.textContent || '').toLowerCase();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                i.click(); return 'clicked_fallback';
            }
        }
        return 'not_found';
    """)
    time.sleep(8)

    if clicked_item not in ('clicked', 'clicked_fallback'):
        return 'no_nova_playlist'

    # Step 3: Find title textbox in the NEW creation dialog (ytcp-playlist-creation-dialog)
    focused = 'no_creation_dialog'
    for retry in range(10):
        focused = driver.execute_script("""
            // PRIMARY: ytcp-playlist-creation-dialog (new YouTube Studio UI)
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            if (cd) {
                var tb = cd.querySelector('#textbox[contenteditable], div[contenteditable="true"]');
                if (tb && tb.offsetParent !== null && tb.offsetHeight > 0 && tb.offsetHeight < 60) {
                    tb.focus(); tb.click(); tb.textContent = '';
                    return 'focused_creation_dialog';
                }
            }
            // FALLBACK: find dialog with "Criar uma nova playlist"
            var allDialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog');
            for (var d of allDialogs) {
                var txt = (d.textContent || '').toLowerCase();
                if ((txt.includes('criar uma nova playlist') || txt.includes('create a new playlist'))
                    && d.offsetHeight > 100) {
                    var tb = d.querySelector('#textbox[contenteditable], div[contenteditable="true"]');
                    if (tb && tb.offsetParent !== null && tb.offsetHeight > 0 && tb.offsetHeight < 60) {
                        tb.focus(); tb.click(); tb.textContent = '';
                        return 'focused_new_dialog';
                    }
                }
            }
            return 'no_creation_dialog';
        """)
        if 'focused' in str(focused):
            break
        time.sleep(2)

    if 'focused' not in str(focused):
        return 'no_textbox'

    # Step 4: Type playlist name
    time.sleep(0.5)
    try:
        active = driver.switch_to.active_element
        active.send_keys(playlist_name)
    except Exception:
        pass
    time.sleep(0.5)
    driver.execute_script("""
        var el = document.activeElement;
        if (el && (el.contentEditable === 'true' || el.contentEditable === '')) {
            var current = (el.textContent || '').trim();
            if (!current) {
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, arguments[0]);
            }
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        }
    """, playlist_name)
    time.sleep(2)

    # Step 4b: Set visibility to unlisted (in creation dialog)
    driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        var containers = [];
        if (cd) containers.push(cd);
        var allDialogs = document.querySelectorAll('tp-yt-paper-dialog');
        for (var d of allDialogs) {
            if (d.offsetHeight > 100 && (d.textContent || '').toLowerCase().includes('criar uma nova')) containers.push(d);
        }
        for (var d of containers) {
            var dds = d.querySelectorAll('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger');
            for (var dd of dds) {
                var txt = (dd.textContent || '').toLowerCase();
                if (txt.includes('visibilidade') || txt.includes('visibility') || txt.includes('pública') || txt.includes('public')) {
                    dd.click(); return 'opened';
                }
            }
        }
        return 'no_dropdown';
    """)
    time.sleep(3)
    driver.execute_script("""
        var items = document.querySelectorAll('tp-yt-paper-item, [role="option"], [role="menuitem"]');
        for (var item of items) {
            var txt = (item.textContent || '').toLowerCase();
            if (txt.includes('unlisted') || txt.includes('não listada') || txt.includes('nao listada')) {
                item.click(); return 'set';
            }
        }
        return 'not_found';
    """)
    time.sleep(2)

    # Step 5: Click "Criar" (with retry)
    for criar_retry in range(5):
        created = driver.execute_script("""
            var containers = [];
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            if (cd) containers.push(cd);
            var allDialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog');
            for (var d of allDialogs) { if (d.offsetHeight > 100) containers.push(d); }
            for (var d of containers) {
                var btns = d.querySelectorAll('#create-button, ytcp-button, button');
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
        if created == 'created':
            return 'created'
        if created == 'criar_disabled':
            driver.execute_script("""
                var cd = document.querySelector('ytcp-playlist-creation-dialog');
                if (!cd) return;
                var tb = cd.querySelector('#textbox[contenteditable], div[contenteditable="true"]');
                if (tb) {
                    tb.focus();
                    tb.dispatchEvent(new Event('input', {bubbles: true}));
                    tb.dispatchEvent(new InputEvent('input', {bubbles: true, data: ' ', inputType: 'insertText'}));
                }
            """)
            time.sleep(2)
        else:
            break

    return created


def close_playlist_dialog(driver):
    """Close the playlist dialog by clicking Concluir/Done."""
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (dialog) {
            var allElements = dialog.querySelectorAll('ytcp-button, button, div');
            for (var el of allElements) {
                var txt = (el.textContent || '').trim().toLowerCase();
                if (txt === 'concluir' || txt === 'done') {
                    el.click();
                    return;
                }
            }
        }
        var allBtns = document.querySelectorAll('ytcp-button, button');
        for (var b of allBtns) {
            if (b.id === 'done-button') continue;
            if (b.offsetParent === null) continue;
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt === 'concluir' || txt === 'done') {
                b.click();
                return;
            }
        }
    """)
    time.sleep(2)


def save_video(driver):
    """Click Save button on the video edit page."""
    time.sleep(1)
    driver.execute_script("""
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            var aria = (b.getAttribute('aria-label') || '').toLowerCase();
            if (txt === 'salvar' || txt === 'save' || aria === 'salvar' || aria === 'save') {
                if (b.offsetParent !== null) {
                    b.click();
                    return 'saved';
                }
            }
        }
        // Try #save button specifically
        var saveBtn = document.querySelector('#save-button, button#save');
        if (saveBtn && saveBtn.offsetParent !== null) {
            saveBtn.click();
            return 'saved_id';
        }
        return 'no_save_btn';
    """)
    time.sleep(3)


def main():
    print("=" * 60)
    print("  FIX PLAYLISTS - Organizar videos em playlists")
    print("=" * 60)
    print()

    # Load results
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Load progress
    progress = load_progress()
    fixed_ids = set(progress.get("fixed", []))

    # Build work list: only clients that need fixing
    work = {}
    for client, videos in results.items():
        if client in SKIP_CLIENTS:
            continue
        pending = [v for v in videos if v['video_id'] not in fixed_ids]
        if pending:
            work[client] = pending

    total_pending = sum(len(v) for v in work.values())
    print(f"  Clientes para corrigir: {len(work)}")
    print(f"  Videos pendentes: {total_pending}")
    print(f"  Ja corrigidos: {len(fixed_ids)}")
    print()

    if total_pending == 0:
        print("[OK] Todos os videos ja estao em playlists!")
        return

    for client, videos in work.items():
        playlist_name = f"Portfolio - {client}"
        print(f"  {client}: {len(videos)} videos -> '{playlist_name}'")
    print()

    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print()
    print("[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

    # Verify YouTube Studio is accessible
    print("[BROWSER] Verificando YouTube Studio...")
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    channel = driver.execute_script("""
        var el = document.querySelector('ytcp-entity-name, .entity-name, #entity-name');
        return el ? el.textContent.trim() : 'unknown';
    """)
    print(f"[CANAL] Nome: {channel}")

    count = 0
    success = 0
    errors = 0

    for client, videos in work.items():
        playlist_name = f"Portfolio - {client}"
        print()
        print("-" * 60)
        print(f"  CLIENTE: {client} ({len(videos)} videos)")
        print(f"  PLAYLIST: {playlist_name}")
        print("-" * 60)

        for i, video in enumerate(videos):
            count += 1
            vid = video['video_id']
            title = video['title'][:60]
            print(f"\n[{count}/{total_pending}] {vid} - {title}")

            try:
                result = add_video_to_playlist(driver, vid, playlist_name)
                print(f"  [RESULTADO] {result}")

                if result in ('added_existing', 'created_and_added', 'already_in_playlist'):
                    success += 1
                    fixed_ids.add(vid)
                    progress["fixed"] = list(fixed_ids)
                    save_progress(progress)
                    print(f"  [OK] Video adicionado a '{playlist_name}'")
                else:
                    errors += 1
                    print(f"  [AVISO] Falha: {result}")
            except Exception as e:
                errors += 1
                print(f"  [ERRO] {str(e)[:80]}")

            time.sleep(3)

    print()
    print("=" * 60)
    print(f"  RESUMO")
    print(f"  Total processados: {count}")
    print(f"  Sucesso: {success}")
    print(f"  Erros: {errors}")
    print("=" * 60)

    print("\nFechando navegador em 5 segundos...")
    time.sleep(5)
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
