---
type: concept
title: "basic_streambuf: get/put areas and the buffering interface"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Stream buffers (`[stream.buffers]`)

The abstract layer between stream classes and character sources/sinks. Parent: [[cpp17-lib-input-output]]. Users: [[stream-base-classes]], [[formatted-and-unformatted-io]], [[string-and-file-streams]], the buffer iterators in [[iterator-adaptors]].

## Model (`[streambuf.reqts]`)

A stream buffer controls two character sequences: an **input** sequence and an **output** sequence. Each is characterized by three pointers into one `charT` array: *beginning* (`xbeg`), *next* (`xnext`) and *end* (`xend`). Invariants:

- If `xnext` is non-null then `xbeg` and `xend` are non-null and point into the same array; otherwise all three are null.
- **Write position** available iff `xnext` non-null and `xnext < xend` for the output sequence.
- **Putback position** available iff `xbeg < xnext` for the input sequence (`xnext[-1]` is defined).
- **Read position** available iff `xnext < xend` for the input sequence.

The input-area pointers are exposed (to derived classes) as `eback()`, `gptr()`, `egptr()` and the output-area ones as `pbase()`, `pptr()`, `epptr()`. A buffer may be unreadable or unwritable, may map to external representations, and may restrict putback or repositioning.

## Public interface (`[streambuf.members]`) and the virtual hooks

| Public (non-virtual) | Delegates to / behavior |
|---|---|
| `pubimbue(loc)` / `getloc()` | `imbue(loc)`; `getloc` is the last imbued locale, else the global locale at construction |
| `pubsetbuf(s, n)`, `pubseekoff(off, way, which)`, `pubseekpos(sp, which)`, `pubsync()` | `setbuf`, `seekoff`, `seekpos`, `sync` |
| `in_avail()` | `egptr() - gptr()` if a read position exists, else `showmanyc()` |
| `snextc()` | `sbumpc()` then `sgetc()` (eof if the first hit eof) |
| `sbumpc()` | if no read position: `uflow()`; else returns `*gptr()` and advances |
| `sgetc()` | if no read position: `underflow()`; else `*gptr()` without advancing |
| `sgetn(s, n)` | `xsgetn(s, n)` |
| `sputbackc(c)` | `pbackfail(c)` when there is no putback position or `c` differs from `gptr()[-1]`; else steps back |
| `sungetc()` | `pbackfail()` if none; else steps back |
| `sputc(c)` | if no write position: `overflow(c)`; else store and advance |
| `sputn(s, n)` | `xsputn(s, n)` |

Derived classes customize behavior by overriding the **protected virtual** functions `imbue`, `setbuf`, `seekoff`, `seekpos`, `sync`, `showmanyc`, `xsgetn`, `underflow`, `uflow`, `pbackfail`, `xsputn`, `overflow`; they also set the six pointers with `setg` / `setp` and move them with `gbump` / `pbump`. A `basic_streambuf` is constructible only by derived classes (default and copy-style constructors are protected); a freshly constructed one has all pointers null and `getloc()` equal to the global locale.

Output functions of `basic_ostream` may invoke only `overflow`, `xsputn` and `sync` among the buffer's virtual members ([[formatted-and-unformatted-io]]).

## Related

[[string-and-file-streams]] (`stringbuf`, `filebuf`) · [[iterator-adaptors]] (`istreambuf_iterator`) · [[char-traits]] (`eof`, `to_int_type`) · [[stream-base-classes]] · [[deprecated-library-facilities]] (`strstreambuf`, `wbuffer_convert`)
