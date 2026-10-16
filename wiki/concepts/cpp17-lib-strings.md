---
type: concept
title: "C++17 clause 24: strings library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 24: Strings library (`[strings]`)

About 15,700 words; 70 labelled sections. Text as sequences of *char-like objects* (non-array POD types): `char`, `char16_t`, `char32_t`, `wchar_t`, or user types. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header | Content | Wiki page |
|---|---|---|---|---|
| 24.2 Character traits | `[char.traits]` | `<string>` | traits requirements, `char_traits` and its four specializations | [[char-traits]] |
| 24.3 String classes | `[string.classes]` | `<string>` | `basic_string`, `string`/`u16string`/`u32string`/`wstring`, `operator+`, comparisons, `stoi`/`to_string` family, `hash`, `""s` literals | [[basic-string]] |
| 24.4 String view classes | `[string.view]` | `<string_view>` | `basic_string_view`, `string_view` etc., `""sv` literals | [[string-view]] |
| 24.5 Null-terminated sequence utilities | `[c.strings]` | `<cctype>`, `<cwctype>`, `<cstring>`, `<cwchar>`, `<cuchar>`, `<cstdlib>` | C character/string functions and multibyte conversion | below |

## C-compatible utilities (`[c.strings]`)

- `<cctype>`, `<cwctype>`, `<cstring>`, `<cwchar>`, `<cuchar>` have the contents and meaning of C `<ctype.h>`, `<wctype.h>`, `<string.h>`, `<wchar.h>`, `<uchar.h>`. `<cwchar>` and `<cuchar>` do not declare the keyword types (`wchar_t`, `char16_t`, `char32_t`) (`[cwchar.syn]/1`, `[cuchar.syn]/1`).
- In `<cstring>`, `strerror` and `strtok` are not required to avoid data races; `memcpy` and `memmove` are signal-safe (`[cstring.syn]/2-3`).
- Multibyte/wide conversion (`mblen`, `mbtowc`, `wctomb`, `mbstowcs`, `wcstombs`, `mbrtowc`, ...): C semantics; the non-restartable ones may race with other calls to the same function, and the restartable ones may race when passed a null `mbstate_t*` (`[c.mb.wcs]`).
- These functions are used by `basic_string` numeric conversions and by locale facets ([[locale-standard-facets]]).

## Why the three pieces are separate

`basic_string` owns and allocates characters via an allocator ([[allocators]]); `basic_string_view` is a non-owning reference to contiguous characters; both are parameterized by a `traits` class that gives character comparison, copying and the end-of-file value that the iostreams library also needs ([[cpp17-lib-input-output]]).

## Related

[[char-traits]] · [[basic-string]] · [[string-view]] · [[cpp17-lib-localization]] · [[bitset]] (string constructors/conversions) · [[literals]]
