---
type: concept
title: "Character traits (char_traits)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Character traits (`[char.traits]`)

The "traits" parameter of `basic_string`, `basic_string_view`, the iostreams and regex classes: it defines how a character type compares, copies, and signals end-of-file. Parent: [[cpp17-lib-strings]]. Related named requirement: [[library-named-requirements]].

## Requirements (Table 54, `[char.traits.require]`)

For a traits class `X` over character type `charT` (`X::char_type` must be `charT`):

- **Types**: `char_type`, `int_type` (can represent every valid character *plus* an end-of-file value), `off_type`, `pos_type` (requirements given in the iostream clauses), `state_type` (CopyAssignable, CopyConstructible, DefaultConstructible, e.g. `mbstate_t`).
- **Character relations**: `eq(c, d)`, `lt(c, d)`; `compare(p, q, n)` (lexicographic, using `eq`/`lt`, linear), `length(p)` (smallest `i` with `eq(p[i], charT())`), `find(p, n, c)`.
- **Moving data**: `move(s, p, n)` (copies correctly even for overlapping ranges), `copy(s, p, n)` (ranges must not overlap), `assign(r, d)`, `assign(s, n, c)`.
- **int_type conversions and EOF**: `to_char_type(e)`, `to_int_type(c)`, `eq_int_type(e, f)` (consistent with `eq` on the corresponding characters; true for two copies of `eof()`), `eof()` (a value that is the image of no character), `not_eof(e)` (returns `e` unless it is eof, then some non-eof value).

## Specializations in `<string>` (`[char.traits.specializations]`)

| Specialization | `int_type` | `pos_type` | EOF | Comparison |
|---|---|---|---|---|
| `char_traits<char>` | `int` | `streampos` | `EOF` | `eq`/`lt` behave like `==`/`<` on `unsigned char` |
| `char_traits<char16_t>` | implementation-defined integer | `u16streampos` | an implementation-defined constant that is not a valid UTF-16 code unit | built-in `=`, `==`, `<` |
| `char_traits<char32_t>` | implementation-defined integer | `u32streampos` | constant that is not a Unicode code point | built-in operators |
| `char_traits<wchar_t>` | `wint_t` | `wstreampos` | `WEOF` | built-in operators |

`state_type` is `mbstate_t` for `char` and `wchar_t`; `off_type` is `streamoff` for `char`. The positional types are implementation-defined types meeting the stream position requirements ([[stream-base-classes]]). The primary `char_traits<charT>` template must be provided so that users can define explicit specializations for their own character types.

## Related

[[cpp17-lib-strings]] · [[basic-string]] · [[string-view]] · [[stream-buffers]] · [[locale-standard-facets]]
