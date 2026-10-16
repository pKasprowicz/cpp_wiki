---
type: concept
title: "std::optional"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `optional<T>` (`[optional]`)

An object that either contains a `T` or does not. Parent: [[cpp17-lib-utilities]]. Sibling vocabulary types: [[variant]], [[any-type]].

## Core guarantees (`[optional.optional]`)

- The contained value lives **inside the `optional`'s own storage**, suitably aligned; the implementation may not use dynamic memory (`/1`). Contextual conversion to `bool` is true iff a value is contained.
- `T` must be an object type satisfying `Destructible`; instantiating `optional` for a reference type, or for (cv) `in_place_t` / `nullopt_t`, is ill-formed (`[optional.syn]/1`, `/3`). Deduction guide: `optional(T) -> optional<T>`.
- The destructor is trivial when `T`'s is. Copy/move constructors are deleted or excluded unless `T` is copy/move constructible, and are `constexpr` for trivially copyable `T` (`[optional.ctor]`).
- `nullopt_t` / `nullopt`: tag meaning "no value"; the type has no default constructor, no initializer-list constructor, and is not an aggregate (`[optional.nullopt]`).

## Construction and assignment

| Operation | Result |
|---|---|
| `optional()`, `optional(nullopt)` | empty; `constexpr` for every object type |
| `optional(const optional&)`, `optional(optional&&)` | copy/move the contained value if present (move leaves the source's engaged state unchanged) |
| `optional(in_place, args...)` / `(in_place, il, args...)` | direct-non-list-initialize the value in place; participates only if `T` is constructible that way |
| `optional(U&&)` (U defaults to `T`) | value-initialize from `U`; excluded when `decay_t<U>` is `in_place_t` or `optional<T>`; `explicit` iff `U&&` is not convertible to `T` |
| `optional(const optional<U>&)`, `optional(optional<U>&&)` | converting; excluded when `T` can already be built/converted directly from an `optional<U>` in any value category (a long list of `is_constructible`/`is_convertible` exclusions) |
| `operator=(nullopt)`, `reset()` | destroy the value if present |
| copy/move assignment, converting assignment, `operator=(U&&)` | four-case table: both engaged → assign values; only source engaged → construct in the target; only target engaged → destroy; neither → no effect. **If an exception is thrown, `bool(*this)` is unchanged** and the value state follows `T`'s own guarantee |
| `emplace(args...)` | destroys any current value, then constructs a new one and returns a reference to it; if the constructor throws, the optional is left **empty** |

Assignments and conversions are deleted or excluded unless `T` is constructible *and* assignable from the source (`[optional.assign]`). `swap` swaps engaged values, or moves the engaged value across when only one is engaged.

## Observers (`[optional.observe]`)

`operator->` / `operator*` (precondition: contains a value; no check, `constexpr`); `has_value()` and `explicit operator bool`; `value()` returns a reference or throws **`bad_optional_access`** when empty; `value_or(u)` returns the value or `static_cast<T>(forward<U>(u))` (ill-formed unless `T` is copy/move constructible and `U&&` converts to `T`). `bad_optional_access` is an exception class ([[standard-exception-classes]]).

## Comparison (`[optional.relops]`, `[optional.nullops]`, `[optional.comp_with_t]`)

- Two optionals: both empty are equal; an empty optional is **less than** any engaged optional; two engaged ones compare their values with the corresponding operator. Requirements: the underlying `*x op *y` must be valid and convertible to `bool`.
- Against `nullopt`: `x == nullopt` iff `!x`; `x < nullopt` is always false; `nullopt < x` iff `bool(x)`; and so on.
- Against a value `v`: `x == v` is `bool(x) ? *x == v : false`; `x < v` is `bool(x) ? *x < v : true`; `v < x` is `bool(x) ? v < *x : false`. So an empty optional orders before every value.
- `make_optional(v)` gives `optional<decay_t<T>>`; `make_optional<T>(args...)` builds in place. `swap(x, y)` calls `x.swap(y)`. `hash<optional<T>>` is enabled iff `hash<remove_const_t<T>>` is; an engaged optional hashes like its value, an empty one to an unspecified value (`[optional.hash]`).

## Related

[[cpp17-lib-utilities]] · [[variant]] · [[any-type]] · [[utility-move-forward-swap]] (`in_place`, `nullopt` neighbors) · [[library-named-requirements]] · [[initialization]]
