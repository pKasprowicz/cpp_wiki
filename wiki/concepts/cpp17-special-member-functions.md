---
type: concept
title: "C++17 clause 15: special member functions"
tags: [cpp17, language-core, standard-clause, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 15: Special member functions (`[special]`)

About 7,400 words; 16 labelled sections. The special member functions are the default constructor, copy constructor, copy assignment, move constructor, move assignment and destructor. Implicitly-declared ones are declared at the closing `}` of the class; programs may refer to but not define them. A class's **potentially constructed subobjects** are its non-static data members, non-virtual direct bases and (if the class is not abstract) virtual bases.

Temporaries and copy/move elision have their own page: [[copy-elision-and-temporary-materialization]].

## Constructors (`[class.ctor]`)

- Constructors have no names; the declarator uses the injected-class-name. Allowed decl-specifiers: `friend`, `inline`, `explicit`, `constexpr`. No return value; address cannot be taken. `const`/`volatile` semantics are **not applied** to an object under construction; they take effect when the most derived constructor ends.
- **Default constructor:** callable with no arguments. With no user-declared constructor, a non-explicit public inline defaulted one is implicitly declared. It is **defined as deleted** if: a union (or anonymous-union holder) has a variant member with a non-trivial default constructor and no default member initializer; any member without a default member initializer is a reference; a const member without initializer lacks a user-provided default constructor; all members of a const union/anonymous union are const; any potentially constructed subobject's default constructor is missing/ambiguous/deleted/inaccessible; any such subobject's destructor is deleted/inaccessible.
- **Trivial default constructor:** not user-provided, no virtual functions or virtual bases, no default member initializers, trivial bases and members.
- It is implicitly defined when odr-used or explicitly defaulted after its first declaration, and is `constexpr` if a hand-written one would qualify.
- Accessing an object (or subobject) during construction through a glvalue not derived from the constructor's `this` gives an **unspecified** value (`/14`).

## Conversions (`[class.conv]`)

User-defined conversions are constructors (without `explicit`: *converting constructors*; copy/move constructors included) and conversion functions `operator T()`. At most one user-defined conversion is applied implicitly to a value; they apply only where unambiguous, and access is checked after ambiguity resolution. A conversion function: no parameters, no defining-type-specifier or `static` specifier, never converts to the same class, a base class, or `void`; can be `explicit` (considered only for direct-initialization), inherited, virtual; a conversion function template can't have a deduced return type. A derived conversion function hides a base one only when they convert to the same type.

## Destructors (`[class.dtor]`)

- Declared `~ClassName()`; no arguments; decl-specifiers only `friend`, `inline`, `virtual`; address cannot be taken. Implicitly declared as defaulted, inline, public if absent. **Deleted** if a union-like class has a variant member with a non-trivial destructor, a potentially constructed subobject has a deleted/inaccessible destructor, or (for a virtual destructor) deallocation function lookup is ambiguous/deleted/inaccessible.
- Trivial: not user-provided, not virtual, trivial bases and members.
- Execution order: body, then destruction of automatic objects in the body, then non-variant data members, then non-virtual direct bases, then (if most derived) virtual bases — all in **reverse order of construction**, called as if qualified (no virtual dispatch). Array elements are destroyed in reverse order.
- A class with a virtual-destructor base has a virtual destructor. If a class's objects are ever created, a virtual destructor must be defined. Destructors are invoked implicitly at program termination (static), thread exit, block exit, end of temporary lifetime, and by `delete`; also explicitly. A potentially-invoked deleted/inaccessible destructor is ill-formed.
- Invoking a destructor for an object not of that class (or derived) — including through a null pointer — is **undefined**; invoking it for an object whose lifetime has ended is **undefined**.

## Free store (`[class.free]`)

Class-specific allocation and deallocation functions are implicitly static (so cannot be virtual). Class-specific `operator delete` is found in the class scope, using the virtual destructor's selection when the static type has one. Access to the deallocation function is checked statically.

## Initialization (`[class.init]`, `[class.base.init]`)

- A ctor-initializer is a `mem-initializer-list` of `id(expr-list)` or `id{init-list}` entries (possibly pack expansions), naming the class itself (delegation), direct/virtual bases, or non-static members. Naming anything else is ill-formed; duplicate entries are ill-formed.
- **Delegating constructor:** the only mem-initializer names the constructor's own class; the target constructor runs first, then the delegating body. Delegation cycles are ill-formed, no diagnostic required.
- A subobject not named in the list is initialized from its **default member initializer** if it has one (for unions/anonymous unions only if no other variant member is named), otherwise default-initialized (variant members: no initialization). More than one initialized union member is ill-formed. A mem-initializer overrides a default member initializer. Binding a temporary to a reference member (from a mem-initializer or a default member initializer) is ill-formed.
- **Order of initialization:** (1) virtual bases (most derived constructor only), depth-first left-to-right in the base-specifier-list; (2) direct bases in declaration order; (3) non-static data members in **declaration order**, regardless of mem-initializer order; (4) the constructor body. A virtual-base mem-initializer is ignored unless in the most derived class's constructor.
- Calling member functions (including virtual) during construction is allowed; if done in the ctor-initializer before all base mem-initializers complete, the behavior is **undefined**.
- **Inherited constructors** (`[class.inhctor.init]`): initialization is one function call; the inherited constructor initializes its base subobject, everything else as for a defaulted default constructor; the inherited constructor's parameters are initialized first. Inheriting from several base subobjects of type B is ill-formed.

## Construction and destruction (`[class.cdtor]`)

- Referring to a non-static member or base of an object with a non-trivial constructor before it starts, or of an object with a non-trivial destructor after it finishes, is **undefined**. Converting to a base pointer/reference, or forming a pointer to a direct member, requires construction to have started and destruction not completed.
- A virtual call from a constructor/destructor (on the object being constructed/destroyed) calls the final overrider **in the constructor's or destructor's class**, not a more-derived one; an explicit-access virtual call on a different subobject of the complete object is undefined.
- `typeid` and `dynamic_cast` during construction/destruction treat the object as of the constructor's/destructor's class (the object is a "most derived object" of that class); an operand whose static type is not that class or a base of it is undefined.

## Copy/move constructors (`[class.copy.ctor]`)

- A **copy constructor** for X: non-template, first parameter `X&`, `const X&`, `volatile X&` or `const volatile X&`, rest defaulted. A **move constructor**: first parameter `X&&` (cv variants), rest defaulted. A constructor whose first parameter is plain `X` (with others defaulted) is ill-formed; no template ever yields such a signature.
- **Implicit copy constructor:** declared if none explicitly declared; defaulted — but **deleted** if the class declares a move constructor or move assignment operator. Defaulting it is *deprecated* when there is a user-declared copy assignment or destructor. Its parameter is `const X&` if every potentially constructed subobject's copy constructor takes a const reference, else `X&`.
- **Implicit move constructor:** declared (defaulted) iff X has no user-declared copy constructor, copy assignment, move assignment or destructor.
- A defaulted copy/move constructor is **deleted** if: union-like with a variant member whose corresponding constructor is non-trivial; a subobject can't be copied/moved (ambiguous, deleted or inaccessible); a subobject's destructor is deleted/inaccessible; or (copy only) a data member has rvalue reference type. A defaulted move constructor defined as deleted is **ignored by overload resolution**.
- Trivial: not user-provided, no virtual functions or bases, trivially copyable/movable bases and members. Memberwise copy/move in base-then-member order; arrays element-wise; rvalue reference members via `static_cast<T&&>`; a union copies its object representation; virtual bases only once.

## Copy/move assignment (`[class.copy.assign]`)

- Copy assignment: non-static non-template `operator=` with one parameter of type `X`, `X&`, `const X&`, `volatile X&` or `const volatile X&`; move assignment: `X&&` variants.
- Implicit copy assignment: declared if absent; **deleted** if the class declares a move constructor/assignment, and deprecated-defaulted when a copy constructor or destructor is user-declared. Implicit move assignment: declared iff no user-declared copy constructor, move constructor, copy assignment or destructor.
- Deleted when: a union-like class with a variant member with non-trivial assignment; a const non-class or reference non-static member; or a base/member that can't be assigned (ambiguous/deleted/inaccessible). A deleted defaulted move assignment is ignored by overload resolution.
- Always hides base-class assignment operators; a using-declaration importing a base assignment operator with a derived-assignment-like signature doesn't suppress the implicit one.
- Memberwise: bases first in base-specifier order, then members in declaration order; class types via qualified `operator=`; arrays elementwise; scalars built-in. Whether virtual-base subobjects are assigned more than once is **unspecified**. `constexpr` if the class is literal and the selected member/base operators are `constexpr`.

## Related

[[cpp17-classes]] · [[copy-elision-and-temporary-materialization]] · [[initialization]] · [[storage-duration-and-object-lifetime]] · [[cpp17-declarators]] (`= default`, `= delete`) · [[cpp17-annex-d-compatibility-features]] (D.2: deprecated implicit copy definitions) · [[grammar-declarations-and-classes]] (A.10)
