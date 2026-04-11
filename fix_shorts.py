"""
Fix Shorts: Identifica Shorts no YouTube Studio, deleta, e limpa do progresso
para re-upload com padding de 181s.

USO: python fix_shorts.py
"""

import json
import os
import sys
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555
PROGRESS_FILE = "upload_progress.json"
RESULTS_FILE = "youtube_results.json"


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
            break
        except Exception as e:
            if attempt < 4:
                print(f"  [RETRY] Tentativa {attempt + 1}/5...")
                time.sleep(5)
            else:
                raise RuntimeError(f"Nao conectou ao Chrome: {e}")
    return driver


def collect_shorts(driver):
    """Navigate to YouTube Studio content page, click Shorts tab, collect IDs."""
    print("\n[NAV] Abrindo YouTube Studio > Conteudo...")
    driver.get("https://studio.youtube.com/channel/UC/content")
    time.sleep(10)

    print(f"[URL] {driver.current_url}")

    # Click "Shorts" tab
    clicked_tab = driver.execute_script("""
        var tabs = document.querySelectorAll('tp-yt-paper-tab');
        for (var t of tabs) {
            var txt = (t.textContent || '').trim();
            if (txt === 'Shorts') {
                t.click();
                return 'clicked_shorts_tab';
            }
        }
        return 'no_shorts_tab';
    """)
    print(f"[TAB] {clicked_tab}")
    time.sleep(5)

    if clicked_tab == 'no_shorts_tab':
        print("[ERRO] Aba 'Shorts' nao encontrada!")
        return []

    all_short_ids = []
    scroll_attempts = 0
    max_scrolls = 50
    no_change_count = 0

    while scroll_attempts < max_scrolls:
        # Collect video IDs from visible rows
        new_ids = driver.execute_script("""
            var ids = [];
            // Method 1: video-row elements
            var rows = document.querySelectorAll('ytcp-video-row');
            for (var r of rows) {
                var vid = r.getAttribute('video-id');
                if (vid && ids.indexOf(vid) === -1) ids.push(vid);
            }
            // Method 2: links with /video/ pattern
            var links = document.querySelectorAll('a[href*="/video/"]');
            for (var l of links) {
                var href = l.getAttribute('href') || '';
                var match = href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                if (match && ids.indexOf(match[1]) === -1) ids.push(match[1]);
            }
            return ids;
        """)

        prev_count = len(all_short_ids)
        for vid in new_ids:
            if vid not in all_short_ids:
                all_short_ids.append(vid)

        scroll_attempts += 1
        print(f"  [SCROLL {scroll_attempts}] Shorts: {len(all_short_ids)}")

        if len(all_short_ids) == prev_count:
            no_change_count += 1
            if no_change_count >= 3:
                print(f"  [OK] Sem mais Shorts para carregar.")
                break
        else:
            no_change_count = 0

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)

    print(f"\n[TOTAL] {len(all_short_ids)} Shorts encontrados")
    return all_short_ids


def delete_short(driver, video_id, index, total):
    """Delete a single Short via YouTube Studio."""
    print(f"\n[{index}/{total}] Deletando Short: {video_id}")

    driver.get(f"https://studio.youtube.com/video/{video_id}/edit")
    time.sleep(6)

    # Click the 3-dot menu (more options) at top right
    clicked_menu = driver.execute_script("""
        // Look for the kebab/more-options menu
        var btns = document.querySelectorAll('#overflow-menu-button, ytcp-icon-button, button');
        for (var b of btns) {
            var aria = (b.getAttribute('aria-label') || '').toLowerCase();
            var id = b.id || '';
            if (id === 'overflow-menu-button' || aria.includes('mais opções') ||
                aria.includes('more options') || aria.includes('mais ações') ||
                aria.includes('more actions')) {
                b.click();
                return 'clicked: ' + (id || aria);
            }
        }

        // Fallback: look for three-dot icon button
        var iconBtns = document.querySelectorAll('ytcp-icon-button');
        for (var ib of iconBtns) {
            var icon = ib.querySelector('tp-yt-iron-icon');
            if (icon) {
                var iconName = icon.getAttribute('icon') || '';
                if (iconName.includes('more') || iconName.includes('vert')) {
                    ib.click();
                    return 'clicked_icon: ' + iconName;
                }
            }
        }

        return 'no_menu';
    """)
    print(f"  [MENU] {clicked_menu}")
    time.sleep(2)

    if 'no_menu' in str(clicked_menu):
        # Debug
        driver.save_screenshot(f"debug_no_menu_{video_id}.png")
        print(f"  [DEBUG] Screenshot salvo")
        return False

    # Click "Excluir" / "Delete"
    clicked_delete = driver.execute_script("""
        var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], tp-yt-paper-listbox tp-yt-paper-item');
        for (var item of items) {
            var txt = (item.textContent || '').trim().toLowerCase();
            if (txt.includes('excluir definitivamente') || txt.includes('delete forever') ||
                txt.includes('excluir') || txt.includes('delete')) {
                item.click();
                return 'clicked: ' + txt.substring(0, 40);
            }
        }
        return 'no_delete';
    """)
    print(f"  [DELETE] {clicked_delete}")
    time.sleep(3)

    if 'no_delete' in str(clicked_delete):
        driver.save_screenshot(f"debug_no_delete_{video_id}.png")
        return False

    # Check the confirmation checkbox
    time.sleep(1)
    checked = driver.execute_script("""
        var checkboxes = document.querySelectorAll(
            'ytcp-checkbox-lit, tp-yt-paper-checkbox, #checkbox, [type="checkbox"]'
        );
        for (var cb of checkboxes) {
            // Only click checkboxes in the visible dialog
            if (cb.offsetParent !== null || getComputedStyle(cb).display !== 'none') {
                cb.click();
                return 'checked';
            }
        }
        return 'no_checkbox';
    """)
    print(f"  [CHECKBOX] {checked}")
    time.sleep(1)

    # Click the final "Excluir" / "Delete" button
    final = driver.execute_script("""
        // Look in dialogs
        var dialogs = document.querySelectorAll(
            'ytcp-confirmation-dialog, tp-yt-paper-dialog, ytcp-dialog, [role="dialog"]'
        );
        for (var d of dialogs) {
            if (d.offsetParent === null && getComputedStyle(d).display === 'none') continue;
            var btns = d.querySelectorAll('ytcp-button, button');
            for (var b of btns) {
                var txt = (b.textContent || '').trim().toLowerCase();
                if (txt.includes('excluir') || txt.includes('delete')) {
                    var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                    if (!disabled) {
                        b.click();
                        return 'deleted: ' + txt;
                    }
                    return 'disabled: ' + txt;
                }
            }
        }
        return 'no_final_delete';
    """)
    print(f"  [FINAL] {final}")
    time.sleep(4)

    if 'deleted' in str(final):
        print(f"  [OK] Short {video_id} excluido!")
        return True
    else:
        driver.save_screenshot(f"debug_final_{video_id}.png")
        return False


def remove_from_progress(short_ids):
    """Remove deleted Short IDs from progress files so they get re-uploaded."""
    if not os.path.exists(PROGRESS_FILE):
        print("[AVISO] upload_progress.json nao encontrado")
        return 0

    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    removed = 0
    short_set = set(short_ids)

    # Nested structure: { "key": { "Client_001": {video_id: ...}, ... } }
    for top_key in list(progress.keys()):
        entries = progress[top_key]
        if isinstance(entries, dict):
            for entry_key in list(entries.keys()):
                entry = entries[entry_key]
                if isinstance(entry, dict) and entry.get('video_id') in short_set:
                    vid = entry['video_id']
                    title = entry.get('title', entry_key)[:50]
                    print(f"  [REMOVE] {entry_key}: {vid} - {title}")
                    del entries[entry_key]
                    removed += 1

    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

    # Also clean youtube_results.json
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            results = json.load(f)

        for client in list(results.keys()):
            if isinstance(results[client], list):
                before = len(results[client])
                results[client] = [
                    v for v in results[client]
                    if v.get('video_id') not in short_set
                ]
                diff = before - len(results[client])
                if diff:
                    print(f"  [RESULTS] {client}: removidos {diff} entries")

        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    return removed


def main():
    print("=" * 60)
    print("  FIX SHORTS - Identificar, Excluir e Limpar Progresso")
    print("=" * 60)

    driver = create_driver()

    try:
        # Step 1: Collect all Shorts
        short_ids = collect_shorts(driver)

        if not short_ids:
            print("\n[OK] Nenhum Short encontrado! Nada a fazer.")
            return

        # Save shorts list
        with open('shorts_to_delete.json', 'w') as f:
            json.dump(short_ids, f, indent=2)
        print(f"[SAVE] {len(short_ids)} Shorts salvos em shorts_to_delete.json")

        # Step 2: Delete each Short
        print(f"\n{'='*60}")
        print(f"  DELETANDO {len(short_ids)} SHORTS")
        print(f"{'='*60}")

        deleted_ids = []
        failed_ids = []

        for i, vid in enumerate(short_ids, 1):
            success = delete_short(driver, vid, i, len(short_ids))
            if success:
                deleted_ids.append(vid)
            else:
                failed_ids.append(vid)
            time.sleep(2)

        # Step 3: Remove from progress
        print(f"\n{'='*60}")
        print(f"  LIMPANDO PROGRESSO")
        print(f"{'='*60}")

        removed = remove_from_progress(deleted_ids)

        # Summary
        print(f"\n{'='*60}")
        print(f"  RESUMO")
        print(f"{'='*60}")
        print(f"  Shorts encontrados: {len(short_ids)}")
        print(f"  Deletados: {len(deleted_ids)}")
        print(f"  Falhas: {len(failed_ids)}")
        print(f"  Removidos do progresso: {removed}")

        if failed_ids:
            print(f"\n  IDs com falha:")
            for vid in failed_ids:
                print(f"    - https://youtu.be/{vid}")

        print(f"\n[NEXT] Rode 'python youtube_compilation_uploader.py' para re-enviar com 181s")

    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n[BROWSER] Chrome permanece aberto.")


if __name__ == "__main__":
    main()
