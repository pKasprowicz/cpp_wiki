---
type: concept
title: "Sequence container requirements and optional operations"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Sequence containers (`[sequence.reqmts]`)

Refinement of [[container-requirements]] for `vector`, `deque`, `list`, `forward_list` (and, with a subset, `array` and `basic_string`). Parent: [[cpp17-lib-containers]]. Concrete classes: [[array-and-vector]], [[deque-and-lists]]. Adaptors built on top: [[container-adaptors]].

## Core operations (Table 87)

| Expression | Requirement and effect |
|---|---|
| `X(n, t)`, `X(i, j)`, `X(il)` | `n` copies (T CopyInsertable) / range (EmplaceConstructible from `*i`; each iterator in `[i, j)` dereferenced exactly once; for `vector` an input iterator also needs MoveInsertable) / initializer list |
| `a = il` | CopyInsertable + CopyAssignable; elements assigned or destroyed |
| `a.emplace(p, args)` | inserts a `T` constructed from `args` before `p` (for `vector`/`deque` T also MoveInsertable and MoveAssignable); returns iterator to the new element |
| `a.insert(p, t / rv / n,t / i,j / il)` | inserts before `p`; returns an iterator to the (first) inserted element, or `p` if nothing was inserted; ranges must not alias `a` |
| `a.erase(q)`, `a.erase(q1, q2)` | for `vector`/`deque` T must be MoveAssignable; returns an iterator to the element after the erased one(s), or `end()` |
| `a.clear()` | destroys everything; **invalidates all** references/pointers/iterators and may invalidate past-the-end |
| `a.assign(i,j)`, `assign(il)`, `assign(n,t)` | replaces contents; the arguments must not refer into `a`; invalidates all (and past-the-end for `vector`/`deque`) |

## Optional operations (Table 88), amortized constant time

| Operation | Provided by |
|---|---|
| `front()` | `basic_string`, `array`, `deque`, `forward_list`, `list`, `vector` |
| `back()` | all of those except `forward_list` |
| `emplace_front`, `push_front`, `pop_front` | `deque`, `forward_list`, `list` |
| `emplace_back`, `push_back`, `pop_back` (and `basic_string`'s `push_back`) | `deque`, `list`, `vector`, `basic_string` |
| `operator[]`, `at` | `basic_string`, `array`, `deque`, `vector` |

`emplace_front` and `emplace_back` **return a reference to the new element** (`a.front()`/`a.back()`). `pop_*` require a non-empty container. `at(n)` is bounds-checked and throws `out_of_range` if `n >= size()`; `operator[]` is not checked.

## Rules for constructor templates

For every sequence container (and `basic_string`): the `(InputIterator, InputIterator)` constructor, the iterator forms of `insert`/`assign`, and deduction guides with an `InputIterator` or `Allocator` parameter must not participate in overload resolution for a type that is not an input iterator or allocator (`/13`).

## Related

[[container-requirements]] · [[iterator-invalidation]] · [[basic-string]] · [[allocators]]
