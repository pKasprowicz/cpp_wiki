---
type: concept
title: "C++17 clauses 1-3: scope, normative references and glossary"
tags: [cpp17, standard-clause, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clauses 1-3: scope, normative references, terms and definitions (`[intro.scope]`, `[intro.refs]`, `[intro.defs]`)

The three front clauses of the draft are short (about 900 words together). They fix what the document is about, which outside documents it depends on, and a handful of defined terms used everywhere. This page is both the clause overview and the **glossary**: a lookup table from each defined term to its meaning and to the wiki page where the idea has real content. Sibling front-matter coverage (clause 4) is [[cpp17-general-principles]]; library-only vocabulary is at the end of this page.

## Section map

| Clause | Label | Content | Where |
|---|---|---|---|
| 1 Scope | `[intro.scope]` | the document is a set of requirements on implementations; C++ is based on C | below |
| 2 Normative references | `[intro.refs]` | nine external documents, four with shorthand names | below |
| 3 Terms and definitions | `[intro.defs]` | 29 numbered entries covering 18 headwords | tables below |

## Scope (`[intro.scope]`)

- `[intro.scope]/1`: the document states requirements for *implementations* of C++. The first requirement is that an implementation implement the language, so the document also defines C++; other requirements, and relaxations of that first one, appear in many places. (The program-side phrasing of those requirements is on [[abstract-machine-and-observable-behavior]], `[intro.compliance]`.)
- `[intro.scope]/2`: C++ is described as a general-purpose language based on C as specified in ISO/IEC 9899:2011 ("the C standard"). On top of C it adds further data types, classes, templates, exceptions, namespaces, operator overloading, function-name overloading, references, free-store management operators and additional library facilities.

## Normative references (`[intro.refs]`)

Dated references mean exactly that edition; an undated reference means the latest edition with amendments (`[intro.refs]/1`). Only ISO/IEC 2382 is cited without a year.

| Item | Document | Shorthand in the text | Where this wiki touches it |
|---|---|---|---|
| 1.1 | ECMAScript language specification, Ecma-262, 3rd edition (1999) | "ECMA-262" (`/4`) | the default regular-expression grammar and replace rules (`[re.grammar]`, `[re.synopt]`, `[re.matchflag]`): [[regex-classes-and-algorithms]] |
| 1.2 | ISO/IEC 2382 (all parts), IT vocabulary | — | clause 3 takes terms from ISO/IEC 2382-1:1993 (`[intro.defs]/1`) |
| 1.3 | ISO/IEC 9899:2011, the C programming language | "the C standard"; its Clause 7 library is "the C standard library" (`/2`) | all the `<cname>` and `name.h` headers: [[library-requirements-and-conformance]], [[cpp17-annex-d-compatibility-features]] |
| 1.4 | ISO/IEC 9899:2011/Cor.1:2012, Technical Corrigendum 1 to the above | — | — |
| 1.5 | ISO/IEC 9945:2003, POSIX | "POSIX" (`/3`) | `errno` and `errc` values: [[cpp17-lib-diagnostics]], [[error-codes-and-system-error]] |
| 1.6 | ISO/IEC 10646-1:1993, Universal Coded Character Set, Part 1 | — | universal-character-names (`[lex.charset]`), `__STDC_ISO_10646__` (`[cpp.predefined]`), the code-conversion facets of Annex D (`[depr.locale.stdcvt.req]`): [[cpp17-lexical-conventions]], [[cpp17-preprocessing-directives]], [[deprecated-library-facilities]] |
| 1.7 | ISO/IEC 10967-1:2012, language independent arithmetic, Part 1 | "LIA-1" (`/5`) | the shorthand is defined but a text search of the whole draft finds no other section that uses it |
| 1.8 | ISO/IEC/IEEE 60559:2011, floating-point arithmetic | — | `numeric_limits::is_iec559` (`[numeric.limits.members]`): [[numeric-limits]]; related floating-point environment: [[math-functions-and-fenv]] |
| 1.9 | ISO 80000-2:2009, mathematical signs and symbols | — | cited again only in `[intro.defs]/1` (terms, definitions and symbols are taken from it) |

The "where" column was built from a text search of the draft for each document's name or shorthand; for the C standard and POSIX it lists a few representative pages, not every use.

## Glossary: terms of clause 3

Clause 3 also says that ISO and IEC maintain terminology databases (Electropedia, the ISO browsing platform), that library-only terms are in `[definitions]` (see below) and that terms used in only a small part of the document are defined and italicized where they are used (`[intro.defs]/2-4`). The angle-bracketed tag before a definition in the standard (for example the "glvalue" or "function-like macro" qualifier) says in which context that sense applies; it is shown here as "(context)". Quoted notes are marked.

### Program properties and behavior classes

| Term | Meaning (paraphrased) | Label | Where it matters |
|---|---|---|---|
| well-formed program | a program built according to the syntax rules, the *diagnosable* semantic rules and the one-definition rule | `[defns.well.formed]` | [[abstract-machine-and-observable-behavior]], [[one-definition-rule]] |
| ill-formed program | a program that is not well-formed | `[defns.ill.formed]` | same; a violated rule marked "no diagnostic required" puts no requirement on the implementation (`[intro.compliance]/2.3`) |
| undefined behavior | behavior for which the standard imposes no requirements at all | `[defns.undefined]` | [[abstract-machine-and-observable-behavior]], [[strict-aliasing]], [[memory-model-and-data-races]] |
| unspecified behavior | for a well-formed construct and correct data, behavior that depends on the implementation, with no duty to document which one | `[defns.unspecified]` | [[abstract-machine-and-observable-behavior]], [[sequencing-and-evaluation-order]] |
| implementation-defined behavior | like unspecified, but each implementation must document its choice | `[defns.impl.defined]` | [[abstract-machine-and-observable-behavior]] |
| locale-specific behavior | behavior depending on local conventions of nationality, culture and language, which each implementation documents | `[defns.locale.specific]` | [[locale-class-and-facets]] |
| conditionally-supported | a construct an implementation need not support | `[defns.cond.supp]` | [[abstract-machine-and-observable-behavior]]; the language examples are in [[cpp17-declarations]] (language linkages) and [[cpp17-preprocessing-directives]] |
| diagnostic message | a message belonging to an implementation-defined subset of the implementation's output messages | `[defns.diagnostic]` | [[abstract-machine-and-observable-behavior]] |
| implementation limits | restrictions the implementation puts on programs | `[defns.impl.limits]` | [[implementation-quantities]] |

Notes that add information (not definitions): for *conditionally-supported*, each implementation documents the constructs it does not support. For *unspecified behavior*, the implementation need not document which behavior occurs, and the range of possibilities is usually bounded elsewhere in the standard. For *undefined behavior*, the note says it may be expected when the standard omits an explicit definition or a program uses an erroneous construct or erroneous data; the permitted range runs from ignoring the situation with unpredictable results, through behaving in a documented way characteristic of the environment (with or without a diagnostic), to stopping translation or execution with a diagnostic; many erroneous constructs are *not* undefined, they must be diagnosed; and evaluating a constant expression never has behavior the standard explicitly calls undefined (all `[defns.undefined]`, note). The last point connects to [[constant-expressions]].

### Expressions, types and calls

| Term | Meaning (paraphrased) | Label | Where it matters |
|---|---|---|---|
| access (execution-time action) | to read or modify the value of an object | `[defns.access]` | [[memory-model-and-data-races]], [[storage-duration-and-object-lifetime]] |
| static type | the type of an expression determined by analyzing the program without looking at execution; per a note it depends only on the form of the program and never changes while it runs | `[defns.static.type]` | [[cpp17-expressions]], [[value-categories]] |
| dynamic type (glvalue) | the type of the most derived object the glvalue refers to; per the note's example, a `B*` pointing at a `D` derived from `B` gives `*p` dynamic type `D` (references behave alike) | `[defns.dynamic.type]` | [[cpp17-derived-classes]], [[cast-expressions]], [[type-identification-rtti]] |
| dynamic type (prvalue) | simply the static type of the prvalue expression | `[defns.dynamic.type.prvalue]` | [[value-categories]] |
| multibyte character | a sequence of one or more bytes representing a member of the extended character set of the source or execution environment (the note adds that the extended set is a superset of the basic one) | `[defns.multibyte]` | [[cpp17-lexical-conventions]], [[translation-phases]] |

### Argument and parameter (each has several senses)

| Term (context) | Meaning (paraphrased) | Label | Where it matters |
|---|---|---|---|
| argument (function call) | an expression in the comma-separated list in the parentheses of a call | `[defns.argument]` | [[cpp17-expressions]], [[overload-resolution]] |
| argument (function-like macro) | a sequence of preprocessing tokens in the comma-separated list in the macro invocation's parentheses | `[defns.argument.macro]` | [[cpp17-preprocessing-directives]] |
| argument (throw) | the operand of `throw` | `[defns.argument.throw]` | [[cpp17-exception-handling]] |
| argument (template instantiation) | the constant-expression, type-id or id-expression in the angle-bracketed list | `[defns.argument.templ]` | [[cpp17-templates]] |
| parameter (function or catch clause) | an object or reference declared in a function declaration/definition or a handler's catch clause that receives a value on entry | `[defns.parameter]` | [[cpp17-declarators]], [[cpp17-exception-handling]] |
| parameter (function-like macro) | an identifier in the parenthesized list right after the macro name | `[defns.parameter.macro]` | [[cpp17-preprocessing-directives]] |
| parameter (template) | a member of a template-parameter-list | `[defns.parameter.templ]` | [[cpp17-templates]] |

### Signatures (six senses)

A *signature* is what distinguishes declarations from one another for overloading and linking. The six sense entries differ in what they include; "enclosing namespace (if any)" is part of the non-member ones, "class of which it is a member" part of the member ones.

| Entry | Components | Label |
|---|---|---|
| function | name, parameter-type-list, enclosing namespace | `[defns.signature]` |
| function template | name, parameter-type-list, enclosing namespace, **return type**, template parameter list | `[defns.signature.templ]` |
| function template specialization | the template's signature plus its template arguments, explicit or deduced | `[defns.signature.spec]` |
| class member function | name, parameter-type-list, class, cv-qualifiers (if any), ref-qualifier (if any) | `[defns.signature.member]` |
| class member function template | the member-function components plus return type (if any) and template parameter list | `[defns.signature.member.templ]` |
| class member function template specialization | the member template's signature plus its template arguments | `[defns.signature.member.spec]` |

Consequence worth remembering: the return type is part of the signature of a function *template* (and its members) but not of an ordinary function. A note on the plain entry says signatures are the basis for name mangling and linking. Detail pages: [[cpp17-overloading]], [[cpp17-templates]], [[linkage]].

### Threads

| Term | Meaning (paraphrased) | Label | Where it matters |
|---|---|---|---|
| block | a thread of execution *blocks* when it waits for some condition, other than the implementation merely executing its own steps, before it can continue past the blocking operation | `[defns.block]` | [[memory-model-and-data-races]] (forward progress), [[mutexes-and-locks]], [[condition-variable]] |
| unblock | to satisfy a condition that one or more blocked threads are waiting for | `[defns.unblock]` | same |

## Library-only vocabulary (`[definitions]`, 20.3)

`[intro.defs]/3` points here: the 25 entries of `[definitions]` are used only in clauses 20-33 and Annex D (a note in `[definitions]` points back at clause 3). They are summarized, with the surrounding reading rules, on [[library-requirements-and-conformance]]; a one-line reference follows.

| Term | Gist | Label |
|---|---|---|
| arbitrary-positional / repositional stream | can seek to any integral position within the stream / can seek to a previously seen position; the first kind is also the second | `[defns.arbitrary.stream]`, `[defns.repositional.stream]` |
| character, character container type | any object that represents text when treated sequentially, not just `char`-like types / the type used for it, the `charT` parameter of strings, iostreams and regex (a note says it is a POD type) | `[defns.character]`, `[defns.character.container]` |
| comparison function | an operator function for an equality or relational operator | `[defns.comparison]` |
| component | a group of library entities related as members, parameters or return types (e.g. `basic_string` plus its non-member operations) | `[defns.component]` |
| constant subexpression | an expression whose evaluation as a subexpression would not stop an enclosing conditional-expression from being a core constant expression | `[defns.const.subexpr]` |
| deadlock | threads cannot proceed because each is blocked waiting on the others | `[defns.deadlock]` |
| default behavior (implementation / specification) | what the implementation does within the required behavior / the description of replacement- and handler-function semantics | `[defns.default.behavior.impl]`, `[defns.default.behavior.func]` |
| direct-non-list-initialization | direct-initialization that is not list-initialization | `[defns.direct-non-list-init]` |
| handler function | a non-reserved function whose definition the program may supply and install through library calls | `[defns.handler]` |
| iostream class templates | the templates of clause 30 with the two parameters `charT` and `traits` | `[defns.iostream.templates]` |
| modifier function / observer function | a member function (not a constructor, assignment or destructor) that changes the object's state / reads it without changing it (observers are `const`) | `[defns.modifier]`, `[defns.observer]` |
| move assignment / move construction | assigning an rvalue of a type to a modifiable lvalue of that type / direct-initializing from an rvalue of the same type | `[defns.move.assign]`, `[defns.move.constr]` |
| NTCTS | the character values before the terminating `charT()` | `[defns.ntcts]` |
| referenceable type | an object type, a function type without cv- or ref-qualifier, or a reference type | `[defns.referenceable]` |
| replacement function | a non-reserved function whose definition the program provides; only one definition is in effect (note) | `[defns.replacement]` |
| required behavior | what any definition of a replacement/handler function must do; failing it is undefined behavior (note) | `[defns.required.behavior]` |
| reserved function | a library function the implementation must define; supplying a definition gives undefined results (note) | `[defns.reserved.function]` |
| stable algorithm | one that preserves the relative order of elements as appropriate to that algorithm | `[defns.stable]` |
| traits class | a class bundling types and functions that templates need to handle objects of the instantiating types | `[defns.traits]` |
| valid but unspecified state | an object value that is not specified except that the invariants hold and operations behave per the type's specification (example: a moved-from vector may be asked `empty()` at any time) | `[defns.valid]` |

See also [[library-named-requirements]] for the plain-identifier requirement names that build on these terms.

## Related

[[cpp17-general-principles]] · [[abstract-machine-and-observable-behavior]] · [[cpp17-lib-introduction]] · [[n4659-cpp17-draft-standard]] · [[cpp17-grammar-summary]]
