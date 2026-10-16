---
type: concept
title: "C++17 clause 11: declarators"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 11: Declarators (`[dcl.decl]`)

About 8,200 words; 19 labelled sections. Initializers (`[dcl.init]` and subsections, section 11.6) have their own page: [[initialization]]; structured bindings (11.5): [[structured-bindings]].

## Section map

| Section | Label | Notes |
|---|---|---|
| 11.1 Type names | `[dcl.name]` | a type-id is a declaration with the name omitted |
| 11.2 Ambiguity resolution | `[dcl.ambig.res]` | anything that could be a declaration is one; anything that could be a type-id is one; a parenthesized type-name in a parameter list is a type, not a declarator-id |
| 11.3 Meaning of declarators | `[dcl.meaning]` (`[dcl.ptr]`, `[dcl.ref]`, `[dcl.mptr]`, `[dcl.array]`, `[dcl.fct]`, `[dcl.fct.default]`) | below |
| 11.4 Function definitions | `[dcl.fct.def]` | below |
| 11.5 Structured binding declarations | `[dcl.struct.bind]` | [[structured-bindings]] |
| 11.6 Initializers | `[dcl.init]` | [[initialization]] |

## Meaning of declarators (`[dcl.meaning]`)

The type of a declarator-id is computed recursively from `T D`: the decl-specifier-seq gives `T`, parentheses do not change the type but change binding. A qualified declarator-id must name a previously declared member of the class/namespace (not merely one introduced by a using-declaration). Specifiers such as `static`, `inline`, `virtual`, `constexpr` apply to each declarator-id individually.

- **Pointers** (`[dcl.ptr]`): cv-qualifiers after `*` qualify the pointer, not the pointee.
- **References** (`[dcl.ref]`): lvalue (`&`) and rvalue (`&&`) references are distinct types. A cv-qualified reference is ill-formed unless the cv comes via typedef/decltype/template parameter, where it is ignored. No reference to `void`, no references to references, arrays of references or pointers to references. A reference must be initialized (except `extern`, class members, parameters, return types). **Reference collapsing** via typedef/decltype/template: `& + &` → `&`, `& + &&` → `&`, `&& + &` → `&`, only `&& + &&` → `&&` (`/6`). Whether a reference occupies storage is unspecified.
- **Pointers to members** (`[dcl.mptr]`): cannot point to static members, reference members, or `cv void`.
- **Arrays** (`[dcl.array]`): element type not a reference, `cv void`, function, or abstract class. The bound is a *converted constant expression of type `std::size_t`* greater than zero. An omitted bound makes an incomplete type (completed by an initializer or a prior declaration). Cv-qualifiers on the array adjust to its elements. Multidimensional arrays may omit only the first bound.
- **Functions** (`[dcl.fct]`):
  - The function type is "(`noexcept`) function of (parameter-types) cv ref-qualifier returning T". The exception specification being **non-throwing is part of the function type**; default arguments are not.
  - Parameter types are adjusted: array of T / function T → pointer to T, then top-level cv is dropped when forming the function type.
  - A lone unnamed `void` parameter means no parameters; otherwise no parameter has type `cv void`. Trailing `...` or a function parameter pack allows more arguments than parameters.
  - Functions cannot return arrays or functions (pointers/references to them are fine); no arrays of functions; no types defined in return/parameter types; parameter/return types of a definition must not be incomplete class types (unless deleted).
  - cv/ref-qualified function types may appear only as non-static member function types, the target of a pointer to member, the top level of a function typedef/alias, or a type-parameter default/argument.
  - A function parameter pack is a pack expansion; `, ...` is synonymous with `...` where syntactically valid.
- **Default arguments** (`[dcl.fct.default]`): specified only in function declarations, lambda-declarators, and template-parameters (as assignment-expressions); none for parameter packs. Non-template functions may add defaults in later declarations in the same scope; each parameter after one with a default needs a default (this or earlier declaration) or must be a pack; a default may not be redefined, even to the same value. Different scopes have distinct sets. Names are bound at the point of the default argument; copy-initialization semantics. Default arguments are **evaluated on every call** that omits them. Local variables and parameters cannot appear as potentially-evaluated expressions in them; non-static members only in member access or pointer-to-member forms. Virtual calls use the defaults from the declaration found via the *static* type; overriders don't inherit defaults. Out-of-class member definitions may add defaults, except for default/copy/move constructors and copy/move assignment (ill-formed).

## Function definitions (`[dcl.fct.def]`)

- Functions are defined only in namespace or class scope. The `function-body` is `ctor-initializer? compound-statement`, a function-try-block, `= default;` or `= delete;`.
- **`__func__`**: an implicitly defined block-scope `static const char __func__[]` holding an implementation-defined string; whether its address differs from other objects is unspecified.
- **Explicitly-defaulted functions** (`[dcl.fct.def.default]`): must be a special member function with the same type as the implicit one (modulo ref-qualifiers and a non-const copy parameter), no default arguments. `constexpr` only if the implicit one would be (and implied when defaulted on the first declaration). A `noexcept` mismatch with the implicit specification: defined as deleted if defaulted on the first declaration, otherwise ill-formed. A function is *user-provided* if user-declared and not defaulted/deleted on its first declaration.
- **Deleted functions** (`[dcl.fct.def.delete]`): any use (other than declaring) is ill-formed; implicitly inline; the deleted definition must be the first declaration; an implicitly declared allocation/deallocation function can't be deleted.

## Related

[[cpp17-declarations]] · [[initialization]] · [[cpp17-special-member-functions]] · [[overload-resolution]] · [[cpp17-basic-concepts]] · [[grammar-declarations-and-classes]] (Annex A.7)
