"""
fix_p0.py
---------
Apply P0 fixes to the Savylla Adryan YouTube channel via Data API v3.

Two categories:
    1) Change 3 videos from private -> unlisted (videos.update).
    2) Create 17 missing "Portfolio - {Cliente}" playlists (playlists.insert,
       privacyStatus=unlisted).

Idempotent:
    - Videos already unlisted -> SKIP.
    - Playlists with the exact title already existing on the channel -> SKIP.

Modes:
    python fix_p0.py --dry-run   # plan only, no writes
    python fix_p0.py             # execute writes

OAuth:
    - scope: https://www.googleapis.com/auth/youtube.force-ssl
    - token cached at youtube_api_token_rw.json (kept separate from the
      read-only youtube_api_token.json).

Output:
    fix_p0_report.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 on stdout/stderr (Windows console default is cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---- Dependencies -----------------------------------------------------------

REQUIRED = [
    "google-api-python-client",
    "google-auth-oauthlib",
    "google-auth-httplib2",
]


def _ensure_deps() -> None:
    missing = []
    try:
        import googleapiclient  # noqa: F401
    except ImportError:
        missing.append("google-api-python-client")
    try:
        import google_auth_oauthlib  # noqa: F401
    except ImportError:
        missing.append("google-auth-oauthlib")
    try:
        import google.auth.transport.requests  # noqa: F401
    except ImportError:
        missing.append("google-auth-httplib2")
    if missing:
        import subprocess

        print(f"[deps] Installing missing packages: {missing}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", *REQUIRED]
        )


_ensure_deps()

from google.auth.transport.requests import Request  # noqa: E402
from google.oauth2.credentials import Credentials  # noqa: E402
from google_auth_oauthlib.flow import InstalledAppFlow  # noqa: E402
from googleapiclient.discovery import build  # noqa: E402
from googleapiclient.errors import HttpError  # noqa: E402


# ---- Config -----------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN_CACHE = ROOT / "youtube_api_token_rw.json"
REPORT_PATH = ROOT / "fix_p0_report.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

# ---- Canonical P0 data ------------------------------------------------------

VIDEOS_TO_UNLIST = [
    {
        "id": "BUQWZssKsKk",
        "title": "Livelo 010 Leticia Pedro pillarbox",
    },
    {
        "id": "pzBSJ7FSpZc",
        "title": "Faculdade Estacio - Fernanda Penna - ESTACIO v4 36s",
    },
    {
        "id": "y_DVjSTJGkA",
        "title": (
            "Bravecto - Loretta Martins - BRAVECTO 2025 Brasil II v4 26s"
        ),
    },
]

# EXACT client names (with accents / punctuation preserved). Order matters only
# for logging; idempotency is by title.
CLIENTS_NEEDING_PLAYLIST = [
    "Cassino.Bet",
    "Agibank",
    "Gama",
    "Bullsbet",
    "Reals Bet",
    "Nestl\u00e9 / Kitkat",        # Nestle / Kitkat
    "Nestl\u00e9 / Nutren",        # Nestle / Nutren
    "Dominos",
    "Bradesco",
    "Sorriso",
    "Tramontina",
    "Softys Kitchen",
    "Aiqfome",
    "Philco Brit\u00e2nia",        # Philco Britania
    "Mycon",
    "Grupo Carrefour",
    "Atacad\u00e3o",               # Atacadao
]


def playlist_title(client: str) -> str:
    return f"Portfolio - {client}"


# ---- Retry wrapper ----------------------------------------------------------


def execute_with_retry(request, op_name: str, max_attempts: int = 3):
    """Execute a googleapiclient request with exponential backoff on 429/5xx.

    Returns (result, error_string_or_None).
    """
    attempt = 0
    last_err: str | None = None
    while True:
        attempt += 1
        try:
            return request.execute(), None
        except HttpError as e:
            status = getattr(e.resp, "status", None)
            content = getattr(e, "content", b"") or b""
            try:
                payload = json.loads(content.decode("utf-8", errors="replace"))
                reason = (
                    payload.get("error", {})
                    .get("errors", [{}])[0]
                    .get("reason", "")
                )
                message = payload.get("error", {}).get("message", "")
            except Exception:
                reason = ""
                message = content.decode("utf-8", errors="replace")

            last_err = f"HTTP {status} reason={reason} message={message}"

            # Hard-fail on quota
            if status == 403 and "quota" in reason.lower():
                return None, f"QUOTA_EXCEEDED: {last_err}"

            if status in (429, 500, 502, 503, 504) and attempt < max_attempts:
                delay = 2 ** attempt
                print(
                    f"[retry] {op_name} HTTP {status} attempt {attempt} "
                    f"-> sleep {delay}s"
                )
                time.sleep(delay)
                continue

            return None, last_err
        except Exception as e:  # network/ssl
            last_err = f"{type(e).__name__}: {e}"
            if attempt < max_attempts:
                delay = 2 ** attempt
                print(
                    f"[retry] {op_name} exception attempt {attempt} "
                    f"-> sleep {delay}s ({last_err})"
                )
                time.sleep(delay)
                continue
            return None, last_err


# ---- OAuth ------------------------------------------------------------------


def get_credentials() -> Credentials:
    creds: Credentials | None = None

    if TOKEN_CACHE.exists():
        try:
            creds = Credentials.from_authorized_user_file(
                str(TOKEN_CACHE), SCOPES
            )
        except Exception as e:
            print(f"[oauth] cached RW token unreadable ({e}); re-authenticating.")
            creds = None

    if creds and creds.valid:
        print(f"[oauth] using cached RW token at {TOKEN_CACHE.name}")
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            TOKEN_CACHE.write_text(creds.to_json(), encoding="utf-8")
            print("[oauth] refreshed RW token")
            return creds
        except Exception as e:
            print(f"[oauth] refresh failed ({e}); starting new flow.")

    if not CLIENT_SECRET.exists():
        raise FileNotFoundError(
            f"client_secret.json not found at {CLIENT_SECRET}"
        )

    print("[oauth] launching local browser for authorization (scope=force-ssl)...")
    print("[oauth] If the browser does not open automatically, copy the URL "
          "printed below into a browser where you are logged in as the channel "
          "owner.")
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    TOKEN_CACHE.write_text(creds.to_json(), encoding="utf-8")
    print(f"[oauth] RW token cached at {TOKEN_CACHE}")
    return creds


# ---- Fix phases -------------------------------------------------------------


def fix_visibility(youtube, dry_run: bool) -> list[dict]:
    results: list[dict] = []
    print()
    print("=" * 70)
    print(f"Phase 1: visibility fix ({len(VIDEOS_TO_UNLIST)} videos)")
    print("=" * 70)

    for v in VIDEOS_TO_UNLIST:
        vid = v["id"]
        title = v["title"]
        entry: dict = {
            "id": vid,
            "title": title,
            "before": None,
            "after": None,
            "status": "FAIL",
            "note": "",
        }

        # 1. Read current status
        req = youtube.videos().list(id=vid, part="status,snippet")
        resp, err = execute_with_retry(req, "videos.list")
        if err:
            entry["note"] = f"list error: {err}"
            print(f"[fix-visibility] {vid} {title[:40]:<40} FAIL {entry['note']}")
            results.append(entry)
            continue
        items = resp.get("items", [])
        if not items:
            entry["note"] = "video not found / not owned"
            print(f"[fix-visibility] {vid} {title[:40]:<40} FAIL {entry['note']}")
            results.append(entry)
            continue

        item = items[0]
        current_status = item.get("status", {})
        snippet = item.get("snippet", {})
        current_privacy = current_status.get("privacyStatus")
        entry["before"] = current_privacy
        entry["after"] = current_privacy  # default if skip/fail
        # Prefer the actual channel title
        entry["title"] = snippet.get("title", title)

        if current_privacy == "unlisted":
            entry["status"] = "SKIP"
            entry["note"] = "already unlisted"
            entry["after"] = "unlisted"
            print(
                f"[fix-visibility] {vid} {entry['title'][:40]:<40} "
                f"{current_privacy} -> unlisted SKIP (already unlisted)"
            )
            results.append(entry)
            continue

        if dry_run:
            entry["status"] = "OK"
            entry["after"] = "unlisted"
            entry["note"] = "dry-run"
            print(
                f"[fix-visibility] {vid} {entry['title'][:40]:<40} "
                f"{current_privacy} -> unlisted DRY-RUN"
            )
            results.append(entry)
            continue

        # 2. Patch status.privacyStatus
        new_status = dict(current_status)
        new_status["privacyStatus"] = "unlisted"
        body = {"id": vid, "status": new_status}

        req = youtube.videos().update(part="status", body=body)
        resp, err = execute_with_retry(req, "videos.update")
        if err:
            entry["note"] = f"update error: {err}"
            print(
                f"[fix-visibility] {vid} {entry['title'][:40]:<40} "
                f"{current_privacy} -> unlisted FAIL {entry['note']}"
            )
            results.append(entry)
            continue

        new_privacy = resp.get("status", {}).get("privacyStatus", "unlisted")
        entry["after"] = new_privacy
        entry["status"] = "OK"
        entry["note"] = "updated"
        print(
            f"[fix-visibility] {vid} {entry['title'][:40]:<40} "
            f"{current_privacy} -> {new_privacy} OK"
        )
        results.append(entry)

    return results


def fetch_existing_playlist_titles(youtube) -> dict[str, str]:
    """Return {title: playlist_id} for all playlists owned by the account."""
    titles: dict[str, str] = {}
    page_token: str | None = None
    while True:
        req = youtube.playlists().list(
            part="id,snippet",
            mine=True,
            maxResults=50,
            pageToken=page_token,
        )
        resp, err = execute_with_retry(req, "playlists.list")
        if err:
            raise RuntimeError(f"playlists.list failed: {err}")
        for item in resp.get("items", []):
            t = item.get("snippet", {}).get("title", "")
            titles[t] = item["id"]
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return titles


def create_playlists(youtube, dry_run: bool) -> list[dict]:
    results: list[dict] = []
    print()
    print("=" * 70)
    print(f"Phase 2: playlist creation ({len(CLIENTS_NEEDING_PLAYLIST)} clients)")
    print("=" * 70)

    print("[playlists] fetching existing playlists for idempotency check...")
    try:
        existing = fetch_existing_playlist_titles(youtube)
        print(f"[playlists] found {len(existing)} existing playlists on channel")
    except RuntimeError as e:
        print(f"[playlists] FATAL: {e}")
        # Mark every target as FAIL
        for client in CLIENTS_NEEDING_PLAYLIST:
            results.append({
                "title": playlist_title(client),
                "id": None,
                "status": "FAIL",
                "note": f"could not list existing playlists: {e}",
            })
        return results

    for client in CLIENTS_NEEDING_PLAYLIST:
        title = playlist_title(client)
        entry: dict = {
            "title": title,
            "id": None,
            "status": "FAIL",
            "note": "",
        }

        if title in existing:
            entry["id"] = existing[title]
            entry["status"] = "SKIP"
            entry["note"] = "already exists"
            print(f"[create-playlist] {title:<45} SKIP (id={entry['id']})")
            results.append(entry)
            continue

        if dry_run:
            entry["status"] = "OK"
            entry["note"] = "dry-run"
            print(f"[create-playlist] {title:<45} DRY-RUN")
            results.append(entry)
            continue

        body = {
            "snippet": {
                "title": title,
                "description": f"Portfolio automatizado - {client}",
                "defaultLanguage": "pt-BR",
            },
            "status": {"privacyStatus": "unlisted"},
        }

        req = youtube.playlists().insert(part="snippet,status", body=body)
        resp, err = execute_with_retry(req, "playlists.insert")
        if err:
            entry["note"] = f"insert error: {err}"
            print(f"[create-playlist] {title:<45} FAIL {entry['note']}")
            results.append(entry)
            continue

        entry["id"] = resp.get("id")
        entry["status"] = "OK"
        entry["note"] = "created"
        print(f"[create-playlist] {title:<45} OK (id={entry['id']})")
        results.append(entry)

    return results


# ---- Report -----------------------------------------------------------------


def write_report(mode: str, vis: list[dict], pls: list[dict]) -> None:
    vis_ok = sum(1 for v in vis if v["status"] == "OK")
    vis_skip = sum(1 for v in vis if v["status"] == "SKIP")
    vis_fail = sum(1 for v in vis if v["status"] == "FAIL")
    pl_ok = sum(1 for p in pls if p["status"] == "OK")
    pl_skip = sum(1 for p in pls if p["status"] == "SKIP")
    pl_fail = sum(1 for p in pls if p["status"] == "FAIL")

    errors = []
    for v in vis:
        if v["status"] == "FAIL":
            errors.append(f"video {v['id']}: {v.get('note', '')}")
    for p in pls:
        if p["status"] == "FAIL":
            errors.append(f"playlist {p['title']}: {p.get('note', '')}")

    report = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "visibility_fixed": vis,
        "playlists_created": pls,
        "summary": {
            "visibility_ok": vis_ok,
            "visibility_skip": vis_skip,
            "visibility_fail": vis_fail,
            "playlists_ok": pl_ok,
            "playlists_skip": pl_skip,
            "playlists_fail": pl_fail,
            "errors": errors,
        },
    }

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"mode:                 {mode}")
    print(
        f"visibility:           OK={vis_ok}  SKIP={vis_skip}  FAIL={vis_fail}"
    )
    print(
        f"playlists:            OK={pl_ok}   SKIP={pl_skip}   FAIL={pl_fail}"
    )
    if errors:
        print("errors:")
        for e in errors:
            print(f"  - {e}")
    print(f"report:               {REPORT_PATH}")


# ---- Main -------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply P0 fixes to the Savylla Adryan YouTube channel."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan only, no writes.",
    )
    args = parser.parse_args()

    mode = "dry-run" if args.dry_run else "live"

    print("=" * 70)
    print(f"fix_p0.py  (mode={mode})")
    print("=" * 70)
    print(f"[paths] client_secret = {CLIENT_SECRET}")
    print(f"[paths] token_cache   = {TOKEN_CACHE}")
    print(f"[paths] report        = {REPORT_PATH}")
    print(f"[targets] videos      = {len(VIDEOS_TO_UNLIST)}")
    print(f"[targets] playlists   = {len(CLIENTS_NEEDING_PLAYLIST)}")

    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)

    vis = fix_visibility(youtube, dry_run=args.dry_run)
    pls = create_playlists(youtube, dry_run=args.dry_run)

    write_report(mode, vis, pls)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback

        print("\n[FATAL] Unhandled exception:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
