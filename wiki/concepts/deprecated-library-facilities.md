---
type: concept
title: "Deprecated library facilities (Annex D): strstream, binders, allocator members, conversions"
tags: [cpp17, library, deprecated]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Deprecated library facilities of Annex D

The larger library components of Annex D (`[depr]`, D.6 and D.8-D.11, D.15-D.16). The language features, the headers and the small items (`uncaught_exception`, `is_literal_type`, `result_of`, `std::iterator`, `shared_ptr::unique`) are on [[cpp17-annex-d-compatibility-features]]. All of these are normative but deprecated: still required of a conforming library, candidates for removal. Reading depth: constructors, members and effects of each class were read; the function-by-function wording is summarized, not reproduced.

## Overview

| Facility | Header | Label | Closest non-deprecated facility in this draft (a pointer, not a statement of the standard) |
|---|---|---|---|
| `strstreambuf`, `istrstream`, `ostrstream`, `strstream` | `<strstream>` | D.6, `[depr.str.strstreams]` | string streams: [[string-and-file-streams]] |
| `argument_type` / `result_type` typedefs, weak result types, `not1`, `not2` | `<functional>` and others | D.8, `[depr.func.adaptor.binding]` | `not_fn`, lambdas, `invoke`: [[function-objects-and-invoke]] |
| `allocator<void>`; `std::allocator` members `pointer`, `address`, `construct`, ... | `<memory>` | D.9, `[depr.default.allocator]` | `allocator_traits`: [[allocators]] |
| `raw_storage_iterator` | `<memory>` | D.10, `[depr.storage.iterator]` | uninitialized-memory algorithms: [[uninitialized-memory-algorithms]] |
| `get_temporary_buffer`, `return_temporary_buffer` | `<memory>` | D.11, `[depr.temporary.buffer]` | allocators, containers |
| `codecvt_utf8`, `codecvt_utf16`, `codecvt_utf8_utf16`, `codecvt_mode` | `<codecvt>` | D.15, `[depr.locale.stdcvt]` | the `codecvt` facet itself: [[locale-standard-facets]] |
| `wstring_convert`, `wbuffer_convert` | `<locale>` | D.16, `[depr.conversions]` | none named in the draft; the `codecvt` facet used through a locale |

## char* streams: `<strstream>` (D.6)

Stream classes that read and write a **character array object** rather than a `basic_string`. (The introductory sentence `[depr.str.strstreams]/1` says the header defines "three types", yet the subsections define four classes; see open questions.) The four classes: the buffer `strstreambuf` (derived from `basic_streambuf<char>`) and three stream wrappers that each own one buffer.

### strstreambuf (`[depr.strstreambuf]`)

- **Exposition-only state** (notes, informative): a bitmask `strmode` of four attributes: *allocated* (the array was allocated by the buffer and the destructor must free it), *constant* (the elements are const, so the output sequence cannot be written), *dynamic* (the array is allocated or reallocated as needed because the sequence can change length), *frozen* (the program asked that the array not be altered, reallocated or freed). Plus `alsize` (suggested minimum size of a dynamic array) and two function pointers `palloc` and `pfree`.
- **Seekable area** (`/4`): delimited by `seeklow` and `seekhigh`; undefined if the get-area next pointer is null, otherwise `seeklow` is the get-area beginning and `seekhigh` is the end of the put area if there is one, else the end of the get area.
- **Constructors** (`[depr.strstreambuf.cons]`):

| Form | Mode and ownership |
|---|---|
| `strstreambuf(streamsize alsize_arg = 0)` | *dynamic*; `alsize` = argument; default allocation (`new[]`/`delete[]`) |
| `strstreambuf(palloc_arg, pfree_arg)` | *dynamic*; allocation through the two given function pointers |
| `strstreambuf(char* g, streamsize n, char* p = 0)` and the `signed char` / `unsigned char` overloads | no flags: a fixed array supplied by the program. The array size N is `n` if positive, `strlen(g)` if `n` is 0, and `INT_MAX` if negative. With `p` null the array is input only (get area is the whole array); otherwise the get area ends at `p` and the put area is `p` to `p + N` |
| the same with `const char*` etc. (two arguments) | like the previous with the *constant* attribute set, so it is input only |

- **Destructor**: frees the array only if *allocated* is set and *frozen* is not (`/8`).
- **Members** (`[depr.strstreambuf.members]`): `freeze(bool = true)` sets or clears *frozen* (only for a dynamic buffer); `str()` calls `freeze()` and returns the get-area beginning (possibly null); `pcount()` returns `pnext - pbeg` of the put area, or 0 if there is no put area. From the destructor and `str()` rules it follows that after `str()` the buffer no longer frees the array: the caller becomes responsible for it unless `freeze(false)` is called (a consequence, not a quoted sentence).
- **Overridden virtuals** (`[depr.strstreambuf.virtuals]`):
  - `overflow` appends a character; to make room it reallocates (or first allocates) an array large enough for the existing contents plus at least one more position, through `palloc` if non-null and `new charT[n]` otherwise; on allocation failure it returns EOF; successful allocation sets *allocated*. It cannot extend a non-dynamic or frozen array. Freeing uses `pfree` or `delete[]`.
  - `pbackfail` puts a character back in one of three ways (matching previous char; overwrite unless *constant*; EOF case just decrements); which way is used when several apply is unspecified.
  - `underflow` returns the next character without consuming it; if the put area has advanced beyond the get area it extends the get area up to the put pointer.
  - `seekoff` and `seekpos` position within the seekable area; the outcome of `seekoff` for each `seekdir` and openmode combination is in Tables 145-146; positions outside the seekable area fail; a null next pointer fails; failure is reported as `pos_type(off_type(-1))`.
  - `setbuf(0, 0)` has no effect; other uses are implementation-defined.

### istrstream, ostrstream, strstream

| Class | Constructors | Members |
|---|---|---|
| `istrstream` | `(const char* s)` / `(char* s)`: array is an ntbs (`strstreambuf(s, 0)`); `(s, n)`: array of `n` elements, `n > 0` | `rdbuf()`, `str()` |
| `ostrstream` | `()`: dynamic buffer; `(char* s, int n, openmode mode = out)`: fixed array of `n`; with the append bit the array must hold an ntbs and writing starts at `s + strlen(s)` | `rdbuf()`, `freeze(bool = true)`, `str()`, `pcount()` |
| `strstream` | `()`; `(char* s, int n, openmode mode = in \| out)` with the same append rule | `rdbuf()`, `freeze(bool = true)`, `str()`, `pcount()` |

Each wraps an exposition-only `strstreambuf sb`; `rdbuf()` returns it, `str()` and `pcount()` forward to it, and `freeze` forwards to it. Compare the non-deprecated string streams, which own a `basic_string`: [[string-and-file-streams]], buffer machinery: [[stream-buffers]].

## Old adaptable function bindings (D.8, `[depr.func.adaptor.binding]`)

This is not a set of old binders (`bind1st` etc. are gone; see [[cpp17-annex-d-compatibility-features]]) but the **typedefs and negators** that pre-C++11 adaptors relied on.

- **Weak result type** (`[depr.weak.result_type]`): a call wrapper has a *weak result type* if its `result_type` is a synonym for the return type of the target when the target is a function pointer or member function pointer, for `T::result_type` when the target is a class type where that name is valid, and is not defined otherwise.
- **Typedefs added to standard components** (`[depr.func.adaptor.typedefs]`): the unary function objects (`negate`, `logical_not`, `bit_not`) get `argument_type` and `result_type`; the binary ones (`plus`, `minus`, `multiplies`, `divides`, `modulus`, the six comparison objects, `logical_and`, `logical_or`, `bit_and`, `bit_or`, `bit_xor`) get `first_argument_type`, `second_argument_type` and `result_type` (`bool` for comparisons and logical ones, `T` otherwise). `owner_less` for `shared_ptr` and `weak_ptr`, `map::value_compare` and `multimap::value_compare` get the binary set. `function<R(T1)>` gets `argument_type`; `function<R(T1, T2)>` gets `first_argument_type` and `second_argument_type`. Every enabled `hash<Key>` has `argument_type` = `Key` and `result_type` = `size_t`.
- **`reference_wrapper<T>`** has a weak result type; it defines `argument_type` only if `T` is a function type or pointer taking one argument, a member function pointer taking none (then `cv T0*`), or a class type with a valid `T::argument_type`; and `first_argument_type` / `second_argument_type` under the analogous two-argument conditions.
- **`bind` and `mem_fn`**: the wrapper from `bind(f, args...)` has a weak result type; from `bind<R>(f, args...)` it has `result_type` = `R`. The simple wrapper from `mem_fn(pm)` gets `result_type` for member function pointers, plus `argument_type` / the two-argument names when the pointer takes zero / one argument.
- **Negators** (`[depr.negators]`): `not1(pred)` returns `unary_negate<Predicate>` and `not2(pred)` returns `binary_negate<Predicate>`, whose call operators return `!pred(x)` and `!pred(x, y)` and which require the predicate to supply the old typedefs. The non-deprecated negating wrapper in this draft is `not_fn` ([[function-objects-and-invoke]]).

## The default allocator's older interface (D.9, `[depr.default.allocator]`)

Members and a specialization added to those in `[default.allocator]` ([[allocators]]):

- `template<> class allocator<void>`: `value_type` = `void`, `pointer` = `void*`, `const_pointer` = `const void*`, and a `rebind<U>` that names `allocator<U>`.
- `allocator<T>` gains: `size_type`, `difference_type`, `pointer`, `const_pointer`, `reference`, `const_reference`, `rebind`; `address(x)` (returns `addressof(x)`); `allocate(n, hint)` (allocates through `::operator new(std::size_t)`, unspecified when and how often; throws `bad_alloc`; over-aligned support is implementation-defined); `construct(p, args...)` (as if `::new((void*)p) U(forward<Args>(args)...)`); `destroy(p)` (as if `p->~U()`); `max_size()` (largest `N` for which `allocate(N, 0)` might succeed).
- Containers go through `allocator_traits` in this draft ([[allocators]]), so these members matter mainly to code that names them on `std::allocator` directly (an inference from the structure of the clause, not a quoted rule).

## Raw storage iterator and temporary buffers (D.10, D.11)

- **`raw_storage_iterator<OutputIterator, T>`** (`<memory>`, `[depr.storage.iterator]`): an output iterator whose assignment *constructs* a `T` in the uninitialized memory the wrapped iterator designates, so algorithms can write results into raw storage. The wrapped iterator must be an output iterator whose `operator*` returns something with an `operator&` yielding a `T*`. `operator=(const T&)` requires `CopyConstructible`, `operator=(T&&)` requires `MoveConstructible`; `operator*` returns `*this`; increments advance; `base()` returns the wrapped iterator. Its `value_type`, `difference_type`, `pointer` and `reference` are `void`. Current tools: [[uninitialized-memory-algorithms]].
- **`get_temporary_buffer<T>(ptrdiff_t n) noexcept`** returns `pair<T*, ptrdiff_t>` for uninitialized contiguous storage; the request is **non-binding** (a note says this leaves room for implementation tricks): the implementation may return capacity `N != n`, even 0. If `n <= 0` or nothing could be obtained the result is a null pointer and 0. **`return_temporary_buffer(p)`** deallocates; `p` must come from an earlier `get_temporary_buffer` call that has not been returned; throws nothing. Over-aligned support is implementation-defined.

## Code conversion facets (D.15, `[depr.locale.stdcvt]`)

`<codecvt>` provides `enum codecvt_mode` with the bit values `consume_header` (4), `generate_header` (2), `little_endian` (1), and three class templates `codecvt_utf8`, `codecvt_utf16`, `codecvt_utf8_utf16`, each `template<class Elem, unsigned long Maxcode = 0x10ffff, codecvt_mode Mode = 0>`, each derived from `codecvt<Elem, char, mbstate_t>` with a `refs` constructor and destructor.

| Facet | Converts | File mode |
|---|---|---|
| `codecvt_utf8` | UTF-8 multibyte sequences to/from UCS2 or UCS4 (by size of `Elem`); endianness does not matter | text or binary |
| `codecvt_utf16` | UTF-16 multibyte sequences to/from UCS2 or UCS4; byte order follows `Mode` | **binary only**; writing to a text file is undefined behavior (`[depr.locale.stdcvt.req]/3.3`) |
| `codecvt_utf8_utf16` | UTF-8 to/from UTF-16 (one or two 16-bit codes) | text or binary |

`Maxcode` is the largest wide-character code the facet reads or writes without reporting an error. `Mode` bits: with `consume_header` the facet consumes an initial header (a byte-order mark) when reading, to learn the endianness; with `generate_header` it writes one; with `little_endian` it writes little-endian instead of the default big-endian (`/1`). The text cites ISO/IEC 10646-1:1993 (see [[cpp17-glossary]]). The ordinary facet machinery: [[locale-class-and-facets]], [[locale-standard-facets]].

## Convenience conversion interfaces (D.16, `[depr.conversions]`)

Two class templates in `<locale>` that use a code-conversion facet *without installing it in a locale*:

- **`wstring_convert<Codecvt, Elem = wchar_t, Wide_alloc, Byte_alloc>`**: converts between a wide string (`wide_string`) and a byte string (`byte_string`). `from_bytes` and `to_bytes` each have four overloads: a single element, a null-terminated pointer, a string object, and a pointer range. Behavior: unless the object was constructed with an explicit state, the conversion state is reset to its initial value before each conversion; the number of input elements converted is stored and returned by `converted()`; `state()` returns the conversion state. On a conversion error it returns the error string it was constructed with, or throws `range_error` if there is none. Constructors: `(Codecvt* pcvt = new Codecvt)`, `(pcvt, state)` (state retained across calls), and `(byte_err, wide_err = wide_string())` (creates its own `Codecvt`, stores the error strings); `pcvt` must not be null for the first two. The object **owns** the facet and deletes it in the destructor; copying is deleted. Usage example in the text (informative): `wstring_convert<codecvt_utf8<wchar_t>>` converting `L"Hello\n"` to a UTF-8 byte string for `cout`.
- **`wbuffer_convert<Codecvt, Elem = wchar_t, Tr = char_traits<Elem>>`**: a wide `basic_streambuf<Elem, Tr>` that performs its I/O through an underlying byte `streambuf`, converting with `Codecvt`. Constructor `(streambuf* bytebuf = 0, Codecvt* pcvt = new Codecvt, state_type state = state_type())` (`pcvt` non-null); `rdbuf()` returns the byte buffer, `rdbuf(bytebuf)` replaces it and returns the previous one; `state()` returns the conversion state. It deletes the facet on destruction; copying is deleted.

Both require `Codecvt` to meet the requirements of the standard code-conversion facet `codecvt<Elem, char, mbstate_t>`. Related: [[stream-buffers]], [[locale-class-and-facets]].

## Open questions

- `[depr.str.strstreams]/1` says `<strstream>` defines three types while D.6.1-D.6.4 define four classes (`strstreambuf`, `istrstream`, `ostrstream`, `strstream`); the draft does not say which count is intended.
- Per-function wording of the `strstreambuf` virtual functions was summarized at family level; exact pointer-update rules for `overflow`/`underflow` should be taken from `[depr.strstreambuf.virtuals]`.
- This page reports what the draft says; it does not say which of these facilities later editions removed.

## Related

[[cpp17-annex-d-compatibility-features]] · [[allocators]] · [[function-objects-and-invoke]] · [[locale-standard-facets]] · [[string-and-file-streams]] · [[uninitialized-memory-algorithms]] · [[cpp17-lib-utilities]] · [[cpp17-lib-input-output]] · [[cpp17-lib-localization]]
