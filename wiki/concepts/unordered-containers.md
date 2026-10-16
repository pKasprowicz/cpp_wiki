---
type: concept
title: "std::unordered_map, unordered_multimap, unordered_set, unordered_multiset"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `unordered_map`, `unordered_multimap`, `unordered_set`, `unordered_multiset` (`[unord]`)

The hash-table containers. Parent: [[cpp17-lib-containers]]. Common contract (hashing, buckets, rehash, invalidation, equality semantics): [[unordered-container-requirements]]. Ordered versions: [[ordered-associative-containers]].

## The four classes

| Container | Keys | Value type | Header |
|---|---|---|---|
| `unordered_map<Key, T, Hash, Pred, Allocator>` | unique | `pair<const Key, T>` | `<unordered_map>` |
| `unordered_multimap<...>` | equivalent | `pair<const Key, T>` | `<unordered_map>` |
| `unordered_set<Key, Hash, Pred, Allocator>` | unique | `Key` | `<unordered_set>` |
| `unordered_multiset<...>` | equivalent | `Key` | `<unordered_set>` |

Defaults: `Hash = std::hash<Key>`, `Pred = std::equal_to<Key>`, `Allocator = std::allocator<...>` ([[function-objects-and-invoke]], [[allocators]]). Iterators are at least forward iterators; elements have **no specified order**, but equivalent keys are adjacent. Each class meets the container, unordered-associative and allocator-aware requirements. A `size_type` parameter in a deduction guide means the deduced container's `size_type`.

## Construction

All constructors accept (`n` buckets, `hf` hasher, `eq` equality predicate, allocator) with trailing defaults, range and initializer-list forms included. The default-constructed bucket count is implementation-defined and **`max_load_factor()` is 1.0 initially**. The number of buckets requested is a lower bound.

## `unordered_map` specifics (`[unord.map.elem]`, `[unord.map.modifiers]`)

Same operations as `map`: `operator[]` is `try_emplace(key).first->second` (inserts a default-constructed mapped value), `at()` throws `out_of_range`, `try_emplace` (no consumption of arguments when the key exists), `insert_or_assign`, `insert(P&&)`/`emplace` forwarding. `unordered_multimap` has none of `operator[]`, `at`, `try_emplace`, `insert_or_assign`. Node-handle `extract`/`insert`/`merge` are available on all four.

## Notes

- No ordered operations (`lower_bound`, `upper_bound`) and no heterogeneous lookup in this draft; instead `bucket*`, `load_factor`, `rehash`, `reserve`.
- Equality is group-wise permutation equality, not sequence equality, and requires matching `Hash`/`Pred` behavior ([[unordered-container-requirements]]).
- For iterator validity under insertion, rehash and merge see [[iterator-invalidation]]; references and pointers survive rehashing.
- `pmr::unordered_map` etc. use [[memory-resources-pmr]].

## Related

[[unordered-container-requirements]] · [[ordered-associative-containers]] · [[associative-container-requirements]] (node handles) · [[library-named-requirements]] (Hash)
