---
type: concept
title: "Random number generation (<random>)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Random number generation (`[rand]`)

Parent: [[cpp17-lib-numerics]]. Consumers: `shuffle` and `sample` ([[mutating-sequence-algorithms]]).

## The component model (`[rand.req]`)

| Concept | What it is |
|---|---|
| **Uniform random bit generator (URBG)** | function object `g()` returning unsigned integers in `[G::min(), G::max()]` (with `min() < max()`), ideally equiprobable; `result_type` unsigned |
| **Random number engine** | a URBG with a well-defined state: default/copy/seed construction (`E(s)` from an integer, `E(q)` from a seed sequence), `seed()` overloads, `discard(z)` (advance by `z` calls), `==`/`!=` (equal iff they would produce the same future sequence), and textual `<<`/`>>` of the state; the spec fixes the state size, the transition algorithm TA and the generation algorithm GA |
| **Engine adaptor** | an engine that post-processes another ("base") engine's output; `base()` returns a const reference to it |
| **Seed sequence** | consumes integers and produces any number of 32-bit-range values via `generate(rb, re)`; `result_type` an unsigned integer of at least 32 bits |
| **Distribution** | function object mapping engine output to values with a given probability function: `result_type` (arithmetic), `param_type`, `reset()`, `param()`, `operator()(g)` and `operator()(g, p)` (amortized constant number of calls to `g`), `min()`/`max()`, equality, streaming |

Template parameters with fixed names carry requirements and **violating them is undefined behavior**: `Sseq` (a seed sequence, cv-unqualified), `URBG`, `Engine`, `RealType` (only `float`, `double`, `long double`), `IntType` (the signed/unsigned short..long long), `UIntType` (the unsigned ones) (`[rand.req.genl]`). Seeding templates `Sseq&` constructors/`seed` do not take part in overload resolution for types that are not seed sequences (at minimum, anything implicitly convertible to `result_type` is excluded).

## Engines, adaptors, predefined types

- **Engines** (`[rand.eng]`): `linear_congruential_engine` (state `x`, `TA(x) = (a·x + c) mod m`; `m == 0` means 2^word-size), `mersenne_twister_engine`, `subtract_with_carry_engine`. Required parameter relationships must hold or the program is ill-formed.
- **Adaptors** (`[rand.adapt]`): `discard_block_engine` (use `r` of every `p` values), `independent_bits_engine` (synthesizes `w`-bit values from a base engine), `shuffle_order_engine` (delivers the base engine's output in a different order).
- **Predefined** (`[rand.predef]`): `minstd_rand0`, `minstd_rand`, `mt19937`, `mt19937_64`, `ranlux24_base`, `ranlux48_base`, `ranlux24`, `ranlux48`, `knuth_b`, `default_random_engine`. Required behavior pins the **10000th output** of each default-constructed engine (e.g. `mt19937` → 4123659995, `minstd_rand` → 399268537) so results are portable.
- **`random_device`**: nondeterministic URBG; may fall back to an engine if the platform has no entropy source, in which case `entropy()` returns 0.0. Construction and `operator()` may throw an implementation-defined `exception`-derived type.
- **`seed_seq`**: default seed sequence built from integers; `generate` fills a range with a fixed mixing algorithm modulo 2^32.
- **`generate_canonical<RealType, bits>(g)`**: maps `g` to a value in `[0, 1)` using exactly `k = max(1, ⌈b / log2 R⌉)` calls where `R = g.max() - g.min() + 1`.

## Distributions (`[rand.dist]`)

Each class template satisfies the distribution requirements; **the algorithm used to produce each distribution is implementation-defined**, so only the statistical definition is portable. Families: uniform (`uniform_int_distribution`, `uniform_real_distribution`); Bernoulli (`bernoulli_distribution`, `binomial_distribution`, `geometric_distribution`, `negative_binomial_distribution`); Poisson-related (`poisson_distribution`, `exponential_distribution`, `gamma_distribution`, `weibull_distribution`, `extreme_value_distribution`); normal-related (`normal_distribution`, `lognormal_distribution`, `chi_squared_distribution`, `cauchy_distribution`, `fisher_f_distribution`, `student_t_distribution`); sampling (`discrete_distribution`, `piecewise_constant_distribution`, `piecewise_linear_distribution`). Probability functions are zero outside their stated domains.

## `rand`/`srand` (`[c.math.rand]`)

C semantics; may or may not race (implementation-defined); the implementation may specify that library functions call `rand`.

## Related

[[cpp17-lib-numerics]] · [[mutating-sequence-algorithms]] (`shuffle`, `sample`) · [[numeric-limits]] · [[formatted-and-unformatted-io]] (engine/distribution streaming)
