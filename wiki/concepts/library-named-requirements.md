---
type: concept
title: "Named requirements on library template arguments (CopyConstructible, Swappable, NullablePointer, Hash, ...)"
tags: [cpp17, library, cross-cutting, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Named requirements on template arguments (`[utility.requirements]`)

C++17 has no language-level concepts. The library therefore constrains the types a program passes as template arguments by **named requirements** that are tables of valid expressions and their semantics. In this draft the names appear as plain identifiers (`CopyConstructible`, `Destructible`, ...). Violating a requirement is undefined behavior (see [[library-requirements-and-conformance]], `[res.on.functions]/2`). Allocator requirements are on [[allocators]].

## Basic object requirements (`[utility.arg.requirements]`, Tables 20-27)

Notation: `T` object or reference type; `a, b, c` possibly-const `T` values; `s, t` modifiable lvalues; `rv` an rvalue; `v` a possibly-const lvalue or const rvalue.

| Requirement | What it demands |
|---|---|
| `EqualityComparable` | `a == b` convertible to `bool` and an **equivalence relation** (reflexive, symmetric, transitive) |
| `LessThanComparable` | `a < b` convertible to `bool` and a **strict weak ordering** |
| `DefaultConstructible` | `T t;`, `T u{};`, `T()`, `T{}` valid; the latter forms value- or aggregate-initialize |
| `MoveConstructible` | `T u = rv;` / `T(rv)` yield an object equivalent to the old value of `rv`; `rv` is left in an unspecified (but valid) state |
| `CopyConstructible` | adds: copying leaves the source unchanged and the copy equivalent |
| `MoveAssignable` | `t = rv` returns `T&` referring to `t`; unless `t` and `rv` are the same object, `t` equals the old `rv`; `rv` unspecified afterwards |
| `CopyAssignable` | adds: `t = v` makes `t` equivalent to `v`, `v` unchanged |
| `Destructible` | `u.~T()` reclaims owned resources and **does not propagate an exception** |

A default constructor is generally *not* required; it is needed only where a container member's default argument is `T()` and is actually used (`/2`). "Equivalent" here is about observable value, not identity.

## Swappable and ValueSwappable (`[swappable.requirements]`)

`t` is swappable with `u` when both `swap(t, u)` and `swap(u, t)` are valid **in a context where overload resolution sees the two `std::swap` templates of `<utility>` plus the ADL lookup set** (the "two-step" idiom: `using std::swap; swap(a, b);`), and they exchange the values. An iterator type is `ValueSwappable` when `*x` is swappable for any dereferenceable `x`; several mutating algorithms require this ([[algorithm-requirements]]). `std::swap` itself: see [[utility-move-forward-swap]].

## NullablePointer (`[nullablepointer.requirements]`)

A type `P` is a NullablePointer when it is `EqualityComparable`, `DefaultConstructible`, `CopyConstructible`, `CopyAssignable`, `Destructible`, lvalues are swappable, and it supports construction/assignment from and comparison with `nullptr` (Table 28). A value-initialized `P` is the null value, equal only to itself; a default-initialized `P` may be indeterminate; contextual conversion to `bool` behaves like `p != nullptr`; **no operation exits via an exception**. Used for `unique_ptr`'s `pointer` type ([[unique-ptr]]) and for allocator pointer types ([[allocators]]).

## Hash (`[hash.requirements]`)

`H` is a function object type that is `CopyConstructible` and `Destructible`, with `h(k)` returning `size_t` that depends **only on the argument for the duration of the program**, and not modifying an lvalue argument. Basis for `std::hash` and the unordered containers ([[unordered-container-requirements]]).

## Where the other named requirements live

| Requirement family | Defined in | Wiki page |
|---|---|---|
| Container, sequence/associative/unordered, `CopyInsertable`, `EmplaceConstructible`, `Erasable`, `MoveInsertable`, allocator-aware | `[container.requirements]` | [[container-requirements]] and siblings |
| Input/Output/Forward/Bidirectional/RandomAccess iterators (plus the contiguous-iterator property) | `[iterator.requirements]` | [[iterator-categories-and-requirements]] |
| Algorithm predicates, `Compare`, binary operations; parallel-algorithm restrictions | `[algorithms.requirements]`, `[algorithms.parallel.user]` | [[algorithm-requirements]] |
| callable type / call wrapper definitions and INVOKE; `UnaryTypeTrait`, `BinaryTypeTrait`, `TransformationTrait` | `[func.def]`, `[func.require]`, `[meta.rqmts]` | [[function-objects-and-invoke]], [[type-traits]] |
| `Clock`, `TrivialClock` | `[time.clock.req]` | [[chrono-and-ratio]] |
| Character traits | `[char.traits.require]` | [[char-traits]] |
| Numeric type requirements (`complex`/`valarray` element types) | `[numeric.requirements]` | [[cpp17-lib-numerics]] |
| Random bit generators, engines, adaptors, distributions, seed sequences | `[rand.req]` | [[random-number-generation]] |
| Stream buffer, `fpos` requirements | `[streambuf.reqts]`, `[fpos.operations]` | [[stream-buffers]], [[stream-base-classes]] |
| `BasicLockable`, `Lockable`, `TimedLockable`, mutex requirements | `[thread.req.lockable]`, `[thread.mutex.requirements]` | [[mutexes-and-locks]] |
| Regular expression traits | `[re.req]` | [[regex-classes-and-algorithms]] |
| Filesystem `path` requirements | `[fs.path.req]` | [[filesystem]] |

## Related

[[library-requirements-and-conformance]] · [[cpp17-lib-introduction]] · [[cpp17-special-member-functions]] (what copy/move mean at language level) · [[cpp17-templates]]
