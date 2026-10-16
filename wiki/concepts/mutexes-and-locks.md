---
type: concept
title: "Mutexes, lock wrappers, generic locking and call_once"
tags: [cpp17, library, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Mutual exclusion (`<mutex>`, `<shared_mutex>`, `[thread.mutex]`)

Parent: [[cpp17-lib-thread]]. Lockable requirements and timing: [[threads]]. Waiting on conditions: [[condition-variable]]. Memory-model meaning of lock/unlock: [[memory-model-and-data-races]].

## Mutex types (`[thread.mutex.requirements]`)

| Type | Ownership | Recursion | Timed | Notes |
|---|---|---|---|---|
| `mutex` | exclusive | no | no | standard-layout |
| `recursive_mutex` | exclusive | yes (depth unspecified; at the maximum, `try_lock` fails and `lock` throws `system_error`) | no | |
| `timed_mutex` | exclusive | no | `try_lock_for`, `try_lock_until` | |
| `recursive_timed_mutex` | exclusive | yes | yes | |
| `shared_mutex` | exclusive **or shared** | no | no | `<shared_mutex>`; adds `lock_shared`, `try_lock_shared`, `unlock_shared` |
| `shared_timed_mutex` | exclusive or shared | no | yes | adds timed shared locking |

Common rules (all mutex types):

- Default-constructible, destructible, **neither copyable nor movable**; construction failure throws `system_error`.
- `lock()`, `try_lock()`, `unlock()` behave as **atomic operations** for data-race purposes and all lock/unlock operations on one mutex appear in a **single total order**. A prior `unlock()` **synchronizes with** the next `lock()` (or successful `try_lock`/`try_lock_for`/`try_lock_until`/`lock_shared`) on the same mutex.
- `lock()`: for non-recursive mutexes the calling thread must not already own the mutex (else undefined; deadlock or `resource_deadlock_would_occur`); blocks until ownership is obtained. `try_lock()` never blocks and never throws, **may fail spuriously** (it should not do so consistently without contention). `unlock()` requires the caller to own the mutex and never throws.
- **Undefined behavior**: destroying a mutex owned by a thread, or a thread terminating while owning a mutex.
- Timed `try_lock_for(rel)`: if `rel <= rel.zero()` it behaves like `try_lock()`; may not return `false` before the timeout; `try_lock_until(abs)` likewise with a time point.
- **Shared ownership**: any number of threads may hold shared ownership concurrently, but never together with exclusive ownership; the maximum number of simultaneous shared owners is unspecified but **at least 10000**; excess `lock_shared` callers block until the count drops below the maximum.

## Lock wrappers (`[thread.lock]`)

| Template | Role |
|---|---|
| `lock_guard<M>` | RAII: locks in the constructor (or adopts an already-locked mutex with `adopt_lock`), unlocks in the destructor; `M` BasicLockable; neither copyable nor movable |
| `scoped_lock<M...>` | like `lock_guard` for **zero or more** mutexes; with several it locks them via `std::lock` (deadlock-free); stores a `tuple` of references; also supports `adopt_lock` |
| `unique_lock<M>` | movable, flexible ownership: constructors `defer_lock`, `try_to_lock`, `adopt_lock`, with `try_lock_for` / `try_lock_until` timeouts; `lock`, `try_lock`, `try_lock_for`, `try_lock_until`, `unlock`, `release`, `swap`, `owns_lock`, `explicit operator bool`, `mutex()`. Locking functions throw `system_error` with `operation_not_permitted` if there is no mutex and `resource_deadlock_would_occur` if already owned. The destructor unlocks only if it owns |
| `shared_lock<M>` | like `unique_lock` but for **shared** ownership of a shared mutex |

All of these have undefined behavior if the referenced mutex doesn't outlive the lock; for a non-recursive mutex the constructor requires that the thread doesn't already own it. Tag types: `defer_lock_t`, `try_to_lock_t`, `adopt_lock_t`.

## Generic locking (`[thread.lock.algorithm]`)

- `try_lock(l1, l2, ...)` calls `try_lock()` on each in order; on the first failure (false **or exception**) it unlocks all those already locked and stops; returns −1 if all succeeded, otherwise the zero-based index of the failing one.
- `lock(l1, l2, ...)` locks all arguments with an unspecified sequence of `lock`, `try_lock`, `unlock` calls that **must not deadlock**; if any call throws, everything locked so far is unlocked.

## `call_once` (`[thread.once]`)

`once_flag` is an opaque, non-copyable flag; `call_once(flag, f, args...)` runs `INVOKE(f, args...)` at most once *successfully*: executions are *active* (call `f`) or *passive*. All active executions for a flag occur in a total order; completion of an active execution synchronizes with the start of the next; the **returning** execution synchronizes with the return of all passive ones. If `f` exits with an exception, that execution is *exceptional*, the exception propagates, and another call may try again. Also may throw `system_error`.

## Related

[[condition-variable]] · [[threads]] · [[atomics-and-memory-order]] · [[pair-and-tuple]] (scoped_lock stores a tuple) · [[chrono-and-ratio]]
