"""
=============================================================
PDF TO PORTFOLIO - Canonical JSON Parser
=============================================================
Le o PDF `Allfluence - Portfolio pessoal (1).pdf` (19 paginas)
e produz um JSON canonico normalizado agrupado por cliente.

Colunas do PDF: Cliente | Plataforma | Funcao | Conteudo |
                Talento / Creator | Data

Saida: portfolio_canonical.json
{
  "generated_at": "<ISO timestamp>",
  "source": "Allfluence - Portfolio pessoal (1).pdf",
  "total_entries": <count>,
  "clients": { "<Cliente>": [ {entry}, ... ], ... },
  "flat":    [ {entry_with_client_field}, ... ]
}

USO: python pdf_to_portfolio.py
=============================================================
"""

from __future__ import annotations

import json
import os
import sys
import html
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

try:
    import pdfplumber  # type: ignore
    _PDF_BACKEND = "pdfplumber"
except ImportError:
    pdfplumber = None  # type: ignore
    _PDF_BACKEND = None
    try:
        from pdfminer.high_level import extract_text as _pdfminer_extract_text  # type: ignore
        _PDF_BACKEND = "pdfminer"
    except ImportError:
        try:
            import PyPDF2  # type: ignore
            _PDF_BACKEND = "PyPDF2"
        except ImportError:
            pass

if _PDF_BACKEND is None:
    sys.stderr.write(
        "ERROR: No PDF backend available. Install with:\n"
        "  pip install pdfplumber\n"
    )
    sys.exit(1)


# --- CONFIG ---
PDF_PATH = (
    "C:\\Users\\savyl\\Downloads\\Allfluence - Portf\u00f3lio pessoal (1).pdf"
)
OUTPUT_JSON = "portfolio_canonical.json"
SOURCE_NAME = "Allfluence - Portfolio pessoal (1).pdf"


# =============================================================
# ACCENT FIXES (reused from audit_youtube_channel.py lines 43-70)
# =============================================================

ACCENT_FIXES = {
    # Client names
    "Atacad o": "Atacad\u00e3o",
    "Faculdade Est cio": "Faculdade Est\u00e1cio",
    "For\ufffda da Terra": "For\u00e7a da Terra",
    "Philco Brit nia": "Philco Brit\u00e2nia",
    "Nestl /": "Nestl\u00e9 /",
    # Talento/title name fragments
    "Jo o Mendes": "Jo\u00e3o Mendes",
    "Jo o Victor": "Jo\u00e3o Victor",
    "Joa\u0303o": "Jo\u00e3o",
    "D bora Melo": "D\u00e9bora Melo",
    "D bora Mel": "D\u00e9bora Mel",
    "Andr Lemos": "Andr\u00e9 Lemos",
    "Maria Lu za": "Maria Lu\u00edza",
    "Lu za Kropotoff": "Lu\u00edza Kropotoff",
    "Qu ren Hapuque": "Qu\u00e9ren Hapuque",
    "Let cia Pedro": "Let\u00edcia Pedro",
    "Vit ria Rodrigues": "Vit\u00f3ria Rodrigues",
    "J lia Horta": "J\u00falia Horta",
    "Val rio": "Val\u00e9rio",
    "Cabe\ufffda": "Cabe\u00e7a",
    "Pablo Sant Anna": "Pablo Sant'Anna",
    "Isadora cecatto": "Isadora Cecatto",
    "Est cio": "Est\u00e1cio",
    "Brit nia": "Brit\u00e2nia",
    "Joa&#771;o": "Jo\u00e3o",
}


def fix_accents(text: str) -> str:
    """Fix broken accents and HTML entities in text (same logic as audit script)."""
    if not text:
        return text
    text = html.unescape(text)
    text = unicodedata.normalize('NFC', text)
    for broken, fixed in ACCENT_FIXES.items():
        if broken in text:
            text = text.replace(broken, fixed)
    return text


# =============================================================
# NORMALIZATION HELPERS
# =============================================================

_HEADER_ROW_MARKERS = {"Cliente", "Portf\u00f3lio pessoal", "Portfolio pessoal"}


def _clean_cell(value) -> str:
    """Normalize a raw table cell:
    - collapse multiline values joined by newline -> single string
    - strip whitespace
    - apply accent fixes
    """
    if value is None:
        return ""
    text = str(value)
    # Multi-line cells -> join with space (preserves visual grouping from PDF)
    parts = [p.strip() for p in text.split("\n") if p.strip()]
    joined = " ".join(parts).strip()
    return fix_accents(joined)


def _clean_multiline(value) -> str:
    """Like _clean_cell but keep distinct lines joined with ' / ' for lists
    (useful for role/platform/talent when they are stacked vertically)."""
    if value is None:
        return ""
    text = str(value)
    parts = [p.strip() for p in text.split("\n") if p.strip()]
    joined = " / ".join(parts).strip()
    return fix_accents(joined)


def _is_header_row(row) -> bool:
    if not row:
        return True
    first = (row[0] or "").strip()
    return first in _HEADER_ROW_MARKERS or first == ""


def _normalize_date(raw: str) -> str:
    """Keep ISO date if already ISO; otherwise return raw cleaned."""
    raw = (raw or "").strip()
    if not raw:
        return ""
    # Expected format: YYYY-MM-DD
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        # Try other common formats used in the PDF (just in case)
        for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return raw  # keep as-is if unparseable


# =============================================================
# PARSER
# =============================================================

def parse_pdf(pdf_path: str):
    """Parse all pages of the PDF and yield normalized entry dicts."""
    if _PDF_BACKEND != "pdfplumber":
        raise RuntimeError(
            f"pdfplumber required for structured table parsing "
            f"(current backend: {_PDF_BACKEND})"
        )

    warnings = []
    entries = []
    pages_seen = 0

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            pages_seen += 1
            tables = page.extract_tables() or []
            if not tables:
                warnings.append(f"page {page_idx}: no tables extracted")
                continue

            for table in tables:
                for row_idx, row in enumerate(table):
                    if _is_header_row(row):
                        continue
                    if len(row) < 6:
                        warnings.append(
                            f"page {page_idx} row {row_idx}: expected 6 columns, got {len(row)} -> {row}"
                        )
                        continue

                    client = _clean_cell(row[0])
                    platform = _clean_multiline(row[1])
                    role = _clean_multiline(row[2])
                    content_tag = _clean_cell(row[3])
                    talent = _clean_multiline(row[4])
                    date_raw = _clean_cell(row[5])

                    # Skip completely empty rows
                    if not any([client, platform, role, content_tag, talent, date_raw]):
                        continue

                    # A valid entry requires at least a client + one content signal
                    if not client:
                        warnings.append(
                            f"page {page_idx} row {row_idx}: missing client -> {row}"
                        )
                        continue

                    entry = {
                        "client": client,
                        "platform": platform,
                        "role": role,
                        "content_tag": content_tag,
                        "talent": talent,
                        "date": _normalize_date(date_raw),
                        "source_page": page_idx,
                    }
                    entries.append(entry)

    return entries, warnings, pages_seen


# =============================================================
# MAIN
# =============================================================

def main():
    if not os.path.exists(PDF_PATH):
        sys.stderr.write(f"ERROR: PDF not found at {PDF_PATH}\n")
        sys.exit(2)

    print(f"[*] Backend: {_PDF_BACKEND}")
    print(f"[*] Reading: {PDF_PATH}")

    try:
        entries, warnings, pages_seen = parse_pdf(PDF_PATH)
    except Exception as exc:
        sys.stderr.write(f"ERROR parsing PDF: {exc}\n")
        raise

    print(f"[*] Pages processed: {pages_seen}")
    print(f"[*] Entries parsed: {len(entries)}")
    if warnings:
        print(f"[!] Warnings: {len(warnings)}")
        for w in warnings[:10]:
            print(f"    - {w}")
        if len(warnings) > 10:
            print(f"    ... (+{len(warnings) - 10} more)")

    # Group by client, preserving first-seen order
    grouped = defaultdict(list)
    client_order = []
    for e in entries:
        if e["client"] not in grouped:
            client_order.append(e["client"])
        # For the "clients" bucket we strip the redundant "client" key
        grouped[e["client"]].append({k: v for k, v in e.items() if k != "client"})

    ordered_clients = {c: grouped[c] for c in client_order}

    canonical = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": SOURCE_NAME,
        "pdf_path": PDF_PATH,
        "pages_processed": pages_seen,
        "total_entries": len(entries),
        "clients": ordered_clients,
        "flat": entries,
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_JSON)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(canonical, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Wrote: {out_path}")
    print(f"[OK] Total entries: {len(entries)}")
    print(f"[OK] Clients: {len(ordered_clients)}")

    # Per-client breakdown
    print("\n--- Per-client counts ---")
    counts = sorted(
        ((c, len(v)) for c, v in ordered_clients.items()),
        key=lambda kv: kv[1],
        reverse=True,
    )
    for client, count in counts:
        print(f"  {count:>4}  {client}")
    print(f"\n  TOTAL: {sum(c for _, c in counts)}")

    return canonical


if __name__ == "__main__":
    main()
