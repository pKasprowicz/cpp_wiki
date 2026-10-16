---
type: concept
title: "Iterator categories, requirements, iterator_traits and tags"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Iterator requirements and primitives (`[iterator.requirements]`, `[iterator.primitives]`)

Parent: [[cpp17-lib-iterators]]. Adaptors and stream iterators: [[iterator-adaptors]]. How algorithms depend on these: [[algorithm-requirements]]; how containers expose them: [[container-requirements]].

## What an iterator is (`[iterator.requirements.general]`)

- A generalization of pointers: every function template taking iterators must also work with raw pointers. An **input iterator** supports `*i` giving a value of the *value type*; an **output iterator** supports `*i = o` for each type writable to it; `i->m` is `(*i).m`. Every iterator with equality has a signed **difference type**.
- **Five categories** (Table 93): input, output, forward, bidirectional, random access; refinement chain **random access → bidirectional → forward → input**, with output a separate branch. Forward and richer iterators that are also output iterators are **mutable**; others are **constant**.
- **Contiguous iterators** are random-access iterators with `*(a + n)` equivalent to `*(addressof(*a) + n)` — an additional property, *not* a sixth tag category (`/6`). Pointers, `vector` (non-bool), `array`, `basic_string`, `basic_string_view` iterators qualify.
- **Values**: *past-the-end* values (never dereferenceable), *dereferenceable* values, *singular* values (not associated with any sequence). Almost every operation on a singular value is undefined; exceptions are destroying it, assigning a non-singular value to it, and (for DefaultConstructible iterators) copying from a value-initialized one.
- **Reachable**: `j` is reachable from `i` if finitely many `++i` give `j`. A **range** `[i, j)` is *valid* iff `j` is reachable from `i`; applying library functions to invalid ranges is undefined. `[i, i)` is empty.
- All operations of every category must be realizable in **amortized constant time** (so no complexity column). Destroying an iterator may invalidate pointers/references obtained from it. An *invalid* iterator is one that may be singular ([[iterator-invalidation]]).

## The category requirement tables

| Category | Adds | Key semantic points |
|---|---|---|
| **Iterator** (base) | CopyConstructible, CopyAssignable, Destructible, swappable lvalues; `*r`, `++r` | the basis of all categories |
| **Input** | `EqualityComparable`; `a != b`; `*a` convertible to `T`; `a->m`; `++r`; `(void)r++`; `*r++` | single-pass: after `++r`, copies of the old value need not be dereferenceable or in the domain of `==`. The *domain of `==`* varies by algorithm |
| **Output** | `*r = o`, `++r` (returns `X&`), `r++`, `*r++ = o` | after writing, `r` need not be dereferenceable but is incrementable; each position written at most once between increments |
| **Forward** | input + `DefaultConstructible`; `reference` is a real reference (`T&` or `const T&`); `r++` returns something convertible to `const X&`; **multi-pass guarantee** (`a == b` implies `++a == ++b`; `++X(a)` does not change `*a`) | equality compares iterators over the same sequence (value-initialized iterators compare equal to each other); if `a == b` both or neither are dereferenceable; if both are, `a == b` iff `*a` and `*b` are bound to the same object |
| **Bidirectional** | `--r`, `r--`, `*r--` | `--(++r) == r`; `--r == --s` implies `r == s` |
| **Random access** | `r += n`, `a + n`/`n + a`, `r -= n`, `a - n`, `b - a`, `a[n]`, `<`, `>`, `<=`, `>=` | `<` is a total ordering; `b == a + (b - a)` |

`ValueSwappable`: an iterator whose dereferenced value is swappable — required by mutating algorithms such as `reverse`/`partition` ([[library-named-requirements]], [[mutating-sequence-algorithms]]).

## `iterator_traits` and tags (`[iterator.traits]`, `[std.iterator.tags]`)

- Every iterator type must supply (or `iterator_traits<I>` must supply) `difference_type`, `value_type`, `pointer`, `reference`, `iterator_category`; for output iterators the first four may be `void`. `iterator_traits<I>` forwards these if `I` has valid nested types of those names; otherwise it has **no members at all** (SFINAE-friendly); it is specialized for `T*` and `const T*` (category `random_access_iterator_tag`).
- Tags: `input_iterator_tag`, `output_iterator_tag`, `forward_iterator_tag`, `bidirectional_iterator_tag`, `random_access_iterator_tag`, each deriving from the next-weaker one (except output), so tag dispatch picks the most specific overload. There is **no contiguous tag** in this draft.

## Iterator operations (`[iterator.operations]`)

`advance(i, n)` (negative `n` only for bidirectional/random access; constant time for random access, linear otherwise), `distance(first, last)` (for random-access iterators `last - first`, otherwise counts increments; `last` must be reachable from `first`, or for random access either direction), `next(x, n = 1)` and `prev(x, n = 1)` (equivalent to `advance` on a copy).

## Related

[[iterator-adaptors]] · [[algorithm-requirements]] · [[container-requirements]] · [[uninitialized-memory-algorithms]] · [[cpp17-lib-iterators]] · [[cpp17-annex-d-compatibility-features]] (deprecated `std::iterator` base)
