# Vendored files

## wiki_lint.py

Unmodified copy of `skills/llm-wiki/scripts/wiki_lint.py` from the **llm-wiki** Claude plugin.

| | |
|---|---|
| Upstream | https://github.com/praneybehl/llm-wiki-plugin |
| Version | 3.2.0 (plugin `package.json` / `plugin.json`) |
| SHA-256 | `2d2b8c9e50a4022eb65ced4f416eaead9765795553697306cc1b354f98143f1b` |
| Licence | MIT, Copyright (c) 2026 Praney Behl (text below) |
| Dependencies | Python 3.9+ standard library only |

**Why it is vendored.** CI cannot reach the plugin cache on a developer machine, and the plugin
is not installable on a hosted runner, so CI needs its own copy. `scripts/check_wiki.py` runs it.

**Why a wrapper is needed.** `wiki_lint.py` reports findings but always exits 0, and it does not
look at `index.md`, `indexes/`, `SCHEMA.md`, `log.md` or `graph/` when checking links.
`scripts/check_wiki.py` turns its JSON report into a pass/fail result and adds its own
wikilink check for every published page.

**Updating.** Copy the new file over `wiki_lint.py` unchanged, update the version and SHA-256 above,
then run `bash scripts/build-site.sh check`. Do not edit the vendored file; put policy in
`check_wiki.py`.

### MIT License

Copyright (c) 2026 Praney Behl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
