---
title: "Index shard: concepts — containers, iterators, algorithms (clauses 26-28)"
---
# Index shard: concepts — containers, iterators, algorithms (clauses 26-28)

One line per page. Directory of shards: `wiki/index.md`. Related requirements pages in the foundations shard: [[allocators]], [[library-named-requirements]].

## Clause 26 — containers

- [[cpp17-lib-containers]] — Clause 26 overview and section map.
- [[container-requirements]] — General container, reversible, allocator-aware requirements; insertable vocabulary; data-race guarantees.
- [[sequence-container-requirements]] — Table 87-88: construction, insert/erase, optional front/back/push/pop operations.
- [[associative-container-requirements]] — Ordered containers: strict weak ordering, complexity, heterogeneous lookup, node handles, insert return type.
- [[unordered-container-requirements]] — Hash containers: buckets, load factor, rehash, equality semantics, validity rules.
- [[iterator-invalidation]] — Cross-cutting table of iterator/pointer/reference invalidation for every container.
- [[array-and-vector]] — `array` (aggregate, zero-size) and `vector` (reserve guarantee, exception safety, `vector<bool>`).
- [[deque-and-lists]] — `deque`, `list` (splice, merge, sort) and `forward_list` (`*_after` interface).
- [[ordered-associative-containers]] — `map`, `multimap`, `set`, `multiset`: `try_emplace`, `insert_or_assign`, `operator[]`.
- [[unordered-containers]] — `unordered_map`/`set` families: constructors, `operator[]`, `try_emplace`, node handles.
- [[container-adaptors]] — `stack`, `queue`, `priority_queue` and their required container operations.

## Clause 27 — iterators

- [[cpp17-lib-iterators]] — Clause 27 overview.
- [[iterator-categories-and-requirements]] — Five categories, contiguity, ranges, singular values, `iterator_traits`, tags, `advance`/`distance`.
- [[iterator-adaptors]] — Reverse, insert, move iterators; stream and streambuf iterators; `begin`/`end`/`size`/`data`.

## Clause 28 — algorithms

- [[cpp17-lib-algorithms]] — Clause 28 overview and section map.
- [[algorithm-requirements]] — Iterator parameter names as requirements, predicates, `Compare` and strict weak ordering.
- [[nonmodifying-sequence-algorithms]] — `all_of` ... `search` with complexity table.
- [[mutating-sequence-algorithms]] — `copy`, `transform`, `remove`/`unique`, `rotate`, `sample`, `shuffle`.
- [[sorting-and-set-algorithms]] — Sorting, binary search, partition, merge, set, heap, min/max, `clamp`, permutations.
