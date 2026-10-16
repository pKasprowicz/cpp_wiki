---
type: concept
title: "Exception support library: exception, terminate, exception_ptr, nested_exception"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Exception support (`<exception>`, `[support.exception]`)

Library types and functions behind throwing and handling. The language rules are in [[cpp17-exception-handling]]; the catalogue of standard exception *classes* is on [[standard-exception-classes]]. Parent: [[cpp17-lib-language-support]].

## `std::exception` (`[exception]`)

Root of the standard hierarchy: thrown by library components and certain expressions. Every standard class derived from it has a publicly accessible, non-throwing copy constructor and copy assignment, with the postcondition that a copy has the same `what()` text (`strcmp == 0`) (`/2`). `what()` returns an implementation-defined null-terminated message that stays valid until the exception object is destroyed or a non-const member is called on it. `bad_exception` is the type referred to by the `exception_ptr` that `current_exception` returns when copying the active exception fails.

## Termination (`[exception.terminate]`)

- `terminate_handler` is `void (*)()`; a handler **must end the program without returning**; the default handler calls `abort()`.
- `terminate()` calls the current handler (which one is used when an exception is active during `set_terminate` is unspecified). It is called by the implementation for the reasons in `[except.terminate]` ([[cpp17-exception-handling]]) and may be called by the program.
- `set_terminate(f)` installs `f` and returns the previous handler (whether a null `f` designates the default is unspecified); `get_terminate()` reads it. Both are race-free (`[handler.functions]`).

## `uncaught_exceptions()` (`[uncaught.exceptions]`)

Returns the number of exceptions currently thrown but not yet caught in the current thread. While it is positive, throwing can lead to `terminate`. Used by scope-guard idioms to compare the count at construction and destruction. Annex D ([[cpp17-annex-d-compatibility-features]]) keeps the deprecated boolean `uncaught_exception()`, defined as `uncaught_exceptions() > 0` (`[depr.uncaught]`).

## `exception_ptr` and propagation (`[propagation]`)

- `exception_ptr` refers to an exception object, satisfies **NullablePointer** ([[library-named-requirements]]), default-constructs to null, and is not implicitly convertible to arithmetic, enumeration or pointer types. Two non-null values are equal iff they refer to the same exception.
- For data-race purposes, operations on `exception_ptr` touch only the pointer objects, not the exceptions; `rethrow_exception` on pointers to the same exception does not race.
- `current_exception()` returns a pointer to the currently handled exception or to a copy (null if none handled); if memory is short it refers to a `bad_alloc`; if copying throws it refers to the thrown exception or, failing that, a `bad_exception`. Whether two consecutive calls return the same object is unspecified; the referent stays valid as long as any `exception_ptr` refers to it.
- `rethrow_exception(p)` requires non-null `p` and throws the referenced object. `make_exception_ptr(e)` creates a pointer to a copy of `e` as if by throwing and catching it.

## `nested_exception` (`[except.nested]`)

A mixin class capturing `current_exception()` on construction. `rethrow_nested()` throws the stored exception (or calls `terminate()` if none is stored); `nested_ptr()` returns it. `throw_with_nested(t)`: with `U = decay_t<T>` (must be CopyConstructible), if `U` is a non-final class not already derived from `nested_exception`, throws an unspecified type publicly derived from both `U` and `nested_exception`; otherwise throws `t` itself. `rethrow_if_nested(e)` does nothing unless `e` is of polymorphic class type with an accessible, unambiguous `nested_exception` base, in which case it rethrows the nested exception.

## Related

[[cpp17-exception-handling]] · [[standard-exception-classes]] · [[error-codes-and-system-error]] · [[library-requirements-and-conformance]] (exceptions library functions may throw) · [[futures-and-async]] (uses `exception_ptr`) · [[cpp17-annex-d-compatibility-features]] (`uncaught_exception`)
