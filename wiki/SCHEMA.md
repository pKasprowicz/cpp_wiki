# Wiki Schema

This file is the configuration for this wiki. It documents the conventions, page types, tag taxonomy, and any workflow customizations. The LLM reads this first when entering the wiki, and its conventions override the defaults documented in the `llm-wiki` skill.

This file is **co-evolved with the user**. When the LLM notices a recurring pattern in your edits or feedback that isn't here, it will propose adding it. When something here stops fitting, prune it.

## Wiki location

- Wiki root: `wiki/`
- Raw sources: `raw/`
- Asset/image storage: `raw/assets/`

## Page types

This wiki uses these page types, each with a dedicated subdirectory:

- `source` (in `wiki/sources/`) — one summary page per ingested source.
- `entity` (in `wiki/entities/`) — pages about specific things: people, papers, products, places, organizations.
- `concept` (in `wiki/concepts/`) — pages about ideas, methods, frameworks, abstractions.
- `synthesis` (in `wiki/synthesis/`) — cross-cutting analyses, comparisons, query answers filed back.

Add additional types here as the wiki evolves.

## Tag taxonomy

Keep this list small and disciplined — a wiki with 200 tags has effectively no tags.

- `cpp17` — content taken from the C++17 draft N4659; pages about other standards would use their own edition tag (`cpp20`, ...).
- `language-core` — core language (clauses 4-19 of N4659).
- `grammar` — Annex A lookup pages (compact productions; see the page `cpp17-grammar-summary`).
- `deprecated` — pages about the deprecated features of Annex D.
- `library` — standard library (clauses 20-33 of N4659). Library overview pages are `cpp17-lib-<topic>`; topic pages use plain slugs (`unique-ptr`, `iterator-invalidation`). Pages that mix library and cross-clause analysis also carry `cross-cutting`.
- `standard-clause` — a per-clause overview page (`cpp17-...` slug) with a section map.
- `cross-cutting` — a page that collects rules from several clauses around one topic.
- `undefined-behavior` — page documents where the standard makes behavior undefined or ill-formed with no diagnostic required.
- `concurrency` — memory model, threads, data races.
- `templates` — template mechanics (deduction, instantiation, folds).
- `open-question` — pages or sections that flag unresolved questions.
- `contested` — pages where sources contradict (none yet).

## Page sizing

- Soft cap: 400 lines / ~2,000 words. Consider splitting beyond this.
- Hard cap: 800 lines. Must split.

## Frontmatter requirements

Every page must have:
- `type`
- `title`
- `tags`
- `created`
- `updated`

Plus type-specific:
- `source` pages: `authors`, `url` (if applicable), `raw`, `ingested`
- Non-source pages: `sources` listing the source-summary pages drawn from

## Optional graph metadata

Pages may declare typed graph metadata under a top-level `graph:` key. This is the source of truth for the compiled knowledge graph under `wiki/graph/`. Markdown remains canonical; the graph is a regenerable index. Pages without `graph:` still appear as nodes (derived from `type`/`kind`) and still contribute `mentions` edges from body `[[wikilinks]]`.

```yaml
graph:
  node_id: person:praney-behl       # optional; default <node_type>:<slug>
  node_type: person                  # optional; default mapped from type/kind via ontology
  canonical: true                    # mark as canonical when multiple slugs alias the same entity
  aliases: [Praney, praney@example.com]
  relationships:
    - predicate: founded
      object: company:seedblocks
      source: praney-founder-context-dump   # source-page slug
      evidence: "Solo technical founder and sole director..."
      confidence: high               # high | medium | low
      status: current                # current | historical | proposed | disputed | superseded
      # optional:
      # valid_from: 2025-01-15
      # valid_to: 2026-03-01
      # notes: "..."
      # raw_ref: "raw/founder-dump.md#L42"
      # contradicts: edge-id-or-source-slug
      # supersedes: edge-id-or-source-slug
```

Required fields on every relationship: `predicate`, `object`, `source`, `evidence`, `confidence`, `status`. Predicates and the subject/object types they accept are declared in `wiki/graph/ontology.yaml`. Typed semantic edges must be supported by an explicit source — never emit one inferred from training data alone.

## Index structure

**Sharded** (2026-10-15, when the library clauses took the wiki from 42 to 117 pages). `wiki/index.md` is now a small directory of shards with page counts and quick routes; the one-line entries live in `wiki/indexes/`:

| Shard | Contents |
|---|---|
| `indexes/sources.md` | source summary pages |
| `indexes/concepts-language.md` | core-language concept pages (clauses 4-19, Annex C) |
| `indexes/concepts-library-foundations.md` | library clauses 20-24 (introduction, language support, diagnostics, utilities, strings) |
| `indexes/concepts-library-containers-algorithms.md` | clauses 26-28 (containers, iterators, algorithms) |
| `indexes/concepts-library-text-io-numerics-concurrency.md` | clauses 25 and 29-33 (localization, numerics, I/O and filesystem, regex, atomics, threads) |
| `indexes/concepts-glossary-grammar-annexes.md` | clauses 1-3 glossary, Annex A grammar lookups, Annex B quantities, Annex C differences from C and C++03, Annex D deprecated features (added when the front clauses and annexes were ingested; the Annex C hub `cpp17-compatibility-differences` stays in the language shard) |
| `indexes/entities.md`, `indexes/synthesis.md` | currently empty |

When adding a page: add its line to the matching shard and bump the count in `index.md`. If a shard passes ~300 lines, split it by sub-topic (as the library shards split the concepts type). New pages for a new clause family or a new source get their own shard rather than growing an existing one past that size. The sharding was done because the ingest task called for it; the playbook thresholds (~150 pages / 300 index lines) were not yet reached (117 pages, ~190 index lines; 125 pages and ~215 index lines after the clauses 1-3 and Annex A, B, D ingest; 127 pages after Annex C.1, C.2, C.5).

## Retrieval

- Search is section-level hybrid by default: `uv run --script skills/llm-wiki/scripts/wiki_search.py "query" --json`.
- Semantic backend: local FastEmbed + sqlite-vec (`BAAI/bge-small-en-v1.5`, 384 dimensions). No wiki or query text leaves the machine.
- First semantic use downloads model artifacts to `~/.cache/llm-wiki/fastembed/`; set `FASTEMBED_CACHE_PATH` to override the model cache.
- Semantic setup verified: 2026-10-16 (re-run after the Annex C.1, C.2, C.5 ingest: 127 pages, 944 sections, 944 vectors; the run after the clauses 1-3 and Annex A, B, D ingest had 125 pages, 906 sections, 906 vectors; the run after the library ingest had 117 pages, 820 sections; earlier run on the empty wiki was idempotent)
- `wiki/.wiki-cache/` holds regenerable retrieval artifacts: `search-index.json` (parse cache) and `embeddings.sqlite` (section metadata + sqlite-vec vectors). Safe to delete; never edit by hand; gitignored.
- The vector index is content-hashed: only new or changed sections are re-embedded, deleted sections are removed, and model/schema changes rebuild it automatically.
- Dependency-free lexical path: `python skills/llm-wiki/scripts/wiki_search.py "query" --no-embed` (direct Python bypasses PEP 723 dependency resolution). A missing or failed local backend also falls back to lexical search without failing the command.

## Graph layer

The wiki has an optional compiled graph layer under `wiki/graph/`:

- `wiki/graph/ontology.yaml` — declares node types and predicates. **Tracked.** Edit this when you introduce new predicates or domain types.
- `wiki/graph/nodes.jsonl`, `wiki/graph/edges.jsonl` — generated. Track in git only if you want graph diffs in PRs.
- `wiki/graph/graph.sqlite` — generated. Gitignored by default.
- `wiki/graph/graph.graphml` — generated. Track only if you want to diff it.

Generation is reproducible from markdown via `scripts/wiki_graph_extract.py`. The graph can be deleted at any time and rebuilt without losing knowledge — markdown is canonical.

## Workflow customizations

### Citing the C++ standard

- Cite by **stable section label plus paragraph**, in backticks: `[basic.def.odr]/6`. Backticks keep these from being read as links; `[[wikilinks]]` are reserved for wiki pages.
- Pages **paraphrase** the standard; do not paste its wording. Short defined terms are fine.
- Per-clause overview pages use the slug `cpp17-<topic>` and carry a section-map table; cross-cutting topics use plain topic slugs and cite every clause they draw on.
- When a rule is stated only in an informative note or example, say so on the page (for example the warning behavior of the `nodiscard` attribute). Write attribute names without brackets: double square brackets are wikilink syntax and trip the lint script.
- Do not label something "new in C++17" unless a source says so (Annex C of the draft lists incompatibilities only; see `cpp17-compatibility-differences`).
- **Library pages**: the library clauses use plain-identifier named requirements (`CopyConstructible`, `Allocator`, `Hash`, `BasicLockable`, ...); write them as printed, in code font, and link [[library-named-requirements]] rather than redefining them. Mark anything stated only in a note or example, and say so when a claim is an inference rather than a quotation of a rule (for example the "after the insertion point" case on [[iterator-invalidation]]). Library-wide rules (what a program may not do, what implementations may do) are on [[library-requirements-and-conformance]]; do not repeat them on every class page.
- **Annex C pages** (`cpp-vs-c-differences`, `cpp03-differences`, `cpp17-compatibility-differences`) key every entry by the draft's own label (`[lex.key]`, `[diff.*]`) and keep the annex's "how widely used" verdicts as labels. Annex C compares with "this International Standard" and does not say which edition made a change, so these pages say "since C++03" and never attribute an entry to C++11, C++14 or C++17. C.5 is a section of `library-requirements-and-conformance`, not a page of its own.
- **Annex pages**: the Annex A pages restate the grammar in a compact one-line notation (nonterminals plain, tokens in code font, a question mark for optional parts, a broken bar between alternatives; legend on the page `cpp17-grammar-summary`) and were generated from the raw file by a throwaway script; the attribute introducer is written as two separate bracket tokens, never as adjacent brackets. Annex D pages cite `[depr.*]` labels and say when a claim comes only from a note or example; they report what this draft says and what Annex C.4.12 records as removed, not what later editions did.
- Wikilink hazard in library text: the POSIX bracket-expression atoms of the regex grammar, attribute names and `[[...]]` in code all collide with wikilink syntax. Describe them in words (see [[regex-classes-and-algorithms]]).
- Raw copy of the standard lives at `raw/n4659-cppwp-full.html`; extraction scripts are throwaway and not stored in the wiki. Retrieval into section-sized chunks is the job of `wiki_search.py`.

## User preferences

(Empty initially. As the user expresses style preferences — "always include a 'Why this matters' section on concept pages", "never use bullet lists in summaries", "prefer comparative tables for synthesis pages" — capture them here so they persist across sessions.)

## Lint cadence

- Structural lint: after every 5 ingests.
- Semantic lint: weekly or after every 20 ingests.
- Gap-finding: monthly.
- Graph lint + extract: after every ingest that adds typed `graph.relationships`.

Adjust based on the wiki's growth rate.

## Skill evolution

Optional: capture verified task experience with `/wiki:learn` and propose tested procedural improvements with `/wiki:evolve`. Existing pages and workflows do not change. Raw experience JSON lives under the configured raw root's `experiences/` directory and is immutable. Consolidate observations into ordinary source/concept pages with evidence, applicability, model/tool versions and counterexamples. Optional pattern fields are `kind: experience-pattern` and `status: hypothesis|supported|superseded`.

`wiki/.evolution/` holds durable experiment snapshots, evidence, diffs and measured outcomes; it is not a cache. Wiki search, lint, stats and graph extraction exclude it. Keep searchable summaries in normal synthesis pages linked to the source/pattern pages and index. Private records must not be published with shared skills.

Candidate edits remain isolated until reviewed, selected on validation tasks, independently measured on untouched final-test tasks, and explicitly applied within the user's authorization. Failed edits leave the active skill unchanged while their records persist. Do not repeat a rejected proposal without new evidence or changed conditions. Keep factual wiki access during normal work; do not inject experiment history into task execution. Correct unsupported lessons without deleting their raw evidence. Follow the installed skill's `references/evolution-workflow.md` for the runner contract, cost limits and recovery.
