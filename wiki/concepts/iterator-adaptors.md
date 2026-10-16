---
type: concept
title: "Iterator adaptors, stream iterators and range/container access functions"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Iterator adaptors, stream iterators, range access (`[predef.iterators]`, `[stream.iterators]`, `[iterator.range]`, `[iterator.container]`)

Parent: [[cpp17-lib-iterators]]. Requirements and traits: [[iterator-categories-and-requirements]].

## Reverse iterators (`[reverse.iterators]`)

`reverse_iterator<Iter>` wraps a **bidirectional** iterator and traverses it backwards; `base()` returns the wrapped iterator, which refers to the element *after* the one the reverse iterator denotes (dereferencing is "the element before `base()`"). If any random-access member (`+`, `-`, `+=`, `-=`, `[]`, `<`, `>`, `<=`, `>=`, difference) is instantiated, `Iter` must be random access. `make_reverse_iterator(i)` constructs one. Containers' `rbegin()` is `reverse_iterator(end())` ([[container-requirements]]).

## Insert iterators (`[insert.iterators]`)

Output iterators that turn assignment into container insertion, so copying algorithms work in "insert mode": `back_insert_iterator` (calls `push_back`), `front_insert_iterator` (`push_front`), `insert_iterator` (`insert(pos, value)` and then advances past the inserted element). Created with `back_inserter(c)`, `front_inserter(c)`, `inserter(c, i)`. `operator*` returns the iterator itself; `operator++` is a no-op returning `*this`; assignment performs the insertion (copy and move forms).

## Move iterators (`[move.iterators]`)

`move_iterator<Iter>` (requires an input iterator; bidirectional/random-access operations require those categories) behaves like `Iter` except that dereferencing yields an **rvalue reference** (`reference` is `remove_reference_t<R>&&` when the wrapped reference type `R` is a reference, otherwise `R`). `make_move_iterator(i)` creates one; used so that copy algorithms move elements instead.

## Stream iterators (`[stream.iterators]`)

- `istream_iterator<T, charT, traits, Distance>` is an **input iterator** that reads `T` values with `operator>>`: it reads on construction (or lazily at first use) and on every `++`; when extraction fails (`fail()` true) it becomes equal to the **end-of-stream iterator**, which is what the default constructor creates. Two end-of-stream iterators are equal; end-of-stream never equals another; two non-end iterators are equal when constructed from the same stream. Dereferencing end-of-stream is undefined.
- `ostream_iterator<T, charT, traits>` is an **output iterator** that writes with `operator<<`, followed by an optional delimiter string after every element.
- `istreambuf_iterator<charT, traits>` is an input iterator over a `basic_streambuf`'s characters: `*` is `sgetc()`, `++` is `sbumpc()`; equal to end-of-stream when `sgetc()` returns `eof`; `equal` is true if both or neither are end-of-stream, regardless of which streambuf; post-increment returns an unspecified proxy that remembers the previous character. `ostreambuf_iterator` writes characters with `sputc` and records failure (`failed()`). See [[stream-buffers]].

## Range access and container access (`[iterator.range]`, `[iterator.container]`)

Free function templates available from `<iterator>` and from the headers of all containers, `<string>`, `<string_view>`, `<regex>`: `begin`, `end`, `cbegin`, `cend`, `rbegin`, `rend`, `crbegin`, `crend` (call the member, or for arrays and `initializer_list` return pointers/`reverse_iterator`s); `size(c)` (`c.size()` or `N`), `empty(c)`, and `data(c)` (`c.data()`, array pointer, or `initializer_list` data). These are what range-based `for` and generic code rely on for arrays and non-member ranges ([[cpp17-statements]]).

## Related

[[iterator-categories-and-requirements]] · [[cpp17-lib-iterators]] · [[stream-buffers]] · [[formatted-and-unformatted-io]] · [[mutating-sequence-algorithms]] (`copy` with insert iterators) · [[cpp17-annex-d-compatibility-features]] (deprecated `std::iterator`)
