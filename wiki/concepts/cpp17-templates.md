---
type: concept
title: "C++17 clause 17: templates"
tags: [cpp17, language-core, standard-clause, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 17: Templates (`[temp]`)

The largest language clause (about 19,000 words; 51 labelled sections). Name resolution and instantiation are in [[dependent-names-and-instantiation]]; deduction in [[template-argument-deduction]]; fold expressions in [[fold-expressions]].

## Section map

| Section | Label | Where summarized |
|---|---|---|
| 17.1 Template parameters | `[temp.param]` | below |
| 17.2 Names of template specializations | `[temp.names]` | below |
| 17.3 Template arguments | `[temp.arg]` | below |
| 17.4 Type equivalence | `[temp.type]` | below |
| 17.5 Template declarations | `[temp.decls]` (class, member, variadic, friend, partial specialization, function, alias templates) | below |
| 17.6 Name resolution | `[temp.res]` | [[dependent-names-and-instantiation]] |
| 17.7 Instantiation and specialization | `[temp.spec]` (implicit, explicit instantiation, explicit specialization) | [[dependent-names-and-instantiation]] |
| 17.8 Function template specializations | `[temp.fct.spec]` (explicit args, deduction, overload) | [[template-argument-deduction]] |
| 17.9 Deduction guides | `[temp.deduct.guide]` | [[template-argument-deduction]] |

## Basics (`[temp]`)

- `template < params > declaration`: declares or defines a function, class, or variable (variable templates; a class-scope one is a static data member template), a member of a class template, a member template, a deduction guide, or an alias. Only at namespace or class scope. Declarators: at most one; none for a class template. The declarator-id of a function template can't end in a template-id.
- A template name has **linkage**; specializations of an internal-linkage template are distinct from those in other translation units. Templates can't have C linkage. Templates must obey the ODR ([[one-definition-rule]]).
- A class template name must be unique in its scope; function templates may overload with non-template functions and other function templates.
- A **templated entity** is a template, anything defined or created inside one, a member of one, an enumerator of a templated enumeration, or a closure type of a lambda in one.
- A function template / member function of a class template / variable template must be defined in every translation unit where it is implicitly instantiated unless explicitly instantiated elsewhere; no diagnostic required.

## Template parameters (`[temp.param]`)

- Kinds: type (`class`/`typename` — no difference), non-type, template template. Packs via `...`.
- **Non-type parameter types** (cv ignored at top level): integral or enumeration; pointer to object or function; lvalue reference to object or function; pointer to member; `std::nullptr_t`; or a type containing a **placeholder** (`auto`, `decltype(auto)`) — deduced from the argument. Not floating-point, class or `void`. Arrays/functions adjust to pointers. A non-reference non-type parameter is a prvalue that can't be modified or have its address taken.
- **Default template arguments:** allowed for any non-pack parameter in template declarations (not in out-of-class member definitions, not on friend class templates; a friend function template with defaults must be the only declaration and a definition); merged across declarations like function defaults; one parameter can't get defaults from two declarations. After a defaulted parameter, every later parameter of a class/variable/alias template needs a default or must be a pack. A primary class/variable/alias template's pack must be last; in a function template a pack may be followed only by deducible or defaulted parameters; deduction-guide parameters without defaults must be deducible.
- Parsing: the first non-nested `>` ends a template-parameter-list/argument-list; `>>` closes two lists.

## Naming specializations and arguments (`[temp.names]`, `[temp.arg]`)

- After lookup finds a template name, a following `<` is always a template-argument-list delimiter. Inside dependent contexts, a member template of an unknown specialization needs `template` prefix (`x.template f<int>()`). A type-id/expression ambiguity in an argument resolves to a type-id.
- An empty list still needs `<>` (when deduction/defaults suffice); an overloaded function template's non-matching entries are ignored.
- **Type arguments:** a type-id. **Non-type arguments:** a **converted constant expression** of the parameter's type; for pointer/reference parameters the value may not be a subobject, a temporary, a string literal, a `typeid` result, or `__func__`. **Template template arguments:** the name of a class template or alias template (only primary templates considered; partial specializations still apply on instantiation); a template matches a template template-parameter P when P is at least as specialized as it (via a rewrite into function templates); packs match zero or more.
- Template arguments are accessibility-checked at the point of use; the template gets no special access.

## Type equivalence (`[temp.type]`)

Two template-ids denote the same entity if they name the same template and have the same type arguments, identical integral/enumeration values, the same object/function/member for pointer, pointer-to-member and reference arguments (or both null), and the same template for template template arguments. Dependent `decltype` types match only when their expressions are equivalent.

## Class templates and members (`[temp.class]`, `[temp.mem]`)

- Out-of-class member definitions are templates with the class template's parameters (names may differ). A member template defined outside needs both parameter lists. Members: functions, classes, enumerations, static data members, member templates.
- A **member template**: cannot be in a local class (unless a closure), cannot be a destructor, cannot be `virtual`; a specialization never overrides a virtual function. A non-template member is preferred to a member template of the same name and type unless explicit template arguments are given. **Conversion function templates** aren't found by name; every visible one is tried with deduction against the target ([[template-argument-deduction]]).
- **Friends** (`[temp.friend]`): a friend template declares all its specializations friends; a function-template friend may be defined in a class; a friend class template may not be defined; no friend templates in local classes; friend declarations can't declare partial specializations; a friend naming a function-template specialization can't have default arguments or `inline`. Names of friends of class template specializations are injected as if declared at the point of instantiation but remain visible only to ADL (`[temp.inject]`).
- **Alias templates** (`[temp.alias]`): `template<...> using A = type-id;` — a specialization is equivalent to the substituted type; dependent ones keep substituting; an alias can't refer to itself; alias templates cannot be partially or explicitly specialized.

## Variadic templates (`[temp.variadic]`)

A **pack expansion** is a pattern plus `...` that instantiates the pattern once per pack element. Contexts: function parameter pack; using-declaration; template parameter pack that is itself an expansion; initializer-list; base-specifier-list; base mem-initializer; template-argument-list; attribute-list; alignment-specifier; lambda capture-list; `sizeof...`; fold expression. All packs in one expansion must have equal length; a pack name outside an expansion is ill-formed; only the innermost expansion expands a name. An empty expansion doesn't change the syntactic interpretation of the enclosing construct. `sizeof...(P)` gives the element count.

## Partial specialization of class templates (`[temp.class.spec]`)

- Declared as `template<params> class X<args>`; the primary must be declared first; a partial specialization must be declared before the first use that would instantiate through it (NDR). It is a distinct template with its own members (the primary's member definitions are never reused). Not found by name lookup; all declared partial specializations are considered when the primary name is used.
- Restrictions: a specialized non-type argument's parameter type can't depend on other parameters; the specialization must be **more specialized** than the primary; no default template arguments; no unexpanded packs; a pack expansion argument must be last.
- **Matching:** collect specializations whose arguments can be deduced from the actual arguments; exactly one → use it; several → pick the most specialized (partial ordering by rewriting to function templates), else ambiguous (ill-formed); none → primary.

## Function templates (`[temp.fct]`, `[temp.func.order]`, `[temp.over.link]`)

- A non-template function is never a specialization of a function template even if names and types agree; function templates overload with each other and with non-templates. Expressions involving template parameters in signatures are part of the signature; equivalent vs. *functionally equivalent* but non-equivalent declarations are ill-formed, NDR.
- **Partial ordering** (`[temp.func.order]`) is used in overload resolution, address-of, placement-delete matching, and friend/explicit-instantiation/specialization matching: synthesize unique types for each template's parameters, substitute into its function type, deduce against the other ([[template-argument-deduction]]). A non-static member is given a synthesized first parameter (lvalue or rvalue reference to the class).

## Related

[[dependent-names-and-instantiation]] · [[template-argument-deduction]] · [[overload-resolution]] · [[lambda-expressions]] (generic lambdas) · [[cpp17-declarations]] · [[grammar-declarations-and-classes]] (Annex A.12)
