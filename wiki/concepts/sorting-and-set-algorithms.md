---
type: concept
title: "Sorting, binary search, partition, merge, set, heap, min/max and permutation algorithms"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Sorting and related operations (`[alg.sorting]`)

Parent: [[cpp17-lib-algorithms]]. The ordering conventions (strict weak ordering, `Compare`) are on [[algorithm-requirements]].

## Sorting (`[alg.sort]`, `[alg.nth.element]`)

| Algorithm | Notes |
|---|---|
| `sort` | `O(N log N)` comparisons; random-access, `ValueSwappable`, Move-constructible and -assignable; **not stable** |
| `stable_sort` | at most `N log² N` comparisons, `N log N` with enough extra memory; stable |
| `partial_sort(first, middle, last)` | the `middle - first` smallest elements sorted into `[first, middle)`, the rest unspecified; about `(last-first) log(middle-first)` comparisons |
| `partial_sort_copy` | like `partial_sort` into a separate output range of the smaller of the two lengths |
| `is_sorted`, `is_sorted_until` | `is_sorted_until` returns the end of the longest sorted prefix; linear |
| `nth_element(first, nth, last)` | element at `nth` is the one a full sort would put there; everything before it is not greater than anything from `nth` on; linear on average |

## Binary search (`[alg.binary.search]`)

`lower_bound`, `upper_bound`, `equal_range`, `binary_search` require the range to be **partitioned** with respect to `e < value` (or `comp(e, value)`) and the analogous expressions (`!(value < e)`); for `equal_range`/`binary_search` also that `e < value` implies `!(value < e)`. They work with non-random-access iterators, minimizing comparisons (though not iterator movement); at most `log2(N) + O(1)` comparisons (`2 log2 N + O(1)` for `equal_range`). Notably the comparison need not be a full strict weak ordering for these ([[algorithm-requirements]]).

## Partitions (`[alg.partitions]`)

`is_partitioned`; `partition` (forward iterators, `ValueSwappable`, exactly `N` predicate applications, at most `N/2` swaps for bidirectional, `N` otherwise; **not stable**); `stable_partition` (bidirectional, at most `N log N` swaps or `O(N)` with extra memory; preserves relative order in both groups); `partition_copy` (writes satisfying elements to `out_true`, others to `out_false`, inputs must not overlap the outputs); `partition_point` (binary search for the boundary of a partitioned range, `O(log N)` predicate applications).

## Merge, set operations, heaps

- `merge(first1, last1, first2, last2, result)`: both inputs sorted, output must not overlap either; at most `N - 1` comparisons; **stable** (elements of the first range precede equivalent ones from the second). `inplace_merge(first, middle, last)`: exactly `N - 1` comparisons with enough memory, else `O(N log N)`; stable; `ValueSwappable` bidirectional iterators.
- `includes`, `set_union`, `set_intersection`, `set_difference`, `set_symmetric_difference`: work on sorted ranges (also multisets); output range may not overlap the inputs; at most `2(N1 + N2) - 1` comparisons. Multiplicities: for `m` and `n` equivalent elements, union keeps `max(m, n)` (all `m` from range 1 first, then the extras from range 2), intersection keeps `min(m, n)` from range 1, difference keeps the last `max(m - n, 0)` of range 1, symmetric difference keeps `|m - n|`.
- **Heap** operations on random-access ranges: a heap satisfies `comp(a[(i-1)/2], a[i])` false for all `0 < i < N`. `push_heap` (new element at `last - 1`; at most `log N` comparisons), `pop_heap` (swaps `first` with `last - 1` and re-heapifies `[first, last-1)`; at most `2 log N`), `make_heap` (at most `3N`), `sort_heap` (at most `N log N`), `is_heap`, `is_heap_until`. `priority_queue` is built on these ([[container-adaptors]]).

## Minimum, maximum, clamp, lexicographic compare, permutations

- `min`, `max` (two values or an `initializer_list`; **return the first/leftmost argument when equivalent**), `minmax` (pair of references; `(a, b)` when equivalent), `min_element`, `max_element` (first minimal/maximal element), `minmax_element` (first minimum and **last** maximum; at most `⌊3(N-1)/2⌋` comparisons).
- `clamp(v, lo, hi)`: `lo` if `v < lo`, `hi` if `hi < v`, else `v`; requires `lo <= hi`; returns a reference; at most two comparisons.
- `lexicographical_compare`: shorter prefix is less; at most `2 min(len1, len2)` comparisons.
- `next_permutation`, `prev_permutation`: permute to the next/previous lexicographic arrangement; return `false` and wrap to the smallest/largest arrangement when none exists; bidirectional `ValueSwappable` iterators; at most `(last - first)/2` swaps.

## C library algorithms (`[alg.c.library]`)

`bsearch` and `qsort` (in `<cstdlib>`) have C semantics; behavior is undefined unless the array elements are of trivial type; exceptions thrown by `compar` propagate.

## Related

[[mutating-sequence-algorithms]] · [[nonmodifying-sequence-algorithms]] · [[algorithm-requirements]] · [[ordered-associative-containers]] · [[random-number-generation]] · [[locale-class-and-facets]] (`locale` as a string comparator)
