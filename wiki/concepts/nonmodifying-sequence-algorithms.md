---
type: concept
title: "Non-modifying sequence algorithms (all_of ... search, for_each, find, count, equal, mismatch)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Non-modifying sequence operations (`[alg.nonmodifying]`)

Parent: [[cpp17-lib-algorithms]]. Conventions: [[algorithm-requirements]].

| Algorithm | Result | Complexity (non-parallel) |
|---|---|---|
| `all_of`, `any_of`, `none_of(first, last, pred)` | `all_of` true for an empty range; `any_of` false for empty; `none_of` true for empty | at most `last - first` predicate applications |
| `for_each(first, last, f)` | applies `f` to every element in order; **returns `f`** (so state can be recovered); `f` must be `MoveConstructible`; any return value is ignored | exactly `last - first` applications |
| `for_each_n(first, n, f)` | same for `[first, first+n)`; `n >= 0`; **returns `first + n`** | `n` applications |
| `find`, `find_if`, `find_if_not` | first iterator satisfying `*i == value` / `pred(*i)` / `!pred(*i)`, else `last` | at most `last - first` |
| `find_end(first1, last1, first2, last2[, pred])` | **last** occurrence of the second sequence in the first; `last1` if the pattern is empty or not found | at most `(last2-first2) * (last1-first1-(last2-first2)+1)` |
| `find_first_of(first1, last1, first2, last2[, pred])` | first element of range 1 equal to *any* element of range 2; `last1` if range 2 is empty/no match | at most `(last1-first1) * (last2-first2)` |
| `adjacent_find` | first `i` with `*i == *(i+1)` (or `pred`) | exactly `min((i - first) + 1, (last - first) - 1)` |
| `count`, `count_if` | number of matching elements (`difference_type`) | exactly `last - first` |
| `mismatch` | pair of iterators at the first position where the ranges differ (or the shorter length); the 3-argument form assumes the second range is at least as long | at most `min(len1, len2)` |
| `equal` | `false` immediately if lengths differ (for the four-iterator forms, with no predicate calls for random-access iterators); otherwise element-wise equality | at most `min(len1, len2)` |
| `is_permutation` | true if some permutation of range 2 equals range 1; both iterators must have the **same value type**; the comparison must be an equivalence relation | no predicate calls if random-access and lengths differ; otherwise exactly `N` if the ranges are already element-wise equal, else at worst O(N²) |
| `search(first1, last1, first2, last2[, pred])` | **first** occurrence of the pattern; `first1` for an empty pattern, `last1` if not found | at most `(last1-first1) * (last2-first2)` |
| `search_n(first, last, count, value[, pred])` | first run of `count` equal values | at most `last - first` |
| `search(first, last, searcher)` | `searcher(first, last).first`; the searcher need not be CopyConstructible | per searcher |

Notes:

- The two-range forms with only `first2` (no `last2`) assume the second range has `last1 - first1` elements.
- `for_each` and `for_each_n` with an `ExecutionPolicy` do **not** get the freedom to copy elements that `[algorithms.parallel.exec]` gives other algorithms.
- Searchers (Boyer-Moore, Boyer-Moore-Horspool, default): [[function-objects-and-invoke]].
- `find_end`/`search` interpret "equal" with `==` or a binary predicate in the pattern-element-second order `pred(*(i+n), *(first2+n))`.

## Related

[[mutating-sequence-algorithms]] · [[sorting-and-set-algorithms]] · [[algorithm-requirements]] · [[execution-policies-and-parallel-algorithms]]
