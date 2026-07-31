"""
=============================================================
YOUTUBE PLAYLIST MANAGER - Savylla Adryan Portfolio
=============================================================
Usa YouTube Data API v3 para:
  1. Listar TODAS as playlists do canal
  2. Identificar playlists DUPLICADAS (mesmo nome)
  3. Listar videos em cada playlist, detectar EXCLUIDOS
  4. MERGE: mover videos das duplicatas para a canonica
  5. LIMPAR: remover entradas de videos excluidos
  6. VERIFICAR: checar quais video IDs do progress realmente existem
  7. ATUALIZAR: upload_progress.json removendo videos deletados

USO:
  python youtube_playlist_manager.py --analyze       # Apenas analisa (sem modificar)
  python youtube_playlist_manager.py --merge         # Merge duplicatas + limpa excluidos
  python youtube_playlist_manager.py --verify        # Verifica videos no progress
  python youtube_playlist_manager.py --full          # Tudo: analyze + merge + verify
=============================================================
"""

import json
import os
import sys
import time
import argparse
from collections import defaultdict
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

TOKEN_FILE = "token.json"
CLIENT_SECRET_FILE = "client_secret.json"
PROGRESS_FILE = "upload_progress.json"
RESULTS_FILE = "youtube_results.json"
REPORT_FILE = "playlist_manager_report.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]


def get_youtube_service():
    """Authenticate and return YouTube Data API service."""
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
                scopes=token_data.get("scopes", SCOPES),
            )
        except Exception as e:
            print(f"[AUTH] Erro ao carregar token: {e}")

    # Try refreshing expired token
    if creds and creds.expired and creds.refresh_token:
        try:
            print("[AUTH] Renovando token...")
            creds.refresh(Request())
            _save_credentials(creds)
            print("[AUTH] Token renovado e salvo.")
            return build("youtube", "v3", credentials=creds)
        except Exception as e:
            print(f"[AUTH] Refresh falhou: {e}")
            creds = None

    # If token looks valid, test it with a real API call
    if creds and (creds.valid or creds.token):
        try:
            service = build("youtube", "v3", credentials=creds)
            # Test with a lightweight API call
            service.channels().list(part="id", mine=True).execute()
            return service
        except Exception as e:
            print(f"[AUTH] Token existente falhou: {str(e)[:80]}")
            creds = None

    # Need new authentication via OAuth2 flow
    print("[AUTH] Token invalido ou ausente. Iniciando autenticacao OAuth2...")
    creds = _run_oauth_flow()
    if not creds:
        print("[ERRO] Autenticacao falhou.")
        sys.exit(1)

    return build("youtube", "v3", credentials=creds)


def _run_oauth_flow():
    """Run OAuth2 installed app flow to get new credentials."""
    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"[ERRO] {CLIENT_SECRET_FILE} nao encontrado.")
        print("       Baixe de Google Cloud Console > APIs & Services > Credentials")
        return None

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=8090, open_browser=True)
        _save_credentials(creds)
        print("[AUTH] Autenticacao concluida e token salvo.")
        return creds
    except ImportError:
        print("[ERRO] google-auth-oauthlib nao instalado.")
        print("       Execute: pip install google-auth-oauthlib")
        return None
    except Exception as e:
        print(f"[ERRO] OAuth flow falhou: {e}")
        return None


def _save_credentials(creds):
    """Save credentials to token.json."""
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes) if creds.scopes else SCOPES,
        "expiry": creds.expiry.isoformat() + "Z" if creds.expiry else None,
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"[AUTH] Token salvo em {TOKEN_FILE}")


def list_all_playlists(youtube):
    """List all playlists on the channel."""
    playlists = []
    next_page = None

    while True:
        request = youtube.playlists().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50,
            pageToken=next_page,
        )
        response = request.execute()

        for item in response.get("items", []):
            playlists.append({
                "id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "video_count": item["contentDetails"]["itemCount"],
                "published_at": item["snippet"]["publishedAt"],
            })

        next_page = response.get("nextPageToken")
        if not next_page:
            break

    return playlists


def list_playlist_items(youtube, playlist_id):
    """List all video items in a playlist, including deleted ones."""
    items = []
    next_page = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails,status",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page,
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"].get("title", "")
            status = item.get("status", {}).get("privacyStatus", "unknown")

            # Deleted videos show as "Deleted video" or "Private video"
            is_deleted = title in ("Deleted video", "Private video", "[Video excluído]",
                                   "Video excluído", "Vídeo excluído")
            # Also check if video is unavailable
            if item["snippet"].get("description", "") == "This video is unavailable.":
                is_deleted = True

            items.append({
                "playlist_item_id": item["id"],
                "video_id": video_id,
                "title": title,
                "position": item["snippet"]["position"],
                "is_deleted": is_deleted,
                "privacy_status": status,
            })

        next_page = response.get("nextPageToken")
        if not next_page:
            break

    return items


def check_videos_exist(youtube, video_ids):
    """Check which video IDs actually exist on YouTube. Returns set of existing IDs."""
    existing = set()
    # API allows up to 50 IDs per request
    batch_size = 50
    id_list = list(video_ids)

    for i in range(0, len(id_list), batch_size):
        batch = id_list[i:i + batch_size]
        request = youtube.videos().list(
            part="id,status",
            id=",".join(batch),
        )
        response = request.execute()
        for item in response.get("items", []):
            existing.add(item["id"])

        # Rate limiting
        if i + batch_size < len(id_list):
            time.sleep(0.5)

    return existing


def add_video_to_playlist(youtube, playlist_id, video_id):
    """Add a video to a playlist."""
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                },
            }
        },
    )
    return request.execute()


def remove_playlist_item(youtube, playlist_item_id):
    """Remove an item from a playlist."""
    youtube.playlistItems().delete(id=playlist_item_id).execute()


def delete_playlist(youtube, playlist_id):
    """Delete a playlist entirely."""
    youtube.playlists().delete(id=playlist_id).execute()


# =============================================================
# PHASE 1: ANALYZE
# =============================================================

def analyze_channel(youtube):
    """Full channel analysis: playlists, duplicates, deleted videos."""
    print("=" * 60)
    print("  FASE 1: ANALISE DO CANAL")
    print("=" * 60)

    # List all playlists
    print("\n[1/3] Listando todas as playlists...")
    playlists = list_all_playlists(youtube)
    print(f"  Total de playlists: {len(playlists)}")

    # Group by name to find duplicates
    by_name = defaultdict(list)
    for pl in playlists:
        by_name[pl["title"]].append(pl)

    duplicates = {name: pls for name, pls in by_name.items() if len(pls) > 1}
    unique = {name: pls[0] for name, pls in by_name.items() if len(pls) == 1}

    print(f"  Playlists unicas: {len(unique)}")
    print(f"  Nomes com duplicatas: {len(duplicates)}")

    if duplicates:
        print("\n  PLAYLISTS DUPLICADAS:")
        for name, pls in sorted(duplicates.items()):
            print(f"    '{name}': {len(pls)} copias")
            for pl in pls:
                print(f"      - ID: {pl['id']} | Videos: {pl['video_count']} | Criada: {pl['published_at'][:10]}")

    # Analyze each playlist for deleted videos
    print("\n[2/3] Verificando videos em cada playlist...")
    playlist_details = {}
    total_deleted = 0
    total_alive = 0

    all_playlists_flat = playlists
    for idx, pl in enumerate(all_playlists_flat):
        items = list_playlist_items(youtube, pl["id"])
        deleted_items = [it for it in items if it["is_deleted"]]
        alive_items = [it for it in items if not it["is_deleted"]]

        total_deleted += len(deleted_items)
        total_alive += len(alive_items)

        playlist_details[pl["id"]] = {
            "title": pl["title"],
            "total": len(items),
            "alive": len(alive_items),
            "deleted": len(deleted_items),
            "items": items,
            "alive_video_ids": {it["video_id"] for it in alive_items},
            "deleted_items": deleted_items,
        }

        status_char = "!" if deleted_items else "."
        print(f"  [{idx+1}/{len(all_playlists_flat)}] {pl['title']}: {len(alive_items)} vivos, {len(deleted_items)} excluidos {status_char}")

        # Rate limiting
        time.sleep(0.3)

    print(f"\n  RESUMO:")
    print(f"    Videos vivos em playlists: {total_alive}")
    print(f"    Videos excluidos (fantasma): {total_deleted}")

    # Check upload_progress
    print("\n[3/3] Verificando upload_progress.json...")
    progress_data = load_progress()
    uploaded = progress_data.get("uploaded", {})
    progress_video_ids = set()
    for entry in uploaded.values():
        vid = entry.get("video_id", "")
        if vid and len(vid) == 11:
            progress_video_ids.add(vid)

    print(f"  Video IDs no progress: {len(progress_video_ids)}")

    # Check which progress videos actually exist
    if progress_video_ids:
        print("  Verificando existencia via API (pode demorar)...")
        existing_ids = check_videos_exist(youtube, progress_video_ids)
        missing_ids = progress_video_ids - existing_ids
        print(f"  Videos que existem: {len(existing_ids)}")
        print(f"  Videos DELETADOS/INEXISTENTES: {len(missing_ids)}")

        if missing_ids:
            print("\n  VIDEOS DELETADOS NO PROGRESS:")
            for key, entry in uploaded.items():
                if entry.get("video_id") in missing_ids:
                    print(f"    {key}: {entry.get('title', '?')[:60]} (ID: {entry.get('video_id')})")
    else:
        existing_ids = set()
        missing_ids = set()

    report = {
        "playlists": playlists,
        "duplicates": {name: [p["id"] for p in pls] for name, pls in duplicates.items()},
        "unique_playlists": {name: p["id"] for name, p in unique.items()},
        "playlist_details": {
            pid: {
                "title": d["title"],
                "total": d["total"],
                "alive": d["alive"],
                "deleted": d["deleted"],
                "deleted_items": d["deleted_items"],
                "alive_video_ids": list(d["alive_video_ids"]),
            }
            for pid, d in playlist_details.items()
        },
        "progress_video_ids": list(progress_video_ids),
        "existing_video_ids": list(existing_ids),
        "missing_video_ids": list(missing_ids),
        "missing_video_details": [
            {"key": k, "video_id": v.get("video_id"), "title": v.get("title"), "client": v.get("client")}
            for k, v in uploaded.items()
            if v.get("video_id") in missing_ids
        ],
    }

    return report, duplicates, playlist_details, playlists


# =============================================================
# PHASE 2: MERGE DUPLICATES + CLEAN DELETED
# =============================================================

def find_similar_playlists(playlists):
    """Find playlists with similar names (typos, broken accents)."""
    import unicodedata

    def normalize(name):
        """Normalize playlist name for comparison."""
        # Fix common typos and encoding issues
        n = name.strip()
        n = n.replace("Portifólio", "Portfolio")  # typo fix
        n = n.replace("Portifolio", "Portfolio")
        # Fix broken UTF-8 (e.g., "ForÃ§a" -> "Força")
        try:
            n_bytes = n.encode('latin-1')
            n = n_bytes.decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
        n = unicodedata.normalize('NFC', n)
        return n

    # Group by normalized name
    groups = defaultdict(list)
    for pl in playlists:
        normalized = normalize(pl["title"])
        groups[normalized].append(pl)

    similar = {name: pls for name, pls in groups.items() if len(pls) > 1}
    return similar


def merge_and_clean(youtube, duplicates, playlist_details, all_playlists=None):
    """Merge duplicate playlists and remove deleted video entries."""
    print("\n" + "=" * 60)
    print("  FASE 2: MERGE E LIMPEZA")
    print("=" * 60)

    # Also find similar playlists (typos, broken accents)
    if all_playlists:
        similar = find_similar_playlists(all_playlists)
        # Add similar groups that aren't already in duplicates
        for norm_name, pls in similar.items():
            names_in_group = set(p["title"] for p in pls)
            if len(names_in_group) > 1:  # Different actual names but same normalized
                print(f"\n  [SIMILAR] Nomes parecidos detectados: {names_in_group}")
                # Add to duplicates using the normalized name
                if norm_name not in duplicates:
                    duplicates[norm_name] = pls
                else:
                    # Extend existing duplicates
                    existing_ids = {p["id"] for p in duplicates[norm_name]}
                    for p in pls:
                        if p["id"] not in existing_ids:
                            duplicates[norm_name].append(p)

    # Merge duplicates
    if duplicates:
        print(f"\n[MERGE] {len(duplicates)} grupos de playlists duplicadas")
        for name, pls_list in sorted(duplicates.items()):
            print(f"\n  Processando: '{name}'")

            # Pick canonical: prefer the one with most videos, then oldest
            sorted_pls = sorted(pls_list, key=lambda p: (-p["video_count"], p["published_at"]))
            canonical = sorted_pls[0]
            to_merge = sorted_pls[1:]

            # If canonical has wrong name (typo/broken accent), rename it
            if canonical["title"] != name and name.startswith("Portfolio"):
                try:
                    youtube.playlists().update(
                        part="snippet",
                        body={
                            "id": canonical["id"],
                            "snippet": {
                                "title": name,
                                "description": canonical.get("description", ""),
                            },
                        },
                    ).execute()
                    print(f"    [RENOMEADA] '{canonical['title']}' -> '{name}'")
                except Exception as e:
                    print(f"    [AVISO] Nao renomeou: {str(e)[:80]}")

            canonical_detail = playlist_details.get(canonical["id"], {})
            canonical_video_ids = canonical_detail.get("alive_video_ids", set())

            print(f"    Canonica: {canonical['id']} ({canonical['video_count']} videos, criada {canonical['published_at'][:10]})")

            for dup in to_merge:
                dup_detail = playlist_details.get(dup["id"], {})
                dup_items = dup_detail.get("items", [])
                alive_items = [it for it in dup_items if not it["is_deleted"]]

                print(f"    Duplicata: {dup['id']} ({len(alive_items)} videos vivos)")

                # Move videos that aren't already in canonical
                moved = 0
                for item in alive_items:
                    if item["video_id"] not in canonical_video_ids:
                        try:
                            add_video_to_playlist(youtube, canonical["id"], item["video_id"])
                            canonical_video_ids.add(item["video_id"])
                            moved += 1
                            print(f"      [MOVIDO] {item['video_id']}: {item['title'][:50]}")
                            time.sleep(0.5)
                        except Exception as e:
                            print(f"      [ERRO] {item['video_id']}: {str(e)[:80]}")
                    else:
                        print(f"      [SKIP] {item['video_id']}: ja existe na canonica")

                print(f"    {moved} videos movidos para canonica")

                # Delete the duplicate playlist
                try:
                    delete_playlist(youtube, dup["id"])
                    print(f"    [DELETADA] Playlist duplicata {dup['id']}")
                except Exception as e:
                    print(f"    [ERRO] Nao deletou playlist {dup['id']}: {str(e)[:80]}")

                time.sleep(1)
    else:
        print("\n[MERGE] Nenhuma playlist duplicada encontrada.")

    # Clean deleted videos from all playlists
    print(f"\n[LIMPEZA] Removendo videos excluidos das playlists...")
    total_cleaned = 0
    for pid, detail in playlist_details.items():
        deleted_items = detail.get("deleted_items", [])
        if not deleted_items:
            continue

        print(f"  Playlist '{detail['title']}': {len(deleted_items)} videos excluidos")
        for item in deleted_items:
            try:
                remove_playlist_item(youtube, item["playlist_item_id"])
                total_cleaned += 1
                print(f"    [REMOVIDO] {item['video_id']} (posicao {item['position']})")
                time.sleep(0.3)
            except Exception as e:
                print(f"    [ERRO] {item['video_id']}: {str(e)[:80]}")

    print(f"\n  Total de entradas fantasma removidas: {total_cleaned}")
    return total_cleaned


# =============================================================
# PHASE 3: VERIFY AND UPDATE PROGRESS
# =============================================================

def verify_and_update_progress(youtube, missing_ids):
    """Update upload_progress.json removing deleted videos."""
    print("\n" + "=" * 60)
    print("  FASE 3: VERIFICAR E ATUALIZAR PROGRESS")
    print("=" * 60)

    if not missing_ids:
        print("\n[OK] Todos os videos do progress existem no YouTube.")
        return 0

    progress = load_progress()
    uploaded = progress.get("uploaded", {})

    # Find keys to remove
    keys_to_remove = []
    for key, entry in uploaded.items():
        if entry.get("video_id") in missing_ids:
            keys_to_remove.append(key)

    print(f"\n[PROGRESS] {len(keys_to_remove)} videos deletados encontrados no progress:")
    for key in keys_to_remove:
        entry = uploaded[key]
        print(f"  - {key}: {entry.get('title', '?')[:60]} (ID: {entry.get('video_id')})")

    # Remove them
    for key in keys_to_remove:
        del uploaded[key]

    # Save updated progress
    progress["uploaded"] = uploaded
    # Also clear playlist_failures since we'll rebuild via API
    progress["playlist_failures"] = []
    save_progress(progress)

    print(f"\n[SALVO] {len(keys_to_remove)} entradas removidas de {PROGRESS_FILE}")
    print(f"  Videos restantes no progress: {len(uploaded)}")

    return len(keys_to_remove)


# =============================================================
# HELPERS
# =============================================================

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"uploaded": {}}
    return {"uploaded": {}}


def save_progress(progress):
    import shutil
    tmp_path = PROGRESS_FILE + ".tmp"
    bak_path = PROGRESS_FILE + ".bak"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    if os.path.exists(PROGRESS_FILE):
        shutil.copy2(PROGRESS_FILE, bak_path)
    os.replace(tmp_path, PROGRESS_FILE)


def save_report(report):
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n[REPORT] Relatorio salvo em {REPORT_FILE}")


# =============================================================
# MAIN
# =============================================================

def main():
    parser = argparse.ArgumentParser(description="YouTube Playlist Manager")
    parser.add_argument("--analyze", action="store_true", help="Apenas analisa (sem modificar)")
    parser.add_argument("--merge", action="store_true", help="Merge duplicatas + limpa excluidos")
    parser.add_argument("--verify", action="store_true", help="Verifica videos no progress e remove deletados")
    parser.add_argument("--full", action="store_true", help="Tudo: analyze + merge + verify")
    args = parser.parse_args()

    if not any([args.analyze, args.merge, args.verify, args.full]):
        parser.print_help()
        print("\nExemplo: python youtube_playlist_manager.py --full")
        return

    print("=" * 60)
    print("  YOUTUBE PLAYLIST MANAGER")
    print("  Portfolio Savylla Adryan")
    print("=" * 60)

    youtube = get_youtube_service()
    print("[OK] Conectado a YouTube Data API v3")

    # Always analyze first
    report, duplicates, playlist_details, all_playlists = analyze_channel(youtube)
    save_report(report)

    missing_ids = set(report.get("missing_video_ids", []))

    if args.merge or args.full:
        if duplicates or any(d.get("deleted", 0) > 0 for d in playlist_details.values()):
            print("\n[CONFIRMAR] Deseja prosseguir com merge e limpeza? (s/n): ", end="", flush=True)
            confirm = input().strip().lower()
            if confirm in ("s", "sim", "y", "yes"):
                merge_and_clean(youtube, duplicates, playlist_details, all_playlists)
            else:
                print("[CANCELADO] Merge e limpeza cancelados.")
        else:
            print("\n[OK] Nenhuma duplicata ou video excluido para limpar.")

    if args.verify or args.full:
        if missing_ids:
            print(f"\n[CONFIRMAR] Remover {len(missing_ids)} videos deletados do progress? (s/n): ", end="", flush=True)
            confirm = input().strip().lower()
            if confirm in ("s", "sim", "y", "yes"):
                verify_and_update_progress(youtube, missing_ids)
            else:
                print("[CANCELADO] Progress nao foi alterado.")
        else:
            print("\n[OK] Todos os videos do progress existem no YouTube.")

    print("\n" + "=" * 60)
    print("  CONCLUIDO")
    print("=" * 60)


if __name__ == "__main__":
    main()
