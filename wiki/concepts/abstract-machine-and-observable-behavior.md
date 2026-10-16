---
type: concept
title: "Abstract machine and observable behavior"
tags: [cpp17, language-core, cross-cutting, undefined-behavior]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Abstract machine and observable behavior

The C++17 standard does not describe compilers directly. It describes a **parameterized nondeterministic abstract machine** and requires a conforming implementation to reproduce only the *observable behavior* of that machine (`[intro.execution]/1`). Implementations need not copy its structure. Part of [[cpp17-general-principles]].

## Three kinds of "not fully specified"

| Term | Meaning in the standard | Consequence |
|---|---|---|
| implementation-defined | an aspect that is a *parameter* of the machine, e.g. `sizeof(int)` | the implementation must document its choice (`/2`) |
| unspecified | the standard gives a *set of allowed behaviors* | one program/input can have several valid executions (`/3`) |
| undefined | no requirements at all, e.g. modifying a const object | see below (`/4`, `/5`) |

## Conformance rule (`/5`)

A conforming implementation running a well-formed program must produce the same observable behavior as **one** of the possible executions of the corresponding abstract-machine instance. If any such execution contains an undefined operation, the standard places **no requirement** on that program/input, "not even with regard to operations preceding the first undefined operation".

## What counts as observable (`/7`)

- accesses through `volatile` glvalues, evaluated strictly per abstract-machine rules;
- data written to files at program termination must equal one of the abstract machine's possible results;
- prompt output to interactive devices must be delivered before the program waits for input (what is "interactive" is implementation-defined).

## Rules about programs vs. implementations (`[intro.compliance]`)

- The **diagnosable rules** are all rules except those marked "no diagnostic required" or described as undefined behavior (`/1`).
- Well-formed program: the implementation must accept and correctly execute it within resource limits. Violating a diagnosable rule (or using an unsupported *conditionally-supported* construct): at least one diagnostic is required. Violating a no-diagnostic-required rule: no requirements (`/2`).
- Extensions are allowed if they do not change the behavior of well-formed programs; an ill-formed program using one must still be diagnosed, after which the implementation may compile and run it (`/8`).
- Two kinds of implementation: **hosted** (the standard defines the available libraries) and **freestanding** (may run without an OS; implementation-defined library set that includes certain language-support libraries) (`/7`).
- Implementations must document unsupported conditionally-supported constructs and locale-specific characteristics (`/9`).

## Forward progress assumption (`[intro.progress]/1`)

The implementation may assume every thread will eventually do one of: terminate, call a library I/O function, access a volatile glvalue, or perform a synchronization/atomic operation. The full progress-guarantee tiers are in [[memory-model-and-data-races]].

## Automatic objects (`[intro.execution]/6`)

Each entry into a block gets its own instance of every automatic-storage object; it exists and keeps its last stored value while the block runs and while it is suspended (by a call or a signal). See [[storage-duration-and-object-lifetime]].

## Related

- Evaluation order and the sequenced-before relation: [[sequencing-and-evaluation-order]].
- Defined terms (well-formed, undefined, unspecified, implementation-defined, conditionally-supported, ...): [[cpp17-glossary]]; recommended capacity limits: [[implementation-quantities]].
- Where undefined behavior is triggered by lifetime, ODR, or data-race violations: [[storage-duration-and-object-lifetime]], [[one-definition-rule]], [[memory-model-and-data-races]].
