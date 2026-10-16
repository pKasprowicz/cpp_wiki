---
type: concept
title: "C++17 clause 26: containers library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 26: Containers library (`[containers]`)

About 35,000 words; 129 labelled sections. Components for storing collections: the **requirements** the containers share, four sequence containers plus `array`, ordered and unordered associative containers, and container adaptors. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header(s) | Content | Wiki page |
|---|---|---|---|---|
| 26.2.1-26.2.2 General container requirements, data races | `[container.requirements.general]` `[container.requirements.dataraces]` | — | Table 83-86, insertable vocabulary, allocator-aware rules, guarantees | [[container-requirements]] |
| 26.2.3 Sequence containers | `[sequence.reqmts]` | — | Table 87-88 | [[sequence-container-requirements]] |
| 26.2.4-26.2.5 Node handles, insert return type | `[container.node]` `[container.insert.return]` | — | `node_handle`, `insert_return_type` | [[associative-container-requirements]] |
| 26.2.6 Associative containers | `[associative.reqmts]` | — | Table 90, heterogeneous lookup | [[associative-container-requirements]] |
| 26.2.7 Unordered associative | `[unord.req]` | — | Table 91, buckets, rehash | [[unordered-container-requirements]] |
| 26.3.7 `array` | `[array]` | `<array>` | fixed-size aggregate container | [[array-and-vector]] |
| 26.3.8 `deque` | `[deque]` | `<deque>` | double-ended sequence | [[deque-and-lists]] |
| 26.3.9 `forward_list` | `[forwardlist]` | `<forward_list>` | singly-linked list | [[deque-and-lists]] |
| 26.3.10 `list` | `[list]` | `<list>` | doubly-linked list | [[deque-and-lists]] |
| 26.3.11-26.3.12 `vector`, `vector<bool>` | `[vector]` `[vector.bool]` | `<vector>` | contiguous dynamic array | [[array-and-vector]] |
| 26.4 Associative containers | `[associative]` | `<map>`, `<set>` | `map`, `multimap`, `set`, `multiset` | [[ordered-associative-containers]] |
| 26.5 Unordered associative | `[unord]` | `<unordered_map>`, `<unordered_set>` | hash containers | [[unordered-containers]] |
| 26.6 Container adaptors | `[container.adaptors]` | `<queue>`, `<stack>` | `queue`, `priority_queue`, `stack` | [[container-adaptors]] |
| (cross-cutting) | — | — | invalidation of iterators/references across all of the above | [[iterator-invalidation]] |

## Core ideas

- **Complexity is stated only in operations on the contained objects.** A container hides how it organizes memory but constrains how many element copies, moves and comparisons an operation performs.
- **Requirements, then specifics.** Each class says which requirement tables it satisfies, then documents only the deviations ("exceptions are `push_front`...", "`forward_list` has no `size()`", "default-constructed `array` is not empty").
- **Allocator-aware everywhere except `array`** ([[allocators]]); `pmr::` aliases for each container live in its header ([[memory-resources-pmr]]).
- **Exception safety floor**: single-element insert has no effect if it throws; `erase`/`clear`/`pop_*`/`swap` never throw (unless a comparator or hasher does).
- **Insertion vocabulary** (`EmplaceConstructible`, `MoveInsertable`, ...) replaces plain "copyable" so allocator-constructed elements are covered.
- Containers interact with algorithms and iterators only through the iterator requirements ([[iterator-categories-and-requirements]], [[cpp17-lib-algorithms]]); `list`/`forward_list` supply members (`sort`, `merge`, `unique`, `remove`, `reverse`) that replace algorithms requiring random access.
- `basic_string` meets most sequence-container and allocator-aware requirements as well ([[basic-string]]).

## Related

[[cpp17-lib-iterators]] · [[cpp17-lib-algorithms]] · [[cpp17-lib-utilities]] · [[library-named-requirements]]
