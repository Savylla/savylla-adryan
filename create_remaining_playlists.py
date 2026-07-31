"""
create_remaining_playlists.py
------------------------------
Creates the 5 playlists that failed with HTTP 429 in fix_p0.py.
Uses long spacing (90s between inserts) and NO burst retry.
Idempotent: skips if playlist already exists.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PROJECT = Path(__file__).parent
TOKEN = PROJECT / "youtube_api_token_rw.json"

REMAINING = [
    "Softys Kitchen",
    "Aiqfome",
    "Philco Britânia",
    "Mycon",
    "Grupo Carrefour",
]

SPACING_SECONDS = 90


def load_creds() -> Credentials:
    if not TOKEN.exists():
        raise FileNotFoundError(f"RW token missing: {TOKEN}")
    data = json.loads(TOKEN.read_text(encoding="utf-8"))
    return Credentials.from_authorized_user_info(data)


def list_existing_titles(yt) -> set[str]:
    titles: set[str] = set()
    page = None
    while True:
        resp = yt.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=page,
        ).execute()
        for item in resp.get("items", []):
            titles.add(item["snippet"]["title"])
        page = resp.get("nextPageToken")
        if not page:
            return titles


def create_playlist(yt, title: str) -> dict:
    body = {
        "snippet": {
            "title": title,
            "description": f"Portfolio automatizado - {title.removeprefix('Portfolio - ')}",
            "defaultLanguage": "pt-BR",
        },
        "status": {"privacyStatus": "unlisted"},
    }
    try:
        resp = yt.playlists().insert(part="snippet,status", body=body).execute()
        return {"status": "OK", "id": resp["id"]}
    except HttpError as e:
        return {"status": "FAIL", "error": f"HTTP {e.resp.status}: {e}"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}


def main() -> int:
    print("=" * 70)
    print("create_remaining_playlists.py (spaced mode, 90s between inserts)")
    print("=" * 70)

    creds = load_creds()
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)

    print("[playlists] fetching existing titles for idempotency...")
    existing = list_existing_titles(yt)
    print(f"[playlists] {len(existing)} existing titles")

    results = []
    for i, client in enumerate(REMAINING):
        title = f"Portfolio - {client}"
        if title in existing:
            print(f"[{i+1}/{len(REMAINING)}] {title:<35} SKIP (already exists)")
            results.append({"title": title, "status": "SKIP"})
            continue

        print(f"[{i+1}/{len(REMAINING)}] {title:<35} creating...")
        result = create_playlist(yt, title)
        if result["status"] == "OK":
            print(f"    -> OK id={result['id']}")
        else:
            print(f"    -> FAIL {result.get('error')}")
        results.append({"title": title, **result})

        # space the next call (except after last)
        if i < len(REMAINING) - 1:
            print(f"    (sleeping {SPACING_SECONDS}s before next)")
            time.sleep(SPACING_SECONDS)

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    ok = sum(1 for r in results if r["status"] == "OK")
    skip = sum(1 for r in results if r["status"] == "SKIP")
    fail = sum(1 for r in results if r["status"] == "FAIL")
    print(f"OK={ok}  SKIP={skip}  FAIL={fail}")
    for r in results:
        marker = {"OK": "OK  ", "SKIP": "SKIP", "FAIL": "FAIL"}[r["status"]]
        print(f"  [{marker}] {r['title']}")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
