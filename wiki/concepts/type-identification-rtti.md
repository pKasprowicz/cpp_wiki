---
type: concept
title: "Type identification library: type_info, bad_cast, bad_typeid, type_index"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Type identification (`<typeinfo>`, `[support.rtti]`; `type_index` from `[type.index]`)

Parent: [[cpp17-lib-language-support]]. The expressions that use these types are `typeid` and `dynamic_cast` ([[cast-expressions]], [[cpp17-expressions]]).

- **`std::type_info`** (result of `typeid`) stores an unspecified name and encoding for comparing types. Names, encoding rule and collating order are unspecified and may differ between programs. Members: `==`/`!=` (same type), `before(rhs)` (collation order), `hash_code()` (unspecified, but equal for equal `type_info`s within one execution; should differ for unequal ones), `name()` (implementation-defined null-terminated string) (`[type.info]`).
- **`bad_cast`** is thrown by an invalid `dynamic_cast` to a reference type; **`bad_typeid`** reports a null pointer in a `typeid` expression (`[bad.cast]`, `[bad.typeid]`). Both derive from `exception` ([[exception-support]]); `what()` is implementation-defined.
- **`type_index`** (`<typeindex>`, `[type.index]`) is a thin wrapper holding a pointer to a `type_info` so the type can be an index in ordered and unordered associative containers. It is constructed from a `type_info&`; `==`, `!=`, `<`, `<=`, `>`, `>=` forward to `type_info`'s equality and `before`; `hash_code()` and `name()` forward too; and `hash<type_index>` agrees with `hash_code()`. See [[ordered-associative-containers]], [[unordered-containers]].

## Related

[[cpp17-lib-language-support]] · [[cast-expressions]] · [[cpp17-lib-utilities]]
