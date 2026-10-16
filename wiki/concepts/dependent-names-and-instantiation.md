---
type: concept
title: "Dependent names, name resolution and template instantiation"
tags: [cpp17, language-core, cross-cutting, templates, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Dependent names, name resolution and instantiation (`[temp.res]`, `[temp.spec]`)

Part of [[cpp17-templates]].

## Name resolution (`[temp.res]`)

- A template definition uses three kinds of names: its own and locally declared names; names **dependent** on template parameters; and names from visible scopes.
- **Non-dependent names** are looked up and bound **at the template definition**; a declaration must be in scope there, and later declarations don't change the binding (`/10`, `[temp.nondep]`). **Dependent names** are looked up when the arguments are known (`[temp.dep.res]`).
- A dependent name is assumed **not** to name a type unless lookup finds a type or it is qualified with `typename`. A qualified-id naming a type that isn't a member of the current instantiation and whose qualifier is dependent needs `typename` (forming a typename-specifier); `typename` is implicit in class-or-decltype, base specifiers, elaborated-type-specifiers, and nested-name-specifiers. If the named entity is not a type at instantiation, the specialization is ill-formed. `typename` isn't needed for previously declared type members inside the class template itself.
- **Ill-formed, no diagnostic required** (`/8`): no valid specialization can be generated (for a template or an `if constexpr` substatement) and it isn't instantiated; every valid specialization of a variadic template needs an empty pack; a hypothetical immediate instantiation would be ill-formed due to a non-dependent construct; or the interpretation of a non-dependent construct would differ between instantiations.
- **Injected-class-name** (`[temp.local]`): inside a class template it names the current specialization when used as a type, and the template itself when followed by `<...>`, passed as a template template argument, or in a friend class template declaration. A template parameter can't be redeclared inside its scope or share the template's name; members and non-dependent base names hide template parameters in specific out-of-class contexts.

## Dependent names and types (`[temp.dep]`)

- In `f(args)` with an unqualified `f`, the name is **dependent** if any argument is a pack expansion or type-dependent, or if `f` is a template-id with dependent arguments. An operator with a type-dependent operand is likewise a dependent name. Such names are looked up in both the definition context and the instantiation context.
- The scope of a **dependent base class** is not examined by unqualified lookup, either at definition or instantiation (`/3`).
- **Current instantiation** (`[temp.dep.type]`): the injected-class-name, or the template-name with its own parameters as arguments, inside the class template, its nested classes and members (and the analogous names in partial specializations). A *member of the current instantiation* is found in that class or a non-dependent base; a *member of an unknown specialization* is a qualified-id (or member access) whose qualifier is a dependent type that isn't the current instantiation, or the current instantiation has dependent bases and lookup finds nothing. A qualified name through the current instantiation that is neither (NDR-ill-formed even if never instantiated).
- A **type is dependent** if it is a template parameter, a member of an unknown specialization, a dependent member nested class/enum, a cv/compound/array/function type built from a dependent type or value-dependent bound/exception spec, a simple-template-id with a dependent name/argument/pack expansion, or `decltype(e)` with type-dependent `e`.
- **Type-dependent expressions** (`[temp.dep.expr]`): an expression is type-dependent if any subexpression is, with exceptions: identifiers declared with a dependent type, `auto`-typed non-type parameters, deduced-return member functions, structured bindings with dependent initializers, `__func__` in templates, dependent template-ids, dependent conversion-function-ids, unknown-specialization members; casts, `new`, and functional conversions are type-dependent only if the named type is dependent; literals, `sizeof`, `alignof`, `typeid`, `delete`, `throw`, `noexcept(...)` and pseudo-destructor calls are never type-dependent. **A fold expression is type-dependent.**
- **Value-dependent expressions** (`[temp.dep.constexpr]`): names of non-type template parameters; dependent static data/member functions of the current instantiation; constants initialized by value-dependent expressions; `sizeof`/`alignof`/`typeid`/`noexcept` of type-dependent operands; `sizeof...(pack)` and fold expressions are always value-dependent; `&qualified-id` of a dependent member.
- **Dependent template arguments** (`[temp.dep.temp]`): type arguments naming dependent types; non-type arguments whose type is dependent or whose expression is value-dependent (or pointing into the current instantiation); template template arguments naming a template parameter or unknown-specialization member.

## Candidate functions for dependent calls (`[temp.dep.candidate]`)

For a call with a dependent postfix-expression: unqualified lookup considers only the **definition context**; ADL considers declarations from both the definition and instantiation contexts. If searching all declarations in all translation units would make the call ill-formed or select a better match, the behavior is **undefined**.

## Point of instantiation (`[temp.point]`)

- A function/member specialization referenced from another specialization in a dependent context has its point of instantiation at the enclosing specialization's; otherwise immediately after the namespace-scope declaration that refers to it. For class template specializations the point is immediately *before* the referencing declaration (or enclosing instantiation). Explicit instantiation definitions are instantiation points. A specialization has multiple points of instantiation within a unit, and the **end of the translation unit** is also one; a class template specialization has at most one per unit. If different points give different meanings under the ODR: ill-formed, NDR. The *instantiation context* is the external-linkage declarations preceding the point of instantiation in the same unit.

## Implicit instantiation (`[temp.inst]`)

- A class template specialization is instantiated when a complete type is required (or completeness affects semantics); member **declarations** are instantiated, but not definitions, default arguments or noexcept-specifiers (unscoped enumerations and anonymous unions are instantiated fully).
- Members, function and variable template specializations, and default arguments are instantiated only when a definition/value is required. Static data member initialization side effects don't occur unless the member is used. It is unspecified whether overload resolution that can be decided without class definitions causes instantiation. Implementations must not instantiate function templates, variable templates, member templates, non-virtual members, member classes, static data members or discarded `if constexpr` substatements unless required; virtual members are unspecified.
- Specializations go in the namespace of the template. Default arguments are instantiated independently, at each use. `noexcept-specifiers` are instantiated when needed. An implementation-defined recursion depth limit exists; **infinite recursive instantiation is undefined** (`/15`).

## Explicit instantiation (`[temp.explicit]`)

`[extern] template declaration;` instantiates a class/function/variable/member specialization; cannot use `inline` or `constexpr`; the template's declaration (or class definition) must precede it; an explicit instantiation of a class instantiates its (already defined) non-inherited, non-template members. An `extern` explicit instantiation **declaration** suppresses implicit instantiation (not for inline entities, deduced-type entities, const literal variables, reference variables, or class specializations) but then some translation unit must provide a definition (NDR). A definition occurs at most once per program. Access checking doesn't apply to names in the instantiation, and it isn't a use of default arguments.

## Explicit specialization (`[temp.expl.spec]`)

`template<> declaration` for function, class, variable templates and their members. The primary must be declared first; the specialization must be declared before the first use that would implicitly instantiate it in every unit (NDR); an implicit instantiation is never generated for a declared-but-undefined explicit specialization (using it is ill-formed, NDR). Members of an explicitly specialized class are defined without `template<>` (as normal class members) and are unrelated to the generated ones. Cannot be a friend declaration; function-template explicit specializations cannot have default arguments; an explicit specialization is `inline` only if declared so (or deleted), independent of the template. A static data member specialization is a definition only with an initializer.

## Related

[[cpp17-templates]] · [[template-argument-deduction]] · [[name-lookup]] · [[one-definition-rule]] · [[translation-phases]]
