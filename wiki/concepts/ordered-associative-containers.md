---
type: concept
title: "std::map, multimap, set, multiset"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `map`, `multimap`, `set`, `multiset` (`[map]`, `[multimap]`, `[set]`, `[multiset]`)

The tree-ordered associative containers. Parent: [[cpp17-lib-containers]]. All semantics common to the four are in [[associative-container-requirements]] (ordering, complexity, node handles, invalidation); hash-based versions: [[unordered-containers]].

## What each one is

| Container | Keys | Value type | Header |
|---|---|---|---|
| `map<Key, T, Compare, Allocator>` | unique | `pair<const Key, T>` | `<map>` |
| `multimap<Key, T, Compare, Allocator>` | equivalent keys allowed | `pair<const Key, T>` | `<map>` |
| `set<Key, Compare, Allocator>` | unique | `Key` | `<set>` |
| `multiset<Key, Compare, Allocator>` | equivalent keys allowed | `Key` | `<set>` |

Each satisfies the container, reversible, associative and allocator-aware requirements; `map` and `set` support the unique-key (`a_uniq`) operations, `multimap` and `multiset` the equivalent-key (`a_eq`) ones. Iterators are bidirectional. Constructors take a comparison object and an allocator (range construction is linear for pre-sorted input, `N log N` otherwise).

## `map`-specific operations (`[map.access]`, `[map.modifiers]`)

- **`operator[](key)`** is defined as `try_emplace(key).first->second`: it inserts a value-initialized mapped value if the key is absent, and therefore needs `mapped_type` to be default-constructible; the rvalue-key overload uses `move(key)`. **`at(key)`** returns a reference or throws `out_of_range`; it never inserts. (`multimap` has neither.)
- **`try_emplace(k, args...)` / `try_emplace(hint, k, args...)`**: if an equivalent key exists, *nothing happens* (in particular `args` are not consumed); otherwise a `value_type` is constructed piecewise as `(k, args...)`. Returns `pair<iterator, bool>` (non-hint form). Rvalue-key overloads move the key only on actual insertion.
- **`insert_or_assign(k, obj)`**: assigns `obj` to the existing mapped value, or inserts `(k, obj)`; returns `pair<iterator, bool>`, `bool` true if inserted. Requires `mapped_type` assignable from `M&&`.
- `insert(P&&)` (and hinted) forwards to `emplace`, taking part in overload resolution only if `value_type` is constructible from `P&&`.
- Node-handle `extract`/`insert`/`merge` (also on the `multi` versions and sets) transfer elements without copying or moving them; keys of a detached map node can be modified ([[associative-container-requirements]]).

## Common reminders

- Equivalence uses the comparator, not `operator==` on keys, and `comp(k1, k2)` must always return the same value for any two keys in the container.
- `multimap`/`multiset` keep equivalent elements in insertion order within the equal range; `equal_range`, `lower_bound`, `upper_bound` find that range. Transparent comparators (`is_transparent`) enable heterogeneous lookup ([[function-objects-and-invoke]]).
- Deduction guides deduce `Key`/`T` from iterator ranges (via the exposition-only `iter_key_t`/`iter_val_t`) and from `initializer_list<pair<const Key, T>>` (excluded when an argument that must be an iterator, comparator or allocator has the wrong kind of type).
- `swap` and the comparison operators (`==`, `<`, ...) are provided; `pmr::map` and friends are aliases using [[memory-resources-pmr]].

## Related

[[associative-container-requirements]] · [[unordered-containers]] · [[iterator-invalidation]] · [[pair-and-tuple]] · [[sorting-and-set-algorithms]] (the set algorithms work on any sorted ranges)
