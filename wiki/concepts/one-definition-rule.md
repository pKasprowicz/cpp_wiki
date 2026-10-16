---
type: concept
title: "One-definition rule (ODR)"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# One-definition rule (`[basic.def.odr]`)

Core statement (`/1`): no translation unit contains more than one definition of any variable, function, class type, enumeration type, or template. Part of [[cpp17-basic-concepts]].

## Declaration vs. definition (`[basic.def]`)

A declaration is a definition **unless** it is, among others: a function declaration without a body; an `extern` declaration (or linkage-specification) with no initializer or body; a non-inline static data member declared in a class; a class-name declaration; an opaque-enum-declaration; a template-parameter; a function parameter declaration (outside a function definition); a typedef or alias-declaration; a using-declaration or using-directive; a deduction-guide; a static_assert-declaration; an attribute-declaration; an empty-declaration; an explicit instantiation declaration; an explicit specialization that is not a definition. Redeclaring, outside the class, a static data member that was defined in the class with `constexpr` is also not a definition (that usage is deprecated, `[depr.static_constexpr]`). Defining an object with incomplete type is ill-formed (`[basic.def]/5`).

## ODR-use (`/2-3`)

- An expression is **potentially evaluated** unless it is an unevaluated operand (or part of one). The *set of potential results* of an expression is computed structurally (id-expression itself; through subscripting of an array operand, member access, parentheses, glvalue conditional operands, comma right operand, and constant pointer-to-member).
- A **variable** named in a potentially-evaluated expression is odr-used **unless** applying lvalue-to-rvalue conversion to it yields a constant expression not invoking non-trivial functions and the usage is only such a read (or a discarded-value expression).
- `this` is odr-used when it appears in a potentially-evaluated expression; a virtual member function is odr-used unless pure; any other function is odr-used when it is the unique lookup result or the member selected by overload resolution (exceptions for pure virtuals). Allocation/deallocation functions, assignment operators, constructors and destructors become odr-used through the constructs that implicitly call them (new/delete expressions, constructor/destructor definitions, implicit copy/move, potentially invoked destructors).

## Whole-program requirements

| Entity | Requirement |
|---|---|
| non-inline function/variable that is odr-used (outside a discarded statement) | exactly one definition in the program; **no diagnostic required** (`/4`) |
| inline function/variable | defined in **every** translation unit in which it is odr-used (outside a discarded statement) (`/4`) |
| class used in a way requiring completeness | exactly one definition in that translation unit (`/5`) |

## Entities that may have several definitions (`/6`)

Class types, enumeration types, inline functions and inline variables with external linkage, class templates, non-static function templates, static data members and member functions of class templates, and template specializations with unspecified parameters may be defined in more than one translation unit (one per unit) **provided** every definition D satisfies:

1. same token sequence;
2. corresponding names (looked up per [[name-lookup]]) denote an entity defined within D or the same entity after overload resolution and partial-specialization matching, with two exceptions — a non-volatile `const` object with internal/no linkage that has the same literal type, a constant initializer, the same value, and is not odr-used in any definition; and a reference with internal/no linkage initialized by a constant expression naming the same entity everywhere;
3. same language linkage for corresponding entities;
4. overloaded operators, implicit conversion-function/constructor calls, and `operator new`/`delete` resolve to the same function (or one defined within D);
5. default arguments used by calls are treated as if present in D, recursively;
6. for a class with an implicitly-declared constructor, the implicit definition in each unit calls the same subobject constructor.

For templates the same requirements cover non-dependent names from the enclosing scope and dependent names at the point of instantiation. If all hold, behavior is as if there were one definition; otherwise the behavior is **undefined**.

## Related

[[linkage]] · [[name-lookup]] · [[cpp17-declarations]] (inline variables, `[dcl.inline]`) · [[translation-phases]]
