"""
=============================================================
UPDATE SITE LINKS - Substitui URLs do ClickUp pelo ScreenPal
=============================================================
Executa APOS todos os uploads ao ScreenPal terem sido feitos.
Le o screenpal_results.json e atualiza o script.js do site.

USO: python update_site_links.py
=============================================================
"""

import json
import re
import sys
import os
import html
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

RESULTS_FILE = "screenpal_results.json"
SITE_SCRIPT = "script.js"
BACKUP_FILE = "script.js.backup"


def clean_url(url):
    """Clean URL removing HTML entities."""
    return html.unescape(url)


def normalize_url(url):
    """Normalize URL for comparison (remove tracking params, decode entities)."""
    url = html.unescape(url)
    # Remove Google redirect params
    if "&sa=D&source=editors" in url:
        url = url.split("&sa=D&source=editors")[0]
    # Remove query params for matching
    base = url.split("?")[0]
    return base.lower().strip()


def build_url_mapping(results):
    """Build mapping from original ClickUp URL -> ScreenPal URL."""
    mapping = {}
    for client_name, videos in results.items():
        for video in videos:
            original = video.get("original_url", "")
            screenpal = video.get("screenpal_url", "")
            if original and screenpal and screenpal != "UPLOADED_NO_URL":
                # Store multiple forms of the URL for matching
                mapping[normalize_url(original)] = screenpal
                # Also store the HTML-escaped version
                escaped = original.replace("&", "&amp;")
                mapping[normalize_url(escaped)] = screenpal
    return mapping


def main():
    print("=" * 60)
    print("  UPDATE SITE LINKS")
    print("=" * 60)

    # Load results
    if not os.path.exists(RESULTS_FILE):
        print(f"[ERRO] {RESULTS_FILE} nao encontrado!")
        print("       Execute o screenpal_uploader.py primeiro.")
        return

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    total_videos = sum(len(vids) for vids in results.values())
    print(f"[INFO] {total_videos} videos no ScreenPal, {len(results)} clientes")

    # Build URL mapping
    mapping = build_url_mapping(results)
    print(f"[INFO] {len(mapping)} URLs mapeadas")

    if not mapping:
        print("[ERRO] Nenhuma URL para atualizar!")
        return

    # Read script.js
    if not os.path.exists(SITE_SCRIPT):
        print(f"[ERRO] {SITE_SCRIPT} nao encontrado!")
        return

    with open(SITE_SCRIPT, "r", encoding="utf-8") as f:
        content = f.read()

    # Backup
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Backup salvo em {BACKUP_FILE}")

    # Find and replace ClickUp URLs
    replaced = 0
    not_found = 0
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        if 'clickup-attachments.com' in line or 'clickup' in line.lower():
            # Extract the URL from this line
            url_match = re.search(r'url:\s*"([^"]+)"', line)
            if url_match:
                original_url = url_match.group(1)
                normalized = normalize_url(original_url)

                # Try to find matching ScreenPal URL
                screenpal_url = mapping.get(normalized)

                if not screenpal_url:
                    # Try partial matching (just the UUID part of ClickUp URL)
                    uuid_match = re.search(r'/([a-f0-9-]{36})/', normalized)
                    if uuid_match:
                        uuid = uuid_match.group(1)
                        for key, val in mapping.items():
                            if uuid in key:
                                screenpal_url = val
                                break

                if screenpal_url:
                    new_line = line.replace(original_url, screenpal_url)
                    new_lines.append(new_line)
                    replaced += 1
                else:
                    new_lines.append(line)
                    not_found += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    new_content = '\n'.join(new_lines)

    # Write updated file
    with open(SITE_SCRIPT, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"\n[RESULTADO]")
    print(f"  URLs substituidas: {replaced}")
    print(f"  URLs nao encontradas: {not_found}")
    print(f"  Arquivo atualizado: {SITE_SCRIPT}")
    print(f"  Backup: {BACKUP_FILE}")

    if not_found > 0:
        print(f"\n[AVISO] {not_found} URLs do ClickUp nao foram encontradas no ScreenPal.")
        print("        Esses videos ainda apontam para o ClickUp.")

    if replaced > 0:
        print(f"\n[SUCESSO] {replaced} links atualizados para ScreenPal!")
        print("          Teste o site localmente antes de fazer deploy.")


if __name__ == "__main__":
    main()
