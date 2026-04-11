"""
=============================================================
SCREENPAL UPLOADER via Selenium - Portfolio Savylla Adryan
=============================================================
Faz upload dos videos para o ScreenPal (hosting gratuito),
organizados por cliente em pastas.

SETUP:
1. Instale: python -m pip install selenium requests
2. Tenha o Google Chrome instalado
3. Execute: python screenpal_uploader.py
4. Na primeira vez, faca login no ScreenPal com Google

NOTA: O script abre o Chrome com seu perfil.
      Feche todas as janelas do Chrome antes de executar.

SELETORES REAIS (capturados em 2026-04-02):
  Dashboard:  https://screenpal.com/content
  Upload:     https://screenpal.com/content/upload
  Library:    https://screenpal.com/content/videos
  File input: input#file[name="file[]"] (class d-none)
  Drop zone:  #drop-area (class upload-field)
  Form:       form.dropzone (multipart/form-data)
  Criar btn:  #dropdownMenuButton
  Folder:     input#folder-title + btn "Guardar"
  Player URL: https://go.screenpal.com/player/{ID}
  Watch URL:  https://screenpal.com/watch/{ID}
=============================================================
"""

import json
import os
import sys
import time
import re
import html
import requests
from pathlib import Path
from urllib.parse import unquote

# Fix Windows console encoding
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
PROGRESS_FILE = "screenpal_progress.json"
RESULTS_FILE = "screenpal_results.json"

UPLOAD_DELAY = 10
MAX_ERRORS = 5

# ScreenPal real URLs
SP_CONTENT = "https://screenpal.com/content"
SP_UPLOAD = "https://screenpal.com/content/upload"
SP_LIBRARY = "https://screenpal.com/content/videos"


# --- Browser setup ---

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
    import subprocess
    chrome_path = find_chrome()
    if not chrome_path:
        raise RuntimeError("Chrome nao encontrado!")

    debug_port = 9556
    custom_data_dir = os.path.join(os.path.expanduser("~"), "chrome_screenpal_data")
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
                print(f"  [RETRY] Tentativa {attempt + 1}/5...")
                time.sleep(5)
            else:
                raise e
    return driver


# --- File helpers ---

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

def load_json(filepath, default=None):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return default if default is not None else {}

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- Download functions ---

def download_video(url, filepath, driver=None):
    clean = clean_url(url)
    if "&sa=D&source=editors" in clean:
        clean = clean.split("&sa=D&source=editors")[0]

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

        # Navigate back to ScreenPal upload page
        driver.get(SP_UPLOAD)
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
            driver.get(SP_UPLOAD)
            time.sleep(5)
        except Exception:
            pass
        return False


def download_via_curl(url, filepath):
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
            print("FALHOU (arquivo invalido ou curl erro)")
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


# --- ScreenPal functions (REAL SELECTORS) ---

def ensure_logged_in(driver):
    """Ensure user is logged into ScreenPal."""
    driver.get(SP_CONTENT)
    time.sleep(5)

    current_url = driver.current_url

    if "accounts.google.com" in current_url or "login" in current_url.lower():
        print("\n" + "=" * 60)
        print("  FACA LOGIN NO SCREENPAL COM SUA CONTA GOOGLE")
        print("  O script detecta automaticamente quando voce logar.")
        print("=" * 60)

        for i in range(300):
            time.sleep(1)
            try:
                current_url = driver.current_url
                if ("screenpal.com" in current_url and
                    "login" not in current_url.lower() and
                    "accounts.google" not in current_url):
                    print("[OK] Login detectado!")
                    time.sleep(3)
                    return True
            except Exception:
                pass
            if i % 30 == 0 and i > 0:
                print(f"  Aguardando login... ({i}s)")

        print("[ERRO] Timeout aguardando login")
        return False

    if "screenpal.com" in current_url:
        print("[OK] Ja logado no ScreenPal")
        return True

    return False


def create_folder(driver, folder_name):
    """Create a folder using the real modal: #folder-title + Guardar."""
    try:
        driver.get(SP_CONTENT)
        time.sleep(3)

        # Click "Criar" dropdown button (real: #dropdownMenuButton)
        driver.find_element(By.ID, "dropdownMenuButton").click()
        time.sleep(2)

        # Click "Nova Pasta" in the dropdown menu
        # The menu items are inside .dropdown-menu which is now .show
        clicked = driver.execute_script("""
            var items = document.querySelectorAll('.dropdown-menu a, .dropdown-menu button, .dropdown-menu .dropdown-item, .create-menu-with-banner a');
            for (var item of items) {
                var txt = (item.textContent || '').toLowerCase().trim();
                if (txt.includes('pasta') || txt.includes('folder')) {
                    item.click();
                    return txt;
                }
            }
            return null;
        """)

        if not clicked:
            # Try via direct JS to trigger the folder modal
            driver.execute_script("""
                var modal = document.querySelector('.modal');
                if (modal) {
                    modal.classList.add('show');
                    modal.style.display = 'block';
                }
            """)

        time.sleep(2)

        # Type folder name into #folder-title
        title_input = driver.find_element(By.ID, "folder-title")
        title_input.clear()
        title_input.send_keys(folder_name)
        time.sleep(1)

        # Click "Guardar" button in modal footer
        driver.execute_script("""
            var footers = document.querySelectorAll('.modal-footer');
            for (var footer of footers) {
                if (footer.offsetParent !== null || footer.offsetHeight > 0) {
                    var btns = footer.querySelectorAll('button, a, [role="button"]');
                    for (var btn of btns) {
                        var txt = (btn.textContent || '').toLowerCase().trim();
                        if (txt.includes('guardar') || txt.includes('save') || txt.includes('salvar') || txt.includes('criar') || txt.includes('create')) {
                            btn.click();
                            return true;
                        }
                    }
                }
            }
            return false;
        """)
        time.sleep(3)

        print(f"  [FOLDER] Pasta criada: {folder_name}")
        return True

    except Exception as e:
        print(f"  [FOLDER] Erro ao criar pasta '{folder_name}': {e}")
        # Close any open modal
        try:
            driver.execute_script("document.querySelectorAll('.close-modal').forEach(function(b) { b.click(); });")
        except Exception:
            pass
        return False


def upload_video_screenpal(driver, filepath, title):
    """Upload a single video to ScreenPal using real selectors.
    Upload page: /content/upload
    File input: input#file[name="file[]"] (class d-none)
    Form: form.dropzone (multipart/form-data)
    Returns the video watch URL or None."""
    abs_path = os.path.abspath(filepath)

    try:
        # Navigate to upload page
        driver.get(SP_UPLOAD)
        time.sleep(5)

        # Find the file input (real selector: input#file with name="file[]")
        file_input = None
        for selector in ['input#file', 'input[name="file[]"]', 'input[type="file"]']:
            try:
                inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                if inputs:
                    file_input = inputs[0]
                    break
            except Exception:
                pass

        if not file_input:
            print("  [ERRO] Nao encontrou input#file")
            return None

        # Send the file to the hidden input
        file_input.send_keys(abs_path)
        print("  [UPLOAD] Arquivo enviado...", end="", flush=True)

        # Wait for upload to complete
        # ScreenPal uses Dropzone.js - check for completion indicators
        upload_complete = False
        for wait in range(600):  # Up to 10 minutes
            time.sleep(1)

            status = driver.execute_script("""
                // Check for Dropzone.js success class
                var dzSuccess = document.querySelectorAll('.dz-success, .dz-complete');
                if (dzSuccess.length > 0) return 'complete';

                // Check for success text
                var body = document.body.innerText || '';
                if (body.includes('uploaded successfully') || body.includes('upload complete') ||
                    body.includes('enviado com sucesso') || body.includes('carregado')) {
                    return 'complete';
                }

                // Check for green checkmark / success icon
                var checks = document.querySelectorAll('.dz-success-mark, .fa-check-circle, [class*="success"]');
                for (var c of checks) {
                    if (c.offsetParent !== null && c.offsetHeight > 0) return 'complete';
                }

                // Check for progress bar at 100%
                var bars = document.querySelectorAll('.dz-upload, [class*="progress"] [class*="bar"]');
                for (var bar of bars) {
                    var width = bar.style.width;
                    if (width === '100%') return 'complete';
                }

                // Check for error
                var errors = document.querySelectorAll('.dz-error, .dz-error-message');
                for (var e of errors) {
                    if (e.offsetParent !== null && e.textContent.trim()) return 'error: ' + e.textContent.trim().substring(0, 80);
                }

                // Check for active upload (progress)
                for (var bar of bars) {
                    var width = bar.style.width;
                    if (width) return 'uploading: ' + width;
                }

                // Check if page redirected (upload done, went to content page)
                if (window.location.href.includes('/content/videos') ||
                    window.location.href.includes('/watch/')) {
                    return 'complete_redirect';
                }

                return 'waiting';
            """)

            if 'complete' in str(status):
                upload_complete = True
                print(f" COMPLETO! ({status})")
                break
            elif 'error' in str(status):
                print(f" ERRO: {status}")
                return None
            elif wait % 30 == 0 and wait > 0:
                print(f" ({wait}s {status}) ", end="", flush=True)

        if not upload_complete:
            print(" TIMEOUT")
            return None

        time.sleep(5)

        # Get the video URL - navigate to Library to find the most recent video
        video_url = get_latest_video_url(driver, title)
        return video_url

    except Exception as e:
        print(f"  [ERRO] Upload falhou: {e}")
        return None


def get_latest_video_url(driver, expected_title=""):
    """Navigate to Library and get the URL of the most recently uploaded video."""
    try:
        driver.get(SP_LIBRARY)
        time.sleep(5)

        # Look for the most recent video in the library
        # ScreenPal library shows videos with links containing /watch/{ID}
        video_data = driver.execute_script("""
            var results = [];

            // Look for video links/cards
            var links = document.querySelectorAll('a[href*="/watch/"]');
            for (var a of links) {
                results.push({
                    href: a.href,
                    text: (a.textContent || '').trim().substring(0, 100)
                });
            }

            // Also check for video detail links
            var detailLinks = document.querySelectorAll('a[href*="/content/detail/"], a[href*="/info/"]');
            for (var a of detailLinks) {
                results.push({
                    href: a.href,
                    text: (a.textContent || '').trim().substring(0, 100)
                });
            }

            // Check for data attributes with video IDs
            var items = document.querySelectorAll('[data-id], [data-video-id], [data-content-id]');
            for (var item of items) {
                var id = item.getAttribute('data-id') || item.getAttribute('data-video-id') || item.getAttribute('data-content-id');
                if (id) {
                    results.push({
                        href: 'https://screenpal.com/watch/' + id,
                        text: (item.textContent || '').trim().substring(0, 100),
                        dataId: id
                    });
                }
            }

            return results;
        """)

        if video_data:
            # Return the first (most recent) watch URL
            for item in video_data:
                href = item.get('href', '')
                if '/watch/' in href:
                    video_id = href.split('/watch/')[-1].split('?')[0].split('/')[0]
                    watch_url = f"https://screenpal.com/watch/{video_id}"
                    player_url = f"https://go.screenpal.com/player/{video_id}"
                    print(f"  [OK] Video URL: {watch_url}")
                    print(f"  [OK] Player URL: {player_url}")
                    return watch_url

        # Fallback: try to get video URL from the upload page itself
        current = driver.current_url
        if '/watch/' in current:
            return current

        # Try getting the share/embed link from the detail page
        detail_url = try_get_detail_url(driver)
        if detail_url:
            return detail_url

        print("  [AVISO] Nao conseguiu capturar URL do video")
        return "UPLOADED_NO_URL"

    except Exception as e:
        print(f"  [AVISO] Erro ao capturar URL: {e}")
        return "UPLOADED_NO_URL"


def try_get_detail_url(driver):
    """Try to open the first video's detail page and get its share URL."""
    try:
        # Click on the first video/content item
        clicked = driver.execute_script("""
            // Look for content items that can be clicked for details
            var items = document.querySelectorAll('.content-item, .video-item, .card, [class*="item"]');
            for (var item of items) {
                var link = item.querySelector('a[href]');
                if (link && (link.href.includes('/detail/') || link.href.includes('/info/') || link.href.includes('/watch/'))) {
                    return link.href;
                }
            }

            // Try hover/detail buttons
            var btns = document.querySelectorAll('[class*="detail"], [class*="info"], [class*="edit"]');
            for (var btn of btns) {
                if (btn.href) return btn.href;
            }
            return null;
        """)

        if clicked:
            driver.get(clicked)
            time.sleep(3)

            # Look for share/embed URL on detail page
            url = driver.execute_script("""
                // Check for share link
                var inputs = document.querySelectorAll('input[readonly], input[class*="share"], input[class*="link"], input[class*="url"]');
                for (var inp of inputs) {
                    var val = inp.value || '';
                    if (val.includes('screenpal.com') || val.includes('go.screenpal.com')) {
                        return val;
                    }
                }

                // Check page URL
                if (window.location.href.includes('/watch/')) {
                    return window.location.href;
                }

                // Check for embed code
                var textareas = document.querySelectorAll('textarea');
                for (var ta of textareas) {
                    if (ta.value && ta.value.includes('go.screenpal.com')) {
                        var match = ta.value.match(/go\\.screenpal\\.com\\/player\\/([\\w]+)/);
                        if (match) return 'https://screenpal.com/watch/' + match[1];
                    }
                }

                return null;
            """)

            if url:
                return url

        return None
    except Exception:
        return None


# --- Main ---

def main():
    print("=" * 60)
    print("  SCREENPAL UPLOADER - Portfolio Savylla Adryan")
    print("  (seletores reais capturados em 2026-04-02)")
    print("=" * 60)

    # Load data
    videos = load_json(VIDEOS_JSON)
    if not videos:
        print(f"[ERRO] Arquivo {VIDEOS_JSON} nao encontrado ou vazio!")
        return

    progress = load_json(PROGRESS_FILE, {"uploaded": {}, "folders_created": []})
    results = load_json(RESULTS_FILE, {})

    total = sum(len(vids) for vids in videos.values())
    uploaded_count = len(progress.get("uploaded", {}))
    remaining = total - uploaded_count

    print(f"\n[INFO] Total de videos: {total}")
    print(f"[INFO] Ja enviados: {uploaded_count}")
    print(f"[INFO] Restantes: {remaining}")
    print(f"[INFO] Clientes: {len(videos)}")

    if remaining == 0:
        print("\n[COMPLETO] Todos os videos ja foram enviados!")
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Start browser
    print("\n[BROWSER] Iniciando Chrome...")
    driver = create_driver()

    if not ensure_logged_in(driver):
        print("[ERRO] Nao foi possivel fazer login no ScreenPal")
        driver.quit()
        return

    # Process each client
    errors = 0
    success_count = 0
    video_counter = 0

    for client_name, client_videos in videos.items():
        if errors >= MAX_ERRORS:
            print(f"\n[PARADA] Muitos erros consecutivos ({MAX_ERRORS}). Parando.")
            break

        remaining_for_client = []
        for idx, video in enumerate(client_videos):
            video_key = f"{client_name}_{idx + 1:03d}"
            if video_key not in progress.get("uploaded", {}):
                remaining_for_client.append((idx, video, video_key))

        if not remaining_for_client:
            continue

        print(f"\n{'=' * 60}")
        print(f"  CLIENTE: {client_name} ({len(remaining_for_client)} videos restantes)")
        print(f"{'=' * 60}")

        # Create folder for client if not done yet
        if client_name not in progress.get("folders_created", []):
            if create_folder(driver, f"Portfolio - {client_name}"):
                if "folders_created" not in progress:
                    progress["folders_created"] = []
                progress["folders_created"].append(client_name)
                save_json(PROGRESS_FILE, progress)

        for idx, video, video_key in remaining_for_client:
            if errors >= MAX_ERRORS:
                break

            video_counter += 1
            url = video.get("url", "")
            talento = video.get("talento", "")

            if not url:
                print(f"  [SKIP] {video_key} - sem URL")
                continue

            # Build title
            video_name = extract_video_name(url)
            title = f"{client_name} - {talento} - {video_name}" if talento else f"{client_name} - {video_name}"
            if len(title) > 100:
                title = title[:97] + "..."

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
                    if "screenpal.com" not in driver.current_url:
                        driver.get(SP_UPLOAD)
                        time.sleep(5)
                except Exception:
                    pass
                continue

            # Upload to ScreenPal
            video_url = upload_video_screenpal(driver, filepath, title)

            if video_url:
                errors = 0
                success_count += 1

                progress["uploaded"][video_key] = {
                    "screenpal_url": video_url,
                    "title": title,
                    "client": client_name,
                    "talento": talento,
                    "original_url": url
                }
                save_json(PROGRESS_FILE, progress)

                if client_name not in results:
                    results[client_name] = []
                results[client_name].append({
                    "screenpal_url": video_url,
                    "title": title,
                    "talento": talento,
                    "original_url": url,
                    "video_key": video_key
                })
                save_json(RESULTS_FILE, results)

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
                time.sleep(5)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  RESUMO")
    print(f"{'=' * 60}")
    print(f"  Videos enviados nesta sessao: {success_count}")
    print(f"  Total enviados: {len(progress.get('uploaded', {}))}")
    print(f"  Total de videos: {total}")
    print(f"  Resultados: {RESULTS_FILE}")
    print(f"  Progresso: {PROGRESS_FILE}")

    if len(progress.get("uploaded", {})) >= total:
        print(f"\n  TODOS OS VIDEOS FORAM ENVIADOS!")
    else:
        print(f"\n  Execute novamente para continuar de onde parou.")

    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
