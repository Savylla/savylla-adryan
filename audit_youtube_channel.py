"""
=============================================================
AUDIT YOUTUBE CHANNEL - Savylla Adryan Portfolio
=============================================================
Audita TODOS os videos do canal verificando conformidade:
- Titulos sem acentos quebrados
- Descricoes sem acentos quebrados
- Visibilidade = Nao listado
- Video esta na playlist "Portfolio - {cliente}"

NAO corrige nada — apenas AUDITA e REPORTA.

USO: python audit_youtube_channel.py
=============================================================
"""

import json
import os
import sys
import time
import subprocess
import shutil
import html
import unicodedata
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- CONFIG ---
RESULTS_FILE = "youtube_results.json"
AUDIT_PROGRESS_FILE = "audit_progress.json"
AUDIT_REPORT_FILE = "audit_report.json"
CHROME_DEBUG_PORT = 9555

# Fix broken accents (same dict from uploader / fix_titles)
ACCENT_FIXES = {
    # Client names
    "Atacad o": "Atacadão",
    "Faculdade Est cio": "Faculdade Estácio",
    "For\ufffda da Terra": "Força da Terra",
    "Philco Brit nia": "Philco Britânia",
    "Nestl /": "Nestlé /",
    # Talento/title name fragments
    "Jo o Mendes": "João Mendes",
    "Jo o Victor": "João Victor",
    "Joa\u0303o": "João",
    "D bora Melo": "Débora Melo",
    "D bora Mel": "Débora Mel",
    "Andr Lemos": "André Lemos",
    "Maria Lu za": "Maria Luíza",
    "Lu za Kropotoff": "Luíza Kropotoff",
    "Qu ren Hapuque": "Quéren Hapuque",
    "Let cia Pedro": "Letícia Pedro",
    "Vit ria Rodrigues": "Vitória Rodrigues",
    "J lia Horta": "Júlia Horta",
    "Val rio": "Valério",
    "Cabe\ufffda": "Cabeça",
    "Pablo Sant Anna": "Pablo Sant'Anna",
    "Isadora cecatto": "Isadora Cecatto",
    "Est cio": "Estácio",
    "Brit nia": "Britânia",
    "Joa&#771;o": "João",
}


def fix_accents(text):
    """Fix broken accents and HTML entities in text."""
    text = html.unescape(text)
    text = unicodedata.normalize('NFC', text)
    for broken, fixed in ACCENT_FIXES.items():
        if broken in text:
            text = text.replace(broken, fixed)
    return text


def has_broken_accents(text):
    """Check if text contains broken accents (would change after fix_accents)."""
    if not text:
        return False
    return fix_accents(text) != text


# =============================================================
# BROWSER SETUP (same pattern as other scripts)
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


# =============================================================
# PROGRESS (atomic write)
# =============================================================

def load_progress():
    if os.path.exists(AUDIT_PROGRESS_FILE):
        try:
            with open(AUDIT_PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Try backup
            bak = AUDIT_PROGRESS_FILE + ".bak"
            if os.path.exists(bak):
                try:
                    with open(bak, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    pass
    return {"audited": {}}


def save_progress(progress):
    tmp_path = AUDIT_PROGRESS_FILE + ".tmp"
    bak_path = AUDIT_PROGRESS_FILE + ".bak"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    if os.path.exists(AUDIT_PROGRESS_FILE):
        shutil.copy2(AUDIT_PROGRESS_FILE, bak_path)
    os.replace(tmp_path, AUDIT_PROGRESS_FILE)


def save_report(report):
    tmp_path = AUDIT_REPORT_FILE + ".tmp"
    bak_path = AUDIT_REPORT_FILE + ".bak"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    if os.path.exists(AUDIT_REPORT_FILE):
        shutil.copy2(AUDIT_REPORT_FILE, bak_path)
    os.replace(tmp_path, AUDIT_REPORT_FILE)


# =============================================================
# AUDIT FUNCTIONS
# =============================================================

def wait_for_editor(driver, timeout=20):
    """Wait for YouTube Studio video editor to load."""
    for _ in range(timeout // 2):
        ready = driver.execute_script("""
            return !!document.querySelector(
                '#title-textarea #textbox, ytcp-mention-textbox #textbox'
            );
        """)
        if ready:
            return True
        time.sleep(2)
    return False


def extract_title(driver):
    """Extract current video title from the editor."""
    return driver.execute_script("""
        var tb = document.querySelector(
            '#title-textarea #textbox, ytcp-mention-textbox #textbox'
        );
        return tb ? tb.textContent.trim() : null;
    """)


def extract_description(driver):
    """Extract current video description from the editor."""
    return driver.execute_script("""
        // The description textbox is the second textbox or inside #description-textarea
        var descBox = document.querySelector(
            '#description-textarea #textbox'
        );
        if (descBox) return descBox.textContent.trim();

        // Fallback: get all textboxes, second one is description
        var boxes = document.querySelectorAll(
            'ytcp-mention-textbox #textbox, #textbox'
        );
        if (boxes.length >= 2) return boxes[1].textContent.trim();

        return null;
    """)


def extract_visibility(driver):
    """Extract current video visibility from the editor page.

    Returns one of: 'public', 'unlisted', 'private', 'unknown'
    """
    return driver.execute_script("""
        // Method 1: Look for visibility badge/label in the page
        var visLabels = document.querySelectorAll(
            '.visibility-label, [class*="visibility"], ' +
            '.badge-shape-wiz--text, .label-text'
        );
        for (var el of visLabels) {
            var txt = (el.textContent || '').trim().toLowerCase();
            if (txt.includes('não listado') || txt.includes('unlisted') ||
                txt.includes('nao listado') || txt.includes('não listada')) {
                return 'unlisted';
            }
            if (txt.includes('público') || txt.includes('public') ||
                txt.includes('publica')) {
                return 'public';
            }
            if (txt.includes('privado') || txt.includes('private')) {
                return 'private';
            }
        }

        // Method 2: Check the visibility section/radio/dropdown
        var visSection = document.querySelector(
            'ytcp-video-visibility-select, #visibility-select'
        );
        if (visSection) {
            var txt = (visSection.textContent || '').toLowerCase();
            if (txt.includes('não listado') || txt.includes('unlisted')) return 'unlisted';
            if (txt.includes('público') || txt.includes('public')) return 'public';
            if (txt.includes('privado') || txt.includes('private')) return 'private';
        }

        // Method 3: Scan all text on the page for visibility indicators
        // in the metadata area (right side panel or inline)
        var allText = document.body ? document.body.innerText : '';
        // Look for the pattern near "Visibilidade" or "Visibility"
        var match = allText.match(
            /(?:visibilidade|visibility)[:\\s]*(não listado|unlisted|público|public|privado|private)/i
        );
        if (match) {
            var found = match[1].toLowerCase();
            if (found.includes('não listado') || found.includes('unlisted')) return 'unlisted';
            if (found.includes('público') || found.includes('public')) return 'public';
            if (found.includes('privado') || found.includes('private')) return 'private';
        }

        // Method 4: Check for the visibility icon/badge near the save button area
        var badges = document.querySelectorAll(
            'tp-yt-paper-badge, .badge, [class*="badge"], ' +
            'ytcp-badge-shape, .ytcp-badge-shape'
        );
        for (var b of badges) {
            var t = (b.textContent || '').trim().toLowerCase();
            if (t.includes('não listado') || t.includes('unlisted')) return 'unlisted';
            if (t.includes('público') || t.includes('public')) return 'public';
            if (t.includes('privado') || t.includes('private')) return 'private';
        }

        // Method 5: Check radio buttons that might be pre-selected
        var radios = document.querySelectorAll(
            'tp-yt-paper-radio-button[checked], ' +
            '[role="radio"][aria-checked="true"]'
        );
        for (var r of radios) {
            var rt = (r.textContent || '').toLowerCase();
            if (rt.includes('não listado') || rt.includes('unlisted')) return 'unlisted';
            if (rt.includes('público') || rt.includes('public')) return 'public';
            if (rt.includes('privado') || rt.includes('private')) return 'private';
        }

        return 'unknown';
    """)


def extract_quality(driver):
    """Extract video quality/resolution info from YouTube Studio.

    Returns a dict with resolution, processing status, and whether it's a Short.
    """
    return driver.execute_script("""
        var result = {resolution: 'unknown', is_short: false, processing: 'unknown'};

        // Method 1: Look for resolution text in the video info panel
        // YouTube Studio shows resolution in the right panel or video details
        var allText = document.body ? document.body.innerText : '';

        // Check for resolution patterns like "1080p", "720p", "4K", "SD", "HD"
        var resMatch = allText.match(/(\\d{3,4})\\s*[xX×]\\s*(\\d{3,4})/);
        if (resMatch) {
            result.resolution = resMatch[1] + 'x' + resMatch[2];
        } else {
            // Try common labels
            var resLabels = allText.match(/(4320p|2160p|1440p|1080p|720p|480p|360p|240p|144p|4K|HD|SD)/i);
            if (resLabels) {
                result.resolution = resLabels[1];
            }
        }

        // Method 2: Check video info elements in Studio
        var infoEls = document.querySelectorAll(
            '.video-info, .video-details, [class*="quality"], [class*="resolution"], ' +
            'ytcp-video-info span, .metadata-row span, .video-metadata span'
        );
        for (var el of infoEls) {
            var txt = (el.textContent || '').trim();
            var m = txt.match(/(\\d{3,4})\\s*[xX×]\\s*(\\d{3,4})/);
            if (m) {
                result.resolution = m[1] + 'x' + m[2];
                break;
            }
        }

        // Method 3: Check for Shorts indicator
        var shortsEls = document.querySelectorAll(
            '[class*="short"], .short-indicator, .shorts-badge'
        );
        for (var el of shortsEls) {
            var txt = (el.textContent || '').toLowerCase();
            if (txt.includes('short')) {
                result.is_short = true;
                break;
            }
        }

        // Also check if aspect ratio info suggests Short (9:16)
        if (result.resolution !== 'unknown') {
            var parts = result.resolution.split(/[xX×]/);
            if (parts.length === 2) {
                var w = parseInt(parts[0]);
                var h = parseInt(parts[1]);
                if (h > w * 1.3) {
                    result.is_short = true;
                }
            }
        }

        // Check for Shorts in URL or page text
        if (allText.toLowerCase().includes('short') &&
            (allText.toLowerCase().includes('este vídeo é um short') ||
             allText.toLowerCase().includes('this video is a short'))) {
            result.is_short = true;
        }

        // Method 4: Processing status
        var processingEls = document.querySelectorAll(
            '.processing-status, [class*="processing"], [class*="upload-status"]'
        );
        for (var el of processingEls) {
            var txt = (el.textContent || '').trim().toLowerCase();
            if (txt.includes('processando') || txt.includes('processing')) {
                result.processing = 'processing';
            } else if (txt.includes('hd') || txt.includes('completo') || txt.includes('complete')) {
                result.processing = 'complete';
            }
        }

        // Method 5: Check the video player/preview for resolution info
        var playerInfo = document.querySelector('.video-preview-container, ytcp-video-preview');
        if (playerInfo) {
            var pTxt = playerInfo.textContent || '';
            var pm = pTxt.match(/(\\d{3,4})\\s*[xX×]\\s*(\\d{3,4})/);
            if (pm) {
                result.resolution = pm[1] + 'x' + pm[2];
            }
        }

        return result;
    """)


def expand_show_more(driver):
    """Click 'Mostrar mais' / 'Show more' button if present."""
    driver.execute_script("""
        var btns = document.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt.includes('mostrar mais') || txt.includes('show more')) {
                b.click();
                break;
            }
        }
    """)


def extract_playlists(driver):
    """Open the playlist dropdown and extract which playlists are checked.

    Returns a list of playlist names that this video belongs to.
    Does NOT modify anything — only reads state.
    """
    # First, open the playlist dropdown
    opened = driver.execute_script("""
        var trigger = document.querySelector(
            'ytcp-dropdown-trigger[aria-label*="playlist"], ' +
            'ytcp-dropdown-trigger[aria-label*="Playlist"]'
        );
        if (trigger && trigger.offsetParent !== null) {
            trigger.click();
            return 'clicked_aria';
        }

        var vmp = document.querySelector('ytcp-video-metadata-playlists');
        if (vmp) {
            var inner = vmp.querySelector(
                'ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, button'
            );
            if (inner) { inner.click(); return 'clicked_vmp_inner'; }
            vmp.click();
            return 'clicked_vmp';
        }

        var triggers = document.querySelectorAll(
            'ytcp-text-dropdown-trigger, ytcp-dropdown-trigger'
        );
        for (var t of triggers) {
            var aria = (t.getAttribute('aria-label') || '').toLowerCase();
            if (aria.includes('playlist')) {
                t.click();
                return 'clicked_fallback';
            }
        }

        return 'no_playlist_trigger';
    """)

    if opened == 'no_playlist_trigger':
        return None  # Could not open — signal to caller

    time.sleep(2)

    # Read checked playlists
    checked = driver.execute_script("""
        var results = [];
        // Method 1: checkbox items with aria-checked
        var items = document.querySelectorAll(
            'ytcp-checkbox-group-item, ' +
            'tp-yt-paper-checkbox, ' +
            '[role="checkbox"]'
        );
        for (var item of items) {
            var isChecked = (
                item.getAttribute('aria-checked') === 'true' ||
                item.hasAttribute('checked') ||
                item.classList.contains('checked')
            );
            if (isChecked) {
                var label = item.querySelector(
                    '.label, .checkbox-label, span'
                );
                var name = label
                    ? label.textContent.trim()
                    : item.textContent.trim();
                if (name && name.length < 200) {
                    results.push(name);
                }
            }
        }

        // Method 2: if no checkbox found, try iron-icon + label pattern
        if (results.length === 0) {
            var rows = document.querySelectorAll(
                '.playlist-item, .checkbox-item'
            );
            for (var r of rows) {
                var icon = r.querySelector(
                    'iron-icon[icon="check"], .checked-icon'
                );
                if (icon) {
                    var lbl = r.querySelector('.label, span');
                    if (lbl) results.push(lbl.textContent.trim());
                }
            }
        }

        return results;
    """)

    # Close the dropdown without saving by pressing Escape or clicking cancel
    driver.execute_script("""
        // Try to close without making changes — click Cancel/Cancelar
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt === 'cancelar' || txt === 'cancel') {
                if (b.offsetParent !== null) { b.click(); return; }
            }
        }
        // Fallback: press Escape
        document.dispatchEvent(
            new KeyboardEvent('keydown', {key: 'Escape', code: 'Escape', bubbles: true})
        );
    """)
    time.sleep(1)

    return checked if checked else []


def audit_single_video(driver, video_id, expected_client, expected_title):
    """Audit a single video by navigating to its edit page.

    Returns a dict with audit results.
    """
    result = {
        "title_ok": True,
        "desc_ok": True,
        "visibility_ok": True,
        "playlist_ok": True,
        "quality_ok": True,
        "issues": [],
        "actual_title": None,
        "actual_description_snippet": None,
        "actual_visibility": None,
        "actual_playlists": [],
        "expected_playlist": f"Portfolio - {expected_client}",
        "resolution": "unknown",
        "is_short": False,
    }

    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(3)

    # Wait for editor
    if not wait_for_editor(driver, timeout=20):
        result["issues"].append("ERRO: pagina nao carregou")
        result["title_ok"] = False
        result["desc_ok"] = False
        result["visibility_ok"] = False
        result["playlist_ok"] = False
        result["quality_ok"] = False
        return result

    # --- TITLE ---
    actual_title = extract_title(driver)
    result["actual_title"] = actual_title
    if actual_title is None:
        result["title_ok"] = False
        result["issues"].append("titulo nao encontrado na pagina")
    elif has_broken_accents(actual_title):
        result["title_ok"] = False
        fixed = fix_accents(actual_title)
        result["issues"].append(
            f"titulo com acento quebrado: \"{actual_title[:60]}\" -> \"{fixed[:60]}\""
        )

    # --- DESCRIPTION ---
    # Expand "Show more" first to access description
    expand_show_more(driver)
    time.sleep(1)

    actual_desc = extract_description(driver)
    if actual_desc:
        result["actual_description_snippet"] = actual_desc[:120]
    if actual_desc and has_broken_accents(actual_desc):
        result["desc_ok"] = False
        result["issues"].append("descricao com acento quebrado")

    # --- VISIBILITY ---
    actual_vis = extract_visibility(driver)
    result["actual_visibility"] = actual_vis
    if actual_vis == 'unknown':
        # Not a hard failure — might just be hard to detect
        result["issues"].append("visibilidade nao detectada (verificar manualmente)")
        result["visibility_ok"] = False
    elif actual_vis != 'unlisted':
        result["visibility_ok"] = False
        result["issues"].append(
            f"visibilidade incorreta: {actual_vis} (esperado: unlisted)"
        )

    # --- PLAYLISTS ---
    playlists = extract_playlists(driver)
    result["actual_playlists"] = playlists if playlists is not None else []

    expected_playlist = f"Portfolio - {fix_accents(expected_client)}"
    result["expected_playlist"] = expected_playlist

    if playlists is None:
        result["playlist_ok"] = False
        result["issues"].append("nao conseguiu abrir dropdown de playlists")
    elif not playlists:
        result["playlist_ok"] = False
        result["issues"].append("video sem nenhuma playlist")
    else:
        # Check if expected playlist is in the list (case-insensitive partial match)
        found = False
        for p in playlists:
            if expected_playlist.lower() in p.lower() or p.lower() in expected_playlist.lower():
                found = True
                break
        if not found:
            result["playlist_ok"] = False
            result["issues"].append(
                f"playlist incorreta: {playlists} (esperado: {expected_playlist})"
            )

    # --- QUALITY / RESOLUTION ---
    quality = extract_quality(driver)
    result["resolution"] = quality.get("resolution", "unknown")
    result["is_short"] = quality.get("is_short", False)

    if quality.get("is_short", False):
        result["quality_ok"] = False
        result["issues"].append(
            f"video classificado como Short (resolucao: {result['resolution']})"
        )

    if quality.get("processing") == "processing":
        result["issues"].append("video ainda em processamento pelo YouTube")

    return result


# =============================================================
# MAIN
# =============================================================

def main():
    print("=" * 60)
    print("  AUDIT YOUTUBE CHANNEL - Savylla Adryan")
    print("=" * 60)
    print(f"  Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Load reference data
    if not os.path.exists(RESULTS_FILE):
        print(f"[ERRO] Arquivo {RESULTS_FILE} nao encontrado!")
        return

    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Build flat list of all videos to audit
    all_videos = []
    for client, videos in results.items():
        for v in videos:
            all_videos.append({
                "video_id": v["video_id"],
                "expected_title": v["title"],
                "client": client,
                "talento": v.get("talento", ""),
            })

    total = len(all_videos)
    print(f"  Total de videos no youtube_results.json: {total}")
    print(f"  Clientes: {len(results)}")
    print()

    # Load progress
    progress = load_progress()
    already_done = set(progress.get("audited", {}).keys())
    remaining = [v for v in all_videos if v["video_id"] not in already_done]

    print(f"  Ja auditados (progresso salvo): {len(already_done)}")
    print(f"  Restantes: {len(remaining)}")
    print()

    if not remaining:
        print("  [OK] Todos os videos ja foram auditados!")
        print("  Gerando relatorio final...\n")
        generate_report(progress, all_videos, results)
        return

    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print("\n[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    # Start browser
    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

    # Verify YouTube Studio
    driver.get("https://studio.youtube.com")
    time.sleep(5)
    channel = driver.execute_script("""
        var el = document.querySelector(
            'ytcp-entity-name, .entity-name, #entity-name'
        );
        return el ? el.textContent.trim() : 'unknown';
    """)
    print(f"[CANAL] {channel}")
    print()

    # ============================================================
    #  FASE 0: Auditoria de playlists no nivel do canal
    # ============================================================
    print("=" * 60)
    print("  FASE 0: Auditoria de playlists do canal")
    print("=" * 60)

    driver.get("https://studio.youtube.com/channel/playlists")
    time.sleep(5)

    # Scroll to load all playlists
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # Extract all playlists with their video counts
    channel_playlists = driver.execute_script("""
        var playlists = [];
        // Try table rows
        var rows = document.querySelectorAll('tr, ytcp-playlist-row, .playlist-row');
        for (var r of rows) {
            var links = r.querySelectorAll('a[href*="/playlist/"]');
            var nameEl = r.querySelector('a.playlist-title, .title-column a, a[href*="playlist"]');
            var name = nameEl ? nameEl.textContent.trim() : '';
            if (!name) continue;

            // Try to get video count
            var cells = r.querySelectorAll('td, .cell, span');
            var count = 0;
            for (var c of cells) {
                var txt = (c.textContent || '').trim();
                var m = txt.match(/^(\\d+)$/);
                if (m && parseInt(m[1]) >= 0 && parseInt(m[1]) < 10000) {
                    count = parseInt(m[1]);
                }
            }

            // Get playlist ID from link
            var pid = '';
            if (links.length > 0) {
                var href = links[0].href || '';
                var pm = href.match(/playlist\\/([A-Za-z0-9_-]+)/);
                if (pm) pid = pm[1];
            }

            playlists.push({name: name, count: count, id: pid});
        }

        // Fallback: look for all playlist links
        if (playlists.length === 0) {
            var allLinks = document.querySelectorAll('a[href*="/playlist/"]');
            for (var l of allLinks) {
                var txt = l.textContent.trim();
                if (txt && txt.length > 2 && txt.length < 100) {
                    var href = l.href || '';
                    var pm = href.match(/playlist\\/([A-Za-z0-9_-]+)/);
                    playlists.push({name: txt, count: -1, id: pm ? pm[1] : ''});
                }
            }
        }

        return playlists;
    """)

    print(f"\n  Playlists encontradas: {len(channel_playlists)}")

    # Detect duplicates
    playlist_names = {}
    for p in channel_playlists:
        name = p.get("name", "")
        if name not in playlist_names:
            playlist_names[name] = []
        playlist_names[name].append(p)

    duplicates = {k: v for k, v in playlist_names.items() if len(v) > 1}
    empty_playlists = [p for p in channel_playlists if p.get("count", 0) == 0]

    if duplicates:
        print(f"\n  [PROBLEMA] Playlists DUPLICADAS encontradas:")
        for name, copies in duplicates.items():
            print(f"    '{name}' - {len(copies)} copias:")
            for c in copies:
                print(f"      ID: {c.get('id', '?')} - {c.get('count', '?')} videos")
    else:
        print("  [OK] Nenhuma playlist duplicada")

    if empty_playlists:
        print(f"\n  [AVISO] Playlists VAZIAS ({len(empty_playlists)}):")
        for p in empty_playlists:
            print(f"    '{p.get('name', '?')}' (ID: {p.get('id', '?')})")

    # Save playlist audit to progress
    progress["channel_playlists"] = {
        "total": len(channel_playlists),
        "playlists": channel_playlists,
        "duplicates": {k: len(v) for k, v in duplicates.items()},
        "empty_count": len(empty_playlists),
    }
    save_progress(progress)

    # Expected playlists per client
    expected = set(f"Portfolio - {fix_accents(c)}" for c in results.keys())
    found_names = set(p.get("name", "") for p in channel_playlists)
    missing = expected - found_names
    if missing:
        print(f"\n  [AVISO] Playlists FALTANDO ({len(missing)}):")
        for m in sorted(missing):
            print(f"    {m}")

    print()
    print("=" * 60)
    print("  FASE 1: Auditoria por video")
    print("=" * 60)
    print()

    # Audit loop
    success_count = 0
    error_count = 0

    for i, video in enumerate(remaining):
        vid = video["video_id"]
        client = video["client"]
        title = video["expected_title"]

        print(f"[{len(already_done) + i + 1}/{total}] {vid} ({client})")
        print(f"  Titulo esperado: {title[:70]}")

        try:
            audit_result = audit_single_video(
                driver, vid, client, title
            )

            # Determine status
            all_ok = (
                audit_result["title_ok"]
                and audit_result["desc_ok"]
                and audit_result["visibility_ok"]
                and audit_result["playlist_ok"]
                and audit_result["quality_ok"]
            )

            if all_ok:
                print(f"  [OK] Conforme")
                success_count += 1
            else:
                issues = audit_result["issues"]
                print(f"  [PROBLEMA] {len(issues)} issue(s):")
                for issue in issues:
                    print(f"    - {issue}")

            # Save to progress
            progress.setdefault("audited", {})[vid] = {
                "client": client,
                "title_ok": audit_result["title_ok"],
                "desc_ok": audit_result["desc_ok"],
                "visibility_ok": audit_result["visibility_ok"],
                "playlist_ok": audit_result["playlist_ok"],
                "quality_ok": audit_result["quality_ok"],
                "issues": audit_result["issues"],
                "actual_title": audit_result.get("actual_title"),
                "actual_visibility": audit_result.get("actual_visibility"),
                "actual_playlists": audit_result.get("actual_playlists", []),
                "expected_playlist": audit_result.get("expected_playlist"),
                "actual_description_snippet": audit_result.get(
                    "actual_description_snippet"
                ),
                "resolution": audit_result.get("resolution", "unknown"),
                "is_short": audit_result.get("is_short", False),
            }
            save_progress(progress)

        except Exception as e:
            error_count += 1
            error_msg = f"EXCEPTION: {str(e)[:100]}"
            print(f"  [ERRO] {error_msg}")

            # Save error in progress so we can retry later
            progress.setdefault("audited", {})[vid] = {
                "client": client,
                "title_ok": False,
                "desc_ok": False,
                "visibility_ok": False,
                "playlist_ok": False,
                "quality_ok": False,
                "issues": [error_msg],
            }
            save_progress(progress)

        # Small delay between navigations
        time.sleep(1.5)

    # Done — generate report
    print("\n" + "=" * 60)
    print("  Audit completo! Gerando relatorio...")
    print("=" * 60)

    generate_report(progress, all_videos, results)

    # Close browser
    print("\nFechando navegador em 5 segundos...")
    time.sleep(5)
    try:
        driver.quit()
    except Exception:
        pass


def generate_report(progress, all_videos, results):
    """Generate and print the final audit report."""
    audited = progress.get("audited", {})
    total_audited = len(audited)

    # Count issues by type
    title_issues = 0
    desc_issues = 0
    visibility_issues = 0
    playlist_issues = 0
    conformes = 0
    non_conformes = 0
    errors = 0

    problem_videos = []

    quality_issues = 0
    short_videos = 0

    for vid, data in audited.items():
        all_ok = (
            data.get("title_ok", False)
            and data.get("desc_ok", False)
            and data.get("visibility_ok", False)
            and data.get("playlist_ok", False)
            and data.get("quality_ok", True)
        )

        if all_ok:
            conformes += 1
        else:
            non_conformes += 1
            issues = data.get("issues", [])

            is_error = any("EXCEPTION" in i or "ERRO" in i for i in issues)
            if is_error:
                errors += 1

            if not data.get("title_ok", True):
                title_issues += 1
            if not data.get("desc_ok", True):
                desc_issues += 1
            if not data.get("visibility_ok", True):
                visibility_issues += 1
            if not data.get("playlist_ok", True):
                playlist_issues += 1
            if not data.get("quality_ok", True):
                quality_issues += 1
            if data.get("is_short", False):
                short_videos += 1

            problem_videos.append({
                "video_id": vid,
                "client": data.get("client", "?"),
                "issues": issues,
                "actual_title": data.get("actual_title"),
                "actual_visibility": data.get("actual_visibility"),
                "actual_playlists": data.get("actual_playlists", []),
                "expected_playlist": data.get("expected_playlist"),
                "resolution": data.get("resolution", "unknown"),
                "is_short": data.get("is_short", False),
            })

    # Build report object
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_videos_in_results": len(all_videos),
            "total_audited": total_audited,
            "conformes": conformes,
            "non_conformes": non_conformes,
            "errors": errors,
        },
        "issues_by_type": {
            "titulo_com_acentos_quebrados": title_issues,
            "descricao_com_acentos_quebrados": desc_issues,
            "visibilidade_incorreta": visibility_issues,
            "playlist_incorreta_ou_ausente": playlist_issues,
            "qualidade_ou_short": quality_issues,
            "classificado_como_short": short_videos,
        },
        "problem_videos": problem_videos,
        "channel_playlists": progress.get("channel_playlists", {}),
        "clients_summary": {},
    }

    # Per-client summary
    for client in results.keys():
        client_vids = [
            vid for vid, d in audited.items()
            if d.get("client") == client
        ]
        client_ok = sum(
            1 for vid in client_vids
            if audited[vid].get("title_ok", False)
            and audited[vid].get("desc_ok", False)
            and audited[vid].get("visibility_ok", False)
            and audited[vid].get("playlist_ok", False)
            and audited[vid].get("quality_ok", True)
        )
        client_problems = len(client_vids) - client_ok
        report["clients_summary"][client] = {
            "total": len(client_vids),
            "ok": client_ok,
            "problems": client_problems,
        }

    # Save report
    save_report(report)
    print(f"\n  Relatorio salvo em: {AUDIT_REPORT_FILE}")

    # Print summary
    print()
    print("=" * 60)
    print("  AUDIT REPORT")
    print("=" * 60)
    print(f"  Total auditados: {total_audited}")
    print(f"  Conformes: {conformes}")
    print(f"  Com problemas: {non_conformes}")
    if errors:
        print(f"  Erros (nao conseguiu auditar): {errors}")
    print()
    print("  Por tipo de problema:")
    print(f"    Titulo com acentos: {title_issues}")
    print(f"    Descricao com acentos: {desc_issues}")
    print(f"    Visibilidade incorreta: {visibility_issues}")
    print(f"    Playlist incorreta/ausente: {playlist_issues}")
    print(f"    Qualidade/Short: {quality_issues}")
    if short_videos:
        print(f"    Classificados como Short: {short_videos}")
    print()
    # Playlist duplicates summary
    ch_pl = progress.get("channel_playlists", {})
    dupes = ch_pl.get("duplicates", {})
    empty = ch_pl.get("empty_count", 0)
    if dupes or empty:
        print("  Problemas de playlists no canal:")
        for name, count in dupes.items():
            print(f"    '{name}' - {count} copias DUPLICADAS")
        if empty:
            print(f"    {empty} playlists VAZIAS")
        print()

    print("  Por cliente:")
    for client, data in report["clients_summary"].items():
        status = "OK" if data["problems"] == 0 else f"{data['problems']} problemas"
        print(f"    {client}: {data['total']} videos - {status}")
    print("=" * 60)

    # Print detailed problems
    if problem_videos:
        print()
        print("-" * 60)
        print("  DETALHES DOS PROBLEMAS")
        print("-" * 60)
        for pv in problem_videos:
            print(f"\n  Video: {pv['video_id']} ({pv['client']})")
            if pv.get("actual_title"):
                print(f"    Titulo atual: {pv['actual_title'][:80]}")
            if pv.get("actual_visibility"):
                print(f"    Visibilidade: {pv['actual_visibility']}")
            if pv.get("actual_playlists"):
                print(f"    Playlists: {pv['actual_playlists']}")
            for issue in pv["issues"]:
                print(f"    -> {issue}")
        print()
        print("-" * 60)


if __name__ == "__main__":
    main()
