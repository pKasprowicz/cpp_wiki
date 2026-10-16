---
type: concept
title: "std::pair and std::tuple"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `pair` and `tuple` (`[pairs]`, `[tuple]`)

Heterogeneous fixed-size aggregates. Parent: [[cpp17-lib-utilities]]. They are the standard "tuple-like" types that [[structured-bindings]] decomposes through `tuple_size`/`tuple_element`/`get`.

## `pair<T1, T2>` (`[pairs.pair]`)

- Public members `first`, `second`; typedefs `first_type`, `second_type`. Constructors and members throw only if an element-wise operation throws (`/1`). The defaulted copy/move constructors are `constexpr` iff the element operations would be; the destructor is trivial if both element destructors are (`/2`).
- **Conditional `explicit`**: every converting constructor is `explicit` exactly when at least one element conversion is not implicit (e.g. `is_convertible_v<U1&&, first_type>` is false). Constructors take part in overload resolution only if the elements are constructible from the arguments (default: both default-constructible; `pair(const T1&, const T2&)`: both copy-constructible; `pair(U1&&, U2&&)`; `pair(const pair<U1,U2>&)`; `pair(pair<U1,U2>&&)`).
- **Piecewise construction**: `pair(piecewise_construct, tuple<Args1...>, tuple<Args2...>)` builds `first` and `second` in place from the unpacked tuples (`[pair.piecewise]`).
- Assignment: copy and move assignment are *deleted* unless both elements support them; converting assignments from `pair<U1,U2>` participate only when the element assignments are valid. `swap` requires element-wise swappability. Deduction guide `pair(T1, T2) -> pair<T1, T2>` exists (`[pairs.pair]`).
- Comparison (`[pairs.spec]`): `==` is element-wise; `<` is lexicographic (`x.first < y.first || (!(y.first < x.first) && x.second < y.second)`); `!=`, `>`, `<=`, `>=` derive from them.
- `make_pair(x, y)` forwards its arguments and **unwraps `reference_wrapper`** (`reference_wrapper<X>` becomes `X&`); otherwise element types are the decayed argument types (`/9`).
- Tuple-like access (`[pair.astuple]`): `tuple_size<pair<..>>` is 2; `tuple_element<0/1>`; `get<0/1>(p)` and `get<T>(p)` (the latter requires `T1` and `T2` distinct, else ill-formed).

## `tuple<Types...>` (`[tuple.tuple]`)

- Any number of elements, including zero; the destructor is trivial if all element destructors are; exceptions arise only from element operations; the defaulted copy/move constructors are `constexpr` iff the element operations are (always for `tuple<>`).
- Constructors mirror `pair`: default (value-initializes all), `tuple(const Types&...)`, `tuple(UTypes&&...)` (sizes equal, at least one element), converting copy/move from `tuple<UTypes...>`, from `pair<U1,U2>` (only for two-element tuples), and allocator-extended forms `tuple(allocator_arg_t, const Alloc&, ...)` that use *uses-allocator construction* ([[allocators]]). Each is `explicit` iff some element conversion is not implicit. The one-element converting constructors have extra constraints so that `tuple<T>` does not accidentally convert from a `tuple<U>` when `T` is constructible from the tuple itself (`[tuple.cnstr]/16, 18`).
- Assignment is deleted unless all elements are copy/move assignable; converting assignment from `tuple<UTypes...>` or `pair` requires element-wise assignability. Deduction guides cover element packs, allocator forms and `pair` (`tuple(UTypes...) -> tuple<UTypes...>`, `tuple(pair<T1,T2>) -> tuple<T1,T2>`).
- **Creation** (`[tuple.creation]`): `make_tuple` decays arguments and unwraps `reference_wrapper`; `forward_as_tuple` builds a tuple of **forwarding references** to the arguments (the result must not outlive them — do not store it in a named variable); `tie` builds a tuple of lvalue references, and assigning to `ignore` has no effect; `tuple_cat` concatenates the elements of several tuples, with the requirement that each element be constructible from the source tuple element (cv/ref-qualification respected).
- **`apply(f, t)`** calls `f` with the elements of `t` unpacked, and `make_from_tuple<T>(t)` constructs a `T` from them (`[tuple.apply]`).
- **Helpers** (`[tuple.helper]`): `tuple_size<T>` is a UnaryTypeTrait with value `sizeof...(Types)`; `tuple_element<I, T>::type` is the Ith type (`I` out of range is ill-formed). cv-qualified versions (`tuple_size<const T>` etc.) exist and are SFINAE-friendly (no `value` if `tuple_size<T>::value` is not well-formed). These templates are available from `<tuple>`, `<array>` and `<utility>`.
- **Element access** (`[tuple.elem]`): `get<I>(t)` (ill-formed if out of bounds); `get<T>(t)` (ill-formed unless `T` occurs exactly once in `Types`). For a reference element type `X&` the result is `X&` even from an rvalue tuple, and constness is shallow (`const tuple<X&>` yields `X&`, not `const X&`) (informative notes).
- **Relational** operators (`[tuple.rel]`): `==` is element-wise, short-circuiting at the first unequal pair (two empty tuples are equal); `<` is lexicographic, requiring both `a < b` and `b < a` to be valid for each element pair; the other operators derive from these.
- `swap` swaps element-wise; `uses_allocator<tuple<Types...>, Alloc>` is specialized (derived from `true_type`) for any `Alloc` that is an Allocator (`[tuple.traits]`).

## Related

[[cpp17-lib-utilities]] · [[utility-move-forward-swap]] (in_place, piecewise tags) · [[structured-bindings]] · [[function-objects-and-invoke]] (`reference_wrapper`, `invoke`) · [[array-and-vector]] (`array` is also tuple-like) · [[template-argument-deduction]] (deduction guides)
