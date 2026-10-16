---
type: concept
title: "std::unique_ptr and default_delete"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `unique_ptr<T, D>` (`[unique.ptr]`)

Sole-ownership smart pointer. Parent: [[cpp17-lib-utilities]]. Shared ownership: [[shared-ptr-and-weak-ptr]].

## Ownership model (`[unique.ptr]/1-5`)

A unique pointer `u` stores a pointer `u.p` to an object it *owns* and a deleter `u.d` that disposes of it when `u` is destroyed or reset. Ownership can be transferred; afterwards the source's pointer is `nullptr` and any deleter state has moved to the target. A `unique_ptr` is MoveConstructible and MoveAssignable but **not** Copy-anything. The template parameter `T` **may be an incomplete type** (but `default_delete` needs `T` complete when `operator()` is instantiated, else ill-formed).

## Deleter and pointer type (`[unique.ptr.single]/1-3`)

- `D` must be a function object type, an lvalue reference to function, or an lvalue reference to function object, such that `d(ptr)` disposes of the pointer. A non-reference `D` must be `Destructible`.
- `pointer` is `remove_reference_t<D>::pointer` if that names a type (so deleters can define "fancy" pointer types), otherwise `T*`; it must be a `NullablePointer` ([[library-named-requirements]]).
- `default_delete<T>` calls `delete`; `default_delete<T[]>` calls `delete[]`. `default_delete<U>` converts to `default_delete<T>` only if `U*` converts to `T*` (arrays: `U(*)[]` to `T(*)[]`).

## Operations (`[unique.ptr.single.*]`)

| Operation | Effect |
|---|---|
| default ctor / `nullptr` ctor | empty; requires a non-throwing default-constructible `D`; excluded if `D` is a pointer type or not default-constructible |
| `unique_ptr(pointer)` | owns `p`; also excluded for pointer-type deleters. **Using it for class template argument deduction is ill-formed** |
| `unique_ptr(pointer, d)` | owns `p`; deleter initialized from `d` (signature depends on whether `D` is non-reference, `A&`, or `const A&`); if `D` is a reference, `get_deleter()` is a reference to `d` itself |
| move ctor; converting ctor from `unique_ptr<U,E>` | takes ownership; deleter moved (copied if a reference type); converting form needs `U*` convertible to `T*`, `U` not an array, and `E` convertible to `D` (or the same reference type) |
| destructor | if `get() != nullptr`, calls `get_deleter()(get())`, which must not throw |
| move/converting assignment, `= nullptr` | `reset(u.release())` then assign the deleter; `= nullptr` is `reset()` |
| `release()` | give up ownership, return the pointer, no deleter call |
| `reset(p)` | store `p`, then call the deleter on the *old* pointer if non-null |
| `swap` | swaps pointers and deleters |
| `operator*`, `operator->`, `get()`, `get_deleter()`, `explicit operator bool` | observers; deref requires non-null |

## The array form `unique_ptr<T[], D>` (`[unique.ptr.runtime]`)

`T` must be complete. Differences: default deleter is `delete[]`; `operator[]` replaces `*`/`->`; conversions that would be invalid for pointer-to-array types, or to/from the non-array form, are ill-formed; constructors and `reset` **reject pointers to derived types** (only `pointer`, `nullptr_t`, or compatible `V*` where `V(*)[]` converts to `T(*)[]`).

## Creation and comparison

- `make_unique<T>(args...)` is `unique_ptr<T>(new T(forward<Args>(args)...))`, only for non-array `T`. `make_unique<T>(n)` (`T` an array of unknown bound) is `unique_ptr<T>(new remove_extent_t<T>[n]())`. The overload for arrays of known bound is deleted (`[unique.ptr.create]`).
- Comparison (`[unique.ptr.special]`): `==` and `!=` compare `get()` values; `<` etc. compare through `less<CT>` where `CT` is the common pointer type, requiring a strict weak order; comparisons with `nullptr` work through `less<pointer>`; `swap` is available if the deleter is swappable. `hash<unique_ptr>` is provided via `hash` of the pointer.

## Related

[[shared-ptr-and-weak-ptr]] · [[library-named-requirements]] · [[new-and-delete-expressions]] · [[storage-duration-and-object-lifetime]] · [[cpp17-special-member-functions]]
