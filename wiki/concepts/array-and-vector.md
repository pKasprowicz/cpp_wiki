---
type: concept
title: "std::array and std::vector (including vector<bool>)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `array` and `vector` (`[array]`, `[vector]`, `[vector.bool]`)

The two contiguous sequence containers. Parent: [[cpp17-lib-containers]]. Requirements they implement: [[container-requirements]], [[sequence-container-requirements]]. Invalidation: [[iterator-invalidation]].

## `array<T, N>` (`[array]`)

- A fixed-size, **contiguous**, reversible container with `size() == N` always. It is an **aggregate** that can be list-initialized with up to `N` elements convertible to `T`; it relies on the implicitly-declared special members, and its implicit move operations require `T` to be move-constructible/assignable. Deduction guide `array(T, U...) -> array<T, 1 + sizeof...(U)>` requires all of `T, U...` to be the same type (otherwise ill-formed).
- It meets the container and reversible container requirements **except** that a default-constructed `array` is *not* empty and `swap` is *linear* (equivalent to `swap_ranges`), not constant (`/3`). It satisfies only some sequence-container requirements (no insertion/erasure; `front`, `back`, `operator[]`, `at`, `data` exist). `fill(u)` is `fill_n(begin(), N, u)`.
- `data()` is such that `data() == addressof(front())` and `[data(), data()+size())` is valid.
- **Zero-sized arrays** (`N == 0`) are supported: `begin() == end()` (a unique value), `data()` is unspecified, `front()`/`back()` are undefined behavior, and `swap` has a non-throwing exception specification (`[array.zero]`).
- Tuple interface: `tuple_size<array<T,N>>` = `N`, `tuple_element<I, array<T,N>>` = `T`, `get<I>(a)` (ill-formed if `I >= N`) — so `array` participates in [[structured-bindings]]. `swap(array&, array&)` participates only if `N == 0` or `T` is swappable.

## `vector<T, Allocator>` (`[vector]`)

- Sequence container with amortized-constant insertion/erasure **at the end**, linear in the middle. Meets container, reversible, sequence (all optional operations except `push_front`/`pop_front`/`emplace_front`), allocator-aware requirements and, for `T` other than `bool`, the contiguous-container requirement. An **incomplete `T`** is allowed if the allocator meets the completeness requirements, but `T` must be complete before any member is referenced ([[allocators]]).
- **Constructors**: empty/allocator; `n` default-inserted elements (T DefaultInsertable); `n` copies; iterator range (for forward-or-better iterators: exactly `N` copy constructions, no reallocation; for pure input iterators: order `N` copies and order `log N` reallocations); initializer list; copy/move (+ allocator).
- **Capacity**: `capacity()`; `reserve(n)` (T MoveInsertable; throws `length_error` if `n > max_size()`; reallocates **iff** the current capacity is less than `n`; after `reserve`, no reallocation until size would exceed capacity — this is the guarantee that makes reserve useful for avoiding invalidation); `shrink_to_fit()` (non-binding; reallocation invalidates everything including past-the-end); `resize(sz[, c])` (erases the tail, or appends default-inserted/copies; no effect if an exception is thrown other than by a non-CopyInsertable T's move constructor).
- **Modifiers**: `insert` and `emplace` family (reallocation if the new size exceeds capacity); exception safety: if an exception is thrown other than by `T`'s copy/move constructor or assignment (or by an input iterator operation), there are no effects; if thrown while inserting a *single* element at the end and `T` is CopyInsertable or nothrow-move-constructible, there are no effects; otherwise, if a non-CopyInsertable `T`'s move constructor throws, the effects are unspecified. `erase` invalidates at or after the erased point; its assignments are the only source of exceptions. `data()` points at `front()` for a non-empty vector. `swap` is constant and exchanges capacity too.
- Non-member `swap`, comparison operators (`==`, `<`, ...), `hash<vector<bool>>`.

## `vector<bool>` (`[vector.bool]`)

A specialization optimized for space: same semantics as the primary template except that **bool operations map to bit values in the storage and `allocator_traits::construct` is not used for the elements**; there is no requirement of contiguous `bool` storage (a bit representation is recommended), so it is **not** a contiguous container. `reference` is a proxy class simulating a reference to one bit (converts to `bool`, assignable from anything convertible to `bool`, has `flip()`); `vector<bool>::flip()` complements all elements. `swap(reference, reference)` and `hash<vector<bool>>` are provided. Concurrent modification of *different elements* of a `vector<bool>` is the one case excluded from the container data-race guarantee ([[container-requirements]]).

## Related

[[deque-and-lists]] · [[container-adaptors]] (`stack`/`queue` over `deque`/`vector`) · [[bitset]] (fixed-size bits) · [[pair-and-tuple]] · [[memory-resources-pmr]] (`pmr::vector`)
