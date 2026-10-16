---
type: concept
title: "C++17 clause 20: library introduction"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 20: Library introduction (`[library]`)

About 9,800 words; 73 labelled sections. Clause 20 is the "front matter" of the library: it defines how library text is written, lists the headers, and states the rules that apply to every facility. The facilities themselves are in Clauses 21-33 (hub: [[n4659-cpp17-draft-standard]]).

## Section map

| Subclause | Label | Content | Wiki page |
|---|---|---|---|
| 20.1 General | `[library.general]` | The thirteen library categories (Table 15) and one-line purposes | below |
| 20.2 The C standard library | `[library.c]` | C library facilities are inherited; signatures may differ and add overloads, behavior and preconditions (including `restrict`) stay the same unless stated | [[library-requirements-and-conformance]] |
| 20.3 Definitions | `[definitions]` | 25 library-specific terms (replacement/handler function, valid but unspecified state, stable algorithm, ...) | [[library-requirements-and-conformance]] |
| 20.4 Method of description | `[description]` | Elements of a specification (Requires/Effects/...), bitmask and enumerated types, character sequences | [[library-requirements-and-conformance]] |
| 20.5.1-20.5.2 Organization, using the library | `[organization]` `[using]` | Namespace `std`, header tables, freestanding set, include rules, linkage | [[library-requirements-and-conformance]] |
| 20.5.3 Requirements on types | `[utility.requirements]` | EqualityComparable ... Destructible, Swappable, NullablePointer, Hash | [[library-named-requirements]] |
| 20.5.3.5 Allocator requirements | `[allocator.requirements]` | Allocator type interface, fancy pointers, propagation traits | [[allocators]] |
| 20.5.4 Constraints on programs | `[constraints]` | What a program may not declare, define, specialize, or macro-define | [[library-requirements-and-conformance]] |
| 20.5.5 Conforming implementations | `[conforming]` | Latitude and obligations: headers, inline/constexpr, data races, exceptions, moved-from state | [[library-requirements-and-conformance]] |

## The thirteen library categories (`[library.general]`, Table 15)

| Clause | Category | Overview page |
|---|---|---|
| 21 | Language support | [[cpp17-lib-language-support]] |
| 22 | Diagnostics | [[cpp17-lib-diagnostics]] |
| 23 | General utilities | [[cpp17-lib-utilities]] |
| 24 | Strings | [[cpp17-lib-strings]] |
| 25 | Localization | [[cpp17-lib-localization]] |
| 26 | Containers | [[cpp17-lib-containers]] |
| 27 | Iterators | [[cpp17-lib-iterators]] |
| 28 | Algorithms | [[cpp17-lib-algorithms]] |
| 29 | Numerics | [[cpp17-lib-numerics]] |
| 30 | Input/output | [[cpp17-lib-input-output]] |
| 31 | Regular expressions | [[cpp17-lib-regex]] |
| 32 | Atomic operations | [[cpp17-lib-atomics]] |
| 33 | Thread support | [[cpp17-lib-thread]] |

Purpose in one line each (`[library.general]/4-14`): language support = components the language itself needs (allocation, exceptions); diagnostics = error-reporting framework and exception classes; utilities = infrastructure (allocator, tuples, function wrappers, time); strings = text as sequences of `char`, `char16_t`, `char32_t`, `wchar_t` or any character-like type; localization = internationalization for text; containers/iterators/algorithms = the common data structures and algorithms; numerics = numeric algorithms, `complex`, `valarray` (n-at-a-time processing), random numbers; I/O = iostreams; regex; atomics = finer-grained shared-data access than locks; thread support = threads, mutual exclusion, inter-thread communication.

## Where the topic pages are

The detailed library knowledge in this wiki is split by topic rather than by subclause: the rules a program must follow with *every* facility are in [[library-requirements-and-conformance]]; requirements on user-supplied types are in [[library-named-requirements]] and [[allocators]].

## Compatibility notes

Annex C lists a handful of library incompatibilities (reserved `stdN` namespaces, a new `<shared_mutex>` header, removed `gets`, removed `auto_ptr` and friends, ...); they are tabulated in [[cpp17-compatibility-differences]]. Library-side differences from ISO C++ 2003 are in [[cpp03-differences]] (C.2.8-C.2.16) and from the C standard library in the Annex C.5 section of [[library-requirements-and-conformance]]. Library pages here do not label features "new in C++17": the draft itself does not mark them.

Annex D (`[depr]`) holds the deprecated library facilities (`<strstream>`, the old binder typedefs and negators, the older `std::allocator` interface, `raw_storage_iterator`, temporary buffers, `<codecvt>`, `wstring_convert`, ...) and the C `name.h` headers: [[cpp17-annex-d-compatibility-features]], [[deprecated-library-facilities]]. Library-only defined terms (`[definitions]`) are in [[cpp17-glossary]].
