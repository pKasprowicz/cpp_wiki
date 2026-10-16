---
type: concept
title: "C++17 clause 29: numerics library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 29: Numerics library (`[numerics]`)

About 28,000 words; 154 labelled sections (most of them the distribution classes and special functions). Components for "seminumerical" operations. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header | Content | Wiki page |
|---|---|---|---|---|
| 29.2 Definitions | `[numerics.defns]` | — | `GENERALIZED_SUM`, `GENERALIZED_NONCOMMUTATIVE_SUM` | [[numeric-operations]] |
| 29.3 Numeric type requirements | `[numeric.requirements]` | — | rules for element types of `complex` and `valarray` | [[complex-numbers]] |
| 29.4 Floating-point environment | `[cfenv]` | `<cfenv>` | C fenv; per-thread | [[math-functions-and-fenv]] |
| 29.5 Complex numbers | `[complex.numbers]` | `<complex>` | `complex<T>` and functions | [[complex-numbers]] |
| 29.6 Random number generation | `[rand]` | `<random>` | engines, adaptors, distributions, `random_device`, `seed_seq` | [[random-number-generation]] |
| 29.7 Numeric arrays | `[numarray]` | `<valarray>` | `valarray`, `slice`, `gslice`, subset arrays | [[valarray]] |
| 29.8 Generalized numeric operations | `[numeric.ops]` | `<numeric>` | `accumulate`, `reduce`, scans, `iota`, `gcd`, `lcm` | [[numeric-operations]] |
| 29.9 Mathematical functions | `[c.math]` | `<cmath>`, `<cstdlib>` | C math plus 3-argument `hypot` and special functions | [[math-functions-and-fenv]] |

## Related

[[numeric-limits]] (in clause 21) · [[cpp17-lib-algorithms]] · [[execution-policies-and-parallel-algorithms]] · [[cpp17-lib-introduction]]
