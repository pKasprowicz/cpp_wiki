---
type: concept
title: "C++17 clause 25: localization library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 25: Localization library (`[localization]`)

About 14,600 words; 77 labelled sections. Encapsulates cultural differences — character classification and collation, numeric, monetary and date/time formatting and parsing, and message retrieval. The iostreams library formats and parses through it ([[cpp17-lib-input-output]]). Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Content | Wiki page |
|---|---|---|---|
| 25.2 `<locale>` synopsis | `[locale.syn]` | declarations | — |
| 25.3 Locales | `[locales]` | `locale`, `locale::facet`, `locale::id`, `use_facet`/`has_facet`, character classification and conversion convenience functions | [[locale-class-and-facets]] |
| 25.4.1 ctype category | `[category.ctype]` | `ctype`, `ctype<char>`, `codecvt` | [[locale-standard-facets]] |
| 25.4.2 numeric category | `[category.numeric]` | `num_get`, `num_put` | [[locale-standard-facets]] |
| 25.4.3 numeric punctuation | `[facet.numpunct]` | `numpunct` | [[locale-standard-facets]] |
| 25.4.4 collate | `[category.collate]` | `collate` | [[locale-standard-facets]] |
| 25.4.5 time | `[category.time]` | `time_get`, `time_put` | [[locale-standard-facets]] |
| 25.4.6 monetary | `[category.monetary]` | `money_get`, `money_put`, `moneypunct` | [[locale-standard-facets]] |
| 25.4.7 messages | `[category.messages]` | `messages` | [[locale-standard-facets]] |
| 25.4.8 Program-defined facets | `[facets.examples]` | defining and installing your own facet | [[locale-class-and-facets]] |
| 25.5 C library locales | `[c.locales]` | `<clocale>`: `setlocale` may race with ~40 listed C functions (`printf` family, `isalpha`..., `strtod`, `mbtowc`, ...) | below |

## Key ideas

- A `locale` is an immutable, copyable set of **facets** indexed by facet type; a facet is both an interface and the lookup key. Six **categories** (`collate`, `ctype`, `monetary`, `numeric`, `time`, `messages`) group facets so locales can be combined.
- The "classic" `"C"` locale never changes; every locale has all the standard facets for `char` and `wchar_t`.
- Interaction with C: `locale::global` sets the C locale (via `setlocale`) when the locale has a name; **no other library function calls `setlocale`**, and `setlocale` calls may race with the listed C functions (`[c.locales]`, `[support.runtime]`).

## Related

[[locale-class-and-facets]] · [[locale-standard-facets]] · [[stream-base-classes]] · [[cpp17-lib-strings]] · [[char-traits]]
