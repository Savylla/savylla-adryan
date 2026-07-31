"""
=============================================================
FIX PLAYLISTS FINAL - Corrige videos pendentes
=============================================================
Corrige o bug do dialog de criacao: o container
ytcp-playlist-creation-dialog tem height=0 mas os inputs
internos sao visiveis. Removida a checagem de height do
container.

USO: python fix_playlists_final.py
=============================================================
"""

import json
import os
import sys
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

RESULTS_FILE = "youtube_results.json"
PROGRESS_FILE = "fix_playlists_progress.json"
CHROME_DEBUG_PORT = 9555

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


def open_playlist_dialog(driver):
    """Open the playlist dialog on a video edit page."""
    opened = driver.execute_script("""
        var trigger = document.querySelector(
            'ytcp-dropdown-trigger[aria-label*="playlist" i]'
        );
        if (trigger && trigger.offsetParent !== null) {
            trigger.click();
            return 'clicked_aria';
        }
        var vmp = document.querySelector('ytcp-video-metadata-playlists');
        if (vmp) {
            var inner = vmp.querySelector('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, button');
            if (inner) { inner.click(); return 'clicked_vmp'; }
            vmp.click();
            return 'clicked_vmp_direct';
        }
        return 'not_found';
    """)
    if 'not_found' in str(opened):
        return False

    # Wait for dialog
    for _ in range(8):
        ready = driver.execute_script("""
            var dialog = document.querySelector('ytcp-playlist-dialog');
            return dialog && dialog.innerHTML.length > 100;
        """)
        if ready:
            return True
        time.sleep(1)

    return False


def scroll_playlist_list(driver):
    """Scroll the playlist list to load all items."""
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var list = dialog.querySelector('tp-yt-iron-list');
        if (list) {
            for (var s = 0; s <= list.scrollHeight; s += 32) {
                list.scrollTop = s;
            }
            list.scrollTop = 0;
        }
    """)
    time.sleep(1)


def find_playlist_in_dialog(driver, playlist_name):
    """Check if playlist exists in the dialog and check it. Returns status string."""
    return driver.execute_script("""
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
        var labels = dialog.querySelectorAll('label');
        for (var label of labels) {
            var txt = (label.textContent || '').trim();
            if (txt.includes(targetName)) {
                label.click();
                return 'checked_fallback';
            }
        }

        return 'not_found';
    """, playlist_name)


def create_playlist_in_dialog(driver, playlist_name):
    """
    Create a new playlist from within the video editor playlist dialog.
    Fixed: removed height checks on ytcp-playlist-creation-dialog container
    (it reports height=0 but inputs inside are visible).
    """

    # Step 1: Click "Nova playlist" button
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var npBtn = dialog.querySelector('.new-playlist-button button');
        if (npBtn) { npBtn.click(); return; }
        var btns = dialog.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').toLowerCase().trim();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                b.click(); return;
            }
        }
    """)
    time.sleep(2)

    # Step 2: Click menu item "Nova playlist"
    clicked_item = driver.execute_script("""
        var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
        if (item) { item.click(); return 'clicked'; }
        var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], [role="option"]');
        for (var i of items) {
            var txt = (i.textContent || '').toLowerCase().trim();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                i.click(); return 'clicked_fallback';
            }
        }
        return 'not_found';
    """)

    if clicked_item not in ('clicked', 'clicked_fallback'):
        return 'no_menu_item'

    time.sleep(5)

    # Step 3: Find and fill the title textbox
    # KEY FIX: Don't check container height. The ytcp-playlist-creation-dialog
    # has height=0 but its internal inputs are visible (height=30).
    focused = 'not_found'
    for retry in range(15):
        focused = driver.execute_script("""
            // PRIMARY: find the creation dialog's textbox directly
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            if (cd) {
                // Find the title textbox (first contenteditable with small height)
                var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
                for (var tb of boxes) {
                    // The title box is ~30px high, description is ~100px
                    if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                        tb.focus();
                        tb.click();
                        tb.textContent = '';
                        return 'focused_creation';
                    }
                }
                // If height check fails, try by placeholder/aria-label
                var allInputs = cd.querySelectorAll('#textbox, [contenteditable="true"], input, textarea');
                for (var inp of allInputs) {
                    var ph = inp.placeholder || inp.getAttribute('aria-label') || '';
                    if (ph.toLowerCase().includes('título') || ph.toLowerCase().includes('title') || ph.toLowerCase().includes('adicione um título')) {
                        inp.focus();
                        inp.click();
                        if (inp.contentEditable === 'true') inp.textContent = '';
                        return 'focused_placeholder';
                    }
                }
                // Last: just grab the first visible editable
                for (var tb of boxes) {
                    if (tb.offsetHeight > 0) {
                        tb.focus();
                        tb.click();
                        tb.textContent = '';
                        return 'focused_any';
                    }
                }
            }

            // FALLBACK: look for any dialog with "Criar uma nova playlist"
            var dialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog');
            for (var d of dialogs) {
                var txt = (d.textContent || '').toLowerCase();
                if (txt.includes('criar uma nova playlist') || txt.includes('create a new playlist')) {
                    var tb = d.querySelector('#textbox[contenteditable], div[contenteditable="true"]');
                    if (tb && tb.offsetHeight > 0) {
                        tb.focus();
                        tb.click();
                        tb.textContent = '';
                        return 'focused_fallback';
                    }
                }
            }

            return 'not_found';
        """)
        if 'focused' in str(focused):
            break
        time.sleep(1)

    if 'focused' not in str(focused):
        return 'no_textbox'

    # Step 4: Type the playlist name
    time.sleep(0.5)

    # Method 1: insertText command (most reliable for contenteditable)
    driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return;
        var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
        for (var tb of boxes) {
            if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                tb.focus();
                tb.textContent = '';
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, arguments[0]);
                tb.dispatchEvent(new Event('input', {bubbles: true}));
                return;
            }
        }
    """, playlist_name)
    time.sleep(1)

    # Method 2: send_keys as backup
    typed_text = driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return '';
        var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
        for (var tb of boxes) {
            if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                return tb.textContent.trim();
            }
        }
        return '';
    """)

    if not typed_text:
        try:
            active = driver.switch_to.active_element
            active.send_keys(playlist_name)
            time.sleep(1)
        except Exception:
            pass

    # Verify text was entered
    typed_text = driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return '';
        var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
        for (var tb of boxes) {
            if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                return tb.textContent.trim();
            }
        }
        return '';
    """)
    print(f"    [TYPED] '{typed_text}'")

    if not typed_text:
        return 'no_text_entered'

    time.sleep(1)

    # Step 5: Set visibility to "Não listada"
    driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return;
        var dds = cd.querySelectorAll('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger');
        for (var dd of dds) {
            var txt = (dd.textContent || '').toLowerCase();
            if (txt.includes('visibilidade') || txt.includes('visibility') ||
                txt.includes('pública') || txt.includes('public') ||
                txt.includes('privad') || txt.includes('private')) {
                dd.click();
                return;
            }
        }
    """)
    time.sleep(2)

    driver.execute_script("""
        var items = document.querySelectorAll('tp-yt-paper-item, [role="option"], [role="menuitem"]');
        for (var item of items) {
            var txt = (item.textContent || '').toLowerCase();
            if (txt.includes('não listada') || txt.includes('nao listada') || txt.includes('unlisted')) {
                item.click();
                return;
            }
        }
    """)
    time.sleep(2)

    # Step 6: Click "Criar"
    for retry in range(5):
        created = driver.execute_script("""
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            var containers = [];
            if (cd) containers.push(cd);
            var dialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog');
            for (var d of dialogs) { if (d.innerHTML.length > 100) containers.push(d); }

            for (var d of containers) {
                var btns = d.querySelectorAll('#create-button, ytcp-button, button');
                for (var b of btns) {
                    var txt = (b.textContent || '').trim().toLowerCase();
                    if (txt === 'criar' || txt === 'create') {
                        var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                        if (!disabled) { b.click(); return 'created'; }
                        return 'disabled';
                    }
                }
            }
            return 'no_button';
        """)

        if created == 'created':
            time.sleep(3)
            return 'created'

        if created == 'disabled':
            # Re-trigger input events to enable the button
            driver.execute_script("""
                var cd = document.querySelector('ytcp-playlist-creation-dialog');
                if (!cd) return;
                var tb = cd.querySelector('#textbox[contenteditable]');
                if (tb && tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                    tb.focus();
                    tb.dispatchEvent(new Event('input', {bubbles: true}));
                    tb.dispatchEvent(new Event('change', {bubbles: true}));
                    tb.dispatchEvent(new InputEvent('input', {
                        bubbles: true, data: tb.textContent, inputType: 'insertText'
                    }));
                }
            """)
            time.sleep(2)
        else:
            break

    return f'create_failed:{created}'


def close_playlist_dialog(driver):
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (dialog) {
            var els = dialog.querySelectorAll('ytcp-button, button');
            for (var el of els) {
                var txt = (el.textContent || '').trim().toLowerCase();
                if (txt === 'concluir' || txt === 'done') {
                    el.click(); return;
                }
            }
        }
        var allBtns = document.querySelectorAll('ytcp-button, button');
        for (var b of allBtns) {
            if (b.offsetParent === null) continue;
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt === 'concluir' || txt === 'done') {
                b.click(); return;
            }
        }
    """)
    time.sleep(2)


def save_video(driver):
    time.sleep(1)
    driver.execute_script("""
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            var aria = (b.getAttribute('aria-label') || '').toLowerCase();
            if (txt === 'salvar' || txt === 'save' || aria === 'salvar' || aria === 'save') {
                if (b.offsetParent !== null) { b.click(); return; }
            }
        }
        var saveBtn = document.querySelector('#save-button');
        if (saveBtn && saveBtn.offsetParent !== null) saveBtn.click();
    """)
    time.sleep(3)


def add_video_to_playlist(driver, video_id, playlist_name):
    """Navigate to video edit page and add to playlist. Creates playlist if needed."""

    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(5)

    # Wait for page
    for _ in range(10):
        ready = driver.execute_script("""
            return document.querySelector('ytcp-video-metadata-editor') !== null
                || document.querySelector('#details') !== null
                || document.querySelector('ytcp-mention-textbox') !== null;
        """)
        if ready:
            break
        time.sleep(2)

    # Open playlist dialog
    if not open_playlist_dialog(driver):
        return 'no_playlist_selector'

    time.sleep(1)
    scroll_playlist_list(driver)

    # Try to find and check the playlist
    select_result = find_playlist_in_dialog(driver, playlist_name)

    if select_result == 'already_checked':
        close_playlist_dialog(driver)
        return 'already_in_playlist'

    if 'checked' in str(select_result):
        time.sleep(1)
        close_playlist_dialog(driver)
        time.sleep(1)
        save_video(driver)
        return 'added_existing'

    # Playlist not found — create it
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


def main():
    print("=" * 60)
    print("  FIX PLAYLISTS FINAL")
    print("=" * 60)
    print()

    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)

    progress = load_progress()
    fixed_ids = set(progress.get("fixed", []))

    work = {}
    for client, videos in results.items():
        if client in SKIP_CLIENTS:
            continue
        pending = [v for v in videos if v['video_id'] not in fixed_ids]
        if pending:
            work[client] = pending

    total_pending = sum(len(v) for v in work.values())
    print(f"  Clientes pendentes: {len(work)}")
    print(f"  Videos pendentes: {total_pending}")
    print(f"  Ja corrigidos: {len(fixed_ids)}")
    print()

    if total_pending == 0:
        print("[OK] Todos os videos ja estao em playlists!")
        return

    for client, videos in work.items():
        print(f"  {client}: {len(videos)} videos -> 'Portfolio - {client}'")

    print()
    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print()
    print("[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

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

        for video in videos:
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
