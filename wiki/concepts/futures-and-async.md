---
type: concept
title: "future, promise, shared_future, packaged_task and async"
tags: [cpp17, library, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Futures (`<future>`, `[futures]`)

One-shot communication of a value or an exception between threads. Parent: [[cpp17-lib-thread]]. Thread creation: [[threads]]. Errors: [[error-codes-and-system-error]], [[exception-support]] (`exception_ptr`).

## Error reporting (`[futures.errors]`, `[futures.future_error]`)

`future_errc`: `broken_promise`, `future_already_retrieved`, `promise_already_satisfied`, `no_state` (distinct, non-zero values). `future_category()` is a category named `"future"`; `make_error_code`/`make_error_condition` overloads exist. **`future_error`** derives from `logic_error` ([[standard-exception-classes]]). `launch` is a bitmask type with `async` and `deferred`; `future_status` is `ready`, `timeout`, `deferred`.

## Shared state (`[futures.state]`)

- A **shared state** holds status plus a possibly-not-yet-computed result (a value, possibly `void`, or an exception). An **asynchronous provider** (`promise`, `packaged_task`, `async`) writes it; an **asynchronous return object** (`future`, `shared_future`) reads it. A *waiting function* may block until ready; a *timed* one can return early on timeout.
- A provider **makes the state ready** by marking it and unblocking waiters; it **abandons** it by storing a `future_error` with `broken_promise` (if not ready), making it ready, and releasing it. **Releasing** a state destroys it if it is the last reference and does not block — **except** when the state was created by `async`, is not yet ready, and this is the last reference: then it may block (this is why an `async` future's destructor can wait).
- Setting the result **synchronizes with** the successful return of waiting/ready-detecting functions. `*_at_thread_exit` functions delay readiness until after the thread's thread-storage objects are destroyed. Concurrent access to the same result may conflict.

## Providers and return objects

| Type | Role and key rules |
|---|---|
| `promise<R>` (also `promise<R&>`, `promise<void>`) | write side. Move-only. `get_future()` once (else `future_error`: `future_already_retrieved` or `no_state`); `set_value`, `set_exception(exception_ptr)` (non-null) store atomically and make the state ready — a second set throws `future_error(promise_already_satisfied)`; `set_value_at_thread_exit`, `set_exception_at_thread_exit`. The destructor/move-assignment **abandons** the state. Allocator-extended constructor |
| `future<R>` | read side, **move-only**, one consumer. `valid()` is true only with a shared state; calling anything except destructor, move assignment, `share()` and `valid()` on an invalid future is **undefined**. `get()` waits, returns the value as an rvalue (or the reference for `future<R&>`, nothing for `void`) **or throws the stored exception**, then releases the state (`valid()` becomes false). `wait()`, `wait_for(rel)`, `wait_until(abs)` (return `future_status`; a deferred state returns `deferred` without waiting). `share()` converts to `shared_future` |
| `shared_future<R>` | copyable, many consumers; `get()` returns a const reference (or `R&`/void) and does not invalidate; same wait functions |
| `packaged_task<R(Args...)>` | wraps a callable; move-only; invoking it (`operator()`) stores the result *or the exception* in the shared state and makes it ready; throws `future_error` (`no_state`, or `promise_already_satisfied` if already invoked); `get_future()` once; `valid()`, `reset()`, `make_ready_at_thread_exit(args...)`; the callable must be copy-equivalent |
| `async` | below |

## `async` (`[futures.async]`)

`async(launch policy, f, args...)` returns `future<invoke_result_t<decay_t<F>, decay_t<Args>...>>`; `async(f, args...)` behaves as `launch::async | launch::deferred` (the implementation may choose).

- **`launch::async`**: runs `INVOKE(decay_copy(f), decay_copy(args)...)` as if in a new thread (copies made in the calling thread); the thread is held by the shared state, and any waiting function on the future **blocks until that thread finishes, as if joined**; return value or exception goes into the state.
- **`launch::deferred`**: stores the copies as a *deferred function*; the first **non-timed waiting function** on the future runs it in the calling thread (timed waits report `deferred` without running it); the state becomes ready only when it completes.
- No recognized policy bit set: undefined behavior. Regardless of policy, the call to `async` **synchronizes with** the start of `f`, and `f`'s completion is sequenced before the state becomes ready. Throws `system_error(resource_unavailable_try_again)` if `async` policy can't start a thread, or `bad_alloc`.

## Related

[[threads]] · [[mutexes-and-locks]] · [[condition-variable]] · [[exception-support]] · [[function-objects-and-invoke]] (INVOKE, `decay_copy`) · [[atomics-and-memory-order]]
