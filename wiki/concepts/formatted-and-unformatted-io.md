---
type: concept
title: "basic_istream / basic_ostream: sentries, formatted and unformatted functions, manipulators"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Formatted and unformatted I/O (`[iostream.format]`)

Parent: [[cpp17-lib-input-output]]. State, flags and buffers: [[stream-base-classes]], [[stream-buffers]]. Numeric parsing/formatting is delegated to facets: [[locale-standard-facets]].

## Common machinery

- **Input functions** are described as obtaining characters through `rdbuf()->sbumpc()`/`sgetc()`; when those return `eof`, the function finishes and does `setstate(eofbit)` (which may throw `ios_base::failure` if enabled). If a called function throws, `badbit` is set; if `badbit` is in `exceptions()` the exception is rethrown, otherwise swallowed and treated as failure (`[istream]/3-4`). **Output functions** insert via `rdbuf()->sputc` and may call only the `overflow`, `xsputn` and `sync` virtual members of the buffer; the same exception rule applies (`[ostream]`).
- **`sentry`**: every formatted and unformatted function constructs a `sentry` first. The input sentry: if `!is.good()` sets `failbit`; otherwise flushes `is.tie()` (if any) and, unless `noskipws` is requested or the stream's `skipws` flag is clear, skips leading whitespace according to the imbued `ctype` (hitting end-of-file during the skip sets `eofbit | failbit`). The sentry converts to `bool`; a false sentry means the function does nothing. The output sentry: if `os.good()`, flushes `os.tie()`; on destruction, if `unitbuf` is set, `uncaught_exceptions()` is zero and the stream is good, it calls `os.rdbuf()->pubsync()` (a return of −1 sets `badbit`, no exception propagated).

## Input (`[input.streams]`)

- **Formatted extractors** (`operator>>`): construct a sentry with skipping of whitespace, then convert using `num_get<charT>` of the stream's locale; failures set `failbit`, end-of-file `eofbit`. Extraction into `char*` (a C-string) reads at most `width() - 1` characters (or fills the largest array that fits), stops at whitespace (per `ctype`) or end-of-file, stores a terminating null, **resets `width(0)`**, and sets `failbit` if no characters were extracted. Extraction into a `char` reads one character. `operator>>(streambuf*)` is an *unformatted* function that copies characters to another buffer. Manipulator forms `operator>>(ios_base& (*)(ios_base&))` etc. just call the function and are not formatted input functions.
- **Unformatted functions** (sentry with `noskipws`): `get()`, `get(c)`, `get(s, n, delim)` (stores at most `n-1` characters, **does not extract the delimiter**, always null-terminates if `n > 0`, sets `failbit` if nothing stored, `eofbit` on end-of-file), `get(streambuf&, delim)`, `getline(s, n, delim)` (like `get` but **extracts and discards the delimiter**, and sets `failbit` if `n-1` characters were stored without finding it), `ignore(n, delim)`, `peek()`, `read(s, n)`, `readsome(s, n)`, `putback(c)`, `unget()`, `sync()`, `tellg()`/`seekg()`, and `gcount()` (the number extracted by the *last unformatted* input function; formatted functions leave it unchanged). Each unformatted function records its count in a member.
- Rvalue-stream extraction (`operator>>(basic_istream&&, T&&)`) forwards to the lvalue overload.

## Output (`[output.streams]`)

- **Formatted inserters** (`operator<<`): construct a sentry, then use `num_put<charT>` for arithmetic types (with the format derived from `flags()`, `precision()`, `width()`, `fill()`), the locale's `ctype` for characters, and string insertion; **padding** adds copies of `fill()` to reach `width()`, placed after the sequence if `adjustfield == left`, otherwise before (with `internal` rules for numeric sign/base); `width(0)` is called afterwards. Failure to generate output sets `failbit`. For `bool` without `boolalpha` the value is output as `int`. `operator<<(const void*)` prints a pointer; `operator<<(streambuf*)` copies from a buffer (unformatted; null sets `badbit`).
- **Unformatted**: `put(c)`, `write(s, n)`, `flush()`, `tellp()`/`seekp()`.
- Rvalue-stream insertion (`operator<<(basic_ostream&&, const T&)`) forwards to the lvalue overload.

## Manipulators

- **`<iomanip>` (`[std.manip]`)**: `resetiosflags(mask)`, `setiosflags(mask)`, `setbase(n)`, `setfill(c)`, `setprecision(n)`, `setw(n)`; each returns an unspecified type that works with both `<<` and `>>` where applicable.
- **Simple manipulators in `<ostream>`/`<istream>`**: `endl` (puts `widen('
')` and then flushes), `ends` (puts a null character `charT()`; does not flush), `flush`, `ws` (skips whitespace).
- **Extended (`[ext.manip]`)**: `get_money`/`put_money` (via `money_get`/`money_put`; the money type must be `long double` or a `basic_string`), `get_time`/`put_time` (via `time_get`/`time_put`).
- **Quoted (`[quoted.manip]`)**: `quoted(s, delim = '"', escape = '\\')` inserts a string surrounded by delimiters with embedded delimiters/escape characters escaped, and extracts the reverse, as a formatted function; works with C strings, `basic_string` and `basic_string_view`.

## Related

[[stream-base-classes]] · [[stream-buffers]] · [[locale-standard-facets]] · [[basic-string]] · [[bitset]] / [[complex-numbers]] / [[string-view]] (their own inserters and extractors)
