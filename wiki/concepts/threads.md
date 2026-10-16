---
type: concept
title: "std::thread, thread::id, this_thread and timing/exception conventions of the thread library"
tags: [cpp17, library, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Threads (`<thread>`, `[thread.threads]`, `[thread.req]`)

Parent: [[cpp17-lib-thread]]. Synchronization: [[mutexes-and-locks]], [[condition-variable]], [[futures-and-async]], [[atomics-and-memory-order]]. Language-level thread semantics: [[memory-model-and-data-races]].

## Library-wide conventions (`[thread.req]`)

- **Exceptions**: functions specified to throw `system_error` do so when a listed error condition is detected or the underlying API fails; the `code()` must compare equal to one of the function's error conditions (`errc` values such as `resource_unavailable_try_again`, `operation_not_permitted`, `resource_deadlock_would_occur`, `invalid_argument`, `no_such_process`). Allocation failure is reported as usual ([[error-codes-and-system-error]], [[library-requirements-and-conformance]]).
- **Native handles**: `native_handle_type` / `native_handle()` presence and meaning are implementation-defined.
- **Timing**: `_for` functions take a duration (relative timeout; *should* use a steady clock), `_until` functions take a time point (absolute; should use the point's clock, tolerant of clock adjustment). Actual delay is the nominal timeout plus implementation and contention delays (`Di`, `Dm`). Clocks used must satisfy `TrivialClock` ([[chrono-and-ratio]]). Exceptions thrown by clocks, time points or durations during a timed function are *timeout-related exceptions*.
- **Lockable requirements** (types usable with locks): `BasicLockable` (`lock()` blocks until acquired and acquires nothing if it throws; `unlock()` precondition: the agent holds the lock, never throws), `Lockable` (adds `bool try_lock()`), `TimedLockable` (adds `try_lock_for(rel)` and `try_lock_until(abs)`) (`[thread.req.lockable]`). An *execution agent* is a thread or similar.
- `DECAY_COPY(x)` means `decay_copy(x)` — used to copy callable and arguments into the new thread.

## `std::thread` (`[thread.thread.class]`)

- A `thread` object **uniquely represents** a thread of execution or none; ownership transfers by move, never by copy. `thread::id` is a trivially copyable class with a unique value per live thread and one distinguished value (`id()`) for "no thread"; it is totally ordered, hashable, streamable, and may be reused after a thread is terminated and can no longer be joined. `this_thread::get_id()` never equals `id()`.
- **Constructor** `thread(f, args...)`: `f` and the arguments are `decay_copy`'d **in the constructing thread**, then the new thread calls `INVOKE(copy of f, copies of args...)`; the return value is ignored; if it exits with an uncaught exception, `terminate()` is called. The constructor's completion **synchronizes with** the start of the invocation. Throws `system_error` (`resource_unavailable_try_again`) if the thread can't start. The template constructor is excluded when `decay_t<F>` is `thread`.
- **Joinability**: `joinable()` is `get_id() != id()`. A `thread` that is still joinable when **destroyed or move-assigned over calls `std::terminate()`** (`[thread.thread.destr]`, `[thread.thread.assign]`). `join()` blocks until the thread finishes; completion **synchronizes with** the successful return of `join()`; errors: `resource_deadlock_would_occur` (self-join or detected deadlock), `no_such_process`, `invalid_argument` (not joinable). `detach()` lets the thread run on independently and releases the thread object (`get_id() == id()` afterwards); the implementation frees the thread's resources when it ends.
- `swap`; `static unsigned hardware_concurrency()` (number of hardware thread contexts, or 0 if unknowable).

## `this_thread` (`[thread.thread.this]`)

`get_id()`, `yield()` (opportunity to reschedule), `sleep_until(abs_time)`, `sleep_for(rel_time)` (block the calling thread; no synchronization; may throw timeout-related exceptions).

## Related

[[cpp17-lib-thread]] · [[exception-support]] (`terminate`) · [[function-objects-and-invoke]] (INVOKE) · [[futures-and-async]] (`async` models a thread) · [[execution-policies-and-parallel-algorithms]]
