---
type: concept
title: "Container requirements (general, reversible, optional, allocator-aware)"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# General container requirements (`[container.requirements.general]`, `[container.requirements.dataraces]`)

The base contract every standard container (and, via `[strings]`, `basic_string`) meets. Parent: [[cpp17-lib-containers]]. Refinements: [[sequence-container-requirements]], [[associative-container-requirements]], [[unordered-container-requirements]]; invalidation summary: [[iterator-invalidation]]; allocators: [[allocators]].

## Base requirements (Table 83)

With `X` a container of `T`: member types `value_type`, `reference`, `const_reference`, `iterator` (forward-iterator category or better, convertible to `const_iterator`), `const_iterator`, `difference_type`, `size_type`; construction (`X u;`, `X()`, copy, move), destruction, `a = b`, `begin/end/cbegin/cend`, `==`/`!=` (element-wise via `equal`), `swap`, `size`, `max_size`, `empty`. `T` must be `Erasable` from `X`.

- Complexity statements are **only about operations on the contained objects** (`/2`): copying `vector<vector<int>>` is linear even though each inner copy is linear. `swap` and move construction (the rows marked Note A/B) are constant for all standard containers except `array`, where they are linear; move assignment is linear in the table.
- `begin()` of an empty container equals `end()`. `i` and `j` of iterator type may be replaced by `const_iterator` values referring to the same element (`/7`).
- **Reversible containers** (bidirectional or better iterators; Table 84): `reverse_iterator`, `const_reverse_iterator`, `rbegin/rend/crbegin/crend`.
- **Optional operations** (Table 85): `<`, `>`, `<=`, `>=`, lexicographic via `lexicographical_compare`, linear; require `<` to be a total ordering on `T`.
- A **contiguous container** has random-access iterators whose `iterator`/`const_iterator` are contiguous iterators (`array`, `vector` except `vector<bool>`, `basic_string`).

## Element requirements: the "insertable" vocabulary (`/15`)

Given allocator `A`, container `X`, pointer `p` to uninitialized storage, `v` a `T`, `rv` an rvalue `T`, `m` an allocator lvalue:

| Term | Means | Extra |
|---|---|---|
| `DefaultInsertable` | `allocator_traits<A>::construct(m, p)` well-formed | an element is *default-inserted* when so initialized |
| `MoveInsertable` | `construct(m, p, rv)` well-formed | afterwards `*p` equals the old `rv` |
| `CopyInsertable` | MoveInsertable and `construct(m, p, v)` well-formed | `v` unchanged and equal to `*p` |
| `EmplaceConstructible` from `args` | `construct(m, p, args...)` well-formed | |
| `Erasable` | `allocator_traits<A>::destroy(m, p)` well-formed | needed for any container's `value_type` |

For non-allocator-aware containers the terms are defined as if the allocator were `std::allocator<T>`. Element construction/destruction **goes through `allocator_traits::construct/destroy`**, only for the element type, not internal nodes (`/3`).

## Allocator-aware containers (Table 86, `/8`, `/15-16`)

All containers except `array` (and `basic_string`) are allocator-aware:

- Copy construction obtains its allocator from `select_on_container_copy_construction`; move construction move-constructs the allocator (must not throw); all other constructors take a `const allocator_type&`. The allocator is replaced only by assignment or `swap`, and only when the matching `propagate_on_container_copy_assignment` / `move_assignment` / `swap` trait is true.
- Move construction `X(rv)` is constant; `X(rv, m)` is constant if `m == rv.get_allocator()`, otherwise linear (elements must be moved). Move assignment, if the allocator does not propagate, requires `MoveInsertable` and `MoveAssignable` elements and is linear.
- `a.swap(b)` exchanges contents **without invoking move, copy or swap on elements** (except `array`); `Compare`/`Pred`/`Hash` objects are swapped via the swappable idiom; allocators are swapped only if propagation says so, otherwise the behavior is undefined if the allocators differ (`/9`).
- `get_allocator()` returns a copy of the allocator.

## Guarantees common to the containers (`/11-12`)

Unless a specific section says otherwise:

- A throwing single-element `insert`/`emplace`, or `push_back`/`push_front`/`emplace_back`/`emplace_front`, has **no effect**.
- `erase`, `clear`, `pop_back`, `pop_front` never throw; iterator copy/assign never throws; **`swap` never throws and does not invalidate** references, pointers or iterators into the swapped containers.
- No member function or library function taking a container may invalidate iterators or change element values **unless specified** (`/12`) — see [[iterator-invalidation]] for what is specified.

## Data races (`[container.requirements.dataraces]`)

For race analysis the library treats `begin`, `end`, `rbegin`, `rend`, `front`, `back`, `data`, `find`, `lower_bound`, `upper_bound`, `equal_range`, `at`, and (except in associative/unordered) `operator[]` as **const**, so concurrent calls to them are not races. Beyond `[res.on.data.races]`, implementations must avoid races when **different elements** of one container (other than `vector<bool>`) are modified concurrently (`/2`). See [[memory-model-and-data-races]].

## Algorithm-selection hints (`[sequence.reqmts]/2`)

`vector` or `array` should be the default choice; `list`/`forward_list` for frequent middle insertion/erasure; `deque` when insertions and deletions mostly happen at the ends.

## Traits of constructor templates

An `InputIterator` constructor/member or deduction guide must not take part in overload resolution for a type that does not qualify as an input iterator (integral types never qualify); likewise a type is not an allocator unless it has a valid `value_type` and `allocate(size_t)` (`/17`). Deduction guides: [[template-argument-deduction]].

## Related

[[cpp17-lib-containers]] · [[library-named-requirements]] · [[iterator-categories-and-requirements]] · [[uninitialized-memory-algorithms]]
