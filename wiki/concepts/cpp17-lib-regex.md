---
type: concept
title: "C++17 clause 31: regular expressions library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 31: Regular expressions library (`[re]`)

About 12,300 words; 48 labelled sections. Pattern matching and searching over character sequences. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Content | Wiki page |
|---|---|---|---|
| 31.2 Definitions | `[re.def]` | collating element, matched, sub-expression, primary equivalence class | [[regex-classes-and-algorithms]] |
| 31.3 Requirements | `[re.req]` | regex traits class | [[regex-classes-and-algorithms]] |
| 31.4 `<regex>` synopsis | `[re.syn]` | declarations and the typedef family | — |
| 31.5 `regex_constants` | `[re.const]` | `syntax_option_type`, `match_flag_type`, `error_type` | [[regex-classes-and-algorithms]] |
| 31.6 `regex_error` | `[re.badexp]` | the exception class | [[regex-classes-and-algorithms]] |
| 31.7 `regex_traits` | `[re.traits]` | traits for `char` and `wchar_t` | [[regex-classes-and-algorithms]] |
| 31.8 `basic_regex` | `[re.regex]` | compiled pattern | [[regex-classes-and-algorithms]] |
| 31.9-31.10 `sub_match`, `match_results` | `[re.submatch]` `[re.results]` | match results | [[regex-classes-and-algorithms]] |
| 31.11 Algorithms | `[re.alg]` | `regex_match`, `regex_search`, `regex_replace` | [[regex-classes-and-algorithms]] |
| 31.12 Iterators | `[re.iter]` | `regex_iterator`, `regex_token_iterator` | [[regex-classes-and-algorithms]] |
| 31.13 Grammar | `[re.grammar]` | modified ECMAScript grammar | [[regex-classes-and-algorithms]] |

## Related

[[cpp17-lib-strings]] · [[cpp17-lib-localization]] · [[cpp17-lib-iterators]]
