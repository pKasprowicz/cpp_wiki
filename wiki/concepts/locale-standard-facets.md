---
type: concept
title: "Standard locale facets: ctype, codecvt, num_get/num_put, numpunct, collate, time, money, messages"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Standard locale categories and facets (`[locale.categories]`)

Parent: [[cpp17-lib-localization]]; mechanism in [[locale-class-and-facets]]. All facets follow one pattern: public non-virtual members forward to protected virtual `do_*` functions that derived facets override. The summary below is behavioral, not signature-level.

## ctype category (`[category.ctype]`)

- **`ctype<charT>`** wraps the C `<cctype>` facilities: `is(mask, c)` and range form that fills a mask array, `scan_is`/`scan_not` (first character that does/doesn't match), `toupper`/`tolower` (single and range), `widen`/`narrow` (char ↔ `charT`, `narrow` takes a default). The `ctype_base::mask` is a bitmask type (`space`, `print`, `cntrl`, `upper`, `lower`, `alpha`, `digit`, `punct`, `xdigit`, `blank`, `alnum`, `graph`). **istream members must use `ctype` for character classification** during input parsing.
- **`ctype<char>`** is a specialization implemented through a 256-or-larger table (`table_size`); its constructor can take a custom table and a flag saying the facet owns (will `delete[]`) it; `classic_table()` is the "C" locale table. For values ≥ `table_size` the table content is assumed implementation-specific without lookup.
- **`codecvt<internT, externT, stateT>`** converts between character encodings: `out` (internal → external), `in` (external → internal), `unshift`, `encoding`, `always_noconv`, `length`, `max_length`. Conversions stop at the first unconvertible character and always leave the `from_next`/`to_next` pointers one past the last converted element; the result codes distinguish ok/partial/error/noconv. Required specializations: `codecvt<char,char,mbstate_t>` (identity, no conversion), `codecvt<char16_t,char,mbstate_t>` (UTF-16 ↔ UTF-8), `codecvt<char32_t,char,mbstate_t>` (UTF-32 ↔ UTF-8), `codecvt<wchar_t,char,mbstate_t>` (native wide ↔ narrow). File streams use `codecvt` to translate ([[string-and-file-streams]]).

## numeric category (`[category.numeric]`, `[facet.numpunct]`)

- **`num_get<charT, InputIterator>::get`** parses numbers in **three stages**: (1) choose a `scanf`-style conversion specifier from the stream's `flags()` — integer base from `basefield` (`oct` → `%o`, `hex` → `%X`, none → `%i`, else `%d`/`%u`), `%g` for floating point, `%p` for `void*`, plus a length modifier; (2) extract the longest run of characters acceptable for that specifier from the input range, translating via `ctype` and `numpunct` (thousands separators checked against `grouping()` after the fact); (3) convert the accumulated `char` field with `strtoll`/`strtoull`/`strtof`/`strtod`/`strtold`; if the whole field is not converted store zero and set `failbit`; on overflow store the maximum/minimum value (or the maximum for unsigned) and set `failbit`. `bool` parsing uses `numeric` flag `boolalpha` and the `truename()`/`falsename()` strings. `eofbit` is set if input ends during parsing.
- **`num_put<charT, OutputIterator>::put`** formats in four stages: (1) pick a `printf` specifier from the flags (`oct`/`hex` with `uppercase`, `%d`/`%u`, floating `fixed`→`%f`, `scientific`→`%e`/`%E`, both → `%a`/`%A`, else `%g`/`%G`; `showbase`, `showpoint`, `showpos`, precision, length modifier) as `printf` would produce in the "C" locale; (2) convert the chars to `charT` and insert thousands separators and the locale's decimal point from `numpunct`; (3) decide padding from `width()` and `adjustfield` (`left`, `right`, `internal`); (4) write the sequence and reset `width(0)`.
- **`numpunct<charT>`**: `decimal_point()`, `thousands_sep()`, `grouping()` (a `string` of group sizes starting at the rightmost group; the last value repeats; `0`, `CHAR_MAX` or negative means unlimited), `truename()`, `falsename()`. The required specializations return `'.'`, `','`, empty grouping, `"true"`, `"false"` (the classic "C" format).

## collate (`[category.collate]`)

`compare(low1, high1, low2, high2)` returns −1/0/1 (lexicographic in the required specializations); `transform` gives a key string whose lexicographic order matches `compare`; `hash` returns an integer equal for strings that compare equal. `locale::operator()` uses it.

## time category (`[category.time]`)

`time_get` parses a character sequence into a `struct tm` (`get_time`, `get_date`, `get_weekday`, `get_monthname`, `get_year`, and a general `get` driven by a `strptime`-like format); on reaching the end of input it sets `eofbit`; errors set `failbit`. `time_put::put` writes a `tm` according to a `strftime`-style pattern: literal characters are copied immediately and each format sequence is turned into a `do_put` call.

## monetary category (`[category.monetary]`)

`moneypunct<charT, International>` supplies the formatting parameters (decimal point, thousands separator, grouping, currency symbol, positive/negative sign, fractional digits, `pos_format`/`neg_format` as a `pattern` of four parts — `symbol`, `sign`, `value`, and `space`/`none` — each appearing once). `money_get` and `money_put` parse and produce monetary amounts (as `long double` or a digit string) through it, according to the stream's `showbase` and similar flags. The `International` bool selects the international currency symbol form.

## messages (`[category.messages]`)

`messages<charT>`: `open(name, loc)` returns a catalog handle (a `messages_base::catalog`, valid only if obtained from `open`), `get(cat, set, msgid, default)` retrieves a message (returning `default` if not found), `close(cat)`.

## Related

[[locale-class-and-facets]] · [[cpp17-lib-localization]] · [[formatted-and-unformatted-io]] · [[stream-base-classes]] · [[basic-string]] · [[deprecated-library-facilities]] (`codecvt_utf8` family, `wstring_convert`)
