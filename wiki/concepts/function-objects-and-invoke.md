---
type: concept
title: "Function objects: INVOKE, reference_wrapper, operator functors, not_fn, bind, mem_fn, searchers, hash"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Function objects (`[function.objects]`, `<functional>`)

Parent: [[cpp17-lib-utilities]]. The type-erased wrapper `std::function` has its own page: [[std-function]]. Closure types from lambdas: [[lambda-expressions]].

## INVOKE (`[func.def]`, `[func.require]`)

Everything in the library that "calls a callable" is defined through **`INVOKE(f, t1, ..., tN)`**:

| `f` is | Expression |
|---|---|
| pointer to member function of `T`, and `t1` is (derived from) `T` | `(t1.*f)(t2, ..., tN)` |
| pointer to member function, and `t1` is a `reference_wrapper` | `(t1.get().*f)(t2, ..., tN)` |
| pointer to member function otherwise (smart or raw pointer) | `((*t1).*f)(t2, ..., tN)` |
| pointer to data member, `N == 1`, same three cases | `t1.*f`, `t1.get().*f`, `(*t1).*f` |
| anything else | `f(t1, ..., tN)` |

`INVOKE<R>(...)` additionally converts the result to `R` (discarding it for cv `void`). A *call wrapper* is MoveConstructible; a *forwarding call wrapper* delivers arguments as references preserving value category; a *simple call wrapper* is a forwarding wrapper that is CopyConstructible/CopyAssignable with non-throwing copy/move. **`std::invoke(f, args...)`** returns `INVOKE(forward<F>(f), forward<Args>(args)...)` (`[func.invoke]`).

## `reference_wrapper<T>` (`[refwrap]`)

A copyable, trivially copyable wrapper around a reference to an object or function. Constructed from `T&` (or another `reference_wrapper`), assignable, `get()` / implicit conversion to `T&`, and callable (`INVOKE(get(), args...)`). `ref(t)` and `cref(t)` create them (and unwrap an existing wrapper). `make_pair`, `make_tuple` and `bind` unwrap `reference_wrapper` arguments ([[pair-and-tuple]]).

## Operator function objects (`[arithmetic.operations]`..`[bitwise.operations]`)

`plus`, `minus`, `multiplies`, `divides`, `modulus`, `negate`; `equal_to`, `not_equal_to`, `greater`, `less`, `greater_equal`, `less_equal`; `logical_and`, `logical_or`, `logical_not`; `bit_and`, `bit_or`, `bit_xor`, `bit_not`. Each class template `F<T>` calls the corresponding operator on two `T` const references. Each also has a `F<void>` specialization — the **transparent** functor — whose `operator()` is a template that perfectly forwards and may accept different types (it is what enables heterogeneous lookup in associative containers, [[associative-container-requirements]]).

For `less`, `greater`, `less_equal`, `greater_equal` (and the `void` forms when comparing pointers), the comparison yields a **strict total order on pointers** consistent with the built-in partial order — unlike built-in `<` on unrelated pointers (`[comparisons]/2`). This is why `unique_ptr` and `shared_ptr` ordering goes through `less` ([[unique-ptr]]).

## `not_fn`, `bind`, `mem_fn` (`[func.not_fn]`, `[func.bind]`, `[func.memfn]`)

- `not_fn(f)` returns a forwarding call wrapper that stores `decay_t<F>` and returns the logical negation of calling it (requires `FD` MoveConstructible and constructible from `F`).
- `bind(f, bound_args...)` returns a forwarding call wrapper `g` such that `g(u...)` is `INVOKE(fd, v1, ..., vN)` (or `INVOKE<R>` for `bind<R>`), where each bound argument `v_i` is determined by `TD_i = decay_t<T_i>`: a `reference_wrapper<T>` binds `T&`; a **bind expression** (`is_bind_expression_v`, true for results of `bind`) is *called* with all the call arguments and its result used; a **placeholder** (`is_placeholder_v` nonzero, i.e. `_1`, `_2`, ... in `std::placeholders`) selects the jth call argument forwarded; anything else is passed as an lvalue of the stored copy. Copy/move of the wrapper throws iff copying/moving a stored component throws; the wrapper is CopyConstructible if all components are. Programs may specialize the two traits for their own types.
- `mem_fn(pm)` returns a simple call wrapper with `fn(t, a2, ...) == INVOKE(pm, t, a2, ...)`.

## Searchers (`[func.search]`)

`default_searcher`, `boyer_moore_searcher`, `boyer_moore_horspool_searcher` are function objects constructed from a pattern range (plus an optional predicate, and for Boyer-Moore a hash function that must agree with the predicate). Calling one on `[first, last)` returns a pair of iterators `(i, j)` delimiting the match (`j = next(i, pattern length)`); an empty pattern matches at `first`; no match returns `(last, last)`. `default_searcher` is equivalent to `search`. They are used as the last argument of the `search` algorithm ([[nonmodifying-sequence-algorithms]]); Boyer-Moore ones need random-access iterators with the same value type and a default-constructible, copyable value type.

## `hash` (`[unord.hash]`)

`std::hash<Key>` is the default hasher of the unordered containers ([[unordered-container-requirements]]). A specialization is either **enabled** or **disabled**. Every header declaring `hash` provides enabled specializations for `nullptr_t` and all cv-unqualified arithmetic, enumeration and pointer types; for any other `Key` with no library or user specialization, `hash<Key>` is disabled — a disabled specialization is not even default-constructible or copyable (not a function object type). An enabled specialization satisfies the Hash requirements ([[library-named-requirements]]), is DefaultConstructible, CopyAssignable and swappable, guarantees `k1 == k2` implies equal hashes, and does not throw (unless a user specialization on a user type). Library specializations exist for `string` types, `error_code`, `bitset`, `optional`, `variant`, smart pointers, `thread::id`, `type_index`, `vector<bool>`.

## Related

[[std-function]] · [[cpp17-lib-utilities]] · [[lambda-expressions]] · [[algorithm-requirements]] · [[type-traits]] (`invoke_result`, `is_invocable`) · [[ordered-associative-containers]] · [[deprecated-library-facilities]] (old binder typedefs, `not1`/`not2`) · [[cpp17-annex-d-compatibility-features]] (`result_of`)
