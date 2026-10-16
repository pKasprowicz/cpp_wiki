---
type: concept
title: "C++17 clause 6: basic concepts"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 6: Basic concepts (`[basic]`)

The largest of the foundational language clauses (about 16,000 words of normative text; 44 labelled sections).

## Section map

| Section | Label | Wiki page |
|---|---|---|
| 6.1 Declarations and definitions | `[basic.def]` | [[one-definition-rule]] |
| 6.2 One-definition rule | `[basic.def.odr]` | [[one-definition-rule]] |
| 6.3 Scope | `[basic.scope]` | [[name-lookup]] |
| 6.4 Name lookup | `[basic.lookup]` | [[name-lookup]] |
| 6.5 Program and linkage | `[basic.link]` | [[linkage]] |
| 6.6 Start and termination | `[basic.start]` | [[program-startup-and-termination]] |
| 6.7 Storage duration | `[basic.stc]` | [[storage-duration-and-object-lifetime]] |
| 6.8 Object lifetime | `[basic.life]` | [[storage-duration-and-object-lifetime]] |
| 6.9 Types | `[basic.types]` and subsections | below |
| 6.10 Lvalues and rvalues | `[basic.lval]` | [[value-categories]], [[strict-aliasing]] |
| 6.11 Alignment | `[basic.align]` | below |

## Entities and names (opening paragraphs)

An **entity** is a value, object, reference, function, enumerator, type, class member, bit-field, template, template specialization, namespace, or parameter pack. A **name** is a use of an identifier, operator-function-id, literal-operator-id, conversion-function-id, or template-id that denotes an entity or label. Every name denoting an entity is introduced by a declaration. A **variable** is introduced by declaring an object or a reference (other than a non-static data member).

## Types (`[basic.types]`)

- **Object representation** = the `sizeof(T)` bytes (as `unsigned char`) of an object; **value representation** = the bits that hold the value (`/4`).
- **Incomplete types:** declared-but-undefined classes, some enums, arrays of unknown bound or incomplete element type, and `cv void`. Objects must not be defined with incomplete type; "array of unknown bound" and "array of N T" are different types (`/5-6`).
- **Categories** (`/9-10`): scalar (arithmetic, enumeration, pointer, pointer-to-member, `std::nullptr_t`), POD, trivially copyable, trivial, standard-layout, and **literal types** (void, scalar, reference, arrays of literal types, and class types with a trivial destructor that are closure types, aggregates, or have a non-copy/move constexpr constructor, with all members/bases literal and non-volatile).
- **Fundamental types** (`[basic.fundamental]`): `char`, `signed char`, `unsigned char` are three distinct narrow character types with the same storage; five standard signed integer types (`signed char`, `short`, `int`, `long`, `long long`, each at least as large as the previous) with corresponding unsigned types; unsigned arithmetic is modulo 2ⁿ; `wchar_t`, `char16_t`, `char32_t` are distinct types with the size/signedness of an underlying integral type; `bool`; `float`/`double`/`long double` (value representation implementation-defined); `void`; `std::nullptr_t` (same size as `void*`). Whether plain `char` is signed is implementation-defined.
- **Compound types** (`[basic.compound]`): arrays, functions, pointers, lvalue/rvalue references, classes, unions, enumerations, pointers to non-static members. A pointer value is one of: points to an object/function; points past the end of an object; null; or invalid. A past-the-end pointer behaves like a pointer to a hypothetical element `x[n]`. Two objects are **pointer-interconvertible** in the cases listed in [[strict-aliasing]].
- **cv-qualifiers** (`[basic.type.qualifier]`): `const`/`volatile` versions are distinct types with the same representation and alignment; cv on an array attaches to the element type; partial order none < const, volatile < const volatile.

## Alignment (`[basic.align]`)

An alignment is an implementation-defined integer (a power of two, value of `std::size_t`) giving the byte spacing of valid addresses. *Fundamental* alignments are ≤ `alignof(std::max_align_t)`; *extended* alignments are greater and their support is implementation-defined (a type needing one is **over-aligned**); a request for an unsupported extended alignment makes the program ill-formed. Narrow character types have the weakest alignment requirement.

## Related

[[cpp17-general-principles]] · [[cpp17-lexical-conventions]] · [[cpp17-standard-conversions]] · [[cpp17-expressions]]
