# Contributing to LoreStore

Thank you for helping. LoreStore is a specification: a file-based, model-agnostic canon
store for fiction, and the agent framework that reads and writes it. This repository
holds the spec, its JSON Schemas, a set of worked examples, and a conformance checker.
It does not hold an implementation.

There are three ways to contribute:

1. **Report a problem or ask a question** about the spec (an issue).
2. **Propose a change** to the spec, the schemas, the examples, or the checker (a pull
   request to this repository).
3. **Submit a package**, such as a canon base, a fanon package, or a fan work, to the
   package registry. See [Submitting a package](#submitting-a-package-to-the-registry).

## Setting up

You need Git and Python 3.10 or later.

```
git clone https://github.com/lorestore-dev/lorestore.git
cd lorestore
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r tools/requirements.txt
python tools/check.py
python tools/refs.py
```

The checker prints one line per check and ends with a failure count. A clean checkout
reports `FAILURES: 0`. If it doesn't, please open an issue.

### What's where

| Path                    | What it is                                                                  |
| ----------------------- | --------------------------------------------------------------------------- |
| `spec/`                 | The specification, one chapter per file. Start with the README's reading order. |
| `spec/03-layers.md` §3.3 | The file catalog: the authority on which agent writes which file           |
| `schemas/`              | JSON Schemas for `project.yaml`, `package.yaml`, and `universe.yaml`        |
| `examples/`             | Abridged Harry Potter and Star Trek packages, a crossover universe, and projects |
| `examples/README.md`    | The numbered example cases and the results a conforming host must give      |
| `tools/check.py`        | The conformance checker                                                     |
| `tools/refs.py`         | Checks that every `§` reference and relative link resolves, and every example case is linked from the spec |
| `DECISIONS.md`          | Every design decision, newest first, with its reasoning                     |

## Reporting a problem

Open an issue on [GitHub](https://github.com/lorestore-dev/lorestore/issues). The most
useful issues:

- quote the rule and give its `§` reference;
- give a concrete case: the files, the stack, the cutoff, and what you expected to happen;
- say whether the problem is a contradiction (two rules disagree), a gap (no rule covers
  the case), or something unclear (a rule can be read two ways).

Some questions are design questions, not bugs. Those are welcome too, and an issue is
the right place to discuss them before anyone writes a pull request.

## Proposing a change

For anything beyond a typo, open an issue first, so the change can be agreed before you
spend time on it. Then:

1. Create a branch from `main`.
2. Make the change, following the rules below.
3. Run `python tools/check.py` and make sure it reports `FAILURES: 0`, and
   `python tools/refs.py`, which checks every `§` reference and link.
4. Open a pull request that links the issue and says which rules changed.

### Rules for spec changes

- **Change a rule where it is defined.** Each concept is defined in exactly one chapter,
  and other chapters refer to it with `§`. If you find a rule restated somewhere else,
  change the definition and point the restatement at it.
- **Keep the agents and the catalog in agreement.** The file catalog (§3.3) is the
  authority on who writes each file. Agent specifications (§12) and workflows (§13) must
  agree with it.
- **Record the decision.** Every change to a rule gets an entry in `DECISIONS.md`: what
  was unclear or wrong, what was decided and why, and the sections it touched. New
  entries go at the top, numbered after the last one.
- **Keep every `§` reference resolving.** If you add, remove, or renumber a section,
  update the references to it.
- **Change behavior, change the checker.** If the change adds or alters behavior in the
  data model, add checks for it to `tools/check.py`, and add the expected result to
  `examples/README.md`. Give a new case an anchor (`<a id="case-<id>"></a>`), and link
  to it from the `**Example cases:**` line at the end of the spec section it shows.
- **Breaking changes** bump `spec_version` in the schemas and the spec.
- Some decisions always belong to the author of a story, never to an agent: order
  inversions (§6.8), divergence conflicts (§6.6), hidden canon (§6.12), theory conflicts
  (§6.13), source conflicts (§6.14), and sending a chapter to early access or releasing it (§13.9, §13.3). A
  change must not let an agent make one of these decisions.

### Writing style

- Plain English. Use **MUST**, **SHOULD**, and **MAY** as RFC 2119 defines them, in
  capitals.
- American spelling ("-ize", "catalog"), as in the rest of the spec.
- Write "LoreStore" in prose and `lorestore` for package, CLI, and directory names.
- Markdown tables are aligned, so they read well as plain text.

### Examples and franchise material

The examples use Harry Potter and Star Trek only to illustrate the system. These works
belong to their owners (see the README).

- **Record facts in your own words, with a citation.** Never copy source text: no
  passages, no dialogue, no episode transcripts. In the examples, even the quotations
  are paraphrased.
- **Check facts against a source before adding them.** Say in your pull request where
  you checked them. Facts that sources disagree on, or that differ between editions,
  make poor examples, unless the example is about that disagreement.
- Keep the examples abridged: add only the rows a rule needs.

### License of contributions

This project is licensed under the [Apache License 2.0](LICENSE). By submitting a
contribution, you agree that it is licensed under the same terms (section 5 of the
license).

## Submitting a package to the registry

> **Status: proposed.** The registry doesn't exist yet. This section describes how it is
> intended to work, so that people can prepare packages and comment on the process.
> Discussion is welcome in the issues.

A **package** (§2.3) is a reusable, read-only bible: a fandom's canon base, an official
work, an adaptation, fanon, a single fan work, or a theories collection. The registry is
where people publish packages so that others can stack them in their projects.

### How it will work

The registry will be a separate repository, `lorestore-dev/registry`, laid out exactly
like a workspace's `worlds/` folder (§2.1, §2.3). Each package has one folder, named by
its id, and its `package.yaml` states the current version:

```
packages/
└── harry-potter/
    ├── base/                 # id harry-potter: the base
    ├── fanon/                # id harry-potter/fanon
    └── fanfic/
        └── <work>/           # id harry-potter/fanfic/<work>
            ├── package.yaml  # version: 1.2.3
            ├── index.md
            ├── sources.md
            └── …
```

Every published version is kept as a Git tag, `<id>@<version>` (for example
`harry-potter@3.2.1` or `harry-potter/fanon@1.0.4`). The tag is exactly the pin a project
writes in its `layers:` (§2.2), so a project names a registry package by its bare id
and version, with no registry prefix, and a host fetches that pin by checking out the
tag.

To submit a package, or a new version of one:

1. Fork the registry. Add the package's folder, or update it and bump `version` in
   `package.yaml` by the rules in §2.8.
2. Run the validator, which will also run in CI on every pull request.
3. Open a pull request. A maintainer reviews it against the requirements below.
4. When it is merged, the maintainers tag the version. A tagged version is
   **immutable**: a correction is a new version.

### Neutrality: the registry records, it never rules

Fans disagree about canon: what counts, what a passage means, which edition is right,
what order things happen in. The registry does not settle these arguments. It gives
each one a place, and leaves the decision to each project, through its stack and
resolution mode (§2.2, §5.4). Maintainers apply the rules below; they do not decide what
is true.

- **Cite it, or cut it.** Every fact cites a source. A fact nobody can cite does not go
  in.
- **Interpretation goes in theories.** A reading of the text ("Death in the tale is
  Dumbledore") is a theory, with numbered claims and evidence, in a `theories` package
  (§6.13). It is never written into a base as fact.
- **Disputed canon goes in its own package.** A base holds only material whose place in
  canon is not in dispute. Official material whose status is disputed, such as Star
  Trek's animated series, goes in an `official` package (§2.3). Maintainers decide what
  counts as disputed. When in doubt, the material goes in its own package: a project
  can always stack it, but it cannot remove it from a base.
- **Contradictions are recorded, not resolved.** When sources disagree, for example two
  editions, both rows go in, each with its citation. Nobody picks a winner in the base:
  each project's author does (§6.14).
- **Editorial choices are explained and can be overridden.** Where a package has to
  choose (the order of the ruler, where an inserted work sits), it says why in the
  table's `Notes`, and any project can reorder (§6.8).
- **Anyone can publish an alternative.** There can be several fanon or theories
  packages for one fandom, each under its own name (`harry-potter/fanon`,
  `harry-potter/fanon-<name>`). Publishing a package is not an endorsement of it.
- **Arguments about what is true happen in issues, about the rules.** A request to
  change a base is reviewed on whether the change is cited and whether it is disputed,
  never on whether a maintainer agrees with it.

### Requirements

**Format.** A package must:

- validate against `schemas/package.schema.json`, with `spec_version` matching the
  current spec;
- have an id that matches its folder, and a `kind` that matches the form of its id
  (§2.3);
- pin every package it relies on, at a version already in the registry;
- register only sources whose tiers its kind allows (§2.3, §5.2);
- date every row with a valid point on its base's ruler (§4.2), plus any segments it
  inserts (§4.10) or works it adapts (§4.9);
- add to a lower package's entities only through extension sheets (§2.7), never by
  redefining a key;
- have `status: locked` (§2.8), and an `index.md` listing every file.

**Content.** A package is published under the [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/) license (CC BY 4.0), so
that anyone can stack, adapt, and build on it, as long as they credit its contributors.
This license covers the contributors' own work only, never the works the package
describes. By submitting a package, you agree to publish it under CC BY 4.0. A package
must also:

- record facts in the contributor's own words, each with a citation. Short quotations
  are the only exception (§2.3, §10.13): never passages, chapters, or transcripts;
- contain world-layer files only, with no source texts, extraction records, manuscripts,
  or project material (§2.3, §2.4);
- credit every source in `sources.md`, and credit fan theories to their origin, or say
  the origin is untraced (§5.6).

**Fan works.** A `fanfic` package imports one fan work. It needs the **fan author's
permission**, recorded in the package's `sources.md` together with the author's credit.
Packages that import a fan work without permission will be removed.

**Ids.** A fandom's base takes the bare fandom id (`harry-potter`). The base belongs
to the registry, not to whoever submitted it first: it is maintained in the open, and
anyone can propose changes to it under the neutrality rules above. Other packages take
an id under the fandom (`harry-potter/fanon`, `harry-potter/fanfic/<work>`) and belong
to their contributors. If an id is disputed, maintainers decide in an issue.

**Rights holders.** A rights holder who objects to a package can open an issue or
contact the maintainers, and the package will be reviewed and, if necessary, removed.

### Still to decide

These questions are open, and the process above may change once they are settled:

- **The validator.** `tools/check.py` in this repository checks only the examples. The
  registry needs a validator for any package, covering the format requirements above.
  It is expected to live in a repository of its own, so that the registry's CI and
  package authors can both run it.
- How deprecated or superseded packages are marked.
