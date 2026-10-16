---
type: concept
title: "C++17 clause 16: overloading"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 16: Overloading (`[over]`)

About 10,500 words; 34 labelled sections. Only functions and function templates can be overloaded.

## Section map

| Section | Label | Where summarized |
|---|---|---|
| 16.1 Overloadable declarations | `[over.load]` | below |
| 16.2 Declaration matching | `[over.dcl]` | below |
| 16.3 Overload resolution | `[over.match]` and subsections | [[overload-resolution]] |
| 16.4 Address of overloaded function | `[over.over]` | [[overload-resolution]] |
| 16.5 Overloaded operators | `[over.oper]` (unary, binary, assignment, call, subscript, member access, inc/dec, literal) | below |
| 16.6 Built-in operators | `[over.built]` | below |

## Overloadable declarations (`[over.load]`)

Declarations that **cannot** be overloaded (same-scope pair is ill-formed):

- functions differing only in return type and/or exception specification;
- member functions with the same name and parameter-type-list where any is `static` (the implicit object parameter is not compared); likewise member function templates with equal template parameter lists;
- member functions with identical names and parameter-type-lists where some, but not all, have a ref-qualifier.

Equivalences when comparing parameter-type-lists: array vs. pointer (only outer array dimension adjusts), function type vs. pointer to function, top-level `const`/`volatile` ignored (nested ones are significant — `T*`, `const T*`, `volatile T*` are distinct, as are the reference forms), and differing default arguments don't matter. Distinct enumerations are distinct types and can distinguish overloads.

## Declaration matching (`[over.dcl]`)

Two declarations refer to the same function if they are in the same scope with equivalent parameters. A derived-class member is not in the same scope as a same-named base member; a locally declared function is not in the same scope as one in an enclosing scope. Different overloads of a member function may have different access.

## Overloaded operators (`[over.oper]`)

- Overloadable: `new delete new[] delete[] + - * / % ^ & | ~ ! = < > += -= *= /= %= ^= &= |= <<= >>= << >> == != <= >= && || ++ -- , ->* -> () []` (unary and binary forms of `+ - * &` both). **Not overloadable:** `.`, `.*`, `::`, `?:`, `#`, `##`.
- An operator function is a non-static member or a non-member with at least one class/enumeration (or reference thereto) parameter. Precedence, grouping and operand count cannot change; `=`, unary `&` and `,` have predefined meanings that user types may override. Built-in identities (`++a` ≡ `a+=1`) need not hold, and lvalue requirements don't apply. Operator functions cannot have default arguments (except `operator()`) and are inherited like other base functions.
- **Specific rules:** unary: member with 0 params or non-member with 1; binary: member with 1 or non-member with 2; assignment: non-static member with exactly one parameter (can be virtual); `operator()`: non-static member, any number of parameters, may have defaults; `operator[]`: non-static member with exactly one parameter; `operator->`: non-static, no parameters, and `->` is applied again to the returned value; `++`/`--` postfix: an extra `int` parameter (argument value 0).
- **Literal operators** (`[over.literal]`): `operator "" _suffix`; declared at namespace scope (or friend / explicit specialization / using-declaration); parameter lists restricted to `const char*`, `unsigned long long`, `long double`, `char`, `wchar_t`, `char16_t`, `char32_t`, or `(const charN_t*, std::size_t)`; no default arguments; a literal operator *template* has an empty parameter list and a single `char...` non-type pack; no C language linkage; some suffix identifiers are reserved for future standardization (declaring one is ill-formed, no diagnostic required; the list is in the library clauses, `[usrlit.suffix]`). The call forms are in [[literals]].

## Built-in operator candidates (`[over.built]`)

Lists, for each operator and promoted arithmetic/integral/pointer/enumeration/pointer-to-member type, the fictional `operator@` signatures that take part in operator overload resolution — e.g. `LR operator*(L, R)` for promoted arithmetic `L`, `R` with `LR` the usual-arithmetic-conversion result; `T* operator+(T*, std::ptrdiff_t)`; `bool operator<(T, T)` for enumeration and pointer `T`; `bool operator==(T, T)` for pointer-to-member and `std::nullptr_t`; integral-only `% & ^ | << >>`; `vq L& operator=(vq L&, R)` etc.; `bool operator!(bool)`, `&&`, `||`; and `operator?:(bool, T, T)` for pointer, member-pointer and scoped-enumeration `T`. They are used for no purpose other than overload resolution ([[overload-resolution]]).

## Related

[[overload-resolution]] · [[cpp17-expressions]] · [[cpp17-declarators]] · [[cpp17-templates]] · [[grammar-declarations-and-classes]] (Annex A.11)
