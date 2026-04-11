"""
=============================================================
SCREENPAL EXPLORER - Descobre seletores da interface
=============================================================
Abre o Chrome, voce faz login no ScreenPal, e o script
captura todos os seletores necessarios para automacao.

USO: python screenpal_explore.py
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
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


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
    time.sleep(8)

    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")

    driver = None
    for attempt in range(5):
        try:
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            break
        except Exception as e:
            if attempt < 4:
                print(f"  [RETRY] Tentativa {attempt + 1}/5...")
                time.sleep(5)
            else:
                raise e
    return driver


def wait_for_login(driver):
    """Wait for user to login to ScreenPal (auto-detect)."""
    driver.get("https://screenpal.com/login")
    time.sleep(3)

    print("\n" + "=" * 60)
    print("  FACA LOGIN NO SCREENPAL COM SUA CONTA GOOGLE")
    print("  O script vai detectar automaticamente quando voce logar.")
    print("=" * 60)

    # Poll until logged in (up to 5 minutes)
    for i in range(300):
        time.sleep(1)
        try:
            current = driver.current_url
            # If we're on a ScreenPal page that's NOT login/google auth, we're in
            if ("screenpal.com" in current and
                "login" not in current.lower() and
                "accounts.google" not in current and
                "register" not in current.lower()):
                print(f"[OK] Login detectado! URL: {current}")
                time.sleep(3)
                return True
        except Exception:
            pass
        if i % 30 == 0 and i > 0:
            print(f"  Aguardando login... ({i}s)")

    print("[ERRO] Timeout aguardando login (5 min)")
    return False


def explore_content_page(driver):
    """Explore the content/hosting dashboard."""
    print("\n[EXPLORANDO] Pagina de conteudo...")

    # Try various content URLs
    for url in ["https://screenpal.com/content", "https://screenpal.com/manage",
                "https://screenpal.com/hosting", "https://screenpal.com/u/home"]:
        driver.get(url)
        time.sleep(5)
        current = driver.current_url
        title = driver.title
        print(f"  URL: {url} -> {current}")
        print(f"  Title: {title}")

        if "login" not in current.lower() and "accounts.google" not in current:
            print(f"  [OK] Esta pagina funcionou!")
            break

    return driver.current_url


def capture_selectors(driver, page_name):
    """Capture all interactive elements on current page."""
    print(f"\n[CAPTURANDO] Seletores da pagina: {page_name}")
    print(f"  URL: {driver.current_url}")

    data = driver.execute_script("""
        var result = {
            buttons: [],
            links: [],
            inputs: [],
            fileInputs: [],
            dropZones: [],
            dialogs: [],
            menuItems: [],
            folders: [],
            videos: [],
            iframes: []
        };

        // Buttons
        document.querySelectorAll('button, [role="button"], .btn').forEach(function(el) {
            if (el.offsetParent !== null || el.offsetHeight > 0) {
                result.buttons.push({
                    tag: el.tagName,
                    text: (el.textContent || '').trim().substring(0, 80),
                    id: el.id || '',
                    className: (el.className || '').toString().substring(0, 100),
                    ariaLabel: el.getAttribute('aria-label') || '',
                    dataAction: el.getAttribute('data-action') || '',
                    type: el.type || ''
                });
            }
        });

        // Links
        document.querySelectorAll('a[href]').forEach(function(el) {
            if (el.offsetParent !== null || el.offsetHeight > 0) {
                result.links.push({
                    text: (el.textContent || '').trim().substring(0, 80),
                    href: (el.href || '').substring(0, 150),
                    id: el.id || '',
                    className: (el.className || '').toString().substring(0, 100)
                });
            }
        });

        // Inputs
        document.querySelectorAll('input, textarea').forEach(function(el) {
            result.inputs.push({
                tag: el.tagName,
                type: el.type || '',
                name: el.name || '',
                id: el.id || '',
                placeholder: el.placeholder || '',
                className: (el.className || '').toString().substring(0, 100),
                accept: el.accept || '',
                visible: el.offsetParent !== null
            });
        });

        // File inputs specifically
        document.querySelectorAll('input[type="file"]').forEach(function(el) {
            result.fileInputs.push({
                name: el.name || '',
                id: el.id || '',
                accept: el.accept || '',
                multiple: el.multiple,
                className: (el.className || '').toString().substring(0, 100)
            });
        });

        // Drop zones
        document.querySelectorAll('[class*="drop"], [class*="drag"], [class*="upload-area"], [class*="dropzone"]').forEach(function(el) {
            result.dropZones.push({
                tag: el.tagName,
                className: (el.className || '').toString().substring(0, 150),
                id: el.id || '',
                text: (el.textContent || '').trim().substring(0, 100)
            });
        });

        // Dialogs/Modals
        document.querySelectorAll('dialog, [role="dialog"], [class*="modal"], [class*="dialog"]').forEach(function(el) {
            result.dialogs.push({
                tag: el.tagName,
                className: (el.className || '').toString().substring(0, 100),
                open: el.open || el.style.display !== 'none',
                text: (el.textContent || '').trim().substring(0, 200)
            });
        });

        // Menu items
        document.querySelectorAll('[role="menuitem"], [role="option"], li > a, .menu-item').forEach(function(el) {
            if (el.offsetParent !== null) {
                result.menuItems.push({
                    text: (el.textContent || '').trim().substring(0, 80),
                    href: el.href || '',
                    className: (el.className || '').toString().substring(0, 100)
                });
            }
        });

        // Folders
        document.querySelectorAll('[class*="folder"], [data-type="folder"]').forEach(function(el) {
            result.folders.push({
                text: (el.textContent || '').trim().substring(0, 80),
                className: (el.className || '').toString().substring(0, 100)
            });
        });

        // Video items
        document.querySelectorAll('[class*="video"], [class*="media"], [class*="content-item"], [class*="card"]').forEach(function(el) {
            if (el.querySelectorAll('a, img, video').length > 0) {
                var links = [];
                el.querySelectorAll('a[href]').forEach(function(a) { links.push(a.href); });
                result.videos.push({
                    text: (el.textContent || '').trim().substring(0, 100),
                    className: (el.className || '').toString().substring(0, 100),
                    links: links.slice(0, 5)
                });
            }
        });

        // Iframes
        document.querySelectorAll('iframe').forEach(function(el) {
            result.iframes.push({
                src: el.src || '',
                id: el.id || '',
                className: (el.className || '').toString().substring(0, 100)
            });
        });

        return result;
    """)

    # Print findings
    for key, items in data.items():
        if items:
            print(f"\n  --- {key.upper()} ({len(items)}) ---")
            for item in items[:15]:  # Limit output
                print(f"    {json.dumps(item, ensure_ascii=False)}")

    return data


def explore_upload_flow(driver):
    """Try to find and open the upload dialog, then capture its selectors."""
    print("\n[EXPLORANDO] Fluxo de upload...")

    # Try clicking upload/new buttons
    clicked = driver.execute_script("""
        var btns = document.querySelectorAll('button, a, [role="button"], .btn');
        var candidates = [];
        for (var btn of btns) {
            var txt = (btn.textContent || '').toLowerCase().trim();
            var aria = (btn.getAttribute('aria-label') || '').toLowerCase();
            var cls = (btn.className || '').toString().toLowerCase();
            if (txt.includes('upload') || txt.includes('new') || txt.includes('novo') ||
                txt.includes('criar') || txt.includes('create') || txt.includes('enviar') ||
                txt.includes('+') || aria.includes('upload') || aria.includes('new') ||
                cls.includes('upload') || cls.includes('create') || cls.includes('new')) {
                if (btn.offsetParent !== null || btn.offsetHeight > 0) {
                    candidates.push({
                        tag: btn.tagName,
                        text: txt.substring(0, 50),
                        className: cls.substring(0, 80),
                        id: btn.id || ''
                    });
                }
            }
        }
        return candidates;
    """)

    print(f"\n  Candidatos a botao de upload/new:")
    for c in (clicked or []):
        print(f"    {json.dumps(c, ensure_ascii=False)}")

    if clicked:
        print(f"\n  Clicando no primeiro candidato: {clicked[0].get('text', '')}")
        driver.execute_script("""
            var btns = document.querySelectorAll('button, a, [role="button"], .btn');
            var target = arguments[0];
            for (var btn of btns) {
                var txt = (btn.textContent || '').toLowerCase().trim();
                if (txt.includes(target)) {
                    btn.click();
                    return true;
                }
            }
            return false;
        """, clicked[0].get('text', '')[:20])

        time.sleep(4)
        print("\n  [APOS CLICAR] Capturando seletores do dialog/menu...")
        capture_selectors(driver, "after_click_upload")

    return clicked


def explore_video_detail(driver):
    """Explore a video detail page to find embed/share URLs."""
    print("\n[EXPLORANDO] Pagina de detalhe do video...")

    # Check if there are any videos to click on
    video_link = driver.execute_script("""
        var links = document.querySelectorAll('a[href]');
        for (var a of links) {
            if (a.href.includes('/watch/') || a.href.includes('/detail/') ||
                a.href.includes('/video/') || a.href.includes('/edit/')) {
                return a.href;
            }
        }
        // Try clicking on a video thumbnail/card
        var cards = document.querySelectorAll('[class*="card"], [class*="item"], [class*="video"], [class*="thumb"]');
        for (var card of cards) {
            var a = card.querySelector('a[href]');
            if (a && a.href.includes('screenpal.com')) {
                return a.href;
            }
        }
        return null;
    """)

    if video_link:
        print(f"  Encontrou link de video: {video_link}")
        driver.get(video_link)
        time.sleep(5)
        capture_selectors(driver, "video_detail")
    else:
        print("  Nenhum video encontrado para explorar detalhes.")
        print("  (Normal se a conta for nova e nao tiver videos ainda)")


def main():
    print("=" * 60)
    print("  SCREENPAL EXPLORER")
    print("=" * 60)

    driver = create_driver()
    wait_for_login(driver)

    # Explore content page
    content_url = explore_content_page(driver)
    data_content = capture_selectors(driver, "content_dashboard")

    # Explore upload flow
    explore_upload_flow(driver)

    # Go back to content and explore video detail
    driver.get(content_url)
    time.sleep(3)
    explore_video_detail(driver)

    # Save all data
    print("\n\n" + "=" * 60)
    print("  EXPLORACAO COMPLETA")
    print("=" * 60)
    print("  Os seletores foram impressos acima.")
    print("  Copie o output e envie para o Claude para ajustar o script.")
    print("=" * 60)

    print("\n  Chrome permanece aberto para inspecao manual.")
    print("  Feche o Chrome manualmente quando terminar.")


if __name__ == "__main__":
    main()
