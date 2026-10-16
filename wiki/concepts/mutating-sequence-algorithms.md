---
type: concept
title: "Mutating sequence algorithms (copy, move, transform, remove, unique, reverse, rotate, sample, shuffle)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Mutating sequence operations (`[alg.modifying.operations]`)

Parent: [[cpp17-lib-algorithms]]. Conventions: [[algorithm-requirements]]. Partitioning algorithms are grouped with sorting in [[sorting-and-set-algorithms]] (as in the standard, `[alg.partitions]`).

| Algorithm | Key requirements and semantics |
|---|---|
| `copy(first, last, result)` | `result` must **not** lie in `[first, last)` (use `copy_backward` when the output overlaps on the right). Exactly `last - first` assignments; returns the end of the output |
| `copy_n`, `copy_if` | `copy_if` is stable; ranges must not overlap |
| `copy_backward(first, last, result)` | copies from the back; `result` must not be in `(first, last]`; returns the beginning of the output |
| `move`, `move_backward` | as `copy` / `copy_backward` but `*(result+n) = std::move(*(first+n))` (not to be confused with the one-argument `std::move` of [[utility-move-forward-swap]]) |
| `swap_ranges`, `iter_swap` | the two ranges must not overlap; elements must be swappable ([[library-named-requirements]]) |
| `transform` | unary or binary op writes into `result` (which **may equal** `first` / `first1` / `first2`); `op` must not invalidate iterators or modify elements in the ranges; exactly one application per element |
| `replace`, `replace_if`, `replace_copy`, `replace_copy_if` | substitute `new_value`; the copying forms require non-overlapping ranges |
| `fill`, `fill_n`, `generate`, `generate_n` | assign a value or `gen()` through each iterator; `_n` forms do nothing for non-positive `n` and return `first` in that case |
| `remove`, `remove_if`, `remove_copy`, `remove_copy_if` | **stable**; the in-place versions *do not shrink the container*: they move retained elements forward and return the new logical end (the "erase–remove" idiom pairs this with a container `erase`); value type must be `MoveAssignable`. Exactly `last - first` predicate applications |
| `unique`, `unique_copy` | collapse consecutive groups of equivalent elements keeping the first; comparison must be an equivalence relation; exactly `(last - first) - 1` applications for non-empty ranges. `unique_copy` has extra value-type requirements depending on whether the input or output iterator is forward |
| `reverse`, `reverse_copy` | `reverse` uses `iter_swap`, exactly `(last - first)/2` swaps, needs `ValueSwappable` bidirectional iterators |
| `rotate`, `rotate_copy` | a **left rotate**: element at `first + i` moves to `first + (i + (last - middle)) % (last - first)`; `rotate` returns `first + (last - middle)`; needs `ValueSwappable` forward iterators and Move-constructible/assignable values; at most `last - first` swaps |
| `sample(first, last, out, n, g)` | selects `min(last - first, n)` elements uniformly at random without replacement; `g` is a uniform random bit generator ([[random-number-generation]]); O(`last - first`); stable only if the population iterator is a forward iterator; `out` must not be in `[first, last)`; if the population iterator is not forward, the sample iterator must be random access |
| `shuffle(first, last, g)` | uniformly random permutation using `g`; exactly `(last - first) - 1` swaps; random access, `ValueSwappable` |

The old `random_shuffle` name is a reserved "zombie" name in this draft ([[library-requirements-and-conformance]]); Annex C records its removal ([[cpp17-compatibility-differences]]).

## Related

[[nonmodifying-sequence-algorithms]] · [[sorting-and-set-algorithms]] · [[iterator-adaptors]] (insert iterators as outputs for `copy`) · [[execution-policies-and-parallel-algorithms]]
