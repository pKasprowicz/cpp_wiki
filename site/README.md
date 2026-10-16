# Site build (Quartz)

The wiki in `wiki/` is published as a static site built with [Quartz](https://quartz.jzhao.xyz) v4.
This repository stays a content repository: Quartz is **not** vendored. The build clones the pinned
Quartz release into `.quartz-cache/`, copies the two files from this directory over Quartz's defaults,
and runs Quartz with `wiki/` as the content directory.

| Path | Role |
|---|---|
| `site/quartz.config.ts` | Quartz configuration: title, `baseUrl`, `ignorePatterns`, plugins |
| `site/quartz.layout.ts` | Page layout: search, graph view, backlinks, explorer |
| `site/versions.env` | Pinned Quartz tag and commit, Node version (read by the script and by CI) |
| `scripts/build-site.sh` | The one build script. `check`, `build`, `serve`, `clean` |
| `Makefile` | Thin wrapper: `site-check`, `site-build`, `site-serve`, `site-clean` |
| `scripts/check_wiki.py` | Pre-build gate: wiki lint plus broken-wikilink check |
| `scripts/check-frontmatter.mjs` | Names the file when frontmatter cannot be parsed the way Quartz parses it |
| `scripts/vendor/wiki_lint.py` | Vendored copy of the llm-wiki plugin's lint (see `scripts/vendor/README.md`) |
| `.github/workflows/site.yml` | CI: checks and build on pull requests, deploy on push to `main` |

Generated and never committed: `public/` (the site), `.quartz-cache/` (Quartz checkout and its
`node_modules`), and the wiki artifacts listed in `.gitignore`.

## Build

Needs Node >= 22 with npm >= 10.9.2 (CI uses the version in `site/versions.env`), git, bash and
Python 3.9+. On Windows use Git Bash. `make` is optional.

```bash
make site-build                      # or: bash scripts/build-site.sh build
```

The first run clones Quartz and runs `npm ci` (about 30 s); later runs take a few seconds. Output
goes to `public/`. After the build the script refuses to leave unexpected file types in `public/`
and checks that no copy of the raw standard ended up there.

`SITE_BASE_URL` sets the deployed address (host and optional path, no protocol), for example
`SITE_BASE_URL=wiki.example.com/cpp make site-build`. It only affects canonical and social-card
URLs. Without it the placeholder `example.invalid/cpp-wiki` from `quartz.config.ts` is used. CI
sets it from the Pages address.

## Preview

```bash
make site-serve                      # or: bash scripts/build-site.sh serve
PORT=9000 make site-serve            # another port
```

Serves `http://localhost:8080/` and rebuilds on every change under `wiki/`. Open a concept page
such as `/concepts/one-definition-rule` to see the backlinks and the graph view; the search box
finds terms such as `odr-use`.

## Checks

```bash
make site-check                      # or: bash scripts/build-site.sh check
```

Needs only Python. It runs the vendored `wiki_lint.py` (which always exits 0, so
`check_wiki.py` turns its report into pass/fail) and then resolves every `[[wikilink]]` the way
Quartz does. It **fails** on:

- broken wikilinks, in any published page including `index.md` and `indexes/` (which the lint skips)
- a bare link name shared by two files (ambiguous with shortest-path resolution)
- a link to a page that `ignorePatterns` excludes from the site
- malformed or missing frontmatter fields, duplicate slugs, pages over the 800-line hard cap
- a non-image file under `wiki/` that Quartz would copy into the site as-is

Orphans, pages over the 400-line soft cap and stale pages are warnings. Quartz itself does not fail on
a dead wikilink (it only emits a 404), which is why this step exists. It reads `ignorePatterns`
from `quartz.config.ts`, so keep that array a plain list of string literals.

Frontmatter Quartz cannot parse fails the build; `check-frontmatter.mjs` runs first so the error names the file.

## What is published

Everything under `wiki/` except these `ignorePatterns`: `drafts`, `templates`, `private`, `raw`,
dot-directories (`.wiki`, `.wiki-cache`, `.evolution`, `.obsidian`), `graph/` (compiled graph
artifacts and ontology), and the maintainer files `SCHEMA.md` and `log.md`. The raw standard in
`raw/` lies outside `wiki/` and can never reach the site. `wiki/sources/` **is** published because
the indexes and a dozen pages link to the source summary. A page with `draft: true` in its
frontmatter is dropped.

To publish `SCHEMA.md` or `log.md`, delete them from `ignorePatterns`.

## Bumping the Quartz version

1. Pick the new tag from <https://github.com/jackyzha0/quartz/tags>. Stay on the v4 line:
   v5 uses a different YAML configuration and needs its own port of these two files.
2. Look up the commit it points to:
   `git ls-remote https://github.com/jackyzha0/quartz.git 'refs/tags/vX.Y.Z^{}'` (an annotated tag
   shows the commit on the `^{}` line; a lightweight tag has only the plain line).
3. Put the tag in `QUARTZ_TAG` and the commit in `QUARTZ_COMMIT` in `site/versions.env`. If the new
   release's `package.json` raises the Node requirement, bump `NODE_VERSION` too.
4. Compare upstream's defaults with ours and port anything you want:
   `git -C .quartz-cache/quartz-vOLD diff vOLD vNEW -- quartz.config.ts quartz.layout.ts`
   (run `make site-build` once first so the old checkout exists, then fetch the new tag there with
   `git fetch --depth 1 origin tag vNEW`).
5. `make site-clean site-build`, then type-check the configuration against the new Quartz:
   `cd .quartz-cache/quartz-vNEW && node node_modules/typescript/bin/tsc --noEmit`.
6. Preview with `make site-serve`, then commit `site/` and open a pull request; CI builds it.

The build aborts if the clone's commit differs from `QUARTZ_COMMIT`, so a moved tag cannot change
the output silently. The CI npm cache key includes the commit, so a bump starts a fresh cache.

## CI and deployment

`.github/workflows/site.yml` has three jobs, all running `scripts/build-site.sh`:

- **check** (every pull request and push): lint and wikilink check. Fails the run on any error.
- **build** (after check): builds the site. On `main` it asks GitHub for the Pages address
  (`SITE_BASE_URL`) and uploads `public/` as the Pages artifact.
- **deploy** (push to `main` only): deploys to GitHub Pages.

Pull requests build the site but publish nothing and upload nothing.

**The site must stay private.** It is derived from copyrighted standard text. The deploy job reads
`GET /repos/{owner}/{repo}/pages` and stops unless `public` is exactly `false`. GitHub restricts
Pages to repository readers only on **GitHub Enterprise Cloud**, for project sites published from a
private or internal repository. One-time setup: Settings > Pages > Source "GitHub Actions", then
set the visibility to private. On a plan without private Pages the deploy job fails by design; the
`check` and `build` jobs still run.

Pinned in the workflow: Node via `site/versions.env`, every action by commit SHA, Quartz by tag and
commit. npm downloads are cached with `actions/cache` (Quartz's lockfile is not in this repo, so
`setup-node`'s built-in cache cannot be used). The workflow can be syntax-checked with
[`actionlint`](https://github.com/rhysd/actionlint).

## Known limitations

- **Page titles.** Quartz titles a page after its frontmatter `title:`, or after the file name when
  there is none. `index.md`, `indexes/*.md` and `log.md` carry a one-line `title:` block for this
  reason; give any new navigation page the same, or it will show up as "index", "sources", ...
- **One stray HTML tag.** `concepts/library-requirements-and-conformance.md` line 17 contains a bare
  `<code>` in prose, which the browser renders as an unclosed code element. Writing it as
  `` `<code>` `` fixes it.
- **cdnjs hint.** Quartz 4.5.2 always emits a `preconnect` link to `cdnjs.cloudflare.com`. With the
  options in `quartz.config.ts` no resource is loaded from it, but a browser may open a connection.
- **Heading anchors** in `[[page#heading]]` links are not verified by the check.
- **`wiki/graph/*` is not rebuilt in CI.** The site's graph view is computed by Quartz from the
  links; the files under `wiki/graph/` are not used by it, and `wiki/index.md` is hand-maintained.
- **Windows.** `scripts/build-site.sh` runs under Git Bash. If `make` is not installed, call the
  script directly.
