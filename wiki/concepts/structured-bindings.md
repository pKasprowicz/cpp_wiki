---
type: concept
title: "Structured bindings"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Structured bindings (`[dcl.struct.bind]`)

A **structured binding declaration** `auto [v0, v1, ...] = expr;` (also `{expr}` or `(expr)` initializers) introduces names for the parts of an object. The decl-specifier-seq may contain only `auto` and cv-qualifiers, optionally with a ref-qualifier (`&`/`&&`) after it; the initializer must be of array or non-union class type. Declared in [[cpp17-declarations]]; usable as a range-for declaration ([[cpp17-statements]]).

## Mechanism

1. A hidden variable `e` is introduced. If the initializer has array type `A` and there is no ref-qualifier, `e` has type `cv A` and its elements are copy- or direct-initialized element-wise from the source array. Otherwise `e` is defined as if by `decl-specifier-seq ref-qualifier e initializer;` (never read as a function declaration). Call its type `E`.
2. The number of names must match, and the meaning is chosen in this order:

| Case | Condition | What `vi` is |
|---|---|---|
| array | `E` is an array type | an lvalue referring to element `i`, type = the element type |
| tuple-like | `std::tuple_size<E>` is a complete type; `tuple_size<E>::value` is an integral constant expression | `get`: a member `e.get<i>()` if member lookup of `get` in `E` finds anything, else `get<i>(e)` found via ADL; `vi` is a variable of type "reference to `Ti`" (`Ti = std::tuple_element<i, E>::type`) initialized from that, an lvalue reference if the initializer is an lvalue, else an rvalue reference. `e` is treated as an lvalue if its type is an lvalue reference, else as an xvalue |
| plain class | otherwise | every non-static data member of `E` must be a **public** direct member of `E` or of one unambiguous public base; no anonymous union member; count must equal the number of members; `vi` names member `mi` of `e` (declaration order) with type `cv Ti` (bit-field if the member is) |

## Type queries

`decltype(vi)` for an unparenthesized binding gives the *referenced type* from the table (the element type, `Ti`, or `cv Ti`), per `[dcl.type.simple]/4`.

## Related

[[cpp17-declarations]] · [[template-argument-deduction]] (`auto` deduction for the hidden variable) · [[value-categories]] · [[name-lookup]] (ADL for `get`)
