---
type: concept
title: "C++ versus ISO C: Annex C.1 differences"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-16
updated: 2026-10-16
---

# C++ versus ISO C (Annex C.1, `[diff.iso]`)

Annex C is informative. Its first subclause, C.1, walks through the language clauses in order and records, for 33 entries, how an ISO C program behaves differently (or stops being valid) when read as C++. Every entry in the draft is a fixed form: the change, the rationale, the effect on the original feature, how hard conversion is, and how widely used the C construct is. The tables below keep the change, the rationale in a few words, and the conversion/frequency verdicts (the annex's own words "common", "seldom", "rare" are quoted as labels). The library side of the same comparison (C headers, `NULL`, `offsetof`, `malloc`) is Annex C.5, summarized on [[library-requirements-and-conformance]]. Sibling Annex C pages: [[cpp17-compatibility-differences]] (C++11/C++14 and the Annex C map) and [[cpp03-differences]].

## How to read the effect labels

The annex classifies each entry by its *effect on the original feature*:

- **deleted** (20 entries): a C construct with well-defined meaning is rejected by C++.
- **changed** (11 entries): a C construct stays legal but means something else, or names (keywords, scopes) are treated differently.
- **other** (2 entries): decrement on `bool` (just stated to be ill-formed) and plain-`int` bit-fields (an implementation-defined choice in C is fixed in C++).

Where the same program text compiles in both languages and gives a different answer, the annex's own examples are all `sizeof`-based: a character literal, a comma expression whose right operand is an array, an enumerator, and a struct tag that hides an array of the same name. The annex gives no other example of silently different behavior: most remaining entries are constructs a C++ translator rejects, except a few definitional ones (`__STDC__`, bit-field signedness, `const` linkage) where the annex does not say whether a diagnostic arises.

The annex rates these as **common** in C code: new keywords used as identifiers, "compatible types" (`[basic.types]`), implicit function declarations, `register`, implicit `int`, assigning integers to enumeration objects, empty parameter lists, and old-style function definitions. `void*` to object-pointer assignment is described as "fairly widely used", and code that references `__STDC__` as "quite common".

## C.1.1 Lexical conventions (`[diff.lex]`) — [[cpp17-lexical-conventions]], [[literals]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[lex.key]` | C++ reserves keywords C does not (the keyword table of `[lex.key]`); a C program using them as identifiers is invalid C++ | Needed for C++ semantics. Renaming is a syntactic transformation; easy for one program, more work for a family of programs. Common |
| `[lex.ccon]` | A character literal has type `char`; in C it has type `int`. A program that relies on `sizeof('x') == sizeof(int)` behaves differently | Lets overloads on `int` and `char` pick the char version for a char literal. Simple to convert. Rare |
| `[lex.string]` | String literals have `const`-qualified array types (narrow, `char16_t`, `char32_t` and wide variants); in C the element type is plain | Avoids calling an overload that expects to modify its argument. Fix: add a cast. Programs that really treat literals as modifiable are rare |

## C.1.2 Basic concepts (`[diff.basic]`) — [[cpp17-basic-concepts]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[basic.def]` | No tentative definitions: two file-scope definitions of the same variable are an error. Consequence: mutually referential file-local static objects cannot be set up with C-style constant initializers; one initializer must call a function. See [[one-definition-rule]] | One initialization rule for fundamental and class types. Semantic transformation. Seldom |
| `[basic.scope]` | A struct is a scope in C++, not in C; names of nested struct, enumeration or enumerators used outside the struct are affected. See [[name-lookup]] | Class scope is central to C++. Semantic transformation. Struct use is frequent but the change shows only when those names are used outside the struct, probably rare |
| `[basic.link]` (also `[dcl.type]`) | A file-scope name declared `const` and not `extern` has internal linkage; in C it has external linkage. See [[linkage]] | Const objects can serve as translation-time values, so programmers should supply initializers; allows const objects in headers shared by several translation units. Semantic transformation. Seldom |
| `[basic.start.main]` | `main` cannot be called recursively and its address cannot be taken. See [[program-startup-and-termination]] | `main` may need special actions. Fix: a wrapper function with another name. Seldom |
| `[basic.types]` | C accepts "compatible types" (for example struct types that differ only in tag name); in C++ they are different types | C++ needs tighter type checking. Semantic transformation. Type-safe linkage catches many but not all; the rest keeps working through the layout-compatibility rules. Common |

## C.1.3 Standard conversions (`[diff.conv]`) — [[cpp17-standard-conversions]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[conv.ptr]` | Converting `void*` to an object pointer type needs a cast | Compile-time type safety. Can be automated; the translator diagnoses every case. Fairly widely used in C, although many C compilers warn without the cast |

## C.1.4 Expressions (`[diff.expr]`) — [[cpp17-expressions]], [[cast-expressions]], [[value-categories]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[expr.call]` | No implicit declaration of functions (obsolescent in C) | Fits the C++ emphasis on type safety. Syntactic transformation; declaration-generating tools are widely available. Common |
| `[expr.post.incr]`, `[expr.pre.incr]` | Decrement on a `bool` operand is ill-formed (a C program can reach this via the C `bool` typedef of `<stdbool.h>`) | The feature behaves in surprising ways. The entry gives no conversion or frequency verdict. The draft's C.4 separately records removal of *increment* on `bool`: see [[cpp17-compatibility-differences]] |
| `[expr.sizeof]`, `[expr.cast]` | A `sizeof` or cast expression cannot define a new type | Makes the place of definitions clear. Syntactic transformation. Seldom |
| `[expr.cond]`, `[expr.ass]`, `[expr.comma]` | The result of a conditional, assignment or comma expression may be an lvalue; code depending on the implied lvalue-to-rvalue conversion changes. `sizeof` of a comma expression ending in an array gives the array size in C++, the pointer size in C | C++ emphasizes lvalues (functions may return them). Fix: cast to the intended rvalue. Rare |

## C.1.5 Statements (`[diff.stat]`) — [[cpp17-statements]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[stmt.switch]`, `[stmt.goto]` | Jumping past a declaration with an explicit or implicit initializer is invalid (except over a whole block that is never entered) | Constructors in initializers may acquire resources; the compile-time rule guarantees that a variable in scope was initialized. Semantic transformation. Seldom |
| `[stmt.return]` | It is invalid to return from a value-returning function without a value, explicitly or implicitly | Class-object return mechanisms would get complicated if some paths gave no value. Fix: return something such as zero. Seldom; many C implementations already warn. The normative text (`[stmt.return]/2`) is narrower: an operand-less `return` in such a function is ill-formed, and flowing off the end is undefined behavior (except in `main`) |

## C.1.6 Declarations (`[diff.dcl]`) — [[cpp17-declarations]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[dcl.stc]` (first) | `static` and `extern` apply only to objects and functions; on a type declaration they are illegal in C++ (ignored in C) | They mean nothing for types, and class members may be `static`, so allowing them would confuse. Syntactic transformation. Seldom |
| `[dcl.stc]` (second) | `register` is not a storage-class specifier in C++ | It had no effect there. Syntactic transformation. Common. The draft's C.4 records the removal of `register` between C++14 and this draft (see [[cpp17-compatibility-differences]]) |
| `[dcl.typedef]` | A typedef name must differ from a class name declared in the same scope (unless the typedef names that same class); in C the two live in different name spaces | C++ lets a class name be used without `class`/`struct`/`union`. One of the two names must be renamed. Semantic transformation. Seldom |
| `[dcl.type]` (see also `[basic.link]`) | `const` objects must be initialized | A const object can't be assigned later. Semantic transformation. Seldom |
| `[dcl.type]` (implicit int) | A decl-specifier-seq must contain a type-specifier unless a declarator for a constructor, destructor or conversion function follows; implicit `int` is gone | Implicit `int` makes declarations ambiguous with function-like casts; the rationale mentions WG14 support for deprecating it in the next C revision. Syntactic, could be automated. Common |
| `[dcl.spec.auto]` | `auto` cannot be a storage-class specifier | Type deduction from the initializer would make the old reading ambiguous in some contexts. Syntactic. Rare |
| `[dcl.enum]` (assignment) | An object of enumeration type accepts only values of that enumeration type; C allows any integral value | Type safety. Fix: explicit cast (automatable). Common |
| `[dcl.enum]` (enumerator type) | The type of an enumerator is its enumeration; in C it is `int`. `sizeof` of an enumerator can differ | An enumeration is a distinct type in C++. Semantic transformation. Seldom; taking the size of an enumerator is uncommon in C |

## C.1.7 Declarators (`[diff.decl]`) — [[cpp17-declarators]], [[initialization]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[dcl.fct]` (empty list) | A function declared with an empty parameter list takes no arguments; in C it means the parameters are unspecified (obsolescent there) | Avoids calls with wrong argument counts/types. Syntactic transformation, but different calls with different argument lists may require more work. Common |
| `[dcl.fct]` (see `[expr.sizeof]`) | Types may not be defined in return or parameter types | C++ compares types by name across translation units; a type defined in a parameter list is scoped to the function. Move the definition to file scope or a header. Semantic transformation. Seldom, seen as poor style |
| `[dcl.fct.def]` | Old-style (K&R) function definitions are not part of the syntax | Type safety depends on prototypes. Syntactic transformation. Common in old programs, known to be obsolescent |
| `[dcl.init.string]` | Initializing a character array with a string literal requires the array to hold the terminating null; C allows a literal that fits only without it | Unterminated arrays are dangerous with string functions. Fix: make the array one element bigger. Seldom, poor style |

## C.1.8 Classes (`[diff.class]`) — [[cpp17-classes]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[class.name]` (see also `[dcl.typedef]`) | A class declaration brings its name into the scope and hides any object, function or other declaration of that name from an enclosing scope; in C a struct tag never hides such a name | This is one of the few incompatibilities that come from the C++ name-space design, which the committee judged worth the cost. Hidden global: use `::`. Hidden block-scope name: rename. Semantic transformation. Seldom |
| `[class.bit]` | Bit-fields of plain `int` are signed | The implementation-defined choice would lead to inconsistent template specializations, so the freedom was removed for non-dependent types too. Syntactic. Seldom |
| `[class.nest]` | A nested class name is local to the enclosing class; in C it is in the scope of the outermost enclosing struct | Classes with member functions must be scopes. Fix: declare the struct tag in the enclosing scope first, or export the nested definitions. The annex notes this follows from the scope difference in `[basic.scope]`. Seldom |
| `[class.nested.type]` | A typedef name cannot be redeclared in a class after being used in that class | Avoids confusion about what the name means. Rename the type or the member. Seldom |

## C.1.9 Special member functions (`[diff.special]`) — [[cpp17-special-member-functions]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[class.copy]` | The implicitly-declared copy constructor and copy assignment cannot copy a `volatile` lvalue | Taking `volatile const X&` would greatly complicate efficient code for class objects, and offering two signatures raised unanswered ambiguity concerns. Fix: a user-declared copy with the wanted volatile semantics, or a `const_cast` for non-volatile semantics. Seldom |

## C.1.10 Preprocessing directives (`[diff.cpp]`) — [[cpp17-preprocessing-directives]]

| Entry | C++ versus C | Why / fix / use in C |
|---|---|---|
| `[cpp.predefined]` | Whether `__STDC__` is defined, and with which value, is implementation-defined | C++ is not identical to ISO C, so mandating the macro would be a false claim; each implementation chooses what suits its market. Semantic transformation. Programs and headers testing it are quite common |

## Open points

- Annex C.1 says "ISO C" without an edition. The normative reference in `[intro.refs]` is ISO/IEC 9899:2011 ([[cpp17-glossary]]), but some rationale text (implicit `int` "in the next revision of C", empty parameter lists "obsolescent") reads as written against an older C. This source cannot say which entries still hold against C11.
- The decrement-on-`bool` entry is the only one without conversion and frequency verdicts.
- Whether `[stmt.return]` as summarized in C.1 ("invalid") is meant to cover undefined behavior from falling off the end is not stated; the page above gives the normative wording of `[stmt.return]/2`.

## Related

[[cpp17-compatibility-differences]] · [[cpp03-differences]] · [[n4659-cpp17-draft-standard]] · [[cpp17-annex-d-compatibility-features]] · [[library-requirements-and-conformance]] (C library differences, Annex C.5)
