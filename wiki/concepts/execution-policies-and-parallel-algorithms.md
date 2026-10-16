---
type: concept
title: "Execution policies and parallel algorithm semantics"
tags: [cpp17, library, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Execution policies and parallel algorithms (`[execpol]`, `[algorithms.parallel]`)

Parent: [[cpp17-lib-algorithms]] (and [[cpp17-lib-utilities]] for `<execution>`). Parallel overloads exist for most `<algorithm>` and `<numeric>` functions and for the `uninitialized_*`/`destroy` family ([[uninitialized-memory-algorithms]], [[numeric-operations]]). Concurrency background: [[memory-model-and-data-races]], [[cpp17-lib-thread]].

## Execution policy types (`<execution>`)

| Type | Object | Meaning |
|---|---|---|
| `execution::sequenced_policy` | `execution::seq` | execution may **not** be parallelized; all element access functions run in the calling thread |
| `execution::parallel_policy` | `execution::par` | may be parallelized; element access functions run in the calling thread or in library-created threads; invocations in the same thread are indeterminately sequenced |
| `execution::parallel_unsequenced_policy` | `execution::par_unseq` | may be parallelized *and* vectorized; invocations may be interleaved/unsequenced even within one thread |
| implementation-defined policy types | — | semantics implementation-defined |

`is_execution_policy<T>` (and `is_execution_policy_v`) is a UnaryTypeTrait true for standard and implementation-defined policy types; **adding specializations is undefined behavior**. Parallel algorithm overloads take part in overload resolution only if `is_execution_policy_v<decay_t<ExecutionPolicy>>` is true (`[algorithms.parallel.overloads]/4`).

## Terms (`[algorithms.parallel.defns]`)

A **parallel algorithm** is a function template with a template parameter named `ExecutionPolicy`. It accesses objects through **element access functions**: all operations of the iterator categories used, operations on the sequence elements that the specification requires, user-provided function objects, and operations on those objects.

## Overload shape (`[algorithms.parallel.overloads]`)

Each parallel overload adds a **first** template parameter `ExecutionPolicy` and a **first** function parameter `ExecutionPolicy&&`. Semantics are those of the non-policy overload unless stated. Complexity is **relaxed**: a bound "at most/exactly `expr`" that does not specify the number of assignments or swaps becomes `O(expr)`. Where the sequential overload accepts input iterators, the parallel overload often names a forward iterator instead (for example the `partition_copy` and `is_partitioned` requirements in `[alg.partitions]`).

## Constraints on user code (`[algorithms.parallel.user]`, `[algorithms.parallel.exec]`)

- Predicates, comparison functions and operation objects passed to parallel algorithms **shall not directly or indirectly modify objects through their arguments**, nor rely on the identity of the argument objects.
- Unless stated otherwise (e.g. `for_each`), the implementation may make arbitrary **copies of elements** whose type is trivially copy-constructible and trivially destructible.
- With `parallel_unsequenced_policy`, invocations may be interleaved on one thread, so **blocking synchronization (e.g. mutexes) risks deadlock**: *vectorization-unsafe* standard library functions — those specified to synchronize with another invocation (other than allocation/deallocation functions) — may not be called by user code run under that policy.
- Forward progress: library-created threads provide *parallel* forward progress if `std::thread` threads provide concurrent forward progress (otherwise implementation-defined) for `par`, and *weakly parallel* for `par_unseq`. The invoking thread either blocks with forward-progress delegation or itself executes element access functions until the algorithm finishes ([[abstract-machine-and-observable-behavior]]).

## Exceptions

If temporary memory for parallelization cannot be obtained, the algorithm throws `bad_alloc`. If an element access function exits via an uncaught exception, behavior is determined by the policy; **all three standard policies call `std::terminate()`** (`[execpol.seq]/2`, `[execpol.par]/2`, `[execpol.parunseq]/2`).

## Related

[[cpp17-lib-algorithms]] · [[algorithm-requirements]] · [[atomics-and-memory-order]] · [[exception-support]] (`terminate`)
