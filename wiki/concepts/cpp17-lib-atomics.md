---
type: concept
title: "C++17 clause 32: atomic operations library"
tags: [cpp17, library, standard-clause, concurrency]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 32: Atomic operations library (`[atomics]`)

About 4,400 words; 13 labelled sections. Fine-grained atomic access to shared data, finer than locks. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Content | Wiki page |
|---|---|---|---|
| 32.2 `<atomic>` synopsis | `[atomics.syn]` | declarations, `ATOMIC_*_LOCK_FREE` macros | — |
| 32.3 Type aliases | `[atomics.alias]` | `atomic_int8_t`..`atomic_uintptr_t` | [[atomics-and-memory-order]] |
| 32.4 Order and consistency | `[atomics.order]` | `memory_order`, seq_cst total order | [[atomics-and-memory-order]] |
| 32.5 Lock-free property | `[atomics.lockfree]` | macros, `is_lock_free` | [[atomics-and-memory-order]] |
| 32.6 Class template `atomic` | `[atomics.types.generic]` | primary, integral, pointer forms, operations | [[atomics-and-memory-order]] |
| 32.7 Non-member functions | `[atomics.nonmembers]` | `atomic_f` / `atomic_f_explicit` | [[atomics-and-memory-order]] |
| 32.8 Flag type | `[atomics.flag]` | `atomic_flag` | [[atomics-and-memory-order]] |
| 32.9 Fences | `[atomics.fences]` | `atomic_thread_fence`, `atomic_signal_fence` | [[atomics-and-memory-order]] |

## Related

[[memory-model-and-data-races]] (the language-level model) · [[cpp17-lib-thread]] · [[shared-ptr-and-weak-ptr]] (atomic access functions for `shared_ptr`)
