---
type: concept
title: "new and delete expressions"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `new` and `delete` expressions (`[expr.new]`, `[expr.delete]`)

Dynamic storage duration is covered in [[storage-duration-and-object-lifetime]]; this page covers the expression rules from [[cpp17-expressions]].

## `new` (`[expr.new]`)

- Allocates an object of a complete, non-abstract object type; returns a pointer (to the first element for arrays). A placeholder type (`auto`) in the type is deduced as for `T x init;`.
- Array form: the size expression is converted to `std::size_t`; later dimensions must be converted constant expressions that are strictly positive. A size is **erroneous** if negative, if the object would exceed the implementation limit, or if a braced initializer has more elements than the array. If erroneous and a core constant expression: ill-formed; otherwise no allocation happens and the result is null (non-throwing allocation function) or `std::bad_array_new_length` is thrown. Zero-size arrays are allowed.
- **Allocation function lookup:** with a leading `::` or a non-class type, global scope; for a class `T` (or array of `T`) look in `T`'s scope first, falling back to global. Overload resolution is performed on a call whose first argument is the size (`std::size_t`), then — for types with new-extended alignment — an `std::align_val_t` argument (dropped and retried if no match), then the placement arguments.
- **Elision:** an implementation may omit calls to the replaceable global allocation functions or merge allocations of several new-expressions provided e1 is sequenced before e2, e2 is evaluated whenever e1 gets storage, both call the same function, exceptions would be caught by the same handler, and the pointers are deleted with e2's delete sequenced before e1's.
- If the allocation function is a non-allocating form that returns null the behavior is undefined; otherwise a null return means no initialization, no deallocation call, and a null result.
- **Initialization:** no initializer → default-initialization; otherwise direct-initialization per `[dcl.init]`. The allocation call is sequenced before the initializer's expressions; initialization is sequenced before the value computation of the new-expression. If initialization throws, a matching deallocation function is called (placement deallocation matched by the same parameter list); if none is found the memory is not freed.

## `delete` (`[expr.delete]`)

- Operand: pointer to object type (class types are contextually implicitly converted). Result type `void`. `delete[]` is chosen by empty brackets.
- **Undefined behavior** unless: (non-array) the operand is null, a pointer to a non-array object from `new`, or a pointer to its base subobject; (array) null or the result of array `new`.
- Static type different from dynamic type in the non-array form: the static type must be a base with a **virtual destructor**, otherwise undefined; in the array form a differing dynamic type is undefined.
- Deleting an object of an incomplete class type with a non-trivial destructor or a deallocation function is undefined.
- Destructors run (array elements in reverse order of construction) when the operand is non-null. The deallocation function receives the allocation call's returned address (accounting for omitted/merged allocations) as first argument. If the operand is null it is unspecified whether the deallocation function is called.
- **Deallocation function selection** among several usual deallocation functions: prefer the `std::align_val_t` form for new-extended-alignment types, otherwise the one without; for class-scope functions prefer the one without `std::size_t`; for a complete type (and, for `delete[]`, a non-trivially-destructible element type) prefer the `std::size_t` form; otherwise it is unspecified whether the sized form is used. The size and alignment arguments are those of the most derived type.

## Related

[[storage-duration-and-object-lifetime]] · [[initialization]] · [[cpp17-special-member-functions]] · [[cpp17-exception-handling]]
