---
type: concept
title: "std::locale, facets, use_facet and the global locale"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `locale`, facets and the global locale (`[locales]`, `[facets.examples]`)

Parent: [[cpp17-lib-localization]]. The standard facets themselves: [[locale-standard-facets]].

## The model (`[locale]`)

- `locale` is a **type-safe polymorphic set of facets, indexed by facet type**. Access is by `use_facet<Facet>(loc)` (returns a reference valid at least as long as any copy of `loc` exists; throws **`bad_cast`** if the facet is absent) and `has_facet<Facet>(loc)` (`[locale.global.templates]`). `Facet` must be a class derived from `locale::facet` with a public static `locale::id id` member; a non-facet or volatile-qualified facet argument is ill-formed; const-qualified is fine.
- Once a facet reference is obtained, the reference and its results may be cached as long as some locale object refers to the facet; successive calls on the same facet in the same locale return identical results (`/6-7`).
- **Names**: a locale built from a name string (`"C"`, `""`, or implementation-defined) or from parts of two named locales has a name; others do not (`name()` is `"*"`). Named locales compare equal if the names match; an unnamed locale equals only itself and its copies. Constructing from an invalid or null name throws `runtime_error`.
- **Categories** are a bitmask `locale::category` (`collate`, `ctype`, `monetary`, `numeric`, `time`, `messages`, `none`, `all`). Constructors: default (a snapshot of the current global locale, which is `classic()` until `locale::global` is called); copy; from name; from another locale plus a name and category set; from another locale plus a facet pointer (installs it, replacing that facet type; if the pointer is null the result is a copy; the result is unnamed); from two locales plus categories. `combine<Facet>(other)` copies one facet from another locale (throws `runtime_error` if absent; result unnamed).
- **Global state** (`[locale.statics]`): `locale::global(loc)` sets the global locale and, if `loc` has a name, also calls `setlocale`; no other library function may change what `locale()` returns. It returns the previous global locale. `locale::classic()` is the immutable "C" locale (does not change with time). **Whether there is one global locale for the program or one per thread is implementation-defined** (one per thread is recommended); with a single global locale, no data-race avoidance is required (`/9`).
- `locale::operator()(a, b)` compares two strings via `collate<charT>` — so a `locale` can be passed as the comparator to `sort` ([[sorting-and-set-algorithms]]).

## `locale::facet` and `locale::id` (`[locale.facet]`, `[locale.id]`)

- `facet(refs)`: with `refs == 0`, the facet is deleted when the last locale containing it is destroyed; with `refs == 1` it is never deleted by the library (so static or stack facets are safe). All single-argument facet constructors in the clause are `explicit`.
- A standard `…_byname` class is provided for many facets, taking a locale name and `refs`, and behaving like that facet of `locale(name)`.
- `locale::id` identifies a facet interface and encapsulates lazy initialization.

## Required content (`[locale.category]`, Tables 69-70)

For any locale built or returned by `classic()`, `has_facet` is true for each facet in Table 69: `collate<char/wchar_t>`, `ctype<char/wchar_t>`, `codecvt<char,char,mbstate_t>`, `codecvt<char16_t,char,mbstate_t>`, `codecvt<char32_t,char,mbstate_t>`, `codecvt<wchar_t,char,mbstate_t>`, `moneypunct<…>` (plain and international), `money_get/put`, `numpunct`, `num_get/put`, `time_get/put`, `messages` for `char` and `wchar_t`. Table 70 adds the `_byname` classes and the `InputIterator`/`OutputIterator` specializations for all iterator types. The standard `num_get`/`num_put` call `use_facet` only for `numpunct<charT>` and `ctype<charT>` of the stream's locale.

## Convenience functions (`[locale.convenience]`)

`isspace`, `isprint`, `iscntrl`, `isupper`, `islower`, `isalpha`, `isdigit`, `ispunct`, `isxdigit`, `isalnum`, `isgraph`, `isblank`, `toupper`, `tolower` taking a `charT` and a `locale`, each defined through `use_facet<ctype<charT>>(loc)`.

## Program-defined facets (`[facets.examples]`)

A program can add a facet by deriving a class from `locale::facet` with a `static locale::id id;` member, and installing an instance with `locale(other, new MyFacet)`; its interface is then used identically to the built-in ones.

## Related

[[locale-standard-facets]] · [[cpp17-lib-localization]] · [[stream-base-classes]] (`imbue`, `getloc`) · [[exception-support]] · [[cpp17-lib-input-output]] · [[deprecated-library-facilities]] (`wstring_convert`, `wbuffer_convert`)
