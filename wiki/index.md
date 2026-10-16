---
title: "Wiki Index"
---
# Wiki Index

Directory of index shards. The index was sharded on 2026-10-15 when the C++17 library clauses (20-33) took the wiki from 42 to 117 pages (125 after clauses 1-3 and Annexes A, B, D were added; 127 after Annex C.1, C.2 and C.5); each shard keeps one line per page with a short summary. Read the shard that matches your question, then open only the pages you need. If no shard surfaces a candidate, fall back to `wiki_search.py` (see `wiki/SCHEMA.md`, "Retrieval").

Shards under `wiki/indexes/`:

| Shard | Pages | Covers |
|---|---|---|
| [[sources]] | 1 | Source summary pages; start here for the clause map and coverage of the C++17 draft |
| [[concepts-language]] | 41 | Core language (clauses 4-19): per-clause overviews, execution model, names and ODR, expressions, declarations, templates, Annex C hub |
| [[concepts-library-foundations]] | 32 | Library introduction and rules (20), language support (21), diagnostics (22), general utilities (23: tuples, optional/variant/any, allocators, smart pointers, function objects, type traits, chrono), strings (24) |
| [[concepts-library-containers-algorithms]] | 19 | Containers (26) with iterator invalidation, iterators (27), algorithms (28) |
| [[concepts-library-text-io-numerics-concurrency]] | 24 | Localization (25), numerics (29), input/output and filesystem (30), regex (31), atomics (32), threads (33) |
| [[concepts-glossary-grammar-annexes]] | 10 | Clauses 1-3 glossary, Annex A grammar lookups (4 pages), Annex B implementation quantities, Annex C differences from C and C++03 (2 pages), Annex D deprecated features (2 pages) |
| [[entities]] | 0 | none yet |
| [[synthesis]] | 0 | none yet (cross-cutting topics are filed as concepts) |

Quick routes:

- "What does the standard say about X in the language?" → [[concepts-language]]; entry page [[cpp17-general-principles]].
- "Which header/class provides X, what are its guarantees?" → [[cpp17-lib-introduction]] (library map), then the per-clause overview `cpp17-lib-*` pages in the library shards.
- "Is X invalidated by Y?" → [[iterator-invalidation]]. "What must my type satisfy?" → [[library-named-requirements]].
- Provenance, clause numbers and coverage of the whole standard → [[n4659-cpp17-draft-standard]].
- "What does term X mean (well-formed, signature, unspecified, ...)?" → [[cpp17-glossary]]. "What is the grammar of X?" → [[cpp17-grammar-summary]] (finder), then the three `grammar-*` pages. "Minimum limits an implementation should support?" → [[implementation-quantities]]. "Is X deprecated / where did `strstream`, `result_of`, `std::iterator`, the C `name.h` headers go?" → [[cpp17-annex-d-compatibility-features]], [[deprecated-library-facilities]].

- "How does C++ differ from C / from C++03 / from C++11 and C++14 / from the C library?" → [[cpp-vs-c-differences]], [[cpp03-differences]], [[cpp17-compatibility-differences]] (Annex C map), [[library-requirements-and-conformance]] (C.5 section).

Maintenance: add a new page's line to the matching shard (create a new shard if one passes ~300 lines) and update the counts here.
