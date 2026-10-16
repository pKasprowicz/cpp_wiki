---
type: concept
title: "Specialized memory algorithms: uninitialized_*, destroy, addressof, C allocation functions"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Specialized memory algorithms (`[specialized.algorithms]`, `[c.malloc]`)

The building blocks containers use to create and destroy objects in raw storage. Parent: [[cpp17-lib-utilities]]. Language side: [[storage-duration-and-object-lifetime]], [[new-and-delete-expressions]].

## Rules for the whole family

- Template parameters named `InputIterator`/`ForwardIterator` must satisfy those iterator categories ([[iterator-categories-and-requirements]]); a `ForwardIterator` argument additionally must not throw from increment, assignment, comparison or indirection.
- **Unless stated otherwise, an exception thrown from the algorithm leaves no effect** (already-constructed objects are destroyed). `uninitialized_move` and `uninitialized_move_n` are the exception: on a throw, some of the source objects are left valid but unspecified.
- Each non-parallel algorithm has an overload taking an `ExecutionPolicy&&` first ([[execution-policies-and-parallel-algorithms]]).

## The functions

| Function | What it does |
|---|---|
| `addressof(r)` | real address of an object or function even if `operator&` is overloaded; a constant subexpression when `r` is; the rvalue overload is deleted (`[specialized.addressof]`) |
| `uninitialized_default_construct(_n)` | default-initialize (`::new T`) each element of an uninitialized range |
| `uninitialized_value_construct(_n)` | value-initialize (`::new T()`) each element |
| `uninitialized_copy(_n)` | copy-construct from an input range into uninitialized output; returns the end of the output |
| `uninitialized_move(_n)` | move-construct from an input range |
| `uninitialized_fill(_n)` | copy-construct each element from a value |
| `destroy_at(p)`, `destroy(first, last)`, `destroy_n(first, n)` | call the destructor of each object in the range |

The construction forms use global placement new at `static_cast<void*>(addressof(*p))` with the iterator's `value_type` (so class-specific `operator new` and an overloaded `operator&` are bypassed); the `destroy` forms apply `destroy_at(addressof(*p))`; the `_n` forms return the end iterator.

## C allocation functions (`[c.malloc]`)

`aligned_alloc`, `calloc`, `malloc`, `realloc`, `free` have C semantics. They **do not** call `::operator new`/`delete`. Storage obtained from them is implicitly declared reachable for the pointer-safety rules. Their interaction with the C++ allocation functions in the data-race rules is in [[dynamic-memory-support]].

## Related

[[allocators]] · [[container-requirements]] · [[cpp17-lib-utilities]] · [[deprecated-library-facilities]] (`raw_storage_iterator`, `get_temporary_buffer`)
