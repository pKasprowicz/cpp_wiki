---
type: concept
title: "Standard exception class hierarchy (stdexcept and friends)"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Standard exception classes

Which exception types the library throws and where they sit in the hierarchy. Parent: [[cpp17-lib-diagnostics]]. Base class and propagation machinery: [[exception-support]].

## `<stdexcept>` (`[std.exceptions]`)

```
exception                         (<exception>, [exception])
├── logic_error                   violations of preconditions/invariants, "detectable before the program runs"
│   ├── domain_error              domain errors
│   ├── invalid_argument          an invalid argument
│   ├── length_error              an object would exceed its maximum size
│   └── out_of_range              an argument outside its expected range
└── runtime_error                 errors "detectable only when the program executes"
    ├── range_error               range errors in internal computations
    ├── overflow_error            arithmetic overflow
    └── underflow_error           arithmetic underflow
```

Each of the nine classes has two constructors, from `const string&` and from `const char*`, with the postcondition that `what()` compares equal (via `strcmp`) to the argument text (`[logic.error]/2-5` and siblings). They hold no further state.

## Other standard exception types by clause

| Type | Derives from | Thrown for | Page |
|---|---|---|---|
| `bad_alloc` | `exception` | failed allocation | [[dynamic-memory-support]] |
| `bad_array_new_length` | `bad_alloc` | array new with a negative or too-large length | [[dynamic-memory-support]] |
| `bad_cast`, `bad_typeid` | `exception` | invalid `dynamic_cast` / null-pointer `typeid` | [[type-identification-rtti]] |
| `bad_exception` | `exception` | copy of the active exception failed | [[exception-support]] |
| `bad_optional_access` | `exception` | `optional::value()` on an empty optional | [[optional]] |
| `bad_variant_access` | `exception` | `get`/`visit` on the wrong or valueless alternative | [[variant]] |
| `bad_any_cast` | `bad_cast` | failed `any_cast` | [[any-type]] |
| `bad_weak_ptr` | `exception` | `shared_ptr` from an expired `weak_ptr` | [[shared-ptr-and-weak-ptr]] |
| `bad_function_call` | `exception` | calling an empty `std::function` | [[std-function]] |
| `system_error` | `runtime_error` | OS / low-level failures carrying an `error_code` | [[error-codes-and-system-error]] |
| `ios_base::failure` | `system_error` (possibly via a synonym) | stream errors when `exceptions()` is set | [[stream-base-classes]] |
| `filesystem_error` | `system_error` | filesystem operation failure | [[filesystem]] |
| `regex_error` | `runtime_error` | malformed regular expression | [[regex-classes-and-algorithms]] |
| `future_error` | `logic_error` | misuse of promises and futures | [[futures-and-async]] |

Library functions may throw only types named in their Throws element or classes derived from them ([[library-requirements-and-conformance]]).

## Related

[[cpp17-lib-diagnostics]] · [[exception-support]] · [[cpp17-exception-handling]]
