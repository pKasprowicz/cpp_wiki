---
type: concept
title: "C++17 clause 9: statements"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 9: Statements (`[stmt.stmt]`)

About 2,900 words; 18 sections. Statements execute in sequence unless noted.

## Conditions (`[stmt.stmt]/2-6`)

A **condition** is an expression or a declaration with initializer (`decl-specifier-seq declarator = ...`/braced init). The declarator may not specify a function or array; no class/enum may be defined in the decl-specifier-seq; `auto` is deduced from the initializer; decl-specifiers are type-specifiers or `constexpr`. A name introduced in a condition is in scope from its declaration to the end of the controlled substatements and may not be redeclared in their outermost block. Condition value: the variable (or expression) contextually converted to `bool`, except in `switch`, where it is the integral/enumeration value (class types are implicitly converted). Anything that parses as either an expression or a block-scope declaration is a **declaration**.

## Selection (`[stmt.select]`)

- Substatements implicitly define block scope (a single statement is treated as if wrapped in braces).
- **`if`** (`[stmt.if]`): runs the first substatement if the condition is true, the `else` part otherwise. A dangling `else` inside the first substatement must have its own `else`.
- **`if constexpr`**: the condition must be a contextually converted constant expression of type `bool`; the not-chosen substatement is a **discarded statement**. In a template, if the condition is not value-dependent after instantiation, the discarded substatement is not instantiated. Labels (`case`/`default`, goto targets) inside obey locality rules.
- **init-statement** form: `if (init; cond) ...` is equivalent to `{ init; if (cond) ... }` except that names from the init-statement are in the *same declarative region* as the condition's names (so they are visible in the `else` too). The same equivalence defines `switch (init; cond)`.
- **`switch`** (`[stmt.switch]`): condition of integral, enumeration or class type (converted); integral promotions apply; each `case` constant is a *converted constant expression* of the adjusted type and no two may be equal; at most one `default`; labels associate with the nearest enclosing `switch`; execution falls through labels; with no match and no `default` nothing runs.

## Iteration (`[stmt.iter]`)

- Substatements define a block scope entered/exited every iteration. Names from an init-statement / for-range-declaration cannot be redeclared in the outermost block of the body.
- **`while`**: a declared condition variable is destroyed and recreated each iteration (equivalent label-and-`goto` expansion given in the text).
- **`do`**: test after the body.
- **`for`**: equals `{ init; while (cond) { stmt; expr; } }` except `continue` runs `expr` before re-testing; missing condition means `true`.
- **Range-based `for`** (`[stmt.ranged]`): expands to
  `auto&& __range = init; auto __begin = begin-expr; auto __end = end-expr; for (; __begin != __end; ++__begin) { decl = *__begin; stmt }`. `__begin` and `__end` are separate `auto` variables (they need not have the same type). The `for-range-declaration` may be a structured binding (`[ identifier-list ]`, see [[structured-bindings]]). `begin-expr`/`end-expr`: array → `__range`/`__range + bound` (unknown/incomplete bound ill-formed); class type with member `begin` or `end` found → `__range.begin()`/`.end()`; otherwise ADL `begin(__range)`/`end(__range)` ([[name-lookup]]).

## Jump (`[stmt.jump]`)

- Leaving a scope destroys its automatic objects in reverse order of construction.
- `break` only in iteration/`switch`; `continue` only in iteration (equivalent to `goto contin;` at the loop's end).
- **`return`** (`[stmt.return]`): an operand-less `return` is for `void` functions, constructors, destructors; an operand of type `void` only in a `void` function; otherwise the operand copy-initializes the call's result object. **Flowing off the end** of a non-`void` function other than `main` is **undefined behavior**; flowing off a constructor/destructor/`void` function is `return;`. Sequencing: result initialization, then destruction of temporaries of the return full-expression, then destruction of the block's locals.
- `goto` targets a label in the same function.

## Declaration statement (`[stmt.dcl]`)

- Automatic variables are initialized each time the declaration is executed.
- **Jumping into a block** past a declaration with initialization is ill-formed unless the bypassed variable has scalar type, class type with trivial default constructor and destructor (or cv-version or array thereof) and no initializer.
- **Block-scope static/thread variables:** dynamically initialized the first time control passes the declaration; if initialization throws, it is retried next time; concurrent entry waits for completion; **recursive re-entry during initialization is undefined behavior**. The destructor runs iff the variable was constructed.

## Ambiguity (`[stmt.ambig]`)

An expression-statement starting with a function-style cast that could also be a declaration (first declarator beginning with `(`) is treated as a **declaration** (the "most vexing parse"); disambiguation is purely syntactic and precedes parsing.

## Labels and expression statements

Labels have function scope and their own name space (`[stmt.label]`). An expression statement evaluates a discarded-value expression and completes all side effects before the next statement (`[stmt.expr]`). A compound statement defines a block scope.

## Related

[[cpp17-expressions]] · [[name-lookup]] · [[storage-duration-and-object-lifetime]] · [[program-startup-and-termination]] · [[cpp17-templates]] · [[grammar-expressions-and-statements]] (Annex A.5)
