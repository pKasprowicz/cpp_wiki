---
type: concept
title: "C++17 clause 12: classes"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 12: Classes (`[class]`)

About 4,800 words; 14 labelled sections.

## Class names and definitions (`[class]`, `[class.name]`)

- A **class-specifier** (`class-key [attributes] [class-head-name] [final] [base-clause] { member-specification }`) defines a class; omitting the name makes an **unnamed class**. `class-key` is `class`, `struct` or `union`.
- The class name is inserted into its scope immediately after the name is seen, and also into the class's own scope as the **injected-class-name** (treated as public for access). A class is defined after the closing brace. A class marked `final` cannot be a base.
- A class definition introduces a new type. A class declaration hides any same-named declaration from an enclosing scope; if a variable, function or enumerator of the same name is declared in the *same* scope, the class can then be named only through an elaborated-type-specifier ([[name-lookup]]). Complete objects and member subobjects of class type have nonzero size.
- A typedef-name naming a class is also a class-name (cv ignored) but cannot be the identifier in a class-head.

## Class categories

| Category | Definition (paraphrased) |
|---|---|
| trivially copyable | every copy/move constructor and copy/move assignment is deleted or trivial, at least one of them non-deleted, and a trivial non-deleted destructor |
| trivial | trivially copyable and has default constructors that are all trivial or deleted, at least one non-deleted |
| standard-layout | no non-static members of non-standard-layout class or reference type; no virtual functions or virtual bases; same access control for all non-static members; no non-standard-layout bases; at most one base subobject of a given type; all non-static members declared in the same class (the class itself or one base); and no base of a type in the set M(S) (the types of "first members" recursively) |
| POD struct/union/class | trivial and standard-layout with no non-POD struct/union members |

Layout facts: non-static members with the same access control are allocated at increasing addresses; the layout across different access controls is unspecified. The **common initial sequence** of two standard-layout structs (same-position, layout-compatible members, bit-fields of equal width) defines layout-compatible classes, and a standard-layout union with an active struct member may read the common initial sequence through another struct member (`[class.mem]/23`). A standard-layout object's address equals its first non-static member's, or its first base subobject's if no members (`/24`).

## Class members (`[class.mem]`)

- Members: data members, member functions, nested types, enumerators of unscoped enums defined in the class, and member templates. No member can be added elsewhere. A member can't be declared twice (except forward-declared nested classes/class templates and opaque enums).
- Not members: friend declarations, `static_assert`, using-declarations, empty-declarations (and unnamed bit-fields).
- The class is **incomplete** in its own member-specification except inside function bodies, default arguments, noexcept-specifiers and default member initializers (including in nested classes), where it is regarded as complete. Non-static data members must have complete types.
- A default member initializer (`brace-or-equal-initializer`) is allowed only on data members and must not (directly or indirectly) cause the implicit definition of the enclosing class's default constructor or its exception specification. An `=` after a function declarator is a pure-specifier (`= 0`), otherwise an initializer.
- `extern` is not allowed on members; `thread_local` only with `static`.
- If `T` is the class name, no static member, member function, member type, member template, unscoped enumerator, or anonymous-union member may be named `T`; with a user-declared constructor, no non-static data member may be named `T`.

### Member functions (`[class.mfct]`, `[class.mfct.non-static]`, `[class.this]`)

- Defined in the class body → inline; outside → must be qualified and appear in an enclosing namespace scope; may be defined `inline`/`constexpr` outside if either declaration says so.
- Non-static member functions may be `const`, `volatile`, ref-qualified, `virtual`. Calling one on an object not of the class (or derived) type is **undefined**. An id-expression naming a non-static member is transformed to `(*this).name` inside members; unqualified names of static members, enumerators and nested types become qualified names.
- `this` has type `X*` / `const X*` / `volatile X*` / `const volatile X*` per the function's cv. A cv-qualified member function is callable only when the object expression is no more cv-qualified. Constructors and destructors can't be cv-qualified.

### Static members (`[class.static]`)

Static members need no object (`X::s`). A static member function can't be virtual or cv-qualified. A static data member is not a subobject; its in-class declaration of a **non-inline** member is not a definition (must be defined at namespace scope, qualified, with the initializer in class scope); an `inline` static data member may be defined with an initializer in the class; a `const` integral/enum non-inline member may have a constant initializer in class but needs a definition if odr-used; a `constexpr` one may be redeclared at namespace scope without an initializer (deprecated, `[depr.static_constexpr]`). Static data members are initialized/destroyed like non-local variables ([[program-startup-and-termination]]). Not `mutable`; not permitted in unnamed or local classes.

### Bit-fields (`[class.bit]`)

`identifier? : constant-expression` (integral constant expression ≥ 0; zero only for unnamed). Width may exceed the type's bits (extra bits are padding). Allocation and alignment are implementation-defined. A bit-field must have integral or enumeration type, cannot be static, can't have its address taken, and can't be bound to a non-const reference. A `bool` stored in any nonzero-width bit-field compares equal after storing.

### Nested and local classes (`[class.nest]`, `[class.local]`)

Nested class names are local to the enclosing class; members of a nested class may be defined in an enclosing namespace scope. Enclosing members get no special access to nested members, and vice versa ([[cpp17-member-access-control]]). A **local class** has the access of its enclosing function, may not odr-use automatic variables of the enclosing scope, must define its member functions inline, and cannot have static data members.

## Unions (`[class.union]`)

At most one non-static data member is **active** (its lifetime has begun and not ended). A union is as large as its largest member, may have member functions (incl. constructors/destructors) but no virtual functions or base classes, can't be a base class, and can't have reference members. **Assignment can begin a member's lifetime:** in `E1 = E2` with built-in or trivial assignment, for each union-member access in the left-hand expression whose modification would otherwise be undefined under `[basic.life]`, an object of that type is implicitly created in that storage with no initialization, ordered after both operand value computations and before the assignment. Details of `S(E)` cover member access and array subscripting of non-class/array/trivially-default-constructible types.

**Anonymous unions** (`union { ... };`): members must be non-static data members or static_asserts, no private/protected members or member functions; members are injected into the enclosing scope and must not collide there; at namespace scope must be `static`; no storage class in class scope. A *union-like class* (a union, or a class with an anonymous-union member) has *variant members*; at most one variant member of a union may have a default member initializer.

## Related

[[cpp17-derived-classes]] · [[cpp17-special-member-functions]] · [[storage-duration-and-object-lifetime]] · [[cpp17-basic-concepts]] · [[cpp17-annex-d-compatibility-features]] (D.1: redundant redeclaration of `static constexpr` members) · [[grammar-declarations-and-classes]] (Annex A.8)
