# LoreStore: notes for Claude

This repository is the LoreStore specification (draft 0.3): a file-based, model-agnostic
canon store for fiction, plus the agent framework that reads and writes it. It holds the
spec, not an implementation.

## Where things are

- `spec/01-…14-…md`: the specification. Each concept is defined in one chapter and
  referenced elsewhere with `§`. Change a rule where it is defined.
- `spec/03-layers.md` §3.3 (the file catalog) is the authority on who writes each file.
- `schemas/`: JSON Schemas for `project.yaml`, `package.yaml`, `universe.yaml`.
- `examples/`: abridged Harry Potter and Star Trek packages under
  `worlds/<fandom>/<package>/` (each base in `base/`), a crossover universe, and eight
  projects. `examples/README.md` lists the numbered cases and their expected results.
- `DECISIONS.md`: decisions D1 onwards, newest first. Add an entry for every rule change.
- `tools/check.py`: the conformance checker.

## Working rules

- After changing a rule, schema, or example, run the checker; it must report
  `FAILURES: 0`:
  `pip install -r tools/requirements.txt && python tools/check.py`
- If a change adds behavior to the data model, add checks for it to `tools/check.py` and
  the expected result to `examples/README.md`.
- A new case in `examples/README.md` starts with an anchor, `<a id="case-<id>"></a>`, and
  the spec section it shows off ends with an `**Example cases:**` line linking to it.
  Link § citations in `examples/README.md` to their headings.
- Check that every `§` reference and relative link resolves, and every case is linked
  from the spec: `python tools/refs.py`.
- Example facts are recorded in our own words with citations; never copy source text.
- Prose style: plain English, RFC 2119 keywords in capitals. Match the existing
  spelling, which is mostly American ("-ize", "catalog").
- Name: "LoreStore" in prose; `lorestore` for package, CLI, and directory names.
  GitHub: `lorestore-dev/lorestore`.

## Design decisions the author owns

Order inversions (§6.8), divergence conflicts (§6.6), hidden canon (§6.12), theory
conflicts (§6.13), seam conflicts (§6.14), and accepting a chronology contradiction in a
project (§4.13) are always the author's decision; agents
surface them but never resolve them. So are sending a chapter to early access and
releasing it (§13.9, §13.3). In a project that lists `authors`, any listed author may
make these decisions (§11.13).
