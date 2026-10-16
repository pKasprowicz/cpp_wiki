---
type: concept
title: "Scope and name lookup"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Scope and name lookup (`[basic.scope]`, `[basic.lookup]`)

Part of [[cpp17-basic-concepts]]. Lookup finds declarations; overload resolution ([[overload-resolution]]) and access checking ([[cpp17-member-access-control]]) come **after** it (`[basic.lookup]/1`).

## Scope

- Every name is introduced in a **declarative region**; its **scope** is the (possibly discontiguous) part where it can be used unqualified for the same entity. A nested declaration's region is excluded from the outer declaration's scope (`[basic.scope.declarative]`). Same-name declarations in one region must all refer to one entity or all to functions/function templates; the exception is one class or enumeration name alongside one variable/enumerator/function name, in which case the class/enum name is hidden.
- **Point of declaration** (`[basic.scope.pdecl]`): immediately after the complete declarator and before its initializer, with special cases — classes and templates (after the identifier in the class-head), enumerations (after the identifier), aliases (after the aliased type-id), enumerators (after the enumerator-definition), injected-class-names (just after the opening brace), template parameters (after the complete parameter).
- Scope kinds: **block** (`[basic.scope.block]`; includes init-statement/condition names of `if`, `while`, `for`, `switch`, local to that statement; function parameters last through the outermost block, or through the handlers of a function-try-block), **function prototype**, **function** (only labels), **namespace** (the global namespace is the outermost region), **class** (covers member function bodies, default arguments, noexcept-specifiers and NSDMIs, even those defined outside the class), **enumeration** (scoped enumerators), **template parameter**.
- **Hiding** (`[basic.scope.hiding]`): nested regions and derived-class members hide outer/base names. A name that is in scope and not hidden is *visible*.

## Unqualified lookup (`[basic.lookup.unqual]`)

Scopes are searched in the order listed for each context and lookup **stops at the first scope containing a declaration**. Names used in a class definition outside member bodies must be declared before use; names in member function bodies, default arguments, noexcept-specifiers and NSDMIs are looked up as if in the completed class. Declarations made visible by a using-directive are treated as members of an enclosing namespace of the directive (`[namespace.udir]`). Names in default arguments and mem-initializers see function parameters first; enumerator initializers see earlier enumerators.

## Argument-dependent lookup (`[basic.lookup.argdep]`)

For an unqualified function name in a call, other namespaces may also be searched, based on argument types:

| Argument type | Associated classes / namespaces |
|---|---|
| fundamental | none |
| class (or union) | the class, its enclosing class, direct and indirect bases; their innermost enclosing namespaces; for class template specializations also those of type template arguments and template template arguments |
| enumeration | innermost enclosing namespace (and enclosing class if a member) |
| pointer/array of U | those of U |
| function | those of parameter and return types |
| pointer to member | those of the member type (and the class) |

Inline namespaces add their enclosing namespace (and an associated namespace's inline children). Typedef names and using-declarations do **not** contribute. Using-directives in associated namespaces are ignored; friend functions declared in associated classes are visible; only functions/function templates are found.

**ADL is suppressed** (the ADL set is empty) when ordinary unqualified lookup finds a class member, a block-scope function declaration that is not a using-declaration, or a non-function declaration. Otherwise the result is the union of both sets.

## Qualified lookup (`[basic.lookup.qual]`)

- Before `::` in a nested-name-specifier, only namespaces, types, and templates whose specializations are types are considered.
- For a **namespace** X and name m, the lookup set S(X,m) is the declarations of m in X and its inline namespace set; only if that is empty are using-directive-nominated namespaces searched (union). Empty set: ill-formed; ambiguity: ill-formed.
- Class-qualified lookup searches the class and its bases; naming the injected-class-name (or the same name in a using-declaration) names the constructor.
- A leading `::` looks only at the global scope. A hidden class member can still be named as `Class::name`.

## Other lookups

- **Elaborated type specifiers** (`[basic.lookup.elab]`): ignore non-type names, so a class name hidden by a variable can still be named with `class X`.
- **Class member access** (`[basic.lookup.classref]`): `obj.name` first looks in the object's class; for `name <` the template-or-less-than decision is made by this lookup, falling back to the full postfix-expression context.
- **Using-directives / namespace aliases**: only namespace names are considered.

## Related

[[one-definition-rule]] · [[linkage]] · [[literals]] (UDL suffix lookup) · [[cpp17-templates]] (dependent names)
