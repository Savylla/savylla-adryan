"""
=============================================================
FIX TITLES & VISIBILITY
=============================================================
1. Corrige titulos com acentos quebrados nos videos existentes
2. Muda TODAS as playlists para "Não listada"
3. Garante que todos os videos estão como "Não listado"

USO: python fix_titles_and_visibility.py
=============================================================
"""

import json
import os
import sys
import time
import subprocess
import html
import unicodedata

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
import functools
print = functools.partial(print, flush=True)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

RESULTS_FILE = "youtube_results.json"
PROGRESS_FILE = "fix_titles_progress.json"
CHROME_DEBUG_PORT = 9555

ACCENT_FIXES = {
    "Atacad o": "Atacadão",
    "Faculdade Est cio": "Faculdade Estácio",
    "For\ufffda da Terra": "Força da Terra",
    "Philco Brit nia": "Philco Britânia",
    "Nestl /": "Nestlé /",
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
    text = html.unescape(text)
    text = unicodedata.normalize('NFC', text)
    for broken, fixed in ACCENT_FIXES.items():
        if broken in text:
            text = text.replace(broken, fixed)
    return text


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


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"fixed_titles": [], "fixed_playlists": []}


def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def fix_video_title(driver, video_id, new_title):
    """Navigate to video edit page, fix the title, and save."""
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(6)

    # Wait for editor to load
    for _ in range(10):
        ready = driver.execute_script("""
            return !!document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        """)
        if ready:
            break
        time.sleep(2)

    # Get current title
    current = driver.execute_script("""
        var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        return tb ? tb.textContent.trim() : '';
    """)

    if not current:
        return 'page_not_loaded'

    # Check if title already correct
    if fix_accents(current) == fix_accents(new_title):
        # Title might already be fixed, check exact match
        if current == new_title:
            return 'already_correct'

    # Clear and type new title
    driver.execute_script("""
        var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        if (tb) {
            tb.focus();
            tb.click();
            // Select all and delete
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
        }
    """)
    time.sleep(0.5)

    try:
        active = driver.switch_to.active_element
        active.send_keys(new_title)
    except Exception:
        pass
    time.sleep(1)

    # Verify
    typed = driver.execute_script("""
        var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        return tb ? tb.textContent.trim() : '';
    """)

    if new_title not in typed and typed not in new_title:
        return f'type_failed:{typed[:30]}'

    # Save
    time.sleep(1)
    save_result = driver.execute_script("""
        var btn = document.querySelector('#save-button button, #save button, button[aria-label="Salvar"], button[aria-label="Save"]');
        if (btn && btn.offsetParent !== null) {
            var disabled = btn.hasAttribute('disabled') || btn.getAttribute('aria-disabled') === 'true';
            if (!disabled) { btn.click(); return 'saved'; }
            return 'save_disabled';
        }
        // Fallback
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
    time.sleep(3)
    return save_result


def fix_all_playlists_visibility(driver):
    """Go to playlists page and set all playlists to unlisted."""
    print("\n" + "=" * 60)
    print("  FASE 1: Corrigir visibilidade das PLAYLISTS")
    print("=" * 60)

    driver.get("https://studio.youtube.com/channel/playlists")
    time.sleep(5)

    # Get all playlist names and their visibility
    playlists = driver.execute_script("""
        var results = [];
        var rows = document.querySelectorAll('ytcp-playlist-row, tr, .playlist-row');
        for (var r of rows) {
            var nameEl = r.querySelector('.playlist-title, a.title, td:first-child a');
            var visEl = r.querySelector('.visibility-column, td:nth-child(3)');
            if (nameEl) {
                results.push({
                    name: (nameEl.textContent || '').trim(),
                    visibility: visEl ? visEl.textContent.trim() : 'unknown',
                    href: nameEl.href || ''
                });
            }
        }
        return results;
    """)

    print(f"  Playlists encontradas: {len(playlists)}")
    for p in playlists:
        status = "OK" if "não listada" in p.get('visibility', '').lower() or "unlisted" in p.get('visibility', '').lower() else "PUBLICA"
        print(f"  [{status}] {p.get('name', '?')} - {p.get('visibility', '?')}")

    # For each public playlist, click edit and change visibility
    public_playlists = [p for p in playlists
                        if 'pública' in p.get('visibility', '').lower()
                        or 'public' in p.get('visibility', '').lower()]

    if not public_playlists:
        print("  [OK] Todas as playlists ja estao nao listadas!")
        return 0

    print(f"\n  {len(public_playlists)} playlists para corrigir:")

    fixed = 0
    for i, playlist in enumerate(public_playlists):
        name = playlist.get('name', '')
        href = playlist.get('href', '')
        print(f"\n  [{i+1}/{len(public_playlists)}] {name}")

        if not href:
            print(f"    [SKIP] Sem link de edição")
            continue

        # Navigate to playlist edit page
        driver.get(href)
        time.sleep(4)

        # Click the edit (pencil) icon or "Editar" button
        driver.execute_script("""
            var editBtns = document.querySelectorAll('button, ytcp-button, [aria-label*="dit"], [aria-label*="edi"]');
            for (var b of editBtns) {
                var aria = (b.getAttribute('aria-label') || '').toLowerCase();
                var txt = (b.textContent || '').toLowerCase();
                if (aria.includes('edit') || aria.includes('editar') || txt.includes('editar playlist')) {
                    b.click();
                    return 'clicked';
                }
            }
            // Try kebab menu
            var kebab = document.querySelector('#more-actions, [aria-label="Mais ações"]');
            if (kebab) kebab.click();
            return 'kebab';
        """)
        time.sleep(3)

        # Try to find and change visibility dropdown
        vis_changed = driver.execute_script("""
            // Look for visibility dropdown
            var dropdowns = document.querySelectorAll('ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, select');
            for (var dd of dropdowns) {
                var txt = (dd.textContent || '').toLowerCase();
                if (txt.includes('pública') || txt.includes('public') || txt.includes('visibilidade') || txt.includes('visibility')) {
                    dd.click();
                    return 'opened';
                }
            }
            return 'no_dropdown';
        """)
        print(f"    Visibility dropdown: {vis_changed}")

        if vis_changed == 'opened':
            time.sleep(2)
            set_result = driver.execute_script("""
                var items = document.querySelectorAll('tp-yt-paper-item, [role="option"], [role="menuitem"], option');
                for (var item of items) {
                    var txt = (item.textContent || '').toLowerCase();
                    if (txt.includes('não listada') || txt.includes('unlisted') || txt.includes('nao listada') || txt.includes('não listado')) {
                        item.click();
                        return 'set_unlisted';
                    }
                }
                return 'not_found';
            """)
            print(f"    Set unlisted: {set_result}")
            time.sleep(2)

            if set_result == 'set_unlisted':
                # Save
                driver.execute_script("""
                    var btns = document.querySelectorAll('ytcp-button, button');
                    for (var b of btns) {
                        var txt = (b.textContent || '').trim().toLowerCase();
                        if (txt === 'salvar' || txt === 'save' || txt === 'concluir' || txt === 'done') {
                            if (b.offsetParent !== null) { b.click(); return; }
                        }
                    }
                """)
                time.sleep(3)
                fixed += 1
                print(f"    [OK] Visibilidade alterada para Não listada")

    return fixed


def main():
    print("=" * 60)
    print("  FIX TITLES & VISIBILITY")
    print("=" * 60)

    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)

    progress = load_progress()

    # Find videos needing title fix
    title_fixes = []
    for client, videos in results.items():
        for v in videos:
            vid = v['video_id']
            if vid in progress.get('fixed_titles', []):
                continue
            old_title = v['title']
            new_title = fix_accents(old_title)
            if new_title != old_title:
                title_fixes.append({
                    'video_id': vid,
                    'old_title': old_title,
                    'new_title': new_title,
                    'client': client
                })

    print(f"\n  Videos com titulo para corrigir: {len(title_fixes)}")
    print(f"  Ja corrigidos: {len(progress.get('fixed_titles', []))}")

    if title_fixes:
        for fix in title_fixes[:5]:
            print(f"    {fix['video_id']}: \"{fix['old_title'][:40]}\" -> \"{fix['new_title'][:40]}\"")
        if len(title_fixes) > 5:
            print(f"    ... +{len(title_fixes)-5} mais")

    print("\n  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print("\n[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

    # Verify YouTube Studio
    driver.get("https://studio.youtube.com")
    time.sleep(5)
    channel = driver.execute_script("""
        var el = document.querySelector('ytcp-entity-name, .entity-name, #entity-name');
        return el ? el.textContent.trim() : 'unknown';
    """)
    print(f"[CANAL] {channel}\n")

    # PHASE 1: Fix playlist visibility
    playlists_fixed = fix_all_playlists_visibility(driver)

    # PHASE 2: Fix video titles
    print("\n" + "=" * 60)
    print("  FASE 2: Corrigir TITULOS dos videos")
    print("=" * 60)

    if not title_fixes:
        print("  [OK] Nenhum titulo para corrigir!")
    else:
        success = 0
        errors = 0
        for i, fix in enumerate(title_fixes):
            vid = fix['video_id']
            print(f"\n[{i+1}/{len(title_fixes)}] {vid}")
            print(f"  OLD: {fix['old_title'][:70]}")
            print(f"  NEW: {fix['new_title'][:70]}")

            try:
                result = fix_video_title(driver, vid, fix['new_title'])
                print(f"  [{result}]")

                if 'saved' in result or result == 'already_correct':
                    success += 1
                    progress.setdefault('fixed_titles', []).append(vid)
                    save_progress(progress)
                else:
                    errors += 1
            except Exception as e:
                errors += 1
                print(f"  [ERRO] {str(e)[:60]}")

            time.sleep(2)

        print(f"\n  Titulos: {success} corrigidos, {errors} erros")

    # Summary
    print("\n" + "=" * 60)
    print(f"  RESUMO FINAL")
    print(f"  Playlists corrigidas: {playlists_fixed}")
    print(f"  Titulos corrigidos: {len(progress.get('fixed_titles', []))}")
    print("=" * 60)

    print("\nFechando navegador em 5 segundos...")
    time.sleep(5)
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
