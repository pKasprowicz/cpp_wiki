---
type: concept
title: "Constant expressions and constexpr"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Constant expressions and `constexpr`

Primary sources: `[expr.const]` ([[cpp17-expressions]]), `[dcl.constexpr]` ([[cpp17-declarations]]), `[basic.start.static]` ([[program-startup-and-termination]]), literal types in `[basic.types]` ([[cpp17-basic-concepts]]).

## Core constant expression (`[expr.const]/2`)

An expression `e` is a **core constant expression** unless evaluating it per the abstract machine would evaluate any of:

- `this`, outside a `constexpr` function/constructor being evaluated as part of `e`;
- a call to anything other than a `constexpr` function, a `constexpr` constructor of a literal class, or an implicit trivial destructor; a call to an undefined `constexpr` function; a call to an instantiated `constexpr` function that fails the requirements;
- an expression exceeding implementation limits;
- an operation with **undefined behavior** specified in clauses [intro] through [cpp] (library undefined behavior makes it *unspecified* whether `e` is a core constant expression);
- an lvalue-to-rvalue conversion, except on: a non-volatile integral/enumeration glvalue naming a complete non-volatile const object with a preceding constant-expression initialization; a subobject of a string literal; a non-volatile object defined `constexpr` (or a non-mutable subobject); or a non-volatile literal-type object whose lifetime began inside `e`;
- an lvalue-to-rvalue conversion of a non-active union member; copy/move of a union whose active member is mutable (unless it began in `e`); an assignment that changes a union's active member;
- an id-expression naming a reference variable/member lacking a preceding constant initialization (unless its lifetime began in `e`);
- inside a lambda, an odr-use of `this` or an outer automatic variable;
- `void*` → object pointer conversion; `dynamic_cast`; `reinterpret_cast`; pseudo-destructor call;
- modification of an object unless it is a non-volatile literal-type object whose lifetime began within `e`;
- `typeid` of a polymorphic glvalue; `new`; `delete`; a relational/equality comparison with unspecified result; `throw`.

## Derived notions

| Notion | Definition |
|---|---|
| integral constant expression | integral/unscoped-enum type, implicitly converted to a prvalue, core constant expression |
| converted constant expression of type `T` | constant expression implicitly converted to `T` using only user-defined conversions, lvalue-to-rvalue, array-to-pointer, function-to-pointer, qualification, integral promotions, non-narrowing integral conversions, null pointer / null member pointer conversions from `std::nullptr_t`, and function pointer conversions; reference binding must be direct |
| contextually converted constant expression of type `bool` | same, contextually converted to `bool` |
| constant expression | glvalue core constant expression referring to a *permitted result*, or a prvalue core constant expression whose value is valid: class-type references refer to permitted results; pointer values are the address of a static-storage object, one-past-the-end of one, the address of a function, or null; subobjects recursively |
| permitted result | an object with static storage duration (a temporary only if its value itself qualifies) or a function |

A class-type expression used where an integral constant is needed is contextually implicitly converted, and the selected conversion function must be `constexpr`. Constant expressions are evaluated assuming copy elision is performed.

## `constexpr` entities (`[dcl.constexpr]`)

See [[cpp17-declarations]] for the full requirement lists. In short: `constexpr` functions and static data members are implicitly `inline`; a `constexpr` variable is `const`, literal-typed and constant-initialized; the specifier does not change the function's type; a `constexpr` function behaves like an equivalent ordinary function except that calls can occur in constant expressions and copy elision is mandatory there. An instantiated `constexpr` function template specialization that fails the requirements is still `constexpr` but cannot appear in a constant expression; if no specialization could satisfy them the template is ill-formed, no diagnostic required.

## Where constant expressions are required

Array bounds, `case` labels, non-type template arguments, enumerator initializers, `static_assert`, `if constexpr` conditions, `alignas`, bit-field widths ([[cpp17-statements]], [[cpp17-declarators]], [[cpp17-templates]]), and *constant initialization* of static/thread-duration variables ([[program-startup-and-termination]]).

## Related

[[cpp17-declarations]] · [[lambda-expressions]] (constexpr lambdas) · [[abstract-machine-and-observable-behavior]] · [[implementation-quantities]] (recursion and evaluation-count limits)
