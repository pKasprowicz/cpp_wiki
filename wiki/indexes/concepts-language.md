---
title: "Index shard: concepts — core language (clauses 4-19, Annex C)"
---
# Index shard: concepts — core language (clauses 4-19, Annex C)

One line per page. Part of the sharded index; start from [[n4659-cpp17-draft-standard]] for the clause map or from `wiki/index.md` for the shard directory. Library pages are in the three `concepts-library-*` shards.

## Standard clauses (one overview page per language clause)

- [[cpp17-general-principles]] — Clauses 1-4: how the standard is organized, grammar notation, pointers to the abstract-machine, memory-model and object-model pages.
- [[cpp17-lexical-conventions]] — Clause 5: character sets, tokens, identifiers and reserved names, keywords, operators.
- [[cpp17-basic-concepts]] — Clause 6: entities, declarations vs. definitions, scope, lookup, linkage, startup, storage duration, lifetime, types, value categories, alignment.
- [[cpp17-standard-conversions]] — Clause 7: conversion sequences, promotions, qualification and function-pointer conversions, integer rank.
- [[cpp17-expressions]] — Clause 8: general expression rules, usual arithmetic conversions, per-operator rules and undefined behavior.
- [[cpp17-statements]] — Clause 9: conditions, if/switch with init-statement, `if constexpr`, loops, range-for expansion, jumps, block-scope statics.
- [[cpp17-declarations]] — Clause 10: specifiers, `constexpr`/`inline` (incl. variables), `auto`/`decltype`, enums, namespaces, using, linkage specs.
- [[cpp17-declarators]] — Clause 11: declarator meaning, references, arrays, function types (noexcept in type), default arguments, `= default`/`= delete`.
- [[cpp17-classes]] — Clause 12: class members, static/bit-field members, unions, anonymous unions, local classes, layout categories.
- [[cpp17-derived-classes]] — Clause 13: bases, member lookup merge rules, virtual functions and covariance, abstract classes.
- [[cpp17-member-access-control]] — Clause 14: private/protected/public, base accessibility, friends, protected-member check.
- [[cpp17-special-member-functions]] — Clause 15: constructors, destructors, implicit declaration/deletion rules, copy/move, construction-order and virtual calls.
- [[cpp17-overloading]] — Clause 16: what can be overloaded, operator functions, literal operators, built-in operator candidates.
- [[cpp17-templates]] — Clause 17: parameters, arguments, class/function/alias/variadic templates, partial specialization, friends.
- [[cpp17-exception-handling]] — Clause 18: throw, unwinding, handler matching, noexcept specifications, terminate.
- [[cpp17-preprocessing-directives]] — Clause 19: conditional inclusion, `__has_include`, macros, `#`/`##`, predefined macros, `__cplusplus` = 201703L.
- [[cpp17-compatibility-differences]] — Annex C hub: map of C.1-C.5 plus C.3-C.4, the incompatibilities with C++11/C++14 (trigraphs, `register`, `auto{}` , noexcept in type, aggregates). C.1 and C.2 are in [[concepts-glossary-grammar-annexes]]; C.5 is on [[library-requirements-and-conformance]].

## Execution model

- [[abstract-machine-and-observable-behavior]] — Abstract machine, implementation-defined/unspecified/undefined, observable behavior, conformance and forward progress.
- [[sequencing-and-evaluation-order]] — Sequenced-before, full-expressions, unsequenced conflicts, per-operator ordering table.
- [[memory-model-and-data-races]] — Memory locations, happens-before family, data races, progress guarantees.
- [[storage-duration-and-object-lifetime]] — Object model, four storage durations, allocation/deallocation functions, lifetime start/end and reuse rules.
- [[program-startup-and-termination]] — `main`, static vs. dynamic initialization ordering, termination order, `exit`/`abort`.
- [[strict-aliasing]] — The type-based access rule for glvalues and related byte-copy and pointer-interconvertibility facts.

## Names, linkage and the ODR

- [[translation-phases]] — The nine phases of translation (incl. template instantiation and linking).
- [[name-lookup]] — Scope kinds, point of declaration, unqualified, qualified and argument-dependent lookup, hiding.
- [[one-definition-rule]] — Declaration vs. definition, odr-use, which entities may be defined in several translation units and under what conditions.
- [[linkage]] — External/internal/no linkage rules, types with linkage, block-scope declarations.

## Expressions and conversions

- [[literals]] — Integer/character/floating/string/boolean/pointer literals, types, raw strings, user-defined literals.
- [[value-categories]] — glvalue/prvalue/xvalue/lvalue/rvalue taxonomy and result objects.
- [[cast-expressions]] — `static_cast`, `reinterpret_cast`, `const_cast`, `dynamic_cast`, C-style and functional casts.
- [[new-and-delete-expressions]] — `new`/`delete` semantics, allocation function lookup, elision, deallocation function selection.
- [[lambda-expressions]] — Closure types, captures (incl. `*this`, init-captures), generic and constexpr lambdas.
- [[constant-expressions]] — Core constant expressions, converted constant expressions, `constexpr` requirements.
- [[copy-elision-and-temporary-materialization]] — Prvalue result objects, remaining optional elisions, move-on-return, temporary lifetime rules.

## Declarations and initialization

- [[initialization]] — Zero/default/value/copy/direct/list initialization, aggregates (with bases), references, narrowing, indeterminate values.
- [[attributes]] — Attribute syntax, standard attributes (`noreturn`, `deprecated`, `fallthrough`, `maybe_unused`, `nodiscard`), `alignas`.
- [[structured-bindings]] — `auto [a, b] = ...`: array, tuple-like and public-member cases.

## Overloading and templates

- [[overload-resolution]] — Candidate sets per context, viability, conversion-sequence ranking, best-function tie-breakers.
- [[template-argument-deduction]] — Deduction from calls and types, SFINAE, partial ordering, class template argument deduction and guides.
- [[dependent-names-and-instantiation]] — Two-phase lookup, dependent types/expressions, instantiation points, explicit instantiation and specialization.
- [[fold-expressions]] — Unary and binary folds, allowed operators, empty-pack values.
