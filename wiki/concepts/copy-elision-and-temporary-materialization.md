---
type: concept
title: "Copy elision, prvalues and temporary materialization"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Copy elision, prvalue result objects and temporaries

Collects the rules from `[basic.lval]`, `[conv.rval]`, `[dcl.init]`, `[class.temporary]` and `[class.copy.elision]` that decide when a copy/move happens.

## Prvalues initialize their destination directly

- A **prvalue** is defined as an expression whose evaluation *initializes an object*; that object is its **result object** ([[value-categories]]). A prvalue used to compute an operand has no result object.
- When the initializer of a class-type object is a prvalue of the same class (cv-unqualified), "the initializer expression is used to initialize the destination object" — **no copy or move constructor is considered** (`[dcl.init]/17.6.1`; also reflected in `[stmt.return]` and argument passing since those are initializations). By the wording, `T x = T();`, `return T();` and passing `T()` as a by-value argument therefore construct the object in place (the initializations in `[stmt.return]/2` and `[expr.call]/4` follow the same rule), so the copy/move constructor is not even considered.
- A prvalue becomes an object only when something needs a glvalue: **temporary materialization conversion** (`[conv.rval]`): "A prvalue of type T can be converted to an xvalue of type T", initializing a temporary with the prvalue as its result object. It is applied for member access on a prvalue, reference binding, `sizeof`, `typeid`, array-to-pointer on a prvalue array, discarded-value prvalues, etc. ([[cpp17-standard-conversions]], [[cpp17-expressions]]).
- Constant expressions are evaluated "assuming copy elision is performed", and elision is **required** in constant expressions and constant initialization (`[class.copy.elision]/1`).

## Remaining permitted (optional) copy elision (`[class.copy.elision]/1`)

An implementation *may* omit a copy/move construction, even if it or the destructor has side effects, treating source and target as two names for one object, in these cases:

1. **Named return** (NRVO): `return name;` where `name` is a non-volatile automatic object (not a function parameter or exception-declaration variable) of the same type as the return type (ignoring cv).
2. **throw name;** where `name` is a non-volatile automatic object (not a function or catch parameter) whose scope ends within the innermost enclosing try-block.
3. **Exception-declaration alias:** a handler declaring an object of the same type as the exception object may alias it if the program's meaning is unchanged other than constructor/destructor execution.

If elided with an rvalue-reference-first-parameter constructor, destruction happens when the target would have been destroyed; otherwise at the later of the two destruction times. Multiple eliminations may combine.

**Move on return/throw (`/3`):** when the expression is a (possibly parenthesized) id-expression naming an automatic object declared in the enclosing function/lambda body or parameter list (return), or the throw operand, overload resolution first treats the object as an rvalue; if that fails, or the selected constructor's first parameter is not an rvalue reference to the object's type, overload resolution is repeated with an lvalue.

## Temporary objects (`[class.temporary]`)

- Created when a prvalue is materialized for use as a glvalue; when the implementation needs a temporary to pass/return a trivially-copyable class type (permitted if every copy/move constructor and destructor is trivial or deleted with at least one non-deleted copy/move constructor — the parameter/result is then initialized as if copying that temporary using the trivial constructor, even if inaccessible); and when throwing an exception. Even unevaluated creations must satisfy the semantic restrictions (constructor/destructor access, etc.).
- Materialization is delayed as long as possible.
- **Destruction:** the last step of the full-expression that lexically contains their creation, even if it ends by exception; in reverse order of construction for those not lifetime-extended.
- **Three exceptions to "end of full-expression":**
  1. default constructor called for array elements lacking an initializer, and 2. copy constructor called for array elements while copying the array: destruction of temporaries in default arguments is sequenced before constructing the next element;
  3. **a reference bound to a temporary**: the temporary (or the complete object containing the bound subobject) lives as long as the reference — except: a temporary bound to a reference **parameter** lasts until the end of the full-expression containing the call; a temporary bound to the *returned value* in a `return` is not extended; one bound in a `new-initializer` lasts until the end of the full-expression containing the new-initializer.
- Temporaries bound to references must also respect destruction ordering relative to other objects of the same storage duration (created before ⇒ destroyed after; created after ⇒ destroyed before).

## Related

[[initialization]] · [[cpp17-special-member-functions]] · [[value-categories]] · [[storage-duration-and-object-lifetime]] · [[cpp17-statements]] (`return`)
