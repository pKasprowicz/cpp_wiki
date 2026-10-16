---
type: concept
title: "Memory model and data races"
tags: [cpp17, language-core, cross-cutting, concurrency, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Memory model and data races

Defined in `[intro.memory]` and `[intro.multithread]` of [[cpp17-general-principles]]. The atomic operations and mutexes that create synchronization live in the library clauses (not yet ingested; see the clause map on [[n4659-cpp17-draft-standard]]).

## Memory layout basics (`[intro.memory]`)

- The fundamental storage unit is the **byte**: large enough for any member of the basic execution character set and for the eight-bit UTF-8 code units; its bit count is implementation-defined. Every byte has a unique address (`/1`).
- A **memory location** is an object of scalar type, or a maximal run of adjacent bit-fields of nonzero width. Distinct memory locations can be accessed by different threads without interference (`/3`).

## Threads (`[intro.multithread]`)

A thread is a single flow of control starting at a top-level function invocation. Every thread can potentially access every object and function. A hosted implementation can run multiple threads; in a freestanding one that is implementation-defined (`/1`).

## Ordering relations (`[intro.races]`)

| Relation | Rule of thumb (paraphrased) |
|---|---|
| modification order | each atomic object has one total order of its modifications (`/4`) |
| release sequence | headed by a release op A: A, then later side effects by the same thread or atomic read-modify-writes (`/5`) |
| synchronizes with | library-defined pairings, e.g. an atomic store-release with a load-acquire reading its value (`/6`) |
| carries a dependency to | value of A is an operand of B (with exceptions such as `std::kill_dependency`, left operand of `&&`, `||`, `?:`, `,`), or A writes a scalar that B reads with A sequenced before B, or transitively (`/7`) |
| dependency-ordered before | release on M paired with a consume of a value from its release sequence in another thread, or transitively (`/8`) |
| inter-thread happens before | synchronizes-with, dependency-ordered-before, or compositions with sequenced-before (`/9`) |
| happens before | sequenced before, or inter-thread happens before; no cycles allowed (`/10`) |
| strongly happens before | sequenced before, or synchronizes with, closed under transitivity (`/11`) |

**Visible side effect** (`/12`): A happens before B and no other side effect X on the location has A happen-before X happen-before B. A non-atomic scalar read must yield the value of the visible side effect. For atomics, coherence rules (`/13–17`) constrain which stored values later reads may observe relative to modification order.

## Data races (`[intro.races]/20`)

Two evaluations **conflict** if one modifies a memory location and the other reads or modifies it (`/2`). A program execution has a **data race** if it contains two *potentially concurrent* conflicting actions, at least one non-atomic, with neither happening before the other (apart from the signal-handler special case). A data race is **undefined behavior**.

**Signal-handler special case (`/21`):** two accesses to the same `volatile std::sig_atomic_t` object do not race when they occur in the same thread, even if one is inside a signal handler.

## Forward progress (`[intro.progress]`)

- Lock-free executions: if only one thread is unblocked in a library function, its lock-free execution must complete; among concurrently running lock-free executions, at least one should complete (`/2`).
- **Execution steps:** thread termination, volatile glvalue access, or completion of a library I/O call / synchronization operation / atomic operation (`/3`). A blocking library call counts as continuously executing steps while it waits (`/4`).
- Guarantee tiers, strongest to weakest (`/13`): **concurrent** (thread eventually progresses while not terminated) > **parallel** (guarantee applies once the thread has executed a step) > **weakly parallel** (none). Whether `main`'s thread and `std::thread`-created threads provide concurrent guarantees is implementation-defined (`/8`).
- *Blocks with forward progress guarantee delegation* (`/14`): while P is blocked on set S, at least one thread in S must have guarantees at least as strong as P's.
- Should-requirement: the last value in modification order written by an atomic/synchronization operation becomes visible to other threads in finite time (`/18`).

## Related

[[sequencing-and-evaluation-order]] · [[abstract-machine-and-observable-behavior]] · [[storage-duration-and-object-lifetime]]
