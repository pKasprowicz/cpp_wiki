---
type: concept
title: "Grammar lookup: expressions, statements, exception handling (A.4, A.5, A.13)"
tags: [cpp17, language-core, grammar]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Grammar lookup: expressions, statements and exception handling (Annex A.4, A.5, A.13)

Compact restatement of `[gram.expr]` (47 productions), `[gram.stmt]` (13) and `[gram.except]` (6). Notation legend and the "superset of valid C++" caveat are on [[cpp17-grammar-summary]]. Meaning of the constructs: [[cpp17-expressions]], [[cpp17-statements]], [[cpp17-exception-handling]].

## A.4 Expressions (`[gram.expr]`)

### The precedence ladder

The grammar encodes operator precedence by layering: each level is defined in terms of the next tighter one. From loosest to tightest (each row's operand is the row below it):

| Level | Production | Operators at this level (in the grammar) |
|---|---|---|
| 1 | expression | `,` (left-recursive list of assignment-expressions) |
| 2 | assignment-expression | the assignment operators (right operand is an initializer-clause, so a braced list is accepted); also `throw` expressions and the conditional level |
| 3 | conditional-expression | `?:` (middle operand is a full expression, last operand an assignment-expression) |
| 4-5 | logical-or, logical-and | `\|\|`, `&&` |
| 6-8 | inclusive-or, exclusive-or, and | `\|`, `^`, `&` |
| 9 | equality | `==`, `!=` |
| 10 | relational | `<`, `>`, `<=`, `>=` (no three-way comparison in this grammar) |
| 11 | shift | `<<`, `>>` |
| 12 | additive | `+`, `-` |
| 13 | multiplicative | `*`, `/`, `%` |
| 14 | pm-expression | `.*`, `->*` |
| 15 | cast-expression | the C-style cast `( type-id ) cast-expression`, otherwise unary |
| 16 | unary-expression | prefix `++`/`--`, unary operators `* & + - ! ~`, `sizeof` (three forms), `alignof ( type-id )`, `noexcept ( expression )`, new- and delete-expressions |
| 17 | postfix-expression | subscripting, calls, functional casts, member access, postfix `++`/`--`, the four named casts, `typeid` |
| 18 | primary-expression | literals, `this`, parenthesized expression, id-expression, lambda, fold-expression |

Because the binary levels are left-recursive, they associate left to right; the right-recursive shape of assignment (`logical-or-expression assignment-operator initializer-clause`) is what makes assignment right-associative in the grammar. Constant-expression is simply a conditional-expression (the extra restrictions are semantic: [[constant-expressions]]). Expression-list is an initializer-list, so call arguments may contain braced lists and pack expansions.

### Points worth noticing

- **Lambda**: introducer is `[`, optional capture, `]`; the declarator part is optional and allows a decl-specifier-seq (which specifiers are meaningful is decided by the semantic rules; for example `mutable` controls whether the call operator is const, `[expr.prim.lambda.closure]/4`), a noexcept-specifier, attributes and a trailing return type. Captures: a default (`&` or `=`), a list, or both; each item is a simple capture (`x`, `&x`, `this`, `*this`) or an init-capture, with optional pack expansion. See [[lambda-expressions]].
- **Fold expression**: three shapes (unary right fold, unary left fold, binary fold with the operator repeated); the operator is one of 32 binary operators including all assignments, `,`, `.*` and `->*`. See [[fold-expressions]].
- **Postfix** also covers `typename`-specifier calls and braced construction (`T{...}`), the pseudo-destructor forms, and the dotted/arrow forms with an optional `template` keyword.
- **new-expression**: optional leading `::`, optional placement, then either a new-type-id or a parenthesized type-id, then an optional initializer; array bounds in a new-declarator allow an expression for the first dimension and constant-expressions after. **delete-expression** has the plain and the `delete [ ]` forms. See [[new-and-delete-expressions]].
- **Cast**: the four named casts are postfix-expressions; only the C-style cast sits at the cast-expression level. See [[cast-expressions]].

- **primary-expression** → literal ¦ `this` ¦ `(` expression `)` ¦ id-expression ¦ lambda-expression ¦ fold-expression
- **id-expression** → unqualified-id ¦ qualified-id
- **unqualified-id** → identifier ¦ operator-function-id ¦ conversion-function-id ¦ literal-operator-id ¦ `~` class-name ¦ `~` decltype-specifier ¦ template-id
- **qualified-id** → nested-name-specifier `template`? unqualified-id
- **nested-name-specifier** → `::` ¦ type-name `::` ¦ namespace-name `::` ¦ decltype-specifier `::` ¦ nested-name-specifier identifier `::` ¦ nested-name-specifier `template`? simple-template-id `::`
- **lambda-expression** → lambda-introducer lambda-declarator? compound-statement
- **lambda-introducer** → `[` lambda-capture? `]`
- **lambda-declarator** → `(` parameter-declaration-clause `)` decl-specifier-seq? noexcept-specifier? attribute-specifier-seq? trailing-return-type?
- **lambda-capture** → capture-default ¦ capture-list ¦ capture-default `,` capture-list
- **capture-default** → `&` ¦ `=`
- **capture-list** → capture `...`? ¦ capture-list `,` capture `...`?
- **capture** → simple-capture ¦ init-capture
- **simple-capture** → identifier ¦ `&` identifier ¦ `this` ¦ `*` `this`
- **init-capture** → identifier initializer ¦ `&` identifier initializer
- **fold-expression** → `(` cast-expression fold-operator `...` `)` ¦ `(` `...` fold-operator cast-expression `)` ¦ `(` cast-expression fold-operator `...` fold-operator cast-expression `)`
- **fold-operator**: one of `+` `-` `*` `/` `%` `^` `&` `|` `<<` `>>` `+=` `-=` `*=` `/=` `%=` `^=` `&=` `|=` `<<=` `>>=` `=` `==` `!=` `<` `>` `<=` `>=` `&&` `||` `,` `.*` `->*`
- **postfix-expression** → primary-expression ¦ postfix-expression `[` expr-or-braced-init-list `]` ¦ postfix-expression `(` expression-list? `)` ¦ simple-type-specifier `(` expression-list? `)` ¦ typename-specifier `(` expression-list? `)` ¦ simple-type-specifier braced-init-list ¦ typename-specifier braced-init-list ¦ postfix-expression `.` `template`? id-expression ¦ postfix-expression `->` `template`? id-expression ¦ postfix-expression `.` pseudo-destructor-name ¦ postfix-expression `->` pseudo-destructor-name ¦ postfix-expression `++` ¦ postfix-expression `--` ¦ `dynamic_cast` `<` type-id `>` `(` expression `)` ¦ `static_cast` `<` type-id `>` `(` expression `)` ¦ `reinterpret_cast` `<` type-id `>` `(` expression `)` ¦ `const_cast` `<` type-id `>` `(` expression `)` ¦ `typeid` `(` expression `)` ¦ `typeid` `(` type-id `)`
- **expression-list** → initializer-list
- **pseudo-destructor-name** → nested-name-specifier? type-name `::` `~` type-name ¦ nested-name-specifier `template` simple-template-id `::` `~` type-name ¦ `~` type-name ¦ `~` decltype-specifier
- **unary-expression** → postfix-expression ¦ `++` cast-expression ¦ `--` cast-expression ¦ unary-operator cast-expression ¦ `sizeof` unary-expression ¦ `sizeof` `(` type-id `)` ¦ `sizeof` `...` `(` identifier `)` ¦ `alignof` `(` type-id `)` ¦ noexcept-expression ¦ new-expression ¦ delete-expression
- **unary-operator**: one of `*` `&` `+` `-` `!` `~`
- **new-expression** → `::`? `new` new-placement? new-type-id new-initializer? ¦ `::`? `new` new-placement? `(` type-id `)` new-initializer?
- **new-placement** → `(` expression-list `)`
- **new-type-id** → type-specifier-seq new-declarator?
- **new-declarator** → ptr-operator new-declarator? ¦ noptr-new-declarator
- **noptr-new-declarator** → `[` expression `]` attribute-specifier-seq? ¦ noptr-new-declarator `[` constant-expression `]` attribute-specifier-seq?
- **new-initializer** → `(` expression-list? `)` ¦ braced-init-list
- **delete-expression** → `::`? `delete` cast-expression ¦ `::`? `delete` `[` `]` cast-expression
- **noexcept-expression** → `noexcept` `(` expression `)`
- **cast-expression** → unary-expression ¦ `(` type-id `)` cast-expression
- **pm-expression** → cast-expression ¦ pm-expression `.*` cast-expression ¦ pm-expression `->*` cast-expression
- **multiplicative-expression** → pm-expression ¦ multiplicative-expression `*` pm-expression ¦ multiplicative-expression `/` pm-expression ¦ multiplicative-expression `%` pm-expression
- **additive-expression** → multiplicative-expression ¦ additive-expression `+` multiplicative-expression ¦ additive-expression `-` multiplicative-expression
- **shift-expression** → additive-expression ¦ shift-expression `<<` additive-expression ¦ shift-expression `>>` additive-expression
- **relational-expression** → shift-expression ¦ relational-expression `<` shift-expression ¦ relational-expression `>` shift-expression ¦ relational-expression `<=` shift-expression ¦ relational-expression `>=` shift-expression
- **equality-expression** → relational-expression ¦ equality-expression `==` relational-expression ¦ equality-expression `!=` relational-expression
- **and-expression** → equality-expression ¦ and-expression `&` equality-expression
- **exclusive-or-expression** → and-expression ¦ exclusive-or-expression `^` and-expression
- **inclusive-or-expression** → exclusive-or-expression ¦ inclusive-or-expression `|` exclusive-or-expression
- **logical-and-expression** → inclusive-or-expression ¦ logical-and-expression `&&` inclusive-or-expression
- **logical-or-expression** → logical-and-expression ¦ logical-or-expression `||` logical-and-expression
- **conditional-expression** → logical-or-expression ¦ logical-or-expression `?` expression `:` assignment-expression
- **throw-expression** → `throw` assignment-expression?
- **assignment-expression** → conditional-expression ¦ logical-or-expression assignment-operator initializer-clause ¦ throw-expression
- **assignment-operator**: one of `=` `*=` `/=` `%=` `+=` `-=` `>>=` `<<=` `&=` `^=` `|=`
- **expression** → assignment-expression ¦ expression `,` assignment-expression
- **constant-expression** → conditional-expression

## A.5 Statements (`[gram.stmt]`)

- A `statement` is a labeled statement, a declaration statement, or one of expression/compound/selection/iteration/jump/try-block, each of those (except labeled and declaration statements) taking an optional leading attribute-specifier-seq. A labeled statement carries its own attribute prefix.
- `if` takes an optional `constexpr`; `if` and `switch` accept an optional init-statement before the condition, which is an expression-statement or a simple-declaration (so it ends with its own semicolon). A **condition** is an expression or a declaration with a brace-or-equal-initializer.
- The range-based `for` declares through for-range-declaration, which includes the structured-binding form with an identifier-list in square brackets and an optional ref-qualifier. The loop range is an expr-or-braced-init-list.
- `return` accepts an expr-or-braced-init-list. Semantics (conditions, if-constexpr discard, range-for expansion): [[cpp17-statements]].

- **statement** → labeled-statement ¦ attribute-specifier-seq? expression-statement ¦ attribute-specifier-seq? compound-statement ¦ attribute-specifier-seq? selection-statement ¦ attribute-specifier-seq? iteration-statement ¦ attribute-specifier-seq? jump-statement ¦ declaration-statement ¦ attribute-specifier-seq? try-block
- **init-statement** → expression-statement ¦ simple-declaration
- **condition** → expression ¦ attribute-specifier-seq? decl-specifier-seq declarator brace-or-equal-initializer
- **labeled-statement** → attribute-specifier-seq? identifier `:` statement ¦ attribute-specifier-seq? `case` constant-expression `:` statement ¦ attribute-specifier-seq? `default` `:` statement
- **expression-statement** → expression? `;`
- **compound-statement** → `{` statement-seq? `}`
- **statement-seq** → statement ¦ statement-seq statement
- **selection-statement** → `if` `constexpr`? `(` init-statement? condition `)` statement ¦ `if` `constexpr`? `(` init-statement? condition `)` statement `else` statement ¦ `switch` `(` init-statement? condition `)` statement
- **iteration-statement** → `while` `(` condition `)` statement ¦ `do` statement `while` `(` expression `)` `;` ¦ `for` `(` init-statement condition? `;` expression? `)` statement ¦ `for` `(` for-range-declaration `:` for-range-initializer `)` statement
- **for-range-declaration** → attribute-specifier-seq? decl-specifier-seq declarator ¦ attribute-specifier-seq? decl-specifier-seq ref-qualifier? `[` identifier-list `]`
- **for-range-initializer** → expr-or-braced-init-list
- **jump-statement** → `break` `;` ¦ `continue` `;` ¦ `return` expr-or-braced-init-list? `;` ¦ `goto` identifier `;`
- **declaration-statement** → block-declaration

## A.13 Exception handling (`[gram.except]`)

- A try-block is `try`, a compound-statement and a handler-seq of one or more handlers; a function-try-block adds an optional ctor-initializer between `try` and the body (used by `function-body` in [[grammar-declarations-and-classes]]).
- A handler is `catch ( exception-declaration )` plus a compound-statement; the declaration is a type-specifier-seq with a declarator or abstract-declarator (with optional attributes) or just `...`.
- A noexcept-specifier has three shapes: `noexcept ( constant-expression )`, bare `noexcept`, and `throw ( )`. The last form is the deprecated one kept in Annex D (`[depr.except.spec]`, see [[cpp17-annex-d-compatibility-features]]).

- **try-block** → `try` compound-statement handler-seq
- **function-try-block** → `try` ctor-initializer? compound-statement handler-seq
- **handler-seq** → handler handler-seq?
- **handler** → `catch` `(` exception-declaration `)` compound-statement
- **exception-declaration** → attribute-specifier-seq? type-specifier-seq declarator ¦ attribute-specifier-seq? type-specifier-seq abstract-declarator? ¦ `...`
- **noexcept-specifier** → `noexcept` `(` constant-expression `)` ¦ `noexcept` ¦ `throw` `(` `)`

## Related

[[cpp17-grammar-summary]] · [[grammar-declarations-and-classes]] · [[grammar-lexical-and-preprocessing]] · [[cpp17-expressions]] · [[cpp17-statements]] · [[cpp17-exception-handling]] · [[sequencing-and-evaluation-order]]
