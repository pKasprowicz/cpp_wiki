---
type: concept
title: "Implementation quantities (Annex B): recommended minimum limits"
tags: [cpp17, language-core, standard-clause, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Annex B: implementation quantities (`[implimits]`)

Annex B is **informative** and about 500 words: a list of 43 quantities with a recommended minimum for each. The numbers are guidelines only and **do not determine compliance** (`[implimits]/2`). What is required elsewhere is the documentation duty in `[implimits]/1`: because computers are finite, every implementation must document its limitations where known, either as fixed limits, as a rule for computing variable limits from the available resources, or by saying that fixed limits do not exist or are unknown. The same idea appears in the glossary as *implementation limits* (`[defns.impl.limits]`, [[cpp17-glossary]]) and in the conformance rule that a conforming implementation accepts and runs a well-formed program "within its resource limits" ([[abstract-machine-and-observable-behavior]], `[intro.compliance]/2.1`). The list is open: limits may constrain quantities "that include those described below or others".

How to read the tables: "min" is the recommended minimum from the bracketed number after each quantity; spaces in the printed numbers (1 024) are thousands separators. The item number is the position in `[implimits]/2`.

## Nesting and depth

| Item | Quantity | Min | Related page |
|---|---|---|---|
| 2.1 | nesting levels of compound, iteration and selection statements | 256 | [[cpp17-statements]] |
| 2.2 | nesting levels of conditional inclusion (`#if` family) | 256 | [[cpp17-preprocessing-directives]] |
| 2.3 | pointer, array and function declarators together modifying a class, arithmetic or incomplete type in one declaration | 256 | [[cpp17-declarators]] |
| 2.4 | nesting of parenthesized expressions in a full-expression | 256 | [[cpp17-expressions]] |
| 2.18 | nesting levels of `#include` files | 256 | [[cpp17-preprocessing-directives]] |
| 2.23 | nested class definitions inside one member-specification | 256 | [[cpp17-classes]] |
| 2.36 | scope qualifications of one identifier | 256 | [[name-lookup]] |
| 2.37 | nested external (linkage) specifications | 1 024 | [[cpp17-declarations]] |
| 2.38 | recursive `constexpr` function invocations | 512 | [[constant-expressions]] |
| 2.39 | full-expressions evaluated within one core constant expression | 1 048 576 | [[constant-expressions]] |
| 2.41 | recursively nested template instantiations, counting substitution during deduction | 1 024 | [[dependent-names-and-instantiation]], [[template-argument-deduction]] |
| 2.42 | handlers per `try` block | 256 | [[cpp17-exception-handling]] |

## Identifiers, macros and source text

| Item | Quantity | Min | Related page |
|---|---|---|---|
| 2.5 | characters in an internal identifier or macro name | 1 024 | [[cpp17-lexical-conventions]] |
| 2.6 | characters in an external identifier | 1 024 | [[linkage]] |
| 2.7 | external identifiers in one translation unit | 65 536 | [[linkage]] |
| 2.8 | identifiers with block scope declared in one block | 1 024 | [[cpp17-basic-concepts]] |
| 2.10 | macro identifiers simultaneously defined in one translation unit | 65 536 | [[cpp17-preprocessing-directives]] |
| 2.13 | parameters in one macro definition | 256 | [[cpp17-preprocessing-directives]] |
| 2.14 | arguments in one macro invocation | 256 | [[cpp17-preprocessing-directives]] |
| 2.15 | characters in one logical source line | 65 536 | [[translation-phases]] |
| 2.16 | characters in a string literal after concatenation | 65 536 | [[literals]] |

## Functions, objects and declarations

| Item | Quantity | Min | Related page |
|---|---|---|---|
| 2.9 | structured bindings introduced in one declaration | 256 | [[structured-bindings]] |
| 2.11 | parameters in one function definition | 256 | [[cpp17-declarators]] |
| 2.12 | arguments in one function call | 256 | [[cpp17-expressions]] |
| 2.17 | size of an object | 262 144 | [[storage-duration-and-object-lifetime]] |
| 2.19 | case labels in a `switch` (excluding nested switches) | 16 384 | [[cpp17-statements]] |
| 2.21 | lambda-captures in one lambda-expression | 256 | [[lambda-expressions]] |
| 2.22 | enumeration constants in one enumeration | 4 096 | [[cpp17-declarations]] |
| 2.35 | initializer-clauses in one braced-init-list | 16 384 | [[initialization]] |
| 2.40 | template arguments in a template declaration | 1 024 | [[cpp17-templates]] |

## Classes

| Item | Quantity | Min | Related page |
|---|---|---|---|
| 2.20 | data members in a single class | 16 384 | [[cpp17-classes]] |
| 2.26 | direct and indirect base classes | 16 384 | [[cpp17-derived-classes]] |
| 2.27 | direct base classes of a single class | 1 024 | [[cpp17-derived-classes]] |
| 2.28 | members declared in a single class | 4 096 | [[cpp17-classes]] |
| 2.29 | final overriding virtual functions in a class, accessible or not | 16 384 | [[cpp17-derived-classes]] |
| 2.30 | direct and indirect virtual bases of a class | 1 024 | [[cpp17-derived-classes]] |
| 2.31 | static members of a class | 1 024 | [[cpp17-classes]] |
| 2.32 | friend declarations in a class | 4 096 | [[cpp17-member-access-control]] |
| 2.33 | access control declarations in a class | 4 096 | [[cpp17-member-access-control]] |
| 2.34 | member initializers in a constructor definition | 6 144 | [[cpp17-special-member-functions]] |

## Library-related

| Item | Quantity | Min | Related page |
|---|---|---|---|
| 2.24 | functions registered by `atexit()` | 32 | [[program-startup-and-termination]] |
| 2.25 | functions registered by `at_quick_exit()` | 32 | [[program-startup-and-termination]] |
| 2.43 | placeholders (`std::placeholders`, `[func.bind.place]`) | 10 | [[function-objects-and-invoke]] |

## Observations

- The list has 43 items; the five tables above cover all of them (2.1-2.43 each appear once). A value of 256 recurs for most nesting and per-construct counts; the largest recommended numbers are for evaluation inside one core constant expression (about a million full-expressions), object size (262 144) and identifier or macro counts (65 536).
- Two items restate library requirements: `atexit` and `at_quick_exit` each carry an "Implementation limits" paragraph requiring registration of at least 32 functions (`[support.start.term]/7` and `/11`), matching items 2.24-2.25. Item 2.43 (10 placeholders) is only a recommendation: the library synopsis calls the number of `std::placeholders` objects, called M there, *implementation-defined* (`[func.bind.place]`, `[functional.syn]`), without stating a minimum. See [[function-objects-and-invoke]] and [[program-startup-and-termination]].
- Items 2.38 and 2.41 (`constexpr` recursion, 512; template instantiation nesting, 1 024) are the two entries about evaluation or instantiation depth rather than the size of source text or of a declaration.

## Related

[[cpp17-glossary]] (implementation limits) · [[cpp17-general-principles]] (the annex is listed in `[intro.structure]`) · [[n4659-cpp17-draft-standard]]
