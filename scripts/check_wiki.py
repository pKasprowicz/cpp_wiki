#!/usr/bin/env python3
"""check_wiki.py - pre-build gate for the published wiki (stdlib only, Python 3.9+).

Run by `scripts/build-site.sh check`, locally and in CI, before the site is built.
Exits 1 when any check fails. Two parts:

1. Wiki lint. Runs the vendored scripts/vendor/wiki_lint.py in --json mode, which
   itself always exits 0, and fails on: broken wikilinks, malformed or missing
   frontmatter, duplicate slugs, unreadable files, pages over the hard size cap.
   Orphan pages, pages over the soft cap and stale pages are printed as warnings.
   The lint does not look at index.md, indexes/, SCHEMA.md, log.md or graph/.

2. Publish check. Mirrors how Quartz (markdownLinkResolution: "shortest") resolves
   links, for every page Quartz will publish (so index.md and indexes/*.md are
   included). Quartz itself does not fail the build on a dead link; it just emits a
   404. Fails on: a [[wikilink]] with no target, a bare name that matches more than
   one file, a link whose only target is excluded by ignorePatterns, and any
   non-image file under wiki/ that Quartz would copy into the site verbatim.

The ignorePatterns list is read from site/quartz.config.ts so there is one source
of truth.

Usage: check_wiki.py [WIKI_DIR] [--config site/quartz.config.ts]
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINT = HERE / "vendor" / "wiki_lint.py"

LINT_FAIL = {
    "broken_links": "broken wikilink",
    "malformed_frontmatter": "malformed frontmatter",
    "missing_frontmatter": "missing frontmatter fields",
    "duplicate_slugs": "duplicate slug",
    "read_errors": "unreadable file",
    "oversized_hard": "page over the hard size cap",
}
LINT_WARN = {
    "orphans": "orphan page (no inbound link from another page)",
    "oversized_soft": "page over the soft size cap",
    "stale_pages": "stale page",
}

# Quartz's own wikilink grammar (quartz/plugins/transformers/ofm.ts).
WIKILINK_RE = re.compile(
    r"(!?)\[\[([^\[\]|#\\]+)?(#+[^\[\]|#\\]+)?(\\?\|[^\[\]#]+)?\]\]"
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")

# Non-Markdown files Quartz copies into the site as-is. Anything else under wiki/
# (a PDF or HTML copy of the standard, a database, ...) must not be published.
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


class Report:
    def __init__(self) -> None:
        self.errors = 0
        self.warnings = 0
        self.github = os.environ.get("GITHUB_ACTIONS") == "true"

    def _emit(self, level: str, msg: str, file: str | None, line: int | None) -> None:
        where = f"{file}:{line}: " if file and line else (f"{file}: " if file else "")
        print(f"  {level}: {where}{msg}")
        if self.github:
            props = f"file={file}" if file else ""
            if file and line:
                props += f",line={line}"
            print(f"::{'error' if level == 'ERROR' else 'warning'} {props}::{msg}")

    def error(self, msg: str, file: str | None = None, line: int | None = None) -> None:
        self.errors += 1
        self._emit("ERROR", msg, file, line)

    def warn(self, msg: str, file: str | None = None, line: int | None = None) -> None:
        self.warnings += 1
        self._emit("WARN", msg, file, line)


# --------------------------------------------------------------------------- lint


def run_lint(wiki: Path, rep: Report) -> None:
    print("== wiki lint (vendored wiki_lint.py)")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(LINT), str(wiki), "--json"],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    if proc.returncode != 0:
        rep.error(f"wiki_lint.py exited with {proc.returncode}: {proc.stderr.strip()}")
        return
    try:
        findings = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        rep.error(f"could not parse wiki_lint.py output: {exc}")
        return
    total = findings["summary"]["total_pages"]
    print(f"  {total} pages linted")
    if total == 0:
        rep.error("wiki_lint.py found no pages; is the wiki directory right?")
    for key, label in LINT_FAIL.items():
        for item in findings.get(key, []):
            rep.error(f"{label}: {_describe(item)}", item.get("path") or item.get("from_path"))
    for key, label in LINT_WARN.items():
        for item in findings.get(key, []):
            rep.warn(f"{label}: {_describe(item)}", item.get("path"))


def _describe(item: dict) -> str:
    if "to" in item:
        return f"[[{item['to']}]] (from {item['from_path']})"
    if "missing" in item:
        return ", ".join(item["missing"])
    if "paths" in item:
        return f"{item['slug']} in {', '.join(item['paths'])}"
    if "lines" in item:
        return f"{item['lines']} lines"
    return item.get("path") or item.get("slug") or json.dumps(item)


# ----------------------------------------------------------------- publish check


def read_ignore_patterns(config: Path) -> list[str]:
    text = config.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)  # block comments
    text = re.sub(r"//[^\n]*", "", text)  # line comments
    m = re.search(r"ignorePatterns\s*:\s*\[(.*?)\]", text, flags=re.S)
    if not m:
        raise SystemExit(f"check_wiki: no ignorePatterns array found in {config}")
    body = m.group(1)
    patterns = re.findall(r'"([^"]*)"', body)
    leftover = re.sub(r'"[^"]*"|[,\s]', "", body)
    if leftover:
        raise SystemExit(
            f"check_wiki: ignorePatterns in {config} must be plain string literals (found {leftover!r})"
        )
    return patterns


def is_ignored(rel: str, patterns: list[str]) -> bool:
    """Approximation of Quartz's globby `ignore` plus its default dot:false."""
    parts = rel.split("/")
    if any(p.startswith(".") for p in parts):
        return True
    for i in range(1, len(parts) + 1):
        prefix = "/".join(parts[:i])
        for pat in patterns:
            if pat.startswith("**/"):
                sub = pat[3:]
                if fnmatch.fnmatchcase(prefix, sub) or fnmatch.fnmatchcase(prefix, "*/" + sub):
                    return True
            elif fnmatch.fnmatchcase(prefix, pat):
                return True
    return False


def sluggify(segment: str) -> str:
    """Close enough to Quartz's github-slugger based sluggify for this wiki's file names."""
    s = segment.replace(" ", "-").replace("&", "-and-").replace("%", "-percent")
    s = s.replace("?", "").replace("#", "")
    return re.sub(r"[^\w\-]", "", s.lower())


def file_slug(rel: str) -> str:
    """Quartz slug of a content file: no .md, each segment slugged, extensions of assets kept."""
    if rel.lower().endswith(".md"):
        rel = rel[:-3]
        return "/".join(sluggify(p) for p in rel.split("/"))
    head, _, name = rel.rpartition("/")
    stem, dot, ext = name.rpartition(".")
    name = sluggify(stem) + dot + ext.lower() if dot else sluggify(name)
    return f"{head}/{name}" if head else name


def link_slug(target: str) -> str:
    target = target.strip().replace("\\", "/").strip("/")
    if target.lower().endswith(".md"):
        target = target[:-3]
    return "/".join(sluggify(p) if "." not in p else file_slug(p) for p in target.split("/"))


def extract_links(text: str):
    """Yield (line_number, is_embed, target, has_anchor) for wikilinks outside code and frontmatter."""
    lines = text.split("\n")
    i = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i = j + 1
                break
    in_fence = False
    for n in range(i, len(lines)):
        line = lines[n]
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)
        for m in WIKILINK_RE.finditer(line):
            target = m.group(2)
            if target is None:  # [[#heading]]: a link within the same page
                continue
            yield n + 1, m.group(1) == "!", target, bool(m.group(3))


def publish_check(wiki: Path, config: Path, rep: Report) -> None:
    print("== publish check (Quartz link resolution, all published pages)")
    patterns = read_ignore_patterns(config)
    print(f"  ignorePatterns: {', '.join(patterns)}")

    published: dict[str, str] = {}  # slug -> relative path
    ignored: dict[str, str] = {}
    pages: list[str] = []
    for path in sorted(wiki.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(wiki).as_posix()
        slug = file_slug(rel)
        if is_ignored(rel, patterns):
            ignored.setdefault(slug, rel)
            continue
        if rel.lower().endswith(".md"):
            pages.append(rel)
        elif path.suffix.lower() not in ASSET_EXTENSIONS:
            rep.error(
                "non-Markdown file would be copied into the site verbatim; "
                "remove it or add it to ignorePatterns",
                f"wiki/{rel}",
            )
        if slug in published:
            rep.error(f"slug collision with wiki/{published[slug]}", f"wiki/{rel}")
        published[slug] = rel

    if "index" not in published:
        rep.error("wiki/index.md is missing; the site would have no home page")

    by_filename: dict[str, list[str]] = {}
    for slug in published:
        by_filename.setdefault(slug.rsplit("/", 1)[-1], []).append(slug)
    ignored_names = {s.rsplit("/", 1)[-1] for s in ignored}

    checked = 0
    anchors = 0
    for rel in pages:
        text = (wiki / rel).read_text(encoding="utf-8")
        for line, _embed, target, has_anchor in extract_links(text):
            checked += 1
            anchors += has_anchor
            slug = link_slug(target)
            if "/" in slug:
                ok = slug in published
                ambiguous = False
            else:
                matches = by_filename.get(slug, [])
                ok = len(matches) == 1
                ambiguous = len(matches) > 1
            if ok:
                continue
            where = f"wiki/{rel}"
            if ambiguous:
                rep.error(f"[[{target}]] is ambiguous: {', '.join(sorted(by_filename[slug]))}", where, line)
            elif slug in ignored or slug.rsplit("/", 1)[-1] in ignored_names:
                rep.error(f"[[{target}]] points to a page excluded by ignorePatterns", where, line)
            else:
                rep.error(f"[[{target}]] does not match any published page", where, line)
    print(f"  {len(pages)} published pages, {checked} wikilinks checked")
    if anchors:
        print(f"  note: {anchors} links carry a #heading anchor; the heading itself is not verified")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("wiki", nargs="?", type=Path, default=HERE.parent / "wiki")
    ap.add_argument("--config", type=Path, default=HERE.parent / "site" / "quartz.config.ts")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass
    if not args.wiki.is_dir():
        print(f"check_wiki: wiki directory not found: {args.wiki}", file=sys.stderr)
        return 2
    if not args.config.is_file():
        print(f"check_wiki: Quartz config not found: {args.config}", file=sys.stderr)
        return 2

    rep = Report()
    run_lint(args.wiki, rep)
    publish_check(args.wiki, args.config, rep)
    print(f"\n{rep.errors} error(s), {rep.warnings} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
