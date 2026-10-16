---
type: concept
title: "C++17 clause 7: standard conversions"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 7: Standard conversions (`[conv]`)

Implicit conversions with built-in meaning. About 2,700 words; 15 sections.

## Standard conversion sequences (`[conv]/1`)

At most one conversion from each group, **in this order**:

1. lvalue-to-rvalue, array-to-pointer, or function-to-pointer;
2. one of: integral promotion, floating-point promotion, integral conversion, floating-point conversion, floating-integral conversion, pointer conversion, pointer-to-member conversion, boolean conversion;
3. function pointer conversion;
4. qualification conversion.

Definitions:

- `e` is **implicitly convertible** to `T` iff `T t = e;` is well-formed for an invented `t` (`/3`).
- **Contextually converted to `bool`**: iff `bool t(e);` is well-formed (`/4`) — used by `if`, `!`, `&&`, `||`, `?:` conditions etc.
- **Contextually implicitly converted** to one of a set of types (e.g. `delete` operand): the class is searched for non-explicit conversion functions yielding an allowed type; there must be exactly one (`/5`).
- The result of an implicit conversion is an lvalue if `T` is an lvalue reference (or rvalue reference to function), an xvalue if an rvalue reference to object, else a prvalue (`/6`).

## The conversions

| Conversion | Section | Key rule |
|---|---|---|
| lvalue-to-rvalue | `[conv.lval]` | glvalue of non-function, non-array `T` → prvalue; ill-formed if `T` is incomplete; type is cv-unqualified `T` for non-class types. For `std::nullptr_t` the result is a null pointer constant; for class types the result object is copy-initialized; reading an object holding an invalid pointer value is implementation-defined. The value is *not accessed* when the operand is unevaluated or names a variable that is not odr-used |
| array-to-pointer | `[conv.array]` | array → pointer to first element; temporary materialization is applied first |
| function-to-pointer | `[conv.func]` | function lvalue → pointer to function |
| **temporary materialization** | `[conv.rval]` | prvalue of `T` → xvalue of `T`: a temporary is initialized with the prvalue as its result object; `T` must be complete. See [[copy-elision-and-temporary-materialization]] |
| qualification | `[conv.qual]` | cv-decomposition; two types are **similar** if they decompose with the same shape (same pointer/array/ptr-to-member components and same underlying type U); conversion allowed if similar, cv added never removed at any level, and `const` present at all intermediate levels when a level changes |
| integral promotion | `[conv.prom]` | small integer types → `int` if it can represent all values, else `unsigned int`; `char16_t`, `char32_t`, `wchar_t`, and unscoped enums without fixed underlying type → first of `int`/`unsigned`/`long`/... that fits; fixed-underlying-type enums → underlying type (and its promotion); bit-fields → `int`/`unsigned int` if they fit; `bool` → `int` |
| floating-point promotion | `[conv.fpprom]` | `float` → `double`, value unchanged |
| integral conversion | `[conv.integral]` | to unsigned: value modulo 2ⁿ; to signed: unchanged if representable, **otherwise implementation-defined**; to `bool` see below; promotions are excluded from this set |
| floating-point conversion | `[conv.double]` | exact if representable; between two neighbors: implementation-defined choice of either; **out of range: undefined behavior** |
| floating-integral | `[conv.fpint]` | float→int truncates; **undefined if the truncated value is not representable**. int→float exact if possible else implementation-defined choice of next lower/higher; out of range is undefined |
| pointer | `[conv.ptr]` | null pointer constant (integer literal 0 or a `std::nullptr_t` prvalue) → null pointer value; `T*` → `void*`; derived → base pointer (ill-formed if base inaccessible or ambiguous) |
| pointer-to-member | `[conv.mem]` | null pointer constant → null member pointer; pointer to member of base → pointer to member of derived (ill-formed if base is inaccessible, ambiguous, or virtual) |
| function pointer | `[conv.fctptr]` | "pointer to `noexcept` function" → "pointer to function" (and the member-function analogue) |
| boolean | `[conv.bool]` | arithmetic, unscoped enum, pointer, pointer-to-member → `bool`; zero/null → `false`. In direct-initialization `std::nullptr_t` → `bool` (false) |

## Integer conversion rank (`[conv.rank]`)

Rank order: `bool` < `signed char` < `short` < `int` < `long` < `long long`; unsigned types equal the rank of their signed counterparts; `char` equals `signed char`/`unsigned char`; `char16_t`/`char32_t`/`wchar_t` equal their underlying types; a standard integer type outranks an extended one of equal size; rank is transitive.

## Usual arithmetic conversions

The common-type rules for binary arithmetic operators live in [[cpp17-expressions]].

## Related

[[value-categories]] · [[strict-aliasing]] · [[cpp17-basic-concepts]] · [[overload-resolution]] (ranking of conversion sequences)
