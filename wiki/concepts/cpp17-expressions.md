---
type: concept
title: "C++17 clause 8: expressions"
tags: [cpp17, language-core, standard-clause, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 8: Expressions (`[expr]`)

The second-largest language clause (about 18,000 words; 48 labelled sections). It defines built-in operator behavior; overloaded operators go through [[overload-resolution]] but may not change the built-in rules (`/3`).

## Section map

| Section | Label | Where summarized |
|---|---|---|
| 8.1 Primary expressions | `[expr.prim]` | below; lambdas: [[lambda-expressions]]; fold expressions: [[fold-expressions]] |
| 8.2 Postfix expressions | `[expr.post]` | below; casts: [[cast-expressions]] |
| 8.3 Unary expressions | `[expr.unary]` | below; `new`/`delete`: [[new-and-delete-expressions]] |
| 8.4 Explicit type conversion (cast notation) | `[expr.cast]` | [[cast-expressions]] |
| 8.5-8.19 Binary and ternary operators, `throw`, assignment, comma | `[expr.mptr.oper]` ... `[expr.comma]` | below |
| 8.20 Constant expressions | `[expr.const]` | [[constant-expressions]] |

## General rules (`[expr]/3-15`)

- If an evaluation's result is not mathematically defined or is outside the representable range, the behavior is **undefined** (`/4`).
- A reference-typed expression has its type adjusted to the referenced type; it is an lvalue or xvalue. A prvalue of cv-qualified non-class, non-array type has its cv removed (`/5-6`).
- Glvalues used where a prvalue operand is expected get lvalue-to-rvalue / array-to-pointer / function-to-pointer; prvalues used where a glvalue is expected get **temporary materialization** (`/9-10`).
- **Usual arithmetic conversions** (`/11`): scoped enum operands: no conversion, ill-formed unless the other has the same type. Otherwise: `long double` > `double` > `float`; else integral promotions then: same type → done; both signed or both unsigned → convert to the higher rank; unsigned rank ≥ signed rank → convert to the unsigned type; signed type can represent all unsigned values → convert to signed; else both convert to the unsigned type corresponding to the signed one.
- **Discarded-value expressions** (`/12`): evaluated only for side effects; lvalue-to-rvalue is applied only to volatile glvalues of specific forms (id-expression, subscript, member access, indirection, pointer-to-member, parenthesized/conditional/comma thereof); prvalues are materialized.
- Floating operands and results may carry extra precision/range (`/13`).
- **cv-combined type** (`/14`) and **composite pointer type** (`/15`) are used by relational/equality/conditional operators; no composite type means ill-formed.

## Primary expressions (`[expr.prim]`)

- A string literal is an lvalue; every other literal is a prvalue.
- `this` is a prvalue pointer to the class (cv-qualified like the member function), valid in member function declarations after the cv-qualifier-seq and in default member initializers; not in static member functions.
- An id-expression naming a non-static member can only be used in class member access, to form a pointer to member, or (for data members) in an unevaluated operand. Identifiers are lvalues if they name a function, variable or data member, prvalues otherwise (enumerators are prvalues).

## Postfix expressions (`[expr.post]`)

- `E1[E2]` is `*((E1)+(E2))` (an array operand yields an lvalue if the array is an lvalue, else an xvalue); braced-init-lists are not allowed.
- Function calls: the call type is the *statically chosen* function's return type; virtual calls go to the final overrider. Calling through the wrong function type is undefined. Variadic arguments get the **default argument promotions** (`float`→`double`, integral promotions, `std::nullptr_t`→`void*`). It is implementation-defined whether a parameter's lifetime ends at function return or at the end of the enclosing full-expression. Recursion is allowed except of `main`.
- Functional-notation conversion `T(x)` equals the cast `(T)x`; with a braced-init-list or several arguments it direct-initializes a prvalue. A deduced class placeholder is resolved by class template argument deduction ([[template-argument-deduction]]).
- Class member access `E1.E2` / `E1->E2` (`(*(E1)).E2`): result is an lvalue for references and static members, an lvalue/xvalue for non-static data members depending on `E1`, a prvalue for member functions (usable only as a call's left operand) and enumerators; a `mutable` member drops `const`.
- Postfix `++`/`--`: operand a modifiable lvalue of arithmetic type other than `bool`, or a pointer to a complete object type; result is a prvalue of the old value.

## Unary expressions (`[expr.unary]`)

- `*p`: lvalue; `&x`: pointer prvalue (or pointer-to-member when applied to an unparenthesized qualified-id naming a non-static member); the address of an overloaded function needs a disambiguating context; `&` on a bit-field is ill-formed.
- Unary `+`, `-`, `~`: integral promotion; unsigned negation is computed modulo 2ⁿ; `!` contextually converts to `bool`.
- Prefix `++`/`--`: lvalue result, equivalent to `x += 1`.
- `sizeof`: operand unevaluated; yields `std::size_t`; `sizeof(char)`, `sizeof(signed char)`, `sizeof(unsigned char)` are 1; applying to a reference gives the referenced type's size; to a class includes padding; ill-formed for function, incomplete or bit-field operands. `sizeof...(pack)` gives the pack length.
- `alignof(type-id)`: `std::size_t` constant; for references/arrays it is the referenced/element type's alignment.
- `noexcept(expr)`: unevaluated; `bool` prvalue constant that is true unless the expression is potentially-throwing.

## Binary and other operators

| Operators | Key rules |
|---|---|
| `.*`, `->*` | second operand pointer to member; if the dynamic type of the object lacks the member the behavior is undefined; a member-function result can only be called; ref-qualifier mismatches ill-formed; null member pointer → undefined |
| `*`, `/`, `%` | usual arithmetic conversions; division by zero **undefined**; if `a/b` is not representable, both `a/b` and `a%b` are undefined; otherwise `(a/b)*b + a%b == a` |
| `+`, `-` | pointer ± integer must stay within `[0, n]` of the array (including one-past-end) else **undefined**; pointer difference defined only within one array, type is `std::ptrdiff_t`; element type must be similar to the pointed-to type; adding 0 to a null pointer yields null |
| `<<`, `>>` | integral promotions; **undefined** if the right operand is negative or ≥ the promoted left operand's bit width; `<<` on signed: defined only if non-negative and the result is representable in the corresponding unsigned type; `>>` of a negative signed value is implementation-defined |
| `<`, `>`, `<=`, `>=` | pointers compare by array position or declaration order within an object (same access control, non-union); otherwise unspecified |
| `==`, `!=` | one-past-the-end vs. another object's address is **unspecified**; null pointers compare equal; pointers to virtual member functions or unrelated classes are unspecified |
| `&`, `^`, `\|` | integral or unscoped enumeration operands, usual arithmetic conversions |
| `&&`, `\|\|` | operands contextually converted to `bool`; short-circuit; result `bool` |
| `?:` | complicated type/value-category rules ([expr.cond]); only one of the 2nd/3rd operands evaluated; one operand may be a throw-expression |
| `throw` | type `void`; the exception object type is the decayed, cv-stripped static type of the operand; a bare `throw;` with no handled exception calls `std::terminate()` |
| `=`, `op=` | modifiable lvalue left operand, result is an lvalue; `x = {v}` means `x = T{v}`; overlapping read/write of objects must overlap exactly with the same type, else **undefined** |
| `,` | left operand is a discarded-value expression; result has the right operand's type and value category |

## Evaluation-order rules per operator

See the table in [[sequencing-and-evaluation-order]] (built from `[expr.*]`).

## Related

[[cpp17-standard-conversions]] · [[value-categories]] · [[overload-resolution]] · [[cpp17-basic-concepts]] · [[grammar-expressions-and-statements]] (Annex A.4)
