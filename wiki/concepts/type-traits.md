---
type: concept
title: "Type traits (<type_traits>)"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Metaprogramming and type traits (`[meta]`)

Compile-time type queries and transformations. Parent: [[cpp17-lib-utilities]]. `<type_traits>` is also in the freestanding header set ([[library-requirements-and-conformance]]). Used heavily for constraining overloads ("shall not participate in overload resolution unless ...") throughout the library, which is how C++17 emulates concept constraints ([[template-argument-deduction]], [[library-named-requirements]]).

## Requirements on a trait (`[meta.rqmts]`)

- **UnaryTypeTrait**: a class template over one type (plus optional helpers); DefaultConstructible and CopyConstructible; publicly and unambiguously derived from its *base characteristic*, a specialization of `integral_constant`; members of the base are not hidden.
- **BinaryTypeTrait**: the same for a relationship between two types.
- **TransformationTrait**: defines a public nested `type` naming the modified type.
- Helpers (`[meta.help]`): `integral_constant<T, v>`, `bool_constant<B>`, `true_type`, `false_type`. Every trait has an `_v` variable template (for `value`) and every transformation an `_t` alias (for `type`); `void_t<...>` maps any list of types to `void`.

## Unary traits (`[meta.unary]`)

- **Primary categories**: `is_void`, `is_null_pointer`, `is_integral`, `is_floating_point`, `is_array` (the class template `array` is *not* an array type), `is_pointer` (includes function pointers, excludes member pointers), `is_lvalue_reference`, `is_rvalue_reference`, `is_member_object_pointer`, `is_member_function_pointer`, `is_enum`, `is_union`, `is_class`, `is_function`. **Exactly one of these is true for any type**, and the answer is the same for `T` and `cv T`.
- **Composite**: `is_reference`, `is_arithmetic`, `is_fundamental`, `is_object`, `is_scalar`, `is_compound`, `is_member_pointer`.
- **Properties**: `is_const`, `is_volatile`, `is_trivial`, `is_trivially_copyable`, `is_standard_layout`, `is_pod`, `is_empty`, `is_polymorphic`, `is_abstract`, `is_final`, `is_aggregate`, `is_signed` (via `T(-1) < T(0)`), `is_unsigned`, `has_virtual_destructor`, `has_unique_object_representations`.
- **Operation traits**, each with `trivially_` and `nothrow_` variants: `is_constructible<T, Args...>` (true iff `T t(declval<Args>()...)` would be well-formed; access ignored, immediate context only), `is_default_constructible`, `is_copy_constructible` (= `is_constructible<T, const T&>`, false for non-referenceable `T`), `is_move_constructible`, `is_assignable`, `is_copy_assignable`, `is_move_assignable`, `is_swappable_with` / `is_swappable` (using the Swappable lookup context), `is_destructible`. "Known to call no non-trivial operation" / "known not to throw" are judged by the implementation.
- **Completeness**: most operation traits require `T` (and `Args`) to be complete, `void`, or an array of unknown bound; a user must not rely on an incomplete class. Instantiating a trait with a class template specialization may implicitly instantiate it only if the trait's semantics need a complete type. It is unspecified whether the library supplies specializations of these templates; **programs may not specialize** them ([[library-requirements-and-conformance]]), except where stated (see `common_type`).
- **Queries** (`[meta.unary.prop.query]`): `alignment_of`, `rank`, `extent<T, I>` — integral constants of type `size_t`.

## Relationships (`[meta.rel]`)

`is_same` (same type and cv), `is_base_of` (including a class being its own base; not for unions), `is_convertible<From, To>` (true iff `To test() { return declval<From>(); }` would be well-formed), and the INVOKE-based `is_invocable`, `is_invocable_r`, `is_nothrow_invocable`, `is_nothrow_invocable_r` ([[function-objects-and-invoke]]).

## Transformations (`[meta.trans]`)

| Group | Traits |
|---|---|
| cv | `remove_const`, `remove_volatile`, `remove_cv`, `add_const`, `add_volatile`, `add_cv` (no effect on references/functions) |
| reference | `remove_reference`, `add_lvalue_reference`, `add_rvalue_reference` (identity for non-referenceable types such as `void`) |
| sign | `make_signed`, `make_unsigned` (keep cv; smallest-rank type of same size for enums/`char`-like) |
| array | `remove_extent`, `remove_all_extents` |
| pointer | `remove_pointer`, `add_pointer` |
| other | `aligned_storage<Len, Align>`, `aligned_union<Len, Types...>`, **`decay`** (remove reference; array → pointer; function → pointer; else remove cv), `enable_if<B, T>` (member `type` only if `B`), `conditional<B, T, F>`, `common_type<T...>`, `underlying_type<E>`, **`invoke_result<Fn, Args...>`** (member `type` only if INVOKE is well-formed) |

`common_type` of one type is `common_type_t<T0, T0>`; of two it is the decayed type of `decltype(false ? declval<D1>() : declval<D2>())` (with decaying first if either argument changes under decay), and of more it folds left; absent when no such type. A program may specialize `common_type<T1, T2>` for non-decayed-changing types (needs to be symmetric); that is the one allowed specialization (`/Note B`). `result_of` and `is_literal_type` are in Annex D (`[depr.meta.types]`), not here; see [[cpp17-annex-d-compatibility-features]].

## Logical operator traits (`[meta.logical]`)

`conjunction<B...>`, `disjunction<B...>`, `negation<B>` **short-circuit instantiation**: `conjunction` stops at the first `Bi` with a false `value`, `disjunction` at the first true; the result derives from that `Bi` (or the last type), so the resulting `value` is not just a `bool` but that type's own `value`. `negation<B>` is `bool_constant<!bool(B::value)>`.

## Related

[[cpp17-lib-utilities]] · [[function-objects-and-invoke]] · [[utility-move-forward-swap]] (`declval`) · [[cpp17-templates]] · [[constant-expressions]] · [[template-argument-deduction]] · [[cpp17-annex-d-compatibility-features]] (`result_of`, `is_literal_type`)
