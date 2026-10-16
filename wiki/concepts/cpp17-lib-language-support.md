---
type: concept
title: "C++17 clause 21: language support library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 21: Language support library (`[language.support]`)

About 10,000 words; 63 labelled sections. These are the library parts that the *language itself* calls implicitly (allocation functions behind `new`, `std::terminate`, `type_info` for `typeid`, `initializer_list` for braced lists) plus the C-compatibility headers. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Content | Wiki page |
|---|---|---|---|
| 21.2 Common definitions | `[support.types]` | `<cstddef>`, `<cstdlib>`; `nullptr_t`, `NULL`, `offsetof`, `size_t`, `ptrdiff_t`, `max_align_t`, `byte` | below |
| 21.3 Implementation properties | `[support.limits]` | `<limits>`, `<climits>`, `<cfloat>`; `numeric_limits` | [[numeric-limits]] |
| 21.4 Integer types | `[cstdint]` | `<cstdint>` = C `<stdint.h>` | below |
| 21.5 Start and termination | `[support.start.term]` | `_Exit`, `abort`, `atexit`, `exit`, `at_quick_exit`, `quick_exit` | below, [[program-startup-and-termination]] |
| 21.6 Dynamic memory management | `[support.dynamic]` | `<new>`: global `operator new`/`delete`, `bad_alloc`, `new_handler`, `launder`, interference sizes | [[dynamic-memory-support]] |
| 21.7 Type identification | `[support.rtti]` | `type_info`, `bad_cast`, `bad_typeid` | [[type-identification-rtti]] |
| 21.8 Exception handling | `[support.exception]` | `exception`, `bad_exception`, `terminate`, `uncaught_exceptions`, `exception_ptr`, `nested_exception` | [[exception-support]] |
| 21.9 Initializer lists | `[support.initlist]` | `initializer_list<E>` | below |
| 21.10 Other runtime support | `[support.runtime]` | `<cstdarg>`, `<csetjmp>`, `<csignal>`, signal-safety | below |

## Common definitions (`[support.types]`)

- `<cstddef>`/`<cstdlib>` match the C `<stddef.h>`/`<stdlib.h>` except they do not declare `wchar_t` (it is a keyword) (`[cstddef.syn]/1`, `[cstdlib.syn]/1`).
- `nullptr_t` is the type of `nullptr`; `NULL` is an implementation-defined null pointer constant (`[support.types.nullptr]`).
- `offsetof(type, member)` follows C but applies conditionally-supported semantics to non-standard-layout classes; never type-dependent, value-dependent iff `type` is; undefined for static data members and member functions; never throws and `noexcept(offsetof(...))` is true (`[support.types.layout]/1`). `size_t` is an unsigned type big enough for any object size; `ptrdiff_t` a signed type for array-subscript differences; `max_align_t` has alignment at least that of every scalar type (`/2-5`). See [[cpp17-basic-concepts]] for alignment.
- **`std::byte`** is declared as `enum class byte : unsigned char` with `<<`, `>>` (templated on integral shift type), `|`, `&`, `^`, `~`, the compound-assignment forms, and `to_integer<IntType>`. The shift and `to_integer` templates take part in overload resolution only for integral `IntType` (`[support.types.byteops]`, `[cstddef.syn]`). It supports bitwise manipulation of raw storage without arithmetic or implicit integer conversion. See [[cpp17-declarations]] for enum rules.

## Integer types (`[cstdint]`)

`<cstdint>` provides everything in C `<stdint.h>`: the fixed-width, least-width, fast-width, `intptr_t`/`uintptr_t` and `intmax_t` types plus limit and constant-macro families (`[cstdint.syn]/2`).

## Start and termination (`[support.start.term]`)

| Function | Behavior | Destructors? |
|---|---|---|
| `_Exit(status)`, `abort()` | C semantics; terminate immediately; both are signal-safe | none run (not automatic, thread or static; `atexit` functions not called) |
| `exit(status)` | destroy current-thread thread-storage objects, then static objects and call `atexit` functions in the order given by `[basic.start.term]`; then flush/close C streams and remove `tmpfile` files; return `status` to the host | automatic objects are **not** destroyed; if a registered function exits with an uncaught exception, `std::terminate()` |
| `quick_exit(status)` | call `at_quick_exit` handlers (reverse registration order, except that a handler registered during the process runs after the earlier-registered handlers already called), then `_Exit(status)`; an escaping exception calls `std::terminate()` | no object destruction; signal-safe if the registered functions are |
| `atexit(f)`, `at_quick_exit(f)` | register `f`; return 0 on success; at least 32 registrations must be supported | — |

`EXIT_SUCCESS`/zero return an implementation-defined success status; `EXIT_FAILURE` an unsuccessful one (`[support.start.term]/9`). Whether `atexit` calls made after `exit` has begun succeed is unspecified. See [[program-startup-and-termination]].

## Initializer lists (`[support.initlist]`)

`initializer_list<E>` gives access to a (conceptually) array of `const E`; `begin()`, `end()`, `size()` are constant-time, and all of its functions are signal-safe. The default constructor makes an empty list (`begin()` and `end()` unspecified but equal). **Declaring an explicit or partial specialization is ill-formed.** `begin(il)`/`end(il)` free functions exist (`[support.initlist]`, `[initializer_list.syn]/2`). The language side (when braces create one) is in [[initialization]]; constructors taking it are in [[cpp17-special-member-functions]].

## Other runtime support (`[support.runtime]`)

- `getenv` does not race with other calls as long as nothing modifies the environment; `setlocale` may race with other `setlocale` calls or locale-dependent C functions, and the library behaves as if only `locale::global` calls it (`/2-3`).
- `<cstdarg>`: `va_start`'s second argument is the rightmost named parameter before `...`; if that is a pack expansion or a lambda capture the program is ill-formed (no diagnostic required); a reference type or a type incompatible with default-promoted arguments is undefined behavior (`[cstdarg.syn]`).
- `<csetjmp>`: `setjmp`/`longjmp` pairs are **undefined** if a corresponding `throw`/`catch` pair would have run any non-trivial automatic destructor (`[csetjmp.syn]/2`).
- **Signals** (`[support.signal]`): `signal` synchronizes with the resulting handler invocation. A handler's evaluation must be *signal-safe* or the behavior is undefined. An evaluation is **not** signal-safe if it contains: a library call other than plain lock-free atomic operations or functions explicitly marked signal-safe; access to thread-storage-duration objects; `dynamic_cast`; a throw; entering a try-block; dynamic initialization of a static-duration variable; or waiting for such an initialization. See [[atomics-and-memory-order]] for "plain lock-free atomic operation".

## Related

[[dynamic-memory-support]] · [[exception-support]] · [[type-identification-rtti]] · [[numeric-limits]] · [[cpp17-exception-handling]] · [[new-and-delete-expressions]] · [[cpp17-basic-concepts]]
