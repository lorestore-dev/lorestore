---
id: extraction
kind: chain
context: package
---
# Workflow: extraction

Builds or grows one package from source texts (§13.6). Phase 1 emits dated fragments,
one per source unit, with no contention; phase 2 assembles history from them, one
writer per output file.

## Steps

| Step | Agent              | Reads                                                                                                                                                 | Writes                                 | Gate      | Repeat     | Parallel |
| ---- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | --------- | ---------- | -------- |
| F0   | worldbuilder       | `package.yaml`; a listing of `texts/`; `bible/sources.md`                                                                                             | `bible/canon-timeline.md` (ruler mode) | milestone |            |          |
| F0b  | character-designer | a listing of `texts/`; a cast list, if a human gives one; the lower layers' rosters                                                                   | `bible/characters/_roster.md` (seed)   | milestone |            |          |
| F1   | extractor          | `texts/<work>/<unit>`; `bible/canon-timeline.md`; `bible/characters/_roster.md`; `bible/sources.md`; `bible/glossary.md`                              | `extractions/<work>/ch<NN>.md`         |           | per-unit   | yes      |
| F2a  | merger             | the `New names` of every record; `bible/characters/_roster.md`; `bible/sources.md`                                                                    | `bible/characters/_roster.md`          | milestone |            |          |
| F2b  | merger             | the rows of every record whose `Target` is `<target>`; `bible/<target>`; `bible/canon-timeline.md`; `bible/characters/_roster.md`; `bible/sources.md` | `bible/<target>`                       |           | per-target | yes      |
| F3   | theorist           | `bible/theories.md`; the slices of the relied-on packages each theory draws on; `bible/canon-timeline.md`; `bible/sources.md`                         | `bible/theories.md`                    |           |            |          |
| F4   | `indexer`          | the package's files                                                                                                                                   | `bible/index.md`                       | milestone |            |          |

## Notes

- Before F0, a human creates `package.yaml` (its `kind`, its `relies-on` pins, and
  `status: open-for-extraction`) and registers the package's own sources in
  `sources.md`.
- **F0** runs for a base; for an adaptation, writing `## Works` and `## Adapts`; and for
  an official or fanfic package with works of its own, writing `## Works` and
  `## Insert`. Other packages skip it. In a world with a calendar it writes `## Dates`,
  and MAY re-run after F1 to add the dates the records give.
- **F0b** seeds only the entities that are new in the package, outside a base.
- Outside a base, extractors and mergers read the relied-on packages as lower layers,
  and a fact about an entity one of them defines goes in an extension sheet.
- **F2a** merges the roster first. Its gate is where a human resolves the extractors'
  `Needs a human` items.
- **F2b** runs one instance per target named in any record's `Target` column.
- **F3** runs only in a `theories` package.
- After F4, a human bumps `version` and, when extraction is complete, sets
  `status: locked`.
- To grow a package, run F1 for the new units, then F2a onwards. F0 re-runs only if
  new works join the ruler.
