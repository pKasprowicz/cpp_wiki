---
type: concept
title: "Storage duration, object model and object lifetime"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Storage duration, object model and object lifetime

Sources: `[intro.object]` ([[cpp17-general-principles]]), `[basic.stc]`, `[basic.life]` ([[cpp17-basic-concepts]]).

## Object model basics (`[intro.object]`)

- Objects are created by definitions, new-expressions, changing a union's active member, or temporaries. An object occupies storage during construction, its lifetime, and destruction.
- **Subobjects:** member subobjects, base class subobjects, array elements. An object not contained in another is a **complete object**. A new object created in storage of a member subobject/array element `e` becomes a subobject of `e`'s container if the container's lifetime is active, the storage exactly overlays `e`, and the type matches (ignoring cv).
- An array of `unsigned char` or `std::byte` can **provide storage** for an object created in it if the array's lifetime is active, the object fits entirely, and no smaller such array qualifies. "Nested within" generalizes both relations.
- Most derived objects (complete object, data member or array element of class type, or non-class type objects) must have nonzero size unless they are bit-fields; **base class subobjects may have zero size**. Objects of trivially copyable or standard-layout type occupy contiguous bytes. Distinct objects with overlapping lifetimes have distinct addresses unless one is nested in the other or a zero-size base class is involved.

## Storage duration (`[basic.stc]`)

| Duration | Which objects | Lifetime of storage |
|---|---|---|
| static | variables that are not local, thread, or dynamic; also `static` locals and static data members | whole program |
| thread | `thread_local` variables | the thread; distinct object per thread |
| automatic | block-scope variables not `static`/`thread_local`/`extern` | until the block exits |
| dynamic | objects created by new-expressions | until deallocation |

- Static and automatic objects whose initialization or destructor has side effects may not be eliminated even if unused (except copy/move elision, see [[copy-elision-and-temporary-materialization]]).
- When storage ends, pointers to any part of it become **invalid pointer values**; indirecting through one or passing it to a deallocation function is **undefined behavior**; other uses are implementation-defined (`/4`).
- Subobjects and reference members share the duration of their complete object.
- **Dynamic allocation** (`[basic.stc.dynamic]`): the global `operator new`/`new[]` (plain and `std::align_val_t` forms) and `operator delete`/`delete[]` (plain, sized, aligned, sized+aligned) are implicitly declared in every translation unit and are replaceable (at most one definition of a replaceable function per program). An allocation function returns `void*`, takes `std::size_t` first (no default), may be a template only with ≥ 2 parameters; it must return suitably aligned storage at least as large as requested or fail by returning null (if non-throwing) or throwing something matching `std::bad_alloc`. Zero-size requests can fail; a successful one returns a distinct non-null pointer. A deallocation function terminating via exception is undefined behavior; a null first argument is allowed (no effect in the library versions). A "usual deallocation function" has 1 parameter, or 2 with the second `std::size_t`/`std::align_val_t`, or 3 (`size_t`, `align_val_t`); a template instance never is one.
- **Pointer safety** (`[basic.stc.dynamic.safety]`): "safely-derived pointers" and integer representations are defined; whether an implementation has relaxed or strict pointer safety is implementation-defined.

## Lifetime (`[basic.life]`)

- **Begins** when storage of proper size/alignment is obtained and, if initialization is non-vacuous, initialization completes (union members: only the initialized member). **Ends** when the destructor call starts (non-trivial destructor) or the storage is released or reused by a non-nested object. Reference lifetime begins after initialization and ends as for a scalar.
- A program may end an object's lifetime by reusing the storage or calling the destructor explicitly; it need not call a non-trivial destructor beforehand, but then it must not depend on the destructor's side effects (and the destructor is not implicitly called).
- **Outside lifetime but with storage still allocated**, a pointer/glvalue to the object is usable only in limited ways. Undefined behavior if: it is the operand of `delete` for a class with non-trivial destructor; used to access a non-static member or call a non-static member function; converted to a virtual base pointer / bound to a virtual base reference; used in `static_cast` (except to `cv void*`, then possibly to `char`/`unsigned char`/`std::byte` pointers) or `dynamic_cast`/`typeid`; or (glvalue) used to access the object.
- **Transparent replacement** (`/8`): after an object's lifetime ends and before its storage is reused, a new object created at the same location can be reached through the old pointer, reference or name if: storage exactly overlays; same type (ignoring top-level cv); the original is not const-qualified and (if a class) has no const-qualified or reference non-static data member; and both are most derived objects.
- If an object with static, thread or automatic duration has a non-trivial destructor, the program must ensure an object of the original type occupies the storage when the implicit destructor call occurs; otherwise undefined (even on exception exit). Creating a new object in the storage of a const complete object (static/thread/automatic) — during or after its lifetime — is undefined.
- In this section "before"/"after" mean the "happens before" relation ([[memory-model-and-data-races]]).

## Related

[[strict-aliasing]] · [[program-startup-and-termination]] · [[cpp17-special-member-functions]] (constructors/destructors, `[class.cdtor]`) · [[abstract-machine-and-observable-behavior]]
