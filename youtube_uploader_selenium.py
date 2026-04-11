"""
=============================================================
YOUTUBE UPLOADER via Selenium - Portfolio Savylla Adryan
=============================================================
Faz upload dos videos para o YouTube via YouTube Studio
(interface web), SEM usar a API e SEM limite de cota diaria.

SETUP:
1. Instale: python -m pip install selenium requests
2. Tenha o Google Chrome instalado
3. Esteja logado no YouTube no Chrome
4. Execute: python youtube_uploader_selenium.py

NOTA: O script abre o Chrome com seu perfil logado.
      Feche todas as janelas do Chrome antes de executar.
=============================================================
"""

import json
import os
import sys
import time

# Fix Windows console encoding (cp1252 não suporta todos os caracteres Unicode)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
import re
import html
import requests
from pathlib import Path
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# --- CONFIG ---
VIDEOS_JSON = "client_videos.json"
DOWNLOAD_DIR = "downloads"
PROGRESS_FILE = "upload_progress.json"
RESULTS_FILE = "youtube_results.json"

# Delay between uploads (seconds) - be gentle with YouTube
UPLOAD_DELAY = 20
# Max wait for upload to process (seconds)
UPLOAD_TIMEOUT = 900  # 15 min per video

# Chrome user data - uses your logged-in profile
CHROME_USER_DATA = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE = "Profile 6"  # Savylla


def find_chrome():
    """Find Chrome executable."""
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
    """Create Chrome WebDriver by launching Chrome with remote debugging."""
    import subprocess

    chrome_path = find_chrome()
    if not chrome_path:
        raise RuntimeError("Chrome nao encontrado!")

    debug_port = 9555  # Ports 9222/9333 conflict with Adobe UXP
    custom_data_dir = os.path.join(os.path.expanduser("~"), "chrome_selenium_data")
    os.makedirs(custom_data_dir, exist_ok=True)

    # Kill any existing Chrome processes
    print("[BROWSER] Fechando Chrome existente...")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"],
                       capture_output=True, timeout=10)
        time.sleep(3)
    except Exception:
        pass

    # Launch Chrome with custom data dir
    chrome_cmd = [
        chrome_path,
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={custom_data_dir}",
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
        "--log-level=3",
    ]
    print(f"[BROWSER] Iniciando Chrome (porta {debug_port})...")
    subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10)

    # Connect Selenium to the running Chrome
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")

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


def load_videos():
    """Load video list from JSON."""
    with open(VIDEOS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_progress():
    """Load upload progress."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"uploaded": {}, "playlists": {}}


def save_progress(progress):
    """Save progress."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def load_results():
    """Load results."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_results(results):
    """Save results."""
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def clean_url(url):
    """Clean URL removing HTML entities."""
    return html.unescape(url)


def extract_video_name(url):
    """Extract readable name from URL."""
    path = url.split("?")[0]
    filename = path.split("/")[-1]
    filename = unquote(filename)
    name = filename.rsplit(".", 1)[0] if "." in filename else filename
    name = re.sub(r'\[.*?\]', '', name).strip()
    name = re.sub(r'_+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name if name else "Video"


def sanitize_filename(name):
    """Create safe filename."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'_+', '_', name)
    return name[:200]


def is_valid_video(filepath):
    """Check if a file is actually a video (not HTML or other junk)."""
    if not os.path.exists(filepath):
        return False
    size = os.path.getsize(filepath)
    if size < 100000:  # Less than 100KB is not a real video
        return False
    # Check magic bytes
    try:
        with open(filepath, "rb") as f:
            header = f.read(32)
        # Check for HTML (common when auth fails)
        if header.startswith(b'<!') or header.startswith(b'<html') or header.startswith(b'<HTML'):
            return False
        # MP4/MOV: ftyp box
        if b'ftyp' in header[:12]:
            return True
        # WebM
        if header.startswith(b'\x1a\x45\xdf\xa3'):
            return True
        # AVI
        if header[:4] == b'RIFF' and header[8:12] == b'AVI ':
            return True
        # If file is large enough and not HTML, assume it's valid
        if size > 500000:
            return True
        return False
    except Exception:
        return False


def download_video(url, filepath, driver=None):
    """Download video. Uses browser session for ClickUp URLs (which require auth)."""
    clean = clean_url(url)
    if "&sa=D&source=editors" in clean:
        clean = clean.split("&sa=D&source=editors")[0]

    print(f"  [DOWNLOAD] Baixando... ", end="", flush=True)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    is_clickup = "clickup" in clean.lower()

    # For ClickUp URLs, use browser session (requires auth)
    if is_clickup and driver:
        return download_via_browser(driver, clean, filepath)

    # For other URLs, try curl
    return download_via_curl(clean, filepath)


def download_via_browser(driver, url, filepath):
    """Download ClickUp file using the browser (same tab, no popups).
    Navigates to the URL, waits for Chrome to download, then goes back to YouTube."""
    abs_path = os.path.abspath(filepath)
    abs_download_dir = os.path.abspath(DOWNLOAD_DIR)
    os.makedirs(abs_download_dir, exist_ok=True)

    # Remove ?view=open to get direct download
    download_url = url.split("?")[0]

    try:
        # Set Chrome to auto-save downloads to our directory
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": abs_download_dir
        })

        # Record files before download
        files_before = set(os.listdir(abs_download_dir))

        # Navigate directly to the file URL (same tab - no popup issues)
        driver.get(download_url)
        time.sleep(5)

        # Check if we landed on a preview page instead of downloading
        page_url = driver.current_url
        if "clickup" in page_url:
            # Try to find and click a download button
            try:
                driver.execute_script("""
                    var links = document.querySelectorAll('a[href], button, [role="button"]');
                    for (var el of links) {
                        var txt = (el.textContent || '').toLowerCase();
                        var href = (el.href || '').toLowerCase();
                        var dl = el.getAttribute('download');
                        if (dl !== null || txt.includes('download') || txt.includes('baixar')) {
                            el.click(); return true;
                        }
                    }
                    return false;
                """)
            except Exception:
                pass
            time.sleep(3)

        # Wait for download file to appear
        download_found = False
        for wait in range(180):  # Wait up to 3 min
            time.sleep(1)
            files_after = set(os.listdir(abs_download_dir))
            new_files = files_after - files_before

            # Check for completed downloads
            for f in new_files:
                if f.endswith('.crdownload'):
                    continue
                fpath = os.path.join(abs_download_dir, f)
                if os.path.getsize(fpath) > 50000:  # At least 50KB
                    time.sleep(2)
                    if is_valid_video(fpath):
                        if os.path.exists(abs_path):
                            os.remove(abs_path)
                        os.rename(fpath, abs_path)
                        download_found = True
                        break

            if download_found:
                break

            # Show progress for active downloads
            if any(f.endswith('.crdownload') for f in new_files):
                if wait % 20 == 0 and wait > 0:
                    print(f"({wait}s) ", end="", flush=True)
                continue

            # If no activity after 15s, try with ?view=open
            if wait == 15 and not new_files:
                driver.get(url)
                time.sleep(3)
                try:
                    driver.execute_script("""
                        var links = document.querySelectorAll('a[href], button');
                        for (var el of links) {
                            var txt = (el.textContent || '').toLowerCase();
                            if (txt.includes('download') || txt.includes('baixar')) {
                                el.click(); return true;
                            }
                        }
                        return false;
                    """)
                except Exception:
                    pass

            # Give up after 40s with no download activity
            if wait > 40 and not any(f.endswith('.crdownload') for f in (set(os.listdir(abs_download_dir)) - files_before)):
                break

        # Navigate back to YouTube Studio
        driver.get("https://studio.youtube.com")
        time.sleep(5)

        if download_found and os.path.exists(abs_path):
            size_mb = os.path.getsize(abs_path) / (1024 * 1024)
            print(f"OK ({size_mb:.1f} MB)")
            return True

        # Clean up partial downloads
        for f in (set(os.listdir(abs_download_dir)) - files_before):
            try:
                os.remove(os.path.join(abs_download_dir, f))
            except Exception:
                pass

        print("FALHOU (download nao completou)")
        return False

    except Exception as e:
        print(f"ERRO: {e}")
        try:
            driver.get("https://studio.youtube.com")
            time.sleep(5)
        except Exception:
            pass
        try:
            os.remove(abs_path)
        except Exception:
            pass
        return False


def download_via_curl(url, filepath):
    """Download file using curl (for direct/public URLs)."""
    import subprocess

    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "120", "--connect-timeout", "15",
             "-o", filepath, url],
            timeout=150,
            capture_output=True
        )
        if result.returncode == 0 and is_valid_video(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"OK ({size_mb:.1f} MB)")
            return True
        else:
            print(f"FALHOU (arquivo invalido ou curl erro)")
            try:
                os.remove(filepath)
            except Exception:
                pass
            return False
    except subprocess.TimeoutExpired:
        print("TIMEOUT (>120s)")
        try:
            os.remove(filepath)
        except Exception:
            pass
        return False
    except Exception as e:
        print(f"ERRO: {e}")
        try:
            os.remove(filepath)
        except Exception:
            pass
        return False


def collect_existing_video_ids(driver):
    """Collect all video IDs currently visible on the page BEFORE upload.
    This prevents capturing stale IDs from previous uploads."""
    try:
        ids = driver.execute_script("""
            var ids = new Set();
            // Check all links
            document.querySelectorAll('a[href]').forEach(function(a) {
                var href = a.href || '';
                var m;
                if (m = href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/)) ids.add(m[1]);
                if (m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/)) ids.add(m[1]);
                if (m = href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/)) ids.add(m[1]);
            });
            // Check URL
            var m = window.location.href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
            if (m) ids.add(m[1]);
            // Check data attributes
            document.querySelectorAll('[video-id], [data-video-id]').forEach(function(el) {
                var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) ids.add(vid);
            });
            return Array.from(ids);
        """)
        return set(ids) if ids else set()
    except Exception:
        return set()


def find_new_video_id(driver, exclude_ids):
    """Find a video ID on the page that is NOT in the exclude set."""
    try:
        all_ids = driver.execute_script("""
            var ids = [];
            // 1. Check data attributes (most reliable - YouTube Studio sets these)
            document.querySelectorAll('[video-id], [data-video-id]').forEach(function(el) {
                var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) ids.push(vid);
            });
            // 2. Check links
            document.querySelectorAll('a[href]').forEach(function(a) {
                var href = a.href || '';
                var m;
                if (m = href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/)) ids.push(m[1]);
                if (m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/)) ids.push(m[1]);
                if (m = href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/)) ids.push(m[1]);
            });
            // 3. Check URL
            var m = window.location.href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
            if (m) ids.push(m[1]);
            // 4. Check .video-url-fadeable specifically (upload dialog link)
            document.querySelectorAll('.video-url-fadeable a, a.ytcp-video-info').forEach(function(el) {
                var href = el.href || el.textContent || '';
                var m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/) ||
                        href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/) ||
                        href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                if (m) ids.push(m[1]);
            });
            return ids;
        """)
        if all_ids:
            for vid in all_ids:
                if vid not in exclude_ids:
                    return vid
        return None
    except Exception:
        return None


def ensure_logged_in(driver):
    """Make sure we're logged into YouTube Studio. Wait for manual login if needed."""
    driver.get("https://studio.youtube.com")
    time.sleep(5)
    for attempt in range(90):
        url = driver.current_url
        if "studio.youtube.com" in url and "accounts.google.com" not in url:
            return True
        if attempt == 0:
            print("  [LOGIN] Aguardando login no YouTube... Faca login no Chrome.")
        time.sleep(2)
    return False


def check_daily_limit(driver):
    """Check if YouTube daily upload limit has been reached.
    Returns the limit message if reached, None otherwise.
    Only matches leaf/near-leaf elements with short text to avoid false positives
    from parent divs whose textContent aggregates unrelated child text."""
    try:
        limit_hit = driver.execute_script("""
            var allEls = document.querySelectorAll('span, p, yt-formatted-string, .error-short, .error-message');
            for (var el of allEls) {
                var txt = (el.textContent || '').trim();
                // Only check short text from leaf-ish elements (real limit messages are concise)
                if (txt.length < 10 || txt.length > 300) continue;
                if (el.children.length > 5) continue;
                var lower = txt.toLowerCase();
                if ((lower.includes('limite diário') || lower.includes('daily limit') ||
                     lower.includes('limite de envios') || lower.includes('upload limit')) &&
                    (lower.includes('alcançado') || lower.includes('atingido') || lower.includes('reached') ||
                     lower.includes('exceeded'))) {
                    return txt.substring(0, 150);
                }
            }
            return null;
        """)
        return limit_hit
    except Exception:
        return None


def verify_upload_started(driver, timeout=30):
    """Verify that upload actually started by checking for progress indicators.
    Returns 'ok' if started, 'daily_limit' if limit reached, None if failed."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            # Check daily limit FIRST
            limit_msg = check_daily_limit(driver)
            if limit_msg:
                print(f"\n  [LIMITE] {limit_msg}")
                return 'daily_limit'

            started = driver.execute_script("""
                // Check for daily limit / error FIRST (highest priority)
                // Only check leaf-ish elements with short text to avoid false positives
                var limitEls = document.querySelectorAll('span, p, yt-formatted-string, .error-short, .error-message');
                for (var el of limitEls) {
                    var txt = (el.textContent || '').trim();
                    if (txt.length < 10 || txt.length > 300 || el.children.length > 5) continue;
                    var lower = txt.toLowerCase();
                    if ((lower.includes('limite diário') || lower.includes('daily limit') ||
                         lower.includes('limite de envios') || lower.includes('upload limit') ||
                         lower.includes('cota') || lower.includes('quota')) &&
                        (lower.includes('alcançado') || lower.includes('alcancado') || lower.includes('atingido') ||
                         lower.includes('reached') || lower.includes('exceeded'))) {
                        return 'daily_limit: ' + txt.substring(0, 100);
                    }
                }

                // Check for upload progress bar
                var progressBar = document.querySelector('.progress-bar, ytcp-video-upload-progress, [class*="upload-progress"]');
                if (progressBar && progressBar.offsetParent !== null) return 'progress_bar';

                // Check for any percentage text
                var spans = document.querySelectorAll('span, div');
                for (var el of spans) {
                    var txt = (el.textContent || '').trim();
                    if (txt.match(/\\d+%/) && txt.length < 50) return 'percentage: ' + txt;
                    if (txt.includes('Enviando') || txt.includes('Uploading')) return 'uploading_text';
                    if (txt.includes('processando') || txt.includes('processing')) return 'processing';
                }

                // Check for video-id attribute appearing (means YouTube accepted the file)
                var vidEls = document.querySelectorAll('[video-id], [data-video-id]');
                for (var el of vidEls) {
                    var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                    if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) return 'video_id_found';
                }

                // Check for title field appearing (upload dialog opened)
                var textboxes = document.querySelectorAll('#textbox[contenteditable="true"]');
                if (textboxes.length > 0) return 'title_field';

                // Check for generic error
                var errorEls = document.querySelectorAll('.error-short, .error-message');
                for (var el of errorEls) {
                    var txt = (el.textContent || '').trim();
                    if (txt.length > 5) return 'error: ' + txt.substring(0, 80);
                }

                return null;
            """)
            if started:
                if started.startswith('daily_limit:'):
                    print(f"\n  [LIMITE] {started}")
                    return 'daily_limit'
                if started.startswith('error:'):
                    print(f"\n  [ERRO] Upload falhou: {started}")
                    return None
                print(f" ({started})")
                return 'ok'
        except Exception:
            pass
        time.sleep(2)
    return None


def upload_video_selenium(driver, filepath, title, description, known_ids, client_name=""):
    """Upload a single video via YouTube Studio.
    known_ids: set of video IDs already uploaded (to detect new ones).
    client_name: used to assign video to a playlist 'Portfolio - {client_name}'.
    Returns the NEW video ID or None on failure."""
    abs_path = os.path.abspath(filepath)

    # Navigate to Studio upload page
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    # Check if redirected to login
    if "accounts.google.com" in driver.current_url:
        if not ensure_logged_in(driver):
            print("  [ERRO] Nao conseguiu fazer login no YouTube")
            return None

    # Capture ALL video IDs currently on the page BEFORE upload
    pre_upload_ids = collect_existing_video_ids(driver)
    pre_upload_ids.update(known_ids)  # Also exclude all previously uploaded IDs
    print(f"  [INFO] IDs pre-existentes na pagina: {len(pre_upload_ids)}")

    # Click the "Criar" (Create) button
    try:
        clicked = driver.execute_script("""
            // Try multiple selectors for the Create button
            var selectors = [
                'button[aria-label="Criar"]',
                'button[aria-label="Create"]',
                '#create-icon',
                'ytcp-button#create-icon'
            ];
            for (var sel of selectors) {
                var btn = document.querySelector(sel);
                if (btn) { btn.click(); return 'clicked: ' + sel; }
            }
            // Fallback: search by text
            var btns = document.querySelectorAll('button, [role="button"], ytcp-button');
            for (var b of btns) {
                var aria = (b.getAttribute('aria-label') || '').toLowerCase();
                var txt = (b.textContent || '').toLowerCase().trim();
                if (aria === 'criar' || aria === 'create' || txt === 'criar' || txt === 'create') {
                    b.click(); return 'clicked_text: ' + txt;
                }
            }
            return null;
        """)
        if not clicked:
            print("  [ERRO] Nao encontrou botao 'Criar'")
            return None
        print(f"  [OK] Botao Criar: {clicked}")
        time.sleep(3)
    except Exception as e:
        print(f"  [ERRO] Nao encontrou botao 'Criar': {e}")
        return None

    # Click "Enviar videos" (Upload videos)
    try:
        clicked = driver.execute_script("""
            // Try #upload-button first
            var btn = document.querySelector('#upload-button');
            if (btn) { btn.click(); return 'upload-button'; }
            // Try menu items
            var items = document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu a, [role="menuitem"]');
            for (var item of items) {
                var txt = (item.textContent || '').toLowerCase();
                if (txt.includes('enviar') || txt.includes('upload')) {
                    item.click(); return 'menu: ' + txt.trim().substring(0, 30);
                }
            }
            return null;
        """)
        if not clicked:
            print("  [ERRO] Nao encontrou opcao 'Enviar videos'")
            return None
        print(f"  [OK] Menu upload: {clicked}")
        time.sleep(4)
    except Exception as e:
        print(f"  [ERRO] Nao encontrou opcao 'Enviar videos': {e}")
        return None

    # Find the file input
    file_input = None
    for attempt in range(8):
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, "input[name='Filedata']")
            if file_input:
                break
        except Exception:
            pass
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            if file_input:
                break
        except Exception:
            pass
        time.sleep(2)

    if not file_input:
        print("  [ERRO] Nao encontrou input de arquivo")
        try:
            debug = driver.execute_script("""
                return {
                    url: window.location.href,
                    inputs: Array.from(document.querySelectorAll('input')).map(
                        i => i.type + '|' + i.name + '|' + i.id
                    ).slice(0, 10)
                };
            """)
            print(f"  [DEBUG] {json.dumps(debug)}")
        except Exception:
            pass
        return None

    # Send the file
    file_input.send_keys(abs_path)
    print("  [UPLOAD] Arquivo enviado ao input...", end="", flush=True)

    # CRITICAL: Verify the upload actually started
    upload_status = verify_upload_started(driver)
    if upload_status == 'daily_limit':
        print("  [LIMITE DIARIO] YouTube bloqueou uploads. Aguarde 24h ou faca verificacao do canal.")
        return "DAILY_LIMIT"
    if not upload_status:
        print("  [ERRO] Upload NAO iniciou - o YouTube nao aceitou o arquivo")
        return None

    time.sleep(3)

    # Set title via keyboard (more reliable than JS for contenteditable)
    try:
        # Wait for upload dialog to fully load
        time.sleep(8)
        # Find title textbox - it's the first contenteditable #textbox
        textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox[contenteditable='true']")
        if not textboxes:
            textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox")

        if textboxes:
            title_box = textboxes[0]
            driver.execute_script("arguments[0].focus(); arguments[0].click();", title_box)
            time.sleep(0.5)
            # Select all existing text and replace
            title_box.send_keys(Keys.CONTROL + "a")
            time.sleep(0.2)
            title_box.send_keys(title[:100])
            time.sleep(0.5)
            print(f"  [OK] Titulo definido: {title[:60]}...")

            # Set description if second textbox exists
            if len(textboxes) > 1:
                desc_box = textboxes[1]
                driver.execute_script("arguments[0].focus(); arguments[0].click();", desc_box)
                time.sleep(0.3)
                desc_box.send_keys(Keys.CONTROL + "a")
                time.sleep(0.2)
                desc_box.send_keys(description)
                print(f"  [OK] Descricao definida")
        else:
            print("  [AVISO] Nao encontrou campo de titulo")
    except Exception as e:
        print(f"  [AVISO] Erro ao definir titulo: {e}")

    # Add to client playlist
    if client_name:
        playlist_name = f"Portfolio - {client_name}"
        try:
            time.sleep(1)
            # Click the "Playlists" dropdown/button in the upload dialog
            opened = driver.execute_script("""
                // Find and click the playlist selector
                var els = document.querySelectorAll(
                    'ytcp-text-dropdown-trigger, ytcp-button, button, .dropdown-trigger'
                );
                for (var el of els) {
                    var txt = (el.textContent || '').trim().toLowerCase();
                    if (txt.includes('playlist') || txt.includes('selecionar')) {
                        // Check if it's inside the upload dialog
                        var parent = el.closest('ytcp-uploads-dialog, ytcp-upload-dialog, ytcp-video-metadata-editor');
                        if (parent || txt.includes('playlist')) {
                            el.click();
                            return 'clicked';
                        }
                    }
                }
                // Fallback: look for the playlist section more broadly
                var labels = document.querySelectorAll('label, .label, span');
                for (var l of labels) {
                    var txt = (l.textContent || '').trim().toLowerCase();
                    if (txt === 'playlists' || txt === 'playlist') {
                        var clickable = l.closest('ytcp-text-dropdown-trigger, button, [role="button"]');
                        if (clickable) { clickable.click(); return 'clicked_label'; }
                        l.click();
                        return 'clicked_span';
                    }
                }
                return 'not_found';
            """)

            if 'clicked' in str(opened):
                time.sleep(2)

                # Look for existing playlist or create new one
                playlist_result = driver.execute_script("""
                    var targetName = arguments[0];

                    // Search for the playlist checkbox in the dropdown
                    var checkboxes = document.querySelectorAll(
                        'ytcp-checkbox-lit, tp-yt-paper-checkbox, ytcp-checkbox-group label, ' +
                        '.playlist-item, [class*="playlist"]'
                    );
                    for (var cb of checkboxes) {
                        var txt = (cb.textContent || '').trim();
                        if (txt.includes(targetName)) {
                            cb.click();
                            return 'selected: ' + txt.substring(0, 40);
                        }
                    }

                    // Playlist not found - try to create it
                    // Look for "Nova playlist" / "New playlist" input or button
                    var createBtns = document.querySelectorAll(
                        'ytcp-button, button, a, span[role="button"]'
                    );
                    for (var btn of createBtns) {
                        var txt = (btn.textContent || '').trim().toLowerCase();
                        if (txt.includes('nova playlist') || txt.includes('new playlist') ||
                            txt.includes('criar playlist') || txt.includes('create playlist')) {
                            btn.click();
                            return 'create_clicked';
                        }
                    }

                    return 'playlist_not_found';
                """, playlist_name)

                if playlist_result == 'create_clicked':
                    time.sleep(2)
                    # Type the playlist name
                    driver.execute_script("""
                        var inputs = document.querySelectorAll(
                            'input[type="text"], #input, ytcp-form-input-container input, ' +
                            '#textbox[contenteditable="true"], input.style-scope'
                        );
                        // Find the playlist name input (usually the last visible text input)
                        for (var inp of inputs) {
                            if (inp.offsetParent !== null &&
                                (inp.placeholder || '').toLowerCase().includes('playlist') ||
                                inp.closest('[class*="playlist"]')) {
                                inp.value = arguments[0];
                                inp.dispatchEvent(new Event('input', {bubbles: true}));
                                return 'typed';
                            }
                        }
                        // Fallback: try contenteditable
                        var boxes = document.querySelectorAll('#textbox[contenteditable="true"]');
                        for (var b of boxes) {
                            if (b.offsetParent !== null && !b.textContent.trim()) {
                                b.textContent = arguments[0];
                                b.dispatchEvent(new Event('input', {bubbles: true}));
                                return 'typed_ce';
                            }
                        }
                        return 'no_input';
                    """, playlist_name)
                    time.sleep(1)

                    # Click "Criar" / "Create" button
                    driver.execute_script("""
                        var btns = document.querySelectorAll('ytcp-button, button');
                        for (var b of btns) {
                            var txt = (b.textContent || '').trim().toLowerCase();
                            if (txt === 'criar' || txt === 'create') {
                                b.click();
                                return 'created';
                            }
                        }
                    """)
                    time.sleep(1)
                    print(f"  [OK] Playlist criada: {playlist_name}")
                elif 'selected' in str(playlist_result):
                    print(f"  [OK] Playlist: {playlist_result}")
                else:
                    print(f"  [AVISO] Playlist nao encontrada: {playlist_result}")

                # Close the playlist dropdown by clicking "Concluir"/"Done" inside it
                time.sleep(1)
                driver.execute_script("""
                    var btns = document.querySelectorAll('ytcp-button, button');
                    for (var b of btns) {
                        var txt = (b.textContent || '').trim().toLowerCase();
                        var parent = b.closest('.playlists-dialog, [class*="playlist-dialog"], ytcp-playlist-dialog');
                        if (parent && (txt === 'concluir' || txt === 'done' || txt === 'salvar' || txt === 'save')) {
                            b.click();
                            return 'closed';
                        }
                    }
                    // Fallback: click outside
                    return 'no_close_btn';
                """)
                time.sleep(1)
            else:
                print(f"  [AVISO] Nao encontrou seletor de playlists: {opened}")
        except Exception as e:
            print(f"  [AVISO] Erro ao definir playlist: {str(e)[:60]}")

    # Set "Not made for kids"
    try:
        time.sleep(1)
        clicked_not_kids = driver.execute_script("""
            var radios = document.querySelectorAll('tp-yt-paper-radio-button');
            for (var r of radios) {
                var txt = (r.textContent || '').toLowerCase();
                if (txt.includes('not made for kids') || txt.includes('no,') ||
                    txt.includes('não é') || txt.includes('nao e') ||
                    txt.includes("isn't made for kids")) {
                    r.click();
                    return true;
                }
            }
            // Fallback: second radio is usually "not for kids"
            if (radios.length >= 2) { radios[1].click(); return true; }
            return false;
        """)
        if clicked_not_kids:
            print("  [OK] Marcado: nao e conteudo para criancas")
    except Exception:
        print("  [AVISO] Nao conseguiu marcar 'nao e para criancas'")

    # Navigate: Details -> Video elements -> Checks -> Visibility (3 clicks of Next)
    for step in range(3):
        try:
            time.sleep(2)
            driver.execute_script("""
                var btn = document.querySelector('#next-button');
                if (btn) btn.click();
            """)
            time.sleep(1)
        except Exception:
            break

    # Set visibility to Unlisted
    try:
        time.sleep(2)
        set_unlisted = driver.execute_script("""
            var radios = document.querySelectorAll('tp-yt-paper-radio-button');
            for (var r of radios) {
                var name = (r.getAttribute('name') || '').toUpperCase();
                var txt = (r.textContent || '').toLowerCase();
                if (txt.includes('unlisted') || txt.includes('nao listado') ||
                    txt.includes('não listado') || name === 'UNLISTED') {
                    r.click();
                    return true;
                }
            }
            return false;
        """)
        if set_unlisted:
            print("  [OK] Visibilidade: nao listado")
        else:
            print("  [AVISO] Nao encontrou opcao 'nao listado'")
    except Exception:
        print("  [AVISO] Nao conseguiu definir como nao listado")

    # Wait for upload to complete and find the NEW video ID
    # IMPORTANT: Only look inside the upload dialog for progress, not the whole page
    print("  [UPLOAD] Aguardando upload completar...")
    video_id = None
    start_time = time.time()
    last_progress = ""
    stall_count = 0
    saw_percentage = False  # Must see real upload progress before allowing exit
    MIN_UPLOAD_WAIT = 30   # Minimum seconds to wait (no file uploads in 0s)

    while time.time() - start_time < UPLOAD_TIMEOUT:
        try:
            status = driver.execute_script("""
                var result = {progress: '', doneEnabled: false, error: '', uploadComplete: false, videoId: ''};

                // ONLY look inside the upload dialog for progress
                var dialog = document.querySelector('ytcp-uploads-dialog, ytcp-upload-dialog');
                var searchRoot = dialog || document;

                // Check for error messages inside dialog (only direct error elements, not broad [class*=error])
                var errorEls = searchRoot.querySelectorAll(
                    '.error-short, .error-message, .error-area'
                );
                for (var el of errorEls) {
                    var txt = (el.textContent || '').trim();
                    // Only match leaf-ish elements with concise error text
                    if (txt && txt.length > 5 && txt.length < 200 && el.children.length < 5 &&
                        (txt.includes('limit') || txt.includes('limite') || txt.includes('erro') ||
                         txt.includes('error') || txt.includes('falha') || txt.includes('fail') ||
                         txt.includes('cota') || txt.includes('quota') || txt.includes('diário') ||
                         txt.includes('daily'))) {
                        result.error = txt.substring(0, 150);
                        break;
                    }
                }

                // Check progress ONLY inside dialog
                var progressEls = searchRoot.querySelectorAll(
                    '.progress-label, .ytcp-video-upload-progress, span.ytcp-uploads-dialog-header, ' +
                    'span[class*="progress"], div[class*="progress"], .upload-status, ' +
                    'ytcp-video-upload-progress-renderer span, ytcp-uploads-dialog span'
                );
                // Also check generic spans but ONLY inside the dialog
                if (dialog) {
                    var dialogSpans = dialog.querySelectorAll('span, div.label');
                    progressEls = Array.from(progressEls).concat(Array.from(dialogSpans));
                }
                for (var el of progressEls) {
                    var txt = (el.textContent || '').trim();
                    if (txt.length > 2 && txt.length < 120 && el.children.length < 3) {
                        // Match percentage, upload/processing status
                        if (txt.match(/\\d+\\s*%/) ||
                            txt.includes('Enviando') || txt.includes('Uploading') ||
                            txt.includes('processando') || txt.includes('processing') ||
                            txt.includes('Upload conclu') || txt.includes('Upload complete') ||
                            txt.includes('Verificações') || txt.includes('checks') ||
                            txt.includes('Processamento conclu') || txt.includes('Processing complete')) {
                            result.progress = txt;
                            // Upload is complete ONLY if explicitly says so or is at 100%
                            if (txt.includes('Upload conclu') || txt.includes('Upload complete') ||
                                txt.includes('Processamento conclu') || txt.includes('Processing complete') ||
                                txt.match(/100\\s*%/)) {
                                result.uploadComplete = true;
                            }
                            break;
                        }
                    }
                }

                // Find video ID from dialog's video link (most reliable)
                if (dialog) {
                    var dialogLinks = dialog.querySelectorAll('a[href]');
                    for (var a of dialogLinks) {
                        var href = a.href || '';
                        var m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/) ||
                                href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/) ||
                                href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                        if (m) { result.videoId = m[1]; break; }
                    }
                    // Also check video-id attributes inside dialog
                    if (!result.videoId) {
                        var vidEls = dialog.querySelectorAll('[video-id], [data-video-id]');
                        for (var el of vidEls) {
                            var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                            if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) { result.videoId = vid; break; }
                        }
                    }
                }

                // Check done button
                var doneBtn = document.querySelector('#done-button');
                if (doneBtn) {
                    var disabled = doneBtn.hasAttribute('disabled') ||
                                   doneBtn.getAttribute('aria-disabled') === 'true';
                    result.doneEnabled = !disabled;
                }

                return result;
            """)

            elapsed = int(time.time() - start_time)

            # Check daily limit during upload
            limit_msg = check_daily_limit(driver)
            if limit_msg:
                print(f"  [LIMITE DIARIO] {limit_msg}")
                return "DAILY_LIMIT"

            # Check for errors
            if status.get('error'):
                err_lower = status['error'].lower()
                if any(w in err_lower for w in ['limite', 'limit', 'cota', 'quota']) and \
                   any(w in err_lower for w in ['diário', 'diario', 'daily', 'alcançado', 'alcancado', 'atingido', 'reached', 'exceeded']):
                    print(f"  [LIMITE DIARIO] {status['error']}")
                    return "DAILY_LIMIT"
                print(f"  [ERRO] YouTube reportou erro: {status['error']}")
                return None

            progress_text = status.get('progress', '')
            done = status.get('doneEnabled', False)
            upload_complete = status.get('uploadComplete', False)

            # Track if we've seen real upload progress
            if progress_text and ('%' in progress_text or 'Enviando' in progress_text or 'Uploading' in progress_text):
                saw_percentage = True

            # Get video ID from dialog (ignore pre_upload_ids since we're inside dialog)
            dialog_vid = status.get('videoId', '')
            if dialog_vid:
                video_id = dialog_vid

            # Detect stalls
            if progress_text == last_progress:
                stall_count += 1
            else:
                stall_count = 0
                last_progress = progress_text

            display = progress_text[:50] if progress_text else 'aguardando...'
            if video_id:
                display += f' [ID: {video_id}]'
            if done:
                display += ' [Done ON]'
            print(f"  [UPLOAD] {display} ({elapsed}s)")

            # SAFETY: Never exit before MIN_UPLOAD_WAIT seconds
            if elapsed < MIN_UPLOAD_WAIT:
                time.sleep(5)
                continue

            # Exit conditions (after minimum wait):
            # 1. Upload explicitly complete AND done enabled
            if upload_complete and done:
                print(f"  [OK] Upload completo confirmado ({elapsed}s)")
                break

            # 2. Done enabled + we saw real progress + no more progress text (upload finished)
            if done and saw_percentage and elapsed > 60:
                print(f"  [OK] Done habilitado + progresso detectado anteriormente ({elapsed}s)")
                break

            # 3. Done enabled for a while (30s+) even without explicit complete text
            if done and elapsed > 90:
                print(f"  [OK] Done habilitado por tempo suficiente ({elapsed}s)")
                break

            # Stalled for too long
            if stall_count > 12 and not video_id:
                print(f"  [AVISO] Sem progresso por 60s")
                if done:
                    break
                if stall_count > 24:
                    print(f"  [ERRO] Upload travou definitivamente")
                    return None

            time.sleep(5)

        except Exception as e:
            print(f"  [WARN] Erro no loop: {str(e)[:60]}")
            time.sleep(5)

    print(f"  [UPLOAD] Loop finalizado ({int(time.time() - start_time)}s)")

    # If we have no video ID yet, try to find it from dialog
    if not video_id:
        print("  [BUSCA] Tentando encontrar video ID no dialog...")
        for attempt in range(10):
            time.sleep(3)
            try:
                dialog_vid = driver.execute_script("""
                    var dialog = document.querySelector('ytcp-uploads-dialog, ytcp-upload-dialog');
                    if (!dialog) return null;
                    // Check links inside dialog
                    var links = dialog.querySelectorAll('a[href]');
                    for (var a of links) {
                        var href = a.href || '';
                        var m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/) ||
                                href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/) ||
                                href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                        if (m) return m[1];
                    }
                    // Check video-id attributes
                    var vidEls = dialog.querySelectorAll('[video-id], [data-video-id]');
                    for (var el of vidEls) {
                        var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                        if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) return vid;
                    }
                    return null;
                """)
                if dialog_vid:
                    video_id = dialog_vid
                    print(f"  [OK] Video ID encontrado: {video_id}")
                    break
            except Exception:
                pass

    # Click Done button - wait for it to be enabled first
    done_clicked = False
    print("  [DONE] Aguardando botao Concluir ficar habilitado...")
    for wait_attempt in range(30):  # Wait up to 150s for Done to be enabled
        try:
            btn_state = driver.execute_script("""
                var btn = document.querySelector('#done-button');
                if (!btn) return 'not_found';
                var disabled = btn.hasAttribute('disabled') ||
                               btn.getAttribute('aria-disabled') === 'true';
                if (disabled) return 'disabled';
                btn.click();
                return 'clicked';
            """)
            if btn_state == 'clicked':
                done_clicked = True
                print(f"  [OK] Clicou 'Concluir'")
                break
            elif btn_state == 'disabled':
                if wait_attempt % 6 == 0:
                    print(f"  [DONE] Botao ainda desabilitado... ({wait_attempt * 5}s)")
            elif btn_state == 'not_found':
                print(f"  [AVISO] Botao Concluir nao encontrado")
                break
        except Exception as e:
            print(f"  [WARN] Erro ao clicar Done: {str(e)[:40]}")
        time.sleep(5)

    if done_clicked:
        # Handle "Ainda estamos verificando seu conteúdo" confirmation dialog
        # YouTube asks to confirm publishing while checks are still running
        time.sleep(3)
        for confirm_attempt in range(5):
            try:
                confirmed = driver.execute_script("""
                    // Look for "Publicar mesmo assim" button in confirmation dialog
                    var allBtns = document.querySelectorAll(
                        'ytcp-button, tp-yt-paper-button, button, .yt-spec-button-shape-next'
                    );
                    for (var btn of allBtns) {
                        var txt = (btn.textContent || '').trim().toLowerCase();
                        if (txt.includes('publicar mesmo assim') || txt.includes('publish anyway') ||
                            txt.includes('publicar mesmo') || txt.includes('publish despite')) {
                            btn.click();
                            return 'clicked_publish_anyway';
                        }
                    }
                    // Also check for the dialog text to know if it appeared
                    var dialogTexts = document.querySelectorAll('span, p, div, yt-formatted-string');
                    for (var el of dialogTexts) {
                        var txt = (el.textContent || '').trim();
                        if (txt.includes('verificando seu conte') || txt.includes('still checking')) {
                            // Dialog is open but button not found yet, wait
                            return 'dialog_visible';
                        }
                    }
                    return 'no_dialog';
                """)
                if confirmed == 'clicked_publish_anyway':
                    print("  [OK] Clicou 'Publicar mesmo assim'")
                    time.sleep(3)
                    break
                elif confirmed == 'dialog_visible':
                    print("  [AVISO] Dialog de verificacao visivel, buscando botao...")
                    time.sleep(2)
                elif confirmed == 'no_dialog':
                    break
            except Exception:
                break
            time.sleep(2)

        # Wait for YouTube to fully register the upload
        print("  [POS-UPLOAD] Aguardando YouTube registrar o upload...")
        time.sleep(5)

        # Check if upload confirmation dialog appeared
        for post_wait in range(6):
            try:
                post_status = driver.execute_script("""
                    // First check if there's STILL a publish-anyway dialog
                    var allBtns = document.querySelectorAll(
                        'ytcp-button, tp-yt-paper-button, button'
                    );
                    for (var btn of allBtns) {
                        var txt = (btn.textContent || '').trim().toLowerCase();
                        if (txt.includes('publicar mesmo assim') || txt.includes('publish anyway')) {
                            btn.click();
                            return 'clicked_publish_anyway';
                        }
                    }
                    var dialog = document.querySelector('ytcp-uploads-dialog, ytcp-upload-dialog');
                    if (!dialog) return 'dialog_closed';
                    var txt = dialog.textContent || '';
                    if (txt.includes('publicado') || txt.includes('published') ||
                        txt.includes('programado') || txt.includes('scheduled') ||
                        txt.includes('nao listado') || txt.includes('não listado') ||
                        txt.includes('unlisted') ||
                        txt.includes('Compartilhar') || txt.includes('Share')) {
                        return 'confirmed';
                    }
                    return 'still_open';
                """)
                if post_status == 'clicked_publish_anyway':
                    print("  [OK] Clicou 'Publicar mesmo assim' (tentativa extra)")
                    time.sleep(3)
                    continue
                print(f"  [POS-UPLOAD] Status: {post_status}")
                if post_status in ('dialog_closed', 'confirmed'):
                    break
            except Exception:
                break
            time.sleep(3)

        # Final wait to be safe
        time.sleep(5)
    else:
        print("  [AVISO] Botao 'Concluir' nao foi clicado!")

    # Try to find video ID one last time after Done
    if not video_id:
        try:
            # Check the URL in case we were redirected to the video page
            url = driver.current_url
            m = re.search(r'/video/([a-zA-Z0-9_-]{11})', url)
            if m:
                video_id = m.group(1)
                print(f"  [OK] Video ID da URL: {video_id}")
        except Exception:
            pass

    if not video_id:
        # Fallback: scan all new links
        new_id = find_new_video_id(driver, pre_upload_ids)
        if new_id:
            video_id = new_id
            print(f"  [OK] Video ID pos-Done: {video_id}")

    # Close any post-upload dialog
    try:
        time.sleep(2)
        driver.execute_script("""
            var closeBtn = document.querySelector('ytcp-button#close-button');
            if (closeBtn && closeBtn.offsetParent !== null) closeBtn.click();
        """)
    except Exception:
        pass

    if video_id:
        print(f"  [SUCESSO] Video enviado: https://youtu.be/{video_id}")
        return video_id

    if done_clicked:
        print("  [FALHA] Done clicado mas video ID nao encontrado")
    else:
        print("  [FALHA] Upload nao completou")

    # Return special marker if Done was clicked (upload probably worked)
    if done_clicked:
        return "UPLOADED_NO_ID"

    return None


def close_upload_dialog(driver):
    """Close any open upload dialog - try to save first, then discard."""
    # First try Done
    try:
        done_clicked = driver.execute_script("""
            var btn = document.querySelector('#done-button');
            if (btn && !btn.hasAttribute('disabled')) { btn.click(); return true; }
            return false;
        """)
        if done_clicked:
            time.sleep(4)
            return
    except Exception:
        pass

    # Try close button
    try:
        driver.execute_script("""
            var btn = document.querySelector('ytcp-button#close-button');
            if (btn && btn.offsetParent !== null) btn.click();
        """)
        time.sleep(2)
    except Exception:
        pass

    # Try save/keep
    try:
        driver.execute_script("""
            var btns = document.querySelectorAll('ytcp-button');
            for (var b of btns) {
                var txt = (b.textContent || '').toLowerCase();
                if (txt.includes('salvar') || txt.includes('save') || txt.includes('manter') || txt.includes('keep')) {
                    if (b.offsetParent !== null) { b.click(); return; }
                }
            }
        """)
        time.sleep(2)
    except Exception:
        pass

    # Last resort: discard
    try:
        driver.execute_script("""
            var btns = document.querySelectorAll('ytcp-button');
            for (var b of btns) {
                var txt = (b.textContent || '').toLowerCase();
                if (txt.includes('descartar') || txt.includes('discard')) {
                    if (b.offsetParent !== null) { b.click(); return; }
                }
            }
        """)
        time.sleep(2)
    except Exception:
        pass


def main():
    print("=" * 60)
    print("  YOUTUBE UPLOADER (Selenium) - Portfolio Savylla Adryan")
    print("=" * 60)
    print()
    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print("  O script vai abrir o Chrome com seu perfil logado.")
    print()

    # Load data
    videos_data = load_videos()
    progress = load_progress()
    results = load_results()

    # Collect all known video IDs from previous uploads (to avoid duplicates)
    known_ids = set()
    for entry in progress["uploaded"].values():
        vid = entry.get("video_id", "")
        if vid and vid != "UPLOADED_NO_ID" and len(vid) == 11:
            known_ids.add(vid)
    print(f"[INFO] {len(known_ids)} video IDs ja conhecidos de uploads anteriores")

    total_videos = sum(len(v) for v in videos_data.values())
    already_done = len(progress["uploaded"])
    remaining = total_videos - already_done
    print(f"Total de videos: {total_videos}")
    print(f"Ja enviados: {already_done}")
    print(f"Restantes: {remaining}")
    print()

    if already_done >= total_videos:
        print("Todos os videos ja foram enviados!")
        return

    # Auto-start (sem prompt interativo)
    print("[AUTO] Iniciando em 3 segundos... Feche o Chrome se ainda estiver aberto!")
    time.sleep(3)
    print()

    # Create downloads dir
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Start Chrome
    print("[BROWSER] Abrindo Chrome...")
    try:
        driver = create_driver()
    except Exception as e:
        print(f"[ERRO] Nao conseguiu abrir o Chrome: {e}")
        print("\nDicas:")
        print("  1. Feche TODAS as janelas do Chrome")
        print("  2. Verifique se o Chrome esta instalado")
        print("  3. Tente novamente")
        sys.exit(1)

    # Navigate to YouTube Studio to verify login
    print("[BROWSER] Verificando login no YouTube Studio...")
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    current_url = driver.current_url
    if "accounts.google.com" in current_url or "studio.youtube.com" not in current_url:
        print("[AVISO] Voce nao esta logado! Aguardando login no navegador...")
        print("        Faca login manualmente no Chrome que abriu.")
        for _ in range(60):
            time.sleep(2)
            try:
                current_url = driver.current_url
                if "studio.youtube.com" in current_url and "accounts.google.com" not in current_url:
                    break
            except Exception:
                pass
        time.sleep(3)

    # Verify we're on the RIGHT YouTube channel
    try:
        channel_info = driver.execute_script("""
            // Try to find the channel name from YouTube Studio
            var name = '';
            var url = window.location.href;
            // Check for channel name in page
            var els = document.querySelectorAll('.channel-name, [id*="channel-name"], .ytcp-channel-name');
            for (var el of els) {
                var txt = (el.textContent || '').trim();
                if (txt.length > 1) { name = txt; break; }
            }
            // Try profile picture alt text
            if (!name) {
                var imgs = document.querySelectorAll('img[alt]');
                for (var img of imgs) {
                    var alt = img.alt || '';
                    if (alt.length > 1 && alt.length < 50 && !alt.includes('YouTube')) {
                        name = alt; break;
                    }
                }
            }
            return {name: name, url: url};
        """)
        ch_name = channel_info.get('name', '')
        ch_url = channel_info.get('url', '')
        print(f"\n[CANAL] Nome: {ch_name or '(nao detectado)'}")
        print(f"[CANAL] URL: {ch_url}")
        if ch_name and 'savylla' not in ch_name.lower() and 'adryan' not in ch_name.lower():
            print()
            print("!" * 60)
            print(f"  ATENCAO: Canal detectado = '{ch_name}'")
            print(f"  Esperado: 'Savylla Adryan'")
            print(f"  Voce pode estar na conta ERRADA!")
            print(f"  Troque de conta no YouTube Studio.")
            print("!" * 60)
            print()
            print("  Aguardando 60s para voce trocar de conta...")
            print("  (ou o script continua com essa conta)")
            time.sleep(60)
    except Exception:
        pass

    print("[OK] YouTube Studio carregado!")

    # Check if any videos need ClickUp download
    has_clickup = any(
        "clickup" in v["url"].lower()
        for vlist in videos_data.values()
        for v in vlist
    )

    if has_clickup:
        # Navigate to ClickUp so user can login (needed for downloads)
        print("\n[BROWSER] Abrindo ClickUp para login...")
        print("          Faca login no ClickUp se ainda nao fez.")
        driver.get("https://app.clickup.com")
        time.sleep(5)

        clickup_url = driver.current_url
        needs_login = "login" in clickup_url.lower() or "sso" in clickup_url.lower() or "accounts.google" in clickup_url.lower()

        if needs_login:
            print("[LOGIN] Aguardando login no ClickUp... (max 3 min)")
            for _ in range(90):
                time.sleep(2)
                try:
                    clickup_url = driver.current_url
                    # Accept any URL that's not obviously a login page
                    if "clickup.com" in clickup_url and \
                       "login" not in clickup_url.lower() and \
                       "sso" not in clickup_url.lower() and \
                       "accounts.google" not in clickup_url.lower():
                        break
                except Exception:
                    pass

        # Check final state but don't block
        clickup_url = driver.current_url
        if "clickup.com" in clickup_url and "login" not in clickup_url.lower():
            print("[OK] ClickUp logado!\n")
        else:
            print("[AVISO] ClickUp pode nao estar logado. Downloads podem falhar.")
            print("        Se os downloads falharem, pare o script e logue no ClickUp.\n")

        # Go back to YouTube Studio
        driver.get("https://studio.youtube.com")
        time.sleep(5)

    print()

    # Process each client
    video_counter = 0
    success_count = 0
    errors = 0
    MAX_ERRORS = 3  # Stop after 3 consecutive errors (was 5 - faster fail)

    try:
        for client_name, videos in videos_data.items():
            print(f"\n{'-' * 60}")
            print(f"  CLIENTE: {client_name} ({len(videos)} videos)")
            print(f"{'-' * 60}")

            for i, video in enumerate(videos, 1):
                url = video["url"]
                talento = video.get("talento", "")
                video_key = f"{client_name}_{i:03d}"

                if video_key in progress["uploaded"]:
                    continue

                video_counter += 1
                video_name = extract_video_name(url)
                title = f"{client_name} - {video_name}"
                if talento:
                    title = f"{client_name} - {talento} - {video_name}"
                if len(title) > 100:
                    title = title[:97] + "..."

                description = f"Portfolio Savylla Adryan\nCliente: {client_name}\n"
                if talento:
                    description += f"Talento: {talento}\n"

                print(f"\n[{video_counter}/{remaining}] {title}")

                # Download
                safe_name = sanitize_filename(f"{video_key}_{talento or 'video'}")
                filepath = os.path.join(DOWNLOAD_DIR, f"{safe_name}.mp4")

                if os.path.exists(filepath) and is_valid_video(filepath):
                    size_mb = os.path.getsize(filepath) / (1024 * 1024)
                    print(f"  [DOWNLOAD] Ja existe localmente ({size_mb:.1f} MB)")
                    downloaded = True
                else:
                    # Remove invalid cached file if exists
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    downloaded = download_video(url, filepath, driver)

                if not downloaded:
                    print(f"  [SKIP] Nao foi possivel baixar - pulando")
                    # Make sure we're back on YouTube Studio
                    try:
                        if "studio.youtube.com" not in driver.current_url:
                            driver.get("https://studio.youtube.com")
                            time.sleep(5)
                    except Exception:
                        pass
                    continue

                # Ensure we're on YouTube Studio before uploading
                try:
                    if "studio.youtube.com" not in driver.current_url:
                        driver.get("https://studio.youtube.com")
                        time.sleep(5)
                except Exception:
                    pass

                # Upload via Selenium (pass known_ids to prevent duplicate detection)
                video_id = upload_video_selenium(driver, filepath, title, description, known_ids, client_name)

                if video_id == "DAILY_LIMIT":
                    print(f"\n[PARADA] Limite diario do YouTube atingido!")
                    print("Aguarde 24 horas ou faca a verificacao do canal no YouTube Studio.")
                    print("O progresso foi salvo - retome amanha.")
                    close_upload_dialog(driver)
                    errors = MAX_ERRORS  # Force stop
                    break

                if video_id and video_id != "DAILY_LIMIT":
                    errors = 0
                    success_count += 1
                    if video_id != "UPLOADED_NO_ID" and len(video_id) == 11:
                        known_ids.add(video_id)

                    youtube_url = f"https://youtu.be/{video_id}" if video_id != "UPLOADED_NO_ID" else "UPLOADED_NO_ID"

                    progress["uploaded"][video_key] = {
                        "video_id": video_id,
                        "url": youtube_url,
                        "title": title,
                        "client": client_name,
                        "talento": talento
                    }
                    save_progress(progress)

                    if client_name not in results:
                        results[client_name] = []
                    results[client_name].append({
                        "youtube_url": youtube_url,
                        "video_id": video_id,
                        "title": title,
                        "talento": talento,
                        "original_url": url
                    })
                    save_results(results)

                    # Clean up downloaded file
                    try:
                        os.remove(filepath)
                        print(f"  [CLEAN] Arquivo local removido")
                    except Exception:
                        pass

                    # Delay between uploads
                    print(f"  [WAIT] Aguardando {UPLOAD_DELAY}s...")
                    time.sleep(UPLOAD_DELAY)

                else:
                    errors += 1
                    print(f"  [ERRO] Upload falhou para {video_key} (erro {errors}/{MAX_ERRORS})")
                    close_upload_dialog(driver)

                    # Wait longer after an error
                    time.sleep(10)

                    if errors >= MAX_ERRORS:
                        print(f"\n[PARADA] {MAX_ERRORS} erros consecutivos.")
                        print("O progresso foi salvo. Verifique o navegador e tente novamente.")
                        break

            if errors >= MAX_ERRORS:
                break

    except KeyboardInterrupt:
        print("\n\n[INTERRUMPIDO] Progresso salvo.")

    finally:
        total_uploaded = len(progress["uploaded"])
        print(f"\n{'=' * 60}")
        print(f"  RESUMO")
        print(f"  Videos enviados nesta sessao: {success_count}")
        print(f"  Total enviados: {total_uploaded}/{total_videos}")
        print(f"  Restantes: {total_videos - total_uploaded}")
        print(f"  Resultados em: {RESULTS_FILE}")
        print(f"{'=' * 60}")

        print("\nFechando navegador em 5 segundos...")
        time.sleep(5)
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
