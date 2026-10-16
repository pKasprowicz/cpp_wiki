#!/usr/bin/env bash
# Build, preview or clean the Quartz site for wiki/.
#
# This is the only place that knows how to build the site. The Makefile and
# .github/workflows/site.yml both call it, so local and CI builds are identical.
#
#   scripts/build-site.sh check   wiki lint + broken-wikilink check (no Node needed)
#   scripts/build-site.sh build   build the site into public/
#   scripts/build-site.sh serve   build and serve with hot reload (PORT, default 8080)
#   scripts/build-site.sh clean   remove public/ and .quartz-cache/
#
# Environment:
#   SITE_BASE_URL  deployed address for baseUrl (host[/path], no protocol); optional
#   PORT           preview port for `serve` (default 8080)
#   PYTHON         Python 3.9+ interpreter for `check` (default: auto-detect)
#
# How it works: Quartz is not vendored. The pinned release (site/versions.env) is
# shallow-cloned into .quartz-cache/, our site/quartz.config.ts and
# site/quartz.layout.ts are copied over its defaults, and Quartz is run with
# wiki/ as the content directory.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTENT_DIR="$ROOT/wiki"
OUT_DIR="$ROOT/public"
CACHE_DIR="$ROOT/.quartz-cache"
QUARTZ_REPO="https://github.com/jackyzha0/quartz.git"
NEED_NODE_MAJOR=22
NEED_NPM=10.9.2

# shellcheck source=../site/versions.env
. "$ROOT/site/versions.env"
QUARTZ_DIR="$CACHE_DIR/quartz-$QUARTZ_TAG"

die() { echo "build-site: $*" >&2; exit 1; }
log() { echo "build-site: $*"; }

# Node on Windows wants C:/... paths, not the /c/... paths of Git Bash.
native_path() {
  if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s' "$1"; fi
}

find_python() {
  local c
  for c in ${PYTHON:-} python3 python py; do
    if "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
      echo "$c"
      return 0
    fi
  done
  return 1
}

version_ge() { # version_ge HAVE NEED: true when HAVE >= NEED (dotted versions)
  [ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

require_node() {
  command -v git >/dev/null 2>&1 || die "git is required"
  command -v node >/dev/null 2>&1 || die "node not found; Quartz $QUARTZ_TAG needs Node >= $NEED_NODE_MAJOR (CI uses $NODE_VERSION)"
  command -v npm >/dev/null 2>&1 || die "npm not found; Quartz $QUARTZ_TAG needs npm >= $NEED_NPM"
  local node_v npm_v
  node_v="$(node --version)"; node_v="${node_v#v}"
  npm_v="$(npm --version)"
  version_ge "$node_v" "$NEED_NODE_MAJOR" || die "node $node_v is too old; need >= $NEED_NODE_MAJOR"
  version_ge "$npm_v" "$NEED_NPM" || die "npm $npm_v is too old; need >= $NEED_NPM"
}

ensure_quartz() {
  if [ ! -d "$QUARTZ_DIR/.git" ]; then
    log "cloning Quartz $QUARTZ_TAG into ${QUARTZ_DIR#"$ROOT"/}"
    mkdir -p "$CACHE_DIR"
    rm -rf "$QUARTZ_DIR.partial"
    git -c advice.detachedHead=false clone --quiet --depth 1 --branch "$QUARTZ_TAG" "$QUARTZ_REPO" "$QUARTZ_DIR.partial"
    mv "$QUARTZ_DIR.partial" "$QUARTZ_DIR"
  fi
  local actual
  actual="$(git -C "$QUARTZ_DIR" rev-parse HEAD)"
  [ "$actual" = "$QUARTZ_COMMIT" ] ||
    die "Quartz $QUARTZ_TAG is at $actual but site/versions.env pins $QUARTZ_COMMIT; fix the pin or run '$0 clean'"
}

ensure_deps() {
  local stamp="$QUARTZ_DIR/node_modules/.site-build-stamp"
  local want="$QUARTZ_COMMIT node-$(node --version)"
  if [ ! -f "$stamp" ] || [ "$(cat "$stamp")" != "$want" ]; then
    log "installing Quartz dependencies (npm ci)"
    (cd "$QUARTZ_DIR" && npm ci --no-audit --no-fund)
    printf '%s' "$want" >"$stamp"
  fi
}

overlay_config() {
  cp "$ROOT/site/quartz.config.ts" "$QUARTZ_DIR/quartz.config.ts"
  cp "$ROOT/site/quartz.layout.ts" "$QUARTZ_DIR/quartz.layout.ts"
}

run_quartz() { # run_quartz [extra build flags...]
  [ -f "$CONTENT_DIR/index.md" ] || die "$CONTENT_DIR/index.md not found; is this the wiki repository root?"
  node "$(native_path "$ROOT/scripts/check-frontmatter.mjs")" \
    "$(native_path "$QUARTZ_DIR")" "$(native_path "$CONTENT_DIR")" ||
    die "frontmatter that Quartz cannot parse (see above)"
  if [ -z "${SITE_BASE_URL:-}" ]; then
    unset SITE_BASE_URL
    log "SITE_BASE_URL not set; using the placeholder baseUrl from site/quartz.config.ts"
  else
    export SITE_BASE_URL
  fi
  (cd "$QUARTZ_DIR" && node quartz/bootstrap-cli.mjs build \
    --directory "$(native_path "$CONTENT_DIR")" \
    --output "$(native_path "$OUT_DIR")" \
    "$@")
}

# Defense in depth: public/ must contain only generated site files. Quartz copies
# every non-Markdown file under wiki/ verbatim, so a stray PDF, HTML copy of the
# standard or database would otherwise be published.
verify_output() {
  [ -f "$OUT_DIR/index.html" ] || die "build produced no public/index.html"
  local bad
  bad="$(find "$OUT_DIR" -type f \
    ! -name '*.html' ! -name '*.css' ! -name '*.js' ! -name '*.json' \
    ! -name '*.png' ! -name '*.svg' ! -name '*.ico' ! -name '*.txt' ! -name '*.xml' \
    -print | head -n 20 || true)"
  [ -z "$bad" ] || die "unexpected file types in public/ (not publishable):
$bad"
  [ -z "$(find "$OUT_DIR" -type f -iname '*n4659-cppwp*' -print -quit)" ] ||
    die "public/ contains a copy of the raw standard; remove it from wiki/"
  log "public/: $(find "$OUT_DIR" -type f -name '*.html' | wc -l | tr -d ' ') HTML files"
}

cmd_check() {
  local py
  py="$(find_python)" || die "Python 3.9+ not found (set PYTHON)"
  "$py" -X utf8 "$ROOT/scripts/check_wiki.py" "$CONTENT_DIR" --config "$ROOT/site/quartz.config.ts"
}

cmd_build() {
  require_node
  ensure_quartz
  ensure_deps
  overlay_config
  run_quartz
  verify_output
  log "done: ${OUT_DIR#"$ROOT"/}/"
}

cmd_serve() {
  require_node
  ensure_quartz
  ensure_deps
  overlay_config
  log "serving on http://localhost:${PORT:-8080}/ (Ctrl+C to stop)"
  run_quartz --serve --port "${PORT:-8080}"
}

cmd_clean() {
  rm -rf "$OUT_DIR" "$CACHE_DIR"
  log "removed public/ and .quartz-cache/"
}

case "${1:-}" in
  check) cmd_check ;;
  build) cmd_build ;;
  serve) cmd_serve ;;
  clean) cmd_clean ;;
  *) die "usage: $0 {check|build|serve|clean}" ;;
esac
