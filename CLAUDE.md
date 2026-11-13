# LoreStore: notes for Claude

This repository is the LoreStore specification (draft 0.1): a file-based, model-agnostic
canon store for fiction, plus the agent framework that reads and writes it. It holds the
spec, not an implementation.

## Where things are

- `spec/01-…14-…md`: the specification. Each concept is defined in one chapter and
  referenced elsewhere with `§`. Change a rule where it is defined.
- `spec/03-layers.md` §3.3 (the file catalog) is the authority on who writes each file.
- `schemas/`: JSON Schemas for `project.yaml`, `world-config.yaml`, `universe.yaml`.
- `examples/`: abridged Harry Potter and Star Trek worlds, a crossover universe, and six
  projects. `examples/README.md` lists the numbered cases and their expected results.
- `DECISIONS.md`: decisions D1 onwards, newest first. Add an entry for every rule change.
- `tools/check.py`: the conformance checker.

## Working rules

- After changing a rule, schema, or example, run the checker; it must report
  `FAILURES: 0`:
  `pip install -r tools/requirements.txt && python tools/check.py`
- If a change adds behavior to the data model, add checks for it to `tools/check.py` and
  the expected result to `examples/README.md`.
- Check that every `§` reference still resolves to a heading after renumbering.
- Example facts are recorded in our own words with citations; never copy source text.
- Prose style: plain English, RFC 2119 keywords in capitals. Match the existing
  spelling, which is mostly American ("-ize", "catalog").
- Name: "LoreStore" in prose; `lorestore` for package, CLI, and directory names.
  GitHub: `lorestore-dev/lorestore`.

## Design decisions the author owns

Order inversions (§6.8), divergence conflicts (§6.6), and hidden canon (§6.12) are always
the author's decision; agents surface them but never resolve them.
