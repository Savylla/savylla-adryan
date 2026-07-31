"""
=============================================================
FIX PLAYLISTS v2 - Corrige videos que falharam na v1
=============================================================
Estrategia melhorada:
  1. Primeiro cria TODAS as playlists necessarias via pagina de playlists
  2. Depois adiciona cada video a playlist existente (sem criar novamente)

Isso evita o bug do dialogo de criacao no editor de video.

USO: python fix_playlists_v2.py
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


# ============================================================
#  FASE 1: Criar playlists via pagina de playlists do canal
# ============================================================

def get_existing_playlists(driver):
    """Navigate to playlists page and get list of existing playlist names."""
    driver.get("https://studio.youtube.com/channel/playlists")
    time.sleep(5)

    # Wait for page to load
    for _ in range(10):
        ready = driver.execute_script("""
            return document.querySelector('ytcp-playlist-list') !== null
                || document.querySelector('.playlist-list') !== null
                || document.querySelectorAll('ytcp-playlist-row, .playlist-row').length > 0
                || document.querySelector('#playlists-table') !== null;
        """)
        if ready:
            break
        time.sleep(2)

    # Scroll to load all playlists
    driver.execute_script("""
        window.scrollTo(0, document.body.scrollHeight);
    """)
    time.sleep(2)
    driver.execute_script("""
        window.scrollTo(0, document.body.scrollHeight);
    """)
    time.sleep(2)

    playlists = driver.execute_script("""
        var names = [];
        // Method 1: playlist rows
        var rows = document.querySelectorAll('ytcp-playlist-row, .playlist-row, tr.playlist');
        for (var r of rows) {
            var title = r.querySelector('a.playlist-title, .title-column a, a[href*="playlist"]');
            if (title) names.push(title.textContent.trim());
        }
        // Method 2: any link that looks like a playlist
        if (names.length === 0) {
            var links = document.querySelectorAll('a[href*="/playlist/"]');
            for (var l of links) {
                var txt = l.textContent.trim();
                if (txt && txt.length > 2 && txt.length < 100) names.push(txt);
            }
        }
        // Method 3: broader search for playlist names in table/list
        if (names.length === 0) {
            var cells = document.querySelectorAll('td a, .title a, [class*="playlist"] a');
            for (var c of cells) {
                var txt = c.textContent.trim();
                if (txt && txt.length > 2 && txt.length < 100) names.push(txt);
            }
        }
        return names;
    """)

    return playlists


def create_playlist_via_studio(driver, playlist_name):
    """Create a playlist via YouTube Studio playlists page (more reliable than video editor)."""
    driver.get("https://studio.youtube.com/channel/playlists")
    time.sleep(5)

    # Click "Nova playlist" / "New playlist" button on the playlists page
    clicked = driver.execute_script("""
        // Look for the create/new playlist button on the playlists management page
        var btns = document.querySelectorAll('ytcp-button, button, a');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt.includes('nova playlist') || txt.includes('new playlist') || txt.includes('criar playlist')) {
                b.click();
                return 'clicked:' + txt.substring(0, 30);
            }
        }
        // Try icon button with tooltip
        var iconBtns = document.querySelectorAll('[aria-label*="playlist" i], [aria-label*="Playlist" i], [tooltip*="playlist" i]');
        for (var b of iconBtns) {
            var label = (b.getAttribute('aria-label') || b.getAttribute('tooltip') || '').toLowerCase();
            if (label.includes('nova') || label.includes('new') || label.includes('criar') || label.includes('create')) {
                b.click();
                return 'clicked_aria:' + label.substring(0, 30);
            }
        }
        return 'not_found';
    """)
    print(f"    [CLICK] Nova playlist: {clicked}")

    if 'not_found' in str(clicked):
        return False

    time.sleep(3)

    # Now a dialog should appear - find the title input
    # Try multiple approaches: input, textarea, contenteditable
    title_filled = False
    for attempt in range(15):
        result = driver.execute_script("""
            // Search ALL visible dialogs/overlays for a text input
            var containers = document.querySelectorAll(
                'ytcp-playlist-creation-dialog, ytcp-dialog, tp-yt-paper-dialog, [role="dialog"], [aria-modal="true"]'
            );

            for (var container of containers) {
                if (container.offsetHeight < 50) continue;
                var txt = (container.textContent || '').toLowerCase();
                // Must be a creation dialog
                if (!txt.includes('playlist') && !txt.includes('título') && !txt.includes('title')) continue;

                // Try 1: regular input/textarea
                var inputs = container.querySelectorAll('input[type="text"], input:not([type]), textarea');
                for (var inp of inputs) {
                    if (inp.offsetParent === null) continue;
                    if (inp.id === 'search-input') continue;
                    if (inp.offsetHeight < 5 || inp.offsetHeight > 100) continue;
                    inp.focus();
                    inp.click();
                    inp.value = arguments[0];
                    inp.dispatchEvent(new Event('input', {bubbles: true}));
                    inp.dispatchEvent(new Event('change', {bubbles: true}));
                    return 'filled_input:' + inp.tagName + '#' + inp.id;
                }

                // Try 2: contenteditable divs (old YouTube Studio)
                var editables = container.querySelectorAll(
                    '#textbox[contenteditable], div[contenteditable="true"], div[contenteditable="plaintext-only"], [contenteditable=""]'
                );
                for (var el of editables) {
                    if (el.offsetParent === null) continue;
                    if (el.offsetHeight < 5 || el.offsetHeight > 80) continue;
                    // Skip large description fields
                    var parent = el.closest('ytcp-social-suggestions-textbox, ytcp-mention-textbox');
                    if (parent && parent.id && parent.id.includes('description')) continue;
                    el.focus();
                    el.click();
                    el.textContent = '';
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, arguments[0]);
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    return 'filled_contenteditable';
                }

                // Try 3: shadow DOM inputs
                var allEls = container.querySelectorAll('*');
                for (var el of allEls) {
                    if (el.shadowRoot) {
                        var shadowInputs = el.shadowRoot.querySelectorAll('input, textarea, [contenteditable="true"]');
                        for (var si of shadowInputs) {
                            if (si.offsetParent === null) continue;
                            if (si.offsetHeight < 5) continue;
                            si.focus();
                            si.value = arguments[0];
                            si.dispatchEvent(new Event('input', {bubbles: true}));
                            return 'filled_shadow:' + si.tagName;
                        }
                    }
                }
            }

            return 'no_input_found';
        """, playlist_name)

        if 'filled' in str(result):
            print(f"    [TITLE] {result}")
            title_filled = True
            break

        time.sleep(1)

    if not title_filled:
        # Last resort: try send_keys to active element after clicking
        print("    [TITLE] Tentando send_keys como fallback...")
        try:
            active = driver.switch_to.active_element
            active.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.3)
            active.send_keys(playlist_name)
            title_filled = True
            print("    [TITLE] send_keys OK")
        except Exception as e:
            print(f"    [TITLE] send_keys falhou: {e}")

    if not title_filled:
        print("    [ERRO] Nao conseguiu preencher titulo")
        driver.save_screenshot("debug_v2_no_title.png")
        return False

    time.sleep(2)

    # Set visibility to "Não listada" / "Unlisted"
    driver.execute_script("""
        var containers = document.querySelectorAll(
            'ytcp-playlist-creation-dialog, ytcp-dialog, tp-yt-paper-dialog, [role="dialog"]'
        );
        for (var d of containers) {
            if (d.offsetHeight < 50) continue;
            var dds = d.querySelectorAll('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, select');
            for (var dd of dds) {
                var txt = (dd.textContent || '').toLowerCase();
                if (txt.includes('visibilidade') || txt.includes('visibility') ||
                    txt.includes('pública') || txt.includes('public') ||
                    txt.includes('privad') || txt.includes('private')) {
                    dd.click();
                    return 'opened';
                }
            }
        }
        return 'no_visibility_dropdown';
    """)
    time.sleep(2)

    driver.execute_script("""
        var items = document.querySelectorAll('tp-yt-paper-item, [role="option"], [role="menuitem"], [role="listbox"] > *');
        for (var item of items) {
            var txt = (item.textContent || '').toLowerCase();
            if (txt.includes('não listada') || txt.includes('nao listada') || txt.includes('unlisted')) {
                item.click();
                return 'set_unlisted';
            }
        }
        return 'not_found';
    """)
    time.sleep(2)

    # Click "Criar" / "Create"
    for retry in range(5):
        created = driver.execute_script("""
            var containers = document.querySelectorAll(
                'ytcp-playlist-creation-dialog, ytcp-dialog, tp-yt-paper-dialog, [role="dialog"]'
            );
            for (var d of containers) {
                if (d.offsetHeight < 50) continue;
                var btns = d.querySelectorAll('#create-button, ytcp-button, button');
                for (var b of btns) {
                    var txt = (b.textContent || '').trim().toLowerCase();
                    if (txt === 'criar' || txt === 'create') {
                        var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                        if (!disabled) {
                            b.click();
                            return 'created';
                        }
                        return 'disabled';
                    }
                }
            }
            return 'no_button';
        """)
        if created == 'created':
            print(f"    [CRIAR] Playlist '{playlist_name}' criada!")
            time.sleep(3)
            return True
        if created == 'disabled':
            # Re-trigger input event
            driver.execute_script("""
                var el = document.activeElement;
                if (el) {
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    el.dispatchEvent(new InputEvent('input', {bubbles: true, data: ' ', inputType: 'insertText'}));
                }
            """)
            time.sleep(2)
        else:
            break

    print(f"    [ERRO] Nao conseguiu clicar Criar: {created}")
    driver.save_screenshot("debug_v2_no_criar.png")
    return False


# ============================================================
#  FASE 2: Adicionar videos a playlists existentes
# ============================================================

def add_video_to_existing_playlist(driver, video_id, playlist_name):
    """Add video to an existing playlist via the video editor."""

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
    opened = driver.execute_script("""
        var trigger = document.querySelector(
            'ytcp-dropdown-trigger[aria-label*="playlist" i], ytcp-dropdown-trigger[aria-label*="Playlist"]'
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
        return 'no_playlist_selector'

    time.sleep(3)

    # Wait for dialog
    dialog_ready = False
    for _ in range(8):
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

    # Scroll playlist list
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var list = dialog.querySelector('tp-yt-iron-list, .playlists, [class*="list"]');
        if (list) {
            for (var s = 0; s <= list.scrollHeight; s += 32) {
                list.scrollTop = s;
            }
            list.scrollTop = 0;
        }
    """)
    time.sleep(1)

    # Find and check the playlist
    select_result = driver.execute_script("""
        var targetName = arguments[0];
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return 'no_dialog';

        // Search checkbox groups
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

    if select_result == 'already_checked':
        close_playlist_dialog(driver)
        return 'already_in_playlist'

    if 'checked' in str(select_result):
        time.sleep(1)
        close_playlist_dialog(driver)
        time.sleep(1)
        save_video(driver)
        return 'added_existing'

    # Playlist not found even after Phase 1 created it
    close_playlist_dialog(driver)
    return f'playlist_not_found:{select_result}'


def close_playlist_dialog(driver):
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (dialog) {
            var els = dialog.querySelectorAll('ytcp-button, button, div');
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
                if (b.offsetParent !== null) { b.click(); return 'saved'; }
            }
        }
        var saveBtn = document.querySelector('#save-button, button#save');
        if (saveBtn && saveBtn.offsetParent !== null) {
            saveBtn.click(); return 'saved_id';
        }
        return 'no_save_btn';
    """)
    time.sleep(3)


def main():
    print("=" * 60)
    print("  FIX PLAYLISTS v2 - Corrigir videos pendentes")
    print("=" * 60)
    print()

    # Load data
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)

    progress = load_progress()
    fixed_ids = set(progress.get("fixed", []))

    # Build work list
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

    needed_playlists = {}
    for client, videos in work.items():
        playlist_name = f"Portfolio - {client}"
        needed_playlists[client] = playlist_name
        print(f"  {client}: {len(videos)} videos -> '{playlist_name}'")

    print()
    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print()
    print("[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

    # Verify YouTube Studio
    print("[BROWSER] Verificando YouTube Studio...")
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    channel = driver.execute_script("""
        var el = document.querySelector('ytcp-entity-name, .entity-name, #entity-name');
        return el ? el.textContent.trim() : 'unknown';
    """)
    print(f"[CANAL] Nome: {channel}")

    # ============================================================
    #  FASE 1: Garantir que playlists existem
    # ============================================================
    print()
    print("=" * 60)
    print("  FASE 1: Verificar/criar playlists")
    print("=" * 60)

    existing = get_existing_playlists(driver)
    print(f"  Playlists existentes ({len(existing)}): {existing}")

    for client, playlist_name in needed_playlists.items():
        # Check if playlist already exists (partial match)
        found = any(playlist_name.lower() in p.lower() or p.lower() in playlist_name.lower()
                     for p in existing)
        if found:
            print(f"  [OK] '{playlist_name}' ja existe")
        else:
            print(f"  [CRIAR] Criando '{playlist_name}'...")
            success = create_playlist_via_studio(driver, playlist_name)
            if success:
                existing.append(playlist_name)
            else:
                print(f"  [AVISO] Falha ao criar '{playlist_name}' - tentara criar no editor de video")

    time.sleep(3)

    # ============================================================
    #  FASE 2: Adicionar videos as playlists
    # ============================================================
    print()
    print("=" * 60)
    print("  FASE 2: Adicionar videos as playlists")
    print("=" * 60)

    count = 0
    success_count = 0
    error_count = 0

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
                result = add_video_to_existing_playlist(driver, vid, playlist_name)
                print(f"  [RESULTADO] {result}")

                if result in ('added_existing', 'already_in_playlist'):
                    success_count += 1
                    fixed_ids.add(vid)
                    progress["fixed"] = list(fixed_ids)
                    save_progress(progress)
                    print(f"  [OK] Video adicionado a '{playlist_name}'")
                elif 'playlist_not_found' in str(result):
                    error_count += 1
                    print(f"  [AVISO] Playlist '{playlist_name}' nao encontrada no dialogo")
                else:
                    error_count += 1
                    print(f"  [AVISO] Falha: {result}")
            except Exception as e:
                error_count += 1
                print(f"  [ERRO] {str(e)[:80]}")

            time.sleep(3)

    print()
    print("=" * 60)
    print(f"  RESUMO")
    print(f"  Total processados: {count}")
    print(f"  Sucesso: {success_count}")
    print(f"  Erros: {error_count}")
    print("=" * 60)

    print("\nFechando navegador em 5 segundos...")
    time.sleep(5)
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
