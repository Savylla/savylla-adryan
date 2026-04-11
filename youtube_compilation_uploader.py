"""
=============================================================
YOUTUBE PLAYLIST UPLOADER - Portfolio Savylla Adryan
=============================================================
Sobe videos INDIVIDUAIS para o YouTube e organiza em PLAYLISTS
por cliente (ex: "Portfolio - Drogasil").

Usa o mesmo progresso do upload_progress.json para nao duplicar
videos ja enviados anteriormente.

USO: python youtube_compilation_uploader.py
=============================================================
"""

import json
import os
import sys
import time
import re
import html
import subprocess
import shutil
from pathlib import Path
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# --- CONFIG ---
VIDEOS_JSON = "client_videos.json"
DOWNLOAD_DIR = "downloads"
PROGRESS_FILE = "upload_progress.json"  # Same as the working uploader
RESULTS_FILE = "youtube_results.json"

# YouTube upload settings
UPLOAD_DELAY = 20
UPLOAD_TIMEOUT = 900  # 15 min per video

# Anti-Shorts: pillarbox converts vertical (9:16) to horizontal (16:9)
# YouTube classifies Shorts by aspect ratio, not just duration
# Video is NOT rescaled — original resolution is preserved, only black bars are added

# Chrome debug port
CHROME_DEBUG_PORT = 9555


# =============================================================
# UTILITY FUNCTIONS
# =============================================================

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


def clean_url(url):
    return html.unescape(url)


def extract_video_name(url):
    path = url.split("?")[0]
    filename = path.split("/")[-1]
    filename = unquote(filename)
    name = filename.rsplit(".", 1)[0] if "." in filename else filename
    name = re.sub(r'\[.*?\]', '', name).strip()
    name = re.sub(r'_+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name if name else "Video"


def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'_+', '_', name)
    return name[:200]


def is_valid_video(filepath):
    if not os.path.exists(filepath):
        return False
    size = os.path.getsize(filepath)
    if size < 100000:
        return False
    try:
        with open(filepath, "rb") as f:
            header = f.read(32)
        if header.startswith(b'<!') or header.startswith(b'<html') or header.startswith(b'<HTML'):
            return False
        if b'ftyp' in header[:12]:
            return True
        if header.startswith(b'\x1a\x45\xdf\xa3'):
            return True
        if header[:4] == b'RIFF' and header[8:12] == b'AVI ':
            return True
        if size > 500000:
            return True
        return False
    except Exception:
        return False


def get_video_dimensions(filepath):
    """Get video width, height using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "csv=p=0", filepath],
            capture_output=True, text=True, timeout=30
        )
        parts = result.stdout.strip().split(",")
        return int(parts[0]), int(parts[1])
    except Exception:
        return 0, 0


def pad_video_to_avoid_shorts(filepath):
    """Convert vertical (9:16) videos to horizontal (16:9) with pillarbox.
    Adds black bars on the sides so YouTube doesn't classify as Shorts.
    Returns path to the pillarboxed file (or original if already horizontal)."""
    width, height = get_video_dimensions(filepath)
    if width <= 0 or height <= 0:
        print(f"  [PILLARBOX] Nao conseguiu ler dimensoes, enviando como esta")
        return filepath

    if width >= height:
        print(f"  [PILLARBOX] Ja horizontal ({width}x{height}) - OK")
        return filepath

    # Vertical video: pad to 16:9 keeping original resolution (no downscale)
    out_h = height
    out_w = int(height * 16 / 9)
    out_w = out_w + (out_w % 2)  # Ensure even

    pillarbox_path = filepath.replace(".mp4", "_pillarbox.mp4")

    print(f"  [PILLARBOX] Vertical {width}x{height} -> {out_w}x{out_h} (barras laterais, sem redimensionar)...")

    try:
        cmd = [
            "ffmpeg", "-y", "-i", filepath,
            "-vf", f"pad={out_w}:{out_h}:(ow-iw)/2:0:black",
            "-c:v", "libx264", "-crf", "17", "-preset", "medium",
            "-c:a", "copy",
            "-movflags", "+faststart",
            pillarbox_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode == 0 and os.path.exists(pillarbox_path):
            size_mb = os.path.getsize(pillarbox_path) / (1024 * 1024)
            new_w, new_h = get_video_dimensions(pillarbox_path)
            print(f"  [PILLARBOX] OK - {width}x{height} -> {new_w}x{new_h} ({size_mb:.1f} MB)")
            return pillarbox_path
        else:
            print(f"  [PILLARBOX] ffmpeg falhou, tentando com re-encode de audio...")
            # Retry with audio re-encode (some codecs can't be stream-copied)
            cmd_retry = [
                "ffmpeg", "-y", "-i", filepath,
                "-vf", f"pad={out_w}:{out_h}:(ow-iw)/2:0:black",
                "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart",
                pillarbox_path
            ]
            result2 = subprocess.run(cmd_retry, capture_output=True, text=True, timeout=600)
            if result2.returncode == 0 and os.path.exists(pillarbox_path):
                size_mb = os.path.getsize(pillarbox_path) / (1024 * 1024)
                new_w, new_h = get_video_dimensions(pillarbox_path)
                print(f"  [PILLARBOX] OK (re-encoded audio) - {width}x{height} -> {new_w}x{new_h} ({size_mb:.1f} MB)")
                return pillarbox_path
            else:
                print(f"  [PILLARBOX] Falhou - enviando original")
                if result2.stderr:
                    print(f"  [PILLARBOX] stderr: {result2.stderr[:200]}")
                return filepath

    except subprocess.TimeoutExpired:
        print(f"  [PILLARBOX] TIMEOUT - enviando original")
        return filepath
    except Exception as e:
        print(f"  [PILLARBOX] ERRO: {e} - enviando original")
        return filepath


def download_video(url, filepath, driver=None):
    clean = clean_url(url)
    if "&sa=D&source=editors" in clean:
        clean = clean.split("&sa=D&source=editors")[0]

    # Handle local files (assets/projetos/...)
    if os.path.exists(clean):
        print(f"  [LOCAL] Copiando arquivo local... ", end="", flush=True)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            shutil.copy2(clean, filepath)
            if is_valid_video(filepath):
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"OK ({size_mb:.1f} MB)")
                return True
            else:
                print("FALHOU (arquivo invalido)")
                return False
        except Exception as e:
            print(f"ERRO: {e}")
            return False

    print(f"  [DOWNLOAD] Baixando... ", end="", flush=True)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    is_clickup = "clickup" in clean.lower()

    if is_clickup and driver:
        return download_via_browser(driver, clean, filepath)

    return download_via_curl(clean, filepath)


def download_via_browser(driver, url, filepath):
    abs_path = os.path.abspath(filepath)
    abs_download_dir = os.path.abspath(DOWNLOAD_DIR)
    os.makedirs(abs_download_dir, exist_ok=True)

    download_url = url.split("?")[0]

    try:
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": abs_download_dir
        })

        files_before = set(os.listdir(abs_download_dir))
        driver.get(download_url)
        time.sleep(5)

        page_url = driver.current_url
        if "clickup" in page_url:
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

        download_found = False
        for wait in range(180):
            time.sleep(1)
            files_after = set(os.listdir(abs_download_dir))
            new_files = files_after - files_before

            for f in new_files:
                if f.endswith('.crdownload'):
                    continue
                fpath = os.path.join(abs_download_dir, f)
                if os.path.getsize(fpath) > 50000:
                    time.sleep(2)
                    if is_valid_video(fpath):
                        if os.path.exists(abs_path):
                            os.remove(abs_path)
                        os.rename(fpath, abs_path)
                        download_found = True
                        break

            if download_found:
                break

            if any(f.endswith('.crdownload') for f in new_files):
                if wait % 20 == 0 and wait > 0:
                    print(f"({wait}s) ", end="", flush=True)
                continue

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

            if wait > 40 and not any(f.endswith('.crdownload') for f in (set(os.listdir(abs_download_dir)) - files_before)):
                break

        driver.get("https://studio.youtube.com")
        time.sleep(5)

        if download_found and os.path.exists(abs_path):
            size_mb = os.path.getsize(abs_path) / (1024 * 1024)
            print(f"OK ({size_mb:.1f} MB)")
            return True

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


# =============================================================
# YOUTUBE UPLOAD FUNCTIONS (individual video + playlist)
# =============================================================

def collect_existing_video_ids(driver):
    try:
        ids = driver.execute_script("""
            var ids = new Set();
            document.querySelectorAll('a[href]').forEach(function(a) {
                var href = a.href || '';
                var m;
                if (m = href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/)) ids.add(m[1]);
                if (m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/)) ids.add(m[1]);
                if (m = href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/)) ids.add(m[1]);
            });
            var m = window.location.href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
            if (m) ids.add(m[1]);
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
    try:
        all_ids = driver.execute_script("""
            var ids = [];
            document.querySelectorAll('[video-id], [data-video-id]').forEach(function(el) {
                var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) ids.push(vid);
            });
            document.querySelectorAll('a[href]').forEach(function(a) {
                var href = a.href || '';
                var m;
                if (m = href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/)) ids.push(m[1]);
                if (m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/)) ids.push(m[1]);
                if (m = href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/)) ids.push(m[1]);
            });
            var m = window.location.href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
            if (m) ids.push(m[1]);
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
    try:
        limit_hit = driver.execute_script("""
            var allEls = document.querySelectorAll('span, p, yt-formatted-string, .error-short, .error-message');
            for (var el of allEls) {
                var txt = (el.textContent || '').trim();
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
    start = time.time()
    while time.time() - start < timeout:
        try:
            limit_msg = check_daily_limit(driver)
            if limit_msg:
                print(f"\n  [LIMITE] {limit_msg}")
                return 'daily_limit'

            started = driver.execute_script("""
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

                var progressBar = document.querySelector('.progress-bar, ytcp-video-upload-progress, [class*="upload-progress"]');
                if (progressBar && progressBar.offsetParent !== null) return 'progress_bar';

                var spans = document.querySelectorAll('span, div');
                for (var el of spans) {
                    var txt = (el.textContent || '').trim();
                    if (txt.match(/\\d+%/) && txt.length < 50) return 'percentage: ' + txt;
                    if (txt.includes('Enviando') || txt.includes('Uploading')) return 'uploading_text';
                    if (txt.includes('processando') || txt.includes('processing')) return 'processing';
                }

                var vidEls = document.querySelectorAll('[video-id], [data-video-id]');
                for (var el of vidEls) {
                    var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                    if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) return 'video_id_found';
                }

                var textboxes = document.querySelectorAll('#textbox[contenteditable="true"]');
                if (textboxes.length > 0) return 'title_field';

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
    """Upload a single video via YouTube Studio and add to client playlist."""
    abs_path = os.path.abspath(filepath)

    driver.get("https://studio.youtube.com")
    time.sleep(5)

    if "accounts.google.com" in driver.current_url:
        if not ensure_logged_in(driver):
            print("  [ERRO] Nao conseguiu fazer login no YouTube")
            return None

    pre_upload_ids = collect_existing_video_ids(driver)
    pre_upload_ids.update(known_ids)
    print(f"  [INFO] IDs pre-existentes na pagina: {len(pre_upload_ids)}")

    # Click "Criar" (Create)
    try:
        clicked = driver.execute_script("""
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
            var btn = document.querySelector('#upload-button');
            if (btn) { btn.click(); return 'upload-button'; }
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

    # Find file input
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
        return None

    # Send file
    file_input.send_keys(abs_path)
    print("  [UPLOAD] Arquivo enviado ao input...", end="", flush=True)

    # Verify upload started
    upload_status = verify_upload_started(driver)
    if upload_status == 'daily_limit':
        print("  [LIMITE DIARIO] YouTube bloqueou uploads.")
        return "DAILY_LIMIT"
    if not upload_status:
        print("  [ERRO] Upload NAO iniciou")
        return None

    time.sleep(3)

    # Set title
    try:
        time.sleep(8)
        textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox[contenteditable='true']")
        if not textboxes:
            textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox")

        if textboxes:
            title_box = textboxes[0]
            # Use JS to set text content (avoids "element not interactable")
            driver.execute_script("""
                var el = arguments[0];
                var title = arguments[1];
                el.focus();
                el.click();
                el.textContent = '';
                el.innerText = title;
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
            """, title_box, title[:100])
            time.sleep(0.5)
            # Fallback: also type via active element to ensure YouTube registers it
            try:
                active = driver.switch_to.active_element
                active.send_keys(Keys.END)
            except Exception:
                pass
            time.sleep(0.5)
            print(f"  [OK] Titulo definido: {title[:60]}...")

            # Set description
            if len(textboxes) > 1:
                desc_box = textboxes[1]
                driver.execute_script("""
                    var el = arguments[0];
                    var desc = arguments[1];
                    el.focus();
                    el.click();
                    el.textContent = '';
                    el.innerText = desc;
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                """, desc_box, description)
                time.sleep(0.5)
                print(f"  [OK] Descricao definida")
        else:
            print("  [AVISO] Nao encontrou campo de titulo")
    except Exception as e:
        print(f"  [AVISO] Erro ao definir titulo: {e}")

    # Add to client playlist (proven logic from organize_playlists.py)
    if client_name:
        playlist_name = f"Portfolio - {client_name}"
        try:
            time.sleep(1)

            # Open playlist dialog via ytcp-video-metadata-playlists
            opened = driver.execute_script("""
                var comp = document.querySelector('ytcp-video-metadata-playlists');
                if (comp) {
                    var trigger = comp.querySelector('ytcp-text-dropdown-trigger, [role="button"]');
                    if (trigger) { trigger.click(); return 'clicked'; }
                    comp.click();
                    return 'clicked_comp';
                }
                return 'not_found';
            """)

            if 'clicked' in str(opened):
                time.sleep(3)

                # Scroll iron-list to load all playlists (virtual scrolling only renders visible items)
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

                # Try to select existing playlist
                playlist_result = driver.execute_script("""
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
                            if (label) { label.click(); return 'clicked_label'; }
                            group.click();
                            return 'clicked_group';
                        }
                    }

                    // Fallback: search all labels
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

                print(f"  [PLAYLIST] Select: {playlist_result}")

                # If playlist not found, create it via 2-step dropdown flow
                if playlist_result == 'not_found':
                    print(f"  [PLAYLIST] Criando '{playlist_name}'...")

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
                    time.sleep(5)

                    if clicked_item in ('clicked', 'clicked_fallback'):
                        # Step 3: Focus title textbox with retry
                        focused = 'no_creation_dialog'
                        for retry in range(8):
                            focused = driver.execute_script("""
                                // Look inside ytcp-playlist-dialog for creation form
                                var pd = document.querySelector('ytcp-playlist-dialog');
                                if (pd) {
                                    // The creation form has a textbox inside ytcp-form-input-container
                                    var selectors = [
                                        '#create-playlist-form #textbox',
                                        '#create-playlist-form div[contenteditable]',
                                        'ytcp-playlist-creation div[contenteditable]',
                                        'ytcp-playlist-creation #textbox',
                                        '.create-playlist-form #textbox',
                                        'div[aria-label*="tulo"]',
                                        'div[aria-label*="itle"]',
                                        'div[aria-label*="Título"]',
                                        'div[aria-label*="Title"]',
                                        'div[aria-label*="playlist"]',
                                        'ytcp-form-input-container div[contenteditable]',
                                        '.input-container div[contenteditable]'
                                    ];
                                    for (var sel of selectors) {
                                        var el = pd.querySelector(sel);
                                        if (el && el.offsetParent !== null) {
                                            el.focus();
                                            el.click();
                                            el.textContent = '';
                                            return 'focused:' + sel;
                                        }
                                    }
                                }

                                // Fallback: any visible tp-yt-paper-dialog
                                var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
                                for (var d of dialogs) {
                                    if (d.offsetHeight > 50 && getComputedStyle(d).display !== 'none') {
                                        var tb = d.querySelector('#textbox[contenteditable], div[contenteditable="true"], div[role="textbox"]');
                                        if (tb && tb.offsetParent !== null) {
                                            tb.focus();
                                            tb.click();
                                            tb.textContent = '';
                                            return 'focused_dialog';
                                        }
                                    }
                                }

                                // Last fallback: any #textbox inside playlist area
                                var allTb = document.querySelectorAll('ytcp-playlist-dialog #textbox, ytcp-playlist-dialog div[contenteditable="true"]');
                                for (var el of allTb) {
                                    if (el.offsetParent !== null && el.offsetHeight > 0 && el.offsetHeight < 100) {
                                        el.focus();
                                        el.click();
                                        el.textContent = '';
                                        return 'focused_last';
                                    }
                                }
                                return 'no_creation_dialog';
                            """)
                            if 'focused' in str(focused):
                                break
                            time.sleep(2)  # wait and retry

                        if 'focused' in str(focused):
                            # Step 4: Type playlist name via JS + keyboard fallback
                            time.sleep(0.5)
                            # Set via JS first
                            driver.execute_script("""
                                var el = document.activeElement;
                                if (el && el.contentEditable === 'true') {
                                    el.textContent = '';
                                    el.innerText = arguments[0];
                                    el.dispatchEvent(new Event('input', {bubbles: true}));
                                    el.dispatchEvent(new Event('change', {bubbles: true}));
                                }
                            """, playlist_name)
                            # Also send via keyboard to ensure registration
                            try:
                                active = driver.switch_to.active_element
                                active.send_keys(Keys.END)
                            except Exception:
                                pass
                            time.sleep(2)

                            # Step 4b: Set visibility to "Não listada" / "Unlisted"
                            unlisted_result = driver.execute_script("""
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
                                    var dropdowns = d.querySelectorAll('tp-yt-paper-dropdown-menu, ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, .dropdown-trigger-text, #visibility-dropdown, [class*="visibility"]');
                                    for (var dd of dropdowns) {
                                        var txt = (dd.textContent || '').toLowerCase();
                                        if (txt.includes('public') || txt.includes('pública') || txt.includes('público') ||
                                            txt.includes('privad') || txt.includes('private') ||
                                            txt.includes('unlisted') || txt.includes('não listada') || txt.includes('não listado')) {
                                            var trigger = dd.querySelector('#trigger, .dropdown-trigger, button') || dd;
                                            trigger.click();
                                            return 'opened_dropdown';
                                        }
                                    }
                                }
                                return 'no_visibility_dropdown';
                            """)
                            print(f"  [PLAYLIST] Visibility dropdown: {unlisted_result}")
                            time.sleep(3)

                            if unlisted_result == 'opened_dropdown':
                                set_unlisted = driver.execute_script("""
                                    var items = document.querySelectorAll('tp-yt-paper-item, [role="option"], [role="menuitem"]');
                                    for (var item of items) {
                                        var txt = (item.textContent || '').toLowerCase();
                                        if (txt.includes('unlisted') || txt.includes('não listada') ||
                                            txt.includes('não listado') || txt.includes('nao listada') || txt.includes('nao listado')) {
                                            item.click();
                                            return 'set_unlisted';
                                        }
                                    }
                                    return 'unlisted_not_found';
                                """)
                                print(f"  [PLAYLIST] Set unlisted: {set_unlisted}")
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
                            time.sleep(5)
                            print(f"  [PLAYLIST] Create: {created}")
                            if created == 'created':
                                print(f"  [OK] Playlist criada: {playlist_name}")
                            else:
                                print(f"  [AVISO] Falha ao criar playlist: {created}")
                        else:
                            print(f"  [AVISO] Nao focou no titulo: {focused}")
                    else:
                        print(f"  [AVISO] Menu 'Nova playlist' nao encontrado")
                elif 'clicked' in str(playlist_result):
                    print(f"  [OK] Playlist selecionada: {playlist_name}")
                elif playlist_result == 'already_checked':
                    print(f"  [OK] Playlist ja marcada: {playlist_name}")
                else:
                    print(f"  [AVISO] Playlist resultado: {playlist_result}")

                # Close playlist dialog - "Concluir" / "Done"
                time.sleep(2)
                close_result = driver.execute_script("""
                    var dialog = document.querySelector('ytcp-playlist-dialog');
                    if (dialog) {
                        var allElements = dialog.querySelectorAll('ytcp-button, button, div');
                        for (var el of allElements) {
                            var txt = (el.textContent || '').trim().toLowerCase();
                            if (txt === 'concluir' || txt === 'done') {
                                el.click();
                                return 'closed: ' + txt;
                            }
                        }
                    }

                    // Fallback: any visible "Concluir"/"Done" that is NOT #done-button
                    var allBtns = document.querySelectorAll('ytcp-button, button');
                    for (var b of allBtns) {
                        if (b.id === 'done-button') continue;
                        if (b.offsetParent === null) continue;
                        var txt = (b.textContent || '').trim().toLowerCase();
                        if (txt === 'concluir' || txt === 'done') {
                            b.click();
                            return 'closed_fallback: ' + txt;
                        }
                    }
                    return 'no_close_btn';
                """)
                print(f"  [PLAYLIST] Fechar dialog: {close_result}")
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
            if (radios.length >= 2) { radios[1].click(); return true; }
            return false;
        """)
        if clicked_not_kids:
            print("  [OK] Marcado: nao e conteudo para criancas")
    except Exception:
        print("  [AVISO] Nao conseguiu marcar 'nao e para criancas'")

    # Navigate: Details -> Video elements -> Checks -> Visibility (3 Next clicks)
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

    # Wait for upload to complete
    print("  [UPLOAD] Aguardando upload completar...")
    video_id = None
    start_time = time.time()
    last_progress = ""
    stall_count = 0
    saw_percentage = False
    MIN_UPLOAD_WAIT = 30

    while time.time() - start_time < UPLOAD_TIMEOUT:
        try:
            status = driver.execute_script("""
                var result = {progress: '', doneEnabled: false, error: '', uploadComplete: false, videoId: ''};

                var dialog = document.querySelector('ytcp-uploads-dialog, ytcp-upload-dialog');
                var searchRoot = dialog || document;

                var errorEls = searchRoot.querySelectorAll('.error-short, .error-message, .error-area');
                for (var el of errorEls) {
                    var txt = (el.textContent || '').trim();
                    if (txt && txt.length > 5 && txt.length < 200 && el.children.length < 5 &&
                        (txt.includes('limit') || txt.includes('limite') || txt.includes('erro') ||
                         txt.includes('error') || txt.includes('falha') || txt.includes('fail') ||
                         txt.includes('cota') || txt.includes('quota') || txt.includes('diário') ||
                         txt.includes('daily'))) {
                        result.error = txt.substring(0, 150);
                        break;
                    }
                }

                var progressEls = searchRoot.querySelectorAll(
                    '.progress-label, .ytcp-video-upload-progress, span.ytcp-uploads-dialog-header, ' +
                    'span[class*="progress"], div[class*="progress"], .upload-status, ' +
                    'ytcp-video-upload-progress-renderer span, ytcp-uploads-dialog span'
                );
                if (dialog) {
                    var dialogSpans = dialog.querySelectorAll('span, div.label');
                    progressEls = Array.from(progressEls).concat(Array.from(dialogSpans));
                }
                for (var el of progressEls) {
                    var txt = (el.textContent || '').trim();
                    if (txt.length > 2 && txt.length < 120 && el.children.length < 3) {
                        if (txt.match(/\\d+\\s*%/) ||
                            txt.includes('Enviando') || txt.includes('Uploading') ||
                            txt.includes('processando') || txt.includes('processing') ||
                            txt.includes('Upload conclu') || txt.includes('Upload complete') ||
                            txt.includes('Verificações') || txt.includes('checks') ||
                            txt.includes('Processamento conclu') || txt.includes('Processing complete')) {
                            result.progress = txt;
                            if (txt.includes('Upload conclu') || txt.includes('Upload complete') ||
                                txt.includes('Processamento conclu') || txt.includes('Processing complete') ||
                                txt.match(/100\\s*%/)) {
                                result.uploadComplete = true;
                            }
                            break;
                        }
                    }
                }

                if (dialog) {
                    var dialogLinks = dialog.querySelectorAll('a[href]');
                    for (var a of dialogLinks) {
                        var href = a.href || '';
                        var m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/) ||
                                href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/) ||
                                href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                        if (m) { result.videoId = m[1]; break; }
                    }
                    if (!result.videoId) {
                        var vidEls = dialog.querySelectorAll('[video-id], [data-video-id]');
                        for (var el of vidEls) {
                            var vid = el.getAttribute('video-id') || el.getAttribute('data-video-id') || '';
                            if (vid.match(/^[a-zA-Z0-9_-]{11}$/)) { result.videoId = vid; break; }
                        }
                    }
                }

                var doneBtn = document.querySelector('#done-button');
                if (doneBtn) {
                    var disabled = doneBtn.hasAttribute('disabled') ||
                                   doneBtn.getAttribute('aria-disabled') === 'true';
                    result.doneEnabled = !disabled;
                }

                return result;
            """)

            elapsed = int(time.time() - start_time)

            limit_msg = check_daily_limit(driver)
            if limit_msg:
                print(f"  [LIMITE DIARIO] {limit_msg}")
                return "DAILY_LIMIT"

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

            if progress_text and ('%' in progress_text or 'Enviando' in progress_text or 'Uploading' in progress_text):
                saw_percentage = True

            dialog_vid = status.get('videoId', '')
            if dialog_vid:
                video_id = dialog_vid

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

            if elapsed < MIN_UPLOAD_WAIT:
                time.sleep(5)
                continue

            if upload_complete and done:
                print(f"  [OK] Upload completo confirmado ({elapsed}s)")
                break

            if done and saw_percentage and elapsed > 60:
                print(f"  [OK] Done habilitado + progresso detectado ({elapsed}s)")
                break

            if done and elapsed > 90:
                print(f"  [OK] Done habilitado por tempo suficiente ({elapsed}s)")
                break

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

    # Try to find video ID from dialog
    if not video_id:
        print("  [BUSCA] Tentando encontrar video ID no dialog...")
        for attempt in range(10):
            time.sleep(3)
            try:
                dialog_vid = driver.execute_script("""
                    var dialog = document.querySelector('ytcp-uploads-dialog, ytcp-upload-dialog');
                    if (!dialog) return null;
                    var links = dialog.querySelectorAll('a[href]');
                    for (var a of links) {
                        var href = a.href || '';
                        var m = href.match(/youtu\\.be\\/([a-zA-Z0-9_-]{11})/) ||
                                href.match(/watch\\?v=([a-zA-Z0-9_-]{11})/) ||
                                href.match(/\\/video\\/([a-zA-Z0-9_-]{11})/);
                        if (m) return m[1];
                    }
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

    # Click Done button
    done_clicked = False
    print("  [DONE] Aguardando botao Concluir ficar habilitado...")
    for wait_attempt in range(30):
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
        # Handle "Publicar mesmo assim" confirmation
        time.sleep(3)
        for confirm_attempt in range(5):
            try:
                confirmed = driver.execute_script("""
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
                    var dialogTexts = document.querySelectorAll('span, p, div, yt-formatted-string');
                    for (var el of dialogTexts) {
                        var txt = (el.textContent || '').trim();
                        if (txt.includes('verificando seu conte') || txt.includes('still checking')) {
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

        print("  [POS-UPLOAD] Aguardando YouTube registrar o upload...")
        time.sleep(5)

        for post_wait in range(6):
            try:
                post_status = driver.execute_script("""
                    var allBtns = document.querySelectorAll('ytcp-button, tp-yt-paper-button, button');
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

        time.sleep(5)
    else:
        print("  [AVISO] Botao 'Concluir' nao foi clicado!")

    # Try to find video ID after Done
    if not video_id:
        try:
            url = driver.current_url
            m = re.search(r'/video/([a-zA-Z0-9_-]{11})', url)
            if m:
                video_id = m.group(1)
                print(f"  [OK] Video ID da URL: {video_id}")
        except Exception:
            pass

    if not video_id:
        new_id = find_new_video_id(driver, pre_upload_ids)
        if new_id:
            video_id = new_id
            print(f"  [OK] Video ID pos-Done: {video_id}")

    # Close post-upload dialog
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
        return "UPLOADED_NO_ID"

    print("  [FALHA] Upload nao completou")
    return None


def close_upload_dialog(driver):
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

    try:
        driver.execute_script("""
            var btn = document.querySelector('ytcp-button#close-button');
            if (btn && btn.offsetParent !== null) btn.click();
        """)
        time.sleep(2)
    except Exception:
        pass

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


# =============================================================
# MAIN
# =============================================================

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"uploaded": {}, "playlists": {}}


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_results(results):
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    print("=" * 60)
    print("  YOUTUBE PLAYLIST UPLOADER - Portfolio Savylla Adryan")
    print("  Upload individual + Playlists por cliente")
    print("=" * 60)
    print()
    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print()

    # Load data
    with open(VIDEOS_JSON, "r", encoding="utf-8") as f:
        client_videos = json.load(f)

    progress = load_progress()
    results = load_results()

    # Collect known video IDs
    known_ids = set()
    for entry in progress["uploaded"].values():
        vid = entry.get("video_id", "")
        if vid and vid != "UPLOADED_NO_ID" and len(vid) == 11:
            known_ids.add(vid)

    total_videos = sum(len(v) for v in client_videos.values())
    already_done = len(progress["uploaded"])
    remaining = total_videos - already_done

    print(f"[INFO] {len(known_ids)} video IDs ja conhecidos")
    print(f"Total de videos: {total_videos}")
    print(f"Ja enviados: {already_done}")
    print(f"Restantes: {remaining}")
    print()

    if already_done >= total_videos:
        print("Todos os videos ja foram enviados!")
        return

    print("[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Start Chrome
    print("[BROWSER] Abrindo Chrome...")
    try:
        driver = create_driver()
    except Exception as e:
        print(f"[ERRO] Nao conseguiu abrir o Chrome: {e}")
        sys.exit(1)

    # Verify YouTube login
    print("[BROWSER] Verificando login no YouTube Studio...")
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    current_url = driver.current_url
    if "accounts.google.com" in current_url or "studio.youtube.com" not in current_url:
        print("[AVISO] Voce nao esta logado! Aguardando login no navegador...")
        for _ in range(60):
            time.sleep(2)
            try:
                current_url = driver.current_url
                if "studio.youtube.com" in current_url and "accounts.google.com" not in current_url:
                    break
            except Exception:
                pass
        time.sleep(3)

    # Verify channel
    try:
        channel_info = driver.execute_script("""
            var name = '';
            var els = document.querySelectorAll('.channel-name, [id*="channel-name"], .ytcp-channel-name');
            for (var el of els) {
                var txt = (el.textContent || '').trim();
                if (txt.length > 1) { name = txt; break; }
            }
            if (!name) {
                var imgs = document.querySelectorAll('img[alt]');
                for (var img of imgs) {
                    var alt = img.alt || '';
                    if (alt.length > 1 && alt.length < 50 && !alt.includes('YouTube')) {
                        name = alt; break;
                    }
                }
            }
            return {name: name, url: window.location.href};
        """)
        ch_name = channel_info.get('name', '')
        print(f"\n[CANAL] Nome: {ch_name or '(nao detectado)'}")
        if ch_name and 'savylla' not in ch_name.lower() and 'adryan' not in ch_name.lower():
            print(f"  ATENCAO: Canal detectado = '{ch_name}' (esperado: Savylla Adryan)")
            print(f"  Aguardando 30s para trocar de conta...")
            time.sleep(30)
    except Exception:
        pass

    print("[OK] YouTube Studio carregado!")

    # Check if ClickUp login needed
    has_clickup = any(
        "clickup" in v["url"].lower()
        for vlist in client_videos.values()
        for v in vlist
    )

    if has_clickup:
        print("\n[BROWSER] Abrindo ClickUp para login...")
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
                    if "clickup.com" in clickup_url and \
                       "login" not in clickup_url.lower() and \
                       "sso" not in clickup_url.lower() and \
                       "accounts.google" not in clickup_url.lower():
                        break
                except Exception:
                    pass

        clickup_url = driver.current_url
        if "clickup.com" in clickup_url and "login" not in clickup_url.lower():
            print("[OK] ClickUp logado!\n")
        else:
            print("[AVISO] ClickUp pode nao estar logado.\n")

        driver.get("https://studio.youtube.com")
        time.sleep(5)

    print()

    # Process each client
    video_counter = 0
    success_count = 0
    errors = 0
    MAX_ERRORS = 3

    try:
        for client_name, videos in client_videos.items():
            print(f"\n{'-' * 60}")
            print(f"  CLIENTE: {client_name} ({len(videos)} videos)")
            print(f"{'-' * 60}")

            client_remaining = 0
            for i, video in enumerate(videos, 1):
                video_key = f"{client_name}_{i:03d}"
                if video_key not in progress["uploaded"]:
                    client_remaining += 1

            if client_remaining == 0:
                print(f"  [SKIP] Todos os videos deste cliente ja foram enviados")
                continue

            print(f"  {client_remaining} videos restantes")

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
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    downloaded = download_video(url, filepath, driver)

                if not downloaded:
                    print(f"  [SKIP] Nao foi possivel baixar - pulando")
                    try:
                        if "studio.youtube.com" not in driver.current_url:
                            driver.get("https://studio.youtube.com")
                            time.sleep(5)
                    except Exception:
                        pass
                    continue

                # Ensure on YouTube Studio
                try:
                    if "studio.youtube.com" not in driver.current_url:
                        driver.get("https://studio.youtube.com")
                        time.sleep(5)
                except Exception:
                    pass

                # Pad video if too short (anti-Shorts)
                upload_filepath = pad_video_to_avoid_shorts(filepath)

                # Upload
                video_id = upload_video_selenium(driver, upload_filepath, title, description, known_ids, client_name)

                # Clean up padded file if different from original
                if upload_filepath != filepath:
                    try:
                        os.remove(upload_filepath)
                    except Exception:
                        pass

                if video_id == "DAILY_LIMIT":
                    print(f"\n[PARADA] Limite diario do YouTube atingido!")
                    print("O progresso foi salvo - retome amanha.")
                    close_upload_dialog(driver)
                    errors = MAX_ERRORS
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

                    print(f"  [WAIT] Aguardando {UPLOAD_DELAY}s...")
                    time.sleep(UPLOAD_DELAY)

                else:
                    errors += 1
                    print(f"  [ERRO] Upload falhou para {video_key} (erro {errors}/{MAX_ERRORS})")
                    close_upload_dialog(driver)
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
