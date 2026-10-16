---
type: concept
title: "Algorithm requirements: iterator parameter names, predicates, Compare, copy/_if suffixes"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Algorithm requirements (`[algorithms.requirements]`, `[alg.sorting]` intro)

Conventions that apply to every algorithm in `<algorithm>` (and `<numeric>`, `<memory>`). Parent: [[cpp17-lib-algorithms]]. Iterator categories: [[iterator-categories-and-requirements]]. Parallel overloads: [[execution-policies-and-parallel-algorithms]].

## Parameter names are the requirements (`/3-4`)

A template parameter named `InputIterator[1|2]`, `OutputIterator[1|2]`, `ForwardIterator[1|2]`, `BidirectionalIterator[1|2]` or `RandomAccessIterator[1|2]` requires the argument to satisfy exactly that iterator category. If an algorithm's Effects modify an element through an iterator, that argument must also be a **mutable** iterator. Many mutating algorithms additionally require `ValueSwappable`, `MoveConstructible`, `MoveAssignable` of the value type — see the individual pages.

## Data races, algebra of names

- For race analysis, algorithms must not modify objects referenced through iterator arguments unless the specification requires it (`/2`).
- **Suffixes**: `_copy` = copying version of an in-place algorithm; `_if` (after `_copy`) = takes a predicate (`/5`).
- `a + n` and `b - a` in descriptions are shorthand for repeated `++`/`--` even for iterators that do not provide those operators (`/10`).

## Predicates and comparison functions

- **Predicate**: when applied as `pred(*first)` (contextually converted to `bool`) it must work; it **shall not apply any non-constant function through the dereferenced iterator** (`/6`).
- **BinaryPredicate**: `binary_pred(*first1, *first2)` or, when a value `T` is part of the signature, `binary_pred(*first1, value)` — the first argument is always of the first iterator's value type; may not apply non-constant functions through the iterators (`/7`).
- Equality in descriptions such as `*first == value` must evaluate to a value usable as `true`/`false` (`/9`).
- **Compare** (`[alg.sorting]`): a function object whose call, contextually converted to `bool`, says whether the first argument is less than the second. Every sorting-related algorithm has two forms, using `operator<` or a `Compare`. Except for the binary-search family, `comp` **must induce a strict weak ordering**: irreflexive (`!comp(x, x)`), transitive (`comp(a,b) && comp(b,c)` implies `comp(a,c)`), and transitivity of the induced equivalence `equiv(a,b) = !comp(a,b) && !comp(b,a)`. A sequence is *sorted* with respect to `comp` if `comp(*(i+n), *i)` is false for all valid `i`, `n`; *partitioned* with respect to `f` if `f` is true for exactly a prefix. "Equivalent" in stability descriptions means this induced equivalence, not `==`.
- Stability definitions: [[library-requirements-and-conformance]] (`[algorithm.stable]`).

## Complexity vocabulary

Statements like "exactly `last - first` applications of the predicate" or "at most `N log N` comparisons" are upper bounds on operations on elements; `ExecutionPolicy` overloads relax "at most/exactly expr" to O(expr) unless assignments/swaps are specified ([[execution-policies-and-parallel-algorithms]]).

## Related

[[nonmodifying-sequence-algorithms]] · [[mutating-sequence-algorithms]] · [[sorting-and-set-algorithms]] · [[numeric-operations]] · [[library-named-requirements]] · [[function-objects-and-invoke]]
