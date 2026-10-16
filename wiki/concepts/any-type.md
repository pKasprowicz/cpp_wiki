---
type: concept
title: "std::any"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `any` (`[any]`)

A type-erased container for a single value of **any copy-constructible type**, or nothing. Parent: [[cpp17-lib-utilities]]. Siblings: [[optional]], [[variant]].

## Rules (`[any.class]`, `[any.cons]`)

- An `any` stores an instance of any type satisfying the constructor requirements or has no value. Two states are equivalent if both are empty or both hold equivalent values. Access to the contained value is through the type-safe `any_cast` functions.
- The stored type `VT = decay_t<T>` must satisfy `CopyConstructible` ([[library-named-requirements]]). The converting constructor `any(T&&)` and `operator=(T&&)` are excluded when `VT` is `any` itself (or `in_place_type_t` for the constructor) or not copy-constructible.
- **Small-object optimization** is recommended (implementations *should* avoid dynamic allocation for small values) but may be applied only to types that are nothrow-move-constructible (`/3`).
- Constructors: default (empty); copy (copies the held value, throws what its copy constructor throws); move (source left valid but unspecified); `any(T&&)`; `any(in_place_type<T>, args...)` and an initializer-list form. Destructor = `reset()`.
- Assignment is strong-guarantee: copy assignment is `any(rhs).swap(*this)`; no effect if an exception is thrown. `emplace<T>(args...)` calls `reset()` first and returns a reference to the new value; if the constructor throws, the `any` is empty.
- Observers: `has_value()`; `type()` returns `typeid(T)` for a held `T`, else `typeid(void)`.

## Non-member functions (`[any.nonmembers]`)

- `make_any<T>(args...)` builds in place. `swap` exchanges states.
- `any_cast<ValueType>(operand)` (const-lvalue, lvalue, rvalue forms): with `U = remove_cv_t<remove_reference_t<ValueType>>`, returns `static_cast<ValueType>(*any_cast<U>(&operand))` (move for the rvalue form) and **throws `bad_any_cast`** if `operand.type() != typeid(remove_reference_t<T>)`. It is ill-formed unless `ValueType` is constructible from the corresponding `U` category.
- `any_cast<T>(any*)` / `(const any*)`: returns a pointer to the held object if the pointer is non-null and `type() == typeid(T)`, else `nullptr` (no throw).
- `bad_any_cast` is the exception class thrown by a failed cast ([[standard-exception-classes]]). It relies on RTTI (`typeid`): [[type-identification-rtti]].

## Related

[[cpp17-lib-utilities]] · [[optional]] · [[variant]] · [[utility-move-forward-swap]]
