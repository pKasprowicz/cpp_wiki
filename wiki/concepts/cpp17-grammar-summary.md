---
type: concept
title: "C++17 Annex A: grammar summary (lookup guide)"
tags: [cpp17, language-core, grammar, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Annex A: grammar summary (`[gram]`)

Annex A (informative, about 2,500 words of productions) repeats the syntax that is spread through clauses 5-19 in one place, in 14 subsections. This wiki restates it in a compact one-line-per-production notation on three lookup pages (below) and uses this page as the guide: what the annex is and is not, the notation, a section map, structural facts that cut across sections, and an alphabetical finder of all 285 nonterminals.

## What the annex promises (and does not)

- It is an **aid to comprehension**, not an exact statement of the language. The grammar accepts a **superset** of valid C++: the disambiguation rules (`[stmt.ambig]` for expression versus declaration statements, `[dcl.spec]`, `[class.member.lookup]`) must be applied, and access control, ambiguity and type rules are needed to weed out constructs that parse but mean nothing (`[gram]/1`).
- Several nonterminals are therefore *context-dependent names* with the same shape (just an identifier): see A.1 on [[grammar-lexical-and-preprocessing]].
- Annex A covers the language only. The grammar of regular expressions is specified separately in clause 31 ([[cpp17-lib-regex]]); the preprocessor has its own start symbol (preprocessing-file, A.14).

## Notation on the lookup pages

The standard prints a production as a heading line and indented alternatives, with an `opt` subscript for optional parts and "one of" for token lists (syntax notation: `[syntax]`, summarized on [[cpp17-general-principles]]). The lookup pages compress each production onto one line:

- `name → alt1 ¦ alt2 ¦ ...`: the arrow starts the right-hand side and the **broken bar** separates alternatives (a plain bar would collide with the `|` token);
- plain words are nonterminals (hyphenated names, as in the standard), code-font text is a literal token (keyword, operator or punctuation), and a trailing `?` is the standard's `opt` subscript;
- `name: one of ...` lists the tokens of a set production;
- an italic phrase replaces a prose "production" such as "any member of the source character set except new-line and the quote";
- the two-bracket attribute introducer is written as two separate bracket tokens, because double square brackets are wikilink syntax in this wiki.

The compression was generated mechanically from the raw HTML of the annex and then spot-checked; it is a reformulation of the structure, not a copy of the printed layout. For the exact printed form open `https://timsong-cpp.github.io/cppwp/n4659/gram` (or the raw file).

## Section map

| Subsection | Label | Productions | Lookup page | Prose rules |
|---|---|---|---|---|
| A.1 Keywords (contextual names) | `[gram.key]` | 6 | [[grammar-lexical-and-preprocessing]] | [[name-lookup]] |
| A.2 Lexical conventions | `[gram.lex]` | 65 | [[grammar-lexical-and-preprocessing]] | [[cpp17-lexical-conventions]], [[literals]] |
| A.3 Basic concepts | `[gram.basic]` | 1 | [[grammar-declarations-and-classes]] | [[cpp17-basic-concepts]] |
| A.4 Expressions | `[gram.expr]` | 47 | [[grammar-expressions-and-statements]] | [[cpp17-expressions]], [[lambda-expressions]], [[fold-expressions]] |
| A.5 Statements | `[gram.stmt]` | 13 | [[grammar-expressions-and-statements]] | [[cpp17-statements]] |
| A.6 Declarations | `[gram.dcl]` | 60 | [[grammar-declarations-and-classes]] | [[cpp17-declarations]], [[attributes]], [[structured-bindings]] |
| A.7 Declarators | `[gram.decl]` | 30 | [[grammar-declarations-and-classes]] | [[cpp17-declarators]], [[initialization]] |
| A.8 Classes | `[gram.class]` | 13 | [[grammar-declarations-and-classes]] | [[cpp17-classes]] |
| A.9 Derived classes | `[gram.derived]` | 5 | [[grammar-declarations-and-classes]] | [[cpp17-derived-classes]] |
| A.10 Special member functions | `[gram.special]` | 7 | [[grammar-declarations-and-classes]] | [[cpp17-special-member-functions]] |
| A.11 Overloading | `[gram.over]` | 3 | [[grammar-declarations-and-classes]] | [[cpp17-overloading]] |
| A.12 Templates | `[gram.temp]` | 14 | [[grammar-declarations-and-classes]] | [[cpp17-templates]] |
| A.13 Exception handling | `[gram.except]` | 6 | [[grammar-expressions-and-statements]] | [[cpp17-exception-handling]] |
| A.14 Preprocessing directives | `[gram.cpp]` | 21 | [[grammar-lexical-and-preprocessing]] | [[cpp17-preprocessing-directives]] |

291 productions in all, 285 distinct nonterminal names. Six names are defined twice, with identical meaning: typedef-name, namespace-name, namespace-alias, class-name, enum-name and template-name (first in A.1, then in A.6, A.8 or A.12). Two nonterminals are used but have no production in the annex: `keyword` and `punctuator` (the token lists are in `[lex.key]` and `[lex.operators]`, see [[cpp17-lexical-conventions]]).

## Structural facts that cut across sections

- **Start symbols**: translation-unit (A.3, language proper: an optional sequence of declarations) and preprocessing-file (A.14, a sequence of groups). The two grammars meet at the token level: preprocessing-token (A.2) is what the preprocessor handles; token (A.2) is what the language grammar consumes ([[translation-phases]]).
- **Declaration versus expression**: a statement can be an expression-statement or a declaration-statement (A.5); the grammar alone cannot decide `T(x);`-like cases, hence the disambiguation rule cited above.
- **Where names get their shape**: nested-name-specifier and qualified-id are in A.4 but are used by declarators (A.7), class heads (A.8) and base clauses (A.9). id-expression, unqualified-id and template-id link A.4 and A.12 (operator-function-id comes from A.11, conversion-function-id from A.10).
- **Optional attributes everywhere**: attribute-specifier-seq appears in 33 productions of A.4-A.13; its own grammar is in A.6 ([[attributes]]).
- **Pack expansion `...`** shows up as an optional suffix in lists of captures, template arguments, base specifiers, mem-initializers, using-declarators, initializer-clauses and attribute lists, and as a leading element in declarator-id.
- **Statements that embed declarations**: condition, init-statement (A.5), for-range-declaration, exception-declaration (A.13); each reuses decl-specifier-seq and declarator from A.6-A.7.

## Quick routes

| Looking for the production of... | Where |
|---|---|
| lambda introducer, captures, `*this` capture | A.4 lambda-introducer, lambda-capture, simple-capture, init-capture |
| fold expressions | A.4 fold-expression, fold-operator |
| `if constexpr`, `switch`/`if` with initializer | A.5 selection-statement, init-statement |
| structured bindings | A.6 simple-declaration (third form) and A.5 for-range-declaration |
| attributes and `alignas` | A.6 attribute-specifier, attribute-list, alignment-specifier |
| user-defined literals | A.2 user-defined-literal and A.11 literal-operator-id |
| deduction guides | A.12 deduction-guide (also a declaration alternative in A.6 and a member-declaration alternative in A.8) |
| function bodies: `= default`, `= delete`, try-blocks | A.7 function-body, A.13 function-try-block |
| `noexcept` | A.4 noexcept-expression, A.13 noexcept-specifier |
| `__has_include`, `defined` in `#if` | A.14 has-include-expression, defined-macro-expression |

## Finder: every nonterminal and its subsection

Entries read `name (A.n)`; a slash means the name appears in two subsections. The detail page for each subsection is in the section map.

- **a**: abstract-declarator (A.7), abstract-pack-declarator (A.7), access-specifier (A.9), additive-expression (A.4), alias-declaration (A.6), alignment-specifier (A.6), and-expression (A.4), asm-definition (A.6), assignment-expression (A.4), assignment-operator (A.4), attribute (A.6), attribute-argument-clause (A.6), attribute-declaration (A.6), attribute-list (A.6), attribute-namespace (A.6), attribute-scoped-token (A.6), attribute-specifier (A.6), attribute-specifier-seq (A.6), attribute-token (A.6), attribute-using-prefix (A.6)
- **b**: balanced-token (A.6), balanced-token-seq (A.6), base-clause (A.9), base-specifier (A.9), base-specifier-list (A.9), binary-digit (A.2), binary-exponent-part (A.2), binary-literal (A.2), block-declaration (A.6), boolean-literal (A.2), brace-or-equal-initializer (A.7), braced-init-list (A.7)
- **c**: c-char (A.2), c-char-sequence (A.2), capture (A.4), capture-default (A.4), capture-list (A.4), cast-expression (A.4), character-literal (A.2), class-head (A.8), class-head-name (A.8), class-key (A.8), class-name (A.1/A.8), class-or-decltype (A.9), class-specifier (A.8), class-virt-specifier (A.8), compound-statement (A.5), condition (A.5), conditional-expression (A.4), conditionally-supported-directive (A.14), constant-expression (A.4), control-line (A.14), conversion-declarator (A.10), conversion-function-id (A.10), conversion-type-id (A.10), ctor-initializer (A.10), cv-qualifier (A.7), cv-qualifier-seq (A.7)
- **d**: d-char (A.2), d-char-sequence (A.2), decimal-floating-literal (A.2), decimal-literal (A.2), decl-specifier (A.6), decl-specifier-seq (A.6), declaration (A.6), declaration-seq (A.6), declaration-statement (A.5), declarator (A.7), declarator-id (A.7), decltype-specifier (A.6), deduction-guide (A.12), defined-macro-expression (A.14), defining-type-id (A.7), defining-type-specifier (A.6), defining-type-specifier-seq (A.6), delete-expression (A.4), digit (A.2), digit-sequence (A.2)
- **e**: elaborated-type-specifier (A.6), elif-group (A.14), elif-groups (A.14), else-group (A.14), empty-declaration (A.6), enclosing-namespace-specifier (A.6), encoding-prefix (A.2), endif-line (A.14), enum-base (A.6), enum-head (A.6), enum-head-name (A.6), enum-key (A.6), enum-name (A.1/A.6), enum-specifier (A.6), enumerator (A.6), enumerator-definition (A.6), enumerator-list (A.6), equality-expression (A.4), escape-sequence (A.2), exception-declaration (A.13), exclusive-or-expression (A.4), explicit-instantiation (A.12), explicit-specialization (A.12), exponent-part (A.2), expr-or-braced-init-list (A.7), expression (A.4), expression-list (A.4), expression-statement (A.5)
- **f**: floating-literal (A.2), floating-suffix (A.2), fold-expression (A.4), fold-operator (A.4), for-range-declaration (A.5), for-range-initializer (A.5), fractional-constant (A.2), function-body (A.7), function-definition (A.7), function-specifier (A.6), function-try-block (A.13)
- **g**: group (A.14), group-part (A.14)
- **h**: h-char (A.2), h-char-sequence (A.2), h-pp-tokens (A.14), h-preprocessing-token (A.14), handler (A.13), handler-seq (A.13), has-include-expression (A.14), header-name (A.2), hex-quad (A.2), hexadecimal-digit (A.2), hexadecimal-digit-sequence (A.2), hexadecimal-escape-sequence (A.2), hexadecimal-floating-literal (A.2), hexadecimal-fractional-constant (A.2), hexadecimal-literal (A.2), hexadecimal-prefix (A.2)
- **i**: id-expression (A.4), identifier (A.2), identifier-list (A.14), identifier-nondigit (A.2), if-group (A.14), if-section (A.14), inclusive-or-expression (A.4), init-capture (A.4), init-declarator (A.7), init-declarator-list (A.7), init-statement (A.5), initializer (A.7), initializer-clause (A.7), initializer-list (A.7), integer-literal (A.2), integer-suffix (A.2), iteration-statement (A.5)
- **j**: jump-statement (A.5)
- **l**: labeled-statement (A.5), lambda-capture (A.4), lambda-declarator (A.4), lambda-expression (A.4), lambda-introducer (A.4), linkage-specification (A.6), literal (A.2), literal-operator-id (A.11), logical-and-expression (A.4), logical-or-expression (A.4), long-long-suffix (A.2), long-suffix (A.2), lparen (A.14)
- **m**: mem-initializer (A.10), mem-initializer-id (A.10), mem-initializer-list (A.10), member-declaration (A.8), member-declarator (A.8), member-declarator-list (A.8), member-specification (A.8), multiplicative-expression (A.4)
- **n**: named-namespace-definition (A.6), namespace-alias (A.1/A.6), namespace-alias-definition (A.6), namespace-body (A.6), namespace-definition (A.6), namespace-name (A.1/A.6), nested-name-specifier (A.4), nested-namespace-definition (A.6), new-declarator (A.4), new-expression (A.4), new-initializer (A.4), new-line (A.14), new-placement (A.4), new-type-id (A.4), nodeclspec-function-declaration (A.6), noexcept-expression (A.4), noexcept-specifier (A.13), nondigit (A.2), nonzero-digit (A.2), noptr-abstract-declarator (A.7), noptr-abstract-pack-declarator (A.7), noptr-declarator (A.7), noptr-new-declarator (A.4)
- **o**: octal-digit (A.2), octal-escape-sequence (A.2), octal-literal (A.2), opaque-enum-declaration (A.6), operator (A.11), operator-function-id (A.11)
- **p**: parameter-declaration (A.7), parameter-declaration-clause (A.7), parameter-declaration-list (A.7), parameters-and-qualifiers (A.7), pm-expression (A.4), pointer-literal (A.2), postfix-expression (A.4), pp-number (A.2), pp-tokens (A.14), preprocessing-file (A.14), preprocessing-op-or-punc (A.2), preprocessing-token (A.2), primary-expression (A.4), pseudo-destructor-name (A.4), ptr-abstract-declarator (A.7), ptr-declarator (A.7), ptr-operator (A.7), pure-specifier (A.8)
- **q**: q-char (A.2), q-char-sequence (A.2), qualified-id (A.4), qualified-namespace-specifier (A.6)
- **r**: r-char (A.2), r-char-sequence (A.2), raw-string (A.2), ref-qualifier (A.7), relational-expression (A.4), replacement-list (A.14)
- **s**: s-char (A.2), s-char-sequence (A.2), selection-statement (A.5), shift-expression (A.4), sign (A.2), simple-capture (A.4), simple-declaration (A.6), simple-escape-sequence (A.2), simple-template-id (A.12), simple-type-specifier (A.6), statement (A.5), statement-seq (A.5), static_assert-declaration (A.6), storage-class-specifier (A.6), string-literal (A.2)
- **t**: template-argument (A.12), template-argument-list (A.12), template-declaration (A.12), template-id (A.12), template-name (A.1/A.12), template-parameter (A.12), template-parameter-list (A.12), text-line (A.14), throw-expression (A.4), token (A.2), trailing-return-type (A.7), translation-unit (A.3), try-block (A.13), type-id (A.7), type-name (A.6), type-parameter (A.12), type-parameter-key (A.12), type-specifier (A.6), type-specifier-seq (A.6), typedef-name (A.1/A.6), typename-specifier (A.12)
- **u**: ud-suffix (A.2), unary-expression (A.4), unary-operator (A.4), universal-character-name (A.2), unnamed-namespace-definition (A.6), unqualified-id (A.4), unsigned-suffix (A.2), user-defined-character-literal (A.2), user-defined-floating-literal (A.2), user-defined-integer-literal (A.2), user-defined-literal (A.2), user-defined-string-literal (A.2), using-declaration (A.6), using-declarator (A.6), using-declarator-list (A.6), using-directive (A.6)
- **v**: virt-specifier (A.8), virt-specifier-seq (A.8)

## Related

[[grammar-lexical-and-preprocessing]] · [[grammar-expressions-and-statements]] · [[grammar-declarations-and-classes]] · [[cpp17-general-principles]] · [[n4659-cpp17-draft-standard]] · [[cpp17-glossary]]
