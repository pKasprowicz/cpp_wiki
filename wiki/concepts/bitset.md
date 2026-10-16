---
type: concept
title: "std::bitset"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `bitset<N>` (`[bitset]`)

A fixed-size sequence of `N` bits. Parent: [[cpp17-lib-utilities]].

## Model (`[template.bitset]`)

- Each bit is zero (reset) or one (set); position `pos` corresponds to integer value `1 << pos`, so converting to/from integral types treats position 0 as the least significant bit.
- Three error kinds map to exceptions: invalid-argument → `invalid_argument` (bad character in a string), out-of-range → `out_of_range` (bad bit position or string offset), overflow → `overflow_error` (value does not fit when converting to `unsigned long`/`unsigned long long`) ([[standard-exception-classes]]).

## Construction (`[bitset.cons]`)

- Default: all bits zero. From `unsigned long long` `val`: the first `M = min(N, bits in unsigned long long)` positions take `val`'s bits; the rest are zero. From a `basic_string` (or `const charT*`) with optional position, length, and characters standing for zero/one: throws `out_of_range` if `pos > str.size()` and `invalid_argument` if a character in the effective range is neither; **the last character of the range is bit 0**, earlier characters are higher bits ([[basic-string]]).

## Members (`[bitset.members]`)

`&=`, `|=`, `^=` (bitwise with another bitset), `<<=`, `>>=` (shift in zeros), `set()`/`set(pos, val=true)`, `reset()`/`reset(pos)`, `flip()`/`flip(pos)`, `operator~`, `to_ulong()`, `to_ullong()`, `to_string()` (character N-1 corresponds to bit 0), `count()`, `size()` (= `N`), `==`/`!=`, `test(pos)` (throws `out_of_range`), `all()`, `any()`, `none()`, `<<`/`>>` returning shifted copies, and `operator[]`.

- `operator[](pos)` has **no range check** (precondition: valid `pos`); the const form returns `bool`, the non-const form returns a proxy `bitset::reference` such that `(*this)[pos] = val` is equivalent to `set(pos, val)`. For data-race purposes any access through the proxy potentially touches the *entire* bitset (`/51`).

## Non-member operators and I/O (`[bitset.operators]`)

`&`, `|`, `^` on bitsets. `operator>>(istream&, bitset&)` is a formatted input function that extracts at most `N` characters equal to `'0'`/`'1'` (via `widen`), stops at end-of-file or any other character (which is left unread), builds the bitset as from a string, and sets `failbit` if nothing was stored. `operator<<` writes the string form. `hash<bitset<N>>` is enabled. See [[formatted-and-unformatted-io]].

## Related

[[cpp17-lib-utilities]] · [[library-requirements-and-conformance]] (bitmask types may be implemented as `bitset`)
