---
type: concept
title: "std::basic_string"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `basic_string<charT, traits, Allocator>` (`[basic.string]`)

The owning string class template; `string`, `u16string`, `u32string`, `wstring` are its common instantiations. Parent: [[cpp17-lib-strings]]. Traits: [[char-traits]]. Non-owning counterpart: [[string-view]].

## General rules (`[basic.string]`, `[string.require]`)

- A `basic_string` is a **contiguous container**; `size() <= capacity()` always. Elements are `charT`; `allocator_traits<Allocator>::value_type` must be `charT` and the string allocates through the allocator ([[allocators]]).
- Two error kinds: `length_error` (any operation that would make `size()` exceed `max_size()`) and `out_of_range` (position arguments past the end) ([[standard-exception-classes]]). **Strong guarantee:** if any member function or operator throws, it has no other effect.
- **Invalidation of references, pointers and iterators**: by passing the string as a non-const reference argument to any library function, and by calling any non-const member function *except* `operator[]`, `at`, `data`, `front`, `back`, `begin`, `rbegin`, `end`, `rend` (`[string.require]/4`). Contrast with the container rules in [[iterator-invalidation]].

## Construction and assignment (`[string.cons]`)

Constructors: default/allocator; copy and move (move leaves the source valid but unspecified; the allocator-extended move throws nothing when allocators compare equal); substring `(str, pos[, n])` (throws `out_of_range` if `pos > str.size()`); from a string-view-convertible `T` (these overloads take part in overload resolution only if `T` converts to `basic_string_view`; the `explicit` `(basic_string_view)` form follows); from `(const charT*, n)`, `(const charT*)` (uses `traits::length`), `(n, c)` (requires `n < npos`), an input-iterator range (not for integer types), `initializer_list`. Assignment: copy (self-assignment is a no-op), move (as a sequence container, may invalidate), from string view, C string, single character, initializer list.

## Capacity, access, modification

- `size()`/`length()`, `max_size()`, `capacity()`, `empty()`, `reserve(n)` (`capacity() >= n` afterwards; `length_error` if `n > max_size()`), `shrink_to_fit()` (non-binding; may reallocate and invalidate), `resize(n[, c])`, `clear()`.
- `operator[]` has precondition `pos <= size()` and returns a reference to the **null character** at `pos == size()` (modifying it to anything else is undefined behavior); `at(pos)` throws `out_of_range` if `pos >= size()`; `front()`/`back()` require non-empty.
- `data()` and `c_str()` return a pointer `p` with `p + i == &operator[](i)` for all `i` in `[0, size()]`, so the buffer is **null-terminated** at `size()`. There is a **non-const `data()`** overload (the program must not alter the character at `p + size()`); Annex C records this as a behavior change that can alter overload choice for code testing `char*` vs `const char*` ([[cpp17-compatibility-differences]]). `operator basic_string_view` converts to a view.
- Modifiers: `operator+=`, `append`, `push_back`, `assign`, `insert`, `erase`, `pop_back`, `replace`, `copy`, `swap` — each in the usual overload families (string, substring, string view or convertible, `(const charT*, n)`, `(const charT*)`, `(n, c)`, iterator range, initializer list). Overloads taking a "T convertible to string view" are excluded when `T` also converts to `const charT*`.
- Search: `find`, `rfind`, `find_first_of`, `find_last_of`, `find_first_not_of`, `find_last_not_of`, each returning a position or `npos`; `substr(pos, n)` (throws `out_of_range` if `pos > size()`); `compare` returns negative/zero/positive after comparing the common prefix with `traits::compare` and then the lengths.
- One deduction guide exists, for the iterator-range constructor (character type taken from `iterator_traits<InputIterator>::value_type`).

## Non-member functions (`[string.nonmembers]`, `[string.conversions]`)

- `operator+` for strings, C strings and characters (rvalue overloads reuse the buffer: `std::move(lhs.append(rhs))`); the six comparison operators (via `compare`), `swap`; `operator<<`/`>>` and `getline` are in the stream clause ([[formatted-and-unformatted-io]]).
- Numeric conversions: `stoi`, `stol`, `stoul`, `stoll`, `stoull`, `stof`, `stod`, `stold` call the C `strto*` function on `str.c_str()` (wide versions use `wcsto*`), store the number of characters consumed in `*idx` if non-null, and throw `invalid_argument` if no conversion could be performed or `out_of_range` if the result is out of range / `errno` is `ERANGE`. `to_string` / `to_wstring` produce the text `sprintf` would give with `%d`, `%u`, `%ld`, `%lu`, `%lld`, `%llu`, `%f`, `%f`, `%Lf`. For locale-independent, non-throwing conversion see `to_chars`/`from_chars` in [[utility-move-forward-swap]].
- For each of the four string types `S` (with `SV` the corresponding string view), `hash<S>()(s) == hash<SV>()(SV(s))` (`[basic.string.hash]`); `""s` literal suffixes (`operator""s`) produce `string`, `u16string`, `u32string`, `wstring` from `(const char*, size_t)` (`[basic.string.literals]`).
- `pmr::string` etc. aliases use [[memory-resources-pmr]].

## Related

[[cpp17-lib-strings]] · [[string-view]] · [[char-traits]] · [[sequence-container-requirements]] · [[bitset]] · [[locale-standard-facets]]
