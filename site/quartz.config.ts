import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 configuration for the C++ Standard Wiki.
 *
 * This file lives in site/ and is copied over the checked-out Quartz's own
 * quartz.config.ts by scripts/build-site.sh. It is evaluated inside the Quartz
 * checkout, so the imports above refer to Quartz's source, not to this repo.
 * Reference: https://quartz.jzhao.xyz/configuration
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "C++ Standard Wiki",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    // The site is access-controlled: no third-party analytics.
    analytics: null,
    locale: "en-US",
    // Host plus optional path, no protocol, no trailing slash.
    // TODO(user): set the real address. CI passes it in SITE_BASE_URL (from
    // actions/configure-pages on GitHub); the placeholder below never resolves.
    baseUrl: process.env.SITE_BASE_URL || "example.invalid/cpp-wiki",
    // Globs relative to the content directory (wiki/). Dot-directories are
    // skipped by Quartz regardless; they are listed to make the intent explicit.
    // scripts/check_wiki.py parses this array to decide which pages are published,
    // so keep it a plain array of string literals.
    ignorePatterns: [
      "drafts",
      "templates",
      "private",
      "raw",
      ".wiki",
      ".wiki-cache",
      ".evolution",
      ".obsidian",
      // Compiled graph artifacts and ontology config, not readable content.
      // (Quartz's graph view is computed from wikilinks and does not use them.)
      "graph",
      // Maintainer-facing files: conventions and the operations log.
      "SCHEMA.md",
      "log.md",
    ],
    defaultDateType: "modified",
    theme: {
      // Local fonts and no CDN: the site makes no third-party requests.
      fontOrigin: "local",
      cdnCaching: false,
      typography: {
        header: "system-ui",
        body: "system-ui",
        code: "ui-monospace",
      },
      colors: {
        lightMode: {
          light: "#faf8f8",
          lightgray: "#e5e5e5",
          gray: "#b8b8b8",
          darkgray: "#4e4e4e",
          dark: "#2b2b2b",
          secondary: "#284b63",
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#fff23688",
        },
        darkMode: {
          light: "#161618",
          lightgray: "#393639",
          gray: "#646464",
          darkgray: "#d4d4d4",
          dark: "#ebebec",
          secondary: "#7b97aa",
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      // Pages carry created/updated in frontmatter. No "git" source: the build
      // does not run inside a full clone of the content history.
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      // Wikilinks and backlinks need this plugin. The Obsidian extras below are
      // switched off because they rewrite plain C++ prose: ==x== becomes a
      // highlight, %% hides text, -> / => become arrows, #word becomes a tag,
      // and mermaid pulls a script from a CDN.
      Plugin.ObsidianFlavoredMarkdown({
        enableInHtmlEmbed: false,
        comments: false,
        highlight: false,
        parseArrows: false,
        parseTags: false,
        mermaid: false,
      }),
      // Smart punctuation would turn "--" and straight quotes in prose into typographic characters.
      Plugin.GitHubFlavoredMarkdown({ enableSmartyPants: false }),
      Plugin.TableOfContents(),
      // Wikilinks resolve by shortest unique file name, e.g. [[one-definition-rule]]
      // finds concepts/one-definition-rule.md. A name shared by two files is
      // ambiguous and is rejected by scripts/check_wiki.py.
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      // contentIndex.json (feeds the built-in full-text search and the graph) is
      // always written; sitemap and RSS are for crawlers and feed readers, which
      // a private site does not want.
      Plugin.ContentIndex({
        enableSiteMap: false,
        enableRSS: false,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Plugin.CustomOgImages() is omitted: it downloads fonts at build time and
      // social preview cards are of no use on a private site.
    ],
  },
}

export default config
