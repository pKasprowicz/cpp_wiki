---
type: concept
title: "Linkage"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Linkage (`[basic.link]`)

A program is one or more translation units linked together; a translation unit is a sequence of declarations. A name **has linkage** when it might denote the same entity as a name introduced in another scope. Part of [[cpp17-basic-concepts]].

| Linkage | The entity can be referred to from... |
|---|---|
| external | scopes of other translation units, and other scopes of the same unit |
| internal | other scopes in the same translation unit |
| none | no other scope |

## What gets internal linkage at namespace scope (`/3-4`)

- a variable, function or function template explicitly declared `static`;
- a **non-inline** variable of non-volatile `const`-qualified type that is neither explicitly `extern` nor previously declared with external linkage;
- a data member of an anonymous union;
- an unnamed namespace, or a namespace declared directly or indirectly inside one, itself has internal linkage.

Other namespace-scope variables, functions, named classes and enumerations, and templates take the linkage of the enclosing namespace: external for ordinary namespaces, internal for entities inside an unnamed namespace. Members of classes (member functions, static data members, nested named classes/enums) take the linkage of their class (`/5`).

## Block scope (`/6-8`)

Block-scope function declarations and block-scope `extern` variable declarations have linkage; they refer to a matching visible entity (innermost enclosing namespace) if one exists, otherwise they receive external linkage and become members of the innermost enclosing namespace without introducing the name there. Declaring one entity with both internal and external linkage in a unit is ill-formed. Other block-scope names have no linkage.

## Types with linkage (`/8`)

Named classes/enums whose name has linkage, unnamed ones that are members of a class with linkage, class template specializations, fundamental types, compound types built only from types with linkage, and cv-qualified versions. A type **without** linkage must not be the type of an external-linkage variable or function unless: the entity has C language linkage, is in an unnamed namespace, or is not odr-used / is defined in the same translation unit.

## Same-entity rule across scopes (`/9-10`)

Two same names in different scopes denote the same variable, function, type, template or namespace when both have external linkage (or both internal in the same unit), are members of the same namespace or non-inherited members of the same class, have identical parameter-type-lists (functions) or the same signatures (function templates). All declarations of one entity must give identical types (arrays may differ in presence of the major bound); violating this is ill-formed with **no diagnostic required**.

## Related

[[one-definition-rule]] · [[name-lookup]] · [[cpp17-declarations]] (language linkage, `inline`, `extern`)
