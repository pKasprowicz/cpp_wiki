---
type: concept
title: "Grammar lookup: lexical conventions, preprocessing, contextual names (A.1, A.2, A.14)"
tags: [cpp17, language-core, grammar]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Grammar lookup: names, lexical conventions and preprocessing (Annex A.1, A.2, A.14)

Compact restatement of the productions of `[gram.key]`, `[gram.lex]` and `[gram.cpp]` (92 productions). Read the notation legend and caveats on [[cpp17-grammar-summary]] first. Short form: nonterminals are plain words, literal tokens are in code font, `?` marks an optional element, the broken bar separates alternatives, and an italic phrase stands for prose that the standard gives instead of a production. The prose rules behind these productions are on [[cpp17-lexical-conventions]], [[literals]], [[translation-phases]] and [[cpp17-preprocessing-directives]].

## A.1 Contextual names (`[gram.key]`)

The annex opens by saying that new context-dependent keywords are introduced into a program by typedef, namespace, class, enumeration and template declarations (`[gram.key]/1`). Grammatically all six categories below are just an `identifier` (or an alias or template-id); only lookup can tell a type name from a variable name, so the parser needs the symbol table. A note adds that a typedef-name naming a class is also a class-name (`[class.name]`). All six are repeated in A.6, A.8 or A.12 (see the finder). Lookup rules: [[name-lookup]].

- **typedef-name** → identifier
- **namespace-name** → identifier ¦ namespace-alias
- **namespace-alias** → identifier
- **class-name** → identifier ¦ simple-template-id
- **enum-name** → identifier
- **template-name** → identifier

## A.2 Lexical conventions (`[gram.lex]`)

What to know before the productions:

- Two token notions coexist. **Preprocessing tokens** (the first production) are what phases 3-6 handle; **tokens** (second production) are what the parser sees after phase 7, and are built from identifiers, keywords, literals, operators and punctuators. The categories keyword, operator and punctuator have no production here; their lists are in `[lex.key]` and `[lex.operators]`. The long list of preprocessing-op-or-punc tokens includes the alternative tokens (`and`, `bitor`, `xor_eq`, ...), the digraphs and the words `new` and `delete`.
- A **pp-number** is deliberately looser than any numeric literal: it admits identifier characters, digit separators, and an exponent sign after `e`, `E`, `p` or `P`, so tokens that no literal rule accepts still survive the preprocessor.
- **Integer literals** come in four bases (binary `0b`, octal leading `0`, decimal, hexadecimal `0x`), each allowing the digit separator (a single quote) between digits, plus an optional suffix made of an unsigned suffix and a long or long long suffix in either order.
- **Floating literals** are decimal (fractional constant with optional exponent and suffix, or digit-sequence with mandatory exponent) or hexadecimal; the hexadecimal form always requires the binary exponent part with `p` or `P`. Floating suffixes: `f`, `l`, `F`, `L`.
- **Character and string literals** share one encoding-prefix list: `u8`, `u`, `U`, `L`. Escape sequences are simple (a fixed set of characters), octal (one to three digits) or hexadecimal (any number of digits). Raw strings are string literals with the prefix letter `R`, a delimiter of d-chars (no spaces, parentheses, backslash or control characters), and unrestricted content up to the matching close.
- **Other literals**: `true`/`false` and `nullptr` are the boolean and pointer literals. A **user-defined literal** is an integer, floating, string or character literal followed by a ud-suffix, which is just an identifier; in the integer and floating cases the grammar lists the literal parts again with a ud-suffix in place of the ordinary suffix.

- **hex-quad** → hexadecimal-digit hexadecimal-digit hexadecimal-digit hexadecimal-digit
- **universal-character-name** → `\u` hex-quad ¦ `\U` hex-quad hex-quad
- **preprocessing-token** → header-name ¦ identifier ¦ pp-number ¦ character-literal ¦ user-defined-character-literal ¦ string-literal ¦ user-defined-string-literal ¦ preprocessing-op-or-punc ¦ *each non-white-space character that cannot be one of the above*
- **token** → identifier ¦ keyword ¦ literal ¦ operator ¦ punctuator
- **header-name** → `<` h-char-sequence `>` ¦ `"` q-char-sequence `"`
- **h-char-sequence** → h-char ¦ h-char-sequence h-char
- **h-char** → *any member of the source character set except new-line and >*
- **q-char-sequence** → q-char ¦ q-char-sequence q-char
- **q-char** → *any member of the source character set except new-line and "*
- **pp-number** → digit ¦ `.` digit ¦ pp-number digit ¦ pp-number identifier-nondigit ¦ pp-number `'` digit ¦ pp-number `'` nondigit ¦ pp-number `e` sign ¦ pp-number `E` sign ¦ pp-number `p` sign ¦ pp-number `P` sign ¦ pp-number `.`
- **identifier** → identifier-nondigit ¦ identifier identifier-nondigit ¦ identifier digit
- **identifier-nondigit** → nondigit ¦ universal-character-name
- **nondigit**: one of `a` `b` `c` `d` `e` `f` `g` `h` `i` `j` `k` `l` `m` `n` `o` `p` `q` `r` `s` `t` `u` `v` `w` `x` `y` `z` `A` `B` `C` `D` `E` `F` `G` `H` `I` `J` `K` `L` `M` `N` `O` `P` `Q` `R` `S` `T` `U` `V` `W` `X` `Y` `Z` `_`
- **digit**: one of `0` `1` `2` `3` `4` `5` `6` `7` `8` `9`
- **preprocessing-op-or-punc**: one of `{` `}` `[` `]` `#` `##` `(` `)` `<:` `:>` `<%` `%>` `%:` `%:%:` `;` `:` `...` `new` `delete` `?` `::` `.` `.*` `+` `-` `*` `/` `%` `^` `&` `|` `~` `!` `=` `<` `>` `+=` `-=` `*=` `/=` `%=` `^=` `&=` `|=` `<<` `>>` `>>=` `<<=` `==` `!=` `<=` `>=` `&&` `||` `++` `--` `,` `->*` `->` `and` `and_eq` `bitand` `bitor` `compl` `not` `not_eq` `or` `or_eq` `xor` `xor_eq`
- **literal** → integer-literal ¦ character-literal ¦ floating-literal ¦ string-literal ¦ boolean-literal ¦ pointer-literal ¦ user-defined-literal
- **integer-literal** → binary-literal integer-suffix? ¦ octal-literal integer-suffix? ¦ decimal-literal integer-suffix? ¦ hexadecimal-literal integer-suffix?
- **binary-literal** → `0b` binary-digit ¦ `0B` binary-digit ¦ binary-literal `'`? binary-digit
- **octal-literal** → `0` ¦ octal-literal `'`? octal-digit
- **decimal-literal** → nonzero-digit ¦ decimal-literal `'`? digit
- **hexadecimal-literal** → hexadecimal-prefix hexadecimal-digit-sequence
- **binary-digit** → `0` ¦ `1`
- **octal-digit**: one of `0` `1` `2` `3` `4` `5` `6` `7`
- **nonzero-digit**: one of `1` `2` `3` `4` `5` `6` `7` `8` `9`
- **hexadecimal-prefix**: one of `0x` `0X`
- **hexadecimal-digit-sequence** → hexadecimal-digit ¦ hexadecimal-digit-sequence `'`? hexadecimal-digit
- **hexadecimal-digit**: one of `0` `1` `2` `3` `4` `5` `6` `7` `8` `9` `a` `b` `c` `d` `e` `f` `A` `B` `C` `D` `E` `F`
- **integer-suffix** → unsigned-suffix long-suffix? ¦ unsigned-suffix long-long-suffix? ¦ long-suffix unsigned-suffix? ¦ long-long-suffix unsigned-suffix?
- **unsigned-suffix**: one of `u` `U`
- **long-suffix**: one of `l` `L`
- **long-long-suffix**: one of `ll` `LL`
- **character-literal** → encoding-prefix? `'` c-char-sequence `'`
- **encoding-prefix**: one of `u8` `u` `U` `L`
- **c-char-sequence** → c-char ¦ c-char-sequence c-char
- **c-char** → *any member of the source character set except the single-quote ', backslash \, or new-line character* ¦ escape-sequence ¦ universal-character-name
- **escape-sequence** → simple-escape-sequence ¦ octal-escape-sequence ¦ hexadecimal-escape-sequence
- **simple-escape-sequence**: one of `\'` `\"` `\?` `\\` `\a` `\b` `\f` `\n` `\r` `\t` `\v`
- **octal-escape-sequence** → `\` octal-digit ¦ `\` octal-digit octal-digit ¦ `\` octal-digit octal-digit octal-digit
- **hexadecimal-escape-sequence** → `\x` hexadecimal-digit ¦ hexadecimal-escape-sequence hexadecimal-digit
- **floating-literal** → decimal-floating-literal ¦ hexadecimal-floating-literal
- **decimal-floating-literal** → fractional-constant exponent-part? floating-suffix? ¦ digit-sequence exponent-part floating-suffix?
- **hexadecimal-floating-literal** → hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part floating-suffix? ¦ hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part floating-suffix?
- **fractional-constant** → digit-sequence? `.` digit-sequence ¦ digit-sequence `.`
- **hexadecimal-fractional-constant** → hexadecimal-digit-sequence? `.` hexadecimal-digit-sequence ¦ hexadecimal-digit-sequence `.`
- **exponent-part** → `e` sign? digit-sequence ¦ `E` sign? digit-sequence
- **binary-exponent-part** → `p` sign? digit-sequence ¦ `P` sign? digit-sequence
- **sign**: one of `+` `-`
- **digit-sequence** → digit ¦ digit-sequence `'`? digit
- **floating-suffix**: one of `f` `l` `F` `L`
- **string-literal** → encoding-prefix? `"` s-char-sequence? `"` ¦ encoding-prefix? `R` raw-string
- **s-char-sequence** → s-char ¦ s-char-sequence s-char
- **s-char** → *any member of the source character set except the double-quote ", backslash \, or new-line character* ¦ escape-sequence ¦ universal-character-name
- **raw-string** → `"` d-char-sequence? `(` r-char-sequence? `)` d-char-sequence? `"`
- **r-char-sequence** → r-char ¦ r-char-sequence r-char
- **r-char** → *any member of the source character set, except a right parenthesis ) followed by the initial d-char-sequence (which may be empty) followed by a double quote ".*
- **d-char-sequence** → d-char ¦ d-char-sequence d-char
- **d-char** → *any member of the basic source character set except: space, the left parenthesis (, the right parenthesis ), the backslash \, and the control characters representing horizontal tab, vertical tab, form feed, and newline.*
- **boolean-literal** → `false` ¦ `true`
- **pointer-literal** → `nullptr`
- **user-defined-literal** → user-defined-integer-literal ¦ user-defined-floating-literal ¦ user-defined-string-literal ¦ user-defined-character-literal
- **user-defined-integer-literal** → decimal-literal ud-suffix ¦ octal-literal ud-suffix ¦ hexadecimal-literal ud-suffix ¦ binary-literal ud-suffix
- **user-defined-floating-literal** → fractional-constant exponent-part? ud-suffix ¦ digit-sequence exponent-part ud-suffix ¦ hexadecimal-prefix hexadecimal-fractional-constant binary-exponent-part ud-suffix ¦ hexadecimal-prefix hexadecimal-digit-sequence binary-exponent-part ud-suffix
- **user-defined-string-literal** → string-literal ud-suffix
- **user-defined-character-literal** → character-literal ud-suffix
- **ud-suffix** → identifier

## A.14 Preprocessing directives (`[gram.cpp]`)

The start symbol is preprocessing-file: a sequence of groups; each group part is a control line, a conditional-inclusion section, a text line, or a `#` followed by a conditionally-supported directive (the slot for implementation-specific directives). Facts visible in the grammar:

- `#include`, `#line`, `#error` and `#pragma` take arbitrary pp-tokens (macro expansion happens before interpretation); the include operand is not itself shaped as a header-name here.
- `#define` has four shapes: object-like, function-like with an optional identifier-list, function-like variadic (`...` only), and function-like with identifiers then `, ...`. The lparen production says that the opening parenthesis of a function-like macro must not be preceded by white space.
- A conditional section is if-group, any number of elif groups, an optional else group, and the endif line; the `#if`-group forms are `if` (constant-expression), `ifdef` and `ifndef` (an identifier). The null directive is a lone `#`.
- Two expression forms exist for use inside `#if`/`#elif`: **defined-macro-expression** (`defined X` or `defined(X)`) and **has-include-expression** (`__has_include` with a header name in angle brackets, in quotes, as a string literal, or as h-pp-tokens), so `__has_include` is part of the grammar of this draft.

- **preprocessing-file** → group?
- **group** → group-part ¦ group group-part
- **group-part** → control-line ¦ if-section ¦ text-line ¦ `#` conditionally-supported-directive
- **control-line** → `#` `include` pp-tokens new-line ¦ `#` `define` identifier replacement-list new-line ¦ `#` `define` identifier lparen identifier-list? `)` replacement-list new-line ¦ `#` `define` identifier lparen `...` `)` replacement-list new-line ¦ `#` `define` identifier lparen identifier-list `,` `...` `)` replacement-list new-line ¦ `#` `undef` identifier new-line ¦ `#` `line` pp-tokens new-line ¦ `#` `error` pp-tokens? new-line ¦ `#` `pragma` pp-tokens? new-line ¦ `#` new-line
- **if-section** → if-group elif-groups? else-group? endif-line
- **if-group** → `#` `if` constant-expression new-line group? ¦ `#` `ifdef` identifier new-line group? ¦ `#` `ifndef` identifier new-line group?
- **elif-groups** → elif-group ¦ elif-groups elif-group
- **elif-group** → `#` `elif` constant-expression new-line group?
- **else-group** → `#` `else` new-line group?
- **endif-line** → `#` `endif` new-line
- **text-line** → pp-tokens? new-line
- **conditionally-supported-directive** → pp-tokens new-line
- **lparen** → *a ( character not immediately preceded by white-space*
- **identifier-list** → identifier ¦ identifier-list `,` identifier
- **replacement-list** → pp-tokens?
- **pp-tokens** → preprocessing-token ¦ pp-tokens preprocessing-token
- **new-line** → *the new-line character*
- **defined-macro-expression** → `defined` identifier ¦ `defined` `(` identifier `)`
- **h-preprocessing-token** → *any preprocessing-token other than >*
- **h-pp-tokens** → h-preprocessing-token ¦ h-pp-tokens h-preprocessing-token
- **has-include-expression** → `__has_include` `(` `<` h-char-sequence `>` `)` ¦ `__has_include` `(` `"` q-char-sequence `"` `)` ¦ `__has_include` `(` string-literal `)` ¦ `__has_include` `(` `<` h-pp-tokens `>` `)`

## Related

[[cpp17-grammar-summary]] · [[grammar-expressions-and-statements]] · [[grammar-declarations-and-classes]] · [[cpp17-lexical-conventions]] · [[literals]] · [[translation-phases]] · [[cpp17-preprocessing-directives]]
