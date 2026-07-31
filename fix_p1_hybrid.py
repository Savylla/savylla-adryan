"""
fix_p1_hybrid.py
----------------
P1 - Attach 147 orphan videos to their correct Portfolio playlists.

Strategy: HYBRID
    Phase API   -> Data API v3 playlistItems.insert (primary).
    Phase Sel   -> Selenium (YouTube Studio UI) as fallback when the API
                   chokes on 429 / quotaExceeded / 403 rate-limits.

Source of truth:
    audit_delta_report.json -> missing_playlist (147 items).

Flow:
    0. Refresh {title -> playlist_id} via playlists.list(mine=True).
    1. Pre-fetch every Portfolio playlist's current videoIds
       (playlistItems.list, paginated) to enforce idempotency.
    2. Phase API: playlistItems.insert per (video_id, playlist_id).
       Stop the entire API phase on the first quota/rate-limit signal and
       mark the remaining targets as pending_selenium.
    3. Phase Selenium: only runs if pending_selenium is non-empty.
       Reuses the dialog-based pattern from fix_playlists_final.py.
    4. Emit fix_p1_report.json with per-phase breakdown.

Modes:
    python fix_p1_hybrid.py --dry-run     # plan only, no writes
    python fix_p1_hybrid.py               # live
    python fix_p1_hybrid.py --skip-api    # go straight to Selenium
    python fix_p1_hybrid.py --skip-sel    # API only, no fallback

OAuth:
    scope https://www.googleapis.com/auth/youtube.force-ssl, token cached at
    youtube_api_token_rw.json.

Exit codes:
    0 = all targets OK (or dry-run plan printed).
    2 = finished but some failures remain (see report).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 on stdout/stderr (Windows console default is cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import functools
print = functools.partial(print, flush=True)  # noqa: A001

# ---- Dependency check -------------------------------------------------------

REQUIRED_GOOGLE = [
    "google-api-python-client",
    "google-auth-oauthlib",
    "google-auth-httplib2",
]


def _ensure_deps() -> None:
    missing: list[str] = []
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
        print(f"[deps] installing missing packages: {missing}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", *REQUIRED_GOOGLE]
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
DELTA_REPORT = ROOT / "audit_delta_report.json"
REPORT_PATH = ROOT / "fix_p1_report.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

CHROME_DEBUG_PORT = 9555
SELENIUM_DELAY = 5  # seconds between videos in the Selenium phase


# ---- Retry / quota helpers --------------------------------------------------


class QuotaSignal(Exception):
    """Raised when the API reports quotaExceeded or rate-limit exhaustion.

    Caught by the phase driver to flip remaining targets into
    pending_selenium and stop hammering the API.
    """


def _parse_http_error(e: HttpError) -> tuple[int | None, str, str]:
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
    return status, reason, message


def _is_quota_error(status: int | None, reason: str, message: str) -> bool:
    reason_l = (reason or "").lower()
    message_l = (message or "").lower()
    if status == 403 and (
        "quota" in reason_l or "quota" in message_l
        or "ratelimit" in reason_l or "rate limit" in message_l
    ):
        return True
    if status == 429:
        return True
    return False


def execute_with_retry(
    request,
    op_name: str,
    max_attempts: int = 3,
    retry_on_rate_limit: bool = False,
):
    """Execute a googleapiclient request with exponential backoff.

    On quotaExceeded / 429 we raise QuotaSignal so the phase driver can
    short-circuit (unless retry_on_rate_limit=True, used only for read ops
    where we *must* get the data back).
    """
    attempt = 0
    last_err: str | None = None
    while True:
        attempt += 1
        try:
            return request.execute(), None
        except HttpError as e:
            status, reason, message = _parse_http_error(e)
            last_err = f"HTTP {status} reason={reason} message={message}"

            if _is_quota_error(status, reason, message):
                if retry_on_rate_limit and attempt < max_attempts:
                    delay = 2 ** attempt
                    print(
                        f"[retry] {op_name} rate-limited attempt {attempt} "
                        f"-> sleep {delay}s"
                    )
                    time.sleep(delay)
                    continue
                raise QuotaSignal(last_err)

            if status in (500, 502, 503, 504) and attempt < max_attempts:
                delay = 2 ** attempt
                print(
                    f"[retry] {op_name} HTTP {status} attempt {attempt} "
                    f"-> sleep {delay}s"
                )
                time.sleep(delay)
                continue

            return None, last_err
        except Exception as e:  # network / ssl / etc
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

    print(
        "[oauth] launching local browser for authorization "
        "(scope=youtube.force-ssl)..."
    )
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    TOKEN_CACHE.write_text(creds.to_json(), encoding="utf-8")
    print(f"[oauth] RW token cached at {TOKEN_CACHE}")
    return creds


# ---- Channel state ----------------------------------------------------------


def load_targets() -> list[dict]:
    """Load the 147 P1 targets from audit_delta_report.json."""
    if not DELTA_REPORT.exists():
        raise FileNotFoundError(f"delta report not found: {DELTA_REPORT}")
    data = json.loads(DELTA_REPORT.read_text(encoding="utf-8"))
    items = data.get("missing_playlist") or []
    # Normalize
    out: list[dict] = []
    for it in items:
        vid = it.get("video_id")
        pl_title = it.get("expected_playlist")
        if not vid or not pl_title:
            continue
        out.append({
            "video_id": vid,
            "video_title": it.get("video_title", ""),
            "expected_playlist": pl_title,
            "client": it.get("client", ""),
        })
    return out


def fetch_playlist_map(youtube) -> dict[str, str]:
    """Return {playlist_title: playlist_id} for every playlist on the channel."""
    titles: dict[str, str] = {}
    page_token: str | None = None
    page = 0
    while True:
        page += 1
        req = youtube.playlists().list(
            part="id,snippet",
            mine=True,
            maxResults=50,
            pageToken=page_token,
        )
        resp, err = execute_with_retry(
            req, "playlists.list", retry_on_rate_limit=True
        )
        if err:
            raise RuntimeError(f"playlists.list failed: {err}")
        for item in resp.get("items", []):
            t = item.get("snippet", {}).get("title", "")
            if t:
                titles[t] = item["id"]
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    print(f"[step0] fetched {len(titles)} playlists across {page} page(s)")
    return titles


def fetch_playlist_videos(
    youtube, playlist_id: str, playlist_title: str
) -> set[str]:
    """Return the set of videoIds currently in a playlist."""
    ids: set[str] = set()
    page_token: str | None = None
    while True:
        req = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token,
        )
        resp, err = execute_with_retry(
            req, f"playlistItems.list[{playlist_title}]",
            retry_on_rate_limit=True,
        )
        if err:
            # Non-quota failure: log and bail on this playlist (dedupe set
            # stays empty -> worst case we try to insert and the API tells us
            # it's already there).
            print(
                f"[warn] could not list items for playlist {playlist_title}: "
                f"{err}"
            )
            break
        for item in resp.get("items", []):
            vid = (
                item.get("contentDetails", {}).get("videoId")
            )
            if vid:
                ids.add(vid)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return ids


# ---- Phase API --------------------------------------------------------------


def api_insert_video(
    youtube, video_id: str, playlist_id: str
) -> tuple[bool, str]:
    """Insert a single video into a playlist via the Data API.

    Returns (ok, note). Raises QuotaSignal on quotaExceeded / 429.
    """
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id,
            },
        }
    }
    req = youtube.playlistItems().insert(part="snippet", body=body)
    resp, err = execute_with_retry(
        req, f"playlistItems.insert[{video_id}]"
    )
    if err:
        # Detect the "already in playlist" race condition: Data API reports
        # this as reason=playlistItemAlreadyExists or similar -- treat as OK.
        err_l = err.lower()
        if "already" in err_l and ("exists" in err_l or "member" in err_l):
            return True, "already_in_playlist"
        return False, err
    return True, "inserted"


def run_phase_api(
    youtube,
    targets: list[dict],
    playlist_map: dict[str, str],
    existing_memberships: dict[str, set[str]],
    dry_run: bool,
) -> tuple[list[dict], list[dict], list[dict]]:
    """Phase 2 executor.

    Returns (api_items, dedupe_skipped, pending_selenium).
    Every list element is a target dict enriched with status fields.
    """
    api_items: list[dict] = []
    dedupe_skipped: list[dict] = []
    pending: list[dict] = []

    total = len(targets)
    print()
    print("=" * 70)
    print(f"Phase API: playlistItems.insert ({total} targets)")
    print("=" * 70)

    quota_tripped = False
    processed = 0
    ok = 0
    failed = 0

    for idx, t in enumerate(targets, start=1):
        vid = t["video_id"]
        pl_title = t["expected_playlist"]
        pl_id = playlist_map.get(pl_title)

        entry = {
            "video_id": vid,
            "video_title": t.get("video_title", ""),
            "playlist": pl_title,
            "client": t.get("client", ""),
            "method": "api",
            "status": "FAIL",
            "note": "",
        }

        # Dedupe: already in the target playlist?
        if pl_id and vid in existing_memberships.get(pl_id, set()):
            entry["method"] = "dedupe"
            entry["status"] = "SKIP"
            entry["note"] = "already_in_playlist"
            print(f"[skip] {vid} already in {pl_title}")
            dedupe_skipped.append(entry)
            continue

        # If the API phase was already tripped, everything else goes to
        # the Selenium fallback bucket.
        if quota_tripped:
            entry["status"] = "PENDING"
            entry["note"] = "api_quota_tripped -> selenium fallback"
            pending.append(entry)
            continue

        if not pl_id:
            entry["status"] = "FAIL"
            entry["note"] = (
                f"playlist '{pl_title}' not found on channel (run fix_p0?)"
            )
            print(f"[api-add] {vid} -> {pl_title} FAIL {entry['note']}")
            api_items.append(entry)
            failed += 1
            processed += 1
            continue

        if dry_run:
            entry["status"] = "OK"
            entry["note"] = "dry-run"
            print(f"[api-add] {vid} -> {pl_title} DRY-RUN")
            api_items.append(entry)
            ok += 1
            processed += 1
            if processed % 10 == 0:
                print(
                    f"[progress] api {processed}/{total} "
                    f"ok={ok} fail={failed}"
                )
            continue

        try:
            success, note = api_insert_video(youtube, vid, pl_id)
        except QuotaSignal as qs:
            print(f"[api-add] quota / rate-limit hit: {qs}")
            print(
                "[api-add] STOP API phase -- remaining targets queued for "
                "Selenium fallback."
            )
            quota_tripped = True
            entry["status"] = "PENDING"
            entry["note"] = f"api_quota_tripped: {qs}"
            pending.append(entry)
            continue

        if success:
            entry["status"] = "OK"
            entry["note"] = note
            existing_memberships.setdefault(pl_id, set()).add(vid)
            print(f"[api-add] {vid} -> {pl_title} OK ({note})")
            ok += 1
        else:
            entry["status"] = "FAIL"
            entry["note"] = note
            print(f"[api-add] {vid} -> {pl_title} FAIL {note}")
            failed += 1

        api_items.append(entry)
        processed += 1
        if processed % 10 == 0:
            print(
                f"[progress] api {processed}/{total} "
                f"ok={ok} fail={failed}"
            )

    print(
        f"[phase-api] done: ok={ok} failed={failed} "
        f"dedupe_skipped={len(dedupe_skipped)} "
        f"pending_selenium={len(pending)}"
    )
    return api_items, dedupe_skipped, pending


# ---- Phase Selenium ---------------------------------------------------------


def _selenium_available() -> bool:
    try:
        import selenium  # noqa: F401
        return True
    except ImportError:
        return False


def _find_chrome() -> str | None:
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser("~")
        + r"\AppData\Local\Google\Chrome\Application\chrome.exe",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def _create_driver():
    """Start Chrome on the Selenium debug port with the cached profile.

    Mirrors fix_playlists_final.create_driver (lines 53-101).
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_path = _find_chrome()
    if not chrome_path:
        raise RuntimeError("chrome.exe not found on standard paths")

    custom_data_dir = os.path.join(
        os.path.expanduser("~"), "chrome_selenium_data"
    )
    os.makedirs(custom_data_dir, exist_ok=True)

    print("[browser] closing any running Chrome instances...")
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "chrome.exe"],
            capture_output=True, timeout=10,
        )
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
    print(f"[browser] starting Chrome (debug port {CHROME_DEBUG_PORT})...")
    subprocess.Popen(
        chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    # Wait for the DevTools debug port to actually accept connections
    import socket
    deadline = time.time() + 60
    port_up = False
    while time.time() < deadline:
        try:
            with socket.create_connection(
                ("127.0.0.1", CHROME_DEBUG_PORT), timeout=1
            ):
                port_up = True
                break
        except OSError:
            time.sleep(1)
    if not port_up:
        print(
            f"[browser] WARNING debug port {CHROME_DEBUG_PORT} never came up; "
            "continuing anyway"
        )
    else:
        print(f"[browser] debug port {CHROME_DEBUG_PORT} ready")
        time.sleep(3)  # give YouTube Studio a moment to render

    options = Options()
    options.add_experimental_option(
        "debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}"
    )

    driver = None
    last_exc = None
    for attempt in range(8):
        try:
            driver = webdriver.Chrome(options=options)
            try:
                driver.maximize_window()
            except Exception:
                pass
            break
        except Exception as e:
            last_exc = e
            short = str(e).splitlines()[0][:120]
            print(f"  [retry] attempt {attempt + 1}/8 ({short})")
            time.sleep(5)
    if driver is None:
        raise RuntimeError(
            f"could not attach to Chrome DevTools after 8 attempts: {last_exc}"
        )
    return driver


def _open_playlist_dialog(driver) -> bool:
    # Scroll the playlist selector into view first -- YouTube Studio lazy
    # loads it below the fold and the dropdown trigger only renders once
    # the element is visible.
    driver.execute_script("""
        var vmp = document.querySelector('ytcp-video-metadata-playlists');
        if (vmp) {
            vmp.scrollIntoView({block: 'center', behavior: 'instant'});
            return 'scrolled';
        }
        return 'no_vmp';
    """)
    time.sleep(2)

    opened = None
    for _ in range(5):
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
                var inner = vmp.querySelector(
                    'ytcp-dropdown-trigger, ytcp-text-dropdown-trigger, button'
                );
                if (inner) { inner.click(); return 'clicked_vmp'; }
                vmp.click();
                return 'clicked_vmp_direct';
            }
            return 'not_found';
        """)
        if opened and "not_found" not in str(opened):
            break
        time.sleep(1)

    if opened is None or "not_found" in str(opened):
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


def _scroll_playlist_list(driver) -> None:
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


def _find_playlist_in_dialog(driver, playlist_name: str) -> str:
    return driver.execute_script("""
        var targetName = arguments[0];
        var dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return 'no_dialog';

        var groups = dialog.querySelectorAll('ytcp-checkbox-group');
        for (var group of groups) {
            var nameSpan = group.querySelector(
                'span.checkbox-label, span.label, span.label-text'
            );
            var txt = nameSpan ? nameSpan.textContent.trim() : '';
            if (!txt) {
                var lbl = group.querySelector('label');
                txt = lbl ? lbl.textContent.trim() : '';
            }
            if (txt.includes(targetName)) {
                var cbDiv = group.querySelector('div[role="checkbox"]');
                var isChecked = cbDiv &&
                    cbDiv.getAttribute('aria-checked') === 'true';
                if (isChecked) return 'already_checked';
                var label = group.querySelector(
                    'label.ytcp-checkbox-label, label'
                );
                if (label) { label.click(); return 'checked'; }
                group.click();
                return 'checked_group';
            }
        }
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


def _close_playlist_dialog(driver) -> None:
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


def _save_video(driver) -> None:
    time.sleep(1)
    driver.execute_script("""
        var btns = document.querySelectorAll('ytcp-button, button');
        for (var b of btns) {
            var txt = (b.textContent || '').trim().toLowerCase();
            var aria = (b.getAttribute('aria-label') || '').toLowerCase();
            if (txt === 'salvar' || txt === 'save'
                || aria === 'salvar' || aria === 'save') {
                if (b.offsetParent !== null) { b.click(); return; }
            }
        }
        var saveBtn = document.querySelector('#save-button');
        if (saveBtn && saveBtn.offsetParent !== null) saveBtn.click();
    """)
    time.sleep(3)


def _selenium_add_video(driver, video_id: str, playlist_name: str) -> str:
    url = f"https://studio.youtube.com/video/{video_id}/edit"
    driver.get(url)
    time.sleep(5)

    # Wait for the editor to be ready
    for _ in range(10):
        ready = driver.execute_script("""
            return document.querySelector('ytcp-video-metadata-editor') !== null
                || document.querySelector('#details') !== null
                || document.querySelector('ytcp-mention-textbox') !== null;
        """)
        if ready:
            break
        time.sleep(2)

    if not _open_playlist_dialog(driver):
        return "no_playlist_selector"

    time.sleep(1)
    _scroll_playlist_list(driver)

    result = _find_playlist_in_dialog(driver, playlist_name)

    if result == "already_checked":
        _close_playlist_dialog(driver)
        return "already_in_playlist"

    if "checked" in str(result):
        time.sleep(1)
        _close_playlist_dialog(driver)
        time.sleep(1)
        _save_video(driver)
        return "added"

    _close_playlist_dialog(driver)
    return f"not_found:{result}"


def run_phase_selenium(
    pending: list[dict],
    dry_run: bool,
) -> list[dict]:
    """Retry every pending target via YouTube Studio UI automation."""
    results: list[dict] = []

    if not pending:
        return results

    print()
    print("=" * 70)
    print(f"Phase Selenium: UI fallback ({len(pending)} targets)")
    print("=" * 70)

    if dry_run:
        for p in pending:
            entry = dict(p)
            entry["method"] = "selenium"
            entry["status"] = "OK"
            entry["note"] = "dry-run"
            print(
                f"[sel-add] {entry['video_id']} -> {entry['playlist']} "
                f"DRY-RUN"
            )
            results.append(entry)
        return results

    if not _selenium_available():
        print(
            "[sel] selenium package not installed. Install with: "
            "pip install selenium"
        )
        for p in pending:
            entry = dict(p)
            entry["method"] = "selenium"
            entry["status"] = "FAIL"
            entry["note"] = "selenium not installed"
            results.append(entry)
        return results

    print()
    print("  IMPORTANT: Close every Chrome window before this phase.")
    print("  If YouTube Studio asks for a password/captcha the script will")
    print("  print a DEBUG screenshot path and keep going -- confirm that")
    print("  you are signed in as the channel owner.")
    print()
    print("[auto] starting in 3 seconds...")
    time.sleep(3)

    try:
        driver = _create_driver()
    except Exception as e:
        print(f"[sel] FATAL could not start browser: {e}")
        for p in pending:
            entry = dict(p)
            entry["method"] = "selenium"
            entry["status"] = "FAIL"
            entry["note"] = f"browser_start_failed: {e}"
            results.append(entry)
        return results

    print("[browser] verifying YouTube Studio session...")
    try:
        driver.get("https://studio.youtube.com")
        time.sleep(5)
        channel = driver.execute_script("""
            var el = document.querySelector(
                'ytcp-entity-name, .entity-name, #entity-name'
            );
            return el ? el.textContent.trim() : 'unknown';
        """)
        print(f"[canal] active channel entity: {channel}")
    except Exception as e:
        print(f"[sel] WARNING could not verify studio session: {e}")

    total = len(pending)
    ok = 0
    failed = 0

    for idx, p in enumerate(pending, start=1):
        vid = p["video_id"]
        pl_title = p["playlist"]
        entry = dict(p)
        entry["method"] = "selenium"
        entry["status"] = "FAIL"
        entry["note"] = ""

        title_preview = (p.get("video_title") or "")[:60]
        print(f"\n[{idx}/{total}] {vid} -> {pl_title}  {title_preview}")

        try:
            result = _selenium_add_video(driver, vid, pl_title)
            print(f"  [result] {result}")
            if result in ("added", "already_in_playlist"):
                entry["status"] = "OK"
                entry["note"] = result
                ok += 1
            else:
                entry["status"] = "FAIL"
                entry["note"] = result
                failed += 1
                # Screenshot for manual triage
                try:
                    shot_path = ROOT / f"debug_p1_{idx}.png"
                    driver.save_screenshot(str(shot_path))
                    print(f"  [debug] screenshot -> {shot_path.name}")
                except Exception:
                    pass
        except Exception as e:
            err_msg = f"{type(e).__name__}: {str(e)[:120]}"
            entry["status"] = "FAIL"
            entry["note"] = err_msg
            failed += 1
            print(f"  [error] {err_msg}")
            try:
                shot_path = ROOT / f"debug_p1_{idx}.png"
                driver.save_screenshot(str(shot_path))
                print(f"  [debug] screenshot -> {shot_path.name}")
            except Exception:
                pass

        results.append(entry)

        if idx % 10 == 0:
            print(
                f"[progress] selenium {idx}/{total} ok={ok} failed={failed}"
            )

        time.sleep(SELENIUM_DELAY)

    print(
        f"[phase-selenium] done: ok={ok} failed={failed}"
    )

    try:
        driver.quit()
    except Exception:
        pass
    return results


# ---- Report -----------------------------------------------------------------


def write_report(
    mode: str,
    total_targets: int,
    dedupe_skipped: list[dict],
    api_items: list[dict],
    pending: list[dict],
    selenium_items: list[dict],
) -> dict:
    api_ok = sum(1 for i in api_items if i["status"] == "OK")
    api_failed = sum(1 for i in api_items if i["status"] == "FAIL")
    sel_ok = sum(1 for i in selenium_items if i["status"] == "OK")
    sel_failed = sum(1 for i in selenium_items if i["status"] == "FAIL")
    dedupe = len(dedupe_skipped)

    total_ok = dedupe + api_ok + sel_ok

    # A target is "remaining" if it neither deduped nor got a final OK
    # from either phase.
    remaining_ids: set[str] = set()
    for it in api_items:
        if it["status"] == "FAIL":
            remaining_ids.add(it["video_id"])
    for it in selenium_items:
        if it["status"] == "FAIL":
            remaining_ids.add(it["video_id"])
    # Also anything that stayed PENDING with no selenium result (skip-sel mode)
    resolved_ids = {i["video_id"] for i in selenium_items}
    for it in pending:
        if it["video_id"] not in resolved_ids:
            remaining_ids.add(it["video_id"])

    total_failed = len(remaining_ids)

    report = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "total_targets": total_targets,
        "dedupe_skipped": dedupe,
        "phase_api": {
            "ok": api_ok,
            "failed": api_failed,
            "items": api_items,
        },
        "phase_selenium": {
            "ok": sel_ok,
            "failed": sel_failed,
            "items": selenium_items,
        },
        "summary": {
            "total_ok": total_ok,
            "total_failed": total_failed,
            "remaining": total_failed,
            "dedupe": dedupe,
            "api_ok": api_ok,
            "api_failed": api_failed,
            "selenium_ok": sel_ok,
            "selenium_failed": sel_failed,
        },
    }

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"mode:                   {mode}")
    print(f"total targets:          {total_targets}")
    print(f"dedupe (already there): {dedupe}")
    print(f"phase API:              ok={api_ok}  failed={api_failed}")
    print(f"phase Selenium:         ok={sel_ok}  failed={sel_failed}")
    print(f"total OK:               {total_ok}")
    print(f"remaining failures:     {total_failed}")
    print(f"report:                 {REPORT_PATH}")

    return report


# ---- Main -------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Hybrid P1 fix: attach 147 orphan videos to Portfolio playlists."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan only, no writes.",
    )
    parser.add_argument(
        "--skip-api",
        action="store_true",
        help="Skip the Data API phase and go straight to Selenium.",
    )
    parser.add_argument(
        "--skip-sel",
        action="store_true",
        help="Skip the Selenium phase (API only).",
    )
    args = parser.parse_args()

    mode_bits = ["dry-run"] if args.dry_run else ["live"]
    if args.skip_api:
        mode_bits.append("skip-api")
    if args.skip_sel:
        mode_bits.append("skip-sel")
    mode = "+".join(mode_bits)

    print("=" * 70)
    print(f"fix_p1_hybrid.py  (mode={mode})")
    print("=" * 70)
    print(f"[paths] client_secret = {CLIENT_SECRET}")
    print(f"[paths] token_cache   = {TOKEN_CACHE}")
    print(f"[paths] delta_report  = {DELTA_REPORT}")
    print(f"[paths] report        = {REPORT_PATH}")

    targets = load_targets()
    print(f"[targets] missing_playlist items = {len(targets)}")
    if not targets:
        print("[noop] nothing to do.")
        return 0

    # Show plan
    by_playlist: dict[str, int] = {}
    for t in targets:
        by_playlist[t["expected_playlist"]] = (
            by_playlist.get(t["expected_playlist"], 0) + 1
        )
    print(f"[plan] {len(by_playlist)} distinct target playlists")
    for name, n in sorted(by_playlist.items(), key=lambda x: -x[1])[:15]:
        print(f"  {n:3d}  {name}")
    if len(by_playlist) > 15:
        print(f"  ... +{len(by_playlist) - 15} more")

    # In skip-api mode, skip everything Data-API related (including OAuth
    # and playlists.list, since playlists.list itself consumes quota).
    # The Selenium phase only needs playlist TITLES, which come from the
    # delta report, so we have everything we need.
    if args.skip_api:
        print()
        print("[phase-api] SKIPPED (--skip-api) -- no Data API calls will be made")
        api_items: list[dict] = []
        dedupe_skipped: list[dict] = []
        pending: list[dict] = []
        # If a previous fix_p1_report.json exists, consume its pending/failed
        # list so we only retry what's actually missing. Otherwise, queue
        # every target for Selenium.
        prior_ok: set[str] = set()
        if REPORT_PATH.exists():
            try:
                prior = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
                for it in prior.get("phase_api", {}).get("items", []):
                    if it.get("status") == "OK":
                        prior_ok.add(it.get("video_id"))
                for it in prior.get("phase_selenium", {}).get("items", []):
                    if it.get("status") == "OK":
                        prior_ok.add(it.get("video_id"))
                print(
                    f"[resume] loaded {len(prior_ok)} prior successes from "
                    f"{REPORT_PATH.name}"
                )
            except Exception as e:
                print(f"[resume] could not read prior report: {e}")

        for t in targets:
            vid = t["video_id"]
            pl_title = t["expected_playlist"]
            if vid in prior_ok:
                entry = {
                    "video_id": vid,
                    "video_title": t.get("video_title", ""),
                    "playlist": pl_title,
                    "client": t.get("client", ""),
                    "method": "dedupe",
                    "status": "SKIP",
                    "note": "previously_resolved",
                }
                dedupe_skipped.append(entry)
                continue
            entry = {
                "video_id": vid,
                "video_title": t.get("video_title", ""),
                "playlist": pl_title,
                "client": t.get("client", ""),
                "method": "api",
                "status": "PENDING",
                "note": "queued_for_selenium",
            }
            pending.append(entry)
        print(
            f"[skip-api] queued {len(pending)} for Selenium, "
            f"{len(dedupe_skipped)} resumed-skipped"
        )
    else:
        creds = get_credentials()
        youtube = build(
            "youtube", "v3", credentials=creds, cache_discovery=False
        )

        # --- Step 0: playlist mapping
        print()
        print("[step0] fetching {title -> playlist_id} map...")
        try:
            playlist_map = fetch_playlist_map(youtube)
        except RuntimeError as e:
            print(f"[fatal] {e}")
            return 1
        except QuotaSignal as qs:
            print(f"[fatal] quota exhausted on playlists.list: {qs}")
            print(
                "[hint] try again after the YouTube Data API daily quota "
                "resets (midnight Pacific Time), or re-run with --skip-api "
                "to bypass the Data API and use Selenium only."
            )
            return 1

        # Which target playlists are not on the channel?
        missing_playlists = sorted(
            {t["expected_playlist"] for t in targets}
            - set(playlist_map.keys())
        )
        if missing_playlists:
            print(
                f"[warn] {len(missing_playlists)} target playlist(s) do NOT "
                "exist on the channel:"
            )
            for m in missing_playlists:
                print(f"  - {m}")
            print("[warn] those videos will be marked FAIL (run fix_p0 first).")

        # --- Step 1: pre-fetch memberships for every distinct target playlist
        print()
        print("[step1] pre-fetching current playlist memberships (dedupe)...")
        memberships: dict[str, set[str]] = {}
        distinct_titles = sorted({t["expected_playlist"] for t in targets})
        for title in distinct_titles:
            pid = playlist_map.get(title)
            if not pid:
                continue
            try:
                vids = fetch_playlist_videos(youtube, pid, title)
            except QuotaSignal as qs:
                print(
                    f"[step1] quota hit while listing {title}: {qs}. "
                    "Proceeding with partial dedupe map."
                )
                break
            memberships[pid] = vids
            print(f"  {title:<45}  {len(vids)} existing item(s)")
        total_existing = sum(len(v) for v in memberships.values())
        print(
            f"[step1] indexed {total_existing} items across "
            f"{len(memberships)} playlists"
        )

        api_items, dedupe_skipped, pending = run_phase_api(
            youtube, targets, playlist_map, memberships, args.dry_run
        )

    # --- Phase Selenium
    if args.skip_sel:
        print()
        print("[phase-selenium] SKIPPED (--skip-sel)")
        selenium_items: list[dict] = []
    else:
        selenium_items = run_phase_selenium(pending, args.dry_run)

    # --- Report
    report = write_report(
        mode=mode,
        total_targets=len(targets),
        dedupe_skipped=dedupe_skipped,
        api_items=api_items,
        pending=pending,
        selenium_items=selenium_items,
    )

    return 0 if report["summary"]["total_failed"] == 0 else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[abort] interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        import traceback
        print("\n[FATAL] unhandled exception:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
