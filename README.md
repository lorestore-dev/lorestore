# LoreStore

A specification for a **file-based, model-agnostic canon store for fiction**: how a
fictional world, and the stories set in it, are stored as small markdown and YAML files;
how facts are dated, sourced, and resolved; how a story forks from canon without
editing it; and how a team of narrow AI agents reads and writes those files.

**Status:** draft, spec version `0.1`. Breaking changes are still expected.

## Reading order

| #  | Chapter                                             | Covers                                                               |
| -- | --------------------------------------------------- | -------------------------------------------------------------------- |
| 1  | [Overview](spec/01-overview.md)                     | Purpose, principles, the golden rule, terms                          |
| 2  | [Layout](spec/02-layout.md)                         | Worlds, universes, projects; path resolution; versioning             |
| 3  | [Layers](spec/03-layers.md)                         | The write boundary, and the catalog of every file and its writer     |
| 4  | [Temporal model](spec/04-temporal.md)               | The ruler, canon points, append-only state histories                 |
| 5  | [Sources](spec/05-sources.md)                       | The source registry, tiers, canon profiles                           |
| 6  | [Divergence](spec/06-divergence.md)                 | The adherence contract, the divergence ledger, classifications       |
| 7  | [Snapshot](spec/07-snapshot.md)                     | The query: what is true as of X, under profile P                     |
| 8  | [Crossovers](spec/08-crossovers.md)                 | Universes and the bridge                                             |
| 9  | [Modules](spec/09-modules.md)                       | Frames (time travel), LitRPG, languages                              |
| 10 | [Formats](spec/10-formats.md)                       | The exact structure of every file                                    |
| 11 | [Agent contract](spec/11-agent-contract.md)         | The orchestration loop, agent anatomy, retrieval, gates              |
| 12 | [Agents](spec/12-agents.md)                         | The eighteen agents                                                  |
| 13 | [Workflows](spec/13-workflows.md)                   | Novel, short story, serial, the overlays, extraction, crossover      |
| 14 | [Implementation](spec/14-implementation.md)         | Host requirements, validation rules, the contracts summarized        |

Chapters 1–7 are the core model. Implementers of a host application (such as the
Integrated Writing Environment) should also read chapters 10, 11, and 14.

## Repository layout

```
spec/        the specification, one chapter per file
schemas/     JSON Schemas for project.yaml, world-config.yaml, universe.yaml
examples/    a small conforming workspace, with expected snapshot results
tools/       the conformance checker for the examples
DECISIONS.md design decisions taken, and the questions still open
LICENSE      Apache License 2.0
```

## Conformance checker

[tools/check.py](tools/check.py) checks that the spec, the schemas, and the examples
agree. It validates every example manifest against the JSON schemas, then runs a
reference implementation of the snapshot algorithm (§7) and compares each result with
the expected answers in [examples/README.md](examples/README.md). It covers canon-point
parsing and ordering (§4.2), the canon track and project order (§6.7–6.8), branch and
retelling modes (§6.6), and hidden truths (§4.4, §6.12).

```
pip install -r tools/requirements.txt
python tools/check.py
```

It prints one line per check and a failure count, and exits non-zero if any check fails.
Run it after changing a rule, a schema, or an example.

**Limitations:**

- It checks the bundled examples only. Paths and expected values are hard-coded, so it is
  not a validator for workspaces of your own.
- It is a reference for the data model only. It does not test the agent contract, the
  agents, or the workflows (chapters 11–13).
- It parses only the tables it needs, not every format in chapter 10.
- It does not check markdown links or `§` references.
- A passing run means the examples are consistent with the checker's reading of the
  spec. Where the two disagree, the spec is the authority.

## Conventions

- **MUST**, **SHOULD**, and **MAY** are used as in RFC 2119.
- Each concept is defined in exactly one chapter, and other chapters link to it with
  `§` references. When changing a rule, change it where it is defined.
- The file catalog (§3.3) is the authority on which agent writes which file. Agent
  specifications and workflows must agree with it.
- Examples use **Harry Potter** (a magic world, novels and chapters) and **Star Trek**
  (a technology world, seasons and episodes), both in the spec text and in the
  abridged world packages in `examples/`. Facts are recorded in our own words, with
  citations, never as copied text.

## Changing the spec

Record any decision that changes a rule in [DECISIONS.md](DECISIONS.md), with the
reasoning. Bump `spec_version` in the schemas and the spec when a change breaks
existing files.

## License

Copyright 2026 Sam Wederell. Licensed under the [Apache License, Version 2.0](LICENSE).
You may use, modify, and distribute this specification, its schemas, and its examples,
including in commercial implementations, provided you keep the license and the
copyright and attribution notices.

## Third-party works

The spec and the examples refer to two franchises purely to illustrate the system:

- **Harry Potter**: the novels, characters, and related names and marks belong to
  J. K. Rowling and Warner Bros. Entertainment Inc.
- **Star Trek**: the series, characters, and related names and marks belong to Paramount
  Global (CBS Studios Inc.).

This project is not affiliated with, endorsed by, or sponsored by any of these owners.
The examples record brief facts in our own words, with citations, and quote no source
text. The Apache License applies only to this project's own material, not to those
works.
