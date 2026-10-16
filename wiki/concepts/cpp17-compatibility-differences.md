---
type: concept
title: "Annex C map and the C++11 and C++14 incompatibilities (C.3-C.4)"
tags: [cpp17, language-core, standard-clause, open-question]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-16
---

# Annex C: map, and the incompatibilities with C++11 and C++14 (C.3-C.4, `[diff.cpp11]`, `[diff.cpp14]`)

Annex C (informative, `[diff]`) lists only changes that can **break previously valid code**; it is not a complete "what's new in C++17" list. For example, sections C.3-C.4 say nothing about the prvalue result-object model in `[basic.lval]`/`[dcl.init]` ([[copy-elision-and-temporary-materialization]]), `if constexpr`, structured bindings or fold expressions, presumably because those do not invalidate older code. This page holds the C.3 and C.4 entries (core-language tables first, library entries at the end); the other subclauses have their own pages.

## Annex C map

| Subclause | Label | Compares this draft with | Where summarized |
|---|---|---|---|
| C.1 | `[diff.iso]` | ISO C (33 entries, clauses `[lex]` to `[cpp]`) | [[cpp-vs-c-differences]] |
| C.2 | `[diff.cpp03]` | ISO C++ 2003 (language and library, 37 entries) | [[cpp03-differences]] |
| C.3 | `[diff.cpp11]` | ISO C++ 2011 | this page |
| C.4 | `[diff.cpp14]` | ISO C++ 2014 | this page |
| C.5 | `[diff.library]` | the C standard library (headers, definitions, declarations, behavior) | section "Differences from the C standard library" on [[library-requirements-and-conformance]] |

## Changes from ISO C++ 2014 (`[diff.cpp14]`, C.4)

| Area | Change | Effect | Wiki page |
|---|---|---|---|
| `[lex.phases]` | Trigraph support removed as a **required** feature | Code using trigraphs may be invalid or change meaning; implementations may still translate them (outside raw strings) as part of the implementation-defined mapping of physical source characters | [[translation-phases]] |
| `[lex.ppnumber]` | pp-number may contain `p` sign / `P` sign (for hexadecimal floating literals) | `0p+0` and `0e1_p+0` become one token instead of three | [[literals]] |
| `[expr.post.incr]`, `[expr.pre.incr]` | `++` on a `bool` operand removed | an increment of a `bool` lvalue (possibly via a template parameter) is ill-formed | [[cpp17-expressions]] |
| `[expr.new]`, `[expr.delete]` | New dynamic allocation mechanism for over-aligned types | `new` of an over-aligned class type with no class allocation functions now calls `::operator new(std::size_t, std::align_val_t)` instead of `::operator new(std::size_t)` | [[new-and-delete-expressions]] |
| `[dcl.stc]` | `register` storage-class-specifier removed (keyword stays reserved) | declarations using it are ill-formed; just delete the specifier | [[cpp17-declarations]] |
| `[dcl.spec.auto]` | `auto` deduction from a braced-init-list changed | `auto x1{1};` was `std::initializer_list<int>`, now `int`; `auto x2{1, 2};` was `initializer_list<int>`, now ill-formed | [[cpp17-declarations]] |
| `[dcl.fct]` | Exception specifications are part of the **type system** | e.g. `f(g1, g2)` with `g1` `noexcept` and `g2` not, for `template<class T> int f(T*, T*)`, is now ill-formed | [[cpp17-declarators]] |
| `[dcl.init.aggr]` | Aggregates may have **base classes** | `derived d1{};` with a private base constructor was a default-constructor call, now aggregate initialization (ill-formed there) | [[initialization]] |
| `[class.inhctor.init]` | Inheriting a constructor no longer injects constructors into the derived class | a constructor using-declaration makes base constructors visible to initialization of the derived class; overload outcomes can change | [[cpp17-special-member-functions]] |
| `[temp.deduct.type]` | Deduction allowed from the type of a non-type template argument | combined with placeholder-typed non-type parameters; some overload outcomes change | [[template-argument-deduction]] |
| `[except.spec]` | **Dynamic exception specifications removed** (only `throw()` remains, deprecated) | declarations with a potentially-throwing dynamic specification are ill-formed; violating a non-throwing one calls `terminate`, not `unexpected`, and may skip unwinding | [[cpp17-exception-handling]] |

## Changes from ISO C++ 2011 (`[diff.cpp11]`, C.3)

| Area | Change | Wiki page |
|---|---|---|
| `[lex.ppnumber]` | pp-number may contain single quotes (digit separators): `M(1'2,3'4, 5)` now yields `3'4, 5` instead of `5` | [[literals]] |
| `[basic.stc.dynamic.deallocation]` | New usual (non-placement) sized deallocator `operator delete(void*, std::size_t)`: a user declaration of that form may now clash with the predefined one | [[storage-duration-and-object-lifetime]] |
| `[expr.cond]` | A conditional with a `throw` operand keeps the other operand's type and value category (`(cond ? s : throw 0).mf()` now mutates `s`; `sizeof(true ? "" : throw 0)` is the array size) | [[cpp17-expressions]] |
| `[dcl.constexpr]` | `constexpr` non-static member functions are no longer implicitly `const` | [[cpp17-declarations]] |
| `[dcl.init.aggr]` | Classes with default member initializers can be aggregates | [[initialization]] |

## Library entries

Library items from C.3-C.4, each pointing at the library page that now covers the facility:

| Source | Change | Wiki page |
|---|---|---|
| C.3.6 `[diff.cpp11.library]` | `<shared_mutex>` is a new header; C++11 code that includes a header of that name may break | [[mutexes-and-locks]], [[library-requirements-and-conformance]] |
| C.3.7 `[diff.cpp11.input.output]` | `gets` is no longer defined (considered dangerous) | [[string-and-file-streams]] (`<cstdio>`) |
| C.4.8 `[diff.cpp14.library]` | top-level namespaces `std` followed by digits are reserved (e.g. `std2`) | [[library-requirements-and-conformance]] |
| C.4.9 `[diff.cpp14.utilities]` | `std::function` allocator constructors removed (no implementation consensus); `shared_ptr` conversion constraint from `unique_ptr` changed to add array support (`shared_ptr<T[]>`, `shared_ptr<T[N]>`) | [[std-function]], [[shared-ptr-and-weak-ptr]] |
| C.4.10 `[diff.cpp14.string]` | non-const `basic_string::data()` added: overloads that distinguish `char*` from `const char*` may now pick differently | [[basic-string]] |
| C.4.11 `[diff.cpp14.containers]` | associative container requirements changed: comparison objects with a non-const `operator()` may fail to compile | [[associative-container-requirements]] |
| C.4.12 `[diff.cpp14.depr]` | `auto_ptr`, `unary_function`, `binary_function`, `random_shuffle`, `ptr_fun`, `mem_fun`, `mem_fun_ref`, `bind1st`, `bind2nd` not defined; old iostreams members removed | [[library-requirements-and-conformance]] (zombie names), [[mutating-sequence-algorithms]]; what Annex D still holds: [[cpp17-annex-d-compatibility-features]], [[deprecated-library-facilities]] |

The library clauses themselves are summarized from [[cpp17-lib-introduction]] on; none of those pages labels a facility "new in C++17".

## Open question

Which of the above are *the* headline C++17 language changes cannot be answered from this source alone: Annex C is incompatibility-focused. A complete feature list would need another source (such as a proposal-level changelog). Annex C is also not an inventory of new library headers: `<optional>`, `<variant>`, `<any>`, `<string_view>`, `<filesystem>`, `<memory_resource>` and `<execution>` are mentioned nowhere in it (see the open points on [[cpp03-differences]]).

## Related

[[n4659-cpp17-draft-standard]] · [[cpp17-general-principles]] · [[translation-phases]] · [[cpp-vs-c-differences]] (C.1) · [[cpp03-differences]] (C.2) · [[cpp17-annex-d-compatibility-features]] (what Annex D still contains) · [[deprecated-library-facilities]]
