---
type: concept
title: "C++17 Annex D: compatibility features (deprecated) - overview"
tags: [cpp17, language-core, library, deprecated, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Annex D: compatibility features (`[depr]`)

About 7,100 words, 16 subsections. Annex D is **normative**: everything in it is part of the standard for this edition, but each feature is *deprecated*, meaning identified as a candidate for removal from future revisions. An implementation may mark library names and entities from this annex with the `deprecated` attribute (`[depr]/1-2`; attribute rules on [[attributes]]). The annex mixes three kinds of content: language features (D.1-D.3), headers (D.4-D.5) and library components (D.6-D.16). This page covers the small items in full and maps the big ones to [[deprecated-library-facilities]].

What is *not* in this annex any more matters as much as what is. Annex C.4.12 (`[diff.cpp14.depr]`, [[cpp17-compatibility-differences]]) records that this edition does not define `auto_ptr`, `unary_function`, `binary_function`, `random_shuffle`, `ptr_fun`, `mem_fun`, `mem_fun_ref`, `bind1st` and `bind2nd`, and removed the "old iostreams members" (`[depr.ios.members]`) that the previous edition kept here. Outside Annex C, a text search of the draft finds `unary_function` only in the list of reserved "zombie" names (`[zombie.names]`, see [[library-requirements-and-conformance]]). Other deprecations are expressed outside Annex D (for example the `deprecated` attribute itself, [[attributes]]).

## Section map

| Subsection | Label | Content | Treated on |
|---|---|---|---|
| D.1 | `[depr.static_constexpr]` | redundant out-of-class redeclaration of a `static constexpr` data member | below |
| D.2 | `[depr.impldec]` | implicit copy constructor / copy assignment defaulting when other special members are user-declared | below |
| D.3 | `[depr.except.spec]` | the exception specification `throw()` | below |
| D.4 | `[depr.cpp.headers]` | `<ccomplex>`, `<cstdalign>`, `<cstdbool>`, `<ctgmath>` | below |
| D.5 | `[depr.c.headers]` | the C headers `name.h` (Table 141) | below |
| D.6 | `[depr.str.strstreams]` | `<strstream>`: `strstreambuf`, `istrstream`, `ostrstream`, `strstream` | [[deprecated-library-facilities]] |
| D.7 | `[depr.uncaught]` | `uncaught_exception()` | below |
| D.8 | `[depr.func.adaptor.binding]` | old adaptable-binder typedefs, weak result types, `not1`/`not2` negators | [[deprecated-library-facilities]] |
| D.9 | `[depr.default.allocator]` | `allocator<void>` and the pre-`allocator_traits` members of `std::allocator` | [[deprecated-library-facilities]] |
| D.10 | `[depr.storage.iterator]` | `raw_storage_iterator` | [[deprecated-library-facilities]] |
| D.11 | `[depr.temporary.buffer]` | `get_temporary_buffer`, `return_temporary_buffer` | [[deprecated-library-facilities]] |
| D.12 | `[depr.meta.types]` | `is_literal_type`, `result_of` | below |
| D.13 | `[depr.iterator.primitives]` | `std::iterator` base class template | below |
| D.14 | `[depr.util.smartptr.shared.obs]` | `shared_ptr::unique()` | below |
| D.15 | `[depr.locale.stdcvt]` | `<codecvt>` facets `codecvt_utf8`, `codecvt_utf16`, `codecvt_utf8_utf16` | [[deprecated-library-facilities]] |
| D.16 | `[depr.conversions]` | `wstring_convert`, `wbuffer_convert` | [[deprecated-library-facilities]] |

## Language features

### D.1 Redeclaration of static constexpr data members (`[depr.static_constexpr]/1`)

For compatibility with earlier standards, a `static constexpr` data member that is defined in its class (with an initializer) may be redeclared at namespace scope **without an initializer**; that usage is deprecated. In this edition a `constexpr` static data member is implicitly `inline` (`[dcl.constexpr]/1`), so its in-class declaration can be the definition; `[class.static.data]/3` itself mentions the out-of-class redeclaration without initializer and points at this section. The out-of-class line is therefore redundant; the annex's example comments contrast this with the previous edition, where the in-class declaration was only a declaration and the out-of-class line was the definition (comments in the example, i.e. informative). Related: [[cpp17-classes]] (static members), [[one-definition-rule]], [[cpp17-declarations]] (inline variables).

### D.2 Implicit declaration of copy functions (`[depr.impldec]/1`)

The implicit definition of the **copy constructor** as defaulted is deprecated when the class has a user-declared copy assignment operator or a user-declared destructor; the implicit definition of the **copy assignment operator** as defaulted is deprecated when the class has a user-declared copy constructor or a user-declared destructor (cross-references to `[class.dtor]` and `[class.copy]`). The annex says that in a future revision these implicit definitions could become *deleted* (`[dcl.fct.def]`). Details of the implicit special members: [[cpp17-special-member-functions]]. This is the "rule of three/five" deprecation: the implicit functions still exist and still work in C++17.

### D.3 Deprecated exception specifications (`[depr.except.spec]/1`)

The noexcept-specifier `throw()` is deprecated (use `noexcept`). It is the only dynamic exception specification that survives in this edition; dynamic exception specifications were removed (`[diff.cpp14.except]` in [[cpp17-compatibility-differences]]). Exception-specification rules: [[cpp17-exception-handling]]; the grammar shape (`throw ( )` is the third noexcept-specifier alternative): [[grammar-expressions-and-statements]].

## Headers

### D.4 C++ standard library headers (`[depr.cpp.headers]`)

For compatibility with earlier editions the library provides four deprecated headers:

| Header | Behavior |
|---|---|
| `<ccomplex>` | behaves as if it simply includes `<complex>` (`[depr.ccomplex.syn]/1`) |
| `<cstdalign>` | same contents as C `<stdalign.h>`, except that neither header defines a macro named `alignas`; it defines `__alignas_is_defined` as 1 (`[depr.cstdalign.syn]`) |
| `<cstdbool>` | same contents as C `<stdbool.h>`, except that neither header defines macros named `bool`, `true` or `false`; it defines `__bool_true_false_are_defined` as 1 (`[depr.cstdbool.syn]`) |
| `<ctgmath>` | simply includes `<complex>` and `<cmath>` (`[depr.ctgmath.syn]/1`); a note says the overloads C gets through type-generic macros are already supplied there by "sufficient" extra overloads (`/2`, informative) |

These four are among the 26 `<cname>` wrappers counted on [[library-requirements-and-conformance]].

### D.5 C standard library headers (`[depr.c.headers]`)

The library provides the 26 C headers of Table 141: `assert.h`, `inttypes.h`, `signal.h`, `stdio.h`, `wchar.h`, `complex.h`, `iso646.h`, `stdalign.h`, `stdlib.h`, `wctype.h`, `ctype.h`, `limits.h`, `stdarg.h`, `string.h`, `errno.h`, `locale.h`, `stdbool.h`, `tgmath.h`, `fenv.h`, `math.h`, `stddef.h`, `time.h`, `float.h`, `setjmp.h`, `stdint.h`, `uchar.h`.

- `<complex.h>` behaves as if it includes `<ccomplex>`; `<tgmath.h>` as if it includes `<ctgmath>` (`/2`).
- Every other `name.h` behaves as if the names that the corresponding `<cname>` header puts into `std` were also placed in the **global namespace**, except the special mathematical functions of `[sf.cmath]`, the declaration of `std::byte` (`[cstddef.syn]`) and the functions and templates of `[support.types.byteops]`. It is unspecified whether the names are first declared or defined in `std` and then injected into the global namespace by using-declarations (`/3`).
- Example in the text (informative): `<cstdlib>` assuredly provides its names in `std` and may also provide them globally; `<stdlib.h>` assuredly provides them globally and may also provide them in `std` (`/4`).

Reading of `/3-4` (an inference, not a quoted rule): code that wants a guaranteed spelling should use `<cname>` for names in `std` and `name.h` for global names, since each header only *assuredly* provides one placement. How the `<cname>` side behaves is on [[library-requirements-and-conformance]] and the per-clause pages such as [[cpp17-lib-language-support]].

## Small library items

### D.7 `uncaught_exception` (`[depr.uncaught]`)

The header `<exception>` has the extra declaration `bool uncaught_exception() noexcept;`, which returns `uncaught_exceptions() > 0` (`/2`). The replacement `uncaught_exceptions()` returns a count and is the basis of scope-guard idioms: [[exception-support]].

### D.12 Deprecated type traits (`[depr.meta.types]`)

`<type_traits>` additionally has `is_literal_type` (with variable template `is_literal_type_v`) and `result_of` (with alias `result_of_t`).

- `is_literal_type<T>` is a `UnaryTypeTrait` whose base characteristic is `true_type` when `T` is a literal type and `false_type` otherwise. Precondition: `remove_all_extents_t<T>` is a complete type or cv void (`/2-3`).
- `result_of<Fn(ArgTypes...)>` is a `TransformationTrait` whose member `type` exists exactly when `invoke_result<Fn, ArgTypes...>::type` exists, and then names the same type as `invoke_result_t<Fn, ArgTypes...>`. Precondition: `Fn` and all `ArgTypes` are complete types, cv void, or arrays of unknown bound. The primary template is declared but not defined.
- A program that adds specializations of `is_literal_type` or `is_literal_type_v` has undefined behavior (`/4`).

Where `invoke_result` and `INVOKE` live: [[function-objects-and-invoke]], [[type-traits]].

### D.13 `std::iterator` (`[depr.iterator.basic]`)

`<iterator>` additionally has the class template `iterator<Category, T, Distance = ptrdiff_t, Pointer = T*, Reference = T&>`, which only defines the five member typedefs `iterator_category`, `value_type`, `difference_type`, `pointer` and `reference`. It may be used as a base class to ease defining those types for a new iterator (`/2`). Informative note: if the new iterator is a class template, the base's aliases are not visible unqualified inside the class template definition (only to callers). The example in the text derives a bidirectional iterator over `double` from it. Iterator requirements and `iterator_traits`: [[iterator-categories-and-requirements]], [[iterator-adaptors]].

### D.14 Deprecated `shared_ptr` observers (`[depr.util.smartptr.shared.obs]`)

`shared_ptr` additionally has `bool unique() const noexcept`, which returns `use_count() == 1`. The rest of the class: [[shared-ptr-and-weak-ptr]].

## Related

[[deprecated-library-facilities]] · [[cpp17-compatibility-differences]] (what was removed; Annex C map) · [[library-requirements-and-conformance]] (C library differences, Annex C.5) · [[cpp17-lib-introduction]] · [[cpp17-general-principles]] · [[cpp17-glossary]] · [[n4659-cpp17-draft-standard]]
