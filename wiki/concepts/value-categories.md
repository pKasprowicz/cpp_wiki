---
type: concept
title: "Value categories (lvalue, xvalue, prvalue)"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Value categories (`[basic.lval]`)

Every expression has exactly one **value category**: lvalue, xvalue, or prvalue. Part of [[cpp17-basic-concepts]].

```
expression
├── glvalue ── lvalue
│          └── xvalue
└── rvalue ─── xvalue
           └── prvalue
```

| Category | Definition (paraphrased) |
|---|---|
| glvalue | evaluation determines the identity of an object, bit-field, or function |
| prvalue | evaluation initializes an object or bit-field, or computes the value of an operator's operand, as the context specifies |
| xvalue | a glvalue denoting an object or bit-field whose resources can be reused (usually near end of lifetime) |
| lvalue | a glvalue that is not an xvalue |
| rvalue | a prvalue or an xvalue |

## Results (`/2`)

- The **result** of a prvalue is the value it stores into its context; its **result object** is the object it initializes. A prvalue used to compute an operand, or of type `cv void`, has no result object. This result-object model is what lets a prvalue initialize its destination directly instead of being copied: see [[copy-elision-and-temporary-materialization]].
- The **result** of a glvalue is the entity it denotes.

## Rules

- A prvalue has complete type or `void` (unless otherwise indicated, `[expr.call]`); a glvalue never has type `cv void` (`/6`).
- An lvalue is **modifiable** unless its type is const-qualified or a function type (`/7`).
- Access through glvalues of the wrong type is undefined: [[strict-aliasing]] (`/8`).
- How categories behave in other contexts is discussed with reference initialization (`[dcl.init.ref]`) and temporaries (`[class.temporary]`).

## Related

[[strict-aliasing]] · [[copy-elision-and-temporary-materialization]] · [[cpp17-expressions]] · [[cpp17-standard-conversions]]
