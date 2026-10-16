---
type: concept
title: "Allocators: requirements, allocator_traits, std::allocator, uses-allocator construction, scoped_allocator_adaptor"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Allocators (`[allocator.requirements]`, `[allocator.traits]`, `[default.allocator]`, `[allocator.uses]`, `[allocator.adaptor]`)

The customization point for how library containers, strings, `match_results`, string streams and similar components obtain memory. Parent: [[cpp17-lib-utilities]]. Polymorphic allocators: [[memory-resources-pmr]]. Container use: [[container-requirements]].

## Who takes an allocator

All string types, all containers **except `array`**, string buffers and string streams, and `match_results` are parameterized by an allocator (`[allocator.requirements]/1`). Code must reach an allocator only through `allocator_traits<A>`, which supplies defaults for every optional member.

## Allocator requirements (Tables 30-31)

An allocator type `X` for value type `T` is a class type (non-class allocators are impossible even though `allocator_traits` would accept the interface). Required: `value_type`; `allocate(n)`, `deallocate(p, n)`; equality (`==`, `!=`) that is an equivalence relation and does not throw; copy and rebinding conversion (`X u(b)` from an allocator of another value type, `Y(u) == b`) that does not throw; move construction that does not throw; `X` is CopyConstructible.

Optional members (the `allocator_traits` default in brackets):

| Member | Default |
|---|---|
| `pointer`, `const_pointer`, `void_pointer`, `const_void_pointer` | `T*` and `pointer_traits<pointer>::rebind<...>` |
| `size_type`, `difference_type` | `make_unsigned_t<difference_type>`, `pointer_traits<pointer>::difference_type` |
| `rebind<U>::other` | `SomeAllocator<U, Args...>` when `X` is `SomeAllocator<T, Args...>` |
| `allocate(n, hint)` | `allocate(n)` |
| `max_size()` | `numeric_limits<size_type>::max() / sizeof(value_type)` |
| `construct(c, args...)` | `::new ((void*)c) C(forward<Args>(args)...)` |
| `destroy(c)` | `c->~C()` |
| `select_on_container_copy_construction()` | returns the allocator unchanged |
| `propagate_on_container_copy_assignment`, `..._move_assignment`, `..._swap` | `false_type` |
| `is_always_equal` | `is_empty<X>::type` |

Semantics worth keeping (`/2-10`):

- `allocate(n)` obtains storage for `n` objects of `T` **without constructing them**; it may throw. `deallocate(p, n)` requires `p` from an earlier `allocate` with the same `n`, and **never throws**. `a1 == a2` means storage from either can be deallocated through the other.
- **Propagation traits**: `true` for copy-assignment/move-assignment/swap means the container copies/moves/swaps its allocator along with its elements; when true the corresponding operation on the allocator must exist and not throw (`Note B`).
- The pointer types must be `NullablePointer`s ([[library-named-requirements]]) whose operations never throw, and `pointer`/`const_pointer` must be random-access and contiguous iterators (so "fancy pointers" are allowed). `static_cast` conversions among the four pointer types must work, and "equivalently-valued" pointers are interchangeable (`/6-8`).
- An allocator may refuse some `T` or some `construct`/`destroy` arguments (instantiation fails); it may fail to support over-aligned types or silently ignore the alignment (`/9-10`).
- **Completeness requirement** (`[allocator.requirements.completeness]`): an allocator class satisfies it if, even for incomplete `T`, `X` and all `allocator_traits<X>` member types other than `value_type` are complete. Needed for containers instantiated with incomplete element types.

## `allocator_traits<Alloc>` (`[allocator.traits]`)

Uniform interface: member types fall back as in the table above; static functions `allocate`, `deallocate`, `construct`, `destroy`, `max_size`, `select_on_container_copy_construction` call the allocator's member if the call is well-formed, else the default. User specializations may change defaults. Container code must construct and destroy **elements** through `allocator_traits<allocator_type>::construct/destroy` (`[container.requirements.general]/3`).

## `pointer_traits` (`[pointer.traits]`)

`pointer_traits<Ptr>` gives `element_type` (`Ptr::element_type`, else `T` for `SomePtr<T, Args>`), `difference_type` (default `ptrdiff_t`), `rebind<U>`, and `pointer_to(r)`; the `T*` specialization uses `addressof`. Related helpers in `<memory>`: `align(alignment, size, ptr, space)` adjusts `ptr` to the next aligned address that leaves `size` bytes (returns null and does nothing if it won't fit; `alignment` must be a power of two); `addressof`; the **pointer-safety** facility (`declare_reachable`, `undeclare_reachable`, `declare_no_pointers`, `undeclare_no_pointers`, `get_pointer_safety` returning `strict`/`relaxed`/`preferred`) which backs the language's safely-derived-pointer rules ([[storage-duration-and-object-lifetime]], `[util.dynamic.safety]`).

## `std::allocator<T>` (`[default.allocator]`)

Stateless; the C++17 interface is minimal: `value_type`, `propagate_on_container_move_assignment` = `true_type`, `is_always_equal` = `true_type`, default/copy/converting constructors (`noexcept`), `allocate(n)`, `deallocate(p, n)`. `allocate` returns storage of `n * sizeof(T)` suitably aligned, obtained from `::operator new` (when and how often it is called is unspecified), and throws `bad_alloc` on failure; `deallocate` uses `::operator delete`. All instances compare equal. Distinct calls must not race and storage events occur in a single total order, each deallocation happening before the next allocation (`[allocator.members]/1`). Satisfies the completeness requirements. (The older members such as `pointer`, `address`, `construct`, `destroy` and the `allocator<void>` specialization are not in this clause; they are the deprecated Annex D interface, see [[deprecated-library-facilities]].)

## Uses-allocator construction (`[allocator.uses]`)

`allocator_arg_t` / `allocator_arg` is the tag that precedes an allocator argument. `uses_allocator<T, Alloc>` is true if `T` has an `allocator_type` convertible from `Alloc` (the program may specialize it for types that accept an allocator via `allocator_arg_t, alloc` first or `alloc` last). **Uses-allocator construction** of `T` with allocator `alloc` and arguments `v...` tries, in order: plain `T(v...)` if `T` does not use allocators; `T(allocator_arg, alloc, v...)`; `T(v..., alloc)`; otherwise ill-formed. `tuple`, `pair`, `variant`, `optional`-like holders and the pmr allocator use it ([[pair-and-tuple]], [[memory-resources-pmr]]).

## `scoped_allocator_adaptor<Outer, Inner...>` (`[allocator.adaptor]`, `<scoped_allocator>`)

An allocator that uses `OuterAlloc` for the container's own storage and passes an **inner allocator** to every element's constructor (via uses-allocator construction), recursively for nested containers. With no inner allocators the outer one is reused. `inner_allocator()` returns `*this` when there are no inner allocators, else the inner adaptor; `outer_allocator()` returns the outer one. `allocate`/`deallocate`/`max_size` forward to the outer allocator; `construct` selects among the three uses-allocator forms using the inner allocator, with the outermost allocator's traits doing the actual construction; propagation traits are the OR of all components (and `is_always_equal` the AND); `select_on_container_copy_construction` applies to each component.

## Related

[[cpp17-lib-utilities]] · [[container-requirements]] · [[memory-resources-pmr]] · [[dynamic-memory-support]] · [[unique-ptr]] and [[shared-ptr-and-weak-ptr]] (allocate through deleters/allocators) · [[library-requirements-and-conformance]] · [[deprecated-library-facilities]] (older `std::allocator` members, Annex D)
