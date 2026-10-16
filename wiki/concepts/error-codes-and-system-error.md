---
type: concept
title: "error_code, error_condition, error_category and system_error"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# System error support (`<system_error>`, `[syserr]`)

A portable vocabulary for errors that come from the OS or other low-level APIs, without exceptions. Parent: [[cpp17-lib-diagnostics]]. Library functions that report through `error_code` out-parameters (filesystem, some stream operations) are in [[filesystem]]; the throwing counterpart is `system_error`.

## The three pieces

| Type | Role |
|---|---|
| `error_category` | Abstract base identifying the *source and encoding* of an error value. Non-copyable singletons are compared by **address**: `==` is `this == &rhs`, ordering uses `less<const error_category*>` |
| `error_code` | A pair (`value()`, `category()`): a **platform-specific** code as reported by the source. Default-constructed: value 0 in `system_category()` |
| `error_condition` | A pair (`value()`, `category()`): a **portable** condition to test against. Default-constructed: value 0 in `generic_category()` |

`explicit operator bool()` on both is `value() != 0`. `message()` is `category().message(value())`. `error_code::default_error_condition()` is `category().default_error_condition(value())` (`[syserr.errcode.observers]`, `[syserr.errcondition.observers]`).

## `error_category` virtuals (`[syserr.errcat.virtuals]`)

`name()` names the category; `default_error_condition(ev)` (default: `error_condition(ev, *this)`) maps a code value to the portable condition; `equivalent(code, condition)` and `equivalent(ev, condition)` decide cross-category equality (defaults compare via `default_error_condition` or same category and value); `message(ev)` describes the condition. A **program-defined category** derives from `error_category` and overrides these (`[syserr.errcat.derived]`).

Two predefined singletons (every call returns a reference to the same object):

- `generic_category()` — name `"generic"`; value space is the POSIX `errno` values (the `errc` enum).
- `system_category()` — name `"system"`; for OS errors. Its `default_error_condition(ev)` returns `error_condition(posv, generic_category())` when `ev` corresponds to a POSIX value `posv`, else `error_condition(ev, system_category())` — what "corresponds" means is unspecified (`[syserr.errcat.objects]/4`).

Library errors from the OS use `system_category()`; those from elsewhere use an implementation-defined category ([[library-requirements-and-conformance]], `[value.error.codes]`).

## `errc` and enum integration (`[system_error.syn]`)

- `enum class errc` has one enumerator per POSIX error (`no_such_file_or_directory` = `ENOENT`, `permission_denied` = `EACCES`, `timed_out` = `ETIMEDOUT`, `invalid_argument` = `EINVAL`, `not_enough_memory` = `ENOMEM`, `operation_would_block` = `EWOULDBLOCK`, `resource_unavailable_try_again` = `EAGAIN`, 78 in all), each with the numeric value of the matching `<cerrno>` macro (`/1`).
- `make_error_code(errc)` builds an `error_code(static_cast<int>(e), generic_category())`; `make_error_condition(errc)` builds an `error_condition` in the generic category.
- `is_error_code_enum<T>` / `is_error_condition_enum<T>` are `false_type` by default and **may be specialized for user enums** (`/2`); the `errc` condition-enum specialization is true. When true, `error_code`/`error_condition` get implicit converting constructors and assignment from `T` (via `make_error_code`/`make_error_condition`, found by ADL), which take part in overload resolution only for such enums.

## Comparison (`[syserr.compare]`)

- `error_code == error_code` and `error_condition == error_condition`: same category **and** same value.
- `error_code == error_condition` (either order): true if the code's category deems it `equivalent` to the condition, or vice versa. This is how `ec == std::errc::no_such_file_or_directory` works across platforms.
- Ordering (`<`): category first, then value. `operator<<` prints `category-name:value`. `hash` specializations exist for `error_code` and `error_condition`.

## `system_error` (`[syserr.syserr]`)

An exception (derived from `runtime_error`) carrying an `error_code`. Constructors take an `error_code` or a `(int ev, const error_category&)` pair, each optionally with a `what_arg` string (or `const char*`); postconditions: `code()` equals the supplied code, and when `what_arg` is given, `what()` contains it as a substring. `code()` returns the stored code; `what()` returns an ntbs incorporating the constructor arguments.

## Related

[[cpp17-lib-diagnostics]] · [[standard-exception-classes]] · [[exception-support]] · [[filesystem]] · [[stream-base-classes]]
