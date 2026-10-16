---
type: concept
title: "std::basic_string_view"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `basic_string_view<charT, traits>` (`[string.view]`)

A non-owning, read-only reference to a contiguous sequence of char-like objects; `string_view`, `u16string_view`, `u32string_view`, `wstring_view` are the standard instantiations. Parent: [[cpp17-lib-strings]]. Owning counterpart: [[basic-string]].

## Model (`[string.view.template]`)

- `traits` must satisfy the character traits requirements and `traits::char_type` must be `charT` ([[char-traits]]). The view holds `(data_, size_)`; **it does not own, copy or null-terminate the characters.**
- Complexity of members is O(1) unless stated.
- Construction: default (empty, `data_ == nullptr`); from `const charT*` (requires a valid range up to `traits::length(str)`, cost O(length)); from `(const charT*, len)` (valid range `[str, str+len)`); copy. Both element-pointer forms are `constexpr`.
- **Iterators** are constant random-access and contiguous iterators; for a non-empty view `&*begin() == data_`. Any operation that invalidates a pointer in `[data(), data()+size())` invalidates pointers, iterators and references obtained from the view. The container-iterator requirements apply to `const_iterator` ([[iterator-categories-and-requirements]]).
- Element access: `operator[]` (precondition `pos < size()`), `at` (throws `out_of_range`), `front`, `back`, `data()`. Capacity: `size`, `length`, `max_size`, `empty`.
- Modifiers: `remove_prefix(n)`, `remove_suffix(n)` (precondition `n <= size()`; adjust the view only), `swap`.
- Operations: `copy(s, n, pos)` (throws `out_of_range` if `pos > size()`), `substr(pos, n)` (same throw; returns a view), `compare` overloads (like `basic_string::compare`; lexicographic via `traits::compare` then lengths), and the six searches (`find`, `rfind`, `find_first_of`, `find_last_of`, `find_first_not_of`, `find_last_not_of`; worst case O(size × needle size)) with `npos` for "not found".

## Non-members and conversions

- The six comparison operators compare via `compare`; the standard guarantees extra overloads so that any type implicitly convertible to the view can be compared with a view on either side (Table 67).
- `operator<<` writes a view as a formatted output function with padding (`os.width()`) and resets the width ([[formatted-and-unformatted-io]]). `hash` specializations are enabled; the literal suffix `""sv` makes `string_view`, `u16string_view`, `u32string_view`, `wstring_view`.
- `basic_string` converts to `basic_string_view` implicitly (`operator basic_string_view`), and has constructors/assignment/append/etc. from view-convertible types; the reverse direction (view to string) is `explicit` ([[basic-string]]). `begin`/`end`/`size`... free-function range access is available from `<string_view>` ([[iterator-adaptors]]).

## Dangling

Because a view is only a pointer and a length, the rule in `[string.view.iterators]/2` ties its validity to the validity of pointers into the designated characters: when those are invalidated (for example by a `basic_string` reallocation), the view and its iterators are too.

## Related

[[basic-string]] · [[char-traits]] · [[cpp17-lib-strings]] · [[optional]] and [[variant]] (other vocabulary types)
