---
type: concept
title: "Polymorphic memory resources (std::pmr)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Memory resources and `polymorphic_allocator` (`[mem.res]`, `<memory_resource>`)

Run-time-swappable allocation. Parent: [[cpp17-lib-utilities]]. Compare compile-time allocator types in [[allocators]].

## `memory_resource` (`[mem.res.class]`)

Abstract interface to an unbounded family of memory sources. Public non-virtual `allocate(bytes, alignment)`, `deallocate(p, bytes, alignment)`, `is_equal(other)` forward to the private virtuals `do_allocate`, `do_deallocate`, `do_is_equal`. A derived class must: return storage of at least `bytes` aligned as requested (or to `max_align` if that alignment is unsupported), throw an appropriate exception on failure, make `do_deallocate` non-throwing and require `p` to come from `allocate(bytes, alignment)` on an *equal* resource, and make `do_is_equal` true iff memory from one can be freed through the other. `a == b` is `&a == &b || a.is_equal(b)`; `alignment` must be a power of two.

## `pmr::polymorphic_allocator<T>` (`[mem.poly.allocator.class]`)

Conforms to the Allocator requirements, but two instances of the same specialization may use different resources, so containers can vary their allocation at run time without changing their type. Default construction uses `get_default_resource()`; a non-null `memory_resource*` may be passed; converting construction copies the resource. `allocate(n)`/`deallocate(p, n)` forward to `resource()->allocate(n*sizeof(T), alignof(T))`. `construct` performs **uses-allocator construction** with `resource()` (including piecewise `pair` construction with the three-way rule of `[mem.poly.allocator.mem]/9`); `destroy` calls the destructor. `select_on_container_copy_construction()` returns a default-constructed `polymorphic_allocator` (so copied containers use the *default* resource). Two allocators are equal iff their resources are equal. `pmr::` aliases for `string`, `vector`, `deque`, `list`, `forward_list`, `map`/`set` families, `unordered_*` and `regex`-related types exist in their headers.

## Program-wide resources (`[mem.res.global]`)

- `new_delete_resource()` — a static object using `::operator new`/`delete`; every call returns the same pointer; equal only to itself.
- `null_memory_resource()` — `allocate` always throws `bad_alloc`; `deallocate` does nothing; same pointer every call.
- The **default memory resource pointer** starts as `new_delete_resource()`; `set_default_resource(r)` installs `r` (null resets to `new_delete_resource()`) and returns the previous one; `get_default_resource()` reads it. These are race-free, and `set_default_resource` synchronizes with later `set`/`get` calls.

## Concrete resources

| Class | Behavior |
|---|---|
| `unsynchronized_pool_resource`, `synchronized_pool_resource` (`[mem.res.pool]`) | General-purpose pools of fixed block sizes. Each request goes to the pool for the smallest block that fits; an exhausted pool takes a new chunk from the **upstream** resource, chunk sizes growing geometrically; requests larger than the biggest pool pass straight to upstream; the resource frees all its memory on destruction even if blocks were not deallocated. `pool_options` (`max_blocks_per_chunk`, `largest_required_pool_block`) tunes it (zero or over-limit values mean implementation-defined defaults). The synchronized variant is thread-safe (may keep thread-specific pools); the unsynchronized one must not be shared across threads. Holds a pointer to, but does not own, upstream |
| `monotonic_buffer_resource` (`[mem.res.monotonic.buffer]`) | Fast bump allocation: `deallocate` does nothing so memory only grows until the resource is destroyed (or `release()` is called). An optional initial buffer is used first, then upstream buffers of geometrically growing size. Not synchronized; frees everything on destruction |

Each concrete resource's `is_equal` is true only for another object of the same class that is the same object (`this == dynamic_cast<const X*>(&other)`).

## Related

[[allocators]] · [[cpp17-lib-utilities]] · [[array-and-vector]] · [[basic-string]] · [[ordered-associative-containers]] (pmr aliases) · [[dynamic-memory-support]]
