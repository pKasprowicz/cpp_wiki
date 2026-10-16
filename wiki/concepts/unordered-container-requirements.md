---
type: concept
title: "Unordered associative container requirements (hashing, buckets, rehash)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Unordered associative containers (`[unord.req]`)

Requirements for `unordered_set`, `unordered_multiset`, `unordered_map`, `unordered_multimap`. Parent: [[cpp17-lib-containers]]. Classes: [[unordered-containers]]. Ordered counterpart: [[associative-container-requirements]].

## Model

- Parameterized on `Key`, a `Hash` function object ([[library-named-requirements]], default `std::hash`, see [[function-objects-and-invoke]]) and a `Pred` equivalence relation. If `k1` and `k2` are equivalent (`pred` true) the hash **must** be equal; `pred(k1, k2)` and `hash(k)` must be stable for the life of the container.
- Worst-case complexity of most operations is **linear**, the average case much faster (average O(1) for find/insert/erase of a single element).
- Unique keys (`unordered_set`/`map`) vs. equivalent keys (`..._multi...`). In the multi containers elements with equivalent keys are **adjacent** in iteration order, and relative order of equivalent elements is preserved by rehashing and erase.
- `iterator`/`const_iterator` are at least **forward iterators**; for set-like containers both are constant iterators. `local_iterator`/`const_local_iterator` iterate **within one bucket only**.
- Elements live in **buckets**; keys with the same hash code share a bucket. The bucket count grows automatically to keep the load factor under `max_load_factor()` (default 1.0 as constructed by the standard classes).
- `a == b` is **not** element-wise sequence comparison: two unordered containers are equal if their sizes match and, for every equivalent-key group in `a`, `b` has a group that is a permutation of it (`is_permutation`). Undefined unless `Hash` and `Pred` behave the same for both containers and key equality is a refinement of the partition into equivalent-key groups (`/12`).

## Interface (Table 91)

- Types: `hasher`, `key_equal`, `local_iterator`, `const_local_iterator`, `node_type`, plus `key_type`/`mapped_type`/`value_type` as for maps and sets.
- Constructors take (`n`, `hf`, `eq`) in that order, with progressive defaults; `n` is the minimum bucket count. Range and initializer-list constructors average O(N), worst O(N²). Copy construction/assignment copy the hash, predicate and max load factor.
- `hash_function()`, `key_eq()`; `emplace`, `emplace_hint` (the hint may be **ignored**), `insert` (single, range, list, node handle), `extract`, `merge`, `erase`, `clear`, `find`, `count`, `equal_range` — all with average O(1)-ish and worst O(size) complexity. Unlike the ordered containers there is **no `lower_bound`/`upper_bound`** and **no heterogeneous lookup** in this draft.
- **Bucket interface**: `bucket_count()`, `max_bucket_count()`, `bucket(k)`, `bucket_size(n)`, `begin(n)`/`end(n)`/`cbegin(n)`/`cend(n)`.
- **Load factor**: `load_factor()`, `max_load_factor()`, `max_load_factor(z)` (hint; `z` positive), `rehash(n)` (postcondition: `bucket_count() >= n` and `>= size() / max_load_factor()`), `reserve(n)` (= `rehash(ceil(n / max_load_factor()))`); rehash cost average linear, worst quadratic.

## Validity (`/9`, `/14-16`)

- **Rehashing invalidates iterators and changes ordering, but not pointers or references to elements.**
- `insert`/`emplace` never affect references, but **may invalidate all iterators**; they leave iterators valid if `(N + n) <= z * B` (no rehash needed).
- `erase` invalidates only iterators/references to erased elements and preserves the relative order of others.
- `extract`: only iterators to the removed element are invalidated; pointers and references stay valid but must not be used while the element is in a `node_type`. `merge` invalidates iterators of transferred elements **and all iterators of the target**; iterators to elements remaining in the source stay valid. See [[iterator-invalidation]].

## Exception safety (`[unord.req.except]`)

`clear()` never throws; `erase(k)` throws only through `Hash`/`Pred`; a throwing single-element `insert`/`emplace` has no effect (unless the hash function itself throws); `swap` throws only through swapping `Hash`/`Pred`; a throwing `rehash` has no effect unless the hash/comparison function throws.

## Deduction guides (`/17`)

Excluded if an input-iterator parameter is not an iterator, an `Allocator` parameter is not an allocator, `Hash` is an integral type or an allocator, or `Pred` is an allocator.

## Related

[[unordered-containers]] · [[container-requirements]] · [[associative-container-requirements]] (node handles shared) · [[function-objects-and-invoke]]
