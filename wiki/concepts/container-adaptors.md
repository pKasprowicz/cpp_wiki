---
type: concept
title: "Container adaptors: stack, queue, priority_queue"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Container adaptors (`[container.adaptors]`)

`stack`, `queue` and `priority_queue` restrict an existing sequence container to an abstract data type. Parent: [[cpp17-lib-containers]].

## Common rules (`[container.adaptors.general]`)

- Each takes a `Container` template parameter; every constructor takes a container object that is **copied (or moved) into the member `c`**. If the container accepts an allocator, a compatible allocator can be passed to the adaptor's constructor (those constructors take part in overload resolution only if `uses_allocator_v<container_type, Alloc>` is true) — see [[allocators]].
- No `swap` throws unless swapping the `Container` or `Compare` throws. Deduction guides are excluded when an iterator/allocator/comparator/container parameter has the wrong kind of type or `uses_allocator_v<Container, Allocator>` is false.
- Adaptors expose **no iterators**, so invalidation questions reduce to the underlying container ([[iterator-invalidation]]).

## The three adaptors

| Adaptor | Required container operations | Default container | Interface |
|---|---|---|---|
| `stack<T, Container>` | `back()`, `push_back()`, `pop_back()` (so `vector`, `list`, `deque`) | `deque<T>` | `push`, `emplace` (returns a reference to the new top, i.e. returns `c.emplace_back(...)`), `top`, `pop`, `empty`, `size`, `swap`; relational operators compare the underlying `c` |
| `queue<T, Container>` | `front()`, `back()`, `push_back()`, `pop_front()` (`list`, `deque`) | `deque<T>` | `push`, `emplace` (returns `reference` — `c.emplace_back(...)`), `front`, `back`, `pop`, `empty`, `size`, `swap`; relational operators compare `c` |
| `priority_queue<T, Container, Compare>` | random-access iterators and `front()`, `push_back()`, `pop_back()` (`vector`, `deque`); `Compare` must define a strict weak ordering | `vector<T>`, `less<T>` | `push` (= `c.push_back(x)` then `push_heap`), `emplace`, `top`, `pop` (= `pop_heap` then `pop_back`), `empty`, `size`, `swap` |

- `priority_queue` constructors call `make_heap(c.begin(), c.end(), comp)` after initializing `c` (and after `c.insert(c.end(), first, last)` for the range form). `top()` is the largest element by `comp`.
- `stack`/`queue` support comparison operators that compare the underlying containers lexicographically (`==`, `!=`, `<`, ...); `priority_queue` has none.

## Related

[[array-and-vector]] · [[deque-and-lists]] · [[sorting-and-set-algorithms]] (heap algorithms) · [[container-requirements]]
