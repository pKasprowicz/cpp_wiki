---
type: concept
title: "<cmath> math functions, special functions and <cfenv>"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Mathematical functions for floating-point types and the floating-point environment (`[c.math]`, `[cfenv]`)

Parent: [[cpp17-lib-numerics]]. Limits and traits of the floating types: [[numeric-limits]].

## `<cmath>` (`[c.math]`)

- `<cmath>` = C `<math.h>` in `std`, **plus** the three-argument `hypot(x, y, z)` (`√(x²+y²+z²)`) and the **mathematical special functions** below (`[cmath.syn]/1`).
- **Overload promotion**: for every overloaded function other than `abs`, additional overloads ensure that if any argument corresponding to a `double` parameter is `long double`, all such arguments are treated as `long double`; otherwise if any is `double` or an integer type, all are treated as `double`; otherwise all are `float` (`/2`). So `pow(2, 3.0f)` is a `double` computation. The classification/comparison functions (`isnan`, `isfinite`, `isgreater`, ...) behave like the C macros and are overloaded for the three floating types.
- `abs` has overloads for the integer and floating types with C semantics; calling it with an unsigned type that cannot be promoted to `int` is ill-formed (`[c.math.abs]/3`).
- `<cstdlib>` also declares `rand`/`srand` and the integer `abs` family ([[random-number-generation]], `[c.math.rand]`).

## Special functions (`[sf.cmath]`)

`assoc_laguerre`, `assoc_legendre`, `beta`, `comp_ellint_1/2/3`, `cyl_bessel_i/j/k`, `cyl_neumann`, `ellint_1/2/3`, `expint`, `hermite`, `laguerre`, `legendre`, `riemann_zeta`, `sph_bessel`, `sph_legendre`, `sph_neumann`, each in `float`/`double`/`long double` versions with a suffix variant (`f`, `l`). Common rules: a NaN argument yields a NaN and **does not** report a domain error; otherwise a domain error is reported exactly when the arguments fall outside the explicitly stated domain, the mathematical value has a non-zero imaginary part, or the function is undefined there. Unless stated, each function is defined for all finite values and for ±∞.

## `<cfenv>` (`[cfenv]`)

Same contents and meaning as C `<fenv.h>`. The floating-point environment has **thread storage duration**: each thread has its own environment, functions act on the calling thread's, and a new thread's environment is initialized from that of the thread that constructed the `thread` object when it did so. See [[threads]].

## Related

[[cpp17-lib-numerics]] · [[complex-numbers]] · [[numeric-limits]] · [[cpp17-lib-language-support]]
