---
type: concept
title: "Incompatibilities with ISO C++ 2003: Annex C.2"
tags: [cpp17, language-core, library, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-16
updated: 2026-10-16
---

# Differences from ISO C++ 2003 (Annex C.2, `[diff.cpp03]`)

Annex C.2 lists, clause by clause, how valid ISO C++ 2003 code (ISO/IEC 14882:2003) can fail to compile or behave differently under this draft. It compares against "this International Standard", i.e. N4659 as a whole: it does not say which later edition introduced each change, so this page says "since C++03" and never attributes an entry to C++11, C++14 or C++17. Each entry has a change, a rationale and an effect; the tables give the first two compactly and the effect in full. The later hops are on [[cpp17-compatibility-differences]] (C++11 to this draft: C.3; C++14 to this draft: C.4); the comparison with C is [[cpp-vs-c-differences]].

Annex C is informative and records incompatibilities only; the C.2 library entries are not an inventory of new library facilities (see "Open points" about the header list).

## Entries that change behavior without a compile error

These are the C++03 programs that keep compiling. Each is a row below; this is a quick checklist of the silent ones.

- `[lex.pptoken]` macros named like a new string-literal prefix, and macros adjacent to a user-defined-literal suffix, are no longer expanded.
- `[lex.icon]` some large integer literals change from an unsigned type to `long long`.
- `[conv.ptr]` an overload set may now pick the other function when a zero-valued non-literal used to be a null pointer constant.
- `[expr.mul]` integer division and remainder always round toward zero.
- `[class.dtor]` a destructor that throws with a non-throwing implicit specification calls `std::terminate`.
- `[temp.dep.candidate]` dependent calls may find functions with internal linkage.
- `[new.delete.single]` replacing global `operator new`/`delete` now also affects the array/other forms, and `operator new` may throw something other than `std::bad_alloc`.
- `[errno]`, `[util.dynamic.safety]`, `[string.classes]`, `[string.require]`, `[algorithms.general]`, `[ios::failure]` library behavior differences, shown below.

## C.2.1 Lexical conventions (`[diff.cpp03.lex]`) — [[cpp17-lexical-conventions]], [[literals]], [[translation-phases]]

| Entry | Change | Effect on C++03 code |
|---|---|---|
| `[lex.pptoken]` | New kinds of string literals (raw and Unicode prefixes). Why: required for new features | A macro named `R`, `u8`, `u8R`, `u`, `uR`, `U`, `UR` or `LR` is no longer expanded when it touches a string literal; it becomes part of the literal. Example in the annex: a macro `u8` defined as a string, followed by `u8"def"`, previously concatenated and now just gives `"def"` |
| `[lex.pptoken]` | User-defined string literal suffixes. Why: required for new features | `"hello"_x` used to be two preprocessing tokens, so a macro `_x` expanded; it is now one token and the macro is not expanded |
| `[lex.key]` | Ten new keywords: `alignas`, `alignof`, `char16_t`, `char32_t`, `constexpr`, `decltype`, `noexcept`, `nullptr`, `static_assert`, `thread_local`. Why: required for new features | C++03 code using them as identifiers is invalid |
| `[lex.icon]` | Type of integer literals. Why: C99 compatibility | Some literals too large for `long` may change from an unsigned type to signed `long long` |

## C.2.2 Standard conversions (`[diff.cpp03.conv]`) — [[cpp17-standard-conversions]]

| Entry | Change | Effect |
|---|---|---|
| `[conv.ptr]` | Only literals are integer null pointer constants. Why: removes surprising interactions with templates and constant expressions | Code may fail to compile or produce other results. The annex's example: inside a template, a call `f(0*N)` with overloads `f(void*)` and `f(...)` used to select the pointer version and now selects the variadic one |

## C.2.3 Expressions (`[diff.cpp03.expr]`) — [[cpp17-expressions]], [[new-and-delete-expressions]]

| Entry | Change | Effect |
|---|---|---|
| `[expr.mul]` | Rounding of integer `/` and `%` is specified. Why: portability, C99 compatibility | C++03 allowed rounding toward zero or toward negative infinity; this draft always rounds toward zero |
| `[expr.log.and]` | `&&` is valid inside a type-name (rvalue-reference declarators). Why: required for new features | Expressions such as `new int && false` or `&S::operator int && false` were valid and gave false; they are now ill-formed |

## C.2.4 Declarations (`[diff.cpp03.dcl.dcl]`) — [[cpp17-declarations]]

| Entry | Change | Effect |
|---|---|---|
| `[dcl.spec]` | `auto` is no longer a storage-class specifier. Why: new feature | The keyword now requests deduction of the variable's type from its initializer, so C++03 code using the old meaning may be invalid. Compare the C++14-to-this-draft change in `auto` deduction from braced lists: [[cpp17-compatibility-differences]] |

## C.2.5 Declarators (`[diff.cpp03.dcl.decl]`) — [[initialization]]

| Entry | Change | Effect |
|---|---|---|
| `[dcl.init.list]` | Narrowing conversions are restricted in aggregate initializers. Why: catches bugs | Valid C++03 code may not compile; the annex's example initializes an `int` array element from a `double` constant |

## C.2.6 Special member functions (`[diff.cpp03.special]`) — [[cpp17-special-member-functions]], [[cpp17-exception-handling]]

| Entry | Change | Effect |
|---|---|---|
| `[class.ctor]`, `[class.dtor]`, `[class.copy]` | An implicitly-declared special member is defined as deleted when its implicit definition would be ill-formed. Why: improves template argument deduction failure | A C++03 program that names such a function in a context that does not need its definition (for example an unevaluated operand) becomes ill-formed |
| `[class.dtor]` | A user-declared destructor has an implicit exception specification. Why: clarifies destructor requirements | A destructor that throws although its specification is non-throwing now calls `std::terminate`, without a call to `std::unexpected` |

## C.2.7 Templates (`[diff.cpp03.temp]`) — [[cpp17-templates]], [[dependent-names-and-instantiation]]

| Entry | Change | Effect |
|---|---|---|
| `[temp.param]` | `export` removed. Why: no implementation consensus | A C++03 declaration containing `export` is ill-formed |
| `[temp.arg]` | No whitespace needed between nested closing template angle brackets. Why: a persistent minor annoyance, and alias templates for non-class types would worsen it | An expression with `>` followed directly by `>` may now close two templates. The annex's example: `X< Y< 1 >> 2 > >` was valid when `>>` was a shift, and is invalid now |
| `[temp.dep.candidate]` | Dependent calls of functions with internal linkage are allowed. Why: the old rule was over-constrained and the change simplifies overload resolution | A valid C++03 program could get a different result |

## C.2.8 Library introduction (`[diff.cpp03.library]`) — [[library-requirements-and-conformance]], [[cpp17-lib-introduction]]

| Entry | Change | Effect |
|---|---|---|
| `[library]` through `[thread]` | New reserved identifiers (every name the library added). Why: required by new features | C++03 code using any of those identifiers may fail or behave differently; the annex points to the Index of Library Names for the full list |
| `[headers]` | New headers. Why: new functionality | 20 C++ headers: `<array>`, `<atomic>`, `<chrono>`, `<codecvt>`, `<condition_variable>`, `<forward_list>`, `<future>`, `<initializer_list>`, `<mutex>`, `<random>`, `<ratio>`, `<regex>`, `<scoped_allocator>`, `<system_error>`, `<thread>`, `<tuple>`, `<typeindex>`, `<type_traits>`, `<unordered_map>`, `<unordered_set>`; and 8 C wrappers: `<ccomplex>`, `<cfenv>`, `<cinttypes>`, `<cstdalign>`, `<cstdbool>`, `<cstdint>`, `<ctgmath>`, `<cuchar>`. A C++03 program including a header of any of these names may be invalid. Four of the wrappers are deprecated in Annex D ([[cpp17-annex-d-compatibility-features]]); `<codecvt>` holds the facets of [[deprecated-library-facilities]] |
| `[swappable.requirements]` | `swap` moved to a different header. Why: remove the dependency on `<algorithm>` for `swap` | Code that got `swap` through `<algorithm>` may need `<utility>` instead ([[utility-move-forward-swap]], [[library-named-requirements]]) |
| `[namespace.posix]` | The global namespace `posix` is reserved for standardization. Why: new functionality | A C++03 program with a top-level namespace `posix` may be invalid |
| `[res.on.macro.definitions]` | Attribute identifiers may not be used as macro names. Why: avoid hard-to-diagnose or non-portable constructs | C++03 code defining `override`, `final`, `carries_dependency` or `noreturn` as macros is invalid ([[attributes]]) |

## C.2.9 Language support (`[diff.cpp03.language.support]`) — [[dynamic-memory-support]], [[new-and-delete-expressions]]

| Entry | Change | Effect |
|---|---|---|
| `[new.delete.single]` (first) | Linking of the `new` and `delete` operators: the two throwing single-object signatures now form the base of the other forms. Why: replacing just those two changes the others, which is now explicit | A program that replaces global `operator new`/`delete` may behave differently. The annex's example replaces the single-object pair with `malloc`/`free`-based versions that print a message on deallocation and expects the message twice, once for `delete` and once for `delete[]` |
| `[new.delete.single]` (second) | `operator new` may throw exceptions other than `std::bad_alloc`. Why: consistent use of `noexcept` | Code assuming only `bad_alloc` can come out of the global `operator new` may behave differently |

## C.2.10 Diagnostics (`[diff.cpp03.diagnostics]`) — [[cpp17-lib-diagnostics]]

| Entry | Change | Effect |
|---|---|---|
| `[errno]` | Error numbers are thread-local. Why: support for threads | Implementation-specific C++03 code that relies on `errno` being shared across threads may change behavior |

## C.2.11 General utilities (`[diff.cpp03.utilities]`) — [[function-objects-and-invoke]], [[allocators]]

| Entry | Change | Effect |
|---|---|---|
| `[util.dynamic.safety]` | Minimal support for garbage-collected regions. Why: required by the new feature | C++03 code built without traceable-pointer support, interacting with newer code that declares regions reachable, may behave differently at run time (see the pointer-safety functions on [[allocators]] and [[storage-duration-and-object-lifetime]]) |
| `[refwrap]`, `[arithmetic.operations]`, `[comparisons]`, `[logical.operations]`, `[bitwise.operations]`, `[depr.negators]` | The standard function-object types no longer derive from `std::unary_function` or `std::binary_function`, which are no longer defined. Why: superseded by a new feature | Code that depends on those bases may not compile. The two names remain reserved ("zombie names"): [[library-requirements-and-conformance]] |

## C.2.12 Strings (`[diff.cpp03.strings]`) — [[basic-string]], [[iterator-invalidation]]

| Entry | Change | Effect |
|---|---|---|
| `[string.classes]` | The `basic_string` requirements no longer allow reference-counted strings. Why: invalidation behaves subtly differently with reference counting; this makes it uniform | C++03 code may execute differently |
| `[string.require]` | Invalidation rules for `basic_string` are loosened. Why: permits the small-string optimization | Code may execute differently; some const members such as `data` and `c_str` no longer invalidate iterators |

## C.2.13 Containers (`[diff.cpp03.containers]`) — [[container-requirements]], [[sequence-container-requirements]], [[associative-container-requirements]]

| Entry | Change | Effect |
|---|---|---|
| `[container.requirements]` (size) | `size()` is constant-time. Why: its complexity was unspecified, so implementations diverged | Some C++03-conforming containers do not meet the requirement; bringing `std::list` into line may need incompatible changes ([[deque-and-lists]]) |
| `[container.requirements]` (relaxed) | The container requirements are relaxed. Why: clarification | Portable-container code may be over-specified. Adjust: not every container has `size()` (use `empty()` instead of comparing `size()` to zero); not every container is empty after construction (`array`, see [[array-and-vector]]); not every container has constant-time `swap()` (`array`) |
| `[container.requirements]` (default constructible) | Requirement change on default-constructibility. Why: clarification | Explicitly instantiating a container with a user type lacking a default constructor may fail to compile |
| `[sequence.reqmts]`, `[associative.reqmts]` | Some signatures no longer return `void`. Why: the old signature discarded information that can be expensive to recompute | Changed: `erase(iter)` and `erase(begin, end)` for `set`, `multiset`, `map`, `multimap`; `insert(pos, num, val)` and `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`. Code relying on a `void` return (for example a pointer to one of these member functions) no longer compiles |
| `[sequence.reqmts]`, `[associative.reqmts]` | Some parameters change from `iterator` to `const_iterator`. Why: over-specification | `insert(iter, val)` for `vector`, `deque`, `list`, `set`, `multiset`, `map`, `multimap`; `insert(pos, beg, end)` for `vector`, `deque`, `list`, `forward_list`; `erase(begin, end)` for the associative containers; all forms of `list::splice` and `list::merge`. Code using them may fail to compile |
| `[sequence.reqmts]`, `[associative.reqmts]` | `resize` signatures change. Why: performance and compatibility with move semantics | For `vector`, `deque` and `list` the fill value is passed by reference rather than by value, and another overload is added; code may fail to compile |

## C.2.14 Algorithms (`[diff.cpp03.algorithms]`) — [[mutating-sequence-algorithms]]

| Entry | Change | Effect |
|---|---|---|
| `[algorithms.general]` | The state of the inputs after some algorithms differs. Why: required by a new feature | A program can observe that an object with a valid but unspecified state has a different unspecified state, for example the tail left by `std::remove` and `std::remove_if` |

## C.2.15 Numerics (`[diff.cpp03.numerics]`) — [[complex-numbers]]

| Entry | Change | Effect |
|---|---|---|
| `[complex.numbers]` | The representation of complex numbers is specified. Why: compatibility with C99 | C++03 code relying on implementation-specific knowledge of the binary representation of the required `std::complex` specializations may be incompatible |

## C.2.16 Input/output (`[diff.cpp03.input.output]`) — [[stream-base-classes]], [[formatted-and-unformatted-io]], [[standard-exception-classes]]

| Entry | Change | Effect |
|---|---|---|
| `[istream::sentry]`, `[ostream::sentry]`, `[iostate.flags]` | The boolean conversion functions are declared `explicit`. Why: clarifies intent, avoids workarounds | Code that relied on implicit conversion to `bool` fails to compile in these situations: passing the value to a `bool` parameter, comparing with `==` to `true` or `false`, returning it from a `bool` function, aggregate-initializing a `bool` member, binding it to a `const bool&` temporary |
| `[ios::failure]` | Different base class for `std::ios_base::failure`. Why: more detailed error messages | It now derives from `std::system_error` (which derives from `std::runtime_error`) rather than directly from `std::exception`; code assuming direct derivation may behave differently ([[error-codes-and-system-error]]) |
| `[ios.base]` | The flag types in `std::ios_base` are bitmask types with `constexpr static` member values. Why: required for new features | Code relying on those flag types being `std::bitset` or an integer type may not compile; the annex's example stores `ios_base::hex` in an `int` and passes it to `setf` |

## Open points

- **Stale exception specifications in an example.** The `[new.delete.single]` example uses `throw(std::bad_alloc)` and `throw()` in C++03 style. This draft's C.4 (`[diff.cpp14.except]`, see [[cpp17-compatibility-differences]]) says declarations with a potentially-throwing dynamic exception specification are ill-formed; only `throw()` survives, as a deprecated spelling ([[cpp17-exception-handling]]). The example therefore illustrates C++03 code, and its first function would not be valid unmodified in this draft. Whether the editors left it deliberately is not stated.
- **The new-headers list is not an inventory.** The C.2.8 list names 20 C++ headers and 8 C wrappers. Headers such as `<optional>`, `<variant>`, `<any>`, `<string_view>`, `<filesystem>`, `<memory_resource>` and `<execution>` are in Table 16 of this draft (`[headers]`) but are mentioned nowhere in Annex C (a text search of all of C.1-C.5 finds none of them; C.3.6 adds only `<shared_mutex>`). Treat Annex C as a list of *incompatibilities its editors recorded*, not as a changelog.
- **Label glitch.** The `[swappable.requirements]` entry prints "Effect on original feature" where the other entries print "Change".
- Several effects are phrased as "may fail to compile or produce different results" without further detail; the table repeats that vagueness rather than guessing.

## Related

[[cpp17-compatibility-differences]] · [[cpp-vs-c-differences]] · [[n4659-cpp17-draft-standard]] · [[cpp17-annex-d-compatibility-features]] · [[deprecated-library-facilities]]
