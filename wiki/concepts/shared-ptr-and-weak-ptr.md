---
type: concept
title: "std::shared_ptr, weak_ptr, enable_shared_from_this and friends"
tags: [cpp17, library, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Shared-ownership pointers (`[util.smartptr]`)

Parent: [[cpp17-lib-utilities]]. Sole ownership: [[unique-ptr]].

## `shared_ptr<T>` (`[util.smartptr.shared]`)

- Stores a pointer (usually from `new`) with **shared ownership**: the last owner disposes of the object. A `shared_ptr` that owns nothing is *empty*. Specializations are CopyConstructible, CopyAssignable, LessThanComparable and contextually convertible to `bool`; `T` may be incomplete.
- `element_type` is `remove_extent_t<T>`, so **`shared_ptr<U[]>` and `shared_ptr<U[N]>` are supported** (a `Y*` is "compatible" with `T*` when it converts, or `Y` is `U[N]` and `T` is `cv U[]`). Annex C records that this array support changed the constraint on conversions from `unique_ptr` ([[cpp17-compatibility-differences]]). `weak_type` is `weak_ptr<T>`.
- **Constructors**: default and `nullptr_t` give empty with `use_count() == 0`; `shared_ptr(Y* p)` (explicit; `Y` complete; `delete p`/`delete[] p` well-formed and non-throwing) takes ownership and calls `delete`/`delete[]` on exception; with a deleter `d` (and optionally an allocator `a` for internal bookkeeping) — if construction throws, `d(p)` is called; `shared_ptr(r, p)` is the **aliasing constructor** (shares `r`'s ownership but stores `p`); copy/move/converting copies; `shared_ptr(const weak_ptr<Y>&)` throws `bad_weak_ptr` if expired; from `unique_ptr<Y, D>&&` (empty if the source is null, otherwise takes the pointer and deleter, using `ref` for a reference deleter). A constructor that takes a raw pointer **enables `shared_from_this`** when the pointee has an `enable_shared_from_this` base, by setting its `weak_this` (non-atomic; conflicts with concurrent access).
- **Destructor**: nothing if empty or other owners remain; otherwise calls the stored deleter or `delete`.
- Assignment is copy/move-and-swap; `reset()`, `reset(p[, d[, a]])`, `swap`.
- **Observers**: `get()`, `operator*` and `operator->` (declaration unspecified for array/void types), `operator[]` (arrays; bounds checked only as a precondition), `use_count()` (the number of owners; 0 if empty; no synchronization), `explicit operator bool`, `owner_before` (an ownership-based strict weak ordering where two instances are equivalent iff they share ownership or are both empty). `get_deleter<D>(p)` returns the address of the owned deleter or null.
- **Creation**: `make_shared<T>(args...)` and `allocate_shared<T>(a, args...)` construct the object by `::new (pv) T(forward<Args>(args)...)`; `use_count() == 1`; implementations *should* do at most one allocation; they enable `shared_from_this`. (In this draft they are specified only via placement new of `T`.)
- **Comparison and casts**: `==`, `<` compare `get()` (via `less<>`), including against `nullptr`; `static_pointer_cast`, `dynamic_pointer_cast`, `const_pointer_cast`, `reinterpret_pointer_cast` return a `shared_ptr` that **shares ownership** with the argument (`dynamic_pointer_cast` yields empty if the cast fails). `operator<<` prints `get()`.
- **Data races**: member functions touch only the smart-pointer objects, never the pointees, and `use_count()` changes are not data-race-relevant (`/4`). Concurrent access to *the same `shared_ptr` object* is a race unless done solely through the atomic free functions below.

## `weak_ptr<T>` (`[util.smartptr.weak]`)

A non-owning reference to an object managed by `shared_ptr`. Copyable and movable; constructs from a `shared_ptr` sharing ownership; `use_count()` (0 if empty), `expired()` (`use_count() == 0`), `lock()` (atomically `expired() ? shared_ptr<T>() : shared_ptr<T>(*this)`), `reset`, `swap`, `owner_before`. Destroying a `weak_ptr` does not affect the object. `bad_weak_ptr` is the exception from the checked `shared_ptr` constructor.

## `owner_less`, `enable_shared_from_this<T>`

- `owner_less<...>::operator()(x, y)` is `x.owner_before(y)`, allowing ownership-based keys for mixed `shared_ptr`/`weak_ptr` associative containers ([[ordered-associative-containers]]).
- `enable_shared_from_this<T>` is a protected-constructor mixin: `shared_from_this()` returns `shared_ptr<T>(weak_this)` (throws `bad_weak_ptr` via that constructor if no `shared_ptr` owns the object); `weak_from_this()` returns the stored `weak_ptr`. Copies do not copy `weak_this`.

## Atomic access to a `shared_ptr` (`[util.smartptr.shared.atomic]`)

Free functions `atomic_is_lock_free`, `atomic_load`, `atomic_store`, `atomic_exchange`, `atomic_compare_exchange_weak/strong` and their `_explicit` forms (with `memory_order` arguments, following the `atomic<T>` rules) make concurrent access to a `shared_ptr` object race-free **provided every access uses them**, passing a pointer to the `shared_ptr`. Preconditions: non-null pointers; load orders may not be release/acq_rel, store orders may not be acquire/acq_rel; failure order of compare-exchange may not be release/acq_rel. All non-throwing. See [[atomics-and-memory-order]].

## Hash

`hash<unique_ptr<T,D>>` is enabled iff `hash<pointer>` is, and equals the hash of `get()`; `hash<shared_ptr<T>>` equals the hash of `get()` (`[util.smartptr.hash]`).

## Related

[[unique-ptr]] · [[cpp17-lib-utilities]] · [[allocators]] · [[atomics-and-memory-order]] · [[standard-exception-classes]] · [[memory-model-and-data-races]] · [[cpp17-annex-d-compatibility-features]] (deprecated `unique()`)
