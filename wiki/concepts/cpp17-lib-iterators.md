---
type: concept
title: "C++17 clause 27: iterators library"
tags: [cpp17, library, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 27: Iterators library (`[iterators]`)

About 7,800 words; 96 labelled sections. The abstraction that decouples containers from algorithms. Parent: [[cpp17-lib-introduction]].

## Section map

| Subclause | Label | Header | Content | Wiki page |
|---|---|---|---|---|
| 27.2 Iterator requirements | `[iterator.requirements]` | — | five categories, contiguity, ranges, singular values | [[iterator-categories-and-requirements]] |
| 27.3 `<iterator>` synopsis | `[iterator.synopsis]` | `<iterator>` | declarations | — |
| 27.4 Iterator primitives | `[iterator.primitives]` | `<iterator>` | `iterator_traits`, tags, `advance`/`distance`/`next`/`prev` | [[iterator-categories-and-requirements]] |
| 27.5 Iterator adaptors | `[predef.iterators]` | `<iterator>` | `reverse_iterator`, insert iterators, `move_iterator` | [[iterator-adaptors]] |
| 27.6 Stream iterators | `[stream.iterators]` | `<iterator>` | `istream_iterator`, `ostream_iterator`, `istreambuf_iterator`, `ostreambuf_iterator` | [[iterator-adaptors]] |
| 27.7 Range access | `[iterator.range]` | `<iterator>` + container headers | `begin`, `end`, `rbegin`, ... | [[iterator-adaptors]] |
| 27.8 Container access | `[iterator.container]` | same | `size`, `empty`, `data` | [[iterator-adaptors]] |

## Key ideas

- Iterator categories are a **requirements taxonomy** plus **tag types** for dispatch; contiguity is an extra property of random-access iterators with no tag.
- Ranges are half-open iterator pairs `[first, last)` and must be *valid* (last reachable from first); algorithms ([[cpp17-lib-algorithms]]) and container constructors consume them.
- Invalidation is a property of the container, not the iterator: [[iterator-invalidation]].

## Related

[[cpp17-lib-containers]] · [[cpp17-lib-algorithms]] · [[iterator-categories-and-requirements]] · [[iterator-adaptors]]
