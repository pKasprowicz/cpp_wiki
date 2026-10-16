---
type: concept
title: "C++17 clause 30: input/output library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 30: Input/output library (`[input.output]`)

About 37,500 words; 240 labelled sections (13,000 words of it are the file system library). The iostreams framework, string and file streams, and `<filesystem>`. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header(s) | Content | Wiki page |
|---|---|---|---|---|
| 30.2 Iostreams requirements | `[iostreams.requirements]` | — | `imbue` limits, position types, thread safety | [[stream-base-classes]] |
| 30.3 Forward declarations | `[iostream.forward]` | `<iosfwd>` | class relationships, `streampos` etc. | [[stream-base-classes]] |
| 30.4 Standard iostream objects | `[iostream.objects]` | `<iostream>` | `cin`, `cout`, `cerr`, `clog` (+ wide) | [[stream-base-classes]] |
| 30.5 Iostreams base classes | `[iostreams.base]` | `<ios>` | `ios_base`, `fpos`, `basic_ios`, flag manipulators | [[stream-base-classes]] |
| 30.6 Stream buffers | `[stream.buffers]` | `<streambuf>` | `basic_streambuf` | [[stream-buffers]] |
| 30.7 Formatting and manipulators | `[iostream.format]` | `<istream>`, `<ostream>`, `<iomanip>` | `basic_istream`/`ostream`, sentries, `setw`, `get_money`, `quoted` | [[formatted-and-unformatted-io]] |
| 30.8 String-based streams | `[string.streams]` | `<sstream>` | `stringbuf`, `istringstream`, `ostringstream`, `stringstream` | [[string-and-file-streams]] |
| 30.9 File-based streams | `[file.streams]` | `<fstream>` | `filebuf`, `ifstream`, `ofstream`, `fstream` | [[string-and-file-streams]] |
| 30.10 File systems | `[filesystems]` | `<filesystem>` | `path`, directory iterators, operations | [[filesystem]] |
| 30.11 C library files | `[c.files]` | `<cstdio>`, `<cinttypes>` | C stdio, inttypes | [[string-and-file-streams]] |

## Architecture in one picture

`basic_ios` (state, formatting flags, locale, tie) ← `basic_istream` / `basic_ostream` (formatted and unformatted operations through a *sentry*) → `basic_streambuf` (buffer and character source/sink: `stringbuf`, `filebuf`, user-defined). Formatting and parsing of numbers, money and time delegate to locale facets ([[locale-standard-facets]]); character classification and EOF come from `char_traits` ([[char-traits]]). Errors are reported through a state bitmask and optional exceptions ([[stream-base-classes]]); the optional exception type `ios_base::failure` is a `system_error` ([[error-codes-and-system-error]]).

## Related

[[cpp17-lib-localization]] · [[cpp17-lib-strings]] · [[iterator-adaptors]] (stream iterators) · [[memory-model-and-data-races]] (thread-safety of streams)
