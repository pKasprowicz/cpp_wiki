---
type: concept
title: "std::ratio and std::chrono (time utilities)"
tags: [cpp17, library, templates]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Compile-time rationals and time utilities (`[ratio]`, `[time]`)

Parent: [[cpp17-lib-utilities]]. Timeouts in the thread library use these types: [[mutexes-and-locks]], [[condition-variable]], [[futures-and-async]].

## `ratio<N, D>` (`[ratio]`)

Exact compile-time rational with `intmax_t` numerator and denominator. `D == 0`, or |N| or |D| not representable, is ill-formed. The members `num` and `den` are the *reduced* form: `num = sign(N)*sign(D)*|N|/gcd`, `den = |D|/gcd`. A template parameter named `R1`/`R2` that is not a `ratio` specialization makes the program ill-formed. `ratio_add`, `ratio_subtract`, `ratio_multiply`, `ratio_divide` are alias templates yielding reduced `ratio`s (the program is ill-formed if the result is not representable in `intmax_t`); `ratio_equal`, `ratio_not_equal`, `ratio_less`, `ratio_less_equal`, `ratio_greater`, `ratio_greater_equal` derive from `bool_constant` (overflow in comparison is ill-formed). SI typedefs `atto` ... `exa` always exist; `yocto`, `zepto`, `zetta`, `yotta` exist only if their constants are representable in `intmax_t`.

## Clock requirements (`[time.clock.req]`)

A **Clock** bundles `rep` (arithmetic or arithmetic-like), `period` (a `ratio`, seconds per tick), `duration` (`duration<rep, period>`), `time_point` (a `time_point` over the same epoch), `is_steady` (true if `now()` never goes backwards and the tick time is constant), and `now()`. **TrivialClock** additionally requires that the types are comparable, default/copy constructible and assignable, swappable, numeric-like, and that `now()` does not throw ([[library-named-requirements]]).

## `duration<Rep, Period>` (`[time.duration]`)

- A count (`rep_`) of ticks of length `Period` seconds. `Rep` must be arithmetic or arithmetic-like and **not** itself a `duration`; `Period` must be a `ratio` with positive `num`. Members throw only what operations on `Rep` throw.
- `treat_as_floating_point<Rep>` controls implicit conversion: if true, any duration converts implicitly to this one; otherwise a conversion is implicit only when it is exact (the ratio of periods has denominator 1). `duration_values<Rep>` supplies `zero()`, `min()`, `max()` (`lowest()` and `max()` of `numeric_limits`) and can be specialized for class representations.
- Arithmetic: unary `+`, `-`, `++`/`--`, `+=`, `-=`, `*=`, `/=`, `%=`; non-member `+`, `-` between durations return the **common type** (`common_type` is specialized: the period is the *gcd* of the two periods); `duration * scalar`, `scalar * duration`, `duration / scalar`, `duration / duration` (a scalar ratio of ticks), `%`. Comparisons first convert to the common type.
- Conversions: `duration_cast<To>(d)` converts by multiplying and dividing the tick count through `common_type<To::rep, Rep, intmax_t>` (integer division truncates, unlike the explicit rounding functions); `floor`, `ceil`, `round` (round-half-even; only for integer representations) give the greatest, least, closest representable result. `abs(d)` requires a signed rep.
- Typedefs `nanoseconds`, `microseconds`, `milliseconds`, `seconds`, `minutes`, `hours`. **Literal suffixes** `h`, `min`, `s`, `ms`, `us`, `ns` in `std::literals::chrono_literals` (inline namespaces, so `using namespace std::chrono_literals` works): integer literals give the integer-rep duration types, floating literals an unspecified floating rep; overflow of an integer literal is ill-formed.

## `time_point<Clock, Duration>` (`[time.point]`)

A duration since the clock's epoch (`d_`). `Duration` must be a `duration`. Default-constructed = the epoch; construct from a duration (epoch + d) or convert from another `time_point` with a convertible duration. `time_since_epoch()`, `+=`/`-=` a duration, `min()`/`max()`; `tp + d`, `d + tp`, `tp - d` (time points), `tp1 - tp2` (a duration); comparisons compare `time_since_epoch()`; `time_point_cast`, `floor`, `ceil`, `round` convert the duration. The common type of two time points has the same clock and the common duration.

## Standard clocks (`[time.clock]`)

All three satisfy TrivialClock.

- `system_clock` — wall-clock time from the system real-time clock; `to_time_t` / `from_time_t` convert to/from `time_t` (rounding vs. truncation is implementation-defined). Required to have a signed duration (`min() < zero()`).
- `steady_clock` — `time_point` never decreases as real time advances, steady rate, cannot be adjusted.
- `high_resolution_clock` — the clock with the shortest tick period; **may be a synonym** for `system_clock` or `steady_clock`.

`<ctime>` (`[ctime.syn]`) is the C time header (C `<time.h>` in `std`).

## Related

[[cpp17-lib-utilities]] · [[numeric-limits]] · [[type-traits]] (`common_type`) · [[cpp17-lib-thread]] · [[literals]] (user-defined literal suffixes)
