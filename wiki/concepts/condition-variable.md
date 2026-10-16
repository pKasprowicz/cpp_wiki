---
type: concept
title: "condition_variable and condition_variable_any"
tags: [cpp17, library, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Condition variables (`<condition_variable>`, `[thread.condition]`)

Parent: [[cpp17-lib-thread]]. They wait on locks from [[mutexes-and-locks]]; timeouts follow [[threads]] and [[chrono-and-ratio]].

## Semantics (`[thread.condition]`)

- A condition variable blocks a thread until another thread signals that some condition may hold, or until a time. `condition_variable` waits only on `unique_lock<mutex>` (allowing maximum efficiency); **`condition_variable_any`** waits on any lock type meeting BasicLockable.
- Concurrent calls of `wait*`, `notify_one`, `notify_all` are allowed. `notify_one`/`notify_all` execute atomically. A wait executes in **three atomic parts**: (1) release the mutex and enter the waiting state, (2) unblock, (3) reacquire the lock. As if all notifications and each wait-part occur in a single unspecified total order consistent with happens-before. Construction/destruction need not be synchronized; destroying requires that no thread is blocked on it.
- `notify_one` unblocks one of the waiting threads (if any); `notify_all` unblocks all.

## `condition_variable` (`[thread.condition.condvar]`)

- Standard-layout; constructor may throw `system_error` (`resource_unavailable_try_again`).
- Every wait requires: the `unique_lock` **owns** its mutex and the mutex is locked by the caller, and either no other thread is waiting on this variable or all concurrently waiting threads use the **same mutex**.
- `wait(lock)`: atomically unlocks and blocks; when unblocked it locks again and returns. It may return when signaled **or spuriously**, so waits are normally paired with a predicate: `wait(lock, pred)` loops until `pred()` is true (equivalent to `while (!pred()) wait(lock);`). If the postcondition (lock owned and mutex locked) cannot be met, **`terminate()` is called**; `wait` itself throws nothing.
- `wait_until(lock, abs_time)` / `wait_for(lock, rel_time)` return `cv_status::timeout` if the timeout expired, else `cv_status::no_timeout`; predicate versions return `pred()`'s final value. If a timed wait exits by exception, the lock is reacquired first. May throw timeout-related exceptions or what `pred` throws.

## `condition_variable_any` (`[thread.condition.condvarany]`)

Same interface with `Lock` templated (BasicLockable); constructor may also throw `bad_alloc`; adds `operation_not_permitted` as an error condition. Waits unlock `lock` and relock it as described above.

## `notify_all_at_thread_exit(cond, lk)` (`[thread.condition.nonmember]`)

Requires `lk` locked by the caller and (no other waiters, or same mutex for all waiters). Transfers ownership of the lock to internal storage and schedules `cond.notify_all()` for when the current thread exits, **after all thread-storage-duration objects of the thread are destroyed**; the implied `lk.unlock()` is sequenced after those destructions. It is the tool for waking waiters only after the thread's `thread_local` objects are gone ([[futures-and-async]] uses the same idea for `*_at_thread_exit`).

## Related

[[mutexes-and-locks]] · [[threads]] · [[futures-and-async]] · [[exception-support]] (`terminate`) · [[memory-model-and-data-races]]
