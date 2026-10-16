---
type: concept
title: "C++17 clause 28: algorithms library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 28: Algorithms library (`[algorithms]`)

About 16,300 words; 69 labelled sections. Function templates over iterator ranges for non-modifying, mutating, sorting-related operations, plus the C `bsearch`/`qsort`. Parent: [[cpp17-lib-introduction]]. The numeric algorithms (`accumulate`, `reduce`, ...) are in clause 29 ([[numeric-operations]]).

## Section map

| Subclause | Label | Header | Content | Wiki page |
|---|---|---|---|---|
| 28.2 `<algorithm>` synopsis | `[algorithm.syn]` | `<algorithm>` | all declarations (~4,000 words, including `ExecutionPolicy` overloads) | — |
| 28.3 Algorithms requirements | `[algorithms.requirements]` | — | parameter naming, predicates, `Compare` | [[algorithm-requirements]] |
| 28.4 Parallel algorithms | `[algorithms.parallel]` | `<algorithm>`, `<execution>` | policies, constraints, exceptions, overload shape | [[execution-policies-and-parallel-algorithms]] |
| 28.5 Non-modifying sequence operations | `[alg.nonmodifying]` | `<algorithm>` | `all_of`, `for_each`, `find*`, `count`, `mismatch`, `equal`, `search*` | [[nonmodifying-sequence-algorithms]] |
| 28.6 Mutating sequence operations | `[alg.modifying.operations]` | `<algorithm>` | `copy`, `move`, `transform`, `remove`, `unique`, `reverse`, `rotate`, `sample`, `shuffle`, ... | [[mutating-sequence-algorithms]] |
| 28.7 Sorting and related operations | `[alg.sorting]` | `<algorithm>` | `sort`, binary search, partition, merge, set, heap, min/max, `clamp`, permutations | [[sorting-and-set-algorithms]] |
| 28.8 C library algorithms | `[alg.c.library]` | `<cstdlib>` | `bsearch`, `qsort` | [[sorting-and-set-algorithms]] |

## Key ideas

- Algorithms are **decoupled from containers** by iterator parameters whose names state the required category.
- Almost every algorithm has: a plain version, a predicate/comparator version, and (in this draft) an `ExecutionPolicy` version; `_copy` and `_if` suffixes distinguish variants.
- Complexity is part of the contract; a "stable" qualifier is defined once in `[algorithm.stable]` ([[library-requirements-and-conformance]]).
- Algorithms never change the size of a container: `remove`/`unique` return a new logical end and the caller erases ([[mutating-sequence-algorithms]]); inserters ([[iterator-adaptors]]) let copying algorithms grow a container.
- Names of algorithms new in this draft relative to older editions are not marked; the draft contains `for_each_n`, `sample`, `clamp`, `shuffle` (but not `random_shuffle`, which is a reserved zombie name).

## Related

[[cpp17-lib-iterators]] · [[cpp17-lib-containers]] · [[cpp17-lib-numerics]] · [[function-objects-and-invoke]]
