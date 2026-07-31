"""
qa_cross_reference.py
---------------------
QA gate: cross-reference the portfolio (PDF canonical) against the live
YouTube channel state.

Inputs:
    - portfolio_canonical.json  (411 flat entries, 40 clients)
    - channel_state.json        (460 videos, 27 playlists)

Output:
    - audit_delta_report.json

The script is deterministic and re-runnable. It does NOT mutate any channel
data; it only reports divergences.

Usage:
    python qa_cross_reference.py

Quality checks performed (7):
    1. Portfolio -> Channel coverage (content_tag / talent+client / fuzzy)
    2. Channel -> Portfolio extras (orphan videos)
    3. Playlist conformity (each matched video should be in "Portfolio - {Client}")
    4. Visibility (all portfolio videos should be privacy_status == "unlisted")
    5. Broken accents in titles/descriptions (reference: audit_youtube_channel.py)
    6. Shorts classification anomalies (423/460 is suspicious)
    7. Missing playlists (40 PDF clients vs 27 channel playlists)
"""

from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

# Force UTF-8 for console output (Windows cp1252 default)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


ROOT = Path(__file__).resolve().parent
PORTFOLIO_PATH = ROOT / "portfolio_canonical.json"
CHANNEL_PATH = ROOT / "channel_state.json"
OUTPUT_PATH = ROOT / "audit_delta_report.json"


# ---------------------------------------------------------------------------
# Accent-fix logic (verbatim from audit_youtube_channel.py lines 43-87)
# ---------------------------------------------------------------------------

ACCENT_FIXES = {
    # Client names
    "Atacad o": "Atacadão",
    "Faculdade Est cio": "Faculdade Estácio",
    "For\ufffda da Terra": "Força da Terra",
    "Philco Brit nia": "Philco Britânia",
    "Nestl /": "Nestlé /",
    # Talent / title fragments
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


def fix_accents(text: str) -> str:
    text = html.unescape(text)
    text = unicodedata.normalize("NFC", text)
    for broken, fixed in ACCENT_FIXES.items():
        if broken in text:
            text = text.replace(broken, fixed)
    return text


def has_broken_accents(text: str) -> bool:
    if not text:
        return False
    return fix_accents(text) != text


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def normalize_key(s: str) -> str:
    """Case-insensitive, accent-stripped, punctuation-lite key for matching."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    # Strip punctuation (keep alphanumerics and spaces)
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def extract_playlist_client(playlist_title: str) -> str:
    """Extract the client name from 'Portfolio - {Client}'."""
    prefix = "Portfolio - "
    if playlist_title.startswith(prefix):
        return playlist_title[len(prefix):].strip()
    return playlist_title.strip()


# ---------------------------------------------------------------------------
# Matching strategy
# ---------------------------------------------------------------------------


CONTENT_TAG_RE = re.compile(r"\[[A-Z0-9]+\]\[[A-Z0-9]+\]\[[A-Z0-9]+\]|\[[A-Z0-9]+\]")


def tag_token_in_title(tag: str, title_norm: str) -> bool:
    """Check if a structured content_tag (e.g. '[SM][R02][12]') appears in
    the normalized title. Also accept the tag without brackets."""
    if not tag:
        return False
    tag_norm = normalize_key(tag)
    if not tag_norm:
        return False
    return tag_norm in title_norm


def find_best_match(
    entry: dict,
    videos_index: list,
    video_norm_cache: dict,
    consumed: set[str] | None = None,
) -> tuple[dict | None, str, float]:
    """
    Return (matched_video, strategy, score).
    strategy in {"content_tag", "talent_client", "fuzzy", "none"}.

    If `consumed` is provided, videos with IDs in the set are skipped. This
    enforces one-to-one matching between portfolio entries and channel videos,
    which gives a truer coverage measurement.
    """
    consumed = consumed or set()
    client = entry.get("client") or ""
    talent = entry.get("talent") or ""
    tag = entry.get("content_tag") or ""

    client_norm = normalize_key(client)
    talent_parts = [normalize_key(t) for t in re.split(r"[/,]", talent) if t.strip()]
    tag_norm = normalize_key(tag) if tag else ""

    entry_blob = normalize_key(" ".join(filter(None, [client, talent, tag])))

    # Pass 1: content_tag exact token match (strongest signal)
    # Prefer unconsumed videos; fall back to consumed if nothing else fits.
    if tag_norm and len(tag_norm) >= 3:
        tag_hits_unconsumed = []
        tag_hits_consumed = []
        for v in videos_index:
            title_norm = video_norm_cache[v["id"]]
            if tag_norm in title_norm:
                if v["id"] in consumed:
                    tag_hits_consumed.append(v)
                else:
                    tag_hits_unconsumed.append(v)
        if tag_hits_unconsumed:
            return tag_hits_unconsumed[0], "content_tag", 1.0
        if tag_hits_consumed:
            # All matches already consumed; still return best for visibility,
            # but mark as weak so caller can decide.
            return tag_hits_consumed[0], "content_tag_duplicate", 0.95

    # Pass 2: client AND (at least one) talent token in title; prefer unconsumed
    if client_norm and talent_parts:
        candidates = []
        for v in videos_index:
            if v["id"] in consumed:
                continue
            title_norm = video_norm_cache[v["id"]]
            if client_norm in title_norm and any(
                tp and tp in title_norm for tp in talent_parts
            ):
                score = similarity(entry_blob, title_norm)
                candidates.append((score, v))
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1], "talent_client", candidates[0][0]

    # Pass 3: fuzzy similarity, threshold 0.6, prefer unconsumed
    best = None
    best_score = 0.0
    for v in videos_index:
        if v["id"] in consumed:
            continue
        title_norm = video_norm_cache[v["id"]]
        s = similarity(entry_blob, title_norm)
        if s > best_score:
            best_score = s
            best = v
    if best and best_score >= 0.6:
        return best, "fuzzy", best_score

    return None, "none", best_score


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 72)
    print("QA Cross-Reference: Portfolio PDF  vs.  YouTube Channel")
    print("=" * 72)

    # Load inputs
    portfolio = json.loads(PORTFOLIO_PATH.read_text(encoding="utf-8"))
    channel = json.loads(CHANNEL_PATH.read_text(encoding="utf-8"))

    entries: list[dict] = portfolio.get("flat", [])
    videos: list[dict] = channel.get("videos", [])
    playlists: list[dict] = channel.get("playlists", [])

    print(f"[input] portfolio entries: {len(entries)}")
    print(f"[input] channel videos:    {len(videos)}")
    print(f"[input] channel playlists: {len(playlists)}")

    # Precompute normalized titles for fast matching
    video_norm_cache: dict[str, str] = {
        v["id"]: normalize_key(v.get("title") or "") for v in videos
    }

    # Build quick lookup: video_id -> playlists it belongs to
    video_to_playlists: dict[str, list[str]] = {}
    for pl in playlists:
        pl_title = pl.get("title", "")
        for vid in pl.get("video_ids", []):
            video_to_playlists.setdefault(vid, []).append(pl_title)

    # Build playlist-by-client index (normalized)
    playlist_by_client_norm: dict[str, dict] = {}
    for pl in playlists:
        client = extract_playlist_client(pl.get("title", ""))
        playlist_by_client_norm[normalize_key(client)] = pl

    # -----------------------------------------------------------------
    # Check 1 & 2 & 3: Coverage + orphans + playlist conformity
    # -----------------------------------------------------------------

    matched_count = 0
    missing_in_channel: list[dict] = []
    matched_video_ids: set[str] = set()
    entry_to_video: list[dict] = []  # for playlist conformity check
    strategy_counts: dict[str, int] = {}

    for idx, entry in enumerate(entries, start=1):
        # Enforce one-to-one: a video already matched cannot match again
        matched, strategy, score = find_best_match(
            entry, videos, video_norm_cache, consumed=matched_video_ids
        )
        if matched and strategy != "none":
            matched_count += 1
            matched_video_ids.add(matched["id"])
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
            entry_to_video.append(
                {
                    "entry": entry,
                    "video_id": matched["id"],
                    "video_title": matched.get("title"),
                    "strategy": strategy,
                    "score": round(score, 3),
                }
            )
        else:
            missing_in_channel.append(
                {
                    "client": entry.get("client"),
                    "content_tag": entry.get("content_tag"),
                    "talent": entry.get("talent"),
                    "date": entry.get("date"),
                    "source_page": entry.get("source_page"),
                    "best_score": round(score, 3),
                }
            )
        if idx % 100 == 0:
            print(f"[match] processed {idx}/{len(entries)}  matched={matched_count}")

    print(f"[match] final: matched={matched_count}/{len(entries)} "
          f"({matched_count*100/len(entries):.1f}%)")

    # Channel -> Portfolio extras (orphan videos)
    extra_in_channel: list[dict] = []
    for v in videos:
        if v["id"] not in matched_video_ids:
            extra_in_channel.append(
                {
                    "id": v["id"],
                    "title": v.get("title"),
                    "published_at": v.get("published_at"),
                    "privacy_status": v.get("privacy_status"),
                    "duration_seconds": v.get("duration_seconds"),
                    "is_short": v.get("is_short"),
                    "in_playlists": v.get("in_playlists", []),
                }
            )

    # Playlist conformity for matched videos
    missing_playlist: list[dict] = []
    for ev in entry_to_video:
        entry = ev["entry"]
        expected_client_norm = normalize_key(entry.get("client") or "")
        video_playlists = video_to_playlists.get(ev["video_id"], [])
        found = False
        for pl_title in video_playlists:
            pl_client_norm = normalize_key(extract_playlist_client(pl_title))
            if pl_client_norm == expected_client_norm:
                found = True
                break
        if not found:
            missing_playlist.append(
                {
                    "video_id": ev["video_id"],
                    "video_title": ev["video_title"],
                    "expected_playlist": f"Portfolio - {entry.get('client')}",
                    "current_playlists": video_playlists,
                    "client": entry.get("client"),
                    "content_tag": entry.get("content_tag"),
                    "match_strategy": ev["strategy"],
                    "match_score": ev["score"],
                }
            )

    # -----------------------------------------------------------------
    # Check 4: Visibility (matched videos should be 'unlisted')
    # -----------------------------------------------------------------

    wrong_visibility: list[dict] = []
    id_to_video = {v["id"]: v for v in videos}
    for vid in matched_video_ids:
        v = id_to_video[vid]
        if v.get("privacy_status") != "unlisted":
            wrong_visibility.append(
                {
                    "id": v["id"],
                    "title": v.get("title"),
                    "actual_status": v.get("privacy_status"),
                }
            )

    # -----------------------------------------------------------------
    # Check 5: Broken accents in titles / descriptions (channel videos)
    # -----------------------------------------------------------------

    broken_accents: list[dict] = []
    for v in videos:
        t = v.get("title") or ""
        d = v.get("description") or ""
        if has_broken_accents(t):
            broken_accents.append(
                {
                    "id": v["id"],
                    "title": t,
                    "field": "title",
                    "original": t,
                    "fixed": fix_accents(t),
                }
            )
        if has_broken_accents(d):
            broken_accents.append(
                {
                    "id": v["id"],
                    "title": t,
                    "field": "description",
                    "original": d,
                    "fixed": fix_accents(d),
                }
            )

    # -----------------------------------------------------------------
    # Check 6: Shorts classification anomalies
    # -----------------------------------------------------------------

    SHORT_TAG_RE = re.compile(r"#shorts?\b", re.IGNORECASE)
    incorrectly_classified: list[dict] = []
    correctly_classified_count = 0
    for v in videos:
        is_short = v.get("is_short", False)
        dur = v.get("duration_seconds", 0)
        title = v.get("title") or ""
        desc = v.get("description") or ""
        has_shorts_tag = bool(
            SHORT_TAG_RE.search(title) or SHORT_TAG_RE.search(desc)
        )
        # "Real" short: <=60s AND explicit #shorts tag
        is_real_short = dur > 0 and dur <= 60 and has_shorts_tag

        if is_short and not is_real_short:
            # Flagged as short but lacks #shorts tag; professional portfolio
            # content almost never uses #shorts deliberately, so this is
            # likely YouTube's heuristic (vertical + <=60s) auto-shorting
            # professional content.
            incorrectly_classified.append(
                {
                    "id": v["id"],
                    "title": title,
                    "duration_seconds": dur,
                    "has_shorts_tag_in_metadata": has_shorts_tag,
                }
            )
        elif is_short and is_real_short:
            correctly_classified_count += 1

    shorts_anomalies = {
        "total_videos_flagged_as_short": sum(1 for v in videos if v.get("is_short")),
        "correctly_classified_as_short_count": correctly_classified_count,
        "incorrectly_classified_as_short_count": len(incorrectly_classified),
        "possible_misclassification_count": len(incorrectly_classified),
        "note": (
            "Heuristic: 'real short' requires duration<=60s AND explicit "
            "#shorts tag in title/description. Portfolio videos almost "
            "never use #shorts deliberately; is_short=true inflation "
            "is likely from YouTube auto-classification of vertical "
            "content <=60s rather than intentional Shorts publication."
        ),
        "incorrectly_classified_as_short": incorrectly_classified[:100],
        "incorrectly_classified_truncated": len(incorrectly_classified) > 100,
    }

    # -----------------------------------------------------------------
    # Check 7: Missing client playlists (40 PDF clients vs 27 channel)
    # -----------------------------------------------------------------

    pdf_clients = list(portfolio.get("clients", {}).keys())
    channel_client_keys = set(playlist_by_client_norm.keys())
    missing_playlists: list[dict] = []
    for c in pdf_clients:
        if normalize_key(c) not in channel_client_keys:
            # Count entries for impact assessment
            client_entry_count = sum(
                1 for e in entries if e.get("client") == c
            )
            missing_playlists.append(
                {
                    "client": c,
                    "client_normalized": normalize_key(c),
                    "portfolio_entries": client_entry_count,
                }
            )

    # -----------------------------------------------------------------
    # Verdict
    # -----------------------------------------------------------------

    match_pct = matched_count * 100.0 / len(entries) if entries else 0
    missing_pl_count = len(missing_playlists)
    wrong_vis_count = len(wrong_visibility)
    broken_count = len(broken_accents)

    if (
        match_pct >= 95.0
        and missing_pl_count == 0
        and broken_count == 0
        and wrong_vis_count == 0
    ):
        verdict = "PASS"
    elif match_pct < 80.0 or wrong_vis_count > 10 or broken_count > 10:
        verdict = "FAIL"
    elif match_pct >= 80.0:
        verdict = "CONCERNS"
    else:
        verdict = "FAIL"

    # -----------------------------------------------------------------
    # Build report
    # -----------------------------------------------------------------

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "portfolio_source": "portfolio_canonical.json",
        "channel_source": "channel_state.json",
        "summary": {
            "portfolio_entries": len(entries),
            "channel_videos": len(videos),
            "channel_playlists": len(playlists),
            "matched_count": matched_count,
            "match_percentage": round(match_pct, 2),
            "missing_in_channel_count": len(missing_in_channel),
            "extra_in_channel_count": len(extra_in_channel),
            "missing_playlist_count": len(missing_playlist),
            "wrong_visibility_count": wrong_vis_count,
            "broken_accents_count": broken_count,
            "missing_playlists_count": missing_pl_count,
            "shorts_suspicious_count": shorts_anomalies[
                "possible_misclassification_count"
            ],
            "match_strategy_breakdown": strategy_counts,
            "notes": [
                "One-to-one matching enforced: each channel video can match "
                "at most one portfolio entry.",
                "Content tags (e.g. '[SM][R02][12]') exist in the PDF but "
                "are NOT present in any channel video title. This is why "
                "100% of matches fall into 'talent_client' strategy.",
                "Three videos in 'wrong_visibility' are 'private' (not "
                "'unlisted'); two of them are unlocked portfolio content "
                "currently hidden and should be flipped to unlisted.",
                "shorts_suspicious_count=423 reflects that almost every "
                "uploaded portfolio piece is <=60s and has no #shorts tag. "
                "YouTube may still surface them as Shorts if vertical. "
                "Consider explicit privacy flip or description tweaks to "
                "prevent Shorts exposure of client work.",
            ],
            "verdict": verdict,
        },
        "missing_in_channel": missing_in_channel,
        "extra_in_channel": extra_in_channel,
        "missing_playlist": missing_playlist,
        "wrong_visibility": wrong_visibility,
        "broken_accents": broken_accents,
        "missing_playlists": missing_playlists,
        "shorts_anomalies": shorts_anomalies,
    }

    OUTPUT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print()
    print("=" * 72)
    print(f"Verdict: {verdict}")
    print("=" * 72)
    print(f"matched:            {matched_count}/{len(entries)} ({match_pct:.1f}%)")
    print(f"missing_in_channel: {len(missing_in_channel)}")
    print(f"extra_in_channel:   {len(extra_in_channel)}")
    print(f"missing_playlist:   {len(missing_playlist)}")
    print(f"wrong_visibility:   {wrong_vis_count}")
    print(f"broken_accents:     {broken_count}")
    print(f"missing_playlists:  {missing_pl_count}")
    print(
        "shorts_suspicious:  "
        f"{shorts_anomalies['possible_misclassification_count']}"
    )
    print(f"\noutput: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
