---
type: concept
title: "C++17 clause 33: thread support library"
tags: [cpp17, library, standard-clause, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 33: Thread support library (`[thread]`)

About 15,200 words; 73 labelled sections. Creating and managing threads, mutual exclusion, condition variables and futures; the language-level memory model is in [[memory-model-and-data-races]], the lock-free primitives in [[cpp17-lib-atomics]]. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header(s) | Content | Wiki page |
|---|---|---|---|---|
| 33.2 Requirements | `[thread.req]` | — | `system_error` conventions, native handles, timeouts, BasicLockable / Lockable / TimedLockable, `DECAY_COPY` | [[threads]] |
| 33.3 Threads | `[thread.threads]` | `<thread>` | `thread`, `thread::id`, `this_thread` | [[threads]] |
| 33.4 Mutual exclusion | `[thread.mutex]` | `<mutex>`, `<shared_mutex>` | six mutex types, `lock_guard`, `scoped_lock`, `unique_lock`, `shared_lock`, `lock`/`try_lock`, `call_once` | [[mutexes-and-locks]] |
| 33.5 Condition variables | `[thread.condition]` | `<condition_variable>` | `condition_variable`, `condition_variable_any`, `notify_all_at_thread_exit` | [[condition-variable]] |
| 33.6 Futures | `[futures]` | `<future>` | `promise`, `future`, `shared_future`, `packaged_task`, `async`, `future_error` | [[futures-and-async]] |

## Cross-cutting rules

- **Synchronizes-with edges** the library promises: thread constructor → start of the new thread's function; thread completion → `join()`; `unlock()` → next `lock()`; a provider's set-result → waiting function returning; `call_once` active execution → next execution and all passive returns; `async` call → start of `f`.
- **Terminating cases** worth knowing: a joinable `thread` destroyed or assigned over; an uncaught exception escaping a thread's function; a condition-variable wait failing to restore its lock postcondition ([[exception-support]]).
- **Timeouts** come in `_for` (relative, steady clock recommended) and `_until` (absolute, the time point's clock) forms based on [[chrono-and-ratio]].
- Parallel algorithms ([[execution-policies-and-parallel-algorithms]]) interact with this clause through forward-progress guarantees and the ban on blocking synchronization under `par_unseq`.
- The thread-local floating-point environment ([[math-functions-and-fenv]]) and the per-thread `errno` ([[cpp17-lib-diagnostics]]) are specified in other clauses.

## Related

[[cpp17-lib-atomics]] · [[memory-model-and-data-races]] · [[cpp17-lib-utilities]] · [[standard-exception-classes]]
