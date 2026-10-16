---
title: "Index shard: concepts — library foundations (clauses 20-24)"
---
# Index shard: concepts — library foundations (clauses 20-24)

Library introduction, language support, diagnostics, general utilities, strings. One line per page. Directory of shards: `wiki/index.md`. Other library shards: `concepts-library-containers-algorithms`, `concepts-library-text-io-numerics-concurrency`.

## Clause 20 — library introduction

- [[cpp17-lib-introduction]] — Clause 20 overview: thirteen library categories, section map to the pages below.
- [[library-requirements-and-conformance]] — How library text is read; headers and freestanding set; what programs may not do (namespace `std`, reserved names, replacement/handler functions); latitude and duties of implementations; differences from the C standard library (Annex C.5).
- [[library-named-requirements]] — EqualityComparable ... Destructible, Swappable, NullablePointer, Hash; map of the other named requirements across the library.

## Clause 21 — language support

- [[cpp17-lib-language-support]] — Clause 21 overview: `<cstddef>`, `byte`, `exit`/`quick_exit`, `initializer_list`, `<csignal>` signal-safety.
- [[numeric-limits]] — `numeric_limits` members and meaning, `<climits>`, `<cfloat>`.
- [[dynamic-memory-support]] — Global `operator new`/`delete` families, replaceability, `new_handler`, `launder`, hardware interference sizes.
- [[exception-support]] — `exception`, `terminate` handlers, `uncaught_exceptions`, `exception_ptr`, `nested_exception`.
- [[type-identification-rtti]] — `type_info`, `bad_cast`, `bad_typeid`, `type_index`.

## Clause 22 — diagnostics

- [[cpp17-lib-diagnostics]] — Clause 22 overview: assertions, `errno`, error model.
- [[standard-exception-classes]] — `logic_error`/`runtime_error` hierarchy and a table of every standard exception type with its base class.
- [[error-codes-and-system-error]] — `error_category`, `error_code`, `error_condition`, `errc`, `system_error`.

## Clause 23 — general utilities

- [[cpp17-lib-utilities]] — Clause 23 overview with a 19-row section map.
- [[utility-move-forward-swap]] — `swap`, `exchange`, `forward`/`move`, `declval`, `in_place` tags, `integer_sequence`, `to_chars`/`from_chars`.
- [[pair-and-tuple]] — Conditional explicit constructors, piecewise construction, `tie`, `tuple_cat`, `apply`, comparisons.
- [[optional]] — `optional<T>`: in-place storage, assignment rules, comparisons with `nullopt` and values.
- [[variant]] — `variant`: valueless state, converting constructor, `get_if`, `visit`, comparison order.
- [[any-type]] — `any`: copyable type erasure, `any_cast` and `bad_any_cast`.
- [[bitset]] — Fixed-size bit sequence, string/integer conversion, errors.
- [[allocators]] — Allocator requirements, `allocator_traits`, `std::allocator`, uses-allocator construction, `scoped_allocator_adaptor`, `pointer_traits`.
- [[memory-resources-pmr]] — `memory_resource`, `polymorphic_allocator`, pool and monotonic resources, default resource.
- [[uninitialized-memory-algorithms]] — `uninitialized_*`, `destroy`, `addressof`, C allocation functions.
- [[unique-ptr]] — `unique_ptr`, deleters, array form, `make_unique`.
- [[shared-ptr-and-weak-ptr]] — `shared_ptr`, `weak_ptr`, aliasing constructor, `enable_shared_from_this`, atomic access functions.
- [[function-objects-and-invoke]] — INVOKE, `reference_wrapper`, operator functors, `not_fn`, `bind`, `mem_fn`, searchers, `hash`.
- [[std-function]] — `std::function`: Lvalue-Callable, null target, `bad_function_call`, no allocator constructors.
- [[type-traits]] — Unary/binary/transformation traits, `decay`, `common_type`, `invoke_result`, `conjunction`.
- [[chrono-and-ratio]] — `ratio`, `duration`, `time_point`, clocks, literals.
- [[execution-policies-and-parallel-algorithms]] — `seq`/`par`/`par_unseq`, element access functions, constraints on user code, exceptions.

## Clause 24 — strings

- [[cpp17-lib-strings]] — Clause 24 overview and C string utility headers.
- [[char-traits]] — Character traits requirements and the four specializations.
- [[basic-string]] — `basic_string`: invalidation, null-terminated `data()`, operations, `stoi`/`to_string`.
- [[string-view]] — `basic_string_view`: non-owning view, operations, invalidation.
