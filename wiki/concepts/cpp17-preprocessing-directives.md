---
type: concept
title: "C++17 clause 19: preprocessing directives"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 19: Preprocessing directives (`[cpp]`)

About 3,900 words; 14 labelled sections. Preprocessing is translation phase 4 ([[translation-phases]]); tokens from [[cpp17-lexical-conventions]].

## Directive syntax (`[cpp]`)

- A directive starts with a `#` token that is the first character of the file or follows white space containing a newline, and ends at the next newline — even in the middle of a function-like macro invocation. Between tokens in a directive only space and horizontal tab may appear. Tokens in a directive are not macro-expanded unless stated.
- Groups: `control-line` (`#include`, `#define`, `#undef`, `#line`, `#error`, `#pragma`, null `#`), `if-section` (`#if/#ifdef/#ifndef`, `#elif`, `#else`, `#endif`), `text-line`, and `# conditionally-supported-directive` (any other `#` line: conditionally-supported, implementation-defined). A text line may not begin with `#`. In skipped groups directive syntax is relaxed.

## Conditional inclusion (`[cpp.cond]`)

- The controlling expression is an integral constant expression, with `defined X` / `defined(X)` (1 if X is a currently defined macro) and **`__has_include`** (1 if the named header/source file can be found, searched as an `#include` would, with no further macro expansion) as unary operators. `__has_include` is treated as a defined macro by `#ifdef`/`defined` and may not appear elsewhere.
- Macros are replaced first (except operands of `defined`); producing the token `defined` through expansion, or a malformed use of it, is **undefined behavior**. Then all remaining identifiers and keywords except `true`/`false` become `0`; the expression is evaluated with at least the ranges in `[support.limits]`, treating every signed/unsigned integer type as `intmax_t`/`uintmax_t`. Character-literal values in `#if` may differ from their value elsewhere (implementation-defined).
- `#ifdef X` ≡ `#if defined X`; `#ifndef X` ≡ `#if !defined X`. Only the first group with a true condition is processed.

## Source file inclusion (`[cpp.include]`)

`#include <h-char-sequence>` searches implementation-defined places; `#include "q-char-sequence"` searches the source file in an implementation-defined manner and falls back to the `<>` form. A third form takes macro-expanded `pp-tokens` that must end up as one of the two forms (otherwise **undefined**). The implementation must map names of the form (nondigits/digits) `.` single-nondigit uniquely; nesting limit is implementation-defined.

## Macro replacement (`[cpp.replace]` and subsections)

- **Redefinition** is allowed only with an identical replacement list (and, for function-like macros, identical parameter names); otherwise ill-formed. An object-like macro needs white space between name and replacement list. `lparen` is a `(` not preceded by white space.
- Function-like invocation: argument count must equal the parameter count (with `...`: more arguments than named parameters); arguments are separated by top-level commas; newlines count as white space; directive-like sequences inside arguments are **undefined behavior**. `__VA_ARGS__` appears only in the replacement list of a variadic macro; the variable arguments (with their commas) merge into one item.
- **Argument substitution:** a parameter not adjacent to `#`/`##` is replaced by the **fully macro-expanded** argument.
- **`#` operator:** each `#` in a function-like macro's replacement list must precede a parameter; the argument's spelling becomes a character string literal (white space runs → single space, ends trimmed, `\` inserted before `"` and `\` inside string/character literals; empty → `""`); an invalid result is undefined.
- **`##` operator:** not at either end of a replacement list; the adjacent tokens are concatenated (an empty argument becomes a *placemarker*; placemarker with placemarker → placemarker; with a token → that token); an invalid token result is **undefined**; order of `#`/`##` evaluation is unspecified.
- **Rescanning:** after substitution and `#`/`##`, placemarkers are removed and the result is rescanned together with the rest of the file; a macro name encountered during its own replacement (including nested replacements) is **not replaced again** and stays unreplaceable. The result is not treated as a directive, but `_Pragma` operators in it are executed.
- **Scope:** a macro lasts until `#undef` (ignored if undefined) or the end of the translation unit; macros have no meaning after phase 4.

## Other directives

- `#line digit-sequence ["file"]` sets the presumed line number (and file name); zero or more than 2147483647 is **undefined**; a macro-expanded form must reduce to one of the two forms (else undefined).
- `#error pp-tokens`: produces a diagnostic and renders the program ill-formed.
- `#pragma pp-tokens`: implementation-defined; may even make the program non-conforming; **unrecognized pragmas are ignored**. `_Pragma("...")` destringizes its literal (removes `L`, outer quotes, turns `\"` → `"` and `\\` → `\`), tokenizes it and executes it as a pragma directive (`[cpp.pragma.op]`).
- Null directive `#` does nothing.

## Predefined macros (`[cpp.predefined]`)

Always defined: **`__cplusplus` = `201703L`**, `__DATE__`, `__FILE__`, `__LINE__`, `__STDC_HOSTED__` (1 hosted, 0 freestanding), `__STDCPP_DEFAULT_NEW_ALIGNMENT__` (a `std::size_t` literal: alignment guaranteed by default `operator new`), `__TIME__`. Conditionally defined: `__STDC__`, `__STDC_VERSION__` (implementation-defined), `__STDC_MB_MIGHT_NEQ_WC__` (1), `__STDC_ISO_10646__` (`yyyymmL`), `__STDCPP_STRICT_POINTER_SAFETY__` (1 iff strict pointer safety), `__STDCPP_THREADS__` (1 iff more than one thread of execution is possible). Values stay constant through the translation unit except `__FILE__`/`__LINE__`. `#define`/`#undef` of a predefined name or of `defined` is **undefined behavior**; other predefined macros start with an underscore followed by an uppercase letter or another underscore.

## Related

[[translation-phases]] · [[literals]] · [[cpp17-lexical-conventions]] · [[constant-expressions]] · [[grammar-lexical-and-preprocessing]] (Annex A.14)
