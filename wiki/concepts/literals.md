---
type: concept
title: "Literals"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Literals (`[lex.literal]`)

Kinds (`[lex.literal.kinds]`): integer, character, floating, string, boolean, pointer and user-defined literals. Part of [[cpp17-lexical-conventions]].

## Integer literals (`[lex.icon]`)

- Bases: binary (`0b`/`0B`), octal (leading `0`), decimal, hexadecimal. Single quotes may separate digits and are ignored for the value.
- The type is the **first** type in the table row for its base/suffix class that can represent the value. For a **decimal** literal with no suffix: `int`, `long int`, `long long int` (never unsigned). For **binary, octal and hexadecimal** with no suffix: `int`, `unsigned int`, `long int`, `unsigned long int`, `long long int`, `unsigned long long int`. Suffix `u`/`U` gives only unsigned types; `l`/`L`, `ll`/`LL` start at `long`/`long long`.
- If nothing fits but an extended integer type does, the literal may have that type. A literal no allowed type can represent makes the program ill-formed.

## Character literals (`[lex.ccon]`)

| Prefix | Kind | Type | Notes |
|---|---|---|---|
| none | ordinary | `char` | multicharacter or non-representable single c-char: conditionally-supported, type `int`, implementation-defined value |
| `u8` | UTF-8 | `char` | ill-formed if the code point does not fit one UTF-8 code unit (C0 controls and Basic Latin) |
| `u` | | `char16_t` | ill-formed if not representable in one 16-bit unit (basic multilingual plane) |
| `U` | | `char32_t` | |
| `L` | wide | `wchar_t` | multi-c-char value is implementation-defined |

Escape sequences: simple (`\n`, `\t`, `\'`, `\"`, `\?`, `\\`, ...), octal (1-3 digits), hexadecimal (`\x` with any number of digits). The single quote and backslash **must** be escaped inside a character literal. Unlisted escapes are conditionally-supported with implementation-defined semantics.

## Floating literals (`[lex.fcon]`)

Decimal or hexadecimal (`0x` mantissa with a mandatory `p`/`P` binary exponent). The type is `double` unless suffixed `f`/`F` (`float`) or `l`/`L` (`long double`). Out-of-range values are ill-formed; in-range but inexact values round to a neighboring representable value chosen in an implementation-defined manner.

## String literals (`[lex.string]`)

- Types: narrow (ordinary and `u8`) is "array of *n* `const char`"; `u"..."` is `const char16_t[n]`; `U"..."` is `const char32_t[n]`; `L"..."` is `const wchar_t[n]`. Each has static storage duration and a trailing terminator element, counted in *n*.
- **Raw strings** (`R"delim(...)delim"`): the delimiter is at most 16 characters; phase 1 and 2 transformations (universal-character-names, line splicing) are reverted inside.
- **Concatenation** (phase 6, see [[translation-phases]]): same prefix concatenates; an unprefixed literal adopts the other's prefix; UTF-8 adjacent to wide is ill-formed; other mixes are conditionally-supported.
- Whether distinct literals occupy distinct storage, and whether re-evaluating the same literal yields the same object, is **unspecified**.

## Boolean and pointer literals

`true`/`false` are prvalues of type `bool` (`[lex.bool]`). `nullptr` is a prvalue of type `std::nullptr_t` (`[lex.nullptr]`).

## User-defined literals (`[lex.ext]`)

A UDL is a call to a *literal operator*: the literal-operator-id with the ud-suffix is found by unqualified lookup and the set must not be empty (see [[name-lookup]]).

| Literal | Call form | Fallbacks |
|---|---|---|
| integer | `operator "" X(unsigned long long)` | else a raw literal operator `operator "" X("n")`, else a literal operator template `operator "" X<'c1',...>()` (raw and template not both present) |
| floating | `operator "" X(long double)` | same raw / template fallbacks |
| string | `operator "" X(str, len)` | none |
| character | `operator "" X(ch)` with the literal's own character type | none |

If a token matches both a user-defined literal and another literal kind, it is the latter. In string concatenation, all participating user-defined strings must use the same ud-suffix, which then applies to the whole result.

## Related

[[translation-phases]] · [[cpp17-lexical-conventions]] · [[value-categories]]
