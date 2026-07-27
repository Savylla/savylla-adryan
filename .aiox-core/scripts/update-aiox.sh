#!/bin/bash
# AIOX Framework Update - v5.3 (Optimized)
#
# LOGIC:
#   - LOCAL only (not in upstream)     → KEEP
#   - LOCAL + UPSTREAM                 → OVERWRITE (upstream wins)
#   - UPSTREAM only (not in local)     → CREATE
#   - WAS in both, UPSTREAM removed    → DELETE
#   - Listed in .aiox-core/.updateignore → PROTECT (upstream copy saved as
#                                          <file>.upstream-new for manual merge)
#
# Usage: bash .aiox-core/scripts/update-aiox.sh [--dry-run]
#
#   --dry-run   Analyze and report only; changes nothing on disk. Does not
#               require a clean working tree.

set -e

DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) echo "❌ Unknown option: $arg"; echo "Usage: bash .aiox-core/scripts/update-aiox.sh [--dry-run]"; exit 1 ;;
  esac
done

if [ "$DRY_RUN" -eq 1 ]; then
  echo "⚡ AIOX Update v5.3 (dry run — nothing will be written)"
else
  echo "⚡ AIOX Update v5.3"
fi
echo ""

# Always operate from the repo root, regardless of where this was invoked from.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "❌ Not inside a git repository."
  exit 1
}
cd "$REPO_ROOT"

if [ ! -d .aiox-core ]; then
  echo "❌ No .aiox-core/ directory at repo root: $REPO_ROOT"
  exit 1
fi

# Copy a directory's contents, preserving attributes.
# Uses rsync when available and falls back to cp -a otherwise (Git Bash on
# Windows ships no rsync).
copy_tree() {
  local src="$1" dest="$2"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$src/" "$dest/"
  else
    cp -a "$src/." "$dest/"
  fi
}

# Validate: clean working tree for .aiox-core (skipped on dry runs, which write
# nothing and therefore cannot lose work).
if [ "$DRY_RUN" -eq 0 ] && [ -n "$(git status --porcelain .aiox-core/)" ]; then
  echo "❌ Commit .aiox-core changes first:"
  git status --short .aiox-core/
  echo ""
  echo "Run: git add .aiox-core && git commit -m 'your message'"
  echo "Or preview without touching anything: bash .aiox-core/scripts/update-aiox.sh --dry-run"
  exit 1
fi

# Temp directory
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# Report files
REPORT_CREATED="$TEMP_DIR/report-created.txt"
REPORT_UPDATED="$TEMP_DIR/report-updated.txt"
REPORT_DELETED="$TEMP_DIR/report-deleted.txt"
REPORT_PRESERVED="$TEMP_DIR/report-preserved.txt"
REPORT_PROTECTED="$TEMP_DIR/report-protected.txt"
touch "$REPORT_CREATED" "$REPORT_UPDATED" "$REPORT_DELETED" "$REPORT_PRESERVED" "$REPORT_PROTECTED"

# Load protected paths from .updateignore (comments and blanks stripped).
PROTECT_LIST="$TEMP_DIR/protected-patterns.txt"
: > "$PROTECT_LIST"
if [ -f .aiox-core/.updateignore ]; then
  sed -e 's/#.*//' -e 's/[[:space:]]*$//' .aiox-core/.updateignore \
    | grep -v '^$' > "$PROTECT_LIST" || true
fi

# is_protected <relative-path> — exact match, or under a `dir/` prefix entry.
is_protected() {
  local candidate="$1" pattern
  while IFS= read -r pattern; do
    [ -z "$pattern" ] && continue
    case "$pattern" in
      */) case "$candidate" in "$pattern"*) return 0 ;; esac ;;
      *)  [ "$candidate" = "$pattern" ] && return 0 ;;
    esac
  done < "$PROTECT_LIST"
  return 1
}

# Clone upstream (shallow)
echo "📥 Cloning upstream..."
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/SynkraAI/aiox-core.git \
  "$TEMP_DIR/upstream" 2>/dev/null || {
  echo "❌ Failed to clone. Check network."
  exit 1
}

git -C "$TEMP_DIR/upstream" sparse-checkout set .aiox-core

UPSTREAM_DIR="$TEMP_DIR/upstream/.aiox-core"
if [ ! -d "$UPSTREAM_DIR" ]; then
  echo "❌ Upstream clone has no .aiox-core/ directory."
  exit 1
fi

echo "✅ Fetched upstream"
echo ""

# Build file lists (relative paths without .aiox-core/ prefix).
# node_modules/ is a local build artifact: excluding it keeps the scan fast and
# keeps thousands of dependency files out of the PRESERVED report. It is never
# deleted, because deletions only ever come from git-tracked files.
echo "📋 Scanning files..."
find .aiox-core -type f -not -path '.aiox-core/node_modules/*' \
  | sed 's|^\.aiox-core/||' | sort > "$TEMP_DIR/local-files.txt"
(cd "$UPSTREAM_DIR" && find . -type f | sed 's|^\./||' | sort) > "$TEMP_DIR/upstream-files.txt"

# Get git-tracked files (for DELETE detection) - ONE call instead of N calls
git ls-files .aiox-core | sed 's|^\.aiox-core/||' | sort > "$TEMP_DIR/tracked-files.txt"

# Use comm to find differences - O(n) instead of O(n²)
echo "🔍 Analyzing differences..."

# LOCAL-ONLY: in local but not in upstream
comm -23 "$TEMP_DIR/local-files.txt" "$TEMP_DIR/upstream-files.txt" > "$REPORT_PRESERVED"

# UPSTREAM-ONLY (CREATE): in upstream but not in local
comm -13 "$TEMP_DIR/local-files.txt" "$TEMP_DIR/upstream-files.txt" > "$TEMP_DIR/created-all.txt"

# IN-BOTH: files that exist in both
comm -12 "$TEMP_DIR/local-files.txt" "$TEMP_DIR/upstream-files.txt" > "$TEMP_DIR/in-both.txt"

# DELETE: was tracked by git, not in upstream, not local-only
comm -23 "$TEMP_DIR/tracked-files.txt" "$TEMP_DIR/upstream-files.txt" | \
  comm -23 - "$REPORT_PRESERVED" > "$TEMP_DIR/deleted-all.txt"

# Split out protected paths so they are never created, overwritten or deleted.
while IFS= read -r rel_path; do
  if is_protected "$rel_path"; then
    echo "$rel_path" >> "$REPORT_PROTECTED"
  else
    echo "$rel_path" >> "$REPORT_CREATED"
  fi
done < "$TEMP_DIR/created-all.txt"

while IFS= read -r rel_path; do
  is_protected "$rel_path" || echo "$rel_path" >> "$REPORT_DELETED"
done < "$TEMP_DIR/deleted-all.txt"

# UPDATED: in both but content differs (protected files are reported, not changed)
echo "📝 Checking for updates..."
while IFS= read -r rel_path; do
  if ! cmp -s ".aiox-core/$rel_path" "$UPSTREAM_DIR/$rel_path"; then
    if is_protected "$rel_path"; then
      echo "$rel_path" >> "$REPORT_PROTECTED"
    else
      echo "$rel_path" >> "$REPORT_UPDATED"
    fi
  fi
done < "$TEMP_DIR/in-both.txt"

if [ "$DRY_RUN" -eq 0 ]; then
  # Back up local-only AND protected files, then restore them after the copy.
  echo "🔐 Backing up local-only files..."
  mkdir -p "$TEMP_DIR/keep"
  cat "$REPORT_PRESERVED" "$REPORT_PROTECTED" | sort -u > "$TEMP_DIR/keep-list.txt"
  while IFS= read -r rel_path; do
    [ -f ".aiox-core/$rel_path" ] || continue
    mkdir -p "$TEMP_DIR/keep/$(dirname "$rel_path")"
    cp -a ".aiox-core/$rel_path" "$TEMP_DIR/keep/$rel_path"
  done < "$TEMP_DIR/keep-list.txt"

  # Execute sync
  echo ""
  echo "🔀 Syncing..."

  # Delete files removed from upstream
  if [ -s "$REPORT_DELETED" ]; then
    while IFS= read -r rel_path; do
      rm -f ".aiox-core/$rel_path"
    done < "$REPORT_DELETED"
  fi

  # Copy all upstream files (creates new + overwrites existing)
  copy_tree "$UPSTREAM_DIR" ".aiox-core"

  # Restore local-only + protected files over the upstream copy
  if [ -n "$(ls -A "$TEMP_DIR/keep" 2>/dev/null)" ]; then
    copy_tree "$TEMP_DIR/keep" ".aiox-core"
  fi

  # For protected files that upstream changed, drop the upstream version next to
  # ours so the diff is not lost silently.
  if [ -s "$REPORT_PROTECTED" ]; then
    while IFS= read -r rel_path; do
      [ -f "$UPSTREAM_DIR/$rel_path" ] || continue
      cp -a "$UPSTREAM_DIR/$rel_path" ".aiox-core/$rel_path.upstream-new"
    done < "$REPORT_PROTECTED"
  fi

  # Clean empty directories
  find .aiox-core -type d -empty -delete 2>/dev/null || true
fi

# Generate report
echo ""
echo "════════════════════════════════════════════════════════════"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "  SYNC REPORT (DRY RUN — nothing was written)"
else
  echo "  SYNC REPORT"
fi
echo "════════════════════════════════════════════════════════════"

CREATED_COUNT=$(wc -l < "$REPORT_CREATED" | tr -d ' ')
UPDATED_COUNT=$(wc -l < "$REPORT_UPDATED" | tr -d ' ')
DELETED_COUNT=$(wc -l < "$REPORT_DELETED" | tr -d ' ')
PRESERVED_COUNT=$(wc -l < "$REPORT_PRESERVED" | tr -d ' ')
PROTECTED_COUNT=$(sort -u "$REPORT_PROTECTED" | grep -c '^' || true)

echo ""
echo "  ➕ CREATED:   $CREATED_COUNT files"
if [ "$CREATED_COUNT" -gt 0 ] && [ "$CREATED_COUNT" -le 20 ]; then
  sed 's/^/       /' "$REPORT_CREATED"
elif [ "$CREATED_COUNT" -gt 20 ]; then
  head -10 "$REPORT_CREATED" | sed 's/^/       /'
  echo "       ... and $((CREATED_COUNT - 10)) more"
fi

echo ""
echo "  📝 UPDATED:   $UPDATED_COUNT files"
if [ "$UPDATED_COUNT" -gt 0 ] && [ "$UPDATED_COUNT" -le 20 ]; then
  sed 's/^/       /' "$REPORT_UPDATED"
elif [ "$UPDATED_COUNT" -gt 20 ]; then
  head -10 "$REPORT_UPDATED" | sed 's/^/       /'
  echo "       ... and $((UPDATED_COUNT - 10)) more"
fi

echo ""
echo "  🗑️  DELETED:   $DELETED_COUNT files"
if [ "$DELETED_COUNT" -gt 0 ] && [ "$DELETED_COUNT" -le 20 ]; then
  sed 's/^/       /' "$REPORT_DELETED"
elif [ "$DELETED_COUNT" -gt 20 ]; then
  head -10 "$REPORT_DELETED" | sed 's/^/       /'
  echo "       ... and $((DELETED_COUNT - 10)) more"
fi

echo ""
echo "  🔐 PRESERVED: $PRESERVED_COUNT local-only files"
if [ "$PRESERVED_COUNT" -gt 0 ] && [ "$PRESERVED_COUNT" -le 10 ]; then
  sed 's/^/       /' "$REPORT_PRESERVED"
elif [ "$PRESERVED_COUNT" -gt 10 ]; then
  head -5 "$REPORT_PRESERVED" | sed 's/^/       /'
  echo "       ... and $((PRESERVED_COUNT - 5)) more"
fi

echo ""
echo "  🛡️  PROTECTED: $PROTECTED_COUNT files differ upstream (.updateignore)"
if [ "$PROTECTED_COUNT" -gt 0 ]; then
  sort -u "$REPORT_PROTECTED" | sed 's/^/       /'
  if [ "$DRY_RUN" -eq 0 ]; then
    echo "       → upstream version saved as <file>.upstream-new — merge by hand"
  fi
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run only. To apply:"
  echo "  bash .aiox-core/scripts/update-aiox.sh"
else
  echo "Choose:"
  echo "  ✅ Apply:  git add .aiox-core && git commit -m 'chore: sync AIOX framework'"
  echo "  ❌ Cancel: git checkout -- .aiox-core/"
fi
echo ""
