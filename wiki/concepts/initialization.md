---
type: concept
title: "Initialization"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Initialization (`[dcl.init]` and subsections)

Section 11.6 of [[cpp17-declarators]]. Covers variable initializers and every other place initialization happens (function parameters, return values, `new`, `throw`, handlers, aggregate members).

## The initial forms

- `= initializer-clause`, `= {braced-init-list}`, `{braced-init-list}` and `( expression-list )` initializers; an initializer in a variable definition may involve arbitrary expressions regardless of storage duration (except `constexpr` objects, [[constant-expressions]]). A block-scope variable with external or internal linkage cannot have an initializer.
- **Copy-initialization**: the `=` form, condition declarations, argument passing, function return, `throw`, handlers, aggregate member initialization. **Direct-initialization**: `T x(a)`, `T x{a}`, `new T(...)`, `static_cast`, functional casts, mem-initializers.
- Parenthesized lists are evaluated in the order specified for function calls; a pack-expansion `...` after an initializer-clause is allowed. A non-class entity's parenthesized list must be a single expression. An object whose initialization has completed is *constructed*.

## Kinds

| Kind | Definition (paraphrased) |
|---|---|
| zero-initialization | scalars get the converted `0`; class types: every non-static member, non-virtual base (and virtual bases of a most-derived object) zero-initialized and padding zeroed; unions: first named member + padding; arrays elementwise; references: nothing |
| default-initialization | class: call the default constructor chosen by overload resolution; array: each element; otherwise **no initialization is performed** |
| value-initialization | class with no default constructor or a user-provided/deleted one: default-initialize; class with an implicit/defaulted one: zero-initialize, then default-initialize if the default constructor is non-trivial; arrays elementwise; otherwise zero-initialize. `()` initializers value-initialize. Value- or default-initializing a reference is ill-formed |
| constant initialization | see [[program-startup-and-termination]] |

A **const-default-constructible** class (user-provided constructor, or all members have default member initializers/are themselves const-default-constructible, ...) is required to default-initialize a const object.

## Indeterminate values (`/12`)

With no initializer the object is default-initialized. Storage of automatic or dynamic objects starts with an **indeterminate value**, which stays until replaced. Producing an indeterminate value is **undefined behavior** except for `unsigned narrow character` or `std::byte` values flowing through: the second/third operand of `?:`, the right operand of `,`, a cast/conversion to those types, a discarded-value expression, the right side of a simple assignment to such an object, or initialization of such an object — in which case the result stays indeterminate.

## Semantics of an initializer (`/17`)

1. Braced-init-list → list-initialization.
2. Reference destination → reference rules (below).
3. Character array with a string literal → `[dcl.init.string]`: elements initialized from successive characters, fewer than the array size → rest zero-initialized, more → ill-formed.
4. `()` → value-initialization. Any other array initializer → ill-formed.
5. Class destination:
   - **If the initializer is a prvalue of the same class (cv-unqualified), it is used directly to initialize the destination object** — no copy or move constructor is considered (this is the rule that makes elision mandatory for prvalue initialization in N4659; see [[copy-elision-and-temporary-materialization]]).
   - else direct-initialization, or copy-initialization from the same/derived class: constructors enumerated by overload resolution ([[overload-resolution]]);
   - else copy-initialization from another type: user-defined conversion sequences are enumerated and the result direct-initializes the destination.
6. Class-type source, non-class destination: conversion functions considered.
7. Otherwise standard conversions only (a bit-field that cannot hold the value gets an implementation-defined value).

## Aggregates (`[dcl.init.aggr]`)

An **aggregate** is an array or a class with: no user-provided, explicit, or inherited constructors; no private/protected non-static data members; no virtual functions; no virtual, private or protected base classes. So public non-virtual **base classes are permitted** and are aggregate *elements*, initialized (in declaration order) before the direct non-static data members. Rules:

- each element is copy-initialized from its initializer-clause; a required narrowing conversion is ill-formed; more clauses than elements is ill-formed;
- fewer clauses: remaining elements use the default member initializer if present, else copy-initialization from `{}`, else (for references) ill-formed; an empty list for a union initializes a variant member with a default initializer or else the first member;
- brace elision applies to subaggregates; multidimensional arrays fill with the last index varying fastest;
- a union's brace initializer holds only a clause for its first member;
- an array of unknown bound initialized by *n* clauses has *n* elements (`n > 0`).
- An aggregate class can also be initialized from a single non-braced expression of its own type via the ordinary rules.

## References (`[dcl.init.ref]`)

Types `cv1 T1` and `cv2 T2`: **reference-related** if same type or T1 is a base of T2; **reference-compatible** if reference-related (or T2 is `noexcept` function and T1 the matching plain function type) and cv1 ≥ cv2.

- Lvalue reference to `cv1 T1` binds directly to an lvalue (not a bit-field) of reference-compatible type, or to the lvalue result of a conversion function on a class-type initializer.
- Otherwise it must be an lvalue reference to non-volatile `const`, or an rvalue reference. Then: an rvalue (not a bit-field) or function lvalue of reference-compatible type binds directly, after **temporary materialization** if it is a prvalue; or a class-type initializer converted by a conversion function to an rvalue; otherwise user-defined conversions may apply and finally the initializer is converted to a prvalue of type `cv1 T1`, materialized, and bound (not "direct").
- If T1 is reference-related to T2: cv1 must be ≥ cv2, and an rvalue reference cannot bind to an lvalue.
- A reference cannot be rebound; binding to an inaccessible or ambiguous base is ill-formed.

## List-initialization (`[dcl.init.list]`)

`{...}` can be direct-list- or copy-list-initialization. Resolution order (`/3`):

1. aggregate class and a single element of type `T` or derived → initialize from that element;
2. char array + single string literal → string rules;
3. aggregate → aggregate initialization;
4. empty list + class with a default constructor → value-initialization;
5. `std::initializer_list<E>` → build a temporary `const E[N]` array (elements copy-initialized; narrowing ill-formed; the array lives like a temporary, extended when bound to the `initializer_list`);
6. other class → constructors via overload resolution (initializer-list constructors first, [[overload-resolution]]); narrowing ill-formed;
7. enumeration with fixed underlying type + single element + direct-list-initialization → `T(v)` (narrowing to the underlying type ill-formed);
8. single-element list → initialize from that element (reference binding if reference-related);
9. reference otherwise → a prvalue of the referenced type is list-initialized and bound;
10. empty list → value-initialization; else ill-formed.

Elements of a braced-init-list (including pack expansions) are evaluated **left to right**, each fully sequenced before the next. Using `std::initializer_list` without including `<initializer_list>` is ill-formed.

**Narrowing conversions** (ill-formed in list-initialization): floating → integer; `long double` → `double`/`float` or `double` → `float` (unless the constant fits the range); integer/unscoped enum → floating (unless a constant that converts back exactly); integer/unscoped enum → an integer type that can't hold all source values (unless a constant that fits).

## Related

[[cpp17-declarators]] · [[value-categories]] · [[cpp17-special-member-functions]] · [[new-and-delete-expressions]] · [[program-startup-and-termination]]
