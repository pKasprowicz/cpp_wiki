---
type: concept
title: "Library support for dynamic memory: operator new/delete, new_handler, launder, interference sizes"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Dynamic memory support in `<new>` (`[support.dynamic]`)

The library side of `new`/`delete` expressions ([[new-and-delete-expressions]]). Parent: [[cpp17-lib-language-support]]. For container/smart-pointer allocation see [[allocators]].

## The global allocation functions (`[new.delete]`)

`<new>` declares, in the global namespace, these families. All have `std::align_val_t` overloads (an `enum class align_val_t : size_t {}`) for over-aligned types; an invalid alignment value is undefined behavior (`[new.delete]/1`).

| Family | Called by | Notes |
|---|---|---|
| `operator new(size)`, `operator new(size, align_val_t)` | new-expression (second form for types with new-extended alignment) | **Replaceable**. Required: return non-null suitably aligned storage or throw `bad_alloc`. Default: loop — try to allocate (whether via `malloc`/`aligned_alloc` is unspecified); on failure, if the current `new_handler` is null throw `bad_alloc`, else call the handler and retry; loop ends on success or when the handler does not return |
| `operator new(size, nothrow_t)` (+ aligned) | placement-new with `std::nothrow` | **Replaceable**. Required: non-null pointer, or null; default calls the throwing form and returns null if it throws |
| `operator delete(ptr)`, `(ptr, size)`, `(ptr, align)`, `(ptr, size, align)` | delete-expression | **Replaceable**. `ptr` must be null or the result of an earlier (possibly replaced) matching `operator new` not yet invalidated; alignment/size arguments must equal those used to allocate; sized forms may be turned into unsized calls; default sized forms forward to the unsized ones; null does nothing. If a program defines the unsized form it *should* also define the sized one; if it defines the sized form it *shall* also define the unsized one (`/11`) |
| `operator delete(ptr, nothrow_t)` (+ aligned) | cleanup when a nothrow-placement constructor throws | Replaceable; default forwards to plain `operator delete` |
| `operator new[]`, `operator delete[]` (same variants) | array forms | Defaults forward to the single-object functions; array `delete[]` unsized/nothrow defaults forward to the single-object `operator delete` |
| `operator new(size, void* ptr)`, `operator new[](size, void* ptr)`, matching `operator delete(void*, void*)` | placement new | **Reserved**: a program may *not* replace these; they return `ptr` and do nothing else; the matching deletes do nothing and are called if the placement constructor throws |

The requirement "if an implementation has strict pointer safety then `ptr` must be a safely-derived pointer" appears on every deallocation function. Replacement functions must meet the *Required behavior* paragraph; they must not be `inline` ([[library-requirements-and-conformance]]).

**Data races**: the allocation functions (library and replacement), `malloc`/`calloc`/`aligned_alloc`/`realloc` and the deallocation functions/`free` must not introduce data races, and the calls affecting one unit of storage occur in a single total order in which each deallocation *happens before* the next allocation (`[new.delete.dataraces]`). See [[memory-model-and-data-races]].

## Allocation errors (`[alloc.errors]`)

- `bad_alloc` is thrown to report failure to allocate storage; `bad_array_new_length` (derived from `bad_alloc`) reports an array size that is negative or beyond an implementation limit (`[expr.new]`). Both are `exception` subclasses with an implementation-defined `what()` message ([[exception-support]]).
- `new_handler` is `void (*)()`. A handler must do one of: make more storage available and return; throw `bad_alloc` or a derived class; terminate without returning (`[new.handler]/2`). `set_new_handler(p)` installs `p` and returns the previous one; **the initial handler is null**; `get_new_handler()` reads it. These are race-free (`[handler.functions]`).

## `std::launder` (`[ptr.launder]`)

`template<class T> constexpr T* launder(T* p) noexcept` returns a pointer to the object located at the address `p` holds. Preconditions: an object `X` within its lifetime, whose type is similar to `T`, is at that address, and every byte reachable through the result is reachable through `p` (reachable = within the object, a pointer-interconvertible object, or the enclosing array). It may appear in a constant expression when its argument may; ill-formed if `T` is a function type or cv `void` (`/1-3`). It is the library tool for getting a usable pointer to a new object created in reused storage; see [[storage-duration-and-object-lifetime]] and [[strict-aliasing]].

## Hardware interference sizes (`[hardware.interference]`)

`hardware_destructive_interference_size` is the minimum recommended offset between concurrently accessed objects to avoid contention slowdowns; `hardware_constructive_interference_size` is the maximum recommended size of contiguous memory for two objects accessed together with temporal locality. Both are `inline constexpr size_t`, implementation-defined, and at least `alignof(max_align_t)`.

## Related

[[cpp17-lib-language-support]] · [[new-and-delete-expressions]] · [[storage-duration-and-object-lifetime]] · [[allocators]] · [[uninitialized-memory-algorithms]]
