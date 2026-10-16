---
type: concept
title: "Grammar lookup: declarations, declarators, classes, templates (A.3, A.6-A.12)"
tags: [cpp17, language-core, grammar]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Grammar lookup: declarations, declarators, classes and templates (Annex A.3, A.6-A.12)

Compact restatement of `[gram.basic]`, `[gram.dcl]`, `[gram.decl]`, `[gram.class]`, `[gram.derived]`, `[gram.special]`, `[gram.over]` and `[gram.temp]` (133 productions). The notation legend and the caveat that Annex A over-accepts (disambiguation and access/type rules weed things out) are on [[cpp17-grammar-summary]]. Semantics: [[cpp17-declarations]], [[cpp17-declarators]], [[cpp17-classes]], [[cpp17-derived-classes]], [[cpp17-special-member-functions]], [[cpp17-overloading]], [[cpp17-templates]].

## A.3 Basic concepts (`[gram.basic]`)

The start symbol of the language proper is translation-unit: an optional declaration-seq. (The preprocessor's own start symbol is preprocessing-file, on [[grammar-lexical-and-preprocessing]].)

- **translation-unit** → declaration-seq?

## A.6 Declarations (`[gram.dcl]`)

- **declaration** has 11 alternatives: block-declaration, nodeclspec-function-declaration, function-definition, template-declaration, deduction-guide, explicit-instantiation, explicit-specialization, linkage-specification, namespace-definition, empty-declaration, attribute-declaration. **block-declaration** has 8: simple-declaration, asm-definition, namespace-alias-definition, using-declaration, using-directive, static_assert-declaration, alias-declaration, opaque-enum-declaration. Only block-declarations can appear as a statement (`declaration-statement` in [[grammar-expressions-and-statements]]).
- **simple-declaration** has three shapes: the usual decl-specifier-seq plus an optional init-declarator-list; the same preceded by an attribute-specifier-seq with a mandatory declarator list; and the **structured binding** form (attributes, specifiers, optional ref-qualifier, an identifier-list in square brackets, and a mandatory initializer). See [[structured-bindings]].
- **nodeclspec-function-declaration** is a declarator followed by `;` with no decl-specifier-seq at all (the shape of constructors, destructors and conversion functions declared outside a class).
- **decl-specifier-seq**: any number of decl-specifiers (storage class, defining-type-specifier, function-specifier, `friend`, `typedef`, `constexpr`, `inline`); an attribute-specifier-seq may follow only the last one. type-specifier-seq and defining-type-specifier-seq are the variants without storage-class and function specifiers.
- **Types**: simple-type-specifier lists the built-in type keywords, `auto`, a type-name, a template-name (for class template argument deduction) and decltype-specifier (`decltype ( expression )` or `decltype ( auto )`).
- **Enums**: enum-key is `enum`, `enum class` or `enum struct`; enum-base is a colon and a type-specifier-seq; an enumerator list may end with a trailing comma; an opaque-enum-declaration redeclares with the base. See [[cpp17-declarations]].
- **Namespaces**: named, unnamed and nested definitions. `inline` is a grammar option on named and unnamed definitions only; the nested form (`namespace A::B { ... }`) takes an enclosing-namespace-specifier and has neither `inline` nor attributes. using-declarations accept a list with pack expansion; using-directive and namespace aliases are separate productions.
- **Attributes** (grammar only; semantics in [[attributes]]): an attribute-specifier is two opening square brackets, an optional `using ns :` prefix, an attribute-list, and two closing brackets, or an alignment-specifier (`alignas`). An attribute-list may have empty entries and pack expansions; an attribute is an optional-scope token plus an optional parenthesized balanced-token sequence.

- **declaration-seq** → declaration ¦ declaration-seq declaration
- **declaration** → block-declaration ¦ nodeclspec-function-declaration ¦ function-definition ¦ template-declaration ¦ deduction-guide ¦ explicit-instantiation ¦ explicit-specialization ¦ linkage-specification ¦ namespace-definition ¦ empty-declaration ¦ attribute-declaration
- **block-declaration** → simple-declaration ¦ asm-definition ¦ namespace-alias-definition ¦ using-declaration ¦ using-directive ¦ static_assert-declaration ¦ alias-declaration ¦ opaque-enum-declaration
- **nodeclspec-function-declaration** → attribute-specifier-seq? declarator `;`
- **alias-declaration** → `using` identifier attribute-specifier-seq? `=` defining-type-id `;`
- **simple-declaration** → decl-specifier-seq init-declarator-list? `;` ¦ attribute-specifier-seq decl-specifier-seq init-declarator-list `;` ¦ attribute-specifier-seq? decl-specifier-seq ref-qualifier? `[` identifier-list `]` initializer `;`
- **static_assert-declaration** → `static_assert` `(` constant-expression `)` `;` ¦ `static_assert` `(` constant-expression `,` string-literal `)` `;`
- **empty-declaration** → `;`
- **attribute-declaration** → attribute-specifier-seq `;`
- **decl-specifier** → storage-class-specifier ¦ defining-type-specifier ¦ function-specifier ¦ `friend` ¦ `typedef` ¦ `constexpr` ¦ `inline`
- **decl-specifier-seq** → decl-specifier attribute-specifier-seq? ¦ decl-specifier decl-specifier-seq
- **storage-class-specifier** → `static` ¦ `thread_local` ¦ `extern` ¦ `mutable`
- **function-specifier** → `virtual` ¦ `explicit`
- **typedef-name** → identifier
- **type-specifier** → simple-type-specifier ¦ elaborated-type-specifier ¦ typename-specifier ¦ cv-qualifier
- **type-specifier-seq** → type-specifier attribute-specifier-seq? ¦ type-specifier type-specifier-seq
- **defining-type-specifier** → type-specifier ¦ class-specifier ¦ enum-specifier
- **defining-type-specifier-seq** → defining-type-specifier attribute-specifier-seq? ¦ defining-type-specifier defining-type-specifier-seq
- **simple-type-specifier** → nested-name-specifier? type-name ¦ nested-name-specifier `template` simple-template-id ¦ nested-name-specifier? template-name ¦ `char` ¦ `char16_t` ¦ `char32_t` ¦ `wchar_t` ¦ `bool` ¦ `short` ¦ `int` ¦ `long` ¦ `signed` ¦ `unsigned` ¦ `float` ¦ `double` ¦ `void` ¦ `auto` ¦ decltype-specifier
- **type-name** → class-name ¦ enum-name ¦ typedef-name ¦ simple-template-id
- **decltype-specifier** → `decltype` `(` expression `)` ¦ `decltype` `(` `auto` `)`
- **elaborated-type-specifier** → class-key attribute-specifier-seq? nested-name-specifier? identifier ¦ class-key simple-template-id ¦ class-key nested-name-specifier `template`? simple-template-id ¦ `enum` nested-name-specifier? identifier
- **enum-name** → identifier
- **enum-specifier** → enum-head `{` enumerator-list? `}` ¦ enum-head `{` enumerator-list `,` `}`
- **enum-head** → enum-key attribute-specifier-seq? enum-head-name? enum-base?
- **enum-head-name** → nested-name-specifier? identifier
- **opaque-enum-declaration** → enum-key attribute-specifier-seq? nested-name-specifier? identifier enum-base? `;`
- **enum-key** → `enum` ¦ `enum` `class` ¦ `enum` `struct`
- **enum-base** → `:` type-specifier-seq
- **enumerator-list** → enumerator-definition ¦ enumerator-list `,` enumerator-definition
- **enumerator-definition** → enumerator ¦ enumerator `=` constant-expression
- **enumerator** → identifier attribute-specifier-seq?
- **namespace-name** → identifier ¦ namespace-alias
- **namespace-definition** → named-namespace-definition ¦ unnamed-namespace-definition ¦ nested-namespace-definition
- **named-namespace-definition** → `inline`? `namespace` attribute-specifier-seq? identifier `{` namespace-body `}`
- **unnamed-namespace-definition** → `inline`? `namespace` attribute-specifier-seq? `{` namespace-body `}`
- **nested-namespace-definition** → `namespace` enclosing-namespace-specifier `::` identifier `{` namespace-body `}`
- **enclosing-namespace-specifier** → identifier ¦ enclosing-namespace-specifier `::` identifier
- **namespace-body** → declaration-seq?
- **namespace-alias** → identifier
- **namespace-alias-definition** → `namespace` identifier `=` qualified-namespace-specifier `;`
- **qualified-namespace-specifier** → nested-name-specifier? namespace-name
- **using-declaration** → `using` using-declarator-list `;`
- **using-declarator-list** → using-declarator `...`? ¦ using-declarator-list `,` using-declarator `...`?
- **using-declarator** → `typename`? nested-name-specifier unqualified-id
- **using-directive** → attribute-specifier-seq? `using` `namespace` nested-name-specifier? namespace-name `;`
- **asm-definition** → attribute-specifier-seq? `asm` `(` string-literal `)` `;`
- **linkage-specification** → `extern` string-literal `{` declaration-seq? `}` ¦ `extern` string-literal declaration
- **attribute-specifier-seq** → attribute-specifier-seq? attribute-specifier
- **attribute-specifier** → `[` `[` attribute-using-prefix? attribute-list `]` `]` ¦ alignment-specifier
- **alignment-specifier** → `alignas` `(` type-id `...`? `)` ¦ `alignas` `(` constant-expression `...`? `)`
- **attribute-using-prefix** → `using` attribute-namespace `:`
- **attribute-list** → attribute? ¦ attribute-list `,` attribute? ¦ attribute `...` ¦ attribute-list `,` attribute `...`
- **attribute** → attribute-token attribute-argument-clause?
- **attribute-token** → identifier ¦ attribute-scoped-token
- **attribute-scoped-token** → attribute-namespace `::` identifier
- **attribute-namespace** → identifier
- **attribute-argument-clause** → `(` balanced-token-seq? `)`
- **balanced-token-seq** → balanced-token ¦ balanced-token-seq balanced-token
- **balanced-token** → `(` balanced-token-seq? `)` ¦ `[` balanced-token-seq? `]` ¦ `{` balanced-token-seq? `}` ¦ *any token other than a parenthesis, a bracket, or a brace*

## A.7 Declarators (`[gram.decl]`)

- **declarator** is either a ptr-declarator or the trailing-return-type shape (`noptr-declarator parameters-and-qualifiers -> type-id`). Pointer, reference and pointer-to-member operators are ptr-operators and nest to the left of the declared name; arrays and function parameter lists nest to the right (noptr-declarator), with parentheses regrouping. See [[cpp17-declarators]].
- **parameters-and-qualifiers** gathers the parameter-declaration-clause with the member-function suffixes in a fixed order: cv-qualifier-seq, ref-qualifier, noexcept-specifier, attribute-specifier-seq.
- The **abstract-declarator** family mirrors the declarator family without a name (for type-ids), plus abstract-pack-declarator for pack expansions. type-id is a type-specifier-seq with an optional abstract-declarator; defining-type-id (used by alias declarations) also permits class and enum definitions.
- **function-body** (in function-definition) is one of: optional ctor-initializer and compound-statement; a function-try-block; `= default ;`; `= delete ;`.
- **Initializers**: an initializer is a brace-or-equal-initializer or a parenthesized expression-list. A braced-init-list is `{`, an initializer-list with an optional trailing comma, `}`, or `{ }`; list elements are initializer-clauses with optional pack expansion. expr-or-braced-init-list lets an expression slot also take a braced list. See [[initialization]].

- **init-declarator-list** → init-declarator ¦ init-declarator-list `,` init-declarator
- **init-declarator** → declarator initializer?
- **declarator** → ptr-declarator ¦ noptr-declarator parameters-and-qualifiers trailing-return-type
- **ptr-declarator** → noptr-declarator ¦ ptr-operator ptr-declarator
- **noptr-declarator** → declarator-id attribute-specifier-seq? ¦ noptr-declarator parameters-and-qualifiers ¦ noptr-declarator `[` constant-expression? `]` attribute-specifier-seq? ¦ `(` ptr-declarator `)`
- **parameters-and-qualifiers** → `(` parameter-declaration-clause `)` cv-qualifier-seq? ref-qualifier? noexcept-specifier? attribute-specifier-seq?
- **trailing-return-type** → `->` type-id
- **ptr-operator** → `*` attribute-specifier-seq? cv-qualifier-seq? ¦ `&` attribute-specifier-seq? ¦ `&&` attribute-specifier-seq? ¦ nested-name-specifier `*` attribute-specifier-seq? cv-qualifier-seq?
- **cv-qualifier-seq** → cv-qualifier cv-qualifier-seq?
- **cv-qualifier** → `const` ¦ `volatile`
- **ref-qualifier** → `&` ¦ `&&`
- **declarator-id** → `...`? id-expression
- **type-id** → type-specifier-seq abstract-declarator?
- **defining-type-id** → defining-type-specifier-seq abstract-declarator?
- **abstract-declarator** → ptr-abstract-declarator ¦ noptr-abstract-declarator? parameters-and-qualifiers trailing-return-type ¦ abstract-pack-declarator
- **ptr-abstract-declarator** → noptr-abstract-declarator ¦ ptr-operator ptr-abstract-declarator?
- **noptr-abstract-declarator** → noptr-abstract-declarator? parameters-and-qualifiers ¦ noptr-abstract-declarator? `[` constant-expression? `]` attribute-specifier-seq? ¦ `(` ptr-abstract-declarator `)`
- **abstract-pack-declarator** → noptr-abstract-pack-declarator ¦ ptr-operator abstract-pack-declarator
- **noptr-abstract-pack-declarator** → noptr-abstract-pack-declarator parameters-and-qualifiers ¦ noptr-abstract-pack-declarator `[` constant-expression? `]` attribute-specifier-seq? ¦ `...`
- **parameter-declaration-clause** → parameter-declaration-list? `...`? ¦ parameter-declaration-list `,` `...`
- **parameter-declaration-list** → parameter-declaration ¦ parameter-declaration-list `,` parameter-declaration
- **parameter-declaration** → attribute-specifier-seq? decl-specifier-seq declarator ¦ attribute-specifier-seq? decl-specifier-seq declarator `=` initializer-clause ¦ attribute-specifier-seq? decl-specifier-seq abstract-declarator? ¦ attribute-specifier-seq? decl-specifier-seq abstract-declarator? `=` initializer-clause
- **function-definition** → attribute-specifier-seq? decl-specifier-seq? declarator virt-specifier-seq? function-body
- **function-body** → ctor-initializer? compound-statement ¦ function-try-block ¦ `=` `default` `;` ¦ `=` `delete` `;`
- **initializer** → brace-or-equal-initializer ¦ `(` expression-list `)`
- **brace-or-equal-initializer** → `=` initializer-clause ¦ braced-init-list
- **initializer-clause** → assignment-expression ¦ braced-init-list
- **initializer-list** → initializer-clause `...`? ¦ initializer-list `,` initializer-clause `...`?
- **braced-init-list** → `{` initializer-list `,`? `}` ¦ `{` `}`
- **expr-or-braced-init-list** → expression ¦ braced-init-list

## A.8 Classes (`[gram.class]`)

A class-specifier is a class-head, a brace-enclosed optional member-specification. The head is a class-key (`class`, `struct`, `union`), optional attributes, an optional class-head-name with optional `final` and optional base-clause; an unnamed class has no name and no `final`. A member-declaration is a declaration with an optional decl-specifier-seq and member-declarator-list, or one of function-definition, using-declaration, static_assert, template-declaration, deduction-guide, alias-declaration, empty-declaration. Member declarators cover plain declarators with virt-specifiers (`override`, `final`) and a pure-specifier (`= 0`), declarators with a default member initializer, and bit-fields (an optional name, then a colon and a constant-expression). See [[cpp17-classes]].

- **class-name** → identifier ¦ simple-template-id
- **class-specifier** → class-head `{` member-specification? `}`
- **class-head** → class-key attribute-specifier-seq? class-head-name class-virt-specifier? base-clause? ¦ class-key attribute-specifier-seq? base-clause?
- **class-head-name** → nested-name-specifier? class-name
- **class-virt-specifier** → `final`
- **class-key** → `class` ¦ `struct` ¦ `union`
- **member-specification** → member-declaration member-specification? ¦ access-specifier `:` member-specification?
- **member-declaration** → attribute-specifier-seq? decl-specifier-seq? member-declarator-list? `;` ¦ function-definition ¦ using-declaration ¦ static_assert-declaration ¦ template-declaration ¦ deduction-guide ¦ alias-declaration ¦ empty-declaration
- **member-declarator-list** → member-declarator ¦ member-declarator-list `,` member-declarator
- **member-declarator** → declarator virt-specifier-seq? pure-specifier? ¦ declarator brace-or-equal-initializer? ¦ identifier? attribute-specifier-seq? `:` constant-expression
- **virt-specifier-seq** → virt-specifier ¦ virt-specifier-seq virt-specifier
- **virt-specifier** → `override` ¦ `final`
- **pure-specifier** → `=` `0`

## A.9 Derived classes (`[gram.derived]`)

A base-clause is a colon and a list of base-specifiers, each with optional pack expansion. A base-specifier is a class-or-decltype with optional attributes, `virtual`, and access-specifier in either order. See [[cpp17-derived-classes]], [[cpp17-member-access-control]].

- **base-clause** → `:` base-specifier-list
- **base-specifier-list** → base-specifier `...`? ¦ base-specifier-list `,` base-specifier `...`?
- **base-specifier** → attribute-specifier-seq? class-or-decltype ¦ attribute-specifier-seq? `virtual` access-specifier? class-or-decltype ¦ attribute-specifier-seq? access-specifier `virtual`? class-or-decltype
- **class-or-decltype** → nested-name-specifier? class-name ¦ nested-name-specifier `template` simple-template-id ¦ decltype-specifier
- **access-specifier** → `private` ¦ `protected` ¦ `public`

## A.10 Special member functions (`[gram.special]`)

Conversion-function-id (`operator` plus a conversion-type-id), and the constructor initializer list: ctor-initializer is a colon and a mem-initializer-list, each mem-initializer naming a class-or-decltype or identifier followed by parenthesized arguments or a braced list. See [[cpp17-special-member-functions]].

- **conversion-function-id** → `operator` conversion-type-id
- **conversion-type-id** → type-specifier-seq conversion-declarator?
- **conversion-declarator** → ptr-operator conversion-declarator?
- **ctor-initializer** → `:` mem-initializer-list
- **mem-initializer-list** → mem-initializer `...`? ¦ mem-initializer-list `,` mem-initializer `...`?
- **mem-initializer** → mem-initializer-id `(` expression-list? `)` ¦ mem-initializer-id braced-init-list
- **mem-initializer-id** → class-or-decltype ¦ identifier

## A.11 Overloading (`[gram.over]`)

The overloadable operator set: the keywords `new`/`delete` and their array forms, the arithmetic, bitwise, comparison and logical operators, the assignment family, `++`, `--`, `,`, `->*`, `->`, the call operator and subscripting. A literal-operator-id has two spellings: `operator` followed by a string-literal (normally empty) and an identifier, or `operator` followed by a user-defined-string-literal. See [[cpp17-overloading]].

- **operator-function-id** → `operator` operator
- **operator**: one of `new` `delete` `new[]` `delete[]` `+` `-` `*` `/` `%` `^` `&` `|` `~` `!` `=` `<` `>` `+=` `-=` `*=` `/=` `%=` `^=` `&=` `|=` `<<` `>>` `>>=` `<<=` `==` `!=` `<=` `>=` `&&` `||` `++` `--` `,` `->*` `->` `()` `[]`
- **literal-operator-id** → `operator` string-literal identifier ¦ `operator` user-defined-string-literal

## A.12 Templates (`[gram.temp]`)

- template-declaration: `template < template-parameter-list > declaration`; explicit-specialization is `template < >` plus a declaration; explicit-instantiation is optional `extern`, `template`, a declaration.
- A template-parameter is a type-parameter (`class` or `typename`, with optional pack `...`, optional name, optional default type-id; or a template template parameter whose default is an id-expression) or an ordinary parameter-declaration (non-type).
- A template-argument is a constant-expression, a type-id or an id-expression; a simple-template-id is a template-name and an optional argument list in angle brackets; template-id additionally allows operator-function-id and literal-operator-id as the name.
- typename-specifier: `typename`, nested-name-specifier, then an identifier or an optional-`template` simple-template-id.
- deduction-guide: optional `explicit`, a template-name, a parenthesized parameter-declaration-clause, `->` and a simple-template-id, then `;`.

See [[cpp17-templates]], [[template-argument-deduction]], [[dependent-names-and-instantiation]].

- **template-declaration** → `template` `<` template-parameter-list `>` declaration
- **template-parameter-list** → template-parameter ¦ template-parameter-list `,` template-parameter
- **template-parameter** → type-parameter ¦ parameter-declaration
- **type-parameter** → type-parameter-key `...`? identifier? ¦ type-parameter-key identifier? `=` type-id ¦ `template` `<` template-parameter-list `>` type-parameter-key `...`? identifier? ¦ `template` `<` template-parameter-list `>` type-parameter-key identifier? `=` id-expression
- **type-parameter-key** → `class` ¦ `typename`
- **simple-template-id** → template-name `<` template-argument-list? `>`
- **template-id** → simple-template-id ¦ operator-function-id `<` template-argument-list? `>` ¦ literal-operator-id `<` template-argument-list? `>`
- **template-name** → identifier
- **template-argument-list** → template-argument `...`? ¦ template-argument-list `,` template-argument `...`?
- **template-argument** → constant-expression ¦ type-id ¦ id-expression
- **typename-specifier** → `typename` nested-name-specifier identifier ¦ `typename` nested-name-specifier `template`? simple-template-id
- **explicit-instantiation** → `extern`? `template` declaration
- **explicit-specialization** → `template` `<` `>` declaration
- **deduction-guide** → `explicit`? template-name `(` parameter-declaration-clause `)` `->` simple-template-id `;`

## Related

[[cpp17-grammar-summary]] · [[grammar-expressions-and-statements]] · [[grammar-lexical-and-preprocessing]] · [[cpp17-declarations]] · [[cpp17-declarators]] · [[cpp17-classes]] · [[cpp17-templates]]
