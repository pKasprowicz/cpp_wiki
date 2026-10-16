---
type: concept
title: "Fold expressions"
tags: [cpp17, language-core, cross-cutting, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Fold expressions (`[expr.prim.fold]`, `[temp.variadic]/9`)

A **fold expression** reduces a template parameter pack over a binary operator. It is a primary expression ([[cpp17-expressions]]) and one of the pack-expansion contexts of [[cpp17-templates]].

## Forms

| Form | Name | Instantiation (pack elements E1…EN) |
|---|---|---|
| `( ... op e )` | unary left fold | `((E1 op E2) op ⋯) op EN` |
| `( e op ... )` | unary right fold | `E1 op (⋯ op (EN−1 op EN))` |
| `( e1 op1 ... op2 e2 )` | binary fold | `op1`, `op2` must be the **same** operator; exactly one of `e1`/`e2` contains an unexpanded pack |
| ↳ pack on the right (`e2`) | binary left fold | `(((E op E1) op E2) op ⋯) op EN` |
| ↳ pack on the left (`e1`) | binary right fold | `E1 op (⋯ op (EN−1 op (EN op E)))` |

The pattern is the `cast-expression` containing the unexpanded pack; in a binary fold, `E` is the other `cast-expression`. The operand in a unary fold must contain an unexpanded parameter pack. The grammar requires parentheses around the whole fold.

## Operators allowed

`+ - * / % ^ & | << >> += -= *= /= %= ^= &= |= <<= >>= = == != < > <= >= && || , .* ->*`

## Empty packs

A **unary** fold over an empty pack (N = 0) has a defined value only for three operators (Table 14); any other operator makes the instantiation ill-formed:

| Operator | Value |
|---|---|
| `&&` | `true` |
| `\|\|` | `false` |
| `,` | `void()` |

Binary folds have no empty-pack problem since `E` is always present.

## Dependence

A fold expression is always **type-dependent** and **value-dependent** (`[temp.dep.expr]/7`, `[temp.dep.constexpr]/4`) — see [[dependent-names-and-instantiation]]. Sizes of packs are given by `sizeof...(pack)`.

## Related

[[cpp17-templates]] · [[cpp17-expressions]] · [[template-argument-deduction]]
