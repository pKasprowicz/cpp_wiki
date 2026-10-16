---
type: concept
title: "ios_base, basic_ios, stream state, format flags, standard stream objects"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Iostreams base classes (`[iostreams.base]`, `[iostream.objects]`, `[iostreams.requirements]`)

Parent: [[cpp17-lib-input-output]]. Buffers: [[stream-buffers]]. Formatting/parsing: [[formatted-and-unformatted-io]], [[locale-standard-facets]]. Derived stream classes: [[string-and-file-streams]].

## Class layout (`[iostream.forward.overview]`)

`basic_ios<charT, traits>` is a **virtual base** of `basic_istream` and `basic_ostream`; `basic_iostream` derives from both. `basic_streambuf` is the base of `basic_stringbuf` and `basic_filebuf`. `basic_istringstream`/`basic_ifstream` derive from `basic_istream`, the `o` versions from `basic_ostream`, and `basic_stringstream`/`basic_fstream` from `basic_iostream`. `ios_base` is the non-template base of `basic_ios`. `fpos<state_type>` carries stream positions; `streampos`, `wstreampos` etc. are its specializations. The classes behave as specified when `traits::pos_type`/`off_type` are `streampos`/`streamoff`; otherwise behavior is implementation-defined.

## `ios_base` (`[ios.base]`)

- **Member types**: `failure` (an exception class derived from `system_error`; implementations *should* give an `error_code` identifying the reason, `[ios::failure]`), `Init`, and three bitmask types plus one enumeration.
- **`fmtflags`** (bitmask): `boolalpha`, `dec`, `oct`, `hex`, `fixed`, `scientific`, `left`, `right`, `internal`, `showbase`, `showpoint`, `showpos`, `skipws`, `unitbuf`, `uppercase`; groups `adjustfield` (`left|right|internal`), `basefield` (`dec|oct|hex`), `floatfield` (`scientific|fixed`). `flags()`, `flags(f)`, `setf(f)`, `setf(f, mask)` (clears `mask` then sets `f & mask`), `unsetf(mask)` all return the previous flags; `precision()` (default 6), `width()` (minimum field width; reset to 0 by most formatted operations).
- **`iostate`**: `badbit` (loss of integrity of the sequence), `eofbit` (input reached the end), `failbit` (input failed to read the expected characters, or output failed to generate them), `goodbit` = 0.
- **`openmode`**: `app` (seek to end before each write), `ate` (seek to end on open), `binary`, `in`, `out`, `trunc`. **`seekdir`**: `beg`, `cur`, `end`.
- **Locale**: `imbue(loc)` calls registered callbacks with `imbue_event` and returns the previous locale; `getloc()` returns the imbued locale, or the global locale in effect at construction ([[locale-class-and-facets]]).
- **`sync_with_stdio(bool)`**: the standard streams are synchronized with C `stdio` by default (first call returns true); calling it before any I/O with `false` lets them run independently of the C streams; calling it after I/O is implementation-defined.
- **Private storage**: `xalloc()` returns a unique index; `iword(i)`/`pword(i)` give long/pointer slots (references invalidated by later calls). **Callbacks**: `register_callback(fn, index)` — called for `imbue`, `copyfmt` and destruction in reverse registration order; `fn` must not throw.
- `ios_base` has no useful constructor: members are indeterminate until `basic_ios::init` is called, and not calling it before use or destruction is undefined.

## `basic_ios` (`[ios]`)

- **State**: `rdstate()`, `clear(state)`, `setstate(state)`, `good()`, `eof()`, `fail()` (failbit or badbit), `bad()`, `explicit operator bool` (= `!fail()`), `operator!`. `exceptions(mask)` selects which state bits throw `ios_base::failure` whenever they become set via `clear`/`setstate`; a null `rdbuf()` forces `badbit`.
- `init(sb)` postconditions: `rdbuf() == sb`, `tie() == 0`, `rdstate()` = `goodbit` (or `badbit` if `sb` is null), `exceptions() == goodbit`, `flags() == skipws | dec`, `width() == 0`, `precision() == 6`, `fill() == widen(' ')`, `getloc()` = global locale.
- `tie()`: the output stream flushed before each input operation on this stream (`cin.tie() == &cout`; `cerr` is tied to `cout` and has `unitbuf`). `rdbuf()`/`rdbuf(sb)` (the latter calls `clear()`), `imbue`, `narrow`/`widen` (via `ctype`), `fill()`, `copyfmt(rhs)` (copies formatting state, tie, exceptions and callbacks, but **not** `rdstate()` or `rdbuf()`), `move`/`swap` (protected; do not move the buffer), `set_rdbuf`.
- `ios_base` manipulators: `boolalpha`/`noboolalpha`, `showbase`, `showpoint`, `showpos`, `skipws`, `uppercase`, `unitbuf`, `internal`/`left`/`right`, `dec`/`hex`/`oct`, `fixed`/`scientific`/`hexfloat`/`defaultfloat` — each a function that calls `setf`/`unsetf` and returns the stream.

## Standard stream objects (`<iostream>`, `[iostream.objects]`)

`cin`, `cout`, `cerr`, `clog` and the wide `wcin`, `wcout`, `wcerr`, `wclog` are bound to the C streams `stdin`, `stdout`, `stderr` (and `clog` to `stderr`). They are constructed before the first `ios_base::Init` object exists (including the implicit one that including `<iostream>` introduces) and **never destroyed**; the `Init` destructor flushes `cout`, `cerr`, `clog` and the wide ones. Concurrent use of a *synchronized* standard stream's formatted and unformatted functions does not race. Mixing narrow and wide stream operations follows C's `FILE` rules.

## Requirements (`[iostreams.requirements]`)

- No library function other than `ios_base::imbue` and `basic_filebuf::pubimbue` calls `imbue`; calling `imbue` from a user function invoked by the library is undefined.
- **Thread safety**: concurrent access to stream objects, stream buffers or C streams from several threads may be a data race unless stated otherwise; if a write by one thread is read by another without a race, the write *synchronizes with* the read ([[memory-model-and-data-races]]).

## `fpos`

`fpos<stateT>` wraps an `streamoff` plus a conversion state; `state()` gets/sets the state; it supports the position arithmetic in Table 112 (conversion to/from `streamoff`, `==`, `!=`, `+`, `-`).

## Related

[[cpp17-lib-input-output]] · [[stream-buffers]] · [[formatted-and-unformatted-io]] · [[string-and-file-streams]] · [[error-codes-and-system-error]] · [[char-traits]]
