---
type: concept
title: "std::atomic, memory_order, atomic_flag and fences"
tags: [cpp17, library, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Atomic operations library (`<atomic>`, `[atomics]`)

Library face of the memory model in [[memory-model-and-data-races]] (`[intro.multithread]`). Parent: [[cpp17-lib-atomics]]. Users elsewhere: signal handlers ([[cpp17-lib-language-support]]), `shared_ptr` atomic access ([[shared-ptr-and-weak-ptr]]), mutexes and futures ([[cpp17-lib-thread]]). `<atomic>` is in the freestanding header set.

## `memory_order` (`[atomics.order]`)

| Value | Effect on the affected location |
|---|---|
| `memory_order_relaxed` | atomicity only; **orders no other memory** |
| `memory_order_consume` | a load performs a *consume* operation (dependency-ordered) |
| `memory_order_acquire` | a load performs an *acquire* operation |
| `memory_order_release` | a store performs a *release* operation |
| `memory_order_acq_rel` | a read-modify-write is both acquire and release |
| `memory_order_seq_cst` | acquire for loads, release for stores, and participates in the single total order below |

Key rules:

- A **release** operation `A` on atomic object `M` **synchronizes with** an **acquire** operation `B` on `M` that takes its value from any side effect in the release sequence headed by `A` (`/2`).
- There is a **single total order `S`** on all `memory_order_seq_cst` operations, consistent with happens-before and with every location's modification order. A seq_cst load observes the last preceding seq_cst modification in `S`, or a non-seq_cst modification that does not happen before it, and seq_cst *fences* constrain which values loads may observe and the modification order (`/3-7`).
- Atomic read-modify-write operations always read the **last value in the modification order** before their write (`/11`). Implementations *should* avoid out-of-thin-air values (`/9`) and make stores visible to loads "within a reasonable amount of time" (`/12`).
- `kill_dependency(y)` returns `y` without carrying a dependency into the return value.

## `atomic<T>` (`[atomics.types.generic]`)

- `T` must be **trivially copyable**. `atomic<bool>` is a standard-layout struct. Primary-template operations (`[atomics.types.operations]`): constructors (default leaves the object **uninitialized**; `atomic(T)` initialization is **not atomic**), `ATOMIC_VAR_INIT`/`atomic_init` (non-atomic initialization, once, on a default-constructed object), `is_lock_free()` and the static `is_always_lock_free`, `store(desired, order)` (order not consume/acquire/acq_rel), `load(order)` (not release/acq_rel), `operator T`, `operator=(T)`, `exchange`, `compare_exchange_weak/strong(expected, desired, success, failure)`. In `compare_exchange`, the comparison and replacement are atomic; memory is affected per `success` if equal and `failure` if not (the single-order form derives `failure` from it, replacing acq_rel by acquire and release by relaxed); `failure` may not be release or acq_rel. **A weak exchange may fail spuriously** (even when the values are equal, writing back the original value into `expected`), so it belongs in a loop; implementations should not fail consistently without cause.
- **Integral specializations** (`char`, `signed char`, `unsigned char`, `short`..`long long` and their unsigned forms, `char16_t`, `char32_t`, `wchar_t`, and the `<cstdint>` types): trivial default constructor/destructor, standard-layout, plus `fetch_add`, `fetch_sub`, `fetch_and`, `fetch_or`, `fetch_xor` (return the **old** value) and the operators `+= -= &= |= ^=`, `++`, `--` (return the new value). **Signed arithmetic is two's complement with no undefined results.**
- **Pointer partial specialization** `atomic<T*>`: `fetch_add`, `fetch_sub`, `+=`, `-=`, `++`, `--`; `T` must be an object type; the result may be an undefined address but there is no other undefined behavior.
- No floating-point specializations exist in this draft.
- Type aliases `atomic_int8_t` ... `atomic_uintptr_t` exist iff the underlying fixed-width types do (`[atomics.alias]`). Non-member `atomic_f` / `atomic_f_explicit` function templates call the member `f` on the first argument (`[atomics.nonmembers]`).

## Lock-freedom (`[atomics.lockfree]`)

`ATOMIC_BOOL_LOCK_FREE`, `ATOMIC_CHAR_LOCK_FREE`, ... `ATOMIC_POINTER_LOCK_FREE` take the value 0 (never lock-free), 1 (sometimes) or 2 (always); signed and unsigned variants and the corresponding specializations share the property. `is_lock_free()` / `atomic_is_lock_free` must give consistent answers for the same type within an execution. **Non-lock-free atomic operations are considered to potentially block** ([[abstract-machine-and-observable-behavior]] on forward progress). "Plain lock-free atomic operations" are the only atomics usable in signal handlers ([[cpp17-lib-language-support]]).

## `atomic_flag` (`[atomics.flag]`)

The classic test-and-set flag: two states (set, clear); **all operations are lock-free**; standard-layout with trivial default constructor/destructor. `test_and_set(order)` atomically sets the flag to true and returns the previous value; `clear(order)` sets it false (order not consume/acquire/acq_rel). `ATOMIC_FLAG_INIT` initializes to clear (statically for static-duration objects); otherwise the initial state is unspecified. There is no `test()` operation in this draft.

## Fences (`[atomics.fences]`)

`atomic_thread_fence(order)`: relaxed — nothing; acquire/consume — acquire fence; release — release fence; acq_rel — both; seq_cst — sequentially consistent acquire+release fence. A **release fence synchronizes with an acquire fence** if atomic operations `X` (after the release fence, modifying `M`) and `Y` (before the acquire fence) read the value of `X` or of a hypothetical release sequence headed by `X`; analogous rules cover fence-to-atomic and atomic-to-fence synchronization (`/2-4`). `atomic_signal_fence(order)` is the same but constrains only the ordering between a thread and a **signal handler in the same thread**.

## Related

[[memory-model-and-data-races]] · [[cpp17-lib-atomics]] · [[mutexes-and-locks]] · [[cpp17-expressions]] · [[sequencing-and-evaluation-order]]
