---
title: "Index shard: concepts — glossary, grammar and annexes (clauses 1-3, Annexes A, B, C, D)"
---
# Index shard: concepts — glossary, grammar and annexes (clauses 1-3, Annexes A, B, C, D)

One line per page. Directory of shards: `wiki/index.md`. The Annex C hub page (map of C.1-C.5, plus C.3-C.4) is in the language shard as [[cpp17-compatibility-differences]]; the C.5 notes are a section of [[library-requirements-and-conformance]]; clause 4 is [[cpp17-general-principles]].

## Clauses 1-3 (scope, references, terms)

- [[cpp17-glossary]] — Clauses 1-3: scope, the nine normative references and their shorthand names, glossary of the 29 clause-3 terms (well-formed, undefined/unspecified/implementation-defined behavior, signature, static/dynamic type, ...) and the 25 library-only terms of `[definitions]`.

## Annex A (grammar summary)

- [[cpp17-grammar-summary]] — Annex A guide: caveats (the grammar over-accepts), compact notation, A.1-A.14 section map, start symbols, quick routes and an alphabetical finder of all 285 nonterminals.
- [[grammar-lexical-and-preprocessing]] — A.1 contextual names, A.2 tokens, literals, escapes, user-defined literals, A.14 preprocessing directives incl. `__has_include`; compact productions.
- [[grammar-expressions-and-statements]] — A.4 expressions (precedence ladder, lambda, fold, new/delete, casts), A.5 statements, A.13 try/catch and noexcept-specifier; compact productions.
- [[grammar-declarations-and-classes]] — A.3 translation-unit, A.6 declarations/enums/namespaces/attributes, A.7 declarators and initializers, A.8-A.10 classes, A.11 operators, A.12 templates; compact productions.

## Annex B (implementation quantities)

- [[implementation-quantities]] — The 43 recommended minimum limits (nesting depths, identifier and macro counts, class sizes, `constexpr` recursion, `atexit` count, placeholders), grouped, with the non-binding status.

## Annex C (compatibility differences, informative)

- [[cpp-vs-c-differences]] — C.1: the 33 ways ISO C code differs from or breaks in C++ (keywords, `char` literals, `const` string literals, tentative definitions, `void*`, implicit `int`, empty parameter lists, `sizeof`-visible changes), each with the annex's rationale, conversion difficulty and "how widely used" label.
- [[cpp03-differences]] — C.2: the 37 differences from ISO C++ 2003 by clause (string-literal prefixes, null pointer constants, `export`, `>>`, new/delete linkage, `explicit` stream bool conversions, container signature changes); silent-behavior checklist; stale-example and header-list caveats.

## Annex D (compatibility features, deprecated)

- [[cpp17-annex-d-compatibility-features]] — D.1-D.16 map; `static constexpr` redeclaration, implicit copy functions, `throw()`, deprecated C++/C headers (`<ccomplex>`, `name.h`), `uncaught_exception`, `result_of`/`is_literal_type`, `std::iterator`, `shared_ptr::unique`; what Annex C says was removed.
- [[deprecated-library-facilities]] — `<strstream>`, old function-object typedefs and `not1`/`not2`, older `std::allocator` members, `raw_storage_iterator`, temporary buffers, `<codecvt>` facets, `wstring_convert`/`wbuffer_convert`.
