---
type: concept
title: "C++17 clause 22: diagnostics library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 22: Diagnostics library (`[diagnostics]`)

About 3,600 words; 42 labelled sections. A small clause: the standard exception classes, `assert`, `errno`, and the `error_code` machinery. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header | Content | Wiki page |
|---|---|---|---|---|
| 22.2 Exception classes | `[std.exceptions]` | `<stdexcept>` | `logic_error` and `runtime_error` hierarchies | [[standard-exception-classes]] |
| 22.3 Assertions | `[assertions]` | `<cassert>` | the `assert` macro | below |
| 22.4 Error numbers | `[errno]` | `<cerrno>` | `errno` and the E-macros | below |
| 22.5 System error support | `[syserr]` | `<system_error>` | `error_category`, `error_code`, `error_condition`, `errc`, `system_error` | [[error-codes-and-system-error]] |

## Assertions (`[assertions]`)

`<cassert>` is C's `<assert.h>` except that a macro named `static_assert` is *not* defined (`[cassert.syn]`). `assert(E)` is a **constant subexpression** (usable inside a constant expression, see [[constant-expressions]]) if `NDEBUG` is defined where `assert` was last defined, or if `E`, contextually converted to `bool`, is a constant subexpression that yields true (`[assertions.assert]`). Including `<cassert>` repeatedly re-evaluates `NDEBUG` each time ([[library-requirements-and-conformance]], `[using.headers]/2`).

## Error numbers (`[errno]`)

`<cerrno>` matches POSIX `<errno.h>`, except that `errno` must be a macro; the macro meanings come from POSIX. There is a **separate `errno` value per thread** (`[errno]/1`). Library components in `[syserr]` must not change `errno` (`[syserr]/2`).

## Error model in one paragraph

The standard splits errors into **logic errors** (flaws in the program's own logic, "in theory preventable") and **runtime errors** (events outside the program's scope, not easily predicted) (`[std.exceptions]/1-3`). Operating-system and low-level failures are carried by `error_code`; throwing forms use `system_error`. How all of these relate to library throwing rules: [[library-requirements-and-conformance]], [[exception-support]].

## Related

[[standard-exception-classes]] · [[error-codes-and-system-error]] · [[exception-support]] · [[cpp17-exception-handling]]
