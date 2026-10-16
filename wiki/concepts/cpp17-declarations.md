---
type: concept
title: "C++17 clause 10: declarations"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 10: Declarations (`[dcl.dcl]`)

About 10,000 words; 33 labelled sections. Declarators and initializers are in [[cpp17-declarators]] and [[initialization]]; attributes in [[attributes]].

## Section map

| Section | Label | Notes |
|---|---|---|
| 10 (intro) | `[dcl.dcl]` | declaration forms, `static_assert`, structured binding declarations |
| 10.1 Specifiers | `[dcl.spec]` (storage class, function, typedef, friend, `constexpr`, `inline`, type specifiers) | below |
| 10.2 Enumeration declarations | `[dcl.enum]` | below |
| 10.3 Namespaces | `[basic.namespace]` (`[namespace.def]`, `.alias`, `.udecl`, `.udir`) | below |
| 10.4 `asm` | `[dcl.asm]` | conditionally-supported, implementation-defined meaning |
| 10.5 Linkage specifications | `[dcl.link]` | below |
| 10.6 Attributes | `[dcl.attr]` | [[attributes]] |

## Declaration basics

- Declaration kinds: simple, function-definition, template-declaration, deduction-guide, explicit instantiation/specialization, linkage-specification, namespace-definition, empty-declaration, attribute-declaration, plus `asm`, namespace alias, using-declaration/directive, `static_assert`, alias-declaration, opaque-enum-declaration.
- An object declaration is also a **definition** unless it has `extern` and no initializer (`/11`); see [[one-definition-rule]].
- `static_assert(cond[, "msg"])`: `cond` is a contextually converted constant expression of type `bool`; false makes the program ill-formed and the diagnostic must include the message text. The message argument is optional.
- A declaration with an identifier-list is a **structured binding declaration** ([[structured-bindings]]); its decl-specifier-seq may contain only `auto` and cv-qualifiers.
- Each init-declarator has exactly one declarator-id and is analyzed as if declared alone.

## Specifiers (`[dcl.spec]`)

- **Storage classes:** at most one of `static`, `extern`, `mutable`, with `thread_local` combinable with `static` or `extern`. `thread_local` applies to namespace/block-scope variables and static data members (implies `static` at block scope) and must appear on all declarations of the entity. `mutable` only on non-static data members that are neither const nor references. `static` and `extern` apply to variables and functions (not parameters/class members for `extern`). Successive declarations must agree in linkage.
- **Function specifiers:** `virtual` only on the initial declaration of a non-static member function; `explicit` only on constructors and conversion functions in the class.
- **`typedef` / alias-declaration:** synonyms, not new types. Re-declaring a typedef-name to the same type is allowed in non-class scopes; to a different type is not. Alias-declarations in templates cannot define a class or enumeration. An unnamed class given a typedef name uses it for linkage purposes.
- **`constexpr`** (`[dcl.constexpr]`): on variables, variable templates, functions and function templates (all declarations of a function must carry it). A `constexpr` function or static data member is implicitly `inline`. A `constexpr` function: not virtual; literal return and parameter types; body `= default`/`= delete` or a compound statement with no `asm`, `goto`, labels, try-blocks, or definitions of non-literal, static/thread-duration or uninitialized variables. A `constexpr` constructor: no virtual bases; literal parameter types; every non-variant member and base initialized; each selected constructor is `constexpr`. If no arguments could ever yield a constant expression, ill-formed, no diagnostic required. A `constexpr` object is `const`, literal type, initialized by a constant expression. Copy elision is mandatory in constant expressions. See [[constant-expressions]].
- **`inline`** (`[dcl.inline]`): functions **and variables** (inline variables). Functions defined in a class are inline. An inline entity must be defined in every translation unit that odr-uses it, with identical definitions; the definition must not precede the first inline declaration; external-linkage inline entities have one address program-wide. Not allowed on block-scope declarations. See [[one-definition-rule]].
- **cv-qualifiers** (`[dcl.type.cv]`): modifying a const object during its lifetime is undefined (except `mutable` members); accessing a volatile-defined object via a non-volatile glvalue is undefined; the meaning of volatile access is implementation-defined.
- **`decltype(e)`** (`[dcl.type.simple]/4`): unparenthesized structured binding → the referenced type; unparenthesized id-expression or class member access → the entity's declared type; otherwise by value category: xvalue → `T&&`, lvalue → `T&`, prvalue → `T`. The operand is unevaluated; for a prvalue no temporary is materialized and the type may be incomplete. `decltype(auto)` is the placeholder form.
- **Elaborated type specifiers** (`[dcl.type.elab]`): `class X;` forward declarations and friend declarations are the only sole-constituent forms; keyword must agree with the entity's kind.
- **`auto`** (`[dcl.spec.auto]`, `[dcl.type.auto.deduct]`): placeholder for variables (needs an initializer; multiple declarators must deduce the same type), function return types (deduced from non-discarded `return` statements; all must deduce the same type; no `return` means `void`; needing the type before any non-discarded `return` has been seen is ill-formed, but afterwards the deduced type may be used in the rest of the body; not for virtual functions; redeclarations must repeat the placeholder), non-type template parameters, `new` expressions, and generic lambda parameters. Deduction uses template argument deduction rules ([[template-argument-deduction]]): `auto` becomes an invented parameter `U` (or `std::initializer_list<U>` for copy-list-initialization); `decltype(auto)` uses `decltype` rules. A braced-init-list cannot be returned from a deduced-return function.
- **Deduced class types** (`[dcl.type.class.deduct]`): `std::pair p(1, 2.0);` — a class template name as the decl-specifier is replaced via class template argument deduction ([[template-argument-deduction]]); also allowed in `new` and functional-cast expressions, nowhere else.

## Enumerations (`[dcl.enum]`)

- `enum` (unscoped) vs `enum class`/`enum struct` (scoped; identifier mandatory; underlying type `int` unless given). The underlying type is **fixed** when given explicitly or for scoped enums. An unscoped opaque declaration must give the base. A scoped enumeration cannot later be redeclared as unscoped or with a different base.
- Enumerator values: first defaults to 0; each next is previous + 1. With a fixed underlying type, enumerators have that type (initializers are converted constant expressions); otherwise the type is chosen per `/5` (initializer type, or an unspecified integral type large enough).
- Without a fixed underlying type, the underlying type is implementation-defined but must hold all enumerators and not exceed `int` unless needed. The value set is the range `bmin..bmax` (smallest bit-field that holds all enumerators), which can include values no enumerator names. With a fixed type the values are those of the underlying type.
- Unscoped enumerators are declared in the scope containing the enum; scoped ones in the enumeration's scope. Unscoped values convert to integers by integral promotion.

## Namespaces

- A namespace is a declarative region whose definition can be split across parts and translation units. `[namespace.def]`: named, unnamed and **nested** definitions — `namespace A::B { ... }` is exactly `namespace A { namespace B { ... } }`.
- **Inline namespaces:** members are usable as members of the enclosing namespace; ADL associated namespaces include both; a using-directive for the inline namespace is implicitly inserted; members can be specialized from the enclosing namespace; properties are transitive. `inline` may be added on an extension only if it was on the original definition.
- **Unnamed namespaces** behave as `namespace unique {}; using namespace unique; namespace unique { ... }` ([[linkage]]).
- A friend declaration in a non-local class that first declares an entity makes it a member of the innermost enclosing namespace, but does not make the name visible to ordinary lookup (only to ADL) ([[name-lookup]]).
- **Using-declarations** (`[namespace.udecl]`): `using using-declarator-list;` — comma-separated lists and pack expansions are allowed. Each introduces synonyms found by qualified lookup. As a member-declaration, the nominated class must be a base (a direct base for constructors; constructor using-declarations inherit constructors). Cannot name a template-id, a namespace, or a scoped enumerator. Derived-class members hide/override base ones with the same name and parameter-type-list/cv/ref; introduced base functions take part in overload resolution as if members of the derived class. Access: all introduced names must be accessible, except no access check for constructor using-declarations.
- **Using-directives** (`[namespace.udir]`): allowed in namespace and block scope (not class scope); names appear as if declared in the nearest enclosing namespace containing both the directive and the nominated namespace; transitive for unqualified lookup; ambiguity if different non-function entities are found.
- **Namespace aliases** are synonyms; may be redefined to the same namespace.

## Linkage specifications (`[dcl.link]`)

Function types, external-linkage function names and variable names have a **language linkage** ("C++" by default; "C" and "C++" required, other strings conditionally-supported). Different language linkages make function types distinct. Linkage specifications nest (innermost wins), occur only at namespace scope, and do not introduce a scope. At most one function of a given name has C linkage; same-named C-linkage functions/variables in different namespaces are the same entity. A conflicting redeclaration is ill-formed (no diagnostic required across translation units).

## Related

[[cpp17-declarators]] · [[initialization]] · [[attributes]] · [[structured-bindings]] · [[constant-expressions]] · [[one-definition-rule]] · [[linkage]] · [[cpp17-basic-concepts]] · [[grammar-declarations-and-classes]] (Annex A.6)
