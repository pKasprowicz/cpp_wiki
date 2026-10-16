---
type: concept
title: "Template argument deduction (functions, partial ordering, deduction guides)"
tags: [cpp17, language-core, cross-cutting, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Template argument deduction (`[temp.deduct]`, `[temp.deduct.guide]`)

Part of [[cpp17-templates]] (sections 17.8-17.9). Feeds overload resolution ([[overload-resolution]]): for each function template, deduction plus explicit/default arguments yields at most one specialization added to the candidate set; failure (or an ill-formed specialization) removes it (`[temp.over]`).

## Explicit arguments and substitution (`[temp.arg.explicit]`, `[temp.deduct]/2-8`)

- Explicit template arguments may be given in calls, address-of, explicit specializations/instantiations and friend declarations. Trailing deducible/defaulted arguments may be omitted; all omitted → `<>` itself optional. Explicit arguments must match in kind; extra arguments only if a pack exists; deduction can extend a pack beyond explicit arguments. A trailing undeduced pack becomes empty.
- Explicit arguments are substituted first; parameter-type adjustments then apply; deduced and defaulted arguments are substituted at the end. Defaults use previously determined arguments.
- **SFINAE:** substitution in all types and expressions of the function type and parameter declarations proceeds in lexical order; if it produces an invalid type or expression (one that would be ill-formed with a required diagnostic), deduction **fails** rather than the program being ill-formed — but only for the **immediate context** of the function type and its template-parameter types. Examples of failures: non-class type in a qualified name; missing member/type/template/non-type in a nested-name-specifier; pointer to reference; reference to `void`; pointer to member of a non-class; invalid conversion in a template argument or function-declaration expression; function type with a `void` parameter or an array/function return type; abstract class by value.

## From a function call (`[temp.deduct.call]`)

Compare each parameter type P with the argument type A:

1. If P is not a reference: arrays become pointers, functions become function pointers, top-level cv of A dropped. If P is cv-qualified, drop its top-level cv. If P is a reference, use the referred type.
2. **Forwarding reference** (the standard's term): an rvalue reference to a cv-unqualified *template parameter of the function template* (not a class template's during class template argument deduction). If the argument is an lvalue, `A&` replaces A.
3. The deduced A must be identical to A, except: a reference parameter may deduce a more cv-qualified A; a pointer/pointer-to-member A may convert to the deduced A by function-pointer and/or qualification conversion; a `simple-template-id` class P (or pointer to one) may match a derived class of the deduced A. These alternatives apply only if ordinary deduction fails and must produce a unique result.
4. **Initializer lists:** for `std::initializer_list<P'>` or `P'[N]` and a non-empty braced list, deduce from each element (and `N` from the length); otherwise a braced-init-list makes the parameter non-deduced.
5. A trailing function parameter pack is deduced from all remaining arguments.
6. A function-type/overload-set argument: with any function template in the set, non-deduced; otherwise trial deduction per member and use it only if exactly one succeeds.
7. After deduction, parameters whose types were non-dependent before substitution are checked for implicit convertibility; failure fails deduction.

Other forms: address of a function template (`[temp.deduct.funcaddr]`; a placeholder return type is non-deduced); conversion function templates (`[temp.deduct.conv]`, P = the conversion's return type against the required type, with extra allowances for `noexcept` function pointers and qualification conversions); explicit specialization/instantiation/friend matching (`[temp.deduct.decl]`).

## Deducing from a type (`[temp.deduct.type]`)

Each P/A pair is deduced independently; results must agree; a template argument neither deduced nor explicit fails the deduction. Deducible forms are the compositions of: `T`, `cv T`, `T*`, `T&`, `T&&`, `T[N]`, `template-name<T>`, function types `T(U)`, pointer-to-member shapes, `TT<T>`, and non-type `i` in `A<i>` / `type[i]` (the type of `N` in `T[N]` is `std::size_t`; a mismatched non-type parameter type fails).

**Non-deduced contexts:** the nested-name-specifier of a qualified type; the expression of a `decltype`; a non-type argument or array bound with a subexpression referencing a template parameter; a parameter with a default argument that is being used; a function/overload-set argument that is ambiguous, unmatched or contains templates; a braced-init-list argument without a deduction rule; a function parameter pack that doesn't end the parameter list. A pack expansion that is not last in a template argument list makes the whole list non-deduced. A template type parameter is never deduced from a default argument.

## Partial ordering (`[temp.func.order]`, `[temp.deduct.partial]`)

Used to choose the more specialized template. Each template's parameters are replaced by unique synthesized types/values/templates; deduction is attempted both ways using parameter types for which the call has arguments (or return types for conversions, or the whole function type elsewhere). References are stripped (tracking whether both were references and which is more cv-qualified); top-level cv removed. If deduction succeeds both ways on identical types: an lvalue-reference argument-template type beats a non-lvalue one; the more cv-qualified one beats the less. F is more specialized than G if F is at least as specialized for every compared type and G is not. Tiebreak: with a trailing pack in G and none in F, F is more specialized. Parameters not used in the compared types may stay without a value.

## Class template argument deduction and deduction guides

- A class template name used as a placeholder (`std::pair p(1, 2.0);`, `new X(...)`, `X(...)` casts, or a variable/`auto`-like declaration — see [[cpp17-declarations]]) is resolved by overload resolution over **notional constructors** (`[over.match.class.deduct]`): per constructor a function template (class parameters then constructor parameters; return type the specialization), a default-constructor candidate if the class has none, the copy deduction candidate, and one per deduction guide ([[overload-resolution]]). The return type of the selected function replaces the placeholder. All declarators in one declaration must deduce the same type.
- **Deduction guide** (`[temp.deduct.guide]`): `explicit? template-name ( parameter-declaration-clause ) -> simple-template-id ;` — not found by name lookup but considered during deduction. The parameter list obeys function-declarator rules; the simple-template-id must name a specialization of the same class template (same identifier); declared in the class template's scope (same access for member templates); two guides for one template may not have equivalent parameter lists. Guide template parameters without defaults must be deducible from its parameters. A guide declared `explicit` yields an `explicit` notional constructor (`[over.match.class.deduct]/2`), so it behaves like an explicit constructor in overload resolution.
- In an overload tie, a guide beats a constructor-derived candidate, the copy deduction candidate beats others, and a non-template constructor beats a constructor template ([overload-resolution]).

## Related

[[cpp17-templates]] · [[overload-resolution]] · [[dependent-names-and-instantiation]] · [[structured-bindings]]
