---
type: concept
title: "std::function"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# `std::function<R(Args...)>` (`[func.wrap]`)

A polymorphic wrapper that can store, copy and call any callable target with a given call signature. Parent: [[function-objects-and-invoke]]; wider context [[cpp17-lib-utilities]].

## Rules (`[func.wrap.func]`)

- A callable type `F` is **Lvalue-Callable** for `ArgTypes` and `R` if `INVOKE<R>(declval<F&>(), declval<ArgTypes>()...)` is well-formed in an unevaluated context. The templated constructor and assignment take part in overload resolution only for such `F` (decayed for assignment).
- `function` is a call wrapper whose call signature is `R(ArgTypes...)`.
- **Construction**:
  - default and `nullptr_t`: no target (`!*this`).
  - copy: targets a copy of the source's target (or none). Does not throw if the target is a function pointer or a `reference_wrapper`; otherwise may throw `bad_alloc` or what the target's copy constructor throws.
  - move: the target is taken over; the source is left valid with an unspecified value.
  - `function(F f)` (requires `F` CopyConstructible): no target if `f` is a null function pointer, a null member pointer, or an empty `function`; otherwise targets a copy of `f` initialized from `std::move(f)`. Same non-throwing guarantee for function pointers and `reference_wrapper`.
  - **No allocator-taking constructors**: they were removed, so `uses_allocator` construction will not pass an allocator to `std::function` (recorded in Annex C, [[cpp17-compatibility-differences]]).
  - **Deduction guides** infer `function<R(A...)>` from a function pointer, and from a functor whose `operator()` is non-overloaded (the type of `&F::operator()` of form `R (G::*)(A...) cv &opt noexcept?`).
- Assignment: `= nullptr` clears, `= f` replaces the target (as if constructing a temporary and swapping), copy/move assignment; `swap`.
- **Observers**: `explicit operator bool` (has a target); comparison with `nullptr` (`f == nullptr` iff `!f`); `target_type()` returns `typeid(T)` of the target or `typeid(void)`; `target<T>()` returns a pointer to the stored target if `target_type() == typeid(T)`, else null (both rely on RTTI, [[type-identification-rtti]]).
- **Invocation**: `operator()(args...)` returns `INVOKE<R>(target, forward<ArgTypes>(args)...)` and **throws `bad_function_call`** if there is no target; otherwise propagates anything the target throws.
- `bad_function_call` is an exception class thrown only by the call operator ([[standard-exception-classes]]).

## Related

[[function-objects-and-invoke]] · [[lambda-expressions]] · [[type-identification-rtti]] · [[allocators]] · [[template-argument-deduction]] (deduction guides)
