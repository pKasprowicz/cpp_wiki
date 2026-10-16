---
type: concept
title: "Associative (ordered) container requirements and node handles"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Associative containers (`[associative.reqmts]`, `[container.node]`, `[container.insert.return]`)

Refinement of [[container-requirements]] for `set`, `multiset`, `map`, `multimap`. Parent: [[cpp17-lib-containers]]. Classes: [[ordered-associative-containers]]. Hash-based variants: [[unordered-container-requirements]].

## Model

- Parameterized on `Key` and `Compare`, which must induce a **strict weak ordering**. *Equivalence of keys* means `!comp(a, b) && !comp(b, a)` — not `operator==`. For any two keys in the container `comp` must always return the same answer.
- Unique keys (`set`, `map`) vs. equivalent keys (`multiset`, `multimap`); in the multi containers `insert`, `emplace` and `erase` **preserve the relative order of equivalent elements**, and a new equivalent element goes at the **end** of the existing equal range. `value_type` is `Key` (set) or `pair<const Key, T>` (map); `value_compare` orders pairs by key.
- `iterator` is **bidirectional**; for set-like containers both `iterator` and `const_iterator` are constant iterators (and may or may not be the same type). Elements iterate in non-descending key order; for unique containers strictly ascending (`/11-12`).
- Allocator-aware, except that for maps the Table 83 requirements on `value_type` apply to `key_type` and `mapped_type` separately.
- The container stores a **copy** of the comparison object (never a pointer/reference to the one passed in), and a copy/assignment uses the source's comparison object (`/13`).

## Operations (Table 90) and complexity

| Operation | Notes |
|---|---|
| construct from range / init list, with optional comparator | `N log N`, linear if the input is sorted by `value_comp()` |
| `key_comp()`, `value_comp()` | return the comparison objects |
| `emplace(args)` / `insert(t)` | unique: `pair<iterator, bool>`, inserts iff no equivalent key; equivalent: returns `iterator`. Logarithmic |
| `emplace_hint(p, args)`, `insert(p, t)` | inserts as close as possible to just before `p`; **amortized constant** if inserted immediately before `p` |
| `insert(i, j)`, `insert(il)` | range inserts, `N log(size+N)` |
| `insert(nh)`, `insert(p, nh)` | insert an extracted node (see below) |
| `extract(k)`, `extract(q)` | detach an element into a `node_type`; `log` / amortized constant |
| `merge(a2)` | transfer every element of `a2` whose key is not yet present (unique containers) into `a` by extracting and inserting nodes, using `a`'s comparator; needs equal allocators; pointers and references to transferred elements stay valid, and their iterators now behave as iterators into `a` |
| `erase(k)` / `erase(q)` / `erase(q1,q2)` / `clear()` | `erase(k)` is `log(size) + count`; the others as for sequences |
| `find`, `count`, `lower_bound`, `upper_bound`, `equal_range` | logarithmic (`count`: plus the count) |

**Heterogeneous lookup**: the member templates `find`, `count`, `lower_bound`, `upper_bound`, `equal_range` taking a key-like type `K` exist and take part in overload resolution only if `Compare::is_transparent` is a valid type (`/14`; the transparent function objects are in [[function-objects-and-invoke]]). Annex C notes that associative containers with a comparison object having a *non-const* call operator are no longer usable through const containers ([[cpp17-compatibility-differences]]).

## Validity of iterators and references (`/9-10`)

`insert` and `emplace` never invalidate anything; `erase` invalidates only the erased elements; `extract` invalidates only iterators to the removed element, and pointers/references to it stay valid — but **using them while the element sits in a `node_type` is undefined behavior**, and they become invalid again if the node is successfully reinserted. See [[iterator-invalidation]].

## Node handles (`[container.node]`)

A **node handle** owns a single element extracted from an associative or unordered container, and can transfer it to any container with *compatible nodes*: maps with maps/multimaps of the same `K, T, A`, sets with sets/multisets, and the same for the unordered ones (Table 89) — comparison/hash/equality may differ. Key properties:

- A non-empty node handle holds a copy of the allocator that was in the source container; an empty one holds none. Move assignment requires `!alloc_`, propagation on move assignment, or equal allocators; `swap` has the analogous requirement.
- It is movable and non-copyable; destroying a non-empty handle destroys the element and deallocates the node. Observers: `value()`; for maps `key()` (a **non-const** reference to the key — modifying it while the node is detached is permitted) and `mapped()`; `get_allocator()`, `explicit operator bool`, `empty()`.
- The class `node_handle` is exposition-only. If the program specializes `pair<const Key, T>` or `pair<Key, T>`, node handle behavior is undefined.
- **Insert return type** (unique-key `insert(node_type&&)`): a struct with `position` (iterator), `inserted` (bool) and `node` (the node handle): if the handle was empty, `inserted == false`, `position == end()`, `node` empty; on success `inserted == true`, `node` empty; on failure (equivalent key present) `inserted == false`, `node` regains the element, `position` points at the blocker.

## Exception safety (`[associative.reqmts.except]`)

`clear()` never throws; `erase(k)` throws only if `Compare` does; a throwing single-element `insert`/`emplace` has no effect; `swap` throws only if swapping `Compare` throws.

## Deduction guides (`/15`)

Do not participate if an `InputIterator` parameter is deduced to a non-iterator, an `Allocator` to a non-allocator, or `Compare` to something that qualifies as an allocator.

## Related

[[ordered-associative-containers]] · [[container-requirements]] · [[iterator-invalidation]] · [[unordered-container-requirements]] · [[pair-and-tuple]]
