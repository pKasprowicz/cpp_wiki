---
type: concept
title: "Phases of translation"
tags: [cpp17, language-core, cross-cutting]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Phases of translation (`[lex.phases]`)

C++17 specifies the **precedence among syntax rules** as nine ordered phases. A source file plus everything it includes (minus lines skipped by conditional inclusion) is a **translation unit** (`[lex.separate]`). Part of [[cpp17-lexical-conventions]].

| Phase | What happens |
|---|---|
| 1 | Physical source characters are mapped (implementation-defined) to the basic source character set; characters outside it become universal-character-names. Extended characters and their `\uXXXX` forms must be handled equivalently, except where the replacement is reverted in a raw string literal. |
| 2 | Backslash-newline pairs are deleted, splicing physical lines into logical lines (only the last backslash on a line can take part in a splice). A splice that creates something matching a universal-character-name is **undefined behavior** (unless reverted in a raw string). A non-empty file not ending in a newline (or ending in backslash-newline) is processed as if a newline were appended. |
| 3 | The file is decomposed into preprocessing tokens and white space. Each comment becomes one space; newlines are kept; whether other white-space runs are kept or collapsed is unspecified. Decomposition is context-dependent. A file must not end in a partial token or comment. |
| 4 | Preprocessing directives run, macros expand, `_Pragma` operators execute. A universal-character-name produced by token concatenation is undefined behavior. `#include` recursively processes the named file through phases 1-4. Directives are then deleted. |
| 5 | Characters and escape sequences in character and (non-raw) string literals are converted to the execution character set; with no corresponding member, an implementation-defined member other than the null character is used. |
| 6 | Adjacent string-literal tokens are concatenated (rules in [[literals]]). |
| 7 | White space stops being significant; preprocessing tokens become tokens; the tokens are syntactically and semantically analyzed and translated as a translation unit. |
| 8 | Each translated translation unit is examined for required template instantiations; template definitions are located (whether the other units' *source* must be available is implementation-defined); all required instantiations form instantiation units. The program is ill-formed if any instantiation fails. |
| 9 | External references are resolved, library components linked, and a program image is produced. |

## Notes on this edition

- There is no phase for trigraph replacement in this text; Annex C.4 (`[diff.cpp14.lex]`) records the removal of trigraph support as a required feature, noting implementations may still translate trigraphs outside raw strings as part of the implementation-defined phase 1 mapping. See [[cpp17-compatibility-differences]].
- Template instantiation is specified as a separate step (phase 8) after analysis of each translation unit and before linking; see [[cpp17-templates]] and [[one-definition-rule]] for the rules on multiple definitions across translation units.

## Related

[[cpp17-preprocessing-directives]] (phase 4 in detail) · [[literals]] · [[cpp17-lexical-conventions]]
