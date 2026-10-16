---
type: concept
title: "std::valarray and its subset classes (slice, gslice, mask_array, indirect_array)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `valarray<T>` (`[numarray]`)

Parent: [[cpp17-lib-numerics]]. Element requirements: see the end of [[complex-numbers]] (`[numeric.requirements]`).

## What it is

- `valarray<T>` is a **one-dimensional "smart array"** of numbered elements (from 0) with element-wise operators and functions; higher-dimensional views are built by computed indices and the generalized subscript operators. It is designed for **n-at-a-time processing**, and the classes are defined to be **free of certain forms of aliasing**, which lets implementations optimize or parallelize.
- A function returning `valarray<T>` may return another type (expression templates) provided all const member functions of `valarray<T>` apply to it and it adds at most two levels of template nesting; implementations that do this must provide the matching overloads for every function taking `const valarray<T>&` (other than `begin`/`end`).
- Constructors: empty; `n` value-initialized elements; `n` copies of a value; from an array pointer and count; copy/move; from an `initializer_list`; and from the subset helper types. Assignment from another `valarray` **resizes** the target to match (as `resize(v.size())`) and assigns element-wise; scalar assignment fills.

## Subsetting (`[valarray.sub]`)

`operator[]` is overloaded to select sequences of elements: by `slice` (start, size, stride), `gslice` (generalized, multi-dimensional strides), `valarray<bool>` mask, and `valarray<size_t>` index array. The **const versions return a new `valarray`** holding copies; the **non-const versions return reference-semantics proxy objects** (`slice_array`, `gslice_array`, `mask_array`, `indirect_array`) that support assignment, compound assignment and `fill` through to the original array.

## Operations

- Unary `+ - ~ !`; element-wise binary and compound-assignment operators (`+ - * / % ^ & | << >>`) with array–array and array–scalar forms; logical `&&`, `||` and comparisons returning `valarray<bool>`; element-wise transcendentals (`abs`, `acos`, ..., `pow`, `sqrt`, `tanh`).
- Member functions: `swap`, `size`, `resize(n, value)`, `sum()` (requires `size() > 0`, `+=` applicable, unspecified order of summation), `min()`, `max()` (use `operator<`), `shift(n)` (shifts elements, filling with `T()`), `cshift(n)` (circular), `apply(f)`, and the non-member `begin(v)`/`end(v)` (iterators that are mutable/constant random-access and contiguous, valid until `resize` or destruction).

## Related

[[complex-numbers]] · [[cpp17-lib-numerics]] · [[iterator-adaptors]] (range access) · [[bitset]] (a different fixed-size value type)
