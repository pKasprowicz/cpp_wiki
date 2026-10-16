---
type: concept
title: "Generalized numeric operations (<numeric>): accumulate, reduce, scans, inner_product, iota, gcd, lcm"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Generalized numeric operations (`[numeric.ops]`)

Parent: [[cpp17-lib-numerics]]. The algorithm conventions in [[algorithm-requirements]] apply; parallel overloads follow [[execution-policies-and-parallel-algorithms]].

## Two summation models (`[numerics.defns]`)

- `GENERALIZED_NONCOMMUTATIVE_SUM(op, a1..aN)`: any way of bracketing the operands **in the given order** (associativity may be exploited, commutativity may not).
- `GENERALIZED_SUM(op, a1..aN)`: the same, over **any permutation** of the operands (both associativity and commutativity may be exploited).

Algorithms defined with the generalized sums (`reduce`, `transform_reduce`, the scans) therefore give the same result as the sequential versions only when the operation is associative (and, for `reduce`/`transform_reduce`, commutative) — otherwise the result is non-deterministic. The classic sequential ones (`accumulate`, `inner_product`, `partial_sum`, `adjacent_difference`) are specified as strict left-to-right loops.

## The algorithms

| Algorithm | Behavior |
|---|---|
| `accumulate(first, last, init[, op])` | left fold: `acc = acc + *i` or `acc = op(acc, *i)`; `T` CopyConstructible/CopyAssignable; `op` must not modify elements or invalidate iterators |
| `reduce([policy,] first, last[, init[, op]])` | `GENERALIZED_SUM(op, init, *i...)`; `init` defaults to `typename iterator_traits<It>::value_type{}`; `op(init, *first)`, `op(*first, init)`, `op(init, init)`, `op(*first, *first)` all convertible to `T`; `O(last - first)` applications |
| `inner_product(first1, last1, first2, init[, op1, op2])` | `acc = op1(acc, op2(*i1, *i2))` (defaults `+`, `*`), in order |
| `transform_reduce` | `reduce` after applying a binary (two ranges) or unary operation to the elements |
| `partial_sum(first, last, result[, op])` | running accumulation, sequential; exactly `(last - first) - 1` applications; `result` may equal `first` |
| `exclusive_scan(first, last, result, init[, op])` | `result[K]` = sum of `init` and the first `K` inputs (so `result[0] == init`); `result` may equal `first`; generalized (non-commutative) sum |
| `inclusive_scan(first, last, result[, op[, init]])` | `result[K]` includes element `K`; if `init` is given it is the first operand; `O(last - first)` applications |
| `transform_exclusive_scan`, `transform_inclusive_scan` | scans of `unary_op(*i)` values |
| `adjacent_difference(first, last, result[, op])` | `result[0] = *first`; then `*(first+d) - *(first+d-1)` or `op(val, acc)`; the sequential form uses an accumulator of the input value type, so `result` may equal `first`; the policy form needs non-overlapping ranges |
| `iota(first, last, value)` | assigns `value`, `++value`, ... ; requires `++val` well-formed |
| `gcd(m, n)`, `lcm(m, n)` | on integer types only (non-integer or `bool` arguments make the program ill-formed); results of type `common_type_t<M, N>`; `gcd(0, 0) == 0`; `lcm` is zero if either argument is zero; throw nothing; `|m|`, `|n|` and for `lcm` the result must be representable |

Requirements for the parallelizable forms (`reduce`, scans): `T` is `MoveConstructible`; the operation must not invalidate iterators/subranges nor modify the input (or output) ranges.

## Related

[[cpp17-lib-numerics]] · [[algorithm-requirements]] · [[execution-policies-and-parallel-algorithms]] · [[function-objects-and-invoke]] (`plus`, `multiplies`)
