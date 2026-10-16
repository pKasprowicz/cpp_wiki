---
type: concept
title: "C++17 clause 13: derived classes"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 13: Derived classes (`[class.derived]`)

A short clause (about 1,700 words; 4 labelled sections) on inheritance, member lookup, virtual functions and abstract classes.

## Base classes (`[class.derived]`, `[class.mi]`)

- `base-clause`: `: [virtual|access] class-or-decltype ...opt, ...`. Each base specifier may carry attributes and may be a pack expansion. A base must be a complete class; non-type names are ignored in lookup of a base name.
- A **direct base** is named in the base-clause; **indirect** bases come from bases' bases. Base members (other than constructors) are **inherited** unless hidden; constructors can be inherited through using-declarations ([[cpp17-declarations]]).
- Any number of bases are allowed, but a class cannot be a *direct* base more than once. **Non-virtual** base occurrences each get their own subobject in the most derived object; a **virtual** base gets a single shared subobject. The allocation order of base subobjects is unspecified.
- Conversions from derived to base must refer to a unique base subobject (ambiguous bases make the conversion ill-formed) ([[cpp17-standard-conversions]]).

## Member name lookup (`[class.member.lookup]`)

Lookup happens **before** access control, and overload resolution (for functions) also happens before access control ([[name-lookup]]). The lookup set S(f, C) = (declaration set, subobject set):

1. If C declares `f` (satisfying the construct's requirements), S(f, C) is those declarations with C as subobject — done.
2. Otherwise, merge S(f, Bi) from each direct base Bi in turn:
   - if every subobject in S(f,Bi) is a base of some subobject in S(f,C) (or S(f,Bi) is empty), keep S(f,C); symmetrically replace S(f,C) with a copy of S(f,Bi);
   - else if the declaration sets differ, the merge is **ambiguous** (invalid declaration set, subobject union);
   - else the result has the shared declarations and the union of subobject sets.
3. An invalid declaration set means the program is ill-formed. Ambiguities can often be resolved by qualifying with a class name.

## Virtual functions (`[class.virtual]`)

- A class declaring or inheriting a virtual function is **polymorphic**. A function with the same name, parameter-type-list, cv-qualification and ref-qualifier as a virtual function of a base **overrides** it and is itself virtual, whether or not declared so (each function overrides itself). A virtual function with several final overriders in a most-derived object makes the program ill-formed.
- `final` on a virtual function: any overrider is ill-formed. `override` on a function that overrides nothing: ill-formed. A derived destructor overrides a virtual base destructor.
- **Covariant return types:** identical, or both pointers/lvalue references/rvalue references to classes where the base's class is the same as, or an unambiguous accessible base of, the derived return's class, with equal cv-qualification on the pointer/reference and the derived class type no more cv-qualified. The derived class must be complete at the declaration or be the class itself. The result is converted to the statically chosen overridden function's return type.
- A virtual function must be defined or pure (or both) — no diagnostic required. Explicit qualification (`Base::f()`) suppresses virtual dispatch. A deleted function cannot override a non-deleted one, nor vice versa.
- Default arguments follow the *static* type ([[cpp17-declarators]]). Access follows the declaration seen at the call ([[cpp17-member-access-control]]).

## Abstract classes (`[class.abstract]`)

A class with at least one pure virtual function whose final overrider is still pure is abstract; no objects of it can be created except as base subobjects. It cannot be a parameter type, return type, or explicit-conversion target (pointers/references are fine). A pure virtual function needs a definition only if called via the qualified-id syntax (including implicitly from a destructor). A virtual call to a pure virtual function for the object under construction/destruction from a constructor/destructor is **undefined behavior** (see [[cpp17-special-member-functions]]).

## Related

[[cpp17-classes]] · [[cast-expressions]] (`dynamic_cast`) · [[cpp17-member-access-control]] · [[grammar-declarations-and-classes]] (Annex A.9)
