"""
=============================================================
DELETE ALL SHORTS - ONE BY ONE
=============================================================
YouTube Studio desabilita "Mais acoes" para Shorts em lote.
Este script coleta todos os IDs de Shorts e deleta um a um
via pagina de edicao do video.

USO: python delete_all_shorts.py
=============================================================
"""

import json
import os
import sys
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

CHROME_DEBUG_PORT = 9555
CHANNEL_ID = "UCaLWwZY1Yn_8svQQevLbMoA"
SHORTS_URL = f"https://studio.youtube.com/channel/{CHANNEL_ID}/videos/short"
PROGRESS_FILE = "shorts_delete_progress.json"


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

    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")

    # Try connecting to existing Chrome first
    print("[BROWSER] Tentando conectar ao Chrome existente...")
    try:
        driver = webdriver.Chrome(options=options)
        print("[BROWSER] Conectado!")
        try:
            driver.maximize_window()
        except Exception:
            pass
        return driver
    except Exception:
        pass

    # Kill and restart
    print("[BROWSER] Iniciando novo Chrome...")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"],
                       capture_output=True, timeout=10)
        time.sleep(5)
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
    subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(15)

    for attempt in range(8):
        try:
            driver = webdriver.Chrome(options=options)
            print("[BROWSER] Conectado!")
            try:
                driver.maximize_window()
            except Exception:
                pass
            return driver
        except Exception:
            if attempt < 7:
                print(f"  [RETRY] {attempt + 1}/8...")
                time.sleep(5)
            else:
                raise


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"deleted": [], "failed": [], "all_shorts": []}


def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def collect_all_short_ids(driver):
    """Scroll through Shorts tab and collect all video IDs."""
    print("\n[SCAN] Coletando todos os IDs de Shorts...")
    driver.get(SHORTS_URL)
    time.sleep(7)

    all_ids = set()
    last_count = 0
    no_change = 0
    page = 1

    while True:
        # Collect IDs from current page
        ids = driver.execute_script(r"""
            var ids = [];
            var rows = document.querySelectorAll("ytcp-video-row");
            for (var row of rows) {
                var link = row.querySelector("a[href*='/video/']");
                if (link) {
                    var match = link.getAttribute("href").match(/\/video\/([a-zA-Z0-9_-]+)/);
                    if (match) ids.push(match[1]);
                }
            }
            return ids;
        """)

        for vid in ids:
            all_ids.add(vid)

        print(f"  [PAGE {page}] {len(ids)} na pagina, {len(all_ids)} total")

        if len(all_ids) == last_count:
            no_change += 1
            if no_change >= 2:
                # Try next page
                has_next = driver.execute_script(r"""
                    var nextBtn = document.querySelector("#navigate-after");
                    if (nextBtn && nextBtn.offsetParent !== null) {
                        var disabled = nextBtn.hasAttribute("disabled");
                        if (!disabled) {
                            nextBtn.click();
                            return true;
                        }
                    }
                    return false;
                """)
                if has_next:
                    time.sleep(4)
                    page += 1
                    no_change = 0
                    last_count = len(all_ids)
                    continue
                else:
                    break
        else:
            no_change = 0
            last_count = len(all_ids)

        # Try scrolling
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)

    # If we only got 30, paginate explicitly
    if len(all_ids) <= 30:
        print("  [PAGINATE] Coletando via paginacao...")
        while True:
            has_next = driver.execute_script(r"""
                var nextBtn = document.querySelector("#navigate-after, ytcp-icon-button#navigate-after");
                if (nextBtn && !nextBtn.hasAttribute("disabled")) {
                    nextBtn.click();
                    return true;
                }
                return false;
            """)
            if not has_next:
                break

            time.sleep(4)
            page += 1

            ids = driver.execute_script(r"""
                var ids = [];
                var rows = document.querySelectorAll("ytcp-video-row");
                for (var row of rows) {
                    var link = row.querySelector("a[href*='/video/']");
                    if (link) {
                        var match = link.getAttribute("href").match(/\/video\/([a-zA-Z0-9_-]+)/);
                        if (match) ids.push(match[1]);
                    }
                }
                return ids;
            """)
            for vid in ids:
                all_ids.add(vid)
            print(f"  [PAGE {page}] {len(ids)} na pagina, {len(all_ids)} total")

    print(f"\n[SCAN] Total: {len(all_ids)} Shorts encontrados")
    return list(all_ids)


def delete_single_short(driver, video_id):
    """Delete a single video via its edit page."""
    edit_url = f"https://studio.youtube.com/video/{video_id}/edit"
    try:
        driver.set_page_load_timeout(30)
        driver.get(edit_url)
    except Exception:
        pass  # Page may timeout but still load enough
    time.sleep(6)

    # Check for error page ("Ops! Algo deu errado" = video already deleted or unavailable)
    is_error = driver.execute_script("""
        var text = document.body ? document.body.innerText : "";
        return text.includes("Algo deu errado") || text.includes("Something went wrong") || text.includes("isn't available");
    """)
    if is_error:
        return "already_gone"

    # Click #overflow-menu-button (kebab menu, aria="Opções")
    # Wait for it to appear
    for wait in range(5):
        clicked = driver.execute_script(r"""
            var btn = document.querySelector("#overflow-menu-button");
            if (btn && btn.offsetParent !== null) {
                btn.click();
                return "ok";
            }
            return "not_found";
        """)
        if clicked == "ok":
            break
        time.sleep(2)

    if clicked == "not_found":
        return "menu_not_found"

    time.sleep(3)

    # Click "Excluir" in the menu - retry up to 3 times with increasing wait
    # Note: some videos (drafts) have menu items with offsetParent=null,
    # so we skip the visibility check and click by text match directly
    result = "not_found"
    for attempt in range(3):
        result = driver.execute_script(r"""
            var items = document.querySelectorAll("tp-yt-paper-item");
            for (var item of items) {
                var txt = (item.textContent || "").trim().toLowerCase();
                if (txt.includes("excluir") || txt === "delete") {
                    item.click();
                    return "ok";
                }
            }
            return "not_found";
        """)
        if result == "ok":
            break
        time.sleep(2)

    if result == "not_found":
        return "delete_btn_not_found"

    time.sleep(2)

    # Check the confirmation checkbox in the dialog
    driver.execute_script(r"""
        var dialogs = document.querySelectorAll("tp-yt-paper-dialog");
        for (var d of dialogs) {
            if (d.getAttribute("aria-hidden") === "true") continue;
            var cbs = d.querySelectorAll("ytcp-checkbox-lit, #confirm-checkbox");
            for (var cb of cbs) {
                cb.click();
                return;
            }
        }
    """)
    time.sleep(1)

    # Click the confirm "Excluir" button in the dialog
    result = driver.execute_script(r"""
        var dialogs = document.querySelectorAll("tp-yt-paper-dialog");
        for (var d of dialogs) {
            if (d.getAttribute("aria-hidden") === "true") continue;
            var btns = d.querySelectorAll("ytcp-button");
            for (var b of btns) {
                var txt = (b.textContent || "").trim().toLowerCase();
                if (txt.includes("excluir") || txt.includes("delete")) {
                    var disabled = b.hasAttribute("disabled") ||
                                   b.getAttribute("aria-disabled") === "true";
                    if (!disabled) {
                        b.click();
                        return "confirmed";
                    }
                    return "disabled";
                }
            }
        }
        return "not_found";
    """)

    if result == "confirmed":
        time.sleep(3)
        return "ok"
    elif result == "disabled":
        # Retry: click checkbox again then confirm
        driver.execute_script(r"""
            var dialogs = document.querySelectorAll("tp-yt-paper-dialog");
            for (var d of dialogs) {
                if (d.getAttribute("aria-hidden") === "true") continue;
                var cbs = d.querySelectorAll("ytcp-checkbox-lit");
                for (var cb of cbs) cb.click();
            }
        """)
        time.sleep(1)
        r2 = driver.execute_script(r"""
            var dialogs = document.querySelectorAll("tp-yt-paper-dialog");
            for (var d of dialogs) {
                if (d.getAttribute("aria-hidden") === "true") continue;
                var btns = d.querySelectorAll("ytcp-button");
                for (var b of btns) {
                    if (b.offsetParent === null) continue;
                    var txt = (b.textContent || "").trim().toLowerCase();
                    if (txt.includes("excluir") && !b.hasAttribute("disabled")) {
                        b.click();
                        return "confirmed";
                    }
                }
            }
            return "failed";
        """)
        if "confirmed" in r2:
            time.sleep(3)
            return "ok"
        return "confirm_failed"
    else:
        return "confirm_not_found"


def main():
    print("=" * 60)
    print("DELETE ALL SHORTS - ONE BY ONE")
    print("=" * 60)

    rescan = "--rescan" in sys.argv

    driver = create_driver()
    progress = load_progress()

    # Clear failed list on each run (they'll be re-tried)
    if progress["failed"]:
        print(f"[RETRY] Limpando {len(progress['failed'])} falhas anteriores para re-tentar")
        progress["failed"] = []
        save_progress(progress)

    try:
        # Collect all short IDs if not already done or --rescan
        if not progress["all_shorts"] or rescan:
            if rescan:
                print("\n[RESCAN] Re-coletando IDs de Shorts (mantendo historico de deletados)...")
            else:
                print("\n[FASE 1] Coletando IDs de todos os Shorts...")
            all_shorts = collect_all_short_ids(driver)
            progress["all_shorts"] = all_shorts
            save_progress(progress)
        else:
            all_shorts = progress["all_shorts"]
            print(f"\n[CACHE] {len(all_shorts)} Shorts ja coletados")

        # Filter out already deleted
        already_deleted = set(progress["deleted"])
        to_delete = [vid for vid in all_shorts if vid not in already_deleted]
        print(f"[INFO] Total: {len(all_shorts)} | Ja deletados: {len(already_deleted)} | Restantes: {len(to_delete)}")

        if not to_delete:
            print("[DONE] Todos os Shorts ja foram deletados!")
            return

        # Delete one by one
        print(f"\n[FASE 2] Deletando {len(to_delete)} Shorts...")
        consecutive_fails = 0

        for i, vid in enumerate(to_delete):
            print(f"\n[{i+1}/{len(to_delete)}] {vid}...", end=" ", flush=True)

            try:
                result = delete_single_short(driver, vid)
            except Exception as e:
                result = f"exception: {str(e)[:50]}"
                # Reconnect driver if needed
                try:
                    driver.current_url
                except Exception:
                    print(f"ERRO (reconectando)...", end=" ", flush=True)
                    try:
                        driver = create_driver()
                    except Exception:
                        print("FALHA ao reconectar")
                        break

            if result == "ok":
                print("DELETADO")
                progress["deleted"].append(vid)
                consecutive_fails = 0
            elif result == "already_gone":
                print("JA REMOVIDO (pagina de erro)")
                progress["deleted"].append(vid)
                consecutive_fails = 0
            else:
                print(f"FALHOU ({result})")
                progress["failed"].append({"id": vid, "reason": result})
                consecutive_fails += 1

                if consecutive_fails >= 10:
                    print("\n[ERRO] 10 falhas consecutivas. Salvando progresso e parando.")
                    try:
                        driver.save_screenshot("debug_consecutive_fails.png")
                    except Exception:
                        pass
                    break

            # Small delay between deletions to avoid rate limiting
            if result == "ok":
                time.sleep(1)

            # Save progress every 5 deletions
            if (i + 1) % 5 == 0:
                save_progress(progress)
                print(f"  [SAVE] Progresso salvo ({len(progress['deleted'])} deletados)")

        # Final save
        save_progress(progress)

        print(f"\n{'='*60}")
        print(f"RESULTADO:")
        print(f"  Deletados: {len(progress['deleted'])}")
        print(f"  Falhas: {len(progress['failed'])}")
        print(f"  Restantes: {len(all_shorts) - len(progress['deleted'])}")
        print(f"{'='*60}")

    except Exception as e:
        save_progress(progress)
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        try:
            driver.save_screenshot("debug_error.png")
        except Exception:
            pass
    finally:
        print("\n[BROWSER] Chrome permanece aberto.")
        print(f"[INFO] Progresso salvo em {PROGRESS_FILE}")
        print("[INFO] Rode novamente para continuar de onde parou.")


if __name__ == "__main__":
    main()
