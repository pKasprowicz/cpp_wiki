---
type: concept
title: "Sequencing and evaluation order"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Sequencing and evaluation order

Single-thread ordering in C++17 is defined by the **sequenced-before** relation in `[intro.execution]`. Cross-thread ordering is in [[memory-model-and-data-races]].

## Vocabulary (`[intro.execution]/9–14`)

- **Full-expression:** an unevaluated operand, a constant-expression, an init-declarator or mem-initializer (including the initializer's constituents), a destructor call generated at end of an object's lifetime (other than a temporary), or an expression that is not a subexpression of another expression and not otherwise part of a full-expression. Implicit conversions applied to satisfy the surrounding construct, and the initialization of an entity, are part of it.
- **Side effects:** reading a volatile glvalue, modifying an object, calling a library I/O function, or calling a function that does any of these.
- **Evaluation of an expression** = *value computations* (determining object identity for glvalues, fetching values for prvalues) plus *initiation of side effects*.

## The relation (`/15`)

*Sequenced before* is asymmetric, transitive and pair-wise, between evaluations in a single thread, inducing a partial order. If A is sequenced before B, A's execution precedes B's. If neither is sequenced before the other they are **unsequenced**; if one precedes the other but it is unspecified which, they are **indeterminately sequenced**.

## Core rules

1. Every value computation and side effect of a full-expression is sequenced before those of the next full-expression (`/16`).
2. Unless noted otherwise, operands of individual operators and subexpressions are **unsequenced**; but the value computations of an operator's operands are sequenced before the value computation of the operator's result (`/17`).
3. A side effect on a memory location that is **unsequenced** relative to another side effect on the same location, or to a value computation using that location's value, is **undefined behavior** when the two are not potentially concurrent (`/17`). Potentially concurrent actions are those on different threads, or unsequenced ones where at least one runs in a signal handler (`[intro.races]/20`).
4. Function calls: all argument evaluations and the evaluation of the postfix expression designating the callee are sequenced before every expression/statement in the callee body. Every evaluation inside a function invocation is either sequenced before or after any evaluation outside it on the same thread (and signal handler) — function bodies are *indeterminately sequenced* with respect to surrounding unsequenced evaluations, never interleaved (`/18`).
5. Language constructs that implicitly call a function are treated as expressions for these purposes (`/12`, `/18`).
6. A signal handler run via `std::raise` is sequenced after the `raise` invocation and before its return (`/19`).

## Per-operator exceptions ("except where noted")

Operator-specific ordering rules in `[expr]` ([[cpp17-expressions]]):

| Construct | Rule | Section |
|---|---|---|
| `E1[E2]` | E1 sequenced before E2 | `[expr.sub]/1` |
| function call | the postfix-expression is sequenced before each argument expression and default argument; each parameter's initialization (all its value computations and side effects) is **indeterminately sequenced** with respect to every other parameter's | `[expr.call]/5` |
| `E1 << E2`, `E1 >> E2` | E1 sequenced before E2 | `[expr.shift]/4` |
| `E1 .* E2`, `E1 ->* E2` | E1 sequenced before E2 | `[expr.mptr.oper]/4` |
| `&&`, `\|\|` | if the second operand is evaluated, everything in the first is sequenced before it; the second is skipped when the first decides the result | `[expr.log.and]`, `[expr.log.or]` |
| `?:` | the first operand's evaluation is sequenced before the second or third; only one of those is evaluated | `[expr.cond]/1` |
| `,` | left operand (a discarded-value expression) sequenced before the right | `[expr.comma]/1` |
| `=` and `op=` | the **right operand is sequenced before the left**; the assignment itself is sequenced after both operands' value computations and before the value computation of the assignment expression; a compound assignment is a single evaluation with respect to an indeterminately-sequenced function call | `[expr.ass]/1` |
| postfix `++` / `--` | the value computation is sequenced before the modification; a single evaluation with respect to an indeterminately-sequenced function call | `[expr.post.incr]/1` |
| `new` | allocation function call sequenced before the evaluations in the new-initializer; initialization sequenced before the value computation of the new-expression | `[expr.new]/19` |

**Overloaded operators:** when an operator expression is rewritten as a call to a user-defined operator function, "the operands are sequenced in the order prescribed for the built-in operator" (`[over.match.oper]/2`), so the table above also governs overloaded `<<`, `>>`, `=`, `&&`-style forms ([[overload-resolution]]).

Everything else (for example the operands of `+`, `*`, `==`, or two arguments of a call against side effects on the same object) remains unsequenced or indeterminately sequenced per the core rules above, so unsequenced conflicting side effects are still undefined behavior.

## Related

[[abstract-machine-and-observable-behavior]] · [[cpp17-general-principles]]
