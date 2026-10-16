---
type: concept
title: "std::deque, std::list and std::forward_list"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `deque`, `list`, `forward_list` (`[deque]`, `[list]`, `[forwardlist]`)

Parent: [[cpp17-lib-containers]]. Common contracts: [[container-requirements]], [[sequence-container-requirements]]; invalidation per operation: [[iterator-invalidation]]. Contiguous sequences: [[array-and-vector]].

## `deque<T, Allocator>` (`[deque]`)

- Random-access iterators; constant-time insertion and erasure **at both ends**, linear in the middle (linear in the number of elements inserted plus the *lesser* of the distances to the two ends). Inserting a single element at either end is constant time and constructs exactly once. Satisfies the container, reversible, sequence (including **all** optional sequence operations), and allocator-aware requirements. Incomplete `T` is allowed under the allocator completeness rule.
- No `capacity()`/`reserve()`; `shrink_to_fit()` exists and invalidates everything including past-the-end. `resize` and constructors work as for `vector`.
- **Invalidation (`[deque.modifiers]`)**: insertion in the middle invalidates all iterators *and* references; insertion at either end invalidates all iterators but **not references**; erasure of the last element invalidates only past-the-end and erased elements; erasure of the first (but not last) invalidates only the erased elements; erasure in the middle invalidates past-the-end and everything else. A throwing single-element insert at either end has no effect.

## `list<T, Allocator>` (`[list]`)

- Doubly-linked sequence with **bidirectional** iterators; constant-time insertion and erasure anywhere; no `operator[]`/`at`. `insert`/`emplace` never affect the validity of iterators and references; `erase` invalidates only the erased elements. Insertion of a single element is constant time with exactly one constructor call; ranges are linear with exactly one copy/move per inserted element (`[list.modifiers]`).
- Operations that **relink** nodes (all require `get_allocator() == x.get_allocator()`, undefined otherwise):
  - `splice(pos, x[, i | first, last])`: move elements from another list (or within the same list) before `pos`. Pointers/references to moved elements stay valid, and iterators keep referring to them but now iterate within the destination list. Constant time for the first two forms, and for the range form if `&x == this`; linear otherwise.
  - `remove(value)`, `remove_if(pred)`, `unique([pred])`: erase matching elements, invalidating only erased ones; stable; exactly `size()` (or `size()-1`) predicate applications.
  - `merge(x[, comp])`: merge two sorted lists (stable; `x` becomes empty; no element is copied; a self-merge does nothing).
  - `sort([comp])`: stable, `N log N`; `reverse()`: linear. Neither affects the validity of iterators and references; if `sort` throws, the order is unspecified.

## `forward_list<T, Allocator>` (`[forwardlist]`)

- Singly-linked sequence with **forward** iterators. Meets the container requirements **except** that it has **no `size()`** and `operator==` is linear; allocator-aware; supports `assign` and several optional operations (`front`, `emplace_front`, `push_front`, `pop_front`, `resize`).
- Because insertion needs the predecessor, the interface is `*_after`: `before_begin()`/`cbefore_begin()` (a non-dereferenceable iterator whose increment is `begin()`; `before_begin() == end()` is false), `insert_after`, `emplace_after`, `erase_after`, `splice_after`. `position` must be `before_begin()` or a dereferenceable iterator in `[begin(), end())`.
- `insert_after` never affects validity; `erase_after` invalidates only the erased elements; `clear()` does not invalidate past-the-end. Inserting `n` elements is linear in `n` with exactly `n` copy/move constructions. `resize` erases the tail or appends default-inserted/copied elements.
- `remove`, `remove_if`, `unique`, `merge`, `sort`, `reverse`, and `splice_after` behave like `list`'s (stable; `sort` and `reverse` do not affect validity; the splice forms are O(1), O(1), and O(distance) respectively).

## Related

[[array-and-vector]] · [[container-adaptors]] (`queue` over `deque`/`list`) · [[iterator-categories-and-requirements]] · [[algorithm-requirements]] (list members substitute for algorithms needing random access)
