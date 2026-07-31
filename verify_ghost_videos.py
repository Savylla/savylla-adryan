"""
Verifica se os 11 videos "fantasma" realmente existem no YouTube Studio
buscando pelo titulo na pagina de conteudo.
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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555

GHOST_VIDEOS = [
    {"id": "T2Wv0fEq9kA", "client": "Drogasil", "title": "Drogasil - Livia Lima - RAIA Cuidado que vale mais Drogasil v2 46s", "talento": "Livia Lima"},
    {"id": "y24LYqbuk4M", "client": "Drogasil", "title": "Drogasil - Frederico Volkmann - RAIA - Cuidado que vale mais - Drogasil v3 46s", "talento": "Frederico Volkmann"},
    {"id": "s4JwRPXRCZA", "client": "Drogasil", "title": "Drogasil - Carolina Cruz - RAIA - Marcas Coreanas - Drogasil v2 27s", "talento": "Carolina Cruz"},
    {"id": "_aTr2OMEiPs", "client": "Drogasil", "title": "Drogasil - Livia Lima - RAIA Cuidado que vale mais Drogasil v3 43s", "talento": "Livia Lima"},
    {"id": "UPLOADED_NO_ID", "client": "Raia", "title": "Raia - Quezia Castro - Raia - Raia Varejar v2 48s", "talento": "Quezia Castro"},
    {"id": "jG_zV5uWkeg", "client": "Raia", "title": "Raia - Karol Alves - RAIA Autosserviço AlwaysOn Infantil v1 31s", "talento": "Karol Alves"},
    {"id": "1vOigJpl8HE", "client": "Raia", "title": "Raia - Loretta Martins - Raia - Raia Varejar v2 34s", "talento": "Loretta Martins"},
    {"id": "qNGAdAOIgL8", "client": "Raia", "title": "Raia - Loretta Martins - Raia - Raia Varejar v2 23", "talento": "Loretta Martins"},
    {"id": "txcLjBXNz4c", "client": "Raia", "title": "Raia - Frederico Volkmann - Raia - Raia Varejar v3 38s", "talento": "Frederico Volkmann"},
    {"id": "UPzGBiPF470", "client": "Raia", "title": "Raia - Frederico Volkmann - Raia - Raia Varejar v42 40s", "talento": "Frederico Volkmann"},
    {"id": "-t6zB2LSDvA", "client": "Garagem Coletiva", "title": "Garagem Coletiva - Presente de Aniversário - video-6", "talento": "Presente de Aniversário"},
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
    custom_data_dir = os.path.join(os.path.expanduser("~"), "chrome_selenium_data")
    os.makedirs(custom_data_dir, exist_ok=True)

    print("[BROWSER] Fechando Chrome existente...")
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

    for attempt in range(5):
        try:
            driver = webdriver.Chrome(options=options)
            try:
                driver.maximize_window()
            except Exception:
                pass
            return driver
        except Exception as e:
            if attempt < 4:
                time.sleep(5)
            else:
                raise e


def search_video_in_studio(driver, search_term):
    """Search for a video by title in YouTube Studio content page.
    Returns list of matching video titles found."""

    # Navigate to content page with search
    # YouTube Studio search is via the filter/search bar on the videos page
    driver.get("https://studio.youtube.com/channel/videos")
    time.sleep(4)

    # Click on the search/filter input
    search_clicked = driver.execute_script("""
        // Try the filter/search input
        var searchInput = document.querySelector(
            '#text-input, input[type="search"], input[placeholder*="Filtrar"], input[placeholder*="Filter"], ' +
            'ytcp-text-field input, #search-input'
        );
        if (searchInput) {
            searchInput.focus();
            searchInput.click();
            return 'found_input';
        }
        // Try filter button
        var filterBtn = document.querySelector(
            '#filter-button, [aria-label*="Filtrar"], [aria-label*="Filter"], ' +
            'button[aria-label*="pesquisar"], button[aria-label*="search"]'
        );
        if (filterBtn) {
            filterBtn.click();
            return 'clicked_filter';
        }
        return 'not_found';
    """)
    time.sleep(1)

    # Type search term using a unique part of the title
    try:
        active = driver.switch_to.active_element
        active.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.2)
        active.send_keys(search_term)
        time.sleep(0.3)
        active.send_keys(Keys.ENTER)
    except Exception:
        # Fallback: try to find and fill the input via JS
        driver.execute_script("""
            var inputs = document.querySelectorAll('input[type="text"], input[type="search"], #text-input');
            for (var inp of inputs) {
                if (inp.offsetParent !== null) {
                    inp.focus();
                    inp.value = arguments[0];
                    inp.dispatchEvent(new Event('input', {bubbles: true}));
                    inp.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', bubbles: true}));
                    return;
                }
            }
        """, search_term)

    time.sleep(4)

    # Read results
    results = driver.execute_script("""
        var videos = [];
        // Look for video rows in the content table
        var rows = document.querySelectorAll(
            'ytcp-video-row, tr.video-row, .video-row, [class*="video-row"]'
        );
        for (var r of rows) {
            var titleEl = r.querySelector(
                'a#video-title, .video-title, a[href*="/video/"], #video-title, ' +
                'ytcp-video-list-cell-video a, h3 a'
            );
            if (titleEl) {
                var title = titleEl.textContent.trim();
                var href = titleEl.href || '';
                var vidMatch = href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                var vidId = vidMatch ? vidMatch[1] : '';
                if (title) {
                    videos.push({title: title.substring(0, 100), id: vidId});
                }
            }
        }

        // Fallback: look for any links to videos
        if (videos.length === 0) {
            var links = document.querySelectorAll('a[href*="/video/"]');
            for (var l of links) {
                var txt = l.textContent.trim();
                var href = l.href || '';
                var m = href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                if (txt && txt.length > 5 && txt.length < 200 && m) {
                    videos.push({title: txt.substring(0, 100), id: m[1]});
                }
            }
        }

        // Check if "no results" message is shown
        var noResults = document.querySelectorAll('span, p, div');
        for (var el of noResults) {
            var txt = (el.textContent || '').trim().toLowerCase();
            if (txt.includes('nenhum resultado') || txt.includes('no results') ||
                txt.includes('nenhum vídeo') || txt.includes('no videos')) {
                return {found: false, message: txt.substring(0, 50), videos: []};
            }
        }

        return {found: videos.length > 0, videos: videos};
    """)

    return results


def main():
    print("=" * 60)
    print("  VERIFICAR VIDEOS FANTASMA NO YOUTUBE STUDIO")
    print("=" * 60)
    print(f"  Videos para verificar: {len(GHOST_VIDEOS)}")
    print()

    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

    driver.get("https://studio.youtube.com")
    time.sleep(5)

    channel = driver.execute_script("""
        var el = document.querySelector('ytcp-entity-name, .entity-name, #entity-name');
        return el ? el.textContent.trim() : 'unknown';
    """)
    print(f"[CANAL] {channel}")
    print()

    exists = []
    missing = []

    for i, video in enumerate(GHOST_VIDEOS):
        vid_id = video["id"]
        client = video["client"]
        title = video["title"]
        talento = video["talento"]

        print(f"[{i+1}/{len(GHOST_VIDEOS)}] [{client}] {title[:60]}")

        # Search by a unique part of the title (talento + key words)
        # Use the talento name + client as search to narrow down
        search_terms = []

        # Extract a unique portion: use part after client name
        parts = title.split(" - ")
        if len(parts) >= 3:
            # Use the filename/video part (most unique)
            search_terms.append(parts[-1][:40])
        if talento:
            search_terms.append(talento)

        # Use the most specific search term
        search = search_terms[0] if search_terms else title[:40]

        result = search_video_in_studio(driver, search)

        if result.get("found") and result.get("videos"):
            # Check if any result matches our title closely
            matched = False
            for rv in result["videos"]:
                rv_title = rv.get("title", "")
                rv_id = rv.get("id", "")
                # Check if the result title contains key parts of our expected title
                if (talento.lower() in rv_title.lower() or
                    client.lower() in rv_title.lower() or
                    search.lower() in rv_title.lower()):
                    matched = True
                    actual_id = rv_id
                    print(f"  [EXISTE] Encontrado: {rv_title[:70]}")
                    if actual_id:
                        print(f"  [ID] https://studio.youtube.com/video/{actual_id}/edit")
                    exists.append({
                        "original_id": vid_id,
                        "actual_id": actual_id,
                        "client": client,
                        "title_found": rv_title,
                        "search_used": search
                    })
                    break

            if not matched:
                print(f"  [?] Resultados nao correspondem: {[v['title'][:40] for v in result['videos'][:3]]}")
                # Try second search term
                if len(search_terms) > 1:
                    search2 = search_terms[1]
                    result2 = search_video_in_studio(driver, search2)
                    if result2.get("found") and result2.get("videos"):
                        for rv in result2["videos"]:
                            rv_title = rv.get("title", "")
                            rv_id = rv.get("id", "")
                            if (talento.lower() in rv_title.lower() or
                                client.lower() in rv_title.lower()):
                                matched = True
                                print(f"  [EXISTE] Encontrado (2a busca): {rv_title[:70]}")
                                if rv_id:
                                    print(f"  [ID] https://studio.youtube.com/video/{rv_id}/edit")
                                exists.append({
                                    "original_id": vid_id,
                                    "actual_id": rv_id,
                                    "client": client,
                                    "title_found": rv_title,
                                    "search_used": search2
                                })
                                break

                if not matched:
                    print(f"  [NAO ENCONTRADO]")
                    missing.append(video)
        else:
            msg = result.get("message", "sem resultados")
            print(f"  [NAO ENCONTRADO] {msg}")
            missing.append(video)

        time.sleep(2)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTADO")
    print("=" * 60)
    print(f"  Existem no canal: {len(exists)}")
    print(f"  NAO existem (precisam re-envio): {len(missing)}")
    print()

    if exists:
        print("  EXISTEM (nao precisam re-envio):")
        for v in exists:
            actual = v.get("actual_id", "?")
            link = f"https://studio.youtube.com/video/{actual}/edit" if actual else "ID desconhecido"
            print(f"    [{v['client']}] {v['title_found'][:60]}")
            print(f"      {link}")
        print()

    if missing:
        print("  FALTAM (precisam re-envio):")
        for v in missing:
            print(f"    [{v['client']}] {v['title'][:60]}")
            print(f"      Talento: {v['talento']}")
        print()

    # Save result
    with open("ghost_videos_result.json", "w", encoding="utf-8") as f:
        json.dump({"exists": exists, "missing": missing}, f, indent=2, ensure_ascii=False)
    print("  Resultado salvo em: ghost_videos_result.json")

    print("\nFechando navegador em 5 segundos...")
    time.sleep(5)
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
