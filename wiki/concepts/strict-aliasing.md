---
type: concept
title: "Type-based access rule (strict aliasing)"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Type-based access rule, informally "strict aliasing" (`[basic.lval]/8`)

The standard does not use the term "strict aliasing"; the rule is stated in the section on value categories ([[value-categories]]).

**Rule:** if a program accesses the stored value of an object through a glvalue of a type *other than* one in the list below, the behavior is **undefined**.

Permitted access types for an object with dynamic type D:

1. D itself;
2. a cv-qualified version of D;
3. a type *similar* to D (the "similar types" notion comes from the qualification-conversion rules, see [[cpp17-standard-conversions]]);
4. the signed or unsigned type corresponding to D;
5. the signed or unsigned type corresponding to a cv-qualified version of D;
6. an aggregate or union type that includes one of the above among its elements or non-static data members (recursively, including sub-aggregates and contained unions);
7. a (possibly cv-qualified) base class type of D;
8. `char`, `unsigned char`, or `std::byte`.

## Related facts

- Trivially copyable types may be copied byte-wise into an array of `char`/`unsigned char`/`std::byte` and back, and the object keeps its value (`[basic.types]/2-3`).
- Pointer-interconvertible objects (same object; standard-layout union and its member; standard-layout class and its first non-static data member or first base) have the same address and can be converted via `reinterpret_cast` (`[basic.compound]/4`).
- Accessing objects outside their lifetime is a separate source of undefined behavior: [[storage-duration-and-object-lifetime]].

## Related

[[value-categories]] · [[cpp17-basic-concepts]] · [[abstract-machine-and-observable-behavior]]
