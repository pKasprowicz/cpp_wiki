---
type: concept
title: "C++17 clause 5: lexical conventions"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 5: Lexical conventions (`[lex]`)

About 6,000 words of normative text; 21 labelled sections.

## Section map

| Section | Label | Where summarized |
|---|---|---|
| 5.1 Separate translation | `[lex.separate]` | [[translation-phases]] |
| 5.2 Phases of translation | `[lex.phases]` | [[translation-phases]] |
| 5.3 Character sets | `[lex.charset]` | below |
| 5.4 Preprocessing tokens | `[lex.pptoken]` | below |
| 5.5 Alternative tokens | `[lex.digraph]` | below |
| 5.6-5.8 Tokens, comments, header names | `[lex.token]`, `[lex.comment]`, `[lex.header]` | below |
| 5.9 Preprocessing numbers | `[lex.ppnumber]` | below |
| 5.10 Identifiers | `[lex.name]` | below |
| 5.11 Keywords | `[lex.key]` | below |
| 5.12 Operators and punctuators | `[lex.operators]` | below |
| 5.13 Literals | `[lex.literal]` (8 subsections) | [[literals]] |

## Character sets (`[lex.charset]`)

The basic source character set has 96 characters (space, horizontal tab, vertical tab, form feed, new-line, and 91 graphic characters). A universal-character-name (`\uNNNN` or `\UNNNNNNNN`) names other characters; a value in the surrogate range makes the program ill-formed, as does a universal-character-name outside literals that denotes a control character or a basic-set character. The basic execution character set additionally contains alert, backspace, carriage return and a null character with value 0; the digits `0-9` must have consecutive values.

## Preprocessing tokens (`[lex.pptoken]`)

Categories: header names, identifiers, preprocessing numbers, character literals (incl. user-defined), string literals (incl. user-defined), operators/punctuators, and any other single non-white-space character. An unmatched `'` or `"` falling into the last category is undefined behavior. Tokenization takes the **longest** possible token ("maximal munch"), even if that makes later analysis fail, with two special cases: a raw-string prefix such as `R"` starts a raw string, and `<::` not followed by `:` or `>` is split so `<` stands alone (so `<::` doesn't become `<:` digraph). A header-name is only formed inside `#include`.

## Alternative tokens (`[lex.digraph]`)

Digraphs `<% %> <: :> %: %:%:` and the word forms `and`, `or`, `not`, `xor`, `compl`, `bitand`, `bitor`, `and_eq`, `or_eq`, `xor_eq`, `not_eq` behave identically to their primary tokens except spelling.

## Comments (`[lex.comment]`)

`/* */` comments do not nest; `//` ends before the next new-line.

## Identifiers (`[lex.name]`)

Arbitrarily long; case-sensitive; all characters significant. Universal-character-names must fall in the allowed ranges of Table 2 and the first character must not be in the combining-character ranges of Table 3. `override` and `final` have special meaning only in context; ambiguity is resolved in favor of a regular identifier. **Reserved to the implementation** (no diagnostic required): any identifier containing a double underscore or beginning with underscore + uppercase letter (any use), and any identifier beginning with an underscore in the global namespace.

## Keywords (`[lex.key]`)

Table 5 lists the unconditional keywords (e.g. `alignas`, `constexpr`, `decltype`, `noexcept`, `nullptr`, `static_assert`, `thread_local`, plus the legacy `register` and `export`); they are keywords in phase 7 except inside an attribute-token. The alternative operator words listed under "Alternative tokens" above are also reserved (Table 6).

## Operators and punctuators (`[lex.operators]`)

A fixed list of preprocessing-op-or-punc tokens, each converted to a single token in phase 7.

## Related

[[literals]] · [[translation-phases]] · [[cpp17-preprocessing-directives]] · [[cpp17-general-principles]] · [[grammar-lexical-and-preprocessing]] (Annex A.1, A.2) · [[cpp-vs-c-differences]] (C keywords, character and string literal types) · [[cpp03-differences]] (new string-literal prefixes, user-defined literal suffixes) · [[cpp17-glossary]] (multibyte character)
