---
type: concept
title: "numeric_limits and the implementation-limits headers"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `numeric_limits`, `<climits>`, `<cfloat>` (`[support.limits]`)

Where a program asks what the arithmetic types look like on this implementation. Parent: [[cpp17-lib-language-support]].

## Rules for the class template (`[numeric.limits]`, `[numeric.special]`)

- The primary template has every member present with value 0/false (`is_specialized` is false). **Specializations are provided for every arithmetic type, including `bool`**, with `is_specialized == true`. cv-qualified types report the same values as the unqualified type. Non-arithmetic standard types (e.g. `complex<T>`) must not be specialized by the library (`/3-6`).
- All `static constexpr` members are usable in constant expressions. Member *functions* (`min`, `max`, `lowest`, `epsilon`, `infinity`, ...) are signal-safe (`[numeric.limits.members]/1`).
- Every member is declared for every specialization, but many are only *meaningful* under a condition (e.g. `epsilon()` only for floating types); a non-meaningful member is set to 0 or false (`[numeric.special]/1`).

## Members and their meaning

| Member | Meaning |
|---|---|
| `min()` | minimum finite value; for floating types with subnormals, the smallest positive *normalized* value; meaningful if bounded, or unbounded and unsigned |
| `max()` | maximum finite value (meaningful if `is_bounded`) |
| `lowest()` | the finite value `x` with no finite `y < x` (differs from `min()` for floating types) |
| `digits` / `digits10` | radix digits / decimal digits representable without change (integers: non-sign bits; floats: mantissa digits) |
| `max_digits10` | decimal digits needed to distinguish all values (floating types) |
| `is_signed`, `is_integer`, `is_exact`, `radix` | representation traits; all integers are exact, not all exact types are integer |
| `epsilon()`, `round_error()` | machine epsilon (gap between 1 and the next larger value); maximum rounding error |
| `min_exponent`, `max_exponent` (and `10` variants) | exponent range (floating types) |
| `has_infinity`, `has_quiet_NaN`, `has_signaling_NaN` | availability of those values; all three must be true when `is_iec559` |
| `infinity()`, `quiet_NaN()`, `signaling_NaN()` | the values themselves (required when `is_iec559`) |
| `has_denorm`, `has_denorm_loss`, `denorm_min()` | subnormal support (`denorm_present`/`denorm_absent`/`denorm_indeterminate`), loss detection, smallest positive subnormal |
| `is_iec559` | conforms to ISO/IEC/IEEE 60559 |
| `is_bounded` | finite set of representable values |
| `is_modulo` | out-of-range `+`, `-`, `*` results wrap modulo `max() - min() + 1` |
| `traps`, `tinyness_before` | trapping arithmetic at startup; tininess detected before rounding |
| `round_style` | one of `round_indeterminate`, `round_toward_zero`, `round_to_nearest`, `round_toward_infinity`, `round_toward_neg_infinity`; integer specializations return `round_toward_zero` |

## Headers

`<climits>` and `<cfloat>` define the same macros as C `<limits.h>` and `<float.h>` (`[climits.syn]`, `[cfloat.syn]`). Whether an integer type is signed or what `char` is are implementation properties documented in [[cpp17-basic-concepts]].

## Related

[[cpp17-lib-language-support]] · [[cpp17-lib-numerics]] · [[constant-expressions]]
