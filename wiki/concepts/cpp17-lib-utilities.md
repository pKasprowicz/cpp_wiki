---
type: concept
title: "C++17 clause 23: general utilities library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 23: General utilities library (`[utilities]`)

About 54,000 words; 310 labelled sections — the largest library clause. It holds the vocabulary types, the memory and allocator machinery, function objects, type traits and time utilities that every other library clause builds on. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header(s) | Content | Wiki page |
|---|---|---|---|---|
| 23.2 Utility components | `[utility]` | `<utility>` | `swap`, `exchange`, `forward`/`move`, `as_const`, `declval`, `to_chars`/`from_chars` | [[utility-move-forward-swap]] |
| 23.3 Integer sequences | `[intseq]` | `<utility>` | `integer_sequence`, `index_sequence` | [[utility-move-forward-swap]] |
| 23.4 Pairs | `[pairs]` | `<utility>` | `pair`, `make_pair`, piecewise construction | [[pair-and-tuple]] |
| 23.5 Tuples | `[tuple]` | `<tuple>` | `tuple`, `tie`, `tuple_cat`, `apply`, `make_from_tuple` | [[pair-and-tuple]] |
| 23.6 Optional objects | `[optional]` | `<optional>` | `optional`, `nullopt`, `bad_optional_access` | [[optional]] |
| 23.7 Variants | `[variant]` | `<variant>` | `variant`, `visit`, `monostate` | [[variant]] |
| 23.8 Storage for any type | `[any]` | `<any>` | `any`, `any_cast` | [[any-type]] |
| 23.9 Bitsets | `[bitset]` | `<bitset>` | fixed-size bit sequence | [[bitset]] |
| 23.10 Memory | `[memory]` | `<memory>`, `<cstdlib>` | `pointer_traits`, pointer safety, `align`, `allocator_traits`, `allocator`, `uses_allocator`, `uninitialized_*`, `destroy`, C allocation | [[allocators]], [[uninitialized-memory-algorithms]] |
| 23.11 Smart pointers | `[smartptr]` | `<memory>` | `unique_ptr`, `shared_ptr`, `weak_ptr`, `enable_shared_from_this`, atomic access | [[unique-ptr]], [[shared-ptr-and-weak-ptr]] |
| 23.12 Memory resources | `[mem.res]` | `<memory_resource>` | `memory_resource`, `polymorphic_allocator`, pool and monotonic resources | [[memory-resources-pmr]] |
| 23.13 Scoped allocators | `[allocator.adaptor]` | `<scoped_allocator>` | `scoped_allocator_adaptor` | [[allocators]] |
| 23.14 Function objects | `[function.objects]` | `<functional>` | INVOKE, `reference_wrapper`, operator functors, `not_fn`, `bind`, `mem_fn`, `function`, searchers, `hash` | [[function-objects-and-invoke]], [[std-function]] |
| 23.15 Type traits | `[meta]` | `<type_traits>` | unary/binary/transformation traits, `conjunction` etc. | [[type-traits]] |
| 23.16 Rational arithmetic | `[ratio]` | `<ratio>` | `ratio`, SI prefixes | [[chrono-and-ratio]] |
| 23.17 Time utilities | `[time]` | `<chrono>`, `<ctime>` | `duration`, `time_point`, clocks | [[chrono-and-ratio]] |
| 23.18 `type_index` | `[type.index]` | `<typeindex>` | wrapper of `type_info` for use as a key | [[type-identification-rtti]] |
| 23.19 Execution policies | `[execpol]` | `<execution>` | `sequenced_policy`, `parallel_policy`, `parallel_unsequenced_policy` | [[execution-policies-and-parallel-algorithms]] |

## Cross-clause themes

- **Constrained templates instead of concepts**: nearly every class template here says a constructor "shall not participate in overload resolution unless ..." in terms of [[type-traits]], and is conditionally `explicit` (`pair`, `tuple`, `optional`, `variant`). Rules for deduction guides in `pair`, `tuple`, `optional`, `function`, `unique_ptr`: [[template-argument-deduction]].
- **Value-wrapper triad**: [[optional]] (value or nothing), [[variant]] (one of N types), [[any-type]] (any copyable type, type-erased). None of them allocates for the contained value except `any`, which may for large objects.
- **Allocator awareness**: `pair`, `tuple`, `variant` (and containers) support uses-allocator construction ([[allocators]]); `std::function` lost allocator constructors in this draft ([[std-function]]).
- **Exceptions defined here**: `bad_optional_access`, `bad_variant_access`, `bad_any_cast`, `bad_weak_ptr`, `bad_function_call` ([[standard-exception-classes]]).
- **`hash` specializations** are spread across the clause (`optional`, `variant`, `bitset`, smart pointers, `type_index`); the primary rules are in [[function-objects-and-invoke]].

## Related

[[cpp17-lib-containers]] · [[cpp17-lib-introduction]] · [[library-named-requirements]] · [[cpp17-lib-thread]]
