---
type: concept
title: "C++17 clause 18: exception handling"
tags: [cpp17, language-core, standard-clause, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 18: Exception handling (`[except]`)

About 2,600 words; 7 labelled sections. In this section "before"/"after" refer to the *sequenced before* relation ([[sequencing-and-evaluation-order]]).

## Structure (`[except]`)

`try compound-statement handler-seq`; `handler` is `catch ( exception-declaration ) compound-statement`. A **function-try-block** (`try ctor-initializer? compound-statement handler-seq`) also covers a constructor's initialization and a destructor's subobject destruction. `goto`/`switch` cannot jump into a try block or handler; `goto`, `break`, `return`, `continue` can leave one (destroying the block's variables). A try-block is a statement.

## Throwing (`[except.throw]`)

- Control transfers to the **nearest** matching handler — the one whose try block was most recently entered and not yet exited by the thread.
- Throwing copy-initializes a temporary, the **exception object**; an incomplete type (or pointer to incomplete other than `cv void`) is ill-formed. For a class type, the copy/move constructor selected (and the one that would be selected treating the thrown object as an lvalue) must be non-deleted and accessible **even if elided**; the destructor is potentially invoked.
- Storage is allocated in an unspecified way. Rethrowing passes control to another handler for the *same* exception object. The object is destroyed at the last of its points of potential destruction: when an active handler exits other than by rethrow (after destroying the handler's variable), and when an `std::exception_ptr` referring to it is destroyed.
- An exception is **caught** once a handler becomes active. If handling mechanism directly invokes a function that exits via exception, `std::terminate` is called.

## Constructors and destructors (`[except.ctor]`)

**Stack unwinding** destroys automatic class objects constructed since the try block was entered, in reverse order of construction completion (including the returned object if destroying a `return`'s temporaries/locals throws). If initialization or destruction of an object (other than via delegating constructor) is terminated by an exception, the destructors of its already-initialized direct subobjects (and, for a complete object, virtual bases) run in reverse order, before entering a function-try-block handler; variant members of a union-like class are not destroyed on the destruction path. If a delegating constructor's body exits by exception, the object's destructor runs.

## Handling (`[except.handle]`)

- The exception-declaration cannot name an incomplete type, abstract class, rvalue reference, or pointer/reference to incomplete type (other than `[cv] void*`). Arrays/functions adjust to pointers.
- **A handler matches an exception object of type E** if: `cv T`/`cv T&` with T the same as E (ignoring top-level cv); T is an **unambiguous public base** of E; T is a pointer/pointer-to-member type (by value or `const T&`) and E converts to it by a standard pointer conversion not involving private/protected/ambiguous bases, a function pointer conversion, or a qualification conversion; or E is `std::nullptr_t` and T a pointer/member pointer.
- Handlers are tried in order of appearance; `catch (...)` matches anything and must be last. If none match, the search continues in the dynamically enclosing try block of the same thread; if there is no handler, `std::terminate()` is called (whether the stack is unwound first is implementation-defined).
- A handler is **active** once the catch parameter is initialized, until the catch clause exits. The *currently handled exception* is the one with the most recently activated, still-active handler.
- The handler variable (`cv T` or `cv T&`) is copy-initialized from the exception object (from the base subobject when T is a base of E); a by-value variable's changes don't affect the exception object, a reference's do. Its lifetime ends when the handler exits, after the automatic objects initialized within it.
- In a **function-try-block handler** of a constructor/destructor, referring to any non-static member or base of the object is **undefined behavior**; parameters' scope and lifetime extend into handlers; `return` in a constructor's handler is ill-formed; reaching the end of such a handler **rethrows** the current exception (for other functions it is as flowing off the function). Function-try-blocks on `main` or a thread's initial function do not catch exceptions from static/thread-duration objects' constructors/destructors.

## Exception specifications (`[except.spec]`)

- A function has a **potentially-throwing** or **non-throwing** exception specification. Explicit forms: `noexcept(constant-expression)` (contextually converted constant `bool`), `noexcept` (= `noexcept(true)`), and `throw()` (deprecated, = `noexcept(true)`). The non-throwing property is part of the function type ([[cpp17-declarators]]).
- Default: potentially-throwing, except destructors, deallocation functions (non-throwing) and functions defaulted on their first declaration (computed from what they call). All overriders of a non-throwing virtual function must be non-throwing (unless deleted). A mismatch among declarations within a translation unit needs a diagnostic.
- If a thrown exception's handler search reaches the outermost block of a non-throwing function, `std::terminate()` is called.
- **Potentially-throwing expression:** a call through a type with a potentially-throwing specification; an implicitly invoked potentially-throwing function (overloaded operator, allocation function, argument constructor, destructor of a full-expression); a throw-expression; a `dynamic_cast` to reference needing a run-time check; `typeid(*p)` on a polymorphic pointer; or any immediate subexpression being potentially-throwing. The `noexcept(e)` operator ([[cpp17-expressions]]) is true unless `e` is potentially-throwing.
- Implicit/defaulted special members are potentially-throwing iff any selected constructor/destructor/assignment (or default argument/default member initializer) they invoke is. Specifications are evaluated/instantiated only when **needed** (named by overload resolution, odr-used, compared, defined, or needed by a defaulted member).

## Special functions (`[except.special]`)

- `std::terminate()` is called for problems in the exception mechanism itself. The stack is unwound before the call only where implementation-defined (no handler; a non-throwing function boundary); in all other cases it shall not be unwound. Implementations may not cut unwinding short because it will eventually end in `terminate`.
- An exception is **uncaught** from completion of exception-object initialization until a handler becomes active (including unwinding and a rethrow's span); `std::uncaught_exceptions()` returns the count in the current thread.

## Related

[[cpp17-expressions]] (`throw`) · [[cpp17-special-member-functions]] · [[copy-elision-and-temporary-materialization]] · [[program-startup-and-termination]] · [[cpp17-annex-d-compatibility-features]] (D.3: `throw()`) · [[grammar-expressions-and-statements]] (A.13)
