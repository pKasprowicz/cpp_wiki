---
type: concept
title: "std::filesystem: path, directory iteration, status and operations"
tags: [cpp17, library]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# File systems (`<filesystem>`, `[filesystems]`)

Lexical path manipulation plus operations on the host file system. Parent: [[cpp17-lib-input-output]]. File streams that accept paths: [[string-and-file-streams]]. Errors: [[error-codes-and-system-error]].

## Conformance and conventions

- Behavior is specified in terms of **POSIX** where stated; implementations should document deviations and need not provide behavior unsupported by the underlying file system. "Operating system dependent" behavior is tied to the implementation-defined OS (possibly an emulator).
- **File system races**: if calls introduce a file system race (concurrent interleaved access/modification of the same object by threads, processes or machines), behavior is **undefined**; where a pre-check would be unreliable because of races, no *Requires* is specified (`[fs.race.behavior]`).
- Template parameters named `EcharT` are restricted to the *encoded character types* `char`, `wchar_t`, `char16_t`, `char32_t`; `InputIterator` parameters need those as value types (`[fs.req]`). Entities live in `std::filesystem`.
- **Error reporting** (`[fs.err.report]`): most functions come in two overloads. Without an `error_code&` argument, an OS error that prevents the function from meeting its spec is thrown as **`filesystem_error`** (a `system_error` subclass storing zero, one or two paths: `path1()`, `path2()`, `code()`, and `what()`); allocation failure is reported as usual; destructors never throw. With an `error_code&` argument, the code is set to the OS error, or `clear()`ed on success; such overloads are typically `noexcept`.

## `path` (`[fs.class.path]`)

- A `path` holds a **pathname** and deals only with **lexical and syntactic** aspects: it need not exist, and need not be valid for the current OS. It keeps the native and generic representations consistent via conversion functions `G` and `N`.
- **Generic format**: optional *root-name*, optional *root-directory*, then filenames separated by *directory-separators*; multiple successive separators count as one (except in a root-name). The filenames `.` and `..` mean current and parent directory. `path::value_type` is the OS-dependent encoded character type; `preferred_separator` is the OS-preferred separator.
- **Format and encoding** (`[fs.path.cvt]`): `path::format` is `native_format`, `generic_format` or `auto_format`; a *detected-format* argument is taken as generic iff it matches the generic format and is not acceptable as a native path. Character types are converted to/from the native encoding: `char` → native narrow encoding, `wchar_t` → native wide, `char16_t` → UTF-16, `char32_t` → UTF-32; the converting constructors accepting a `locale` use its `codecvt` facets.
- **`Source` arguments** can be a `basic_string`, a `basic_string_view`, an input iterator over a null-terminated sequence, or a character array decaying to a pointer to a null-terminated sequence; null pointers are not allowed.
- **Modifying**: `operator/=` and `append` (insert a separator if needed; if the argument is absolute, or has a different root-name, it **replaces** the path), `concat`/`+=` (no separator), `clear`, `make_preferred`, `remove_filename`, `replace_filename`, `replace_extension`, `swap`.
- **Observers**: `native()`, `c_str()`, string conversions in native and generic format, `compare`, decomposition `root_name()`, `root_directory()`, `root_path()`, `relative_path()`, `parent_path()`, `filename()`, `stem()` (filename without the last extension, except `.` / `..` and leading-dot names), `extension()`; queries `empty()`, `has_*()`, `is_absolute()`, `is_relative()`; generation `lexically_normal()`, `lexically_relative(base)`, `lexically_proximate(base)`. Normalization replaces separators with `preferred-separator`, removes `.` elements, collapses `name/..` pairs, removes `..` after a root directory, and yields `.` for an empty result.
- A `path` is a **range** of its elements (root-name, root-directory, filenames) via `begin()`/`end()` constant bidirectional iterators (value type `path`; any non-const member call invalidates them); `operator<<`/`>>` use quoted forms; `u8path(...)` factory functions build paths from UTF-8 input.

## Enumerations and small types

`file_type` (`none`, `not_found`, `regular`, `directory`, `symlink`, `block`, `character`, `fifo`, `socket`, `unknown`, plus implementation-defined extras); `copy_options` (bitmask in groups: existing-file policy `skip_existing` / `overwrite_existing` / `update_existing`; `recursive`; symlink policy `copy_symlinks` / `skip_symlinks`; form of copy `directories_only` / `create_symlinks` / `create_hard_links`; `none` is the default in each group); `perms` (owner/group/others read-write-exec bits, set-uid/gid, sticky, `all`, `mask`, `unknown`); `perm_options`; `directory_options` (`none`, `follow_directory_symlink`, `skip_permission_denied`); `file_status` (type + permissions); `space_info` (`capacity`, `free`, `available`); `file_time_type` (a `chrono::time_point` of an unspecified trivial clock, [[chrono-and-ratio]]).

## Directory iteration

- `directory_entry` stores a `path` and possibly **cached** attributes (hard link count, status, symlink status, size, last write time) that directory iteration may fill in and `refresh()` updates.
- `directory_iterator` is an **input iterator** over `directory_entry`s of one directory: the default-constructed value is the end iterator and the only valid end value; reaching the end or an error makes an iterator equal to it; the order of entries is **unspecified**; `.` and `..` are never produced; `path()` of an entry is the directory path with the filename appended. `recursive_directory_iterator` additionally descends into subdirectories and offers `depth()`, `options()`, `recursion_pending()`, `pop()` and `disable_recursion_pending()` (undefined on a non-dereferenceable iterator).

## Operations (`[fs.op.funcs]`)

`absolute`, `canonical` (path must exist; no symlink/dot/dot-dot), `weakly_canonical`, `relative`, `proximate`, `copy` (governed by `copy_options`), `copy_file`, `copy_symlink`, `create_directory`, `create_directories`, `create_hard_link`, `create_symlink`, `create_directory_symlink`, `current_path` (get/set), `exists`, `equivalent`, `file_size`, `hard_link_count`, `is_block_file`, `is_character_file`, `is_directory`, `is_empty`, `is_fifo`, `is_other`, `is_regular_file`, `is_socket`, `is_symlink`, `last_write_time` (get/set), `permissions`, `read_symlink`, `remove`, `remove_all` (recursive; `!exists(symlink_status(p))` afterwards), `rename`, `resize_file`, `space`, `status` (follows symlinks), `symlink_status`, `status_known`, `temp_directory_path`. Error returns for the `error_code` overloads are documented per function (e.g. `exists` and `is_*` return `false`, `file_size` returns `static_cast<uintmax_t>(-1)`, `hard_link_count` returns `uintmax_t(-1)`, `last_write_time` returns `file_time_type::min()`, `current_path` returns an empty path).

## Related

[[string-and-file-streams]] · [[error-codes-and-system-error]] · [[standard-exception-classes]] · [[chrono-and-ratio]] · [[basic-string]]
