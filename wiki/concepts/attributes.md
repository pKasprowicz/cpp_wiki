---
type: concept
title: "Attributes and alignment specifiers"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Attributes (`[dcl.attr]`)

Part of [[cpp17-declarations]].

## Syntax and general rules (`[dcl.attr.grammar]`)

- Attribute syntax is an attribute-list wrapped in two pairs of square brackets, optionally with a shared namespace prefix `using ns:` that treats each token in the list as `ns::token` (a using-prefix list may not also contain scoped tokens). `alignas(...)` is also an attribute-specifier. (This page writes attribute names without their brackets because double square brackets are this wiki's wikilink syntax.)
- An attribute may take a balanced-token argument clause in parentheses and may be followed by `...` (pack expansion) only if its specification permits it. Order within a list is not significant. No name lookup is performed on attribute identifiers; keywords count as identifiers there.
- Each attribute-specifier-seq **appertains** to the entity or statement given by syntactic position. An attribute not allowed on that entity makes the program ill-formed. A friend declaration with attributes must be a definition. Nothing may appertain to an explicit instantiation.
- Attributes not specified by the standard have implementation-defined behavior; an unrecognized attribute-token is **ignored**. Two consecutive opening square brackets may appear only to start an attribute or inside an attribute argument.

## Standard attributes

| Attribute | Applies to | Rules |
|---|---|---|
| `noreturn` | function declarator-id | the first declaration must carry it if any does; mismatch across translation units is ill-formed, no diagnostic required; if such a function actually returns, behavior is **undefined** |
| `carries_dependency` | parameters, functions | dependency propagation for memory ordering (consume); first declaration must carry it if any declaration does; cross-TU mismatch ill-formed, NDR. See [[memory-model-and-data-races]] |
| `deprecated` (optionally with a string-literal reason) | class, typedef-name, variable, non-static data member, function, namespace, enumeration, enumerator, template specialization | use still allowed but discouraged; at most once per list; may be added or removed on later redeclarations, with different message forms allowed |
| `fallthrough` | a null statement inside a `switch` | the next statement executed must be a `case`/`default` label of the same switch, else ill-formed. Its purpose (per a note) is to suppress fallthrough warnings; implementations are encouraged to warn if it is not dynamically reachable |
| `maybe_unused` | class, typedef-name, variable, non-static data member, function, enumeration, enumerator | per a note, implementations are encouraged not to warn about unused entities so marked; may be added by a later redeclaration |
| `nodiscard` | function declarator-id, class, enumeration | per a note, discarding the result of a call to such a function (or one returning a nodiscard class/enum type) is discouraged unless cast to `void`, and a warning is encouraged; a function returning a reference to a nodiscard type is *not* a nodiscard call |

All standard attributes: at most once per attribute-list, and no argument clause (except `deprecated`'s optional string).

## Alignment specifier (`[dcl.align]`)

- `alignas(constant-expression)` or `alignas(type-id)` (equivalent to `alignas(alignof(type-id))`); with `...` it is a pack expansion.
- Applies to variables, class data members (not bit-fields), classes and enumerations — **not** to function parameters or exception-declarations.
- The expression must be an integral constant expression evaluating to a valid alignment; an unsupported extended alignment is ill-formed.
- The entity's alignment is the strictest nonzero alignment among its specifiers; the combined effect must not be weaker than the natural alignment. If a defining declaration has an alignment-specifier, every other declaration must be equivalent or have none (and vice versa for defining declarations); cross-translation-unit mismatch needs no diagnostic.

## Related

[[cpp17-declarations]] · [[cpp17-statements]] (fallthrough in switch) · [[cpp17-basic-concepts]] (alignment values)
