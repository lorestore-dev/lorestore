# Roadmap

A working note on the path from draft 0.2 to LoreStore 1.0. It is removed at the 1.0 cut,
along with everything else that records how the spec was made rather than what it says.

## The goal: a clean 1.0

The 1.0 repository holds only what an implementer needs:

- `spec/`: the specification;
- `schemas/`: the JSON Schemas;
- `examples/`: the conforming workspace, which doubles as the conformance fixtures;
- `agents/` and `workflows/`: the reference agent and workflow files;
- `README.md`, `CONTRIBUTING.md`, `LICENSE`, and a `CHANGELOG.md` that starts at 1.0.

No decision log, no working notes, no tools. The decision history stays in git, under an
archive tag.

## Steps

### 1. Land 0.2

- Commit the `spec-0.2` work in logical commits, and open a PR to `main`.
- Add the § reference check as `tools/refs.py`, and a `.gitattributes` that fixes
  CRLF line endings, so that no normalizer script is needed.
- Add CI that runs `tools/check.py` and the § reference check on every PR.
- Tag `v0.2`.

### 2. In-world time (0.3)

The ruler orders reading, not the story's own chronology (§4.1), and the spec has no
structured in-world date: `Story time` is free text (§10.15), `True from` is a ruler
point (§4.4), and universe offsets (§8.1) shift a base calendar that nothing defines.

- Design an optional in-world calendar for a base, flexible enough for real-world dates,
  stardates, and an original world's own calendar.
- Let rows and story events carry in-world dates, so that ages, durations, prequels,
  and time travel can be checked rather than judged.
- Give universe offsets a calendar to apply to.
- Build on the dates with three modules: travel (journey times), mysteries (clues and
  fair play), and lineage (parentage and titles).
- Add the examples, checks, and decisions that go with it. Tag `v0.3`.

### 3. Reference agents and workflows (0.4)

- Write the 19 agent files (`agents/*.md`) to the anatomy of §11.3 and the
  specifications of §12.
- Write the workflow files (`workflows/*.md`) for every chain and overlay of §13.
- Change §1.2: the spec defines the contract (§11–12), and `agents/` and `workflows/`
  are an informative reference implementation of it, no longer out of scope.
- Prove the model-agnostic claim (§11.1) with a minimal tool-less loop: run
  `short-story` end to end on `three-brothers`.
- Tag `v0.4`.

### 4. Outside review (0.5)

- Stop internal review rounds.
- Add `REVIEWING.md`, a guide for reviewers, and a **Review finding** issue form.
- Have one or two people who did not write the spec read it, ideally by implementing a
  piece of it, such as the snapshot query (§7).
- Fold their findings into the spec and the agents. Tag `v0.5`.

### 5. Split out the tools

- Create `lorestore-dev/lorestore-tools`, which holds the spec repository as a **git
  submodule**, pinned to a spec tag. The dependency runs from the tools to the spec: the
  tools read its schemas and examples, never the other way round. Moving to a new spec
  version is one deliberate submodule bump in the tools repo.
- Move `check.py` there. Grow it into the `lorestore` Python package, with a CLI that
  works on any workspace (`validate` for the §14.2 checks, `snapshot`, `compose`,
  `points`), and keep the example checks as its test suite.
- The spec repository holds no submodule. Its README links to the tools repo.
- The spec repository's CI keeps two light checks: the examples validate against the
  schemas, and every § reference resolves. Optionally it also checks out the tools repo
  in the workflow file and runs the full checker on every spec PR, so that a change that
  breaks the examples is caught before it merges.

### 6. Cut 1.0

- Tag the last pre-1.0 commit `v0-archive`, which keeps the decision history.
- Remove `DECISIONS.md`, `CLAUDE.md`, `ROADMAP.md`, `REVIEWING.md`, and `tools/`.
- Remove "draft" from the README status, and set `spec_version: "1.0"` in the schemas,
  the spec, and every example manifest.
- Point CONTRIBUTING.md's package registry at something that exists, or remove the
  mention.
- Start `CHANGELOG.md`, recording only changes made after 1.0.
- Make a final pass for consistency, then tag `v1.0`.

## After 1.0

- A package registry for shared packages.
- Conformance guidance for hosts and IWE builders.
- An extraction pilot on a public-domain work, such as the Sherlock Holmes stories,
  to test extraction and merging at full scale.
