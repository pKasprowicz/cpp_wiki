---
type: concept
title: "Iterator, pointer and reference invalidation rules for the standard containers"
tags: [cpp17, library, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Iterator invalidation across the containers

Cross-cutting summary of what the draft guarantees about iterators (I), pointers and references (P/R) after container operations. "Invalidated" means the iterator/pointer/reference may no longer be used (except to assign to or destroy it, for iterators). Where the text gives no guarantee, this page says "not guaranteed" and does not assume. Sources: `[container.requirements.general]/11-12`, `[sequence.reqmts]`, `[associative.reqmts]/9-10`, `[unord.req]/9,14-16`, the per-class modifier sections. Parent: [[cpp17-lib-containers]]; background in [[container-requirements]].

## General rules (all containers)

1. **Default**: unless a rule says otherwise, no member function or library function taking a container may invalidate iterators or change element values (`/12`).
2. **`swap`** never invalidates references, pointers or iterators referring to the elements of the swapped containers (`/11.6`).
3. `erase`, `clear`, `pop_back`, `pop_front` never throw (`/11.3`); a throwing single-element insert has no effect (`/11.1-2`).
4. Moving elements between containers by `splice` / `merge` / node-handle `insert` keeps pointers/references valid, and iterators keep referring to their elements but now behave as iterators into the *destination* container (with the unordered-container `merge` exception below).

## Per-container table

| Container | Insert / emplace | Erase | Other |
|---|---|---|---|
| `vector` | If **no reallocation**, I and P/R **before** the insertion point stay valid (nothing is promised for those at/after it). If it reallocates (new size > capacity), **all** I/P/R are invalidated. After `reserve(n)`, no reallocation occurs until size would exceed the capacity | I and P/R **at or after** the erased point are invalidated | `reserve` that reallocates and `shrink_to_fit` that reallocates: all I/P/R and past-the-end; `clear`/`assign`: all and past-the-end |
| `deque` | In the **middle**: all I and P/R invalidated. At **either end**: all I invalidated, **P/R stay valid** | Erasing the **last**: only past-the-end I and I/P/R of the erased elements. Erasing the **first** (not last): only erased. Erasing **neither end**: past-the-end I and I/P/R of **all** elements | `shrink_to_fit`: all and past-the-end; `clear`/`assign`: all |
| `list` | no I/P/R invalidated | only the erased elements | `splice` keeps pointers/references valid (iterators now point into the destination); `remove`, `unique`: only erased; `sort`, `reverse`: no invalidation; `merge` copies no elements |
| `forward_list` | `insert_after`/`emplace_after`: none | `erase_after`: only the erased | `clear`: past-the-end not invalidated; `splice_after`, `merge`, `sort`, `reverse`: no invalidation |
| `array` | n/a (fixed size) | n/a | `swap` is linear (equivalent to `swap_ranges`) |
| `basic_string` | any non-const member except `operator[]`, `at`, `data`, `front`, `back`, `begin`, `rbegin`, `end`, `rend` may invalidate; also passing it by non-const reference to a library function; `shrink_to_fit` that reallocates invalidates all and past-the-end | covered by the same rule | `swap`: as general rule |
| `map`, `multimap`, `set`, `multiset` | **none** | only the erased elements | `extract`: only iterators to the removed element (P/R remain valid but must not be used while the node is detached; they are invalidated again if the node is reinserted); `merge`: transferred elements' P/R stay valid, iterators now point into the target |
| `unordered_*` | P/R **not** affected; I **may all be invalidated** (rehash) unless `(N + n) <= z * B` | only the erased elements (and the relative order of remaining elements is preserved) | `rehash`/`reserve`: I invalidated, P/R **not**; `extract`: only the removed element's I; `merge`: transferred elements' I and **all** the target's I invalidated, source's remaining I stay valid |
| `string_view` | n/a | n/a | invalidation of any pointer in `[data(), data()+size())` invalidates the view's iterators, pointers and references (`[string.view.iterators]/2`) |

(`z` is the max load factor, `B` the bucket count, `N` the old element count, `n` the number of inserted elements.)

## What the draft does *not* spell out

- For `vector`, the text states validity only **before** the insertion/erase point; saying that iterators after the point are invalid is an inference from "invalidates iterators and references at or after the point of the erase" for erasure and from the reallocation text for insertion.
- Container adaptors (`stack`, `queue`, `priority_queue`) expose no iterators; their underlying container rules apply to whatever operations the adaptor performs ([[container-adaptors]]).

## Related

[[container-requirements]] · [[sequence-container-requirements]] · [[associative-container-requirements]] · [[unordered-container-requirements]] · [[array-and-vector]] · [[deque-and-lists]] · [[iterator-categories-and-requirements]] · [[algorithm-requirements]]
