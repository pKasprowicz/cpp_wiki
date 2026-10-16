// Parse every page's frontmatter exactly the way Quartz's FrontMatter plugin does
// (gray-matter with js-yaml's JSON_SCHEMA) and report each failure with its file name.
//
// Why: Quartz stops the build on frontmatter it cannot parse, but its own error text
// can be unhelpful (on Windows it prints "ERR_INVALID_URL_SCHEME" without naming the
// file). The wiki lint cannot catch this either, because it uses a hand-written parser.
//
// Usage: node scripts/check-frontmatter.mjs <quartz-checkout-dir> <content-dir>
// gray-matter and js-yaml are resolved from the Quartz checkout's node_modules, so this
// needs no dependencies of its own and runs from scripts/build-site.sh after `npm ci`.

import { createRequire } from "node:module"
import fs from "node:fs"
import path from "node:path"

const [quartzDir, contentDir] = process.argv.slice(2)
if (!quartzDir || !contentDir) {
  console.error("usage: node check-frontmatter.mjs <quartz-checkout-dir> <content-dir>")
  process.exit(2)
}

const require = createRequire(path.join(path.resolve(quartzDir), "package.json"))
const matter = require("gray-matter")
const yaml = require("js-yaml")
const toml = require("toml")

function* markdownFiles(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".")) continue // Quartz skips dot-files and dot-directories
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) yield* markdownFiles(full)
    else if (entry.isFile() && entry.name.endsWith(".md")) yield full
  }
}

let checked = 0
let failed = 0
for (const file of markdownFiles(path.resolve(contentDir))) {
  checked++
  try {
    matter(fs.readFileSync(file, "utf8"), {
      engines: {
        yaml: (s) => yaml.load(s, { schema: yaml.JSON_SCHEMA }),
        toml: (s) => toml.parse(s),
      },
    })
  } catch (err) {
    failed++
    const rel = path.relative(path.resolve(contentDir), file).split(path.sep).join("/")
    const message = String(err && err.message ? err.message : err).split("\n")[0]
    console.error(`  ERROR: wiki/${rel}: frontmatter Quartz cannot parse: ${message}`)
    if (process.env.GITHUB_ACTIONS === "true") {
      console.error(`::error file=wiki/${rel}::frontmatter Quartz cannot parse: ${message}`)
    }
  }
}
console.log(`frontmatter: ${checked} files checked, ${failed} unparseable`)
process.exit(failed ? 1 : 0)
