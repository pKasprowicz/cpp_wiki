---
type: concept
title: "String streams and file streams (stringbuf, filebuf, ifstream, ofstream, fstream)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# String-based and file-based streams (`[string.streams]`, `[file.streams]`, `[c.files]`)

Concrete stream classes built on [[stream-buffers]] and the interfaces of [[formatted-and-unformatted-io]]. Parent: [[cpp17-lib-input-output]]. Base-class behavior: [[stream-base-classes]].

## String streams (`<sstream>`, `[string.streams]`)

- **`basic_stringbuf<charT, traits, Allocator>`** associates the input and/or output sequence with an arbitrary character sequence that can be initialized from or exposed as a `basic_string` ([[basic-string]]). It remembers an `openmode` (`in` ⇒ readable, `out` ⇒ writable). `str()` returns a copy of the underlying sequence: the whole input area for an input-only buffer, or `[pbase(), high-water mark)` if `out` was set; `str(s)` replaces the contents and re-initializes the pointers according to the mode (`out`: put area starts at the first character, and with `ate` the put pointer is placed at the end; `in`: get area covers all of `s`).
- Overridden virtuals: `underflow` returns the current character without consuming; `pbackfail` can put back in three ways (same character; any character if the buffer is writable; or eof); `overflow` appends if a write position exists or can be made (only with `out`; it may reallocate and extend `egptr()` if `in` is also set); `seekoff`/`seekpos` reposition within the sequence according to the open mode (Table 115).
- **Move**: a moved-to `stringbuf` has the same observable state but the two objects reference separate buffers (whether the pointers are copied verbatim is implementation-defined).
- `basic_istringstream`, `basic_ostringstream`, `basic_stringstream` each own a `basic_stringbuf`, add the corresponding `in`/`out` bits to the open mode, expose `rdbuf()` and `str()`, and are movable and swappable.

## File streams (`<fstream>`, `[file.streams]`)

- **`basic_filebuf`** associates **both** sequences with a file using a *joint file position*, with the same restrictions as C `FILE`s (a stream not open for reading cannot read, etc.). It converts between external bytes and `charT` through `use_facet<codecvt<charT, char, state_type>>(getloc())` ([[locale-standard-facets]]). Behavior is defined only when `traits::pos_type` is `fpos<traits::state_type>`.
- **`open(path, mode)`** (`const char*`, `const string&`, and — in this draft — `filesystem::path` overloads): fails (returns null) if already open; maps the mode (minus `ate`) to a C `fopen` mode string by Table 117; **combinations not in the table fail**:

| `in` | `out` | `trunc` | `app` | `binary` | fopen |
|---|---|---|---|---|---|
| | + | | | | `"w"` |
| | + | | + | | `"a"` |
| | | | + | | `"a"` |
| | + | + | | | `"w"` |
| + | | | | | `"r"` |
| + | + | | | | `"r+"` |
| + | + | + | | | `"w+"` |
| + | + | | + | | `"a+"` |
| + | | | + | | `"a+"` |

(with `binary` set, `b` is appended to the corresponding string). If `ate` is set, it then seeks to the end (as `fseek(file, 0, SEEK_END)`), and closes and fails if the seek fails.
- **`close()`** flushes the put area (`overflow(eof)`), emits any shift termination sequence via `codecvt::unshift` if the last operation was a write, and closes the file regardless of errors in the earlier steps; exceptions from the earlier steps are rethrown after the file is closed. The destructor calls `close()` and swallows exceptions.
- **`basic_ifstream` / `basic_ofstream` / `basic_fstream`** own a `basic_filebuf`, add `in` / `out` / both to the open mode passed to `open`, and set `failbit` if the open fails; `is_open()`, `open(...)`, `close()` (sets `failbit` on failure), `rdbuf()`. Constructors accept `const char*`, `const string&` and `filesystem::path`-based names. They are movable and swappable (swapping the contained filebuf).

## C library files (`[c.files]`)

`<cstdio>` has the contents of C `<stdio.h>`; calls to `tmpnam` with a null argument may race with each other. `<cinttypes>` is C `<inttypes.h>` but includes `<cstdint>`, and adds `imaxabs`/`imaxdiv` signatures if `intmax_t` is an extended integer type. Annex C records that `gets` is no longer defined ([[cpp17-compatibility-differences]]).

## Related

[[stream-base-classes]] · [[stream-buffers]] · [[filesystem]] · [[basic-string]] · [[cpp17-lib-input-output]] · [[deprecated-library-facilities]] (`<strstream>`)
