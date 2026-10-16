---
title: "Wiki Log"
---
# Wiki Log

Append-only chronological record of operations on the wiki. Each entry begins with `## [YYYY-MM-DD] <op> | <description>` so it's parseable with `grep "^## \[" log.md | tail -N`.

Operations:
- `ingest` — a source was processed into the wiki.
- `query` — a question was answered against the wiki (typically only logged when the answer was filed back as synthesis).
- `lint` — a health check was run.
- `schema` — the schema was modified.
- `shard` — an index was sharded.

---

## [2026-10-15] schema | Added C++ tag taxonomy and a "Citing the C++ standard" workflow note to SCHEMA.md
   Retrieval setup recorded earlier today (local FastEmbed + sqlite-vec, verified on the empty wiki).

## [2026-10-15] ingest | Working draft of the C++ standard, C++17 (N4659) — cppwp HTML rendering
   raw: raw/n4659-cppwp-full.html (12,941,278 bytes, sha256 c92f56a2...b4fa; contents page read for the clause map)
   scope: language clauses 4-19 and Annex C.3-C.4 summarized; library clauses 20-33, Annexes A, B, D and clauses 1-3 mapped only
   created: sources/n4659-cpp17-draft-standard + 41 concept pages (17 clause/annex overviews, 24 cross-cutting pages)
   touched: none (wiki was empty); no contradictions
   open: library clauses; page claims not yet spot-checked with wiki_search.py; N-number not printed on the page (identity inferred from URL and `__cplusplus` = 201703L)

## [2026-10-15] ingest | C++17 library clauses 20-33 (N4659, from raw/n4659-cppwp-full.html)
   scope: all fourteen library clauses (~1,450 labelled sections); created 75 concept pages: 14 overviews (cpp17-lib-introduction, -language-support, -diagnostics, -utilities, -strings, -localization, -containers, -iterators, -algorithms, -numerics, -input-output, -regex, -atomics, -thread) + 61 topic pages (e.g. library-requirements-and-conformance, library-named-requirements, allocators, unique-ptr, shared-ptr-and-weak-ptr, optional, variant, any-type, std-function, container-requirements, iterator-invalidation, iterator-categories-and-requirements, algorithm-requirements, locale-class-and-facets, stream-base-classes, filesystem, atomics-and-memory-order, mutexes-and-locks, futures-and-async)
   touched: sources/n4659-cpp17-draft-standard (coverage table, library page list, method/limitations, follow-ups, concepts and tags in frontmatter); concepts/cpp17-compatibility-differences (library entries C.3.6-C.3.7, C.4.8-C.4.12 now tabulated with links); SCHEMA.md (library tag, library conventions, index structure)
   method: throwaway splitter in the session scratchpad (HTML -> section index with notes/examples/footnotes stripped); reading depth varied: container/iterator/algorithm/smart-pointer/concurrency text read paragraph by paragraph, repetitive facet/distribution/special-function/filesystem-operation descriptions skimmed (see source page "Method and limitations")
   verified-against-source corrections made during writing: exception-class base classes, errc count (78), shared-mutex shared-owner limit (>= 10000, excess callers block), `file_size` error value, `endl`/`ends` behavior, regex_iterator zero-length-match handling, string hash equals string_view hash
   open: per-signature coverage is deliberately not attempted; Annex A, B, D and clauses 1-3 still unsummarized; Annex D holds items the library pages refer to (old allocator members, result_of, uncaught_exception, iostream members); page claims not systematically spot-checked with wiki_search.py (only a few retrieval queries were run)
   graph: regenerated after the ingest — 117 nodes, 1158 edges (1041 mentions, 116 sourced_from, 1 summarizes_raw); graph lint clean; no typed `graph:` relationships were added
   checks: wiki_lint.py clean (117 pages, no broken links/orphans/oversize); setup_wiki.py --cache ready (820 sections, 820 vectors)

## [2026-10-15] shard | Index split into wiki/indexes/ (sources, concepts-language, three concepts-library-*, empty entities and synthesis shards); wiki/index.md is now a directory with counts and quick routes
   reason: task asked for sharded index after the library ingest (117 pages, ~190 index lines; playbook thresholds of 150 pages / 300 lines not yet crossed); SCHEMA.md "Index structure" updated

## [2026-10-15] schema | Added the `library` tag, library citation/naming conventions and the shard table to SCHEMA.md

## [2026-10-15] ingest | C++17 clauses 1-3 and Annexes A, B, D (N4659, from raw/n4659-cppwp-full.html)
   scope: clause 1 Scope, 2 Normative references, 3 Terms and definitions; Annex A grammar summary (all 291 productions); Annex B implementation quantities (43 items); Annex D compatibility features (D.1-D.16); created 8 concept pages: cpp17-glossary, cpp17-grammar-summary, grammar-lexical-and-preprocessing, grammar-expressions-and-statements, grammar-declarations-and-classes, implementation-quantities, cpp17-annex-d-compatibility-features, deprecated-library-facilities
   touched: sources/n4659-cpp17-draft-standard (coverage table rows 1-3, A, B, D; new "Front clauses and annexes" section; method and follow-ups; concepts and tags in frontmatter); SCHEMA.md (tags `grammar` and `deprecated`, Annex page conventions, shard table, page counts); index.md and indexes/sources.md (counts, quick routes, coverage line); new shard indexes/concepts-glossary-grammar-annexes.md; one-line "Related" links added to 31 existing pages (allocators, exception-support, type-traits, library-requirements-and-conformance, function-objects-and-invoke, shared-ptr-and-weak-ptr, uninitialized-memory-algorithms, iterator-adaptors, iterator-categories-and-requirements, locale-class-and-facets, locale-standard-facets, string-and-file-streams, stream-buffers, cpp17-lib-introduction, cpp17-classes, cpp17-special-member-functions, cpp17-exception-handling, cpp17-lexical-conventions, cpp17-preprocessing-directives, cpp17-expressions, cpp17-statements, cpp17-declarations, cpp17-declarators, cpp17-templates, cpp17-overloading, cpp17-derived-classes, abstract-machine-and-observable-behavior, program-startup-and-termination, constant-expressions, cpp17-compatibility-differences, cpp17-general-principles)
   method: throwaway splitter (HTML -> section index, once with and once without notes/examples) in the session scratchpad; Annex A productions compressed mechanically into one-line notation by a second throwaway script (two manual fixes: the wrapped lambda-declarator alternative and the `()` / `[]` operator tokens); Annex B numbers checked programmatically against the source (43/43); labels used on the new pages checked against the section index
   findings: LIA-1 is defined in `[intro.refs]` but used nowhere else in the draft text; the draft's `[depr.str.strstreams]/1` says `<strstream>` defines three types while D.6.1-D.6.4 define four classes; Annex D no longer holds `unary_function`, `ptr_fun`, `bind1st` etc. (Annex C.4.12 records the removal, also of `[depr.ios.members]`); `__has_include` is part of the A.14 grammar
   open: Annex C.1 (C++ and ISO C), C.2 (C++ and ISO C++ 2003) and C.5 (C standard library) still unsummarized (~6,500 words); Annex D function-level wording summarized at class level only; claims not systematically spot-checked with wiki_search.py beyond four retrieval queries
   graph: regenerated (125 nodes, 1387 edges, lint clean); checks: wiki_lint.py clean (125 pages); setup_wiki.py --cache ready (906 sections, 906 vectors)

## [2026-10-16] ingest | C++17 Annex C.1, C.2 and C.5 (N4659, from raw/n4659-cppwp-full.html)
   scope: C.1 C++ and ISO C (`[diff.iso]`, 33 entries, C.1.1-C.1.10), C.2 C++ and ISO C++ 2003 (`[diff.cpp03]`, 37 entries, C.2.1-C.2.16 incl. library), C.5 C standard library (`[diff.library]`); this completes the draft: every clause and annex is now summarized. Created 2 concept pages: cpp-vs-c-differences, cpp03-differences
   touched: library-requirements-and-conformance (new section on Annex C.5: headers, definitions, declarations, behavior, `offsetof`, allocation functions; the sections C.5 points to were read too); cpp17-compatibility-differences (retitled, Annex C map table, open question and Related updated); sources/n4659-cpp17-draft-standard (coverage row for Annex C, Annex C line in the page lists, method note, follow-up 2, tags/concepts in frontmatter); SCHEMA.md (shard table, Annex C conventions, page counts); index.md and indexes/{concepts-glossary-grammar-annexes,concepts-language,concepts-library-foundations,sources}.md (new section, counts 8->10, quick route); one-line Related links on cpp17-annex-d-compatibility-features, cpp17-lexical-conventions, cpp17-lib-introduction
   method: throwaway splitter in the session scratchpad (copy of the earlier notes-keeping HTML splitter, outputs per-section text with notes/examples); Annex C read in full; cited labels checked programmatically against the section index (all found; three library labels containing `::` only differ by soft hyphens in the heading text); entries paraphrased, annex "how widely used" verdicts kept as labels
   findings: Annex C says "ISO C" without an edition (normative reference is C11, rationale text reads older); C.2.8's new-header list omits `<optional>`, `<variant>`, `<any>`, `<string_view>`, `<filesystem>`, `<memory_resource>`, `<execution>` (none appear anywhere in Annex C); the C.2.9 example still uses `throw(std::bad_alloc)`, which C.4.7 says is now ill-formed; the C.2.8 `swap` entry prints "Effect on original feature" where "Change" is expected; C.1's `[stmt.return]` entry says "invalid" while the normative rule makes flowing off the end undefined behavior
   open: C.1 and C.2 entries not checked against later standards (out of scope for this source); the wiki has not been spot-checked with wiki_search.py beyond the structural lint
   graph: regenerated (127 nodes, 1464 edges, lint clean); checks: wiki_lint.py clean (127 pages); setup_wiki.py --cache ready (944 sections, 944 vectors)
