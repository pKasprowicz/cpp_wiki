---
type: concept
title: "C++17 clause 14: member access control"
tags: [cpp17, language-core, standard-clause]
sources: [n4659-cpp17-draft-standard]
created: 2026-10-15
updated: 2026-10-15
---

# Clause 14: Member access control (`[class.access]`)

About 1,700 words; 7 labelled sections.

## Core rules

- **private**: usable only by members and friends of the declaring class. **protected**: additionally by derived classes and their friends (subject to the extra check below). **public**: anywhere. Members of a class defined with `class` default to private; with `struct` or `union`, public. Members can access everything their class can; a local class of a member function accesses what that function can.
- Access control applies uniformly to all names; for overloaded names it applies to the function chosen by overload resolution. It controls *access*, **not visibility**: inaccessible names are still found by lookup, and implicit conversions to inaccessible bases are still considered; a construct using something inaccessible is then ill-formed (`[class.access]/5`). See [[name-lookup]] and [[overload-resolution]] for the order: lookup → overload resolution → access.
- Access in default arguments is checked at the point of declaration; for default template arguments, in the context where they appear.
- A member access-specifier label governs members up to the next specifier; any number is allowed; a redeclared member must have the same access (`[class.access.spec]`).

## Accessibility of bases and base members (`[class.access.base]`)

| Base specifier | Public base members become | Protected base members become |
|---|---|---|
| `public` | public | protected |
| `protected` | protected | protected |
| `private` | private | private |

With no access-specifier, `public` is assumed for `struct` and `private` for `class`. A base B of N is accessible at R if an invented public member of B would be public in N; or R is in a member/friend of N (or of a class derived from N) and the invented member would be private/protected in N; or through an intermediate accessible class. A member `m` named in class N (the **naming class**, where lookup found it) is accessible at R if it is public in N, private/protected in N and R is a member/friend of N (or, for protected, of a class derived from N), or via an accessible base. A member access through an implicit or explicit `this->` is ill-formed if the object pointer cannot be implicitly converted to a pointer to the naming class.

## Friends (`[class.friend]`)

- A friend (function or class) may use private and protected member names; it is not a member. Friend classes get access in base-specifiers and member declarations too.
- A friend declaration that doesn't declare a function has the form `friend elaborated-type-specifier;`, `friend simple-type-specifier;` or `friend typename-specifier;`; if the type is not a class, the declaration is ignored. A class can't be *defined* in a friend declaration. No storage-class-specifier. The meaning does not depend on which access section it sits in.
- A function first declared as a friend takes the linkage of its namespace. For overloaded names only the matching function is a friend. A member function of one class may be a friend of another.
- A friend function may be **defined** in the class only if the class is non-local, the name is unqualified, and the function has namespace scope; it is then implicitly `inline` and in the lexical scope of the class. Not inherited, not transitive (`/10`). Friend declarations in local classes look up prior declarations only within the innermost enclosing non-class scope.

## Protected members (`[class.protected]`)

For a protected non-static member of its naming class accessed by a member/friend of class C: forming a pointer to member requires the nested-name-specifier to denote C or a class derived from C; any other access requires the object expression's class to be C or derived from C.

## Other rules

- **Virtual functions** (`[class.access.virt]`): access is determined by the declaration visible via the object expression's static type, not by overriders.
- **Multiple paths** (`[class.paths]`): the access is that of the path giving the most access.
- **Nested classes** (`[class.access.nest]`): a nested class is a member with ordinary member access rights; enclosing-class members get no special access to the nested class.

## Related

[[cpp17-classes]] · [[cpp17-derived-classes]] · [[cpp17-declarations]] (using-declaration accessibility)
