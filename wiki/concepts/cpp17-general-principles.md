---
type: concept
title: "C++17 clauses 1-4: scope and general principles"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clauses 1-4: scope and general principles (`[intro]`)

On the cppwp rendering of N4659, Scope (`[intro.scope]`), Normative references (`[intro.refs]`) and Terms and definitions (`[intro.defs]`) are clauses 1-3, and **General principles** (`[intro]`) is clause 4. Clauses 1-3 are tiny (about 100-700 words each) and are summarized, with a glossary of the defined terms, on [[cpp17-glossary]]; the substance is clause 4.

## Section map of clause 4

| Section | Label | Wiki page |
|---|---|---|
| 4.1 Implementation compliance | `[intro.compliance]` | [[abstract-machine-and-observable-behavior]] |
| 4.2 Structure of this document | `[intro.structure]` | below |
| 4.3 Syntax notation | `[syntax]` | below |
| 4.4 The C++ memory model | `[intro.memory]` | [[memory-model-and-data-races]] |
| 4.5 The C++ object model | `[intro.object]` | [[storage-duration-and-object-lifetime]] |
| 4.6 Program execution | `[intro.execution]` | [[abstract-machine-and-observable-behavior]], [[sequencing-and-evaluation-order]] |
| 4.7 Multi-threaded executions and data races | `[intro.multithread]` (`[intro.races]`, `[intro.progress]`) | [[memory-model-and-data-races]] |
| 4.8 Acknowledgments | `[intro.ack]` | not summarized |

## How the document is organized (`[intro.structure]`)

- Clauses `[lex]` through `[cpp]` describe the **language**; Annex `[gram]` repeats all syntax in one place ([[cpp17-grammar-summary]]).
- Clauses `[language.support]` through `[thread]`, plus Annex `[depr]`, describe the **library**, in the form set out in `[library]`.
- Annex `[implimits]` recommends lower bounds on implementation capacity ([[implementation-quantities]]).
- Annex `[diff]` summarizes the evolution of C++ and the differences from C. `[depr]` collects compatibility-only (deprecated) features ([[cpp17-annex-d-compatibility-features]], [[deprecated-library-facilities]]).

## Syntax notation (`[syntax]`)

Syntactic categories are in italics, literal words/characters in constant width; alternatives on separate lines (or after "one of"); an `opt` subscript marks optional elements. Naming conventions for grammar categories:

- `X-name`: a use of an identifier in a context fixing its meaning (class-name, typedef-name);
- `X-id`: an identifier with no context-dependent meaning (qualified-id);
- `X-seq`: one or more X without delimiters (declaration-seq);
- `X-list`: one or more X separated by commas (identifier-list).

## Object model in one paragraph (`[intro.object]`)

Objects are created by definitions, new-expressions, changing a union's active member, or temporaries. They have a type, a storage duration, optionally a name. Objects can contain subobjects (member, base class, array element); an object that is not a subobject of another is a complete object. A complete object, data member or array element of class type is regarded as the *most derived class*, and an object of such a type (or of non-class type) is a *most derived object*. Details in [[storage-duration-and-object-lifetime]].

## Related

[[n4659-cpp17-draft-standard]] · [[abstract-machine-and-observable-behavior]]
