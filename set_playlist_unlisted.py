"""
Set a YouTube playlist to Unlisted using Selenium.
Usage: python set_playlist_unlisted.py
"""

import os
import sys
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_DEBUG_PORT = 9555
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLc0_ioTU8huSBWKGOtLiTHTvbs-BCVvKg"


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
            break
        except Exception as e:
            if attempt < 4:
                print(f"  [RETRY] Tentativa {attempt + 1}/5 - aguardando Chrome...")
                time.sleep(5)
            else:
                raise RuntimeError(f"Nao conectou ao Chrome: {e}")
    return driver


def set_playlist_unlisted(driver):
    playlist_id = PLAYLIST_URL.split("list=")[1]
    studio_url = f"https://studio.youtube.com/playlist/{playlist_id}/edit"

    print(f"[NAV] Abrindo YouTube Studio: {studio_url}")
    driver.get(studio_url)
    time.sleep(8)

    # Take debug screenshot first
    driver.save_screenshot("debug_playlist_page.png")
    print("[DEBUG] Screenshot salvo: debug_playlist_page.png")

    # Dump page structure to find the visibility element
    page_info = driver.execute_script("""
        var info = [];

        // Find all dropdowns
        var dropdowns = document.querySelectorAll('ytcp-dropdown-trigger, tp-yt-paper-dropdown-menu');
        info.push('=== DROPDOWNS (' + dropdowns.length + ') ===');
        for (var i = 0; i < dropdowns.length; i++) {
            var d = dropdowns[i];
            var txt = (d.textContent || '').trim().replace(/\\s+/g, ' ').substring(0, 100);
            var cls = d.className || '';
            var id = d.id || '';
            info.push('  [' + i + '] tag=' + d.tagName + ' id=' + id + ' class=' + cls.substring(0, 60) + ' text="' + txt + '"');
        }

        // Find elements with "visib" or "público" text
        info.push('=== VISIBILITY ELEMENTS ===');
        var all = document.querySelectorAll('*');
        for (var el of all) {
            if (el.children.length > 5) continue;
            var txt = (el.textContent || '').trim().toLowerCase();
            if (txt.length > 200) continue;
            if (txt.includes('visib') || txt === 'público' || txt === 'public' ||
                txt === 'unlisted' || txt === 'não listado' || txt === 'privado' || txt === 'private') {
                info.push('  tag=' + el.tagName + ' id=' + (el.id || '') + ' class=' + (el.className || '').substring(0, 40) + ' text="' + txt.substring(0, 80) + '"');
            }
        }

        // Find buttons/links
        info.push('=== BUTTONS ===');
        var btns = document.querySelectorAll('ytcp-button, button[aria-label]');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().replace(/\\s+/g, ' ').substring(0, 60);
            var aria = b.getAttribute('aria-label') || '';
            if (txt || aria) {
                info.push('  tag=' + b.tagName + ' aria="' + aria + '" text="' + txt + '"');
            }
        }

        return info.join('\\n');
    """)
    print(page_info)

    # Click the visibility dropdown specifically (identified as #metadata-visibility-menu)
    print("\n[ACTION] Procurando dropdown de visibilidade...")
    result = driver.execute_script("""
        // Direct target: the visibility menu element
        var visMenu = document.querySelector('#metadata-visibility-menu, ytcp-playlist-metadata-visibility');
        if (visMenu) {
            var trigger = visMenu.querySelector('ytcp-dropdown-trigger') || visMenu;
            trigger.click();
            return 'clicked_visibility_menu';
        }

        // Fallback: find dropdown whose label text is "visibilidade" or "visibility"
        var dropdowns = document.querySelectorAll('ytcp-dropdown-trigger');
        for (var dd of dropdowns) {
            var labelEl = dd.querySelector('.label-text');
            if (labelEl) {
                var labelTxt = (labelEl.textContent || '').trim().toLowerCase();
                if (labelTxt === 'visibilidade' || labelTxt === 'visibility') {
                    dd.click();
                    return 'clicked_by_label: ' + labelTxt;
                }
            }
        }

        // Fallback 2: find dropdown containing "pública" or "public" (visibility value)
        for (var dd of dropdowns) {
            var ddText = (dd.textContent || '').toLowerCase();
            if (ddText.includes('pública') || ddText.includes('public') ||
                ddText.includes('não listado') || ddText.includes('unlisted')) {
                dd.click();
                return 'clicked_by_text: ' + ddText.trim().substring(0, 50);
            }
        }

        return 'visibility_dropdown_not_found';
    """)
    print(f"[RESULT] {result}")
    time.sleep(3)

    if 'not_found' in str(result):
        print("[AVISO] Dropdown de visibilidade não encontrado na página.")
        driver.save_screenshot("debug_no_visibility.png")
        print("[DEBUG] Screenshot: debug_no_visibility.png")
        return

    # Select "Unlisted" / "Não listado"
    print("[ACTION] Selecionando 'Não listado'...")
    time.sleep(3)

    # Debug: dump dropdown menu items
    menu_info = driver.execute_script("""
        var info = [];
        // Check tp-yt-paper-item elements
        var items = document.querySelectorAll('tp-yt-paper-item');
        info.push('tp-yt-paper-item count: ' + items.length);
        for (var i = 0; i < items.length; i++) {
            var txt = (items[i].textContent || '').trim().replace(/\\s+/g, ' ').substring(0, 80);
            var vis = items[i].offsetParent !== null ? 'visible' : 'hidden';
            info.push('  [' + i + '] ' + vis + ' text="' + txt + '"');
        }

        // Check iron-dropdown, paper-listbox
        var listboxes = document.querySelectorAll('tp-yt-paper-listbox, tp-yt-iron-dropdown, ytcp-text-menu');
        info.push('listbox/dropdown count: ' + listboxes.length);
        for (var lb of listboxes) {
            var vis = lb.offsetParent !== null || getComputedStyle(lb).display !== 'none' ? 'visible' : 'hidden';
            info.push('  tag=' + lb.tagName + ' ' + vis + ' children=' + lb.children.length);
        }

        // Check any element with "listado" or "unlisted"
        var all = document.querySelectorAll('*');
        var found = [];
        for (var el of all) {
            var txt = (el.textContent || '').trim().toLowerCase();
            if (txt.length < 60 && (txt.includes('não listada') || txt.includes('não listado') ||
                txt.includes('unlisted') || txt.includes('nao lista'))) {
                found.push('tag=' + el.tagName + ' class=' + (el.className||'').substring(0,40) + ' text="' + txt + '"');
            }
        }
        info.push('Elements with unlisted text: ' + found.length);
        for (var f of found) info.push('  ' + f);

        return info.join('\\n');
    """)
    print(menu_info)

    driver.save_screenshot("debug_dropdown_open.png")
    print("[DEBUG] Screenshot dropdown aberto: debug_dropdown_open.png")

    select_result = driver.execute_script("""
        // Method 1: tp-yt-paper-item with unlisted text
        var items = document.querySelectorAll('tp-yt-paper-item');
        for (var item of items) {
            var txt = (item.textContent || '').toLowerCase();
            if (txt.includes('não listada') || txt.includes('não listado') ||
                txt.includes('nao listada') || txt.includes('nao listado') ||
                txt.includes('unlisted')) {
                item.click();
                return 'selected_unlisted_paper_item';
            }
        }

        // Method 2: any clickable with the right text
        var all = document.querySelectorAll('div, span, a, button, tp-yt-paper-radio-button');
        for (var el of all) {
            if (el.children.length > 5) continue;
            var txt = (el.textContent || '').trim().toLowerCase();
            if (txt.length < 60 && (txt.includes('não listada') || txt.includes('unlisted'))) {
                el.click();
                return 'clicked_fallback: ' + el.tagName + ' ' + txt;
            }
        }

        return 'unlisted_not_found';
    """)
    print(f"[RESULT] {select_result}")
    time.sleep(3)

    # Save
    print("[ACTION] Salvando alteracoes...")
    driver.save_screenshot("debug_before_save.png")
    save_result = driver.execute_script("""
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            if (b.offsetParent === null) continue;
            var txt = (b.textContent || '').trim().toLowerCase();
            if (txt === 'save' || txt === 'salvar') {
                var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                if (!disabled) {
                    b.click();
                    return 'saved: ' + txt;
                }
                return 'save_disabled';
            }
        }
        return 'no_save_btn';
    """)
    print(f"[RESULT] {save_result}")
    time.sleep(5)

    driver.save_screenshot("debug_after_save.png")
    print("[DEBUG] Screenshots salvos para verificação.")

    if 'saved' in str(save_result):
        print("[OK] Playlist configurada como não listada!")
    else:
        print("[AVISO] Verifique manualmente se a alteração foi salva.")


def main():
    print("=" * 60)
    print("SET PLAYLIST TO UNLISTED")
    print("=" * 60)
    print(f"Playlist: {PLAYLIST_URL}")
    print()

    driver = create_driver()
    try:
        set_playlist_unlisted(driver)
    except Exception as e:
        print(f"[ERRO] {e}")
        try:
            driver.save_screenshot("debug_error.png")
        except Exception:
            pass
    finally:
        print("\n[BROWSER] Chrome permanece aberto para verificação.")


if __name__ == "__main__":
    main()
