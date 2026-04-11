"""
=============================================================
DELETE ALL SHORTS + ANALYZE MISSING VIDEOS
=============================================================
1. Abre YouTube Studio
2. Vai na aba Shorts e deleta TODOS
3. Vai na aba Videos e coleta os IDs restantes
4. Compara com client_videos.json para achar faltantes
5. Gera relatorio completo

USO: python delete_shorts_and_analyze.py
=============================================================
"""

import json
import os
import sys
import time
import subprocess
import re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

CHROME_DEBUG_PORT = 9555
STUDIO_SHORTS_URL = "https://studio.youtube.com/channel/UC/content/shorts"
STUDIO_VIDEOS_URL = "https://studio.youtube.com/channel/UC/content/videos"


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
                print(f"  [RETRY] Tentativa {attempt + 1}/5 - aguardando Chrome...")
                time.sleep(5)
            else:
                raise e

    return driver


def navigate_to_studio_content(driver):
    """Navigate to YouTube Studio content page."""
    print("[NAV] Abrindo YouTube Studio > Content...")
    driver.get("https://studio.youtube.com/channel/UC/content")
    time.sleep(8)

    # Check if we're on the right page
    current = driver.current_url
    print(f"[NAV] URL atual: {current}")

    if "studio.youtube.com" not in current:
        print("[ERRO] Nao esta logado no YouTube Studio!")
        driver.save_screenshot("debug_not_logged.png")
        return False
    return True


def click_shorts_tab(driver):
    """Click the Shorts tab in YouTube Studio content."""
    print("[NAV] Clicando na aba 'Shorts'...")
    result = driver.execute_script("""
        // Look for Shorts tab
        var tabs = document.querySelectorAll('tp-yt-paper-tab, [role="tab"], .tab-header');
        for (var tab of tabs) {
            var txt = (tab.textContent || '').trim().toLowerCase();
            if (txt.includes('short')) {
                tab.click();
                return 'clicked_shorts_tab: ' + txt;
            }
        }

        // Alternative: look for links with shorts
        var links = document.querySelectorAll('a[href*="shorts"]');
        for (var link of links) {
            link.click();
            return 'clicked_shorts_link';
        }

        return 'shorts_tab_not_found';
    """)
    print(f"[NAV] {result}")
    time.sleep(5)
    return 'not_found' not in str(result)


def collect_all_shorts(driver):
    """Scroll through Shorts tab and collect all video IDs."""
    print("[SCAN] Coletando todos os Shorts...")

    all_shorts = set()
    last_count = 0
    no_change_count = 0

    for scroll in range(50):  # Max 50 scroll attempts
        # Collect video IDs from current view
        ids = driver.execute_script("""
            var ids = [];
            // Method 1: video rows with hrefs
            var links = document.querySelectorAll('a[href*="/video/"], a[href*="/shorts/"]');
            for (var link of links) {
                var href = link.getAttribute('href') || '';
                var match = href.match(/\\/video\\/([a-zA-Z0-9_-]+)/) || href.match(/\\/shorts\\/([a-zA-Z0-9_-]+)/);
                if (match) ids.push(match[1]);
            }

            // Method 2: video-row elements
            var rows = document.querySelectorAll('ytcp-video-row');
            for (var row of rows) {
                var editLink = row.querySelector('a[href*="/video/"]');
                if (editLink) {
                    var match = editLink.getAttribute('href').match(/\\/video\\/([a-zA-Z0-9_-]+)/);
                    if (match) ids.push(match[1]);
                }
            }

            // Method 3: from data attributes
            var elements = document.querySelectorAll('[video-id]');
            for (var el of elements) {
                var vid = el.getAttribute('video-id');
                if (vid) ids.push(vid);
            }

            return [...new Set(ids)];
        """)

        for vid in ids:
            all_shorts.add(vid)

        if len(all_shorts) == last_count:
            no_change_count += 1
            if no_change_count >= 3:
                break
        else:
            no_change_count = 0
            last_count = len(all_shorts)

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

        if scroll % 5 == 0:
            print(f"  [SCAN] Scroll {scroll} - {len(all_shorts)} Shorts encontrados...")

    print(f"[SCAN] Total de Shorts encontrados: {len(all_shorts)}")
    return list(all_shorts)


def delete_short_video(driver, video_id, index, total):
    """Delete a single Short from YouTube Studio."""
    # Navigate to the video edit page
    edit_url = f"https://studio.youtube.com/video/{video_id}/edit"
    print(f"  [{index}/{total}] Deletando {video_id}...", end=" ", flush=True)

    driver.get(edit_url)
    time.sleep(5)

    # Click the three-dot menu (more options)
    result = driver.execute_script("""
        // Look for the "more options" or three-dot menu button
        var moreBtn = document.querySelector('ytcp-button#more-actions, ytcp-button[icon="more_vert"], #overflow-menu-button');
        if (moreBtn) {
            moreBtn.click();
            return 'clicked_more';
        }

        // Fallback: any button with more_vert icon
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            var icon = b.querySelector('tp-yt-iron-icon[icon="more_vert"], iron-icon[icon="more_vert"]');
            if (icon) {
                b.click();
                return 'clicked_more_fallback';
            }
            var aria = (b.getAttribute('aria-label') || '').toLowerCase();
            if (aria.includes('more') || aria.includes('mais') || aria.includes('opções') || aria.includes('options')) {
                b.click();
                return 'clicked_more_aria: ' + aria;
            }
        }

        return 'more_not_found';
    """)

    if 'not_found' in str(result):
        print(f"FALHOU (menu nao encontrado)")
        return False

    time.sleep(2)

    # Click "Delete" / "Excluir" from the dropdown
    result = driver.execute_script("""
        var items = document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu .item, [role="menuitem"], tp-yt-paper-listbox tp-yt-paper-item');
        for (var item of items) {
            var txt = (item.textContent || '').trim().toLowerCase();
            if (txt.includes('excluir') || txt.includes('delete') || txt.includes('apagar')) {
                // Skip "excluir permanentemente" - we want the first delete option
                item.click();
                return 'clicked_delete: ' + txt.substring(0, 40);
            }
        }
        return 'delete_not_found';
    """)

    if 'not_found' in str(result):
        print(f"FALHOU (botao delete nao encontrado)")
        return False

    time.sleep(2)

    # Handle confirmation dialog - check the checkbox first if needed
    driver.execute_script("""
        // Check the confirmation checkbox if present
        var checkboxes = document.querySelectorAll('#confirm-checkbox, ytcp-checkbox-lit, tp-yt-paper-checkbox, [type="checkbox"]');
        for (var cb of checkboxes) {
            if (!cb.checked && cb.offsetParent !== null) {
                cb.click();
            }
        }

        // Also try clicking on label/container of checkbox
        var labels = document.querySelectorAll('.checkbox-container, .style-scope.ytcp-checkbox-lit');
        for (var lbl of labels) {
            var txt = (lbl.textContent || '').toLowerCase();
            if (txt.includes('entendo') || txt.includes('understand') || txt.includes('permanente')) {
                lbl.click();
            }
        }
    """)
    time.sleep(1)

    # Click the final "Delete" / "Excluir" confirmation button
    result = driver.execute_script("""
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            if (b.offsetParent === null) continue;
            var txt = (b.textContent || '').trim().toLowerCase();
            var aria = (b.getAttribute('aria-label') || '').toLowerCase();
            if (txt === 'excluir' || txt === 'delete' || txt === 'excluir definitivamente' ||
                txt === 'delete forever' || aria.includes('excluir') || aria.includes('delete')) {
                var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                if (!disabled) {
                    b.click();
                    return 'confirmed_delete';
                }
                return 'delete_btn_disabled';
            }
        }
        return 'confirm_not_found';
    """)

    if 'confirmed' in str(result):
        print("OK")
        time.sleep(3)
        return True
    else:
        print(f"FALHOU ({result})")
        return False


def delete_all_shorts_via_content_page(driver):
    """Alternative: delete shorts directly from the content list."""
    print("\n[DELETE] Deletando Shorts via pagina de conteudo...")

    deleted_count = 0
    failed_count = 0

    while True:
        # Navigate to content page and click Shorts tab
        driver.get("https://studio.youtube.com/channel/UC/content")
        time.sleep(6)

        # Click Shorts tab
        if not click_shorts_tab(driver):
            # Try direct URL
            driver.get("https://studio.youtube.com/channel/UC/content/shorts")
            time.sleep(6)

        time.sleep(3)

        # Check if there are any shorts left
        shorts_info = driver.execute_script("""
            var rows = document.querySelectorAll('ytcp-video-row');
            if (rows.length === 0) return JSON.stringify({count: 0, ids: []});

            var ids = [];
            for (var row of rows) {
                var link = row.querySelector('a[href*="/video/"]');
                if (link) {
                    var match = link.getAttribute('href').match(/\\/video\\/([a-zA-Z0-9_-]+)/);
                    if (match) ids.push(match[1]);
                }
            }

            // Also check for "no content" message
            var noContent = document.querySelector('.empty-state-content, .no-content-message');
            if (noContent) return JSON.stringify({count: 0, ids: []});

            return JSON.stringify({count: rows.length, ids: ids});
        """)

        info = json.loads(shorts_info)
        if info['count'] == 0:
            print(f"\n[DELETE] Nenhum Short restante! Total deletados: {deleted_count}")
            break

        print(f"\n[DELETE] {info['count']} Shorts na pagina. Deletando o primeiro...")

        # Select the first short's checkbox
        selected = driver.execute_script("""
            var rows = document.querySelectorAll('ytcp-video-row');
            if (rows.length === 0) return 'no_rows';

            var firstRow = rows[0];
            var checkbox = firstRow.querySelector('#checkbox, ytcp-checkbox-lit, [type="checkbox"]');
            if (checkbox) {
                checkbox.click();
                return 'selected';
            }

            // Try clicking the row's checkbox area
            var checkArea = firstRow.querySelector('.checkbox-cell, .selection-checkbox');
            if (checkArea) {
                checkArea.click();
                return 'selected_area';
            }

            return 'checkbox_not_found';
        """)

        if 'not_found' in str(selected):
            print(f"  [WARN] Checkbox nao encontrado, tentando metodo alternativo...")
            # Try selecting via video edit page instead
            if info['ids']:
                vid_id = info['ids'][0]
                success = delete_short_video(driver, vid_id, deleted_count + 1, "?")
                if success:
                    deleted_count += 1
                else:
                    failed_count += 1
                    if failed_count >= 5:
                        print("[ERRO] Muitas falhas seguidas, parando.")
                        break
                continue

        time.sleep(1)

        # Click "More actions" dropdown in the top bar
        driver.execute_script("""
            var moreBtn = document.querySelector('#overflow-menu-button, ytcp-button[icon="more_vert"]');
            if (moreBtn) moreBtn.click();
        """)
        time.sleep(1)

        # Click "Delete forever" / "Excluir definitivamente"
        result = driver.execute_script("""
            var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"]');
            for (var item of items) {
                var txt = (item.textContent || '').trim().toLowerCase();
                if (txt.includes('excluir') || txt.includes('delete')) {
                    item.click();
                    return 'clicked_delete';
                }
            }
            return 'delete_not_found';
        """)

        if 'not_found' in str(result):
            # Fallback: go to video edit page
            if info['ids']:
                vid_id = info['ids'][0]
                success = delete_short_video(driver, vid_id, deleted_count + 1, "?")
                if success:
                    deleted_count += 1
                else:
                    failed_count += 1
                continue

        time.sleep(2)

        # Handle confirmation
        driver.execute_script("""
            var checkboxes = document.querySelectorAll('#confirm-checkbox, ytcp-checkbox-lit, tp-yt-paper-checkbox');
            for (var cb of checkboxes) {
                if (cb.offsetParent !== null) cb.click();
            }
        """)
        time.sleep(1)

        confirm_result = driver.execute_script("""
            var btns = document.querySelectorAll('ytcp-button, button');
            for (var b of btns) {
                if (b.offsetParent === null) continue;
                var txt = (b.textContent || '').trim().toLowerCase();
                if (txt.includes('excluir') || txt.includes('delete')) {
                    var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                    if (!disabled) {
                        b.click();
                        return 'confirmed';
                    }
                }
            }
            return 'not_confirmed';
        """)

        if 'confirmed' in str(confirm_result):
            deleted_count += 1
            failed_count = 0
            print(f"  [OK] Short deletado ({deleted_count} total)")
            time.sleep(3)
        else:
            failed_count += 1
            print(f"  [FALHA] Nao confirmou exclusao ({confirm_result})")
            if failed_count >= 5:
                print("[ERRO] Muitas falhas, parando.")
                break
            time.sleep(2)

    return deleted_count


def collect_remaining_videos(driver):
    """After deleting shorts, collect all remaining video IDs."""
    print("\n[SCAN] Coletando videos restantes no canal...")

    driver.get("https://studio.youtube.com/channel/UC/content/videos")
    time.sleep(8)

    all_videos = {}
    last_count = 0
    no_change = 0

    for scroll in range(100):
        videos = driver.execute_script("""
            var results = [];
            var rows = document.querySelectorAll('ytcp-video-row');
            for (var row of rows) {
                var link = row.querySelector('a[href*="/video/"]');
                var titleEl = row.querySelector('#video-title, .video-title-wrapper a, h3 a');

                var id = '';
                if (link) {
                    var match = link.getAttribute('href').match(/\\/video\\/([a-zA-Z0-9_-]+)/);
                    if (match) id = match[1];
                }

                var title = titleEl ? (titleEl.textContent || '').trim() : '';
                if (id) results.push({id: id, title: title});
            }
            return JSON.stringify(results);
        """)

        for v in json.loads(videos):
            all_videos[v['id']] = v['title']

        if len(all_videos) == last_count:
            no_change += 1
            if no_change >= 3:
                break
        else:
            no_change = 0
            last_count = len(all_videos)

        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

        if scroll % 10 == 0:
            print(f"  [SCAN] Scroll {scroll} - {len(all_videos)} videos encontrados...")

    print(f"[SCAN] Total de videos restantes: {len(all_videos)}")
    return all_videos


def collect_playlists(driver):
    """Collect all playlists from YouTube Studio."""
    print("\n[SCAN] Coletando playlists...")

    driver.get("https://studio.youtube.com/channel/UC/content/playlists")
    time.sleep(8)

    playlists = driver.execute_script("""
        var results = [];
        var rows = document.querySelectorAll('ytcp-playlist-row, .playlist-row');
        for (var row of rows) {
            var link = row.querySelector('a[href*="/playlist/"]');
            var titleEl = row.querySelector('.playlist-title, h3 a, a[href*="playlist"]');

            var id = '';
            if (link) {
                var match = link.getAttribute('href').match(/\\/playlist\\/([a-zA-Z0-9_-]+)/);
                if (match) id = match[1];
            }

            var title = titleEl ? (titleEl.textContent || '').trim() : '';
            var countEl = row.querySelector('.video-count, .count');
            var count = countEl ? (countEl.textContent || '').trim() : '';

            if (id || title) results.push({id: id, title: title, count: count});
        }
        return JSON.stringify(results);
    """)

    pl = json.loads(playlists)
    print(f"[SCAN] {len(pl)} playlists encontradas")
    for p in pl:
        print(f"  - {p['title']} ({p['count']}) [ID: {p['id']}]")
    return pl


def analyze_missing_videos(remaining_videos, client_videos, upload_progress):
    """Compare remaining videos against the full portfolio."""
    print("\n" + "=" * 60)
    print("ANALISE DE VIDEOS FALTANTES")
    print("=" * 60)

    uploaded = upload_progress.get('uploaded', {})

    # Map uploaded video IDs to their keys
    uploaded_ids = {}
    for key, val in uploaded.items():
        vid = val.get('video_id', '')
        if vid and vid != 'UPLOADED_NO_ID':
            uploaded_ids[vid] = key

    remaining_ids = set(remaining_videos.keys())

    report = {
        'total_portfolio': 0,
        'total_on_channel': len(remaining_ids),
        'clients': {}
    }

    total_missing = 0
    total_present = 0

    for client, videos in client_videos.items():
        expected = len(videos)
        report['total_portfolio'] += expected

        # Find which videos from this client are on the channel
        present = []
        missing = []

        for idx, video in enumerate(videos):
            key = f"{client}_{idx+1:03d}"
            upload_info = uploaded.get(key)

            if upload_info:
                vid_id = upload_info.get('video_id', '')
                if vid_id and vid_id != 'UPLOADED_NO_ID' and vid_id in remaining_ids:
                    present.append({
                        'index': idx + 1,
                        'video_id': vid_id,
                        'title': upload_info.get('title', ''),
                        'talento': video.get('talento', '')
                    })
                else:
                    missing.append({
                        'index': idx + 1,
                        'talento': video.get('talento', ''),
                        'uploaded_but_deleted': vid_id != '' and vid_id != 'UPLOADED_NO_ID'
                    })
            else:
                missing.append({
                    'index': idx + 1,
                    'talento': video.get('talento', ''),
                    'uploaded_but_deleted': False
                })

        total_present += len(present)
        total_missing += len(missing)

        status = "OK" if not missing else f"FALTA {len(missing)}"
        print(f"\n{client}: {len(present)}/{expected} ({status})")

        if missing:
            for m in missing:
                reason = " (foi enviado mas deletado)" if m['uploaded_but_deleted'] else " (nunca enviado)"
                print(f"  FALTA #{m['index']:03d} - {m['talento']}{reason}")

        report['clients'][client] = {
            'expected': expected,
            'present': len(present),
            'missing': len(missing),
            'missing_details': missing
        }

    print(f"\n{'=' * 60}")
    print(f"RESUMO:")
    print(f"  Portfolio total: {report['total_portfolio']} videos")
    print(f"  No canal: {report['total_on_channel']} videos")
    print(f"  Presentes: {total_present}")
    print(f"  Faltantes: {total_missing}")
    print(f"{'=' * 60}")

    # Save report
    with open('missing_videos_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print("\n[SAVE] Relatorio salvo em missing_videos_report.json")

    return report


def main():
    print("=" * 60)
    print("DELETE ALL SHORTS + ANALYZE MISSING VIDEOS")
    print("=" * 60)

    # Load data
    with open('client_videos.json', 'r', encoding='utf-8') as f:
        client_videos = json.load(f)

    with open('upload_progress.json', 'r', encoding='utf-8') as f:
        upload_progress = json.load(f)

    total_portfolio = sum(len(v) for v in client_videos.values())
    total_uploaded = len(upload_progress.get('uploaded', {}))
    print(f"Portfolio: {total_portfolio} videos | Enviados: {total_uploaded}")
    print()

    # Create driver
    driver = create_driver()

    try:
        # Step 1: Navigate to YouTube Studio
        if not navigate_to_studio_content(driver):
            print("[ERRO] Nao conseguiu acessar YouTube Studio. Verifique o login.")
            return

        # Step 2: Take screenshot to see current state
        driver.save_screenshot("debug_studio_content.png")
        print("[DEBUG] Screenshot: debug_studio_content.png")

        # Step 3: Delete all shorts
        print("\n" + "=" * 60)
        print("FASE 1: DELETAR TODOS OS SHORTS")
        print("=" * 60)

        deleted = delete_all_shorts_via_content_page(driver)
        print(f"\n[RESULTADO] {deleted} Shorts deletados")

        # Step 4: Collect remaining videos
        print("\n" + "=" * 60)
        print("FASE 2: COLETAR VIDEOS RESTANTES")
        print("=" * 60)

        remaining = collect_remaining_videos(driver)

        # Save remaining videos
        with open('remaining_videos.json', 'w', encoding='utf-8') as f:
            json.dump(remaining, f, indent=2, ensure_ascii=False)
        print("[SAVE] Videos restantes salvos em remaining_videos.json")

        # Step 5: Collect playlists
        playlists = collect_playlists(driver)
        with open('channel_playlists.json', 'w', encoding='utf-8') as f:
            json.dump(playlists, f, indent=2, ensure_ascii=False)

        # Step 6: Analyze missing videos
        report = analyze_missing_videos(remaining, client_videos, upload_progress)

        # Step 7: Update upload_progress to remove deleted videos
        print("\n[UPDATE] Atualizando upload_progress.json...")
        updated_progress = {"uploaded": {}}
        removed_count = 0
        for key, val in upload_progress.get('uploaded', {}).items():
            vid_id = val.get('video_id', '')
            if vid_id and vid_id != 'UPLOADED_NO_ID' and vid_id in remaining:
                updated_progress['uploaded'][key] = val
            else:
                removed_count += 1
                print(f"  Removido do progresso: {key} ({vid_id})")

        with open('upload_progress.json', 'w', encoding='utf-8') as f:
            json.dump(updated_progress, f, indent=2, ensure_ascii=False)
        print(f"[UPDATE] {removed_count} entradas removidas do progresso")

        # Also update all_video_ids.json
        with open('all_video_ids.json', 'w', encoding='utf-8') as f:
            json.dump(list(remaining.keys()), f, indent=2, ensure_ascii=False)
        print("[UPDATE] all_video_ids.json atualizado")

    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        try:
            driver.save_screenshot("debug_error.png")
        except Exception:
            pass
    finally:
        print("\n[BROWSER] Chrome permanece aberto para verificacao.")


if __name__ == "__main__":
    main()
