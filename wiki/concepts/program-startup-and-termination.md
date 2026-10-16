---
type: concept
title: "Program startup and termination"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Program startup and termination (`[basic.start]`)

Part of [[cpp17-basic-concepts]].

## `main` (`[basic.start.main]`)

- A program contains a global function `main`; running it starts the main thread. Whether a freestanding program must define `main` is implementation-defined.
- Required forms: `int main()` and `int main(int argc, char* argv[])`-style (second parameter pointer to pointer to char); other types are implementation-defined, but the return type is `int` and the type has C++ language linkage. `argv[argc]` is 0 and `argv[0]` names the program or is `""`.
- `main` cannot be overloaded, used in the program, deleted, `inline`, `static`, `constexpr`, or declared with a linkage-specification. A global variable named `main`, or `main` with C language linkage, is ill-formed. The linkage of `main` is implementation-defined.
- `return` in `main` leaves it (destroying automatic objects) and calls `std::exit` with the value. Falling off the end behaves like `return 0`.
- Terminating without leaving the block (e.g. calling `std::exit`) does **not** destroy automatic objects. Calling `std::exit` during destruction of an object with static or thread storage duration is undefined behavior.

## Static initialization (`[basic.start.static]`)

Variables with static duration are initialized at program initiation; thread-duration ones as a consequence of thread execution. A **constant initializer** is an initializer whose full-expression is a constant expression (constexpr constructors may be used even for non-literal class types). If constant initialization isn't performed, the variable is first **zero-initialized**. Zero- plus constant-initialization are **static initialization**; everything else is **dynamic initialization**. All static initialization strongly happens before any dynamic initialization. An implementation may perform dynamic initialization statically if it changes no other static/thread object before that object is initialized and yields the same value.

## Dynamic initialization of non-local variables (`[basic.start.dynamic]`)

| Category | Variables |
|---|---|
| unordered | implicitly or explicitly instantiated specializations (e.g. static data members of class templates) |
| partially ordered | inline variables that are not instantiated specializations |
| ordered | everything else |

Ordering (`/2`): ordered variables defined earlier in one translation unit are initialized earlier (sequenced before). Partially ordered V before W (V defined before W in every unit where W is defined): V's initialization is sequenced before W's, or strongly happens before when threads other than main exist. Otherwise, with extra threads started first, the thread that runs each initialization is unspecified (unsequenced if on the same thread); without them the initializations are indeterminately sequenced.

Whether dynamic initialization happens before the first statement of `main` or is **deferred** is implementation-defined (for non-inline variables, inline variables, and thread-duration variables separately); if deferred, it must strongly happen before the first non-initialization odr-use of any non-inline function or non-inline variable defined in the same translation unit (non-inline variables), or of that variable itself (inline variables); for thread-duration variables the initialization is sequenced before the first non-initialization odr-use by that thread. If initialization of such a variable exits by exception, `std::terminate` is called.

## Termination (`[basic.start.term]`)

- `std::exit` runs destructors of initialized static-duration objects and `std::atexit` functions; the call to `exit` is sequenced before them. Thread-duration objects of a thread are destroyed when it returns from its initial function or calls `exit`, and that completes before static-duration destruction starts.
- Destruction order is the reverse of initialization completion (for static duration: where one's completion strongly happens before the other's); statically initialized objects are destroyed as if dynamically initialized; subobject block-scope statics are destroyed after the subobjects. `atexit` registrations are interleaved with destructors by the order of initialization/registration (a later `atexit` call's function runs first).
- Exiting via an exception from a static/thread object's destruction calls `std::terminate`.
- Using a block-scope static/thread object after its destruction (re-entering its definition, or via a pointer) is undefined behavior.
- A use of a standard-library facility not permitted in signal handlers that doesn't happen before completion of static destruction and `atexit` functions is undefined.
- `std::abort()` terminates without running destructors or `atexit`/`at_quick_exit` functions.

## Related

[[storage-duration-and-object-lifetime]] · [[initialization]] · [[memory-model-and-data-races]] · [[constant-expressions]] · [[implementation-quantities]] (32 `atexit` / `at_quick_exit` functions)
