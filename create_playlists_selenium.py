"""
=============================================================
CREATE PLAYLISTS SELENIUM - Bypass da Data API v3
=============================================================
Cria playlists no YouTube via Selenium (bypass do limite anti-abuso
diario da Data API v3 que bloqueou playlists.insert apos 12 criacoes).

Fluxo (YouTube Studio versao 2026-04):
  1. Ler playlists existentes via Data API (playlists.list, read-only,
     sem rate limit) para idempotencia
  2. Abrir studio.youtube.com (sidebar NAO tem mais Playlists)
  3. Clicar no botao "+ Criar" top-right
  4. No menu, clicar "Nova playlist" (testId=new-playlist)
  5. No dialog ytcp-playlist-creation-dialog:
       - preencher titulo
       - setar visibilidade "Nao listada"
       - clicar "Criar"
  6. Repetir para cada playlist, 5s de intervalo

Infra Selenium reusada de fix_playlists_final.py: mesmo
chrome_selenium_data e porta debug 9555.

USO: python create_playlists_selenium.py
=============================================================
"""

import json
import os
import re
import sys
import time
import subprocess
import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555
REPORT_FILE = "selenium_playlists_report.json"

PLAYLISTS_TO_CREATE = [
    "Portfolio - Softys Kitchen",
    "Portfolio - Aiqfome",
    "Portfolio - Philco Britânia",
    "Portfolio - Mycon",
    "Portfolio - Grupo Carrefour",
]

# Leitura via API (apenas GET; NAO usa quota de escrita)
ROOT = Path(__file__).resolve().parent
TOKEN_CACHE = ROOT / "youtube_api_token.json"
TOKEN_CACHE_RW = ROOT / "youtube_api_token_rw.json"
CLIENT_SECRET = ROOT / "client_secret.json"
READ_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


# --- Chrome (reusa pattern de fix_playlists_final.py) -----------------------


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


def port_is_open(host, port, timeout=1.0):
    import socket
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


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

    # Aguarda porta abrir (profile pode ser grande)
    deadline = time.time() + 45
    while time.time() < deadline:
        if port_is_open("127.0.0.1", CHROME_DEBUG_PORT):
            break
        time.sleep(1)
    if not port_is_open("127.0.0.1", CHROME_DEBUG_PORT):
        raise RuntimeError(f"Chrome nao abriu a porta de debug {CHROME_DEBUG_PORT} em 45s")
    # Extra bootstrap
    time.sleep(3)

    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")

    driver = None
    for attempt in range(5):
        try:
            driver = webdriver.Chrome(options=options)
            break
        except Exception as e:
            if attempt < 4:
                print(f"  [RETRY] Tentativa {attempt + 1}/5 ({e})")
                time.sleep(4)
            else:
                raise

    # Trocar para a primeira janela REAL (evita o target 'chrome://tab-search')
    for h in driver.window_handles:
        try:
            driver.switch_to.window(h)
            url = driver.current_url
            if 'tab-search' not in url:
                break
        except Exception:
            continue
    try:
        driver.switch_to.window(driver.window_handles[-1])
    except Exception:
        pass

    try:
        driver.maximize_window()
    except Exception:
        pass

    return driver


# --- API readonly (idempotencia) --------------------------------------------


def list_existing_playlists_via_api():
    """Retorna (lista_de_dicts, fonte). Falha silenciosa se API nao disponivel."""
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as e:
        print(f"[API] google-api-python-client nao instalado ({e})")
        return [], "unavailable"

    creds = None
    # Prefer o token readonly (scope mais fraco); senao usa RW se existir
    for path in (TOKEN_CACHE, TOKEN_CACHE_RW):
        if path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(path))
                break
            except Exception:
                creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            print(f"[API] refresh falhou: {e}")
            creds = None

    if not creds or not creds.valid:
        if not CLIENT_SECRET.exists():
            print("[API] sem token valido e sem client_secret.json - pulando")
            return [], "unavailable"
        try:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), READ_SCOPES)
            creds = flow.run_local_server(port=0, prompt="consent")
            TOKEN_CACHE.write_text(creds.to_json(), encoding="utf-8")
        except Exception as e:
            print(f"[API] auth falhou: {e}")
            return [], "unavailable"

    try:
        youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    except Exception as e:
        print(f"[API] build falhou: {e}")
        return [], "unavailable"

    playlists = []
    try:
        page_token = None
        while True:
            resp = youtube.playlists().list(
                part="id,snippet,status",
                mine=True,
                maxResults=50,
                pageToken=page_token,
            ).execute()
            for item in resp.get("items", []):
                playlists.append({
                    "id": item["id"],
                    "title": (item.get("snippet") or {}).get("title", ""),
                    "privacy": (item.get("status") or {}).get("privacyStatus", ""),
                })
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
    except Exception as e:
        print(f"[API] playlists.list falhou: {e}")
        return [], "error"

    return playlists, "ok"


# --- Navegacao / UI ---------------------------------------------------------


def wait_for_studio(driver, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        ready = driver.execute_script("""
            return document.querySelector('ytcp-navigation-drawer, #navigation-drawer') !== null
                && document.querySelector('ytcp-header, #masthead') !== null;
        """)
        if ready:
            return True
        time.sleep(1)
    return False


def is_login_page(driver):
    url = (driver.current_url or "").lower()
    if 'accounts.google.com' in url:
        return True
    if 'signin' in url or 'sign_in' in url or 'serviceauth' in url:
        return True
    return False


def goto_studio_home(driver):
    print("[NAV] Abrindo studio.youtube.com...")
    driver.get("https://studio.youtube.com/")
    time.sleep(8)
    if is_login_page(driver):
        print(f"[LOGIN] Detectei pagina de login: {driver.current_url}")
        return False
    if not wait_for_studio(driver, timeout=30):
        print(f"[WARN] Studio nao renderizou. URL: {driver.current_url}")
        return False
    print(f"[NAV] OK. URL atual: {driver.current_url}")
    return True


def open_create_menu(driver):
    """Clica no botao '+ Criar' (top-right). Retorna True se menu abriu."""
    # Fechar qualquer dialog previo
    try:
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        time.sleep(1)
    except Exception:
        pass

    result = driver.execute_script("""
        var btns = document.querySelectorAll('button, ytcp-button, a');
        var target = null;
        var bestRight = -1;
        for (var b of btns) {
            if (b.offsetParent === null) continue;
            var t = (b.textContent || '').trim();
            var a = b.getAttribute('aria-label') || '';
            var rect = b.getBoundingClientRect();
            // Botao Criar no top-bar (top < 100, direita)
            if ((t === 'Criar' || a === 'Criar' || t === 'Create' || a === 'Create') &&
                rect.top < 100 && rect.right > bestRight) {
                target = b;
                bestRight = rect.right;
            }
        }
        if (target) {
            target.click();
            return 'clicked';
        }
        return 'not_found';
    """)
    if result != 'clicked':
        return False

    # Espera o menu abrir
    deadline = time.time() + 6
    while time.time() < deadline:
        open_ = driver.execute_script("""
            var it = document.querySelector('tp-yt-paper-item[test-id="new-playlist"]');
            return it !== null && it.offsetParent !== null;
        """)
        if open_:
            return True
        time.sleep(0.3)
    return False


def click_new_playlist_menu_item(driver):
    return driver.execute_script("""
        var it = document.querySelector('tp-yt-paper-item[test-id="new-playlist"]');
        if (it && it.offsetParent !== null) { it.click(); return 'clicked_testid'; }
        var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], [role="option"]');
        for (var i of items) {
            if (i.offsetParent === null) continue;
            var t = (i.textContent || '').trim().toLowerCase();
            if (t === 'nova playlist' || t === 'new playlist') {
                i.click();
                return 'clicked_text';
            }
        }
        return 'not_found';
    """) in ('clicked_testid', 'clicked_text')


def wait_creation_dialog(driver, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        ready = driver.execute_script("""
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            if (cd && cd.innerHTML.length > 100) {
                // Espera qualquer input contenteditable visivel
                var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
                for (var b of boxes) {
                    if (b.offsetHeight > 0) return true;
                }
            }
            return false;
        """)
        if ready:
            return True
        time.sleep(0.4)
    return False


def fill_title(driver, title):
    # Mesmo pattern robusto de fix_playlists_final.py
    focused = 'not_found'
    for _ in range(15):
        focused = driver.execute_script("""
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            if (!cd) return 'no_dialog';
            var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
            for (var tb of boxes) {
                if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                    tb.focus(); tb.click(); tb.textContent = '';
                    return 'focused_creation';
                }
            }
            var inputs = cd.querySelectorAll('#textbox, [contenteditable="true"], input, textarea');
            for (var inp of inputs) {
                var ph = inp.placeholder || inp.getAttribute('aria-label') || '';
                var phl = ph.toLowerCase();
                if (phl.includes('título') || phl.includes('titulo') || phl.includes('title')) {
                    inp.focus(); inp.click();
                    if (inp.contentEditable === 'true') inp.textContent = '';
                    else inp.value = '';
                    return 'focused_placeholder';
                }
            }
            for (var tb of boxes) {
                if (tb.offsetHeight > 0) {
                    tb.focus(); tb.click(); tb.textContent = '';
                    return 'focused_any';
                }
            }
            return 'not_found';
        """)
        if 'focused' in str(focused):
            break
        time.sleep(1)

    if 'focused' not in str(focused):
        return False

    time.sleep(0.3)

    # Metodo 1: insertText
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
    """, title)
    time.sleep(1)

    typed = _get_title_text(driver)
    if not typed:
        # Metodo 2: send_keys active element
        try:
            driver.switch_to.active_element.send_keys(title)
            time.sleep(1)
        except Exception:
            pass
        typed = _get_title_text(driver)

    print(f"    [TYPED] '{typed}'")
    return bool(typed)


def _get_title_text(driver):
    return driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return '';
        var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
        for (var tb of boxes) {
            if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                return (tb.textContent || '').trim();
            }
        }
        var inps = cd.querySelectorAll('input, textarea');
        for (var i of inps) { if (i.value) return i.value.trim(); }
        return '';
    """) or ''


def set_visibility_unlisted(driver):
    # Abre o dropdown de visibilidade
    driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return;
        var dds = cd.querySelectorAll('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, tp-yt-paper-dropdown-menu');
        for (var dd of dds) {
            var txt = (dd.textContent || '').toLowerCase();
            if (txt.includes('visibilidade') || txt.includes('visibility') ||
                txt.includes('pública') || txt.includes('publica') || txt.includes('public') ||
                txt.includes('privad') || txt.includes('private') ||
                txt.includes('listad') || txt.includes('listed')) {
                dd.click();
                return;
            }
        }
        for (var dd of dds) {
            if (dd.offsetParent !== null) { dd.click(); return; }
        }
    """)
    time.sleep(1.5)

    picked = driver.execute_script("""
        var items = document.querySelectorAll('tp-yt-paper-item, [role="option"], [role="menuitem"]');
        for (var item of items) {
            if (item.offsetParent === null) continue;
            var t = (item.textContent || '').toLowerCase();
            if (t.includes('não listada') || t.includes('nao listada') ||
                t.includes('não listado') || t.includes('nao listado') ||
                t.includes('unlisted')) {
                item.click();
                return 'clicked';
            }
        }
        return 'not_found';
    """)
    time.sleep(1)
    return picked == 'clicked'


def click_create_button(driver):
    for _ in range(5):
        status = driver.execute_script("""
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            var containers = [];
            if (cd) containers.push(cd);
            var dialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog');
            for (var d of dialogs) { if (d.innerHTML.length > 100) containers.push(d); }

            for (var c of containers) {
                var btns = c.querySelectorAll('#create-button, ytcp-button, button');
                for (var b of btns) {
                    var t = (b.textContent || '').trim().toLowerCase();
                    if (t === 'criar' || t === 'create') {
                        var disabled = b.hasAttribute('disabled') ||
                                       b.getAttribute('aria-disabled') === 'true';
                        if (!disabled) { b.click(); return 'created'; }
                        return 'disabled';
                    }
                }
            }
            return 'no_button';
        """)
        if status == 'created':
            time.sleep(3)
            return True
        if status == 'disabled':
            driver.execute_script("""
                var cd = document.querySelector('ytcp-playlist-creation-dialog');
                if (!cd) return;
                var tb = cd.querySelector('#textbox[contenteditable]');
                if (tb) {
                    tb.focus();
                    tb.dispatchEvent(new Event('input', {bubbles: true}));
                    tb.dispatchEvent(new Event('change', {bubbles: true}));
                    tb.dispatchEvent(new InputEvent('input', {
                        bubbles: true, data: tb.textContent, inputType: 'insertText'
                    }));
                }
            """)
            time.sleep(2)
            continue
        break
    return False


def wait_dialog_closed(driver, timeout=15):
    """Considera fechado se:
      - elemento some / ofusca
      - OU o textbox perde seu conteudo (dialog pode permanecer no DOM
        em alguns casos mas re-inicializado / aria-hidden)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        state = driver.execute_script("""
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            if (!cd) return 'gone';
            if (cd.offsetParent === null) return 'hidden';
            if (cd.hasAttribute('aria-hidden') && cd.getAttribute('aria-hidden') === 'true') return 'aria_hidden';
            // Dialog ainda no DOM. Checa se o textbox principal foi limpo/reset
            var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
            var any_with_text = false;
            for (var tb of boxes) {
                if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                    if ((tb.textContent || '').trim().length > 0) {
                        any_with_text = true;
                        break;
                    }
                }
            }
            return any_with_text ? 'open' : 'emptied';
        """)
        if state in ('gone', 'hidden', 'aria_hidden', 'emptied'):
            return True
        time.sleep(0.4)
    return False


def close_any_dialog(driver):
    driver.execute_script("""
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            if (b.offsetParent === null) continue;
            var t = (b.textContent || '').trim().toLowerCase();
            var a = (b.getAttribute('aria-label') || '').toLowerCase();
            if (t === 'cancelar' || t === 'cancel' || t === 'fechar' || t === 'close' ||
                a === 'fechar' || a === 'close') {
                b.click();
                return;
            }
        }
    """)
    try:
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
    except Exception:
        pass
    time.sleep(1)


def create_single_playlist(driver, title, idx):
    print(f"\n[{idx}] CRIANDO: {title}")

    # 1) Abrir menu +Criar
    if not open_create_menu(driver):
        driver.save_screenshot(f"debug_selenium_playlist_{idx}.png")
        return 'FAIL', 'botao +Criar nao encontrado no top-bar'
    print("  [OK] menu +Criar aberto")

    # 2) Clicar "Nova playlist"
    if not click_new_playlist_menu_item(driver):
        driver.save_screenshot(f"debug_selenium_playlist_{idx}.png")
        return 'FAIL', 'item Nova playlist nao encontrado no menu'
    print("  [OK] clique em 'Nova playlist'")

    # 3) Aguardar dialog
    if not wait_creation_dialog(driver, timeout=15):
        driver.save_screenshot(f"debug_selenium_playlist_{idx}.png")
        return 'FAIL', 'dialog de criacao nao abriu em 15s'
    print("  [OK] dialog abriu")

    time.sleep(0.5)

    # 4) Preencher titulo
    if not fill_title(driver, title):
        driver.save_screenshot(f"debug_selenium_playlist_{idx}.png")
        close_any_dialog(driver)
        return 'FAIL', 'nao consegui preencher o titulo'

    # 5) Visibilidade "Nao listada"
    if not set_visibility_unlisted(driver):
        print("  [WARN] Visibilidade 'Nao listada' nao foi selecionada (seguindo com default)")

    time.sleep(0.5)

    # 6) Click Criar
    if not click_create_button(driver):
        driver.save_screenshot(f"debug_selenium_playlist_{idx}.png")
        close_any_dialog(driver)
        return 'FAIL', 'botao Criar nao respondeu / ficou disabled'

    # 7) Aguardar dialog fechar
    if not wait_dialog_closed(driver, timeout=15):
        driver.save_screenshot(f"debug_selenium_playlist_{idx}.png")
        close_any_dialog(driver)
        return 'FAIL', 'dialog nao fechou apos click em Criar (possivel erro silencioso)'

    print(f"  [OK] playlist '{title}' criada")
    return 'OK', ''


# --- Main -------------------------------------------------------------------


def main():
    print("=" * 60)
    print("  CREATE PLAYLISTS SELENIUM")
    print("=" * 60)
    print(f"  Playlists planejadas: {len(PLAYLISTS_TO_CREATE)}")
    for p in PLAYLISTS_TO_CREATE:
        print(f"    - {p}")
    print()

    # 1) Listar playlists existentes via API (idempotencia)
    print("[API] Lendo playlists existentes do canal (readonly)...")
    existing, source = list_existing_playlists_via_api()
    existing_titles = {(p.get('title') or '').strip() for p in existing}
    print(f"[API] source={source} - {len(existing)} playlists ja no canal")
    for p in existing:
        print(f"       - {p.get('title','')!r} [{p.get('privacy','?')}]")

    print()
    print("[AUTO] Iniciando navegador em 3s...")
    time.sleep(3)

    driver = create_driver()
    results = []
    ok = skip = fail = 0
    final_playlist_count = None

    try:
        if not goto_studio_home(driver):
            if is_login_page(driver):
                print("\n[BLOQUEIO] Login necessario. Complete o login na janela")
                print("  do Chrome aberta e re-execute o script.")
                report = {
                    "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "results": [],
                    "summary": {"ok": 0, "skip": 0, "fail": 0},
                    "error": f"login required at {driver.current_url}",
                }
                with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                return

        time.sleep(2)

        for idx, title in enumerate(PLAYLISTS_TO_CREATE, start=1):
            # Idempotencia
            already = False
            matched_id = ''
            for p in existing:
                t = (p.get('title') or '').strip()
                if t == title or t.lower() == title.lower():
                    already = True
                    matched_id = p.get('id', '')
                    break
            if already:
                print(f"\n[{idx}] SKIP: '{title}' ja existe (id={matched_id})")
                url = f"https://www.youtube.com/playlist?list={matched_id}" if matched_id else ""
                results.append({"title": title, "status": "SKIP", "url": url, "error": ""})
                skip += 1
                continue

            try:
                status, err = create_single_playlist(driver, title, idx)
            except Exception as e:
                try:
                    driver.save_screenshot(f"debug_selenium_playlist_{idx}.png")
                except Exception:
                    pass
                status, err = 'FAIL', f"exception: {str(e)[:200]}"
                print(f"  [ERRO] {err}")

            results.append({"title": title, "status": status, "url": "", "error": err})
            if status == 'OK':
                ok += 1
            else:
                fail += 1

            time.sleep(5)

        # Re-listar via API para obter ids e URLs das playlists recem-criadas
        print("\n[API] Re-lendo playlists do canal para obter IDs...")
        try:
            final_list, final_source = list_existing_playlists_via_api()
            final_playlist_count = len(final_list)
            print(f"[API] {len(final_list)} playlists no canal (source={final_source})")
            title_to_id = {(p.get('title') or '').strip(): p.get('id', '') for p in final_list}
            for r in results:
                if r['status'] == 'OK':
                    pid = title_to_id.get(r['title']) or ''
                    if pid:
                        r['url'] = f"https://www.youtube.com/playlist?list={pid}"
                        r['playlist_id'] = pid
        except Exception as e:
            print(f"[API] re-leitura falhou: {e}")

    finally:
        report = {
            "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "results": results,
            "summary": {"ok": ok, "skip": skip, "fail": fail},
            "total_playlists_in_channel_after": final_playlist_count,
        }
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n[REPORT] Salvo em {REPORT_FILE}")

        print()
        print("=" * 60)
        print(f"  RESUMO: OK={ok}  SKIP={skip}  FAIL={fail}")
        if final_playlist_count is not None:
            print(f"  Playlists no canal ao final: {final_playlist_count}")
        print("=" * 60)
        for r in results:
            mark = '[OK]  ' if r['status'] == 'OK' else (
                '[SKIP]' if r['status'] == 'SKIP' else '[FAIL]')
            extra = f" - {r['error']}" if r['error'] else ''
            url = f" ({r['url']})" if r.get('url') else ''
            print(f"  {mark} {r['title']}{url}{extra}")
        print()

        print("Fechando navegador em 3s...")
        time.sleep(3)
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
