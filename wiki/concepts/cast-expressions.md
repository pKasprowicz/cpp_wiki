---
type: concept
title: "Casts: static, reinterpret, const, dynamic and C-style"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Cast expressions

From `[expr.cast]`, `[expr.static.cast]`, `[expr.reinterpret.cast]`, `[expr.const.cast]`, `[expr.dynamic.cast]`, `[expr.type.conv]` in [[cpp17-expressions]]. Result category for all named casts to a reference: lvalue if `T` is an lvalue reference (or rvalue reference to function), xvalue if rvalue reference to object; otherwise a prvalue (with lvalue-to-rvalue / array-to-pointer / function-to-pointer applied to the operand).

## `static_cast<T>(v)` (`[expr.static.cast]`)

Never casts away constness. Allowed conversions, in order of the rules:

- Anything implicitly convertible, or direct-initialization of `T` from `v` that has a viable constructor/conversion (`/4`).
- Any expression to `cv void` (becomes a discarded-value expression).
- The **inverse of a standard conversion sequence** that contains none of: lvalue-to-rvalue, array-to-pointer, function-to-pointer, null pointer, null member pointer, boolean, or function pointer conversion (`/7`).
- Scoped enum → integral (value unchanged if representable, else unspecified; `bool`: zero → false) or floating type; integral/enum/floating → enumeration (**undefined** if the value is outside the enumeration's range, for integral/enum sources) (`/9-10`).
- **Downcast** pointer/reference to base → derived: ill-formed through a virtual base or when no valid derived→base standard conversion exists; if the base is not actually a subobject of a derived object the behavior is **undefined** (`/2`, `/11`). The same for pointer to member base ↔ derived (`/12`).
- `void*` → `T*`: unspecified if the address is misaligned for `T`; otherwise, if an object pointer-interconvertible with the pointed-to object has type `T`, the result points to it, else the value is unchanged (`/13`).

## `reinterpret_cast<T>(v)` (`[expr.reinterpret.cast]`)

Never casts away constness. Permitted: pointer → integer large enough (mapping implementation-defined); integer/enum → pointer (round trip through a large enough integer preserves the pointer); function pointer ↔ function pointer of another type (round trip back yields the original; other results unspecified); object pointer ↔ object pointer (equivalent to `static_cast` through `void*`); function pointer ↔ object pointer is only **conditionally-supported**; member pointers between like kinds (results unspecified except for round trips); glvalue of `T1` → "reference to `T2`" when the pointer conversion is allowed (no temporaries, constructors or conversion functions). Null pointer values convert to null pointer values.

## `const_cast<T>(v)` (`[expr.const.cast]`)

Between **similar types**, referring to the original entity; reference forms also allowed. A conversion *casts away constness* when no qualification conversion could produce the same cv-structure.

## `dynamic_cast<T>(v)` (`[expr.dynamic.cast]`)

`T` is a pointer or reference to a complete class type, or `cv void*`; never casts away constness. Same-type or more-cv-qualified target returns `v`; a null pointer gives a null pointer; derived → base (unique, accessible) needs no run-time check. Otherwise `v` must have polymorphic type, and a run-time check on the most derived object succeeds if `v` points to a public base subobject of a unique `C` object, or the most derived object has an unambiguous public base of type `C`. A failed pointer cast yields a null pointer; a failed reference cast throws something matching `std::bad_cast`. `dynamic_cast<cv void*>` yields a pointer to the most derived object.

## C-style cast `(T)e` and functional notation (`[expr.cast]`, `[expr.type.conv]`)

The cast notation can perform, trying in this order and taking the first that applies: `const_cast`; `static_cast`; `static_cast` then `const_cast`; `reinterpret_cast`; `reinterpret_cast` then `const_cast`. Additionally, `static_cast`-like base/derived conversions are valid even if the base class is inaccessible. Two interpretations as `static_cast`+`const_cast` make it ill-formed. Casting to/from pointers to incomplete class types is allowed, and which interpretation is used between incomplete class types is unspecified.

`T(e)` with a single parenthesized expression is equivalent to `(T)e`; otherwise the result prvalue's object is direct-initialized.

## Related

[[cpp17-standard-conversions]] · [[strict-aliasing]] · [[storage-duration-and-object-lifetime]] · [[value-categories]]
