---
type: concept
title: "Overload resolution"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Overload resolution (`[over.match]`)

Selects the best function from a candidate set given an argument list. Comes **after** name lookup and **before** access checking ([[name-lookup]], [[cpp17-member-access-control]]). If a unique best viable function exists it is chosen; otherwise the call is ill-formed; if it is chosen but inaccessible, ill-formed (`[over.match]/3`). Part of [[cpp17-overloading]].

## Seven contexts (`[over.match]/2`)

Function call syntax; call of a class object (call operator or surrogate for conversion to function pointer/reference); operator expressions; constructor selection for default/direct initialization; user-defined conversion for copy-initialization of a class; conversion function for initializing a non-class object from a class object; conversion function yielding something a reference binds directly to. Each defines its own candidates and argument list; after that the process is identical: build the **viable** set, then pick the **best**.

## Candidates by context (`[over.match.funcs]` and subsections)

- **Implicit object parameter:** member functions get a first parameter of type "lvalue reference to cv X" (no ref-qualifier or `&`) or "rvalue reference to cv X" (`&&`); static members match any object; constructors have none. Only standard conversions apply to it. For member functions without a ref-qualifier an *rvalue can bind* even to a non-const implicit object parameter.
- **Named function call** (`[over.call.func]`): lookup finds a set of non-members or of members of one class (qualified `obj.f(...)` or unqualified inside a member, where `*this` or a contrived object is the implied argument; selecting a non-static member with a contrived object is ill-formed).
- **Class object call** (`[over.call.object]`): `operator()` members plus *surrogate call functions* for each non-explicit conversion function to pointer-to-function/reference-to-function.
- **Operators** (`[over.match.oper]`): if no operand has class or enumeration type, the built-in operator is used. Otherwise operator notation becomes function-call notation (`a@b` → `a.operator@(b)` or `operator@(a,b)`), with **member candidates** (qualified lookup in the left operand's class), **non-member candidates** (unqualified lookup plus ADL, ignoring members) and **built-in candidates** ([over.built], not for `,`, unary `&`, `->`). **The operands are still sequenced as the built-in operator prescribes** (`[over.match.oper]/2`) — so the evaluation-order rules in [[sequencing-and-evaluation-order]] hold for overloaded operators. Built-in assignment restricts conversions of the left operand (no temporaries, no user-defined conversions). If `,`, unary `&`, `->` have no viable function, the built-in meaning is used.
- **Constructors** (`[over.match.ctor]`): all constructors for direct/default init; converting constructors for copy-init.
- **Copy-init by conversion** (`[over.match.copy]`), **conversion function init** (`[over.match.conv]`), **reference binding** (`[over.match.ref]`): converting constructors / non-explicit (and, in direct-init, explicit) conversion functions of the source class and bases that yield the target (or derived).
- **List-initialization** (`[over.match.list]`): phase 1 considers only **initializer-list constructors** with the whole list as one argument; if none is viable, phase 2 considers all constructors with the list elements as arguments. An empty list with a default constructor skips phase 1. Choosing an `explicit` constructor in copy-list-initialization is ill-formed.
- **Class template argument deduction** (`[over.match.class.deduct]`): the "constructors" are function templates derived from each constructor of the primary template (template parameters of the class followed by the constructor's own, return type = the specialization), a hypothetical default constructor if none, the **copy deduction candidate** `C(C)`, and one per **deduction guide**; notional constructors inherit `explicit`-ness. See [[template-argument-deduction]].
- Function templates contribute specializations produced by template argument deduction. Defaulted-as-deleted move constructors/assignments are excluded from all candidate sets.

## Viable functions (`[over.match.viable]`)

With *m* arguments: a candidate with exactly *m* parameters is viable; fewer parameters only with an ellipsis; more parameters only if the (m+1)-th has a default argument. Each argument also needs an implicit conversion sequence to its parameter, including reference-binding constraints (non-const lvalue references can't bind rvalues; rvalue references can't bind lvalues).

## Implicit conversion sequences (`[over.best.ics]`, subsections)

- Forms: **standard** (rank Exact Match / Promotion / Conversion by the worst component, including reference binding), **user-defined** (standard + one user-defined conversion + standard), **ellipsis**. Only type, cv-qualification and value category matter; lifetime, accessibility, deletedness and bit-field-ness are ignored here, so a sequence may exist yet the final initialization be ill-formed.
- Table 13 categories: identity, lvalue transformations (lvalue-to-rvalue, array-to-pointer, function-to-pointer, qualification) and function pointer conversion are **Exact Match**; promotions are **Promotion**; other conversions (integral/floating conversions, floating-integral, pointer, pointer-to-member, boolean) are **Conversion**.
- Class argument to same-class parameter: identity; to a base: derived-to-base *Conversion* rank. Several equally good sequences → the **ambiguous conversion sequence** (treated as user-defined; fatal only if its function is chosen).
- User-defined conversions are not considered for: the first parameter of a constructor when copying a temporary (second step of class copy-initialization), the implicit object parameter, and certain list cases (`[over.best.ics]/4`).
- **List-initialization sequences** (`[over.ics.list]`): single same/derived-class element → that conversion; char array + string literal → identity; `std::initializer_list<X>` → worst element conversion; array of *N* X → worst; non-aggregate class → user-defined (or Exact Match/Conversion for a single same/derived element via a non-initializer-list constructor); aggregate → user-defined; non-class → the single element's conversion, or identity for `{}`.

## Ranking (`[over.ics.rank]`)

1. Standard better than user-defined better than ellipsis.
2. List-init: `std::initializer_list<X>` conversions beat others; a smaller array-of-*N* beats a larger one.
3. Standard sequences: a proper subsequence beats a longer one (ignoring lvalue transformations); better rank wins; for reference bindings an rvalue reference binding an rvalue beats an lvalue reference (except for implicit object parameters of unqualified member functions); lvalue ref beats rvalue ref for function lvalues; fewer cv-qualifiers in a qualification-only difference (signature a proper subset) wins; less-cv-qualified referred-to type wins.
4. Same-rank tie-breakers: conversion not to `bool` from pointer/member-pointer/`nullptr_t` beats one that is; promotion of a fixed-underlying-type enum to its underlying type beats promotion to the promoted type; `B*`→`A*` beats `B*`→`void*` and `A*`→`void*` beats `B*`→`void*`; closer base in an inheritance chain wins (pointer, reference binding, pointer-to-member, class conversions).
5. User-defined sequences are comparable only if they use the same conversion function/constructor (or initialize the same class in aggregate initialization); then the second standard conversions are compared.

## Best viable function (`[over.match.best]`)

F1 is better than F2 if for every argument ICSi(F1) is not worse than ICSi(F2) **and** one of (in order):

1. some argument has a strictly better conversion;
2. (user-defined-conversion contexts) F1's return-type standard conversion to the destination is better;
3. (direct reference binding to function reference) F1's return type is the matching kind of reference and F2's isn't;
4. F1 is a **non-template** and F2 a template specialization;
5. both templates and F1's is **more specialized** by partial ordering (`[temp.func.order]`);
6. F1 comes from a **deduction guide** and F2 doesn't;
7. F1 is the **copy deduction candidate** and F2 isn't;
8. F1 comes from a non-template constructor and F2 from a constructor template.

Exactly one function must be better than all others. If several declarations of the chosen function each supply the default argument that made it viable, the program is ill-formed. For static member functions the implicit object conversion is neither better nor worse than any other function's.

## Address of an overloaded function (`[over.over]`)

An overloaded name without arguments is resolved against the target type in: initialization, assignment left side, function/operator argument, return value, explicit conversion, non-type template argument; also with `&`. A function template name triggers deduction against the target; non-template functions beat template specializations, then more specialized templates beat less specialized; exactly one must remain.

## Related

[[cpp17-overloading]] · [[cpp17-standard-conversions]] · [[initialization]] · [[template-argument-deduction]] · [[name-lookup]]
