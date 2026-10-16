---
type: source
title: "Working draft of the C++ standard, C++17 (N4659) — cppwp HTML rendering"
authors: ["C++ standard draft sources (cplusplus/draft), rendered by cxxdraft-htmlgen / timsong-cpp cppwp"]
url: "https://timsong-cpp.github.io/cppwp/n4659/"
raw: "raw/n4659-cppwp-full.html"
ingested: 2026-10-15
tags: [cpp17, standard-clause, language-core, library, grammar, deprecated]
entities: []
concepts: [cpp17-general-principles, abstract-machine-and-observable-behavior, sequencing-and-evaluation-order, memory-model-and-data-races, cpp17-lexical-conventions, translation-phases, literals, cpp17-basic-concepts, one-definition-rule, name-lookup, linkage, program-startup-and-termination, storage-duration-and-object-lifetime, value-categories, strict-aliasing, cpp17-standard-conversions, cpp17-expressions, cast-expressions, new-and-delete-expressions, lambda-expressions, fold-expressions, constant-expressions, cpp17-statements, cpp17-declarations, attributes, structured-bindings, cpp17-declarators, initialization, cpp17-classes, cpp17-derived-classes, cpp17-member-access-control, cpp17-special-member-functions, copy-elision-and-temporary-materialization, cpp17-overloading, overload-resolution, cpp17-templates, dependent-names-and-instantiation, template-argument-deduction, cpp17-exception-handling, cpp17-preprocessing-directives, cpp17-compatibility-differences, cpp-vs-c-differences, cpp03-differences, algorithm-requirements, allocators, any-type, array-and-vector, associative-container-requirements, atomics-and-memory-order, basic-string, bitset, char-traits, chrono-and-ratio, complex-numbers, condition-variable, container-adaptors, container-requirements, cpp17-lib-algorithms, cpp17-lib-atomics, cpp17-lib-containers, cpp17-lib-diagnostics, cpp17-lib-input-output, cpp17-lib-introduction, cpp17-lib-iterators, cpp17-lib-language-support, cpp17-lib-localization, cpp17-lib-numerics, cpp17-lib-regex, cpp17-lib-strings, cpp17-lib-thread, cpp17-lib-utilities, deque-and-lists, dynamic-memory-support, error-codes-and-system-error, exception-support, execution-policies-and-parallel-algorithms, filesystem, formatted-and-unformatted-io, function-objects-and-invoke, futures-and-async, iterator-adaptors, iterator-categories-and-requirements, iterator-invalidation, library-named-requirements, library-requirements-and-conformance, locale-class-and-facets, locale-standard-facets, math-functions-and-fenv, memory-resources-pmr, mutating-sequence-algorithms, mutexes-and-locks, nonmodifying-sequence-algorithms, numeric-limits, numeric-operations, optional, ordered-associative-containers, pair-and-tuple, random-number-generation, regex-classes-and-algorithms, sequence-container-requirements, shared-ptr-and-weak-ptr, sorting-and-set-algorithms, standard-exception-classes, std-function, stream-base-classes, stream-buffers, string-and-file-streams, string-view, threads, type-identification-rtti, type-traits, uninitialized-memory-algorithms, unique-ptr, unordered-container-requirements, unordered-containers, utility-move-forward-swap, valarray, variant, cpp17-glossary, cpp17-grammar-summary, grammar-lexical-and-preprocessing, grammar-expressions-and-statements, grammar-declarations-and-classes, implementation-quantities, cpp17-annex-d-compatibility-features, deprecated-library-facilities]
created: 2026-10-15
updated: 2026-10-16
---

# C++17 working draft (N4659), cppwp rendering

The HTML rendering of the C++17 draft standard published at timsong-cpp.github.io/cppwp/n4659/. The front clauses (1-3), the language clauses (4-19), the library clauses (20-33), Annexes A, B, C and D are summarized in this wiki. Every clause and annex of the draft has now been ingested.

## Provenance and identity

- **Retrieved** 2026-10-15 from `https://timsong-cpp.github.io/cppwp/n4659/full` (single-page edition, 12,941,278 bytes, SHA-256 `c92f56a211de958a1b95b4fa158164dd47eff853aadbb428c1b16d8215fdb453`), stored verbatim as `raw/n4659-cppwp-full.html`. The contents page (`.../n4659/`, 426,887 bytes) was read for the clause map.
- The page states: *"Generated on 2026-04-09 from the C++ standard's draft LaTeX sources ... by cxxdraft-htmlgen. This is not an ISO publication."* Source commit shown: `1af12266e2ba8c5a0eb0699f09fa5bde53dd70f3` (github.com/cplusplus/draft). The page title is just "14882".
- **No N-number is printed in the content.** The identification as N4659 / C++17 rests on the URL path and on content checks: `__cplusplus` is defined as `201703L` (`[cpp.predefined]`), C++17 features are present (fold expressions, deduction guides, structured bindings, `if constexpr`, the `nodiscard` attribute, inline variables) and C++20 features (spaceship operator, modules, concepts, coroutines, ranges) are absent.
- Clause numbers on this site: 1-3 are Scope / Normative references / Terms and definitions, 4 General principles, 5 Lexical conventions, ... 19 Preprocessing directives, 20-33 the library, Annexes A-D. Stable section labels (`[basic.lookup]`) are used for citations throughout this wiki; they can be opened at `https://timsong-cpp.github.io/cppwp/n4659/<label>`.

## Clause map and coverage

"Words" is the approximate size of the normative text (notes, examples and footnotes removed) from the extraction used for reading; "sections" is the number of labelled entries in the contents page.

| Clause | Label | Sections | Words | Coverage | Wiki page |
|---|---|---|---|---|---|
| 1-3 Scope, normative references, terms | `[intro.scope]` `[intro.refs]` `[intro.defs]` | 0 | 1,000 | summarized (glossary of the 29 clause-3 entries plus the 25 library terms of `[definitions]`) | [[cpp17-glossary]] |
| 4 General principles | `[intro]` | 10 | 4,800 | summarized | [[cpp17-general-principles]] |
| 5 Lexical conventions | `[lex]` | 21 | 6,000 | summarized | [[cpp17-lexical-conventions]] |
| 6 Basic concepts | `[basic]` | 44 | 15,900 | summarized | [[cpp17-basic-concepts]] |
| 7 Standard conversions | `[conv]` | 15 | 2,700 | summarized | [[cpp17-standard-conversions]] |
| 8 Expressions | `[expr]` | 48 | 18,100 | summarized | [[cpp17-expressions]] |
| 9 Statements | `[stmt.stmt]` | 18 | 2,900 | summarized | [[cpp17-statements]] |
| 10 Declarations | `[dcl.dcl]` | 33 | 10,300 | summarized | [[cpp17-declarations]] |
| 11 Declarators | `[dcl.decl]` | 19 | 8,200 | summarized | [[cpp17-declarators]] |
| 12 Classes | `[class]` | 14 | 4,800 | summarized | [[cpp17-classes]] |
| 13 Derived classes | `[class.derived]` | 4 | 1,700 | summarized | [[cpp17-derived-classes]] |
| 14 Member access control | `[class.access]` | 7 | 1,700 | summarized | [[cpp17-member-access-control]] |
| 15 Special member functions | `[special]` | 16 | 7,400 | summarized | [[cpp17-special-member-functions]] |
| 16 Overloading | `[over]` | 34 | 10,500 | summarized | [[cpp17-overloading]] |
| 17 Templates | `[temp]` | 51 | 19,000 | summarized | [[cpp17-templates]] |
| 18 Exception handling | `[except]` | 7 | 2,600 | summarized | [[cpp17-exception-handling]] |
| 19 Preprocessing directives | `[cpp]` | 14 | 3,900 | summarized | [[cpp17-preprocessing-directives]] |
| 20 Library introduction | `[library]` | 73 | 10,200 | summarized | [[cpp17-lib-introduction]] |
| 21 Language support library | `[language.support]` | 63 | 10,000 | summarized | [[cpp17-lib-language-support]] |
| 22 Diagnostics library | `[diagnostics]` | 42 | 3,700 | summarized | [[cpp17-lib-diagnostics]] |
| 23 General utilities library | `[utilities]` | 310 | 54,100 | summarized | [[cpp17-lib-utilities]] |
| 24 Strings library | `[strings]` | 70 | 15,500 | summarized | [[cpp17-lib-strings]] |
| 25 Localization library | `[localization]` | 77 | 14,700 | summarized | [[cpp17-lib-localization]] |
| 26 Containers library | `[containers]` | 129 | 35,300 | summarized | [[cpp17-lib-containers]] |
| 27 Iterators library | `[iterators]` | 96 | 7,900 | summarized | [[cpp17-lib-iterators]] |
| 28 Algorithms library | `[algorithms]` | 69 | 16,400 | summarized | [[cpp17-lib-algorithms]] |
| 29 Numerics library | `[numerics]` | 154 | 28,200 | summarized | [[cpp17-lib-numerics]] |
| 30 Input/output library | `[input.output]` | 240 | 37,500 | summarized | [[cpp17-lib-input-output]] |
| 31 Regular expressions library | `[re]` | 48 | 12,200 | summarized | [[cpp17-lib-regex]] |
| 32 Atomic operations library | `[atomics]` | 13 | 4,400 | summarized | [[cpp17-lib-atomics]] |
| 33 Thread support library | `[thread]` | 73 | 15,100 | summarized | [[cpp17-lib-thread]] |
| Annex A Grammar summary (informative) | `[gram]` | 14 | 2,500 | summarized as lookup pages (all 291 productions in compact notation, plus a nonterminal finder) | [[cpp17-grammar-summary]], [[grammar-lexical-and-preprocessing]], [[grammar-expressions-and-statements]], [[grammar-declarations-and-classes]] |
| Annex B Implementation quantities (informative) | `[implimits]` | 0 | 500 | summarized (all 43 quantities) | [[implementation-quantities]] |
| Annex C Compatibility (informative) | `[diff]` | 63 | 8,600 | summarized in full: C.1 (C++ and ISO C, 33 entries), C.2 (C++ and ISO C++ 2003, 37 entries), C.3-C.4 (C++11 and C++14, language and library entries), C.5 (C standard library) | [[cpp17-compatibility-differences]] (Annex C map, C.3-C.4), [[cpp-vs-c-differences]], [[cpp03-differences]], [[library-requirements-and-conformance]] (C.5 section) |
| Annex D Compatibility features (normative) | `[depr]` | 42 | 7,100 | summarized (all 16 subsections; the larger library facilities at family level) | [[cpp17-annex-d-compatibility-features]], [[deprecated-library-facilities]] |

Plus 146 tables and 7 figures in the lists at the start of the contents page.

## Cross-cutting pages built from several clauses

[[abstract-machine-and-observable-behavior]] · [[sequencing-and-evaluation-order]] · [[memory-model-and-data-races]] · [[translation-phases]] · [[literals]] · [[one-definition-rule]] · [[name-lookup]] · [[linkage]] · [[program-startup-and-termination]] · [[storage-duration-and-object-lifetime]] · [[value-categories]] · [[strict-aliasing]] · [[cast-expressions]] · [[new-and-delete-expressions]] · [[lambda-expressions]] · [[fold-expressions]] · [[constant-expressions]] · [[attributes]] · [[structured-bindings]] · [[initialization]] · [[copy-elision-and-temporary-materialization]] · [[overload-resolution]] · [[dependent-names-and-instantiation]] · [[template-argument-deduction]]

## Library pages (clauses 20-33)

Each library clause has an overview page (`cpp17-lib-<topic>`, section map); 61 topic pages hold the load-bearing content. By clause:

- **20**: [[library-requirements-and-conformance]] · [[library-named-requirements]]
- **21**: [[numeric-limits]] · [[dynamic-memory-support]] · [[exception-support]] · [[type-identification-rtti]]
- **22**: [[standard-exception-classes]] · [[error-codes-and-system-error]]
- **23**: [[utility-move-forward-swap]] · [[pair-and-tuple]] · [[optional]] · [[variant]] · [[any-type]] · [[bitset]] · [[allocators]] · [[memory-resources-pmr]] · [[uninitialized-memory-algorithms]] · [[unique-ptr]] · [[shared-ptr-and-weak-ptr]] · [[function-objects-and-invoke]] · [[std-function]] · [[type-traits]] · [[chrono-and-ratio]] · [[execution-policies-and-parallel-algorithms]]
- **24**: [[char-traits]] · [[basic-string]] · [[string-view]]
- **25**: [[locale-class-and-facets]] · [[locale-standard-facets]]
- **26**: [[container-requirements]] · [[sequence-container-requirements]] · [[associative-container-requirements]] · [[unordered-container-requirements]] · [[iterator-invalidation]] · [[array-and-vector]] · [[deque-and-lists]] · [[ordered-associative-containers]] · [[unordered-containers]] · [[container-adaptors]]
- **27**: [[iterator-categories-and-requirements]] · [[iterator-adaptors]]
- **28**: [[algorithm-requirements]] · [[nonmodifying-sequence-algorithms]] · [[mutating-sequence-algorithms]] · [[sorting-and-set-algorithms]]
- **29**: [[complex-numbers]] · [[random-number-generation]] · [[valarray]] · [[numeric-operations]] · [[math-functions-and-fenv]]
- **30**: [[stream-base-classes]] · [[stream-buffers]] · [[formatted-and-unformatted-io]] · [[string-and-file-streams]] · [[filesystem]]
- **31**: [[regex-classes-and-algorithms]]
- **32**: [[atomics-and-memory-order]]
- **33**: [[threads]] · [[mutexes-and-locks]] · [[condition-variable]] · [[futures-and-async]]

## Front clauses and annexes (1-3, A, B, C, D)

- **1-3**: [[cpp17-glossary]] (scope, normative references with their shorthand names, defined terms).
- **Annex A**: [[cpp17-grammar-summary]] (guide and nonterminal finder) with the lookup pages [[grammar-lexical-and-preprocessing]], [[grammar-expressions-and-statements]], [[grammar-declarations-and-classes]].
- **Annex B**: [[implementation-quantities]].
- **Annex C**: [[cpp17-compatibility-differences]] (map of C.1-C.5; C.3-C.4), [[cpp-vs-c-differences]] (C.1), [[cpp03-differences]] (C.2); C.5 is a section of [[library-requirements-and-conformance]].
- **Annex D**: [[cpp17-annex-d-compatibility-features]] (language features, headers, small library items) and [[deprecated-library-facilities]] (`<strstream>`, binder typedefs, allocator members, `<codecvt>` and conversions).

## Method and limitations

- The raw HTML was split into per-clause plain text by a throwaway script (kept in the scratchpad, not in the wiki), and each language clause was read in full in that text. For reading, **informational notes, examples and footnotes were stripped**; paragraphs that consist only of notes appear empty there. Where a normative claim depended on that material (the attribute semantics in `[dcl.attr]`), the full text was consulted and the pages say that the behavior is stated in a note.
- Pages **paraphrase and summarize**; they do not reproduce the standard's wording. Quote section labels and paragraph numbers (`[expr.ass]/1`) rather than wording when verifying against the source.
- Grammar productions inside the language clauses, Table contents and figures were read but are summarized, not reproduced. **Annex A** is the exception: its 291 productions were compressed mechanically (a throwaway script in the scratchpad) into a one-line notation on the three `grammar-*` pages, so those pages restate the structure of the grammar rather than paraphrase it; check the printed form in the raw file for exact layout.
- **Library clauses (20-33)** were read through a section index (`label -> text`) built by a second throwaway script, section by section, with notes/examples/footnotes stripped. Reading depth varied by importance: container, iterator, algorithm, smart-pointer, vector-like and concurrency material was read paragraph by paragraph; the repetitive per-member descriptions of the random distributions, special math functions, locale facets, `valarray` subset classes, `time_get`/`money_*` details, filesystem operation functions, `regex_traits` and the many `_copy`/`_n` variants were read at skim depth, so those pages summarize behavior at family level and do not list every signature. Class synopses (code blocks) were mostly skipped except where they carried a fact (deduction guides, base classes, defaults), so signature-level details should be taken from the standard itself.
- **Annex C** (C.1, C.2 and C.5 added 2026-10-16) was split with a throwaway script that keeps notes and examples (parts of its Change/Rationale/Effect entries sit in examples) and read in full; entries are paraphrased and keyed by the draft's own labels, with the annex's "how widely used" verdicts kept as labels. C.5 is a pointer list, so the sections it points to (`[cstring.syn]`, `[cwchar.syn]`, `[support.start.term]`, `[csetjmp.syn]`, `[support.types.layout]`, `[c.malloc]`) were read as well for the summary.
- **Clauses 1-3 and Annexes B and D** were read in full (notes kept for definitions and for Annex D, since several facts there live in notes and examples; the pages say when a point comes from a note or example). The larger Annex D components (`<strstream>`, `wstring_convert`, binder typedefs) are summarized at class and behavior level, not per signature. Annex B's list was checked entry by entry against the page (43 of 43).
- The library text uses **plain-identifier named requirements** (`CopyConstructible`, `Allocator`, `Hash`, ...) and still contains features removed or changed in later editions (for example pointer-safety functions, `strict pointer safety` wording in `operator delete`, `std::function` without allocator constructors, no `atomic_flag::test`). Pages report what this draft says.
- The cppwp page was regenerated from the draft sources in April 2026; if the site is updated again, the section labels remain stable but content could differ. The raw copy is the reference for this wiki.

## Follow-ups worth doing

1. Deepen the library pages that were read at skim depth (see Method): random distributions, locale facets (`time_get`/`money_*`), `valarray`, special math functions, filesystem operations, `regex_traits`; add per-algorithm or per-class pages if needed.
2. Annex C.1, C.2 and C.5 were summarized on 2026-10-16, so no part of the draft is left unsummarized. Annex C open points: it names "ISO C" without an edition, its C.2.8 new-header list omits headers that Table 16 has (`<optional>`, `<string_view>`, `<filesystem>`, ...), and one C.2.9 example still uses a dynamic exception specification (see [[cpp-vs-c-differences]], [[cpp03-differences]]).
3. Annex D per-signature detail (`strstreambuf` virtual functions, `wstring_convert` members) is at summary level only.
4. Spot-check the pages against the raw file with `wiki_search.py` section-level retrieval (`--json`) before relying on a specific paragraph number; the library pages cite `[label]/N` for many claims but not all.
5. Consider a separate source for "what changed in C++17" (see the open question on [[cpp17-compatibility-differences]]).

## Where this fits

Entry point for the whole wiki: [[cpp17-general-principles]] (how the standard is organized), [[cpp17-basic-concepts]] (object model, lookup, lifetime), [[cpp17-expressions]], [[cpp17-declarations]], [[cpp17-templates]]. Library entry point: [[cpp17-lib-introduction]] (library-wide rules, named requirements, header lists) and the per-clause overviews linked in the table above.
