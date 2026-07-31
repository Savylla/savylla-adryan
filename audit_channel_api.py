"""
audit_channel_api.py
--------------------
YouTube channel auditor using the official Data API v3.

Extracts the full state of the authenticated channel:
- All uploaded videos (with title, description, privacy, duration, is_short flag)
- All playlists (with items / video_ids)
- Cross-references videos -> playlists membership

Output: channel_state.json in the project root.

OAuth:
    - Reads client_secret.json
    - Caches token in youtube_api_token.json

Run:
    python audit_channel_api.py
"""

from __future__ import annotations

import json
import os
import re
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

# ---- Dependencies (install if missing) --------------------------------------

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
TOKEN_CACHE = ROOT / "youtube_api_token.json"
OUTPUT = ROOT / "channel_state.json"
PARTIAL = ROOT / "channel_state_partial.json"

# force-ssl includes read+write; readonly is enough for auditing but we request
# both so the same token can be reused by the future editor script.
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
]

SHORT_HINT_RE = re.compile(r"#shorts?\b", re.IGNORECASE)

# Quota cost table (approximate per Data API docs)
QUOTA_COSTS = {
    "channels.list": 1,
    "playlistItems.list": 1,
    "videos.list": 1,
    "playlists.list": 1,
}

# ---- Quota tracker ----------------------------------------------------------


class QuotaMeter:
    def __init__(self) -> None:
        self.total = 0
        self.breakdown: dict[str, int] = {}

    def charge(self, op: str) -> None:
        cost = QUOTA_COSTS.get(op, 1)
        self.total += cost
        self.breakdown[op] = self.breakdown.get(op, 0) + cost


QUOTA = QuotaMeter()


# ---- Retry wrapper ----------------------------------------------------------


def execute_with_retry(request, op_name: str, max_attempts: int = 5):
    """Execute a googleapiclient request with exponential backoff on 429/5xx."""
    attempt = 0
    while True:
        attempt += 1
        try:
            result = request.execute()
            QUOTA.charge(op_name)
            return result
        except HttpError as e:
            status = getattr(e.resp, "status", None)
            # Quota exceeded -> abort immediately
            if status == 403:
                content = getattr(e, "content", b"") or b""
                try:
                    payload = json.loads(content.decode("utf-8", errors="replace"))
                    reason = (
                        payload.get("error", {})
                        .get("errors", [{}])[0]
                        .get("reason", "")
                    )
                except Exception:
                    reason = ""
                if "quota" in reason.lower():
                    raise RuntimeError(
                        f"YouTube API quota exceeded on {op_name}. "
                        f"Used {QUOTA.total} units. Reason={reason}"
                    ) from e
            if status in (429, 500, 502, 503, 504) and attempt < max_attempts:
                delay = min(2 ** attempt, 32)
                print(
                    f"[retry] {op_name} HTTP {status} attempt {attempt} "
                    f"-> sleep {delay}s"
                )
                time.sleep(delay)
                continue
            raise


# ---- OAuth ------------------------------------------------------------------


def get_credentials() -> Credentials:
    creds: Credentials | None = None

    if TOKEN_CACHE.exists():
        try:
            creds = Credentials.from_authorized_user_file(
                str(TOKEN_CACHE), SCOPES
            )
        except Exception as e:
            print(f"[oauth] cached token unreadable ({e}); re-authenticating.")
            creds = None

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            TOKEN_CACHE.write_text(creds.to_json(), encoding="utf-8")
            return creds
        except Exception as e:
            print(f"[oauth] refresh failed ({e}); starting new flow.")

    if not CLIENT_SECRET.exists():
        raise FileNotFoundError(f"client_secret.json not found at {CLIENT_SECRET}")

    print("[oauth] launching local browser for authorization...")
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    # port=0 -> OS picks a free port; matches the http://localhost redirect URI
    creds = flow.run_local_server(port=0, prompt="consent")
    TOKEN_CACHE.write_text(creds.to_json(), encoding="utf-8")
    print(f"[oauth] token cached at {TOKEN_CACHE}")
    return creds


# ---- Helpers ----------------------------------------------------------------


def iso_duration_to_seconds(iso: str) -> int:
    """Convert ISO 8601 duration (PT#H#M#S) to total seconds."""
    if not iso:
        return 0
    m = re.match(
        r"^P(?:(?P<d>\d+)D)?T?(?:(?P<h>\d+)H)?(?:(?P<mi>\d+)M)?(?:(?P<s>\d+)S)?$",
        iso,
    )
    if not m:
        return 0
    d = int(m.group("d") or 0)
    h = int(m.group("h") or 0)
    mi = int(m.group("mi") or 0)
    s = int(m.group("s") or 0)
    return d * 86400 + h * 3600 + mi * 60 + s


def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def save_partial(state: dict) -> None:
    PARTIAL.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---- Extraction steps --------------------------------------------------------


def fetch_channel(youtube) -> dict:
    req = youtube.channels().list(
        part="id,snippet,contentDetails,statistics",
        mine=True,
    )
    resp = execute_with_retry(req, "channels.list")
    items = resp.get("items", [])
    if not items:
        raise RuntimeError("No channel returned for the authenticated user.")
    ch = items[0]
    snippet = ch.get("snippet", {})
    content = ch.get("contentDetails", {})
    stats = ch.get("statistics", {})
    return {
        "id": ch["id"],
        "title": snippet.get("title"),
        "custom_url": snippet.get("customUrl"),
        "description": snippet.get("description"),
        "published_at": snippet.get("publishedAt"),
        "uploads_playlist_id": content.get("relatedPlaylists", {}).get("uploads"),
        "statistics": {
            "view_count": stats.get("viewCount"),
            "subscriber_count": stats.get("subscriberCount"),
            "video_count": stats.get("videoCount"),
        },
    }


def fetch_upload_video_ids(youtube, uploads_playlist_id: str) -> list[str]:
    video_ids: list[str] = []
    page_token: str | None = None
    while True:
        req = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=page_token,
        )
        resp = execute_with_retry(req, "playlistItems.list")
        for item in resp.get("items", []):
            vid = item.get("contentDetails", {}).get("videoId")
            if vid:
                video_ids.append(vid)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return video_ids


def fetch_video_details(youtube, video_ids: list[str]) -> list[dict]:
    out: list[dict] = []
    total = len(video_ids)
    processed = 0
    for batch in chunked(video_ids, 50):
        req = youtube.videos().list(
            part="snippet,status,contentDetails",
            id=",".join(batch),
            maxResults=50,
        )
        resp = execute_with_retry(req, "videos.list")
        for item in resp.get("items", []):
            snippet = item.get("snippet", {})
            status = item.get("status", {})
            cdet = item.get("contentDetails", {})
            duration_iso = cdet.get("duration") or ""
            duration_s = iso_duration_to_seconds(duration_iso)
            description = snippet.get("description", "") or ""
            # Short heuristic: <=60s AND (#shorts hint in title/desc OR very short)
            title = snippet.get("title", "") or ""
            has_shorts_tag = bool(
                SHORT_HINT_RE.search(description) or SHORT_HINT_RE.search(title)
            )
            is_short = duration_s > 0 and duration_s <= 60 and (
                has_shorts_tag or duration_s <= 60
            )
            out.append(
                {
                    "id": item["id"],
                    "title": title,
                    "description": description,
                    "published_at": snippet.get("publishedAt"),
                    "channel_id": snippet.get("channelId"),
                    "tags": snippet.get("tags", []),
                    "category_id": snippet.get("categoryId"),
                    "privacy_status": status.get("privacyStatus"),
                    "made_for_kids": status.get("madeForKids"),
                    "self_declared_made_for_kids": status.get(
                        "selfDeclaredMadeForKids"
                    ),
                    "upload_status": status.get("uploadStatus"),
                    "license": status.get("license"),
                    "duration_iso": duration_iso,
                    "duration_seconds": duration_s,
                    "is_short": bool(is_short),
                    "default_language": snippet.get("defaultLanguage"),
                    "default_audio_language": snippet.get("defaultAudioLanguage"),
                    "in_playlists": [],  # filled later
                }
            )
        processed += len(batch)
        if processed % 50 == 0 or processed >= total:
            print(f"[videos] details fetched {processed}/{total}")
    return out


def fetch_playlists(youtube) -> list[dict]:
    playlists: list[dict] = []
    page_token: str | None = None
    while True:
        req = youtube.playlists().list(
            part="id,snippet,status,contentDetails",
            mine=True,
            maxResults=50,
            pageToken=page_token,
        )
        resp = execute_with_retry(req, "playlists.list")
        for item in resp.get("items", []):
            snippet = item.get("snippet", {})
            status = item.get("status", {})
            cdet = item.get("contentDetails", {})
            playlists.append(
                {
                    "id": item["id"],
                    "title": snippet.get("title"),
                    "description": snippet.get("description", "") or "",
                    "published_at": snippet.get("publishedAt"),
                    "privacy_status": status.get("privacyStatus"),
                    "item_count": cdet.get("itemCount", 0),
                    "video_ids": [],  # filled next
                }
            )
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return playlists


def fetch_playlist_items(youtube, playlist_id: str) -> list[str]:
    ids: list[str] = []
    page_token: str | None = None
    while True:
        req = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token,
        )
        resp = execute_with_retry(req, "playlistItems.list")
        for item in resp.get("items", []):
            vid = item.get("contentDetails", {}).get("videoId")
            if vid:
                ids.append(vid)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return ids


# ---- Main -------------------------------------------------------------------


def main() -> int:
    print("=" * 70)
    print("YouTube Channel Audit (Data API v3)")
    print("=" * 70)
    print(f"[paths] client_secret = {CLIENT_SECRET}")
    print(f"[paths] token_cache   = {TOKEN_CACHE}")
    print(f"[paths] output        = {OUTPUT}")
    print()

    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)

    # 1) Channel metadata
    print("[step 1/5] fetching channel metadata...")
    channel = fetch_channel(youtube)
    uploads_pl = channel["uploads_playlist_id"]
    print(
        f"  -> {channel['title']} (id={channel['id']}, "
        f"uploads_playlist={uploads_pl})"
    )

    # 2) All upload video IDs
    print("[step 2/5] fetching upload video ids (paginating)...")
    video_ids = fetch_upload_video_ids(youtube, uploads_pl)
    print(f"  -> {len(video_ids)} video ids collected")

    # 3) Video details in batches of 50
    print("[step 3/5] fetching video details (batches of 50)...")
    videos = fetch_video_details(youtube, video_ids)
    # Partial save checkpoint after video extraction
    save_partial(
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "channel": channel,
            "videos": videos,
            "playlists": [],
            "partial": True,
        }
    )
    print(f"  -> partial saved to {PARTIAL.name}")

    # 4) Playlists
    print("[step 4/5] fetching playlists...")
    playlists = fetch_playlists(youtube)
    print(f"  -> {len(playlists)} playlists found")

    # 5) Playlist items + cross-reference
    print("[step 5/5] fetching playlist items...")
    video_index: dict[str, dict] = {v["id"]: v for v in videos}
    for idx, pl in enumerate(playlists, start=1):
        ids = fetch_playlist_items(youtube, pl["id"])
        pl["video_ids"] = ids
        for vid in ids:
            if vid in video_index:
                video_index[vid]["in_playlists"].append(pl["title"])
        print(
            f"  [{idx}/{len(playlists)}] {pl['title'][:48]:<48} items={len(ids)}"
        )

    # Final stats
    total_shorts = sum(1 for v in videos if v.get("is_short"))
    state = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "channel": {
            "id": channel["id"],
            "title": channel["title"],
            "custom_url": channel["custom_url"],
            "description": channel["description"],
            "published_at": channel["published_at"],
            "uploads_playlist_id": channel["uploads_playlist_id"],
            "statistics": channel["statistics"],
        },
        "stats": {
            "total_videos": len(videos),
            "total_playlists": len(playlists),
            "total_shorts": total_shorts,
            "quota_used": QUOTA.total,
            "quota_breakdown": QUOTA.breakdown,
        },
        "videos": videos,
        "playlists": playlists,
    }

    OUTPUT.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Clean up partial if final succeeded
    try:
        if PARTIAL.exists():
            os.remove(PARTIAL)
    except OSError:
        pass

    print()
    print("=" * 70)
    print("Audit complete")
    print("=" * 70)
    print(f"output:        {OUTPUT}")
    print(f"videos:        {len(videos)}")
    print(f"playlists:     {len(playlists)}")
    print(f"shorts:        {total_shorts}")
    print(f"quota used:    {QUOTA.total} units")
    print(f"quota detail:  {QUOTA.breakdown}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        # Quota exceeded / domain errors - print clean message
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        import traceback

        print("\n[FATAL] Unhandled exception:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
