---
type: concept
title: "<utility> components: swap, exchange, move, forward, declval, in_place tags, integer_sequence, to_chars/from_chars"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `<utility>` components (`[utility]`, `[intseq]`)

The small foundational helpers. Parent: [[cpp17-lib-utilities]]. Pair, tuple and the other value types have their own pages: [[pair-and-tuple]], [[optional]], [[variant]], [[any-type]].

## Operators (`[operators]`)

`std::rel_ops` supplies `!=`, `>`, `<=`, `>=` templates derived from `==` and `<` (`!(x == y)`, `y < x`, `!(y < x)`, `!(x < y)`). Elsewhere in the library, any `!=`, `>`, `<=`, `>=` declared without further text has exactly these semantics (`[operators]/10`).

## swap and exchange (`[utility.swap]`, `[utility.exchange]`)

- `swap(T&, T&)` exchanges two values; it takes part in overload resolution only when `T` is move-constructible and move-assignable, and is `noexcept` conditionally (`/1-3`). The array overload `swap(T(&)[N], T(&)[N])` requires `a[i]` swappable with `b[i]` and acts like `swap_ranges`. The rule that library code should call swap *unqualified after `using std::swap`* comes from the Swappable requirements ([[library-named-requirements]]).
- `exchange(obj, new_val)` replaces `obj` with `new_val` and returns the old value.

## forward / move helpers (`[forward]`, `[utility.as_const]`, `[declval]`)

All are `constexpr`-capable and signal-safe.

- `forward<T>(t)` is `static_cast<T&&>(t)`; the rvalue overload makes it ill-formed to forward an rvalue as an lvalue reference. This is the "perfect forwarding" primitive.
- `move(t)` is `static_cast<remove_reference_t<T>&&>(t)`; `move_if_noexcept(x)` yields `T&&` if `T` is nothrow-move-constructible or not copy-constructible, otherwise `const T&`.
- `as_const(t)` returns a reference to `t` as const; the overload for const rvalues is deleted.
- `declval<T>()` returns `T&&` for use in unevaluated operands only; odr-using it is ill-formed; `T` may be incomplete.

## in_place tags (synopsis `[utility.syn]`)

Empty tag types used to disambiguate in-place construction: `in_place_t` (`in_place`), `in_place_type_t<T>` (`in_place_type<T>`), `in_place_index_t<I>` (`in_place_index<I>`), plus `piecewise_construct_t` (`piecewise_construct`) for `pair`. Their default constructors are `explicit`, so `{}` cannot silently pick them. Consumers: [[optional]], [[variant]], [[any-type]], [[pair-and-tuple]].

## Compile-time integer sequences (`[intseq]`)

`integer_sequence<T, I...>` (T an integer type) carries a pack of values that a function template can deduce and expand. Aliases: `index_sequence<I...>`, `make_integer_sequence<T, N>` (the sequence 0..N-1; negative N is ill-formed), `make_index_sequence<N>`, `index_sequence_for<Types...>`. See [[cpp17-templates]] for pack expansion.

## Numeric conversion to and from character ranges (`[utility.to.chars]`, `[utility.from.chars]`)

Locale-independent primitives, declared in `<utility>` in this draft.

- **`to_chars(first, last, value[, base])`** writes into the valid range `[first, last)`. On success the result's `ec` is false-valued and `ptr` is one past the last character written; otherwise `ec` is `errc::value_too_large`, `ptr` is `last`, and the buffer contents are unspecified. Integers: `base` must be 2..36, digits above 9 are lowercase, a minus sign is written for negatives, no leading zeros; overloads exist for all signed and unsigned integer types and `char`. Floating-point: without `chars_format` the shortest representation that round-trips via `from_chars` is produced (ties between `f` and `e` style go to `f`); with `chars_format` (`fixed`, `scientific`, `hex` without `0x`, `general`) or with a precision the result is as `printf` in the "C" locale with the matching specifier. Never throws.
- **`from_chars(first, last, value[, base | fmt])`** parses the longest prefix matching the pattern. No match: `value` unchanged, `ptr == first`, `ec == errc::invalid_argument`. Out-of-range: `value` unchanged, `ec == errc::result_out_of_range`. Otherwise `value` is set and `ptr` points to the first unmatched character (or `last`). Integer patterns follow `strtol` in the "C" locale, with no `0x` prefix allowed for base 16 and only `-` allowed as a sign (and only for signed types). Floating patterns follow `strtod` with only `-`, plus rules for `chars_format` (`scientific` requires an exponent, `fixed` forbids it, `hex` assumes `0x`); the result is one of the two nearest representable values. Never throws.

Error codes come from [[error-codes-and-system-error]].

## Related

[[cpp17-lib-utilities]] · [[function-objects-and-invoke]] · [[cpp17-expressions]] (value categories) · [[value-categories]] · [[library-named-requirements]]
