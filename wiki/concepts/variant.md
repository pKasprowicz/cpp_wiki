---
type: concept
title: "std::variant"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `variant<Types...>` (`[variant]`)

A type-safe tagged union. Parent: [[cpp17-lib-utilities]]. Siblings: [[optional]], [[any-type]].

## Core rules (`[variant.variant]`)

- At any time a `variant` holds a value of one *alternative* type or is **valueless** (`valueless_by_exception()` is true; `index()` returns `variant_npos`). The contained value is stored inside the variant object; **no dynamic memory** (`/1`).
- All alternatives must be (possibly cv-qualified) **non-array object types** (`/2`); `variant<>` with no alternatives is ill-formed (`/3`). Destructor trivial iff all alternatives' are.
- The default constructor value-initializes alternative **0** (so it exists only if `T0` is default-constructible); `monostate` is provided as a cheap first alternative to make a variant default-constructible (`[variant.monostate]`).

## Construction and assignment

- Copy/move construct the same alternative from the source; if the source is valueless, so is the result.
- **Converting constructor** `variant(T&&)`: the alternative is chosen by an imaginary overload set `FUN(Ti)` over all alternatives — whichever `FUN(Tj)` overload wins for `FUN(forward<T>(t))` selects `Tj` (`[variant.ctor]/12-13`). It is excluded when `decay_t<T>` is the variant itself or an `in_place_*` tag. Converting assignment uses the same selection.
- `variant(in_place_type<T>, args...)` / `(in_place_index<I>, args...)` (and initializer-list forms) choose the alternative explicitly; the type form requires `T` to occur exactly once.
- Copy assignment table: both valueless → no effect; target has a value, source valueless → destroy target value; same index → assign; different index → if `Tj` is nothrow-copy-constructible or not nothrow-move-constructible, `emplace<j>(copy)`, otherwise construct a temporary variant and move-assign it (`[variant.assign]/2`). **If the move construction of the new alternative throws, the variant becomes valueless.** Converting assignment of a value `t`: assign if the held alternative is the chosen `Tj`, else emplace-or-temporary by the same nothrow rule.
- `emplace<T>(args...)`/`emplace<I>(args...)` destroys the current value first and returns a reference to the new one; if its initialization throws the variant **might be valueless** (`[variant.mod]`).
- `swap`: both valueless → nothing; same index → swap the held values; otherwise exchange via moves (`[variant.swap]`).

## Access and visitation

- `holds_alternative<T>(v)` (ill-formed unless `T` appears exactly once). `get<I>(v)` / `get<T>(v)` return a reference or **throw `bad_variant_access`** if the held alternative differs; `get_if<I>(&v)` / `get_if<T>(&v)` return a pointer or `nullptr` (null for a null `v`) (`[variant.get]`). `I >= sizeof...(Types)` is ill-formed.
- `variant_size<V>` and `variant_alternative_t<I, V>` are the metafunctions (cv-qualified versions follow).
- **`visit(vis, vars...)`** calls `INVOKE(vis, get<is>(vars)...)` for the current indices; the call must be valid for **every** combination of alternatives and all results must share a common type; it throws `bad_variant_access` if any variant is valueless. For zero or one variant the dispatch is constant time; for several variants no complexity is guaranteed (`[variant.visit]`).

## Comparison, hash

Different indices: `==` false; the one with the smaller index is less. Same index: valueless variants are equal; otherwise compare the alternatives. A valueless variant orders before any non-valueless one (`[variant.relops]`). `monostate` values all compare equal. `hash<variant<...>>` is enabled iff all alternatives are hashable (`[variant.hash]`). `uses_allocator` is specialized true.

## Related

[[cpp17-lib-utilities]] · [[optional]] · [[any-type]] · [[function-objects-and-invoke]] (INVOKE) · [[standard-exception-classes]] · [[template-argument-deduction]]
