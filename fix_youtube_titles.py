"""
=============================================================
FIX YOUTUBE TITLES & DESCRIPTIONS
=============================================================
Lê youtube_results.json, identifica títulos e descrições com
caracteres quebrados e corrige diretamente no YouTube Studio.

Baseado no PDF "Allfluence - Portfólio pessoal" como referência
dos nomes corretos.

USO: python fix_youtube_titles.py
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

# Mapa de correções confirmado com o PDF "Allfluence - Portfólio pessoal"
ACCENT_FIXES = {
    # Nomes de clientes
    "Atacad o": "Atacadão",
    "Faculdade Est cio": "Faculdade Estácio",
    "For\ufffda da Terra": "Força da Terra",
    "Philco Brit nia": "Philco Britânia",
    "Nestl /": "Nestlé /",
    # Nomes de talentos (confirmados com PDF)
    "Jo o Mendes": "João Mendes",
    "Jo o Victor": "João Victor",
    "Joa\u0303o": "João",           # tilde combinante
    "D bora Melo": "Débora Melo",
    "D bora Mel": "Débora Mel",     # truncado em nomes de arquivo
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
    # HTML entities que sobrevivem nos títulos
    "Joa&#771;o": "João",
}


def fix_accents(text):
    """Corrige acentos quebrados e HTML entities."""
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
        "--no-first-run", "--no-default-browser-check", "--log-level=3",
    ]
    print(f"[BROWSER] Iniciando Chrome (porta {CHROME_DEBUG_PORT})...")
    subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
                print(f"  [RETRY] Tentativa {attempt + 1}/5...")
                time.sleep(5)
            else:
                raise e


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"fixed_titles": []}


def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def replace_field_text(driver, selector, new_text):
    """Replace text in a contenteditable field identified by CSS selector."""
    # Foca no campo
    driver.execute_script(f"""
        var tb = document.querySelector('{selector}');
        if (tb) {{ tb.focus(); tb.click(); }}
    """)
    time.sleep(0.5)

    # Seleciona tudo e apaga
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

    # Digita o novo texto via send_keys
    try:
        active = driver.switch_to.active_element
        active.send_keys(new_text)
    except Exception:
        driver.execute_script(f"""
            var tb = document.querySelector('{selector}');
            if (tb) {{
                tb.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, arguments[0]);
            }}
        """, new_text)
    time.sleep(1)

    # Verifica o que foi digitado
    typed = driver.execute_script(f"""
        var tb = document.querySelector('{selector}');
        return tb ? tb.textContent.trim() : '';
    """)
    return typed


def save_video_edit(driver):
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


def fix_video_title_and_description(driver, video_id, new_title):
    """Navega à página de edição do vídeo, corrige título e descrição, e salva."""

    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(6)

    # Espera o editor carregar
    for _ in range(15):
        ready = driver.execute_script("""
            var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
            return tb && tb.textContent.trim().length > 0;
        """)
        if ready:
            break
        time.sleep(2)

    # Pega título e descrição atuais
    current_title = driver.execute_script("""
        var tb = document.querySelector('#title-textarea #textbox, ytcp-mention-textbox #textbox');
        return tb ? tb.textContent.trim() : '';
    """)

    current_desc = driver.execute_script("""
        var tb = document.querySelector('#description-textarea #textbox, #description-container #textbox');
        if (tb) return tb.textContent.trim();
        // Fallback: second textbox on the page
        var boxes = document.querySelectorAll('ytcp-social-suggestions-textbox #textbox');
        return boxes.length > 0 ? boxes[boxes.length - 1].textContent.trim() : '';
    """)

    if not current_title:
        return 'page_not_loaded', False

    # Calcula novas versões
    fixed_desc = fix_accents(current_desc) if current_desc else current_desc
    title_needs_fix = current_title != new_title
    desc_needs_fix = current_desc and fixed_desc != current_desc

    if not title_needs_fix and not desc_needs_fix:
        return 'already_correct', False

    changed = False

    # Corrige título se necessário
    if title_needs_fix:
        typed = replace_field_text(driver, '#title-textarea #textbox', new_title)
        if typed:
            print(f"    [TITLE] Corrigido")
            changed = True
        else:
            print(f"    [TITLE] Falha ao digitar")

    # Corrige descrição se necessário
    if desc_needs_fix:
        print(f"    [DESC] Corrigindo descricao...")

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

        typed_desc = replace_field_text(
            driver,
            '#description-textarea #textbox',
            fixed_desc
        )
        if typed_desc:
            print(f"    [DESC] Corrigido")
            changed = True
        else:
            # Fallback selector
            typed_desc = replace_field_text(
                driver,
                '#description-container #textbox',
                fixed_desc
            )
            if typed_desc:
                print(f"    [DESC] Corrigido (fallback)")
                changed = True
            else:
                print(f"    [DESC] Falha ao digitar descricao")

    if not changed:
        return 'no_changes_applied', False

    # Salva
    save_result = save_video_edit(driver)
    return save_result, desc_needs_fix


def main():
    print("=" * 60)
    print("  FIX YOUTUBE TITLES - Corrigir acentos quebrados")
    print("=" * 60)
    print()

    # Carrega resultados
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Carrega progresso
    progress = load_progress()
    fixed_ids = set(progress.get("fixed_titles", []))

    # Identifica vídeos com título para corrigir
    # Nota: descrição será verificada ao vivo no YouTube Studio
    # (não temos no JSON), então incluímos todos com título quebrado
    fixes = []
    for client, videos in results.items():
        for v in videos:
            vid = v['video_id']
            if vid in fixed_ids:
                continue
            old_title = v['title']
            new_title = fix_accents(old_title)
            if new_title != old_title:
                fixes.append({
                    'video_id': vid,
                    'client': client,
                    'old_title': old_title,
                    'new_title': new_title,
                })

    print(f"  Videos com titulo para corrigir: {len(fixes)}")
    print(f"  (descricao sera verificada ao vivo no YouTube Studio)")
    print(f"  Ja corrigidos anteriormente: {len(fixed_ids)}")
    print()

    if not fixes:
        print("[OK] Todos os titulos ja estao corretos!")
        return

    # Mostra o que vai ser corrigido
    by_client = {}
    for f in fixes:
        by_client.setdefault(f['client'], []).append(f)

    for client, client_fixes in by_client.items():
        print(f"  {client} ({len(client_fixes)} videos):")
        for cf in client_fixes[:2]:
            print(f"    {cf['video_id']}: \"{cf['old_title'][:55]}\"")
            print(f"             -> \"{cf['new_title'][:55]}\"")
        if len(client_fixes) > 2:
            print(f"    ... +{len(client_fixes)-2} mais")
        print()

    print("  IMPORTANTE: Feche todas as janelas do Chrome antes!")
    print()
    print("[AUTO] Iniciando em 3 segundos...")
    time.sleep(3)

    # Abre Chrome
    print("[BROWSER] Abrindo Chrome...")
    driver = create_driver()

    # Verifica YouTube Studio
    print("[BROWSER] Verificando YouTube Studio...")
    driver.get("https://studio.youtube.com")
    time.sleep(5)
    channel = driver.execute_script("""
        var el = document.querySelector('ytcp-entity-name, .entity-name, #entity-name');
        return el ? el.textContent.trim() : 'desconhecido';
    """)
    print(f"[CANAL] {channel}")
    print()

    # Processa cada vídeo
    success = 0
    errors = 0

    for i, fix in enumerate(fixes):
        vid = fix['video_id']
        client = fix['client']
        old = fix['old_title']
        new = fix['new_title']

        print(f"[{i+1}/{len(fixes)}] {vid} ({client})")
        print(f"  DE:   \"{old[:65]}\"")
        print(f"  PARA: \"{new[:65]}\"")

        try:
            result, desc_fixed = fix_video_title_and_description(driver, vid, new)
            print(f"  -> {result}")

            if 'saved' in result or result == 'already_correct':
                success += 1
                progress.setdefault("fixed_titles", []).append(vid)
                save_progress(progress)

                if result == 'already_correct':
                    print(f"  [OK] Titulo e descricao ja estavam corretos")
                else:
                    msg = "Titulo"
                    if desc_fixed:
                        msg += " e descricao"
                    print(f"  [OK] {msg} corrigido(s)!")

                    # Atualiza youtube_results.json com o título correto
                    for v in results.get(client, []):
                        if v['video_id'] == vid:
                            v['title'] = new
                            break
                    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
            else:
                errors += 1
                print(f"  [FALHA] {result}")

        except Exception as e:
            errors += 1
            print(f"  [ERRO] {str(e)[:80]}")

        time.sleep(3)

    # Resumo
    print()
    print("=" * 60)
    print(f"  RESUMO")
    print(f"  Total processados: {len(fixes)}")
    print(f"  Corrigidos: {success}")
    print(f"  Erros: {errors}")
    print("=" * 60)

    print("\nFechando navegador em 5 segundos...")
    time.sleep(5)
    try:
        driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
