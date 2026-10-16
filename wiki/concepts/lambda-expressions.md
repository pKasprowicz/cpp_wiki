---
type: concept
title: "Lambda expressions"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Lambda expressions (`[expr.prim.lambda]`)

A lambda-expression is a **prvalue whose result object is the closure object**. It may not appear in an unevaluated operand, a template-argument, an alias-declaration, a typedef, or in a function declaration outside the function body and default arguments. In the decl-specifier-seq of the lambda-declarator only `mutable` and `constexpr` are allowed. Without a lambda-declarator it is as if `()` were written; the return type is `auto` (a trailing-return-type, or deduction from `return` statements per `[dcl.spec.auto]`). Part of [[cpp17-expressions]].

## Closure type (`[expr.prim.lambda.closure]`)

- A unique, unnamed, non-union, **non-aggregate** class type declared in the smallest enclosing block, class or namespace scope. Implementations may differ from the described layout only in size/alignment and whether the type is trivially copyable, standard-layout or POD; they must not add rvalue-reference members.
- **Function call operator:** public, inline, non-virtual, non-volatile; declared `const` unless the lambda is `mutable`. A *generic* lambda (any `auto` parameter) gets an operator *template* with one invented template parameter per `auto` (a pack if the parameter is a pack). `noexcept-specifier` and attributes in the declarator transfer to the operator. It is `constexpr` if declared so or if it satisfies the constexpr-function requirements ([[constant-expressions]]).
- **Conversion to function pointer:** a non-generic lambda with no capture converts to a pointer to function (C++ language linkage; `noexcept` pointer if the call operator is non-throwing); the pointed-to function behaves like the call operator and is `constexpr` if the operator is. Generic captureless lambdas get a conversion function template. The conversion function is public, constexpr, non-virtual, non-explicit, const and non-throwing.
- The body's name lookup, `this`, and member-access transformation are in the context of the lambda-expression; `__func__` is defined in the body.
- No default constructor, a deleted copy assignment operator, a defaulted copy constructor and defaulted move constructor, an implicitly-declared destructor. Members cannot be explicitly instantiated, specialized, or named in friend declarations.

## Captures (`[expr.prim.lambda.capture]`)

| Form | Meaning |
|---|---|
| `[&]` / `[=]` | capture-default (by reference / by copy); with `&` default no simple-capture may be `&x`; with `=` every simple-capture must be `&x` or `*this` |
| `x`, `&x` | simple-capture of an automatic-storage variable from the reaching scope |
| `this`, `*this` | capture the pointer / a copy of the object (`*this` is a copy-capture; requires a non-static member function context) |
| `x = init`, `&x = init` | **init-capture**: behaves as `auto x = init;` explicitly captured; for copy init-capture the data member and the variable are two names for one object; not allowed with an ellipsis |

Rules: an entity cannot appear twice (initializers aside); only *local* lambdas (smallest enclosing scope is a block) can capture; a simple-capture naming a parameter is ill-formed; a lambda in a default argument cannot capture anything. An entity is **implicitly captured** when the capture-default is present and the body odr-uses it (or names it in a potentially-evaluated expression dependent on a generic parameter). A captured entity is odr-used in the enclosing scope, and the lambda must capture every odr-used automatic variable or `this` from its reaching scope.

- **By copy:** an unnamed non-static data member per entity (declaration order unspecified; a bit-field or anonymous-union member can't be copy-captured); id-expressions referencing it become member accesses. `*this` copy: odr-uses of `this` become a pointer to the data member.
- **By reference:** unspecified whether extra members exist; if they do, they have literal type. A bit-field or anonymous-union member cannot be captured by reference.
- Nested lambdas: the inner capture of an entity the outer captures by copy captures the outer's data member; if by reference, the same entity.
- `decltype((x))` for a captured automatic variable `x` is computed as if `x` were the corresponding closure member.
- On evaluation, copy-captured entities and init-captures direct/copy-initialize the members in (unspecified) declaration order; arrays element-wise in increasing subscript order.
- A simple-capture followed by `...` is a pack expansion.

## Related

[[cpp17-expressions]] · [[constant-expressions]] · [[cpp17-templates]] (generic lambdas) · [[value-categories]]
