"""
Migra URLs ClickUp -> YouTube IDs em script.js usando youtube_results.json como mapping.

Estratégia:
1. URL match exato (original_url == url no script.js)
2. Fallback: match por filename do .mp4
3. URLs sem match permanecem intactas (4 vídeos Carrefour ainda nao subidos pro YT)

Substituicao apenas troca a propriedade `url: "..."` por `youtubeId: "..."`,
preservando todas as outras propriedades (talento, direcao, etc.) e a ordem.
"""
import json
import re
from urllib.parse import unquote
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPT_JS = ROOT / "script.js"
YT_RESULTS = ROOT / "youtube_results.json"
BACKUP = ROOT / "script.js.bak.pre-migration"


def build_lookup():
    with open(YT_RESULTS, "r", encoding="utf-8") as f:
        data = json.load(f)
    url_map = {}
    fn_map = {}
    for cliente, vids in data.items():
        for v in vids:
            ou = v.get("original_url")
            vid = v.get("video_id")
            if not (ou and vid):
                continue
            url_map[ou] = vid
            m = re.search(r"/([^/?]+\.mp4)", ou)
            if m:
                fn = unquote(m.group(1)).strip().lower()
                fn_map.setdefault(fn, vid)
    return url_map, fn_map


def main():
    url_map, fn_map = build_lookup()
    print(f"[mapping] {len(url_map)} URLs, {len(fn_map)} filenames")

    js = SCRIPT_JS.read_text(encoding="utf-8")
    SCRIPT_JS.with_name("script.js.bak.pre-migration").write_text(js, encoding="utf-8")
    print(f"[backup] {BACKUP.name}")

    pattern = re.compile(r'url:\s*"(https://t9007008605\.p\.clickup-attachments\.com[^"]+)"')

    stats = {"replaced": 0, "filename_match": 0, "unmatched": 0}
    unmatched_samples = []

    def repl(m):
        url = m.group(1)
        if url in url_map:
            stats["replaced"] += 1
            return f'youtubeId: "{url_map[url]}"'
        # Fallback filename
        mfn = re.search(r"/([^/?]+\.mp4)", url)
        if mfn:
            fn = unquote(mfn.group(1)).strip().lower()
            if fn in fn_map:
                stats["replaced"] += 1
                stats["filename_match"] += 1
                return f'youtubeId: "{fn_map[fn]}"'
        stats["unmatched"] += 1
        if len(unmatched_samples) < 10:
            unmatched_samples.append(url[:140])
        return m.group(0)

    new_js = pattern.sub(repl, js)
    SCRIPT_JS.write_text(new_js, encoding="utf-8")

    print(f"[done] replaced={stats['replaced']} (filename_fallback={stats['filename_match']}) unmatched={stats['unmatched']}")
    if unmatched_samples:
        print("\nUnmatched (mantidos como url ClickUp):")
        for u in unmatched_samples:
            print(f"  - {u}...")


if __name__ == "__main__":
    main()
