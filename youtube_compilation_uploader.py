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
import unicodedata
from pathlib import Path
from urllib.parse import unquote
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build as build_youtube_api

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
UPLOAD_DELAY = 5
UPLOAD_TIMEOUT = 900  # 15 min per video

# Anti-Shorts: pillarbox converts vertical (9:16) to horizontal (16:9)
# YouTube classifies Shorts by aspect ratio, not just duration
# Video is NOT rescaled — original resolution is preserved, only black bars are added

# Chrome debug port
CHROME_DEBUG_PORT = 9555

# Cache of playlists that failed to be created (avoid retrying every video)
_playlist_create_failed = set()

# YouTube Data API - playlist cache {name: playlist_id}
_playlist_cache = {}
_youtube_api = None
_api_disabled = False  # True apos falha de credencial: impede fluxo OAuth interativo
TOKEN_FILE = "token.json"
CLIENT_SECRET_FILE = "client_secret.json"
YT_SCOPES = ["https://www.googleapis.com/auth/youtube"]


def _save_yt_credentials(creds):
    """Save OAuth2 credentials to token.json."""
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes) if creds.scopes else YT_SCOPES,
        "expiry": creds.expiry.isoformat() + "Z" if creds.expiry else None,
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)


def get_youtube_api():
    """Get or create YouTube Data API service (singleton)."""
    global _youtube_api
    # Desligado apos falha irrecuperavel de credencial: sem isto, cada chamada
    # seguinte cairia no fluxo OAuth interativo (run_local_server) e travaria
    # uma execucao nao supervisionada.
    if _api_disabled:
        return None
    if _youtube_api is not None:
        return _youtube_api

    creds = None

    # Try loading existing token
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                token_data = json.load(f)
            creds = Credentials(
                token=token_data.get("token"),
                refresh_token=token_data.get("refresh_token"),
                token_uri=token_data.get("token_uri"),
                client_id=token_data.get("client_id"),
                client_secret=token_data.get("client_secret"),
                scopes=token_data.get("scopes", YT_SCOPES),
            )
        except Exception:
            creds = None

    # Try refreshing
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_yt_credentials(creds)
        except Exception:
            creds = None

    # If still invalid, try OAuth flow
    if not creds or not creds.valid:
        if os.path.exists(CLIENT_SECRET_FILE):
            try:
                from google_auth_oauthlib.flow import InstalledAppFlow
                print("[API] Token invalido. Abrindo navegador para re-autenticacao...")
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, YT_SCOPES)
                creds = flow.run_local_server(port=8090, open_browser=True)
                _save_yt_credentials(creds)
                print("[API] Re-autenticacao concluida.")
            except Exception as e:
                print(f"[API] OAuth flow falhou: {str(e)[:80]}")
                return None
        else:
            print("[API] token.json invalido e client_secret.json ausente - playlists NAO serao atribuidas")
            return None

    try:
        _youtube_api = build_youtube_api("youtube", "v3", credentials=creds)
        print("[API] YouTube Data API v3 conectada com sucesso")
        return _youtube_api
    except Exception as e:
        print(f"[API] Falha ao conectar API: {str(e)[:80]}")
        return None


def load_playlist_cache():
    """Load all existing playlists from the channel into cache."""
    global _playlist_cache
    youtube = get_youtube_api()
    if not youtube:
        return

    print("[API] Carregando playlists existentes do canal...")
    _playlist_cache = {}
    next_page = None

    while True:
        request = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page,
        )
        response = request.execute()

        for item in response.get("items", []):
            name = item["snippet"]["title"]
            pid = item["id"]
            # If duplicate name, keep the first one (oldest)
            if name not in _playlist_cache:
                _playlist_cache[name] = pid

        next_page = response.get("nextPageToken")
        if not next_page:
            break

    print(f"[API] {len(_playlist_cache)} playlists carregadas no cache")
    for name, pid in sorted(_playlist_cache.items()):
        print(f"  - {name} ({pid})")


def api_find_or_create_playlist(playlist_name):
    """Find existing playlist or create new one via API. Returns playlist_id or None."""
    youtube = get_youtube_api()
    if not youtube:
        return None

    # Check cache first
    if playlist_name in _playlist_cache:
        return _playlist_cache[playlist_name]

    # Not in cache - create it (with retry for rate limits)
    for attempt in range(4):
        try:
            print(f"  [API] Criando playlist '{playlist_name}'{'...' if attempt == 0 else f' (tentativa {attempt + 1}/4)...'}")
            request = youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": playlist_name,
                        "description": f"Portfolio Savylla Adryan - {playlist_name.replace('Portfolio - ', '')}",
                    },
                    "status": {
                        "privacyStatus": "unlisted",
                    },
                },
            )
            response = request.execute()
            pid = response["id"]
            _playlist_cache[playlist_name] = pid
            print(f"  [API] Playlist criada: {playlist_name} ({pid})")
            return pid
        except Exception as e:
            err_str = str(e)
            if '429' in err_str or 'quota' in err_str.lower() or 'rate' in err_str.lower():
                if attempt < 3:
                    wait = (attempt + 1) * 15
                    print(f"  [API] Rate limit (429) - aguardando {wait}s antes de tentar novamente...")
                    time.sleep(wait)
                    continue
            print(f"  [API] Erro ao criar playlist '{playlist_name}': {err_str[:80]}")
            return None
    print(f"  [API] Erro: rate limit persistente para '{playlist_name}'")
    return None


def api_add_video_to_playlist(playlist_id, video_id):
    """Add a video to a playlist via API."""
    youtube = get_youtube_api()
    if not youtube:
        return False

    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id,
                    },
                },
            },
        ).execute()
        return True
    except Exception as e:
        error_str = str(e)
        if "duplicate" in error_str.lower() or "already" in error_str.lower():
            print(f"  [API] Video {video_id} ja esta na playlist")
            return True
        print(f"  [API] Erro ao adicionar video {video_id} a playlist: {error_str[:80]}")
        return False

# Fix broken accents from client_videos.json (encoding issues in source data)
ACCENT_FIXES = {
    # Client names
    "Atacad o": "Atacadão",
    "Faculdade Est cio": "Faculdade Estácio",
    "For\ufffda da Terra": "Força da Terra",
    "Philco Brit nia": "Philco Britânia",
    "Nestl /": "Nestlé /",
    # Talento/title name fragments (applied globally)
    "Jo o Mendes": "João Mendes",
    "Jo o Victor": "João Victor",
    "Joa\u0303o": "João",  # combining tilde
    "D bora Melo": "Débora Melo",
    "D bora Mel": "Débora Mel",  # truncated in filenames
    "Andr Lemos": "André Lemos",
    "Maria Lu za": "Maria Luíza",
    "Lu za Kropotoff": "Luíza Kropotoff",
    "Qu ren Hapuque": "Quéren Hapuque",
    "Let cia Pedro": "Letícia Pedro",
    "Vit ria Rodrigues": "Vitória Rodrigues",
    "J lia Horta": "Júlia Horta",
    "Val rio": "Valério",
    "For\ufffda da Terra": "Força da Terra",
    "Cabe\ufffda": "Cabeça",
    "Pablo Sant Anna": "Pablo Sant'Anna",
    "Isadora cecatto": "Isadora Cecatto",
    "Est cio": "Estácio",
    "Brit nia": "Britânia",
    # HTML entities that survive in filenames
    "Joa&#771;o": "João",
}


def fix_accents(text):
    """Fix broken accents and HTML entities in text."""
    text = html.unescape(text)  # Fix &Iacute; &#771; etc.
    text = unicodedata.normalize('NFC', text)  # a + combining tilde -> ã
    # Apply manual fixes for corrupted chars
    for broken, fixed in ACCENT_FIXES.items():
        if broken in text:
            text = text.replace(broken, fixed)
    return text



# (Phase 0 playlist pre-creation removed - CSS selectors broken in current YouTube Studio)


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
    except Exception as e:
        print(f"  [AVISO] taskkill falhou: {str(e)[:60]}")

    chrome_cmd = [
        chrome_path,
        f"--remote-debugging-port={CHROME_DEBUG_PORT}",
        f"--user-data-dir={custom_data_dir}",
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--log-level=3",
    ]
    print(f"[BROWSER] Iniciando Chrome (porta {CHROME_DEBUG_PORT})...")
    subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(12)

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


def source_key(url):
    """Chave normalizada de um arquivo-fonte, para deteccao de duplicata.

    Usa o nome do arquivo (sem query string, sem escape de URL, minusculo).
    O mesmo criterio do fallback de migrate_clickup_to_youtube.py: a URL do
    ClickUp carrega parametros volateis (ust/usg), entao comparar a URL crua
    deixa duplicata passar.
    """
    if not url:
        return None
    limpo = clean_url(url).split("?")[0]
    nome = unquote(limpo.split("/")[-1]).strip().lower()
    return nome or None


def build_source_index(results):
    """Indexa fontes ja enviadas: {chave_do_arquivo: (video_id, cliente)}.

    Evita reenviar o mesmo arquivo — foi assim que 9 videos duplicados
    entraram no canal e precisaram ser apagados manualmente depois.
    """
    idx = {}
    for cliente, vids in results.items():
        for v in vids:
            vid = v.get("video_id")
            if not vid or vid == "UPLOADED_NO_ID" or len(vid) != 11:
                continue
            for campo in ("original_url", "source_url"):
                k = source_key(v.get(campo))
                if k:
                    idx.setdefault(k, (vid, cliente))
    return idx


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
            "-c:v", "libx264", "-crf", "23", "-preset", "ultrafast",
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
                "-c:v", "libx264", "-crf", "23", "-preset", "ultrafast",
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
        download_url = url

        # Google Drive sharing links: convert to direct download URL
        gdrive_match = re.search(r'drive\.google\.com/file/d/([^/]+)', url)
        if gdrive_match:
            file_id = gdrive_match.group(1)
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            print(f"(GDrive) ", end="", flush=True)

        result = subprocess.run(
            ["curl", "-sL", "--max-time", "180", "--connect-timeout", "15",
             "-o", filepath, download_url],
            timeout=210,
            capture_output=True
        )
        if result.returncode == 0 and is_valid_video(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"OK ({size_mb:.1f} MB)")
            return True

        # Google Drive large files need confirm token to bypass virus scan warning
        if gdrive_match and os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(10000)
                confirm_match = re.search(r'confirm=([0-9A-Za-z_-]+)', content)
                if confirm_match or 'download_warning' in content or 'virus scan' in content.lower():
                    token = confirm_match.group(1) if confirm_match else 't'
                    confirm_url = f"https://drive.google.com/uc?export=download&confirm={token}&id={file_id}"
                    os.remove(filepath)
                    print(f"(confirm) ", end="", flush=True)
                    result = subprocess.run(
                        ["curl", "-sL", "--max-time", "180", "--connect-timeout", "15",
                         "-o", filepath, confirm_url],
                        timeout=210,
                        capture_output=True
                    )
                    if result.returncode == 0 and is_valid_video(filepath):
                        size_mb = os.path.getsize(filepath) / (1024 * 1024)
                        print(f"OK ({size_mb:.1f} MB)")
                        return True
            except Exception:
                pass

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
    except Exception as e:
        print(f"  [AVISO] collect_existing_video_ids falhou: {str(e)[:80]}")
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
                if (el.offsetParent === null) continue;
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
        except Exception as e:
            err_str = str(e).lower()
            if 'session' in err_str or 'disconnected' in err_str or 'connection' in err_str:
                print(f"\n  [ERRO FATAL] Sessao do browser perdida: {str(e)[:80]}")
                return None
            # DOM errors are expected during page transitions
            pass
        time.sleep(2)
    return None


def upload_video_selenium(driver, filepath, title, description, known_ids, client_name=""):
    """Upload a single video via YouTube Studio and add to client playlist."""
    abs_path = os.path.abspath(filepath)

    driver.get("https://studio.youtube.com")
    time.sleep(3)

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
        time.sleep(1.5)
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
        time.sleep(2)
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

    # Set title (with retry — YouTube Studio form can take a while to render)
    try:
        textboxes = []
        for attempt in range(6):
            time.sleep(3)
            textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox[contenteditable='true']")
            if not textboxes:
                textboxes = driver.find_elements(By.CSS_SELECTOR, "#textbox")
            if textboxes:
                break
            print(f"  [RETRY] Aguardando campos de texto... ({attempt+1}/6)")

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

    # NOTE: Playlist assignment is now handled AFTER upload via YouTube Data API
    # (see main loop - api_add_video_to_playlist call after getting video_id)
    # Old Selenium playlist logic removed — it caused duplicate playlists due to
    # virtual scrolling in YouTube Studio not loading all playlists reliably.
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
            time.sleep(1)
            driver.execute_script("""
                var btn = document.querySelector('#next-button');
                if (btn) btn.click();
            """)
            time.sleep(1)
        except Exception:
            break

    # Verify we reached the visibility page
    time.sleep(1)
    on_visibility_page = driver.execute_script("""
        var radios = document.querySelectorAll('tp-yt-paper-radio-button');
        for (var r of radios) {
            var txt = (r.textContent || '').toLowerCase();
            if (txt.includes('unlisted') || txt.includes('nao listado') || txt.includes('não listado') ||
                txt.includes('public') || txt.includes('privat')) {
                return true;
            }
        }
        return false;
    """)
    if not on_visibility_page:
        print("  [ERRO] Nao chegou na pagina de visibilidade - ABORTANDO upload")
        close_upload_dialog(driver)
        return None

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
            print("  [ERRO] Nao encontrou opcao 'nao listado' - ABORTANDO upload para evitar video publico")
            close_upload_dialog(driver)
            return None
    except Exception:
        print("  [ERRO] Nao conseguiu definir como nao listado - ABORTANDO upload para evitar video publico")
        close_upload_dialog(driver)
        return None

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
                has_limit_word = any(w in err_lower for w in ['limite', 'limit', 'cota', 'quota'])
                has_daily_word = any(w in err_lower for w in ['diário', 'diario', 'daily'])
                if has_limit_word and has_daily_word:
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
        time.sleep(2)

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

        time.sleep(2)
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
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or "uploaded" not in data:
                print(f"[AVISO] {PROGRESS_FILE} com estrutura invalida, recriando...")
                ts = int(time.time())
                shutil.copy2(PROGRESS_FILE, f"{PROGRESS_FILE}.corrupted.{ts}")
                return {"uploaded": {}, "playlists": {}}
            return data
        except json.JSONDecodeError:
            ts = int(time.time())
            corrupted_path = f"{PROGRESS_FILE}.corrupted.{ts}"
            shutil.copy2(PROGRESS_FILE, corrupted_path)
            print(f"[AVISO] {PROGRESS_FILE} corrompido! Backup salvo em {corrupted_path}")
            # Try .bak file
            bak_path = PROGRESS_FILE + ".bak"
            if os.path.exists(bak_path):
                try:
                    with open(bak_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, dict) and "uploaded" in data:
                        print(f"[RECUPERADO] Usando backup {bak_path}")
                        return data
                except Exception:
                    pass
            return {"uploaded": {}, "playlists": {}}
    return {"uploaded": {}, "playlists": {}}


def save_progress(progress):
    tmp_path = PROGRESS_FILE + ".tmp"
    bak_path = PROGRESS_FILE + ".bak"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    if os.path.exists(PROGRESS_FILE):
        shutil.copy2(PROGRESS_FILE, bak_path)
    os.replace(tmp_path, PROGRESS_FILE)


def load_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            ts = int(time.time())
            corrupted_path = f"{RESULTS_FILE}.corrupted.{ts}"
            shutil.copy2(RESULTS_FILE, corrupted_path)
            print(f"[AVISO] {RESULTS_FILE} corrompido! Backup salvo em {corrupted_path}")
            bak_path = RESULTS_FILE + ".bak"
            if os.path.exists(bak_path):
                try:
                    with open(bak_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    pass
            return {}
    return {}


def save_results(results):
    tmp_path = RESULTS_FILE + ".tmp"
    bak_path = RESULTS_FILE + ".bak"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    if os.path.exists(RESULTS_FILE):
        shutil.copy2(RESULTS_FILE, bak_path)
    os.replace(tmp_path, RESULTS_FILE)


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

    # Restore playlist failures from previous sessions
    for pf in progress.get("playlist_failures", []):
        _playlist_create_failed.add(pf)
    if _playlist_create_failed:
        print(f"[INFO] {len(_playlist_create_failed)} playlists com falha de sessoes anteriores")

    total_videos = sum(len(v) for v in client_videos.values())
    already_done = len(progress["uploaded"])

    # Contar pendentes pelas chaves que faltam, nao pela diferenca de totais:
    # progress["uploaded"] pode conter chaves que nao existem mais no catalogo
    # (ex.: cliente renumerado), inflando o total e mascarando videos pendentes.
    pending_keys = [
        f"{client_name_raw}_{i:03d}"
        for client_name_raw, videos in client_videos.items()
        for i in range(1, len(videos) + 1)
        if f"{client_name_raw}_{i:03d}" not in progress["uploaded"]
    ]
    remaining = len(pending_keys)

    # Indice de arquivos-fonte ja enviados (deduplicacao)
    source_index = build_source_index(results)
    skipped_duplicates = 0
    print(f"[DEDUP] {len(source_index)} arquivos-fonte ja mapeados para videos existentes")

    print(f"[INFO] {len(known_ids)} video IDs ja conhecidos")
    print(f"Total de videos: {total_videos}")
    print(f"Ja enviados: {already_done}")
    print(f"Restantes: {remaining}")
    if pending_keys:
        print(f"Pendentes: {', '.join(fix_accents(k) for k in pending_keys[:10])}"
              + (" ..." if len(pending_keys) > 10 else ""))
    print()

    # Check ffprobe availability
    try:
        subprocess.run(["ffprobe", "-version"], capture_output=True, timeout=10)
        print("[OK] ffprobe disponivel - pillarbox anti-Shorts ativo")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("[AVISO] ffprobe NAO encontrado - videos verticais serao enviados sem pillarbox (podem virar Shorts)")

    if remaining == 0:
        print("Todos os videos ja foram enviados!")
        return

    # Initialize YouTube Data API for playlist management
    print()
    youtube_api = get_youtube_api()
    if youtube_api:
        # get_youtube_api() so monta o cliente; o token so e validado na 1a
        # requisicao. Um refresh_token expirado (invalid_grant) estourava aqui e
        # abortava o upload inteiro, apesar de existir fallback sem API.
        try:
            load_playlist_cache()
        except Exception as e:
            youtube_api = None
            globals()["_youtube_api"] = None
            globals()["_api_disabled"] = True
            print(f"[AVISO] YouTube API falhou ({type(e).__name__}: {str(e)[:120]})")
            print("        Seguindo SEM atribuicao de playlists.")
            print("        Execute 'python youtube_playlist_manager.py --full' depois para corrigir.")
    else:
        print("[AVISO] YouTube API indisponivel - playlists NAO serao atribuidas durante o upload")
        print("        Execute 'python youtube_playlist_manager.py --full' depois para corrigir.")
    print()

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
    for nav_attempt in range(3):
        try:
            driver.get("https://studio.youtube.com")
            time.sleep(5)
            current_url = driver.current_url
            break
        except Exception as e:
            if nav_attempt < 2:
                print(f"  [RETRY] Navegacao falhou ({nav_attempt + 1}/3), recriando driver...")
                try:
                    driver.quit()
                except Exception:
                    pass
                time.sleep(3)
                driver = create_driver()
                time.sleep(3)
            else:
                print(f"[ERRO] Chrome nao consegue acessar YouTube Studio: {e}")
                sys.exit(1)

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
            print(f"  [ERRO FATAL] Canal detectado = '{ch_name}' (esperado: Savylla Adryan)")
            print(f"  PARANDO para evitar upload no canal errado!")
            driver.quit()
            sys.exit(1)
        elif not ch_name:
            print(f"  [AVISO] Nome do canal nao detectado (pode ser problema de seletor)")
    except Exception as e:
        print(f"  [AVISO] Erro ao verificar canal: {str(e)[:60]}")

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

    # Playlists are created inline during upload (Phase 0 removed - CSS selectors broken)

    # Process each client
    video_counter = 0
    success_count = 0
    errors = 0
    MAX_ERRORS = 3

    try:
        for client_name_raw, videos in client_videos.items():
            client_name = fix_accents(client_name_raw)
            print(f"\n{'-' * 60}")
            print(f"  CLIENTE: {client_name} ({len(videos)} videos)")
            print(f"{'-' * 60}")

            client_remaining = 0
            for i, video in enumerate(videos, 1):
                video_key = f"{client_name_raw}_{i:03d}"
                if video_key not in progress["uploaded"]:
                    client_remaining += 1

            if client_remaining == 0:
                print(f"  [SKIP] Todos os videos deste cliente ja foram enviados")
                continue

            print(f"  {client_remaining} videos restantes")

            for i, video in enumerate(videos, 1):
                url = video["url"]
                talento = fix_accents(video.get("talento", ""))
                video_key = f"{client_name_raw}_{i:03d}"

                if video_key in progress["uploaded"]:
                    continue

                # Deduplicacao por arquivo-fonte: se este mp4 ja virou video no
                # canal (mesmo sob outro cliente), reaproveita em vez de subir de
                # novo. Sem isto o mesmo arquivo pode gerar 2 videos no YouTube.
                skey = source_key(url)
                if skey and skey in source_index:
                    dup_id, dup_cliente = source_index[skey]
                    print(f"\n[{video_counter + 1}/{total_videos}] {client_name} - {skey[:60]}")
                    print(f"  [DUPLICADO] Arquivo ja enviado como {dup_id}"
                          + (f" (cliente '{fix_accents(dup_cliente)}')" if dup_cliente != client_name_raw else ""))
                    # garante que o video existente esteja na playlist DESTE cliente
                    if get_youtube_api():
                        pl_nome = f"Portfolio - {client_name}"
                        pl_id = api_find_or_create_playlist(pl_nome)
                        if pl_id and api_add_video_to_playlist(pl_id, dup_id):
                            print(f"  [API] Vinculado a '{pl_nome}'")
                    progress["uploaded"][video_key] = {
                        "video_id": dup_id,
                        "url": f"https://youtu.be/{dup_id}",
                        "title": "(reaproveitado de upload anterior)",
                        "client": client_name,
                        "deduplicado_de": dup_cliente,
                    }
                    save_progress(progress)
                    skipped_duplicates += 1
                    continue

                video_counter += 1
                video_name = fix_accents(extract_video_name(url))
                title = f"{client_name} - {video_name}"
                if talento:
                    title = f"{client_name} - {talento} - {video_name}"
                title = fix_accents(title)
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
                    progress["playlist_failures"] = sorted(_playlist_create_failed)
                    save_progress(progress)

                    # Add video to client playlist via YouTube Data API
                    if client_name and video_id and video_id != "UPLOADED_NO_ID":
                        playlist_name = f"Portfolio - {client_name}"
                        playlist_id = api_find_or_create_playlist(playlist_name)
                        if playlist_id:
                            if api_add_video_to_playlist(playlist_id, video_id):
                                print(f"  [API] Video adicionado a '{playlist_name}'")
                            else:
                                print(f"  [API] Falha ao adicionar video a '{playlist_name}'")
                        else:
                            print(f"  [API] Nao conseguiu obter/criar playlist '{playlist_name}'")
                            _playlist_create_failed.add(playlist_name)

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

                    # Registra a fonte no indice para nao reenviar o mesmo
                    # arquivo mais adiante na propria sessao.
                    if skey and video_id and video_id != "UPLOADED_NO_ID":
                        source_index.setdefault(skey, (video_id, client_name_raw))

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
        # Retry failed playlists: create playlists and add videos that were uploaded but not assigned
        if _playlist_create_failed:
            print(f"\n[RETRY-PLAYLISTS] Tentando criar {len(_playlist_create_failed)} playlists que falharam...")
            fixed_playlists = []
            for playlist_name in list(_playlist_create_failed):
                client_name = playlist_name.replace("Portfolio - ", "")
                print(f"\n  [RETRY] {playlist_name}...")
                time.sleep(10)  # wait before retrying to avoid rate limits
                playlist_id = api_find_or_create_playlist(playlist_name)
                if playlist_id:
                    # Find all uploaded videos for this client and add them
                    added = 0
                    for vkey, vdata in progress.get("uploaded", {}).items():
                        if vdata.get("client") == client_name:
                            vid = vdata.get("video_id", "")
                            if vid and vid != "UPLOADED_NO_ID":
                                if api_add_video_to_playlist(playlist_id, vid):
                                    added += 1
                                time.sleep(1)
                    print(f"  [OK] {playlist_name}: {added} videos adicionados")
                    fixed_playlists.append(playlist_name)
                else:
                    print(f"  [FALHOU] {playlist_name}: ainda nao foi possivel criar")

            for pn in fixed_playlists:
                _playlist_create_failed.discard(pn)
            progress["playlist_failures"] = sorted(_playlist_create_failed)
            save_progress(progress)
            if fixed_playlists:
                print(f"  [RETRY-PLAYLISTS] {len(fixed_playlists)} playlists corrigidas!")
        total_uploaded = len(progress["uploaded"])
        print(f"\n{'=' * 60}")
        print(f"  RESUMO")
        print(f"  Videos enviados nesta sessao: {success_count}")
        if skipped_duplicates:
            print(f"  Duplicados evitados (fonte ja no canal): {skipped_duplicates}")
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
