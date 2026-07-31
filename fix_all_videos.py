"""
=============================================================
FIX ALL VIDEOS - Corrige TODOS os problemas do audit
=============================================================
Processa cada video UMA vez, aplicando todas as correcoes
necessarias na mesma visita a pagina:
  - Correcao de titulo (acentos quebrados)
  - Correcao de descricao (acentos quebrados)
  - Adicao a playlist (cria se nao existir)
  - Verificacao de visibilidade (Projetos IA)

Dados: audit_report.json
Progresso: fix_all_progress.json (atomico)

USO: python fix_all_videos.py
=============================================================
"""

import json
import os
import sys
import time
import subprocess
import html
import unicodedata
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# =============================================================
# CONFIG
# =============================================================

AUDIT_REPORT = "audit_report.json"
PROGRESS_FILE = "fix_all_progress.json"
CHROME_DEBUG_PORT = 9555

# =============================================================
# ACCENT FIXES (from youtube_compilation_uploader.py)
# =============================================================

ACCENT_FIXES = {
    # Client names
    "Atacad o": "Atacadao",
    "Faculdade Est cio": "Faculdade Estacio",
    "For\ufffda da Terra": "Forca da Terra",
    "Philco Brit nia": "Philco Britania",
    "Nestl /": "Nestle /",
    # Talento/title name fragments
    "Jo o Mendes": "Joao Mendes",
    "Jo o Victor": "Joao Victor",
    "Joa\u0303o": "Joao",
    "D bora Melo": "Debora Melo",
    "D bora Mel": "Debora Mel",
    "Andr Lemos": "Andre Lemos",
    "Maria Lu za": "Maria Luiza",
    "Lu za Kropotoff": "Luiza Kropotoff",
    "Qu ren Hapuque": "Queren Hapuque",
    "Let cia Pedro": "Leticia Pedro",
    "Vit ria Rodrigues": "Vitoria Rodrigues",
    "J lia Horta": "Julia Horta",
    "Val rio": "Valerio",
    "Cabe\ufffda": "Cabeca",
    "Pablo Sant Anna": "Pablo Sant'Anna",
    "Isadora cecatto": "Isadora Cecatto",
    "Est cio": "Estacio",
    "Brit nia": "Britania",
    # HTML entities
    "Joa&#771;o": "Joao",
}

# Now fix the ACCENT_FIXES to use proper Unicode accented chars
ACCENT_FIXES = {
    # Client names
    "Atacad o": "Atacad\u00e3o",
    "Faculdade Est cio": "Faculdade Est\u00e1cio",
    "For\ufffda da Terra": "For\u00e7a da Terra",
    "Philco Brit nia": "Philco Brit\u00e2nia",
    "Nestl /": "Nestl\u00e9 /",
    # Talento/title name fragments
    "Jo o Mendes": "Jo\u00e3o Mendes",
    "Jo o Victor": "Jo\u00e3o Victor",
    "Joa\u0303o": "Jo\u00e3o",
    "D bora Melo": "D\u00e9bora Melo",
    "D bora Mel": "D\u00e9bora Mel",
    "Andr Lemos": "Andr\u00e9 Lemos",
    "Maria Lu za": "Maria Lu\u00edza",
    "Lu za Kropotoff": "Lu\u00edza Kropotoff",
    "Qu ren Hapuque": "Qu\u00e9ren Hapuque",
    "Let cia Pedro": "Let\u00edcia Pedro",
    "Vit ria Rodrigues": "Vit\u00f3ria Rodrigues",
    "J lia Horta": "J\u00falia Horta",
    "Val rio": "Val\u00e9rio",
    "For\ufffda da Terra": "For\u00e7a da Terra",
    "Cabe\ufffda": "Cabe\u00e7a",
    "Pablo Sant Anna": "Pablo Sant\u2019Anna",
    "Isadora cecatto": "Isadora Cecatto",
    "Est cio": "Est\u00e1cio",
    "Brit nia": "Brit\u00e2nia",
    # HTML entities
    "Joa&#771;o": "Jo\u00e3o",
}


def fix_accents(text):
    """Fix broken accents and HTML entities in text."""
    text = html.unescape(text)
    text = unicodedata.normalize('NFC', text)
    for broken, fixed in ACCENT_FIXES.items():
        if broken in text:
            text = text.replace(broken, fixed)
    return text


# =============================================================
# CHROME / SELENIUM
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
                print(f"  [RETRY] Tentativa {attempt + 1}/5...")
                time.sleep(5)
            else:
                raise e

    return driver


# =============================================================
# PROGRESS (atomic write)
# =============================================================

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "fixed": [],
        "created_playlists": [],
        "stats": {
            "titles_fixed": 0,
            "descriptions_fixed": 0,
            "playlists_added": 0,
            "playlists_created": 0,
            "visibility_fixed": 0,
            "errors": 0,
        }
    }


def save_progress(progress):
    """Atomic save: write to temp file then replace."""
    dir_name = os.path.dirname(os.path.abspath(PROGRESS_FILE))
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
        # On Windows, need to remove target first
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
        os.rename(tmp_path, PROGRESS_FILE)
    except Exception:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        # Fallback: direct write
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)


# =============================================================
# YOUTUBE STUDIO: PAGE NAVIGATION & WAIT
# =============================================================

def navigate_to_video(driver, video_id):
    """Navigate to video edit page and wait for editor to load."""
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(5)

    for _ in range(15):
        ready = driver.execute_script("""
            var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
            return tb && tb.textContent.trim().length > 0;
        """)
        if ready:
            return True
        time.sleep(2)

    # Fallback: check if metadata editor exists at all
    fallback = driver.execute_script("""
        return document.querySelector('ytcp-video-metadata-editor') !== null
            || document.querySelector('#details') !== null;
    """)
    return fallback


# =============================================================
# YOUTUBE STUDIO: TITLE FIX
# =============================================================

def fix_title(driver, new_title):
    """Fix the title field. Returns True if changed."""
    current_title = driver.execute_script("""
        var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        return tb ? tb.textContent.trim() : '';
    """)

    if not current_title:
        print("    [TITLE] Campo titulo nao encontrado")
        return False

    fixed_title = fix_accents(current_title)
    if fixed_title == current_title:
        return False

    print(f"    [TITLE] Corrigindo: '{current_title[:50]}...'")
    print(f"    [TITLE]      para: '{fixed_title[:50]}...'")

    # Focus, select all, delete, type new
    driver.execute_script("""
        var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        if (tb) { tb.focus(); tb.click(); }
    """)
    time.sleep(0.5)

    try:
        active = driver.switch_to.active_element
        active.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.3)
        active.send_keys(Keys.DELETE)
        time.sleep(0.3)
    except Exception:
        driver.execute_script("""
            var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
            if (tb) {
                tb.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
            }
        """)
        time.sleep(0.5)

    try:
        active = driver.switch_to.active_element
        active.send_keys(fixed_title)
    except Exception:
        driver.execute_script("""
            var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
            if (tb) {
                tb.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, arguments[0]);
            }
        """, fixed_title)
    time.sleep(1)

    # Verify
    typed = driver.execute_script("""
        var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        return tb ? tb.textContent.trim() : '';
    """)

    if typed:
        print(f"    [TITLE] OK - corrigido")
        return True
    else:
        print(f"    [TITLE] FALHA ao digitar")
        return False


# =============================================================
# YOUTUBE STUDIO: DESCRIPTION FIX
# =============================================================

def fix_description(driver):
    """Fix description field if it has broken accents. Returns True if changed."""

    # Expand "Mostrar mais" if needed
    driver.execute_script("""
        var btns = document.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt.includes('mostrar mais') || txt.includes('show more')) {
                b.click(); break;
            }
        }
    """)
    time.sleep(1)

    current_desc = driver.execute_script("""
        var tb = document.querySelector('#description-textarea #textbox, #description-container #textbox');
        if (tb) return tb.textContent.trim();
        var boxes = document.querySelectorAll('ytcp-social-suggestions-textbox #textbox');
        return boxes.length > 0 ? boxes[boxes.length - 1].textContent.trim() : '';
    """)

    if not current_desc:
        return False

    fixed_desc = fix_accents(current_desc)
    if fixed_desc == current_desc:
        return False

    print(f"    [DESC] Corrigindo descricao com acentos quebrados...")

    selector = '#description-textarea #textbox'

    # Focus, select all, delete, type
    driver.execute_script(f"""
        var tb = document.querySelector('{selector}');
        if (tb) {{ tb.focus(); tb.click(); }}
    """)
    time.sleep(0.5)

    try:
        active = driver.switch_to.active_element
        active.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.3)
        active.send_keys(Keys.DELETE)
        time.sleep(0.3)
    except Exception:
        driver.execute_script(f"""
            var tb = document.querySelector('{selector}');
            if (tb) {{
                tb.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
            }}
        """)
        time.sleep(0.5)

    try:
        active = driver.switch_to.active_element
        active.send_keys(fixed_desc)
    except Exception:
        driver.execute_script(f"""
            var tb = document.querySelector('{selector}');
            if (tb) {{
                tb.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, arguments[0]);
            }}
        """, fixed_desc)
    time.sleep(1)

    # Verify
    typed = driver.execute_script(f"""
        var tb = document.querySelector('{selector}');
        return tb ? tb.textContent.trim() : '';
    """)

    if typed:
        print(f"    [DESC] OK - corrigido")
        return True
    else:
        # Fallback selector
        selector2 = '#description-container #textbox'
        driver.execute_script(f"""
            var tb = document.querySelector('{selector2}');
            if (tb) {{ tb.focus(); tb.click(); }}
        """)
        time.sleep(0.5)
        try:
            active = driver.switch_to.active_element
            active.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.3)
            active.send_keys(Keys.DELETE)
            time.sleep(0.3)
            active.send_keys(fixed_desc)
        except Exception:
            pass
        time.sleep(1)
        typed2 = driver.execute_script(f"""
            var tb = document.querySelector('{selector2}');
            return tb ? tb.textContent.trim() : '';
        """)
        if typed2:
            print(f"    [DESC] OK - corrigido (fallback)")
            return True
        print(f"    [DESC] FALHA ao digitar descricao")
        return False


# =============================================================
# YOUTUBE STUDIO: PLAYLIST (from fix_playlists_final.py)
# =============================================================

def open_playlist_dialog(driver):
    """Open the playlist dialog on a video edit page."""
    opened = driver.execute_script("""
        var trigger = document.querySelector(
            'ytcp-dropdown-trigger[aria-label*="playlist" i]'
        );
        if (trigger && trigger.offsetParent !== null) {
            trigger.click();
            return 'clicked_aria';
        }
        var vmp = document.querySelector('ytcp-video-metadata-playlists');
        if (vmp) {
            var inner = vmp.querySelector('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, button');
            if (inner) { inner.click(); return 'clicked_vmp'; }
            vmp.click();
            return 'clicked_vmp_direct';
        }
        return 'not_found';
    """)
    if 'not_found' in str(opened):
        return False

    for _ in range(8):
        ready = driver.execute_script("""
            var dialog = document.querySelector('ytcp-playlist-dialog');
            return dialog && dialog.innerHTML.length > 100;
        """)
        if ready:
            return True
        time.sleep(1)

    return False


def scroll_playlist_list(driver):
    """Scroll the playlist list to load all items."""
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var list = dialog.querySelector('tp-yt-iron-list');
        if (list) {
            for (var s = 0; s <= list.scrollHeight; s += 32) {
                list.scrollTop = s;
            }
            list.scrollTop = 0;
        }
    """)
    time.sleep(1)


def find_playlist_in_dialog(driver, playlist_name):
    """Check if playlist exists in the dialog and check it. Returns status string."""
    return driver.execute_script("""
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
                if (label) { label.click(); return 'checked'; }
                group.click();
                return 'checked_group';
            }
        }

        // Fallback: search all labels
        var labels = dialog.querySelectorAll('label');
        for (var label of labels) {
            var txt = (label.textContent || '').trim();
            if (txt.includes(targetName)) {
                label.click();
                return 'checked_fallback';
            }
        }

        return 'not_found';
    """, playlist_name)


def create_playlist_in_dialog(driver, playlist_name):
    """
    Create a new playlist from within the video editor playlist dialog.
    Fixed: removed height checks on ytcp-playlist-creation-dialog container
    (it reports height=0 but inputs inside are visible).
    """

    # Step 1: Click "Nova playlist" button
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return;
        var npBtn = dialog.querySelector('.new-playlist-button button');
        if (npBtn) { npBtn.click(); return; }
        var btns = dialog.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').toLowerCase().trim();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                b.click(); return;
            }
        }
    """)
    time.sleep(2)

    # Step 2: Click menu item "Nova playlist"
    clicked_item = driver.execute_script("""
        var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
        if (item) { item.click(); return 'clicked'; }
        var items = document.querySelectorAll('tp-yt-paper-item, [role="menuitem"], [role="option"]');
        for (var i of items) {
            var txt = (i.textContent || '').toLowerCase().trim();
            if (txt.includes('nova playlist') || txt.includes('new playlist')) {
                i.click(); return 'clicked_fallback';
            }
        }
        return 'not_found';
    """)

    if clicked_item not in ('clicked', 'clicked_fallback'):
        return 'no_menu_item'

    time.sleep(5)

    # Step 3: Find and fill the title textbox
    # KEY FIX: Don't check container height. ytcp-playlist-creation-dialog
    # has height=0 but its internal inputs are visible (height=30).
    focused = 'not_found'
    for retry in range(15):
        focused = driver.execute_script("""
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            if (cd) {
                var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
                for (var tb of boxes) {
                    if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                        tb.focus();
                        tb.click();
                        tb.textContent = '';
                        return 'focused_creation';
                    }
                }
                var allInputs = cd.querySelectorAll('#textbox, [contenteditable="true"], input, textarea');
                for (var inp of allInputs) {
                    var ph = inp.placeholder || inp.getAttribute('aria-label') || '';
                    if (ph.toLowerCase().includes('título') || ph.toLowerCase().includes('titulo') || ph.toLowerCase().includes('title') || ph.toLowerCase().includes('adicione um título')) {
                        inp.focus();
                        inp.click();
                        if (inp.contentEditable === 'true') inp.textContent = '';
                        return 'focused_placeholder';
                    }
                }
                for (var tb of boxes) {
                    if (tb.offsetHeight > 0) {
                        tb.focus();
                        tb.click();
                        tb.textContent = '';
                        return 'focused_any';
                    }
                }
            }

            var dialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog');
            for (var d of dialogs) {
                var txt = (d.textContent || '').toLowerCase();
                if (txt.includes('criar uma nova playlist') || txt.includes('create a new playlist')) {
                    var tb = d.querySelector('#textbox[contenteditable], div[contenteditable="true"]');
                    if (tb && tb.offsetHeight > 0) {
                        tb.focus();
                        tb.click();
                        tb.textContent = '';
                        return 'focused_fallback';
                    }
                }
            }

            return 'not_found';
        """)
        if 'focused' in str(focused):
            break
        time.sleep(1)

    if 'focused' not in str(focused):
        return 'no_textbox'

    # Step 4: Type the playlist name
    time.sleep(0.5)

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
    """, playlist_name)
    time.sleep(1)

    # Verify + send_keys backup
    typed_text = driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return '';
        var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
        for (var tb of boxes) {
            if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                return tb.textContent.trim();
            }
        }
        return '';
    """)

    if not typed_text:
        try:
            active = driver.switch_to.active_element
            active.send_keys(playlist_name)
            time.sleep(1)
        except Exception:
            pass

    # Final verify
    typed_text = driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return '';
        var boxes = cd.querySelectorAll('#textbox[contenteditable], div[contenteditable="true"]');
        for (var tb of boxes) {
            if (tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                return tb.textContent.trim();
            }
        }
        return '';
    """)
    print(f"    [TYPED] '{typed_text}'")

    if not typed_text:
        return 'no_text_entered'

    time.sleep(1)

    # Step 5: Set visibility to "Nao listada"
    driver.execute_script("""
        var cd = document.querySelector('ytcp-playlist-creation-dialog');
        if (!cd) return;
        var dds = cd.querySelectorAll('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger');
        for (var dd of dds) {
            var txt = (dd.textContent || '').toLowerCase();
            if (txt.includes('visibilidade') || txt.includes('visibility') ||
                txt.includes('publica') || txt.includes('public') ||
                txt.includes('privad') || txt.includes('private')) {
                dd.click();
                return;
            }
        }
    """)
    time.sleep(2)

    driver.execute_script("""
        var items = document.querySelectorAll('tp-yt-paper-item, [role="option"], [role="menuitem"]');
        for (var item of items) {
            var txt = (item.textContent || '').toLowerCase();
            if (txt.includes('nao listada') || txt.includes('unlisted')) {
                item.click();
                return;
            }
        }
    """)
    time.sleep(2)

    # Step 6: Click "Criar"
    for retry in range(5):
        created = driver.execute_script("""
            var cd = document.querySelector('ytcp-playlist-creation-dialog');
            var containers = [];
            if (cd) containers.push(cd);
            var dialogs = document.querySelectorAll('tp-yt-paper-dialog, ytcp-dialog');
            for (var d of dialogs) { if (d.innerHTML.length > 100) containers.push(d); }

            for (var d of containers) {
                var btns = d.querySelectorAll('#create-button, ytcp-button, button');
                for (var b of btns) {
                    var txt = (b.textContent || '').trim().toLowerCase();
                    if (txt === 'criar' || txt === 'create') {
                        var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                        if (!disabled) { b.click(); return 'created'; }
                        return 'disabled';
                    }
                }
            }
            return 'no_button';
        """)

        if created == 'created':
            time.sleep(3)
            return 'created'

        if created == 'disabled':
            driver.execute_script("""
                var cd = document.querySelector('ytcp-playlist-creation-dialog');
                if (!cd) return;
                var tb = cd.querySelector('#textbox[contenteditable]');
                if (tb && tb.offsetHeight > 5 && tb.offsetHeight < 60) {
                    tb.focus();
                    tb.dispatchEvent(new Event('input', {bubbles: true}));
                    tb.dispatchEvent(new Event('change', {bubbles: true}));
                    tb.dispatchEvent(new InputEvent('input', {
                        bubbles: true, data: tb.textContent, inputType: 'insertText'
                    }));
                }
            """)
            time.sleep(2)
        else:
            break

    return f'create_failed:{created}'


def close_playlist_dialog(driver):
    """Close the playlist dialog by clicking Concluir/Done."""
    driver.execute_script("""
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (dialog) {
            var els = dialog.querySelectorAll('ytcp-button, button');
            for (var el of els) {
                var txt = (el.textContent || '').trim().toLowerCase();
                if (txt === 'concluir' || txt === 'done') {
                    el.click(); return;
                }
            }
        }
        var allBtns = document.querySelectorAll('ytcp-button, button');
        for (var b of allBtns) {
            if (b.offsetParent === null) continue;
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt === 'concluir' || txt === 'done') {
                b.click(); return;
            }
        }
    """)
    time.sleep(2)


def add_to_playlist(driver, playlist_name, created_playlists):
    """
    Add the current video to a playlist. Creates playlist if needed.
    Returns (status_string, was_created_bool).
    """

    if not open_playlist_dialog(driver):
        return 'no_playlist_selector', False

    time.sleep(1)
    scroll_playlist_list(driver)

    select_result = find_playlist_in_dialog(driver, playlist_name)

    if select_result == 'already_checked':
        close_playlist_dialog(driver)
        return 'already_in_playlist', False

    if 'checked' in str(select_result):
        time.sleep(1)
        close_playlist_dialog(driver)
        return 'added_existing', False

    # Playlist not found - create it (with retry on failure)
    if select_result == 'not_found':
        create_result = create_playlist_in_dialog(driver, playlist_name)
        if create_result == 'created':
            time.sleep(2)
            close_playlist_dialog(driver)
            return 'created_and_added', True

        # First attempt failed - close everything, reload page, and retry
        print(f"    [PLAYLIST] Tentativa 1 falhou ({create_result}), recarregando pagina...")
        close_playlist_dialog(driver)
        time.sleep(2)

        # Dismiss any leftover dialogs by pressing Escape multiple times
        try:
            for _ in range(3):
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                time.sleep(0.5)
        except Exception:
            pass

        # Reload the page fresh
        current_url = driver.current_url
        driver.get(current_url)
        time.sleep(5)

        # Wait for editor to load again
        for _ in range(10):
            ready = driver.execute_script("""
                return document.querySelector('ytcp-video-metadata-editor') !== null
                    || document.querySelector('#details') !== null;
            """)
            if ready:
                break
            time.sleep(1)

        # Retry: open playlist dialog and try creating again
        if not open_playlist_dialog(driver):
            return f'create_failed_retry:no_dialog', False

        time.sleep(1)
        scroll_playlist_list(driver)

        # Check if playlist was actually created by first attempt
        recheck = find_playlist_in_dialog(driver, playlist_name)
        if 'checked' in str(recheck) or recheck == 'already_checked':
            close_playlist_dialog(driver)
            return 'added_existing_after_retry', False

        # Still not found - retry creation
        create_result2 = create_playlist_in_dialog(driver, playlist_name)
        if create_result2 == 'created':
            time.sleep(2)
            close_playlist_dialog(driver)
            return 'created_and_added_retry', True
        else:
            close_playlist_dialog(driver)
            return f'create_failed:{create_result2}', False

    close_playlist_dialog(driver)
    return f'unexpected:{select_result}', False


# =============================================================
# YOUTUBE STUDIO: VISIBILITY CHECK (for Projetos IA)
# =============================================================

def check_and_fix_visibility(driver):
    """
    Check if the video visibility is unlisted. If not detected or wrong,
    try to set it to unlisted via the visibility settings.
    Returns True if visibility was changed.
    """
    # Read current visibility from the page
    visibility = driver.execute_script("""
        // Try to find visibility indicator on the edit page
        var vis = document.querySelector('ytcp-video-visibility-select');
        if (vis) {
            var txt = vis.textContent.toLowerCase().trim();
            if (txt.includes('unlisted') || txt.includes('nao listado') || txt.includes('nao listada')) return 'unlisted';
            if (txt.includes('public')) return 'public';
            if (txt.includes('private') || txt.includes('privado')) return 'private';
            return txt.substring(0, 30);
        }
        // Check radio buttons
        var radios = document.querySelectorAll('tp-yt-paper-radio-button');
        for (var r of radios) {
            if (r.getAttribute('aria-checked') === 'true') {
                var txt = r.textContent.toLowerCase().trim();
                if (txt.includes('unlisted') || txt.includes('nao listado')) return 'unlisted';
                if (txt.includes('public')) return 'public';
                if (txt.includes('private') || txt.includes('privado')) return 'private';
                return txt.substring(0, 30);
            }
        }
        return 'unknown';
    """)

    if visibility == 'unlisted':
        return False  # Already correct

    print(f"    [VISIBILITY] Status atual: {visibility} - tentando corrigir para unlisted...")

    # Navigate to the visibility section
    # Click on the visibility section/tab
    driver.execute_script("""
        // Try clicking visibility radio on edit page (basic details has visibility sometimes)
        var vis = document.querySelector('ytcp-video-visibility-select');
        if (vis) { vis.click(); return; }
        // Otherwise look for the Visibility button/section
        var btns = document.querySelectorAll('button, ytcp-button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt.includes('visibilidade') || txt.includes('visibility')) {
                b.click(); return;
            }
        }
    """)
    time.sleep(2)

    # Select "Nao listado" / "Unlisted"
    selected = driver.execute_script("""
        var radios = document.querySelectorAll('tp-yt-paper-radio-button, [role="radio"]');
        for (var r of radios) {
            var txt = (r.textContent || '').toLowerCase().trim();
            if (txt.includes('nao listado') || txt.includes('nao listada') || txt.includes('unlisted')) {
                r.click();
                return 'selected';
            }
        }
        return 'not_found';
    """)

    if selected == 'selected':
        time.sleep(1)
        print(f"    [VISIBILITY] Selecionado 'Nao listado'")
        return True

    print(f"    [VISIBILITY] Nao conseguiu selecionar visibilidade")
    return False


# =============================================================
# YOUTUBE STUDIO: SAVE
# =============================================================

def save_video(driver):
    """Click Save button and handle disabled state."""
    time.sleep(2)

    save_result = driver.execute_script("""
        var saveBtn = document.querySelector('#save-button');
        if (saveBtn) {
            var btn = saveBtn.querySelector('button') || saveBtn;
            var disabled = btn.hasAttribute('disabled') || btn.getAttribute('aria-disabled') === 'true';
            if (!disabled) { btn.click(); return 'saved'; }
            return 'save_disabled';
        }
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            if ((txt === 'salvar' || txt === 'save') && b.offsetParent !== null) {
                var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                if (!disabled) { b.click(); return 'saved_fallback'; }
                return 'save_disabled_fallback';
            }
        }
        return 'no_save_btn';
    """)

    if 'disabled' in save_result:
        # Force input event to enable save
        driver.execute_script("""
            var fields = document.querySelectorAll('#title-textarea #textbox, #description-textarea #textbox');
            for (var f of fields) {
                f.dispatchEvent(new Event('input', {bubbles: true}));
                f.dispatchEvent(new Event('change', {bubbles: true}));
            }
        """)
        time.sleep(2)
        save_result = driver.execute_script("""
            var saveBtn = document.querySelector('#save-button');
            if (saveBtn) {
                var btn = saveBtn.querySelector('button') || saveBtn;
                var disabled = btn.hasAttribute('disabled') || btn.getAttribute('aria-disabled') === 'true';
                if (!disabled) { btn.click(); return 'saved_retry'; }
            }
            return 'still_disabled';
        """)

    time.sleep(3)
    return save_result


# =============================================================
# AUDIT DATA PROCESSING
# =============================================================

def load_audit_data():
    """Load audit_report.json and build work list grouped by client."""
    with open(AUDIT_REPORT, 'r', encoding='utf-8') as f:
        audit = json.load(f)

    videos = audit.get("problem_videos", [])

    # Group by client, preserving order
    by_client = {}
    for v in videos:
        vid = v.get("video_id", "")
        client = v.get("client", "unknown")
        issues = v.get("issues", [])

        # SKIP invalid IDs
        if vid == "UPLOADED_NO_ID" or not vid:
            continue

        # SKIP page errors (no actual_title = page didn't load during audit)
        if any("ERRO:" in i for i in issues):
            continue

        # Determine what needs fixing
        needs_title_fix = any("titulo com acento quebrado" in i for i in issues)
        needs_desc_fix = any("descricao com acento quebrado" in i for i in issues)
        needs_playlist = any("playlist" in i.lower() for i in issues)
        needs_visibility = any("visibilidade nao detectada" in i for i in issues)

        entry = {
            "video_id": vid,
            "client": client,
            "issues": issues,
            "actual_title": v.get("actual_title", ""),
            "expected_playlist": v.get("expected_playlist", ""),
            "actual_visibility": v.get("actual_visibility", ""),
            "needs_title_fix": needs_title_fix,
            "needs_desc_fix": needs_desc_fix,
            "needs_playlist": needs_playlist,
            "needs_visibility": needs_visibility,
        }

        by_client.setdefault(client, []).append(entry)

    return by_client


# =============================================================
# MAIN PROCESSING
# =============================================================

def process_video(driver, video, playlist_name, created_playlists, progress):
    """
    Process a single video: navigate, fix title, fix description,
    add to playlist, fix visibility, save.
    Returns dict of what was done.
    """
    vid = video["video_id"]
    result = {
        "title_fixed": False,
        "desc_fixed": False,
        "playlist_added": False,
        "playlist_created": False,
        "visibility_fixed": False,
        "saved": False,
        "error": None,
    }

    # 1. Navigate to video editor
    if not navigate_to_video(driver, vid):
        result["error"] = "page_not_loaded"
        return result

    any_change = False

    # 2. Fix title if needed
    if video["needs_title_fix"]:
        title_changed = fix_title(driver, video["actual_title"])
        if title_changed:
            result["title_fixed"] = True
            any_change = True

    # 3. Fix description if needed
    if video["needs_desc_fix"]:
        desc_changed = fix_description(driver)
        if desc_changed:
            result["desc_fixed"] = True
            any_change = True

    # 4. Add to playlist
    if video["needs_playlist"]:
        playlist_status, was_created = add_to_playlist(driver, playlist_name, created_playlists)
        print(f"    [PLAYLIST] {playlist_status}")

        if playlist_status in ('added_existing', 'created_and_added', 'already_in_playlist'):
            result["playlist_added"] = True
            if was_created:
                result["playlist_created"] = True
            if playlist_status != 'already_in_playlist':
                any_change = True
        else:
            result["error"] = f"playlist_fail:{playlist_status}"

    # 5. Fix visibility if needed (Projetos IA)
    if video["needs_visibility"]:
        vis_changed = check_and_fix_visibility(driver)
        if vis_changed:
            result["visibility_fixed"] = True
            any_change = True

    # 6. Save if any change was made
    if any_change:
        save_result = save_video(driver)
        print(f"    [SAVE] {save_result}")
        if 'saved' in save_result:
            result["saved"] = True
        elif save_result == 'still_disabled':
            # No actual changes detected by YouTube
            result["saved"] = True  # Consider it OK
        else:
            result["error"] = f"save_fail:{save_result}"
    else:
        # No changes needed or playlist was already set
        result["saved"] = True

    return result


def main():
    print("=" * 60)
    print("  FIX ALL VIDEOS - Corrigir todos os problemas do audit")
    print("=" * 60)
    print()

    # 1. Load audit data
    by_client = load_audit_data()
    total_videos = sum(len(vids) for vids in by_client.values())

    # 2. Load progress
    progress = load_progress()
    fixed_ids = set(progress.get("fixed", []))
    created_playlists = set(progress.get("created_playlists", []))

    # 3. Count pending work
    pending_by_client = {}
    for client, videos in by_client.items():
        pending = [v for v in videos if v["video_id"] not in fixed_ids]
        if pending:
            pending_by_client[client] = pending

    total_pending = sum(len(v) for v in pending_by_client.values())

    print(f"  Total videos no audit: {total_videos}")
    print(f"  Ja corrigidos: {len(fixed_ids)}")
    print(f"  Pendentes: {total_pending}")
    print(f"  Clientes pendentes: {len(pending_by_client)}")
    print()

    if total_pending == 0:
        print("[OK] Todos os videos ja foram corrigidos!")
        return

    # Show work summary
    for client, videos in pending_by_client.items():
        needs_title = sum(1 for v in videos if v["needs_title_fix"])
        needs_desc = sum(1 for v in videos if v["needs_desc_fix"])
        needs_vis = sum(1 for v in videos if v["needs_visibility"])
        playlist_name = f"Portfolio - {client}"
        already_created = playlist_name in created_playlists
        print(f"  {client}: {len(videos)} videos -> '{playlist_name}'"
              f"{'  [playlist ja criada]' if already_created else ''}")
        if needs_title > 0:
            print(f"    - {needs_title} titulos para corrigir")
        if needs_desc > 0:
            print(f"    - {needs_desc} descricoes para corrigir")
        if needs_vis > 0:
            print(f"    - {needs_vis} visibilidades para verificar")

    print()
    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print()
    print("[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    # 4. Open browser
    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

    print("[BROWSER] Verificando YouTube Studio...")
    driver.get("https://studio.youtube.com")
    time.sleep(5)

    channel = driver.execute_script("""
        var el = document.querySelector('ytcp-entity-name, .entity-name, #entity-name');
        return el ? el.textContent.trim() : 'desconhecido';
    """)
    print(f"[CANAL] {channel}")
    print()

    # 5. Process each client, then each video
    count = 0
    stats = progress.get("stats", {
        "titles_fixed": 0,
        "descriptions_fixed": 0,
        "playlists_added": 0,
        "playlists_created": 0,
        "visibility_fixed": 0,
        "errors": 0,
    })

    for client, videos in pending_by_client.items():
        playlist_name = f"Portfolio - {client}"
        print()
        print("-" * 60)
        print(f"  CLIENTE: {client} ({len(videos)} videos)")
        print(f"  PLAYLIST: {playlist_name}")
        print("-" * 60)

        for video in videos:
            count += 1
            vid = video["video_id"]
            title_preview = (video.get("actual_title") or vid)[:55]

            # Build action summary
            actions = []
            if video["needs_title_fix"]:
                actions.append("titulo")
            if video["needs_desc_fix"]:
                actions.append("desc")
            if video["needs_playlist"]:
                actions.append("playlist")
            if video["needs_visibility"]:
                actions.append("visibilidade")

            print(f"\n[{count}/{total_pending}] {vid}")
            print(f"  Titulo: {title_preview}")
            print(f"  Acoes: {', '.join(actions)}")

            try:
                result = process_video(driver, video, playlist_name, created_playlists, progress)

                # Update stats
                if result["title_fixed"]:
                    stats["titles_fixed"] += 1
                if result["desc_fixed"]:
                    stats["descriptions_fixed"] += 1
                if result["playlist_added"]:
                    stats["playlists_added"] += 1
                if result["playlist_created"]:
                    stats["playlists_created"] += 1
                    created_playlists.add(playlist_name)
                if result["visibility_fixed"]:
                    stats["visibility_fixed"] += 1

                if result["error"]:
                    stats["errors"] += 1
                    print(f"  [AVISO] {result['error']}")

                # Mark as fixed if saved successfully
                if result["saved"]:
                    fixed_ids.add(vid)

                    # Build result summary
                    done = []
                    if result["title_fixed"]:
                        done.append("titulo")
                    if result["desc_fixed"]:
                        done.append("desc")
                    if result["playlist_added"]:
                        if result["playlist_created"]:
                            done.append("playlist CRIADA")
                        else:
                            done.append("playlist")
                    if result["visibility_fixed"]:
                        done.append("visibilidade")

                    if done:
                        print(f"  [OK] Corrigido: {', '.join(done)}")
                    else:
                        print(f"  [OK] Nenhuma correcao necessaria (ja estava ok)")
                else:
                    stats["errors"] += 1
                    print(f"  [FALHA] Nao salvou")

            except Exception as e:
                stats["errors"] += 1
                print(f"  [ERRO] {str(e)[:100]}")

            # Save progress after each video
            progress["fixed"] = list(fixed_ids)
            progress["created_playlists"] = list(created_playlists)
            progress["stats"] = stats
            save_progress(progress)

            time.sleep(3)

    # 6. Final summary
    print()
    print("=" * 60)
    print("  RESUMO FINAL")
    print("=" * 60)
    print(f"  Total processados: {count}")
    print(f"  Titulos corrigidos: {stats['titles_fixed']}")
    print(f"  Descricoes corrigidas: {stats['descriptions_fixed']}")
    print(f"  Playlists adicionadas: {stats['playlists_added']}")
    print(f"  Playlists criadas: {stats['playlists_created']}")
    print(f"  Visibilidade corrigida: {stats['visibility_fixed']}")
    print(f"  Erros: {stats['errors']}")
    print(f"  Total ja corrigidos: {len(fixed_ids)}")
    print("=" * 60)

    print("\nFechando navegador em 5 segundos...")
    time.sleep(5)
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
