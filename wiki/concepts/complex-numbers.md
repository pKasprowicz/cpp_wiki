---
type: concept
title: "std::complex"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `complex<T>` (`[complex.numbers]`)

Parent: [[cpp17-lib-numerics]].

## Model and guarantees

- `complex<T>` stores Cartesian `real()` and `imag()` parts. The effect of instantiating it for anything other than `float`, `double` or `long double` is **unspecified**; those three specializations are literal types. Results that are not mathematically defined or out of range are **undefined behavior** (`/3`).
- **Array-compatible layout** (`/4`): for an lvalue `z` of type cv `complex<T>`, `reinterpret_cast<cv T(&)[2]>(z)` is well-formed with `[0]` the real part and `[1]` the imaginary part, and for an array of complex numbers, `reinterpret_cast<cv T*>(a)[2*i]` / `[2*i + 1]` designate the real/imaginary parts of `a[i]`. This gives C interoperability ([[strict-aliasing]]).
- Members: `real()`, `imag()` (getters and setters), constructor from `(re, im)` with defaults, converting constructors between the three specializations (`explicit` where narrowing), compound assignments `+= -= *= /=` with scalar or complex right-hand side.

## Operations

- Non-member `+`, `-`, `*`, `/` (complex–complex, complex–scalar, scalar–complex), unary `+`/`-`, `==`, `!=` (scalar comparisons assume a zero imaginary part). **Stream I/O**: extraction accepts `u`, `(u)` or `(u,v)`; bad input sets `failbit`; insertion writes `(real,imag)`.
- Value operations: `real`, `imag`, `abs` (magnitude), `arg` (phase angle, as `atan2(imag, real)`), `norm` (squared magnitude), `conj`, `proj` (projection onto the Riemann sphere, as C `cproj`), `polar(rho, theta)` (requires `rho` non-negative and non-NaN, `theta` finite).
- Transcendentals: `acos`, `asin`, `atan`, `acosh`, `asinh`, `atanh` (behaving as the C `c…` functions), `cos`, `cosh`, `exp`, `log` (imaginary part in `[−π, π]`, branch cut on the negative real axis), `log10`, `pow` (`exp(y·log(x))`; the value of `pow(0, 0)` is implementation-defined), `sin`, `sinh`, `sqrt` (right half-plane; a negative real argument gives a value on the positive imaginary axis), `tan`, `tanh`.
- **Additional overloads** (`[cmplx.over]`): functions such as `arg`, `norm`, `conj`, `proj`, `real`, `imag` accept scalars: an argument of `long double` acts as `complex<long double>`, `double` or an integer type as `complex<double>`, `float` as `complex<float>`; `pow` with at least one complex argument promotes both arguments to the widest type among them.
- **Literal suffixes** `i`, `il`, `if` (in `std::literals::complex_literals`) build `complex<double>`, `complex<long double>`, `complex<float>` with the given imaginary part and zero real part.

## Element-type requirements

`complex` and `valarray` may be instantiated only with types meeting `[numeric.requirements]` (`T` not abstract/reference/cv-qualified; if a class, it needs public default and copy constructors, a public destructor, a public copy assignment, mutually consistent initialization/assignment semantics, no overloaded unary `&`); if any operation on `T` throws, the effects are undefined.

## Related

[[cpp17-lib-numerics]] · [[valarray]] · [[math-functions-and-fenv]] · [[formatted-and-unformatted-io]] · [[literals]]
