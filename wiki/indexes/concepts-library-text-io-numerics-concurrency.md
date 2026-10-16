---
title: "Index shard: concepts — localization, numerics, I/O, regex, atomics, threads (clauses 25, 29-33)"
---
# Index shard: concepts — localization, numerics, I/O, regex, atomics, threads (clauses 25, 29-33)

One line per page. Directory of shards: `wiki/index.md`. Strings are in the foundations shard; iterators in the containers-algorithms shard.

## Clause 25 — localization

- [[cpp17-lib-localization]] — Clause 25 overview and section map.
- [[locale-class-and-facets]] — `locale`, facets, `use_facet`/`has_facet`, global locale, program-defined facets.
- [[locale-standard-facets]] — `ctype`, `codecvt`, `num_get`/`num_put`, `numpunct`, `collate`, time, money, messages.

## Clause 29 — numerics

- [[cpp17-lib-numerics]] — Clause 29 overview.
- [[complex-numbers]] — `complex<T>`: array-compatible layout, operations, literals, numeric type requirements.
- [[random-number-generation]] — URBG/engine/adaptor/distribution model, predefined engines, `random_device`, `seed_seq`.
- [[valarray]] — `valarray` and `slice`/`gslice`/mask/indirect subsets.
- [[numeric-operations]] — `accumulate`, `reduce`, scans, `inner_product`, `iota`, `gcd`, `lcm`; generalized sums.
- [[math-functions-and-fenv]] — `<cmath>` promotion rules, special functions, per-thread `<cfenv>`.

## Clause 30 — input/output

- [[cpp17-lib-input-output]] — Clause 30 overview and architecture.
- [[stream-base-classes]] — `ios_base`, `basic_ios`, state bits, format flags, standard stream objects.
- [[stream-buffers]] — `basic_streambuf` get/put areas and virtual hooks.
- [[formatted-and-unformatted-io]] — Sentries, extractors/inserters, `get`/`getline`/`ignore`, manipulators.
- [[string-and-file-streams]] — `stringbuf`, `filebuf` (open-mode table), string/file stream classes, `<cstdio>`.
- [[filesystem]] — `path`, directory iterators, status types, operations, error reporting.

## Clause 31 — regular expressions

- [[cpp17-lib-regex]] — Clause 31 overview.
- [[regex-classes-and-algorithms]] — Traits, constants, `basic_regex`, `match_results`, `regex_match`/`search`/`replace`, iterators, grammar.

## Clause 32 — atomics

- [[cpp17-lib-atomics]] — Clause 32 overview.
- [[atomics-and-memory-order]] — `memory_order`, `atomic<T>`, lock-freedom, `atomic_flag`, fences.

## Clause 33 — threads

- [[cpp17-lib-thread]] — Clause 33 overview and synchronizes-with summary.
- [[threads]] — `thread`, `thread::id`, `this_thread`, Lockable requirements, timing conventions.
- [[mutexes-and-locks]] — Six mutex types, `lock_guard`/`scoped_lock`/`unique_lock`/`shared_lock`, `lock`/`try_lock`, `call_once`.
- [[condition-variable]] — `condition_variable`, `condition_variable_any`, spurious wakeups, `notify_all_at_thread_exit`.
- [[futures-and-async]] — `promise`, `future`, `shared_future`, `packaged_task`, `async` launch policies.
