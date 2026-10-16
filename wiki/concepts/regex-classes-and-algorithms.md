---
type: concept
title: "Regular expressions: basic_regex, match_results, regex_match/search/replace, iterators, grammar"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Regular expressions library (`<regex>`, `[re]`)

Parent: [[cpp17-lib-regex]]. Strings and iterators it operates on: [[basic-string]], [[iterator-categories-and-requirements]].

## Traits (`[re.req]`, `[re.traits]`)

`basic_regex<charT, traits>` obtains locale-dependent behavior from a **regex traits** class `X`: `char_type`, `string_type`, `locale_type` (copy-constructible), `char_class_type` (a bitmask type), and the operations `length(p)`, `translate(c)`, `translate_nocase(c)`, `transform(F1, F2)` (collation sort key), `transform_primary(F1, F2)` (case-insensitive key), `lookup_collatename(F1, F2)`, `lookup_classname(F1, F2, icase)` (returns a mask, `0` for unknown names; masks can be OR-ed), `isctype(c, cl)`, `value(c, base)` (digit value or −1), `imbue(loc)`, `getloc()`. `regex_traits<char>` and `regex_traits<wchar_t>` must exist. A `basic_regex` holds a default-constructed traits instance and **must not call any locale-dependent C or C++ API directly** — only the traits — so localization is fully customizable (`[re.grammar]/2`).

## Constants (`[re.const]`)

- **`syntax_option_type`** (bitmask): `icase`, `nosubs`, `optimize`, `collate`, `multiline` (ECMAScript only) and **one** grammar flag at most: `ECMAScript` (default), `basic`, `extended`, `awk`, `grep`, `egrep`.
- **`match_flag_type`** (bitmask): `match_default`, `match_not_bol`, `match_not_eol`, `match_not_bow`, `match_not_eow`, `match_any`, `match_not_null`, `match_continuous`, `match_prev_avail`; formatting flags `format_default` (ECMAScript `replace` rules), `format_sed`, `format_no_copy`, `format_first_only`.
- **`error_type`**: `error_collate`, `error_ctype`, `error_escape`, `error_backref`, `error_brack`, `error_paren`, `error_brace`, `error_badbrace`, `error_range`, `error_space`, `error_badrepeat`, `error_complexity`, `error_stack`. **`regex_error`** (derives from `runtime_error`) carries one via `code()`; constructing a `basic_regex` from an invalid pattern throws it ([[standard-exception-classes]]).

## `basic_regex` (`[re.regex]`)

`regex` = `basic_regex<char>`, `wregex` = `basic_regex<wchar_t>`. Compiles a pattern into an unspecified internal "finite state machine". Constructors: default (matches nothing), from a null-terminated pointer (non-null required), `(ptr, len)`, a string, an iterator range, an initializer list, plus flags `f` (default ECMAScript); `assign` overloads; `mark_count()` (number of marked sub-expressions), `flags()`, `imbue(loc)`, `getloc()`, `swap`. Pointer arguments must be non-null; an invalid pattern throws `regex_error`.

## `sub_match` and `match_results` (`[re.submatch]`, `[re.results]`)

- `sub_match<BiIter>` is a `pair<BiIter, BiIter>` plus `matched`; `length()` is `matched ? distance(first, second) : 0`; `str()`, conversion to `basic_string`, `compare`, and a large family of comparison operators against other sub_matches, strings, C strings and characters. Typedefs `csub_match`, `ssub_match`, `wcsub_match`, `wssub_match`.
- `match_results<BiIter, Allocator>` is an **allocator-aware, read-only sequence of `sub_match`es** (only const-container operations; comparison semantics differ from containers). It is *ready* only after a match algorithm has filled it; most members have undefined behavior on a non-ready object. Element `0` is the whole match (always `matched`); element `n` is marked sub-expression `n`; also `prefix()`, `suffix()`, `position(n)`, `length(n)`, `str(n)`, `format(...)`. Typedefs `cmatch`, `smatch`, `wcmatch`, `wsmatch`.

## Algorithms (`[re.alg]`)

All take bidirectional iterators (or a pointer/`string`) and may throw `regex_error` only with `error_complexity` or `error_stack`.

| Function | Meaning |
|---|---|
| `regex_match(first, last, m, e, flags)` | does the regex match the **whole** sequence? On success `m.size() == 1 + e.mark_count()`, `m[0]` spans `[first, last)`, prefix and suffix are empty; on failure `m.size() == 0` (ready) |
| `regex_search(first, last, m, e, flags)` | is there **some subsequence** that matches? `m[0]` is the match; `prefix()` = `[first, m[0].first)`, `suffix()` = `[m[0].second, last)`. For an unmatched sub-expression, `first == second == last` and `matched` is false |
| `regex_replace(out, first, last, e, fmt, flags)` (and a string-returning form) | uses a `regex_iterator` to find every match; copies non-matching sections unless `format_no_copy`; applies `format` for each match; `format_first_only` stops after the first |

The overloads taking a **temporary `basic_string`** together with a `match_results` are `= delete`d, so a result can't refer into a dead string. See `ssub_match` / `smatch` for string use.

## Iterators (`[re.iter]`)

- `regex_iterator` (`cregex_iterator`, `sregex_iterator`, ...) is a forward-style adaptor that enumerates **all matches** by repeated `regex_search`; it holds `begin`, `end`, a pointer to the regex, flags and the current match. Dereference yields the `match_results`. Handling of **zero-length matches**: after one, the next search starts at the same position with `match_not_null | match_continuous` and, if that fails, advances by one character; `++` at the end of input after a zero-length match produces the end iterator. Two iterators are equal if both are end iterators, or have identical range, regex pointer, flags and `match[0]`.
- `regex_token_iterator` enumerates chosen sub-expressions of each match, given a list of indices; index `-1` selects the *non-matching* sections (field splitting), `0` the whole match.

## ECMAScript grammar (`[re.grammar]`)

The default grammar is ECMA-262's, modified: POSIX-style bracket-expression atoms inside a character class are added: `ClassAtomExClass` (written colon-name-colon between brackets, e.g. alpha), `ClassAtomCollatingElement` (dot-delimited name) and `ClassAtomEquivalence` (equals-delimited name); valid class names include `alnum alpha blank cntrl digit graph lower print punct space upper xdigit` plus `d s w`; invalid class or collating names, and Unicode escapes larger than `charT`, throw `regex_error`. Character comparison during matching is `translate_nocase` equality under `icase`, `translate` equality under `collate`, else `==`; ranges `[c1-c2]` are locale-sensitive under `collate`. Digit-to-integer conversion goes through the traits' `value`.

## Related

[[cpp17-lib-regex]] · [[basic-string]] · [[locale-class-and-facets]] · [[iterator-adaptors]] · [[memory-resources-pmr]] (`pmr::match_results`)
