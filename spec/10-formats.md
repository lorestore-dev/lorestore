# 10. File formats

This chapter defines the exact structure of every file a host needs to parse. Prose
sections (a character's backstory, a place's description) are free-form. The structures
below are what tools rely on.

## 10.0 Conventions

**Manifests** are YAML 1.2. Each has a JSON Schema in [`schemas/`](../schemas/).

**Spec versions.** Every manifest (`project.yaml`, `package.yaml`, `universe.yaml`)
declares `spec_version`: the `<major>.<minor>` of this specification whose rules its
directory follows. This document is version `0.3`.

- A host MUST list the spec versions it supports, and MUST refuse a stack that holds a
  manifest of any other version, naming it.
- One stack MAY mix versions that the host supports. The host reads each directory by
  the rules of its own version: a feature that version lacks is absent there (a `0.2`
  base has no calendar).
- Before `1.0`, any minor version may break the one before it, so a host supports each
  version deliberately. From `1.0` on, a minor version only adds, and a host that
  supports `1.n` reads every `1.m` with `m` up to `n`.
- Moving a directory to a new spec version is a human change: set `spec_version` and
  make the changes that `DECISIONS.md` lists for the versions in between. In a package,
  it bumps the version (§2.8).

**Structured markdown** uses two forms:

- **Tables.** A table is identified by the `##` heading it sits under and by its
  required header cells, which MUST appear in the order given, spelled exactly as
  given. A file MAY add columns **after** the required ones. Parsers MUST ignore columns
  they do not know.
  - An added column SHOULD be registered in the `## Columns` table of `index.md`
    (§10.3), which says what it means and what values it takes. A host SHOULD warn
    about an added column that is not registered.
  - An agent that reads a table also reads the registry rows for it, and treats each
    registered column as part of the table's meaning. The file's writer (§3.3) fills
    registered columns as part of its normal step; registering a column never adds a
    second writer.
  - Escape a literal `|` inside a cell as `\|`.
  - An empty cell means "not given". The token `—` (em dash) means "explicitly none".
  - Multiple values in one cell are separated by `; `.
- **Entry blocks.** For records with long text, each entry is a `###` heading of the
  form `### <ID> — <Name>`, followed by a list of `- <key>: <value>` lines. Free prose
  MAY follow the list. Unknown keys MUST be ignored.

**Front matter.** A file MAY begin with a YAML front-matter block (`---` … `---`). Where
this chapter requires front matter, its keys are listed.

**Common cell types:**

| Type        | Form                                                                        |
| ----------- | --------------------------------------------------------------------------- |
| id / slug   | `^[a-z0-9]+(-[a-z0-9]+)*$`                                                  |
| attribute   | kebab-case, for example `blood-status`                                      |
| point       | a ruler point, `work{:index}[+HH:MM:SS[.f]]` (§4.2), or empty when timeless (§4.7) |
| source      | a source id registered in the row's own package's `sources.md` (§5.1), or a reserved id |
| citation    | free text that locates the evidence, for example `PS ch.6` or `TNG "Q Who"` |
| chapter     | a manuscript chapter id, `chapter-<NN>`                                     |
| date        | an in-world date in the stack's calendar, such as `1991-07-31`, `..1991`, or `~1975` (§4.13) |
| duration    | a length of in-world time, such as `3d`, `4d..6d`, or `~8h` (§9.4)          |

**Example cases:** [25](../examples/README.md#case-25).

## 10.1 `project.yaml`

Schema: [`schemas/project.schema.json`](../schemas/project.schema.json).

```yaml
spec_version: "0.3"
id: two-witnesses
name: "Two Witnesses"
workflow: novel                 # novel | short-story | serial
gates: milestones               # none | milestones | all
seed: "Cedric survives the graveyard, and Harry is no longer the only witness to Voldemort's return."
parameters:
  pov: third-limited
  tense: past
  target_length: 90000          # words
  viewpoints: chapter           # none (default) | chapter | scene (§7.7)
  told_from: end                # optional: a chapter id or end, for a narrator looking back (§7.7)

layers:                         # from the base up; absent or empty = self-contained
  - harry-potter@3.2.1
  - harry-potter/fanon@1.0.4
  - harry-potter/fanfic/example@1.2.3
resolution: recency             # precedence (default) | recency | fill

setting:
  type: established             # original | established
  fidelity: flexible            # strict | flexible | au   (established only)
  fidelity_notes: "The rules of magic and the Ministry's politics are load-bearing."
  cutoff: "GoF:37"              # the default cutoff, on the stack's ruler (§4.12)
  follow: retelling             # retelling (default) | branch   (established only)
  divergence_point: "GoF:32"    # required for a branch; recommended for a retelling
  temporal_model: linear        # linear | frames

modules:
  litrpg: false
  languages: false
  travel: false
  mysteries: false
  lineage: false

authors:                        # optional: who makes the author's decisions (§11.13)
  - id: ade
    name: "Ade"
  - id: kit
    name: "Kit"

content_notes:                  # optional: the content notes chapters may carry (§13.11)
  death: "The death of a character"
  grief: "Grief and mourning"

publishing:                     # optional: what the export's metadata says (§13.13)
  summary: "Cedric lives, and Harry is no longer the only one who saw."
  rating: teen                  # free text, in the author's words or a site's
  language: en                  # BCP 47
  tags: [hurt/comfort, canon divergence]
  relationships: [harry-potter+cedric-diggory]
  scene_break: "* * *"          # optional; the default
```

- `authors`: optional. Each entry has an `id` (§10.0), unique in the list, and a
  `name`. Absent means one author, unnamed. With two or more, every record of an
  author's decision names who made it (§11.13).
- `content_notes`: optional. A map from a note's id (§10.0) to what it warns of, in
  the words readers will see. Absent means the project does not track content notes,
  and its chapters MUST NOT carry them (§13.11).
- `publishing`: optional. Without it, the export writes clean chapters but no metadata
  (§13.13). `summary`, `rating`, and `tags` are the author's words, copied as they are.
  `language` is a BCP 47 tag. `relationships` lists pairs of slugs in the stack's
  roster: `a+b` for a friendship or other bond, `a/b` for a romance, as fan sites write
  them. `scene_break` is the line that stands between scenes in an exported chapter.
- `layers`: layer references, from the base up (§2.2): `<package-id>@<version>`,
  `universe:<id>@<version>`, or `project:<id>@chapter-<NN>`. The project itself is the
  implicit top layer.
- `resolution`: how rows from different layers combine (§5.4).
- `setting` holds the project's adherence settings (§6.3). In an established world it
  MAY also hold `order`, the project order: a list of every segment of the stack's ruler
  (the base's, or the series ruler, §4.12), inserted segments included, each once
  (§6.8). Absent means the ruler's order. An original setting has no layers (§6.1), and
  `fidelity`, `fidelity_notes`, `follow`, `divergence_point`, `cutoff`, and `order`, and
  their universe maps, are invalid in it (§4.7). An original project MAY declare
`calendar` and `notation` (§4.13), at the top level, as a base does (§10.2). They are
invalid in an established project, which dates in its stack's calendar.

A serial project (`workflow: serial`) MAY add:

```yaml
serial:
  released: revisable           # locked (default) | revisable
```

The `serial` block is invalid for any other workflow (§13.3).

A project with a universe layer replaces `cutoff`, `divergence_point`, and `order`
with `cutoffs`, `divergence_points`, and `orders`, maps keyed by base id (§7.4).
`orders` lists only the bases the project reorders. Without a universe
layer, the maps are invalid.

Overlay workflows are derived, not configured: `setting.type: established` applies
the established-world overlay, and `temporal_model: frames` applies the frames overlay
(§13).

## 10.2 `package.yaml`

Schema: [`schemas/package.schema.json`](../schemas/package.schema.json).

Every package has one, in the package's folder:

```yaml
spec_version: "0.3"
id: harry-potter/fanon          # <fandom> | <fandom>/<package> | <fandom>/fanfic/<work>
kind: fanon                     # base | official | adaptation | fanon | fanfic | theories
name: "Harry Potter fanon"
version: 1.0.0
status: open-for-extraction     # open-for-extraction | locked
relies-on:                      # pinned; empty for a base package
  - harry-potter@3.2.1
license: CC-BY-4.0              # optional: an SPDX license expression (§2.10)
credit: "Compiled by the fans of the example"   # optional: how to credit the makers
```

- `id` MUST match the package's folder (§2.3). A `base` package's id is the bare fandom
  id, and it relies on nothing. Every other kind relies on at least its base.
- `relies-on` lists `<package-id>@<version>` pins. Every entry MUST appear below the
  package in any stack that uses it (§2.2).
- The tiers a package may register depend on its kind (§2.3, §5.2).
- `license` and `credit` are optional (§2.10). `license` MUST be a valid SPDX license
  expression; a `LicenseRef-<id>` in it needs a `LICENSE.md` beside the manifest.
- A `base` package MAY declare its world's calendar (§4.13): `calendar: iso`, with an
  optional `notation`, or a custom calendar. Both keys are invalid in every other kind.

```yaml
calendar: iso
notation: gregory               # optional; a BCP 47 calendar identifier, iso only
```

### 10.2.1 `universe.yaml`

Schema: [`schemas/universe.schema.json`](../schemas/universe.schema.json). Example in
§8.1. `kind` is always `universe`; `relies-on` pins two or more bases; `offsets` is
keyed by base id. The bridge's source id is the reserved `bridge`, tier `crossover`.
`license` and `credit` are optional, as in `package.yaml` (§2.10).

## 10.3 `index.md`

```markdown
## Files
| Path           | Layer | Holds                                   |
| -------------- | ----- | --------------------------------------- |
| world.md       | world | Setting, era, rules and systems         |
| magic/spells.md | world | Spell catalog                          |
```

`Path` is relative to the package or project the index lives in. `Layer` is one of the
layers in §3.2. Every world-layer file in a package, and every file in a project's own
`bible/`, MUST be listed. Each layer lists only its own files; the composed bible's
index is their union (§2.7).

An optional `## Columns` table registers the columns an author has added to tables
(§10.0):

```markdown
## Columns
| File         | Table   | Column | Meaning                                          | Values    |
| ------------ | ------- | ------ | ------------------------------------------------ | --------- |
| timelines.md | ## Legs | Notes  | Why the leg is dated as it is, for human readers | free text |
```

- `File` is a path in the same package or project as the index. Each layer registers
  columns only in its own files. Like `## Files`, the table is read as a union (§2.7).
- `Table` is the `##` heading the table sits under.
- `Values` is `free text`, a cell type from §10.0 (`slug`, `point`, `chapter`, …), or an
  enumeration written `a | b | c` (escaped as `a \| b \| c` inside the cell).
- A column name MUST NOT repeat a required column of its table.

**Example cases:** [25](../examples/README.md#case-25).

## 10.4 `canon-timeline.md` (the ruler)

```markdown
## Works
| Work | Title               | Levels                   | Timed level | Notes |
| ---- | ------------------- | ------------------------ | ----------- | ----- |
| PS   | Philosopher's Stone | chapter › scene          |             |       |
| TOS  | The Original Series | season › episode › scene | episode     |       |

## Order
| Order | Segment | Title               | Children | Notes |
| ----- | ------- | ------------------- | -------- | ----- |
| 1     | PS      | Philosopher's Stone | 17       |       |

## Counts
| Node    | Children |
| ------- | -------- |
| TOS:3:2 | 14       |
```

- `Work`: unique. Matches `^[A-Za-z][A-Za-z0-9-]*$`; case is preserved, for familiar
  abbreviations.
- `Levels`: level names from the top down, separated by `›`. A work with no levels
  (`Levels` empty) cannot be divided.
- `Timed level`: one of the work's level names, `work` (the work itself is timed, as in
  a film), or empty (not timed).
- `Order`: a positive integer, unique, with no gaps.
- `Segment` and `Node`: a path, `work{:index}`, with no timecode.
- `Children`: an integer, empty, or `—` (§4.1).
- `## Counts` is optional. A node in it must lie inside a segment.

An **adaptation** package's `canon-timeline.md` has no `## Order` or `## Counts`. It
has a `## Works` table listing its own works, each with `Timed level: work`, and an
`## Adapts` table (§4.9):

```markdown
## Adapts
| Work    | From | To    | Notes |
| ------- | ---- | ----- | ----- |
| PS-film | PS:1 | PS:17 |       |
```

- `Work`: a work in the adaptation's own `## Works` table.
- `From` and `To`: points on the base's ruler, with no timecode. The row covers every
  path from `From` to `To`, inclusive. A work MAY have several rows, one per contiguous
  range, when it takes scenes out of the base's order. Ranges of different works MAY
  share a node only if each covers it at a finer level (a chapter split between two
  films is mapped scene by scene).

An **official** or **fanfic** package that inserts works (§4.10) has a `## Works` table
for its own works, in the base's format, and an `## Insert` table in place of `##
Order`:

```markdown
## Insert
| Segment | After | Title                         | Children | Notes |
| ------- | ----- | ----------------------------- | -------- | ----- |
| TAS:1   | TOS:3 | The Animated Series, season 1 | 16       |       |
```

- `Segment`: a path on one of the package's own works.
- `After`: a segment of the base's `## Order`, or one inserted by an earlier row or a
  lower layer, or `—` for before every segment.
- `Children`: as in `## Order`. A `## Counts` table MAY follow, for nodes inside
  inserted segments.

A later book in a series begun by a self-contained book (§4.12) has the same two tables
in its own `bible/canon-timeline.md`. Its `After` may also name the work of a project
layer.

Any `canon-timeline.md` except an adaptation's MAY add a `## Dates` table, which dates
its own nodes in-world (§4.13), and an `## Accepted` table (§10.5) for the dates that
contradict their parents on purpose:

```markdown
## Dates
| Node | Date       | Notes                                     |
| ---- | ---------- | ----------------------------------------- |
| PS   | 1991..1992 |                                           |
| PS:1 | 1981-11    | The night Harry is left with the Dursleys |

## Accepted
| Check          | Subject | Reason                                                | Citation |
| -------------- | ------- | ----------------------------------------------------- | -------- |
| outside-parent | PS:1    | The first chapter is set ten years before the rest    | PS ch.1  |
```

- `Node`: a path on one of the file's own works (the base's, or the works the file
  inserts), with no timecode. A node appears at most once.
- `Date`: a date (§10.0).

## 10.5 State histories

**Single-entity files** (a character sheet) hold one table:

```markdown
## State history
| Attribute | Value | As of | Source | Citation |
```

**Multi-entity files** (`world.md`, `places.md`, `society.md`, `culture.md`) add an
entity column:

```markdown
## State history
| Entity | Attribute | Value | As of | Source | Citation |
```

`Entity` is an id unique within the file.

**`relationships.md`:**

```markdown
## State history
| Pair                      | Attribute | Value         | As of | Source | Citation |
| ------------------------- | --------- | ------------- | ----- | ------ | -------- |
| harry-potter+ron-weasley  | bond      | strangers     | PS    | books  | PS ch.1  |
| harry-potter+ron-weasley  | bond      | acquaintances | PS:6  | books  | PS ch.6  |
| harry-potter+ron-weasley  | bond      | friends       | PS:10 | books  | PS ch.10 |
```

`Pair` is two slugs joined by `+`, in alphabetical order.

**`knowledge.md`:**

```markdown
## Secrets
| Secret | Truth | Source | Citation |

## Knowledge
| Character | Secret | State | As of | Source | Citation |
```

`State` is `unaware`, `suspects`, or `knows`.

**Character sheets** (`characters/<slug>.md`) require front matter and a state
history. Narrative sections are free-form but SHOULD include the headings shown:

```markdown
---
slug: harry-potter
name: Harry Potter
origin: canon          # canon | original | crossover
---
## Voice signature
## Wants and needs
## Arc
## State history
| Attribute | Value | As of | Source | Citation |
```

**In-world dates** (§4.13). Any state-history table above MAY add an `In-world`
column, after `True from`: a date (§10.0), on which the fact became true. The optional
columns come in the order `True from`, `In-world`, `From chapter`, and any of them MAY
be left out. A row whose attribute is `born`, `died`, or an event's `date` leaves
`In-world` empty.

**`history.md`** (world history, §4.13) is a multi-entity state history whose entities
are events:

```markdown
## State history
| Entity               | Attribute    | Value                                          | As of | Source | Citation |
| -------------------- | ------------ | ---------------------------------------------- | ----- | ------ | -------- |
| grindelwald-defeated | date         | 1945                                           | PS:6  | books  | PS ch.6  |
| grindelwald-defeated | summary      | Dumbledore defeats the dark wizard Grindelwald | PS:6  | books  | PS ch.6  |
| grindelwald-defeated | participants | albus-dumbledore; gellert-grindelwald          | PS:6  | books  | PS ch.6  |
```

`Entity` is an event id (§10.0). Every event MUST have a `date` row; `date`, `summary`,
and `participants` (slugs) are reserved, and other attributes are free.

**`## Accepted`** excuses a chronology contradiction that the story means (§4.13). It
MAY follow the table it excuses, in `canon-timeline.md` or in any state-history file:

```markdown
## Accepted
| Check     | Subject | Reason                                           | Citation |
| --------- | ------- | ------------------------------------------------ | -------- |
| born-died | born    | Born in 2051, she travels back and dies in 1990  | EP:4     |
```

- `Check`: `outside-parent`, `in-world-after`, or `born-died` (§4.13); or, with the
  lineage module, `born-before-parent` or `ancestry-cycle` (§9.6).
- `Subject`: for `outside-parent`, the node. Otherwise the row's key: its attribute in
  a single-entity file, or `<entity>.<attribute>` in a multi-entity one (the `born`
  attribute, for `born-died` and `born-before-parent`; any `parents` or
  `descends-from` row on the cycle, for `ancestry-cycle`).
- `Reason`: free text, required.
- `Citation`: required in a package, where the acceptance records what the source does.
  In a project, it MAY be empty.
- `By` (optional column, last; projects only): the author who accepted it, an id from
  `authors`. Required in a project with two or more authors (§11.13).

An original character (`origin: original`) uses project-defined sources. Its rows MAY
leave `As of` empty, and use `Source: project`.

**Story-dated rows** (§4.11). A project's rows about its own entities MAY add a
`From chapter` column, last, in any of the tables above. It holds the chapter id from
which the row holds. A row with a `From chapter` MUST cite `project` and leave `As of`
empty.

An **extension sheet** (§2.7) adds a package's rows to a character defined in a lower
layer. Its front matter holds only the slug and the package that defines it, and it
has no roster row of its own:

```markdown
---
slug: daphne-greengrass
extends: harry-potter
---
## State history
| Attribute | Value     | As of | Source      | Citation              |
| --------- | --------- | ----- | ----------- | --------------------- |
| house     | Slytherin | PS:7  | conventions | common fan convention |
```

## 10.6 Extraction record

`extraction/<pkg>/extractions/<work>/ch<NN>.md` is one record per source unit:

```markdown
---
package: harry-potter  # the package being extracted
point: PS:6            # the unit this record covers, on the base's ruler
source: books
text: texts/ps/ch06.md
---
## Facts
| Target | Entity | Attribute | Value | As of | Source | Citation | Change | True from |

## New names
| Name | Proposed slug | Context | Citation |

## Quotations
| Line | Speaker | Rank | As of | Citation |

## Needs a human
- <question>
```

- `Target`: the world-layer file the fact belongs in, for example
  `characters/harry-potter.md`. For a character a lower layer defines, the target is the
  package's extension sheet.
- `Entity`: the slug or entity id (empty for a single-entity target).
- `Change`: `new`, `change`, or `confirm`.
- `True from` (optional): when the fact became true, if the passage reveals backstory
  (§4.4). An `In-world` column (optional) MAY follow it, with the date (§4.13).
- The front matter MAY add `date`: the in-world date of the unit, if the source gives
  it, for the ruler's `## Dates` (§13.6).
- `Rank`: 1 (most important) to 5.

## 10.7 `sources.md`

```markdown
## Sources
| ID    | Tier    | Title                   | Author / origin | Notes |
| ----- | ------- | ----------------------- | --------------- | ----- |
| books | primary | The seven novels        | J. K. Rowling   |       |

## Bibliography
### books — The seven novels
- author: Rowling, J. K.
- year: 1997–2007
- publisher: Bloomsbury
```

Bibliography keys: `author`, `year`, `title`, `container`, `volume`, `issue`, `pages`,
`doi`, `url`, `edition`, `publisher`.

## 10.8 `divergences.md`

```markdown
## Divergences
| ID | Canon establishes | This story changes it to | Overrides | Kind | First occurs |

## Consequences
| Divergence | Consequence | Status | Absorbed in |

## Hidden canon
| Entity | Attribute | Revealed at | Decision | Divergence | Decided in | Note |

## Theory conflicts
| Theory | Claim | Evidence | At | Decision | Note |

## Seam conflicts
| Item | Decision | Divergence | Decided in | Note |
```

- `ID`: `D<n>`, never reused.
- `Overrides`: `<slug>.<attribute>=<value>` assignments, separated by `; `, or `—`. The
  value may be `(unset)`, which makes the attribute absent.
  For a relationship, use the pair as the slug (`harry+ron.bond=rivals`). In a
  project with a universe layer, qualify each slug by its base
  (`harry-potter:harry-potter.house=Ravenclaw`, §8.3).
- `Kind`: `planned` or `emergent`.
- `First occurs`: a chapter id.
- `Until` (optional column, after `First occurs`): the chapter id from which the
  divergence stops applying. It MUST be after `First occurs`. Empty means permanent.
- `Basis` (optional column, after `First occurs` and `Until`): the theory a divergence
  adopts, as `<package-id>:<theory id> (claims <n>, <n>, …)`, or `(claim <n>)` for one
  (§6.13). The package MUST be in the stack, and every claim MUST exist.
- `Divergence` in `## Consequences`: a divergence id, or `<project-id>:<id>` for an
  earlier book's divergence the project honors (§6.4).
- `Status`: `open`, `absorbed`, or `accepted`. `Absorbed in` is a chapter id, required
  when absorbed. `accepted` (serials with locked releases only, §13.3) means the author
  accepts an inconsistency in a released installment. It requires an optional `Note`
  column, after `Absorbed in`, saying why.
- `## Hidden canon` (optional section, §6.12): one row per hidden truth the author has
  decided about. `Revealed at` is the canon row's `As of`. `Decision` is `reveal-early`,
  `keep-hidden`, or `other`. `Divergence` is the ID of the divergence a `reveal-early`,
  or an `other` that changes canon state, produced, or `—`. `Decided in` is the chapter
  being written when the decision was made. `Note` is required for `other`.
- `## Theory conflicts` (optional section, §6.13): one row per piece of evidence against
  a claim of a theory the project adopts or considered adopting. `Theory` is
  `<package-id>:<theory id>`. `Claim` is the claim's number. `Evidence` says, in the
  curator's own words, what contradicts the claim and where. `At` is the ruler point of
  the evidence, before or after the cutoff. `Decision` is `keep`, `adapt`, or
  `discard`. `Note` is required for `adapt`, and says how the claim changed.
- `## Seam conflicts` (optional section, §6.14): one row per seam the author has
  decided. `Item` is an earlier book's item, or a pattern of them:
  `<project>:D<n>`, `<project>:<slug>.<attribute>`, or
  `<project>:<slug>.<attribute>@<chapter>`, with `*` in place of a whole slug,
  attribute, chapter, or divergence number; or, for a value seam,
  `<slug>.<attribute>`. `Decision` is `carry-back`, `not-yet`, or `other` for an
  item, and `keep-earlier`, `accept`, or `other` for a value seam. `Divergence` is the
  ID of the divergence a `keep-earlier` or `other` produced, or `—`. `Decided in` is
  the chapter being written when the decision was made. `Note` is required for
  `other`.
- `By` (optional column, last, in every table of the file): the author who made the
  decision the row records, an id from `authors` (§11.13). In a project with two or
  more authors it is required on every row of `## Hidden canon`, `## Theory conflicts`,
  and `## Seam conflicts`, and on every `accepted` consequence. A divergence logged to
  carry out an author's decision (an order inversion or a divergence conflict) SHOULD
  name the author too.

## 10.9 `characters/_roster.md`

```markdown
## Characters
| Slug | Name | Origin | Aliases | Reveal of | Revealed at | Version of |
```

- `Aliases`: other names that refer openly to this character.
- `Reveal of` and `Revealed at`: for a **reveal alias**, a surface identity that is
  secretly someone else. The surface identity gets its own row and its own slug, and
  facts are filed under it. `Reveal of` names the true slug, and `Revealed at` is the
  ruler point from which the identity is known. Extractors MUST NOT file facts under the
  true slug before the reveal, because that leaks it.
- The snapshot never joins a reveal alias to its true identity (§7.3); agents do.
- `Version of`: for a **version**, a canon-distinct instance of one identity (an
  alternate-universe self) with its own sheet. A time-traveling copy is not a version;
  it stays on one sheet.

**Example cases:** [7](../examples/README.md#case-7), [10](../examples/README.md#case-10).

## 10.10 `glossary.md`

```markdown
## Terms
| Term | Meaning | Kind | Source | Citation |
```

`Term` is the canonical spelling every agent MUST use.

## 10.11 Catalogs (`magic/*.md`, `technology.md`, `game-system.md`, other catalogs)

One entry block per item. The same fields serve magic and technology: each system
states what it does in theory, how it behaves in practice, and its **cost** and
**limit**.

```markdown
### expelliarmus — Disarming Charm
- effect: disarms the target (the theory)
- practice: can also throw the target backwards; reliable in duels
- definition: defined            # defined | partial | named-only
- cost: —
- limit: line of sight
- as-of: CoS:11
- source: books
- citation: CoS ch.11
```

```markdown
### transporter — Transporter
- effect: converts a person or object to energy and rematerializes it elsewhere
- practice: routine crew transport; malfunctions are rare but dramatic, e.g. an ion
  storm sends a landing party to a parallel universe (TOS "Mirror, Mirror")
- definition: partial
- cost: ship's power
- limit: cannot beam through raised deflector shields; limited range
- as-of: TOS
- source: canon
- citation: TOS, recurring
```

A catalog entry that changes over time adds a `## State history` table (§10.5,
multi-entity form) at the end of the file, keyed by the entry's id.

`magic/artifacts.md` also holds an **ownership ledger**: a state history whose
attribute is `owner`. For example, the Elder Wand's allegiance passes from Dumbledore to
Draco at `HBP:27` and to Harry at `DH:23`. Those rows are true from those points even
though the characters only work it out much later. Who knows what, and when, belongs in
`knowledge.md` (§10.5), not in the ownership rows.

## 10.12 `lang/<language>.md`

```markdown
## Dictionary
| Term | Meaning | Part of speech | Source | Citation |
```

## 10.13 `theories.md` and `quotations.md`

`theories.md` lives in a `theories` package (§2.3). Theories are entry blocks:

```markdown
### T3 — <short claim>
- kind: reading-beyond-text          # authorial-intent | reading-beyond-text
- confidence: plausible              # speculative | plausible | well-supported
- status: open                       # open | supported | contradicted | retired
- source: fan-community              # a theory-tier source in this package
- earliest-reference: —              # where the theory was first seen, if known
- claim-1: <one checkable claim>
- claim-2: <another>
- evidence: PS:6 (PS ch.6); CoS:17 (CoS ch.17)
- falsifier: <what would refute it>

<reasoning, in prose>
```

- `claim-<n>` keys number the theory's claims from 1. A project adopts claims by number
  (§6.13), so a claim's number never changes; a retired claim keeps its number and
  says so.
- `source` names a `theory`-tier source in the package's `sources.md`: the theorist, a
  credited fan author, or "the fan community (origin untraced)" (§5.6).

Quotations:

```markdown
## Quotations
| ID | Line | Speaker | Rank | As of | Source | Citation |
```

- `ID`: names one quotation. A file MAY give a quotation several rows, from different
  sources or as-ofs, as an attribute has a history. A row in a higher layer whose `ID`
  is qualified,
  `<package-id>:<ID>`, gives that lower package's quotation another row rather than
  defining a new one (§2.7): a film re-attributing a line, say. Its `Line` or `Speaker`
  MAY be empty, meaning the row says nothing about that column.
- `Speaker` and `Line` resolve across the stack by the project's resolution mode, each
  like an attribute (§5.4). A package holds at most one row per quotation, column,
  tier, and as-of (§4.4); a corrected line's error is an erratum row (§5.2).
- `quotations.md` is a package file. A project has none: its own lines are in its
  manuscript, and a later book reads an earlier book's lines there, through the project
  layer (`manuscript/@<project>/…`, §2.6).

**Example cases:** [3a](../examples/README.md#case-3a).

## 10.14 `bridge.md`

```markdown
## Concept mappings
| Concept | Relation | Concept | Rule |
| ------- | -------- | ------- | ---- |
| harry-potter:magic | ∥ | star-trek:technology | Spells do not register on sensors; a tricorder reads a wizard as baseline human |
| harry-potter:muggle | ≡ | star-trek:human | A Muggle is any non-magical human |

## Crossover canon
| Entity | Attribute | Value | As of | Source | Citation |

## Collisions
| Name | Resolves to | Rule |

## Consistency rules
- <rule>

## Open questions
- <question>
```

`## Open questions` (optional) lists what the bridge-builder could not settle, for the
human at the gate (§12.19). Concepts and entities are base-qualified (`<base-id>:<id>`). Crossover canon rows use
source `bridge`. `As of` in crossover canon is a ruler point qualified by world
(`harry-potter:HBP:7`) or empty.

## 10.15 `timeline.md` (story time)

```markdown
## Events
| Chapter | Story time | Event | Entities |
```

Rows are in manuscript order. `Story time` is free text (an in-world date or "three
days later"). `Entities` lists the slugs involved. Two optional columns MAY follow the
required ones, in this order: in a stack with a calendar, `Date`, holding the event's
date (§4.13) when it is known; and with the travel module, `Place`, the id in
`places.md` of where the event happens (§9.4).

## 10.16 `timelines.md` and `branches.md` (frames)

```markdown
## Legs
| Traveler | Leg | Mechanism | Departs | Arrives | Personal cutoff | Chapter |

## Ripples
| Traveler | Attribute | Value | Caused at | Chapter |
```

`Mechanism` is the id of an entry in `time-travel.md` (§10.24). `Departs`, `Arrives`, and
`Caused at` are world points (`<point>@<branch>`). `Personal cutoff` is the latest point
the traveler has lived through, which bounds what they know. A ripple applies from its
`Chapter` onwards. `## Ripples` is required only when a leg uses a `feedback` mechanism.

```markdown
## Branches
| Branch | Splits from | At | Cause | Mechanism | Status |

## Paradoxes
| ID | Description | Decision | Rationale | Chapter |
```

- The default branch is `main`, which has no `Splits from`, `At`, or `Mechanism`.
- `Mechanism` is the `time-travel.md` entry that created the branch, or `—` for a
  branch that no mechanism created (a parallel universe the story reaches some other
  way).
- `Status` is `live`, `overwritten` (a `mutable` or `feedback` branch has replaced it,
  or it has been restored over), or `abandoned` (an earlier iteration of a `loop`).
- `Decision` is `fixed` or `accepted`.

## 10.17 `game-state.md`

```markdown
## State history
| Chapter | Attribute | Value | Change | Cause |
```

`Attribute` covers stats (`stat.strength`), level (`level`), inventory
(`inventory.<item>`, value = quantity), skills (`skill.<id>`), and quests
(`quest.<id>`, value = stage). `Change` is the signed delta where numeric.

## 10.18 Manuscript chapters

```markdown
---
chapter: 7
title: "The Long Road South"  # optional: the chapter's title, as readers see it
status: drafted         # drafted | line-edited | final | early-access | released | withdrawn
early-access: 2026-10-27  # set by the release skill when the chapter goes to early readers
released: 2026-11-03    # serial only: the first release, set by the release skill
re-released: 2026-11-20 # serial only: the latest re-release, if any
withdrawn: 2026-12-01   # serial only: when the author took it down, if they did
release-on: 2026-11-03T18:00+00:00  # a scheduled release, until it is carried out
---
```

- Every date key holds a date (`2026-11-03`). `release-on` and `early-access-on`, the
  schedule keys, MAY hold a date and time with its offset, as fan sites schedule posts.
- The release skill writes every key above except `chapter` and `title`; the drafter
  writes `title`, and the line-editor may polish it (§13.12).
- With two or more authors (§11.13), the release skill also records who took each
  step: `early-access-by`, `released-by`, `re-released-by`, and `withdrawn-by`, and,
  for a schedule, `early-access-on-by` or `release-on-by`. Each is an id from `authors`.

**Content notes** (§13.11). In a project with `content_notes`:

```yaml
content-notes-suggested: [death, new:violence]   # set by the line-editor
content-notes: [death]  # set by the release skill, from what the author confirms
```

- `content-notes-suggested`: ids from `content_notes`, or `new:<id>` for a note the
  list lacks.
- `content-notes`: ids from `content_notes` only. An empty list (`[]`) means the
  author confirmed that the chapter needs none. Required on every chapter that is
  `early-access`, `released`, or `withdrawn`, or scheduled for either step.
- In a project without `content_notes`, both keys are invalid.

| Status         | Meaning                                                                      | Workflows       |
| -------------- | ---------------------------------------------------------------------------- | --------------- |
| `drafted`      | Written, not yet polished                                                    | all             |
| `line-edited`  | Polished and approved. In a serial, **ready**: waiting in the buffer (§13.3) | all             |
| `final`        | Approved as finished                                                         | novel, short story |
| `early-access` | Read by early readers (beta readers, patrons, advance copies), still editable (§13.9) | all     |
| `released`     | Published to everyone                                                        | serial          |
| `withdrawn`    | Released, then taken down by the author (§13.12)                            | serial          |

- A chapter moves `drafted` → `line-edited` → (`early-access`) → `released` in a serial,
  and `drafted` → `line-edited` → (`early-access`) → `final` otherwise. Early access is
  optional. A released chapter MAY move to `withdrawn`, and back to `released`.
- Moving a chapter to `early-access`, `released`, or `withdrawn` is always the author's
  decision (§13.12).
- **Both happen in order.** Released chapters, counting withdrawn ones, form an
  unbroken run from chapter 1, and early-access chapters form an unbroken run straight
  after them: no chapter is `released` while an earlier one has never been, and none is
  `early-access` while an earlier one is still unreleased and not in early access.
- `early-access` and `released` record the date of each step, and are never
  overwritten. A released chapter keeps its `early-access` date if it had one, and a
  withdrawn one its `released` date.

**Viewpoints** (§7.7). In a project that records viewpoints, the front matter records
them as drafted, beside the outline's plan:

```yaml
viewpoints: scene         # only where the chapter overrides parameters.viewpoints
viewpoint: ines-varga     # in chapter mode: the chapter's viewpoint character
told-from: end            # only where it differs from parameters.told_from; — for in the moment
```

In `scene` mode, `viewpoint` and `told-from` move from the front matter to each scene's
marker (below).

Markers in the prose:

- **Scene markers.** Each scene of a chapter in `scene` mode, and every scene of a
  frames project, opens with a marker of `key=value` pairs: `viewpoint` and, where it
  differs from the project's, `told-from` (viewpoints, §7.7); `at` and `travelers`
  (frames, §9.1). For example,
  `<!-- scene: viewpoint=tomas-hale told-from=— -->`, or
  `<!-- scene: at=PoA:21@main travelers=harry-potter,hermione-granger viewpoint=harry-potter -->`
- **Missing canon** is marked where the drafter needed it:
  `<!-- TODO: needs bible: <what is missing> -->`
- **Hidden canon** is marked where a beat touches a hidden truth (§6.12):
  `<!-- TODO: hidden canon: <slug>.<attribute> -->`
- **Seam conflicts** are marked where a beat needs an earlier book's item that is
  ahead of the chapter and undecided (§6.14): `<!-- TODO: seam conflict: <item> -->`

**Example cases:** [V4](../examples/README.md#case-v4), [U2](../examples/README.md#case-u2), [U3](../examples/README.md#case-u3).

## 10.19 Reviews

A review file is free-form but MUST end with:

```markdown
## Priorities
1. <the most important fix>
2. …
```

In `reviews/beta-reader.md`, a priority drawn from a human reader's notes (§10.25) is
marked `(human: <reader>)`, so it is never confused with the agent's simulated read:

```markdown
## Priorities
1. (human: reader-a) The sickbay scene repeats chapter 2's ending; move Mira somewhere public.
2. The war is told, not shown, until the last page.
```

`reviews/beta-reader.md` additionally lists any `TODO` markers left in the prose, before
its priorities. The section is present, and says `None`, even when there are none:

```markdown
## Leftover markers
| Chapter    | Marker                                     |
| ---------- | ------------------------------------------ |
| chapter-07 | TODO: needs bible: the Ravenclaw password  |
```

`reviews/canon.md` additionally lists every finding in a table:

```markdown
## Findings
| # | Class | Location | Finding | Resolution |
```

`Class` is one of the classes in §6.9. `Resolution` is `fix`, `decide`, or `author`
(order inversions, divergence conflicts, hidden canon, theory conflicts, and seam
conflicts, which only the author may decide).

An **order audit** (§6.8) adds one entry block per inversion, after the findings table:

```markdown
## Order inversions

### I1 — harry-potter+sirius-black.bond
- now earlier: GoF:2 "correspondents" (Harry writes to Sirius about his scar)
- now later: PoA:17 "met in the Shrieking Shack"
- depends on: Harry and Sirius having met
- option remove: Harry writes to no one. Fallout: nobody adult hears about the scar
  pain; Sirius's advice before the first task has no source.
- option substitute: Harry writes to someone he already knows (Dumbledore, Hagrid).
  Fallout: that person learns of the scar months early and must act, or choose not to.
- option supply: an original scene has Harry meet Sirius before the Tournament.
  Fallout: Sirius is known to Harry while still a fugitive; PoA's reveal loses its
  surprise.
- option reorder: move PoA back before GoF. Fallout: undoes part of the premise.
```

After its entries, the order audit lists the host's inversion candidates (§6.8), one
row each, with how it addressed them:

```markdown
## Inversion candidates
| Candidate                            | Addressed |
| ------------------------------------ | --------- |
| harry-potter+sirius-black (PoA, GoF) | I1        |
```

- `Candidate`: the entity, then the two segments the order swaps, in ruler order.
- `Addressed`: the inversions raised from it (`I1`, `I2 and I3`), or `none: <reason>`,
  saying why its rows on the two sides do not depend on each other.

A **divergence audit** (retellings, §6.6) uses the same form under
`## Divergence conflicts`, with entries `C1`, `C2`, …, each naming the divergence, the
canon row it reaches, and the options keep, adapt, remove, and substitute:

```markdown
## Divergence conflicts

### C2 — harry-potter.role (D1: Harry is blind)
- canon: PS:9 "Gryffindor Seeker" (McGonagall sees him fly and recruits him)
- option keep: he is made Seeker anyway. Fallout: the story must make a blind Seeker credible.
- option adapt: McGonagall sees him fly by sound and feel. Fallout: his flying becomes a defining skill.
- option remove: he is never on the team. Fallout: no Nimbus Two Thousand (PS:10); Quidditch leaves his story.
- option substitute: someone else is made Seeker. Fallout: a new rivalry or friendship.
```

A **theory audit** (§6.13) uses the same form under `## Theory conflicts`, with entries
`Q1`, `Q2`, …, each naming the theory and claim, the evidence, and the options keep,
adapt, and discard. Evidence that is an erratum (§5.2) is marked `(erratum: <source>)`:

```markdown
## Theory conflicts

### Q1 — harry-potter/theories:T1, claim 2 (the middle brother is Snape)
- evidence: DH:35, after the cutoff: Dumbledore, not Snape, used the Stone to try to reach his dead
- option keep: the middle brother is Snape. Fallout: the story must answer the Stone question.
- option adapt: the middle brother is both men. Fallout: a looser mapping that readers may question.
- option discard: the middle brother stays unnamed. Fallout: the frame covers two brothers and Death.
```

A **seam audit** (§6.14) uses the same form under `## Seam conflicts`, with entries
`S1`, `S2`, …. An entry for an item ahead names the item, its anchor, what it holds,
and the chapters it is ahead of, with the options carry back, not yet, and other. An
entry for a value seam names the attribute, the earlier book's value, and the later
book's, with the options keep earlier, accept, and other. When the later book starts
before an earlier book's cutoff at its pin, a `- pin:` line under the heading says so,
before any entry:

```markdown
## Seam conflicts
- pin: chapter-01 is set at youth, before lantern-road's cutoff at its pin (lantern-road:12)

### S2 — lantern-road:ines-varga.role
- anchor: lantern-road:1 (book 1's starting state)
- holds: apprentice lamplighter
- ahead of: chapter-01 to chapter-05
- option carry back: she is already an apprentice. Fallout: her first winter is not her first in the trade.
- option not yet: she is not yet apprenticed. Fallout: the book can lead up to it.
- option other: anything else. Fallout: logged as a divergence of this book.
```

The options set out choices and their consequences in story terms. The canon-keeper
MUST NOT mark one as the answer. The author decides, and the curator logs the decision
(§6.6, §6.8, §6.12, §6.13, §6.14).

## 10.20 `showrunner-log.md`

Entries are in reverse-chronological order, each a `## <timestamp> — <summary>`
heading followed by the decisions taken and the steps scheduled. It is a control file,
never canon.

## 10.21 `sync-points.md`

Established-world projects only. An empty or missing file means a fixed cutoff
(`setting.cutoff`).

```markdown
## Sync points
| From chapter | Cutoff |
| ------------ | ------ |
| chapter-01   | PS:6   |
```

- Rows in manuscript order, one `From chapter` per row. `Cutoff` is a valid ruler point
  (§4.2), compared in the project order if there is one (§6.8). Universe projects add a
  `Base` column after `Cutoff`, holding a base id.

## 10.22 `revisions.md`

One row per change to a chapter readers have already seen, appended by the chronicler:
any change to an `early-access` chapter, in every workflow, any change to a released
installment of a serial with `serial.released: revisable`, and any change to a
`withdrawn` one (§13.12).

```markdown
## Revisions
| Chapter    | Audience     | Date       | Change                                | Reason                           | Reader note                                    |
| ---------- | ------------ | ---------- | ------------------------------------- | -------------------------------- | ---------------------------------------------- |
| chapter-03 | public       | 2026-11-20 | Harry's letter now goes to Dumbledore | Order inversion I1 resolved (D2) | Chapter 3 updated: Harry writes to Dumbledore. |
```

- `Audience`: `early-access` (the change went to early readers) or `public` (a released
  installment was released again).
- `Date`: when the changed text went out.
- `Reader note`: the text an author can publish to tell readers what changed. It is
  required for every row, whatever `serial.released` says, because these readers have
  already seen the earlier text.

## 10.23 `outline.md`

The outline is the story's plan: its acts and chapters in prose, the setup and payoff
ledger, and a table of chapters, which agents read row by row. Free prose MAY surround
the table.

In a **novel** or a **short story**, the table sits under `## Chapters`:

```markdown
## Chapters
| Chapter    | Beat                                         | Scene | Viewpoints | Viewpoint  | Told from |
| ---------- | -------------------------------------------- | ----- | ---------- | ---------- | --------- |
| chapter-01 | Ines lights her first lamp in Highcairn      |       |            | ines-varga |           |
| chapter-02 | A lamp gutters out on the empty road, unseen |       | none       |            |           |
| chapter-06 | The inn on a busy night                      | 1     | scene      | ines-varga |           |
| chapter-06 | The innkeeper alone with the oil casks       | 2     |            | tomas-hale | —         |
```

In a **serial**, the outline groups installments into arcs, one heading per arc, each
with the same table:

```markdown
## Arc 1 — <title>
| Chapter    | Beat |
| ---------- | ---- |
| chapter-01 | …    |
```

An arc's installments are the chapters in its table. The architect appends a new arc at
each planning step (A1, §13.3). Beats for released chapters are not rewritten; beats for
chapters still in the buffer may be.

- `Chapter` and `Beat` are required. The other four columns record viewpoints (§7.7).
  They follow `Beat`, in the order shown, and are needed only where the project's mode
  or a chapter's override is not `none`.
- Rows are in chapter order. A chapter has one row, or, in `scene` mode, one row per
  scene.
- `Scene`: the scene's number within its chapter, from 1. Empty unless the chapter is in
  `scene` mode.
- `Viewpoints`: the chapter's override of `parameters.viewpoints`, `none`, `chapter`, or
  `scene`, on the chapter's first row only. Empty when the chapter follows the project.
- `Viewpoint`: the slug of the viewpoint character (§10.9): on the one row of a chapter
  in `chapter` mode, and on each row of a chapter in `scene` mode, where `—` means that
  scene has no viewpoint character. Empty in a chapter in `none` mode.
- `Told from`: a chapter id or `end`, at or after the row's chapter, for a narrator
  looking back; `—` for "in the moment"; empty to take `parameters.told_from` (§7.7).
  Always empty where `Viewpoint` is empty or `—`.

**Example cases:** [V1](../examples/README.md#case-v1).

## 10.24 `time-travel.md` (frames)

One entry block per mechanism (§9.1), with the catalog fields of §10.11 plus the
module's own:

```markdown
### time-turner — Time-Turner
- model: fixed                   # dilation | fixed | loop | mutable | branching | feedback
- direction: back                # back | forward | both
- reach: one hour per turn of the hourglass
- carries: body; memory; anything held
- free-will: none                # everyone (default) | traveler | none
- immune: —                      # loop only: what does not reset
- effect: carries the wearer, and anyone inside the chain, back in time
- cost: —
- limit: travelers must not be seen by their past selves
- as-of: PoA:21
- source: books
- citation: PoA ch.21
```

- `model` is required. Every other field may be empty, and `free-will` defaults to
  `everyone`.
- `immune` lists what survives a `loop`'s reset beyond the traveler's own memory: slugs,
  catalog ids, or a short description (`faint déjà vu`).
- `limit` is checked by judgment (§9.1); state it as a rule the canon-keeper can apply.
- A mechanism whose rules change over time adds a `## State history` table, as a catalog
  does (§10.11).

**Example cases:** [23](../examples/README.md#case-23).

## 10.25 Human feedback

`references/feedback/chapter-<NN>/<reader>.md` holds one human reader's notes on one
chapter, as the author received them. Feedback is input (§3.2): agents read it, and no
agent writes it.

```markdown
---
reader: reader-a        # an id the author chooses; never the reader's contact details
chapter: 3
received: 2026-09-17
---
<the reader's notes, as received>
```

The beta-reader folds these notes into its review's `## Priorities`, each marked as
human (§12.18).

## 10.26 `routes.md` (travel)

```markdown
## Modes
| Mode | Name    | Notes |
| ---- | ------- | ----- |
| foot | On foot |       |
| cart | By cart |       |

## State history
| Route                   | Attribute | Value | As of | Source  | Citation |
| ----------------------- | --------- | ----- | ----- | ------- | -------- |
| highcairn+the-halfway-inn | foot    | 3d    |       | project | premise  |
| highcairn+the-halfway-inn | cart    | 2d    |       | project | premise  |
```

- `Mode`: an id (§10.0), and a key of the file (§2.7): a higher layer adds modes, and
  never redefines one.
- `Route`: two place ids from `places.md`. Joined by `+`, in alphabetical order, the
  route runs both ways. Joined by `>`, it runs one way only, from the first to the
  second (a river current, a one-way portal).
- `Attribute`: a mode from `## Modes`, or `distance` (free text, for readers).
- `Value`, for a mode: a duration (§9.4), `—` (the mode cannot make the journey), or
  `(unset)` (the route closes to that mode).

## 10.27 `mysteries.md` (mysteries)

```markdown
## Mysteries
| Mystery        | Question                                   | Revealed at | Notes |
| -------------- | ------------------------------------------ | ----------- | ----- |
| moody-identity | Who is the Moody teaching Defence this year? | GoF:35    |       |

## Clues
| Mystery        | Clue | Kind        | Points to                          | Planted at | Needed | Citation |
| -------------- | ---- | ----------- | ---------------------------------- | ---------- | ------ | -------- |
| moody-identity | c1   | clue        | Moody drinks only from his own flask | GoF:13   | yes    | GoF ch.13 |
| moody-identity | c3   | red-herring | Karkaroff, a former Death Eater    | GoF:27     | no     | GoF ch.27 |
```

- `Mystery`: a secret in `knowledge.md` (§10.5), which holds the answer. A key of the
  file.
- `Revealed at`: where the reader learns the answer: a ruler point in a package, or a
  chapter id in a project.
- `Clue`: an id, unique within its mystery.
- `Kind`: `clue` or `red-herring`.
- `Points to`: what the clue suggests, in free text.
- `Planted at`: where the clue first appears, in the same form as `Revealed at`.
- `Needed`: `yes` if a reader needs the clue to reach the answer, otherwise `no`. A red
  herring is always `no`.
- A higher layer, a project included, MAY add clues to a lower layer's mystery, under
  the same `Mystery` id. It MUST NOT change or remove them: a project that moves or
  drops a canon clue logs a divergence (§6.2).

## 10.28 `titles.md` (lineage)

A multi-entity state history (§10.5) whose entities are titles and offices:

```markdown
## State history
| Entity                 | Attribute | Value                          | As of  | Source | Citation |
| ---------------------- | --------- | ------------------------------ | ------ | ------ | -------- |
| headmaster-of-hogwarts | holder    | albus-dumbledore               | PS:4   | books  | PS ch.4  |
| headmaster-of-hogwarts | holder    | dolores-umbridge               | OotP:28 | books | OotP ch.28 |
```

- `holder`: a slug (§10.9), or `(unset)` while the title is vacant.
- `rule`: how the title passes on, in free text.
- Other attributes are free.

## 10.29 `prompts/<id>.md` (image prompts)

One image prompt, written by the prompter (§12.20). `<id>` is an id (§10.0) that the
author chooses.

```markdown
---
kind: family-tree          # character | family-portrait | family-tree | map | location
subjects: [harry-potter]   # slugs, or place ids for a map or location
cutoff: "GoF:37"           # a ruler point; or, in a project with no stack, omit it
position: chapter-12       # optional: a chapter, for story-dated rows (§4.11)
date: "1995"               # family-portrait only: the in-world date it is painted (§4.13)
---
## Prompt
<plain descriptive prose for an image generator>

## Gaps
- <a detail the bible does not give, and how the prompt treats it>

## Sources
| Fact                         | From                                   |
| ---------------------------- | -------------------------------------- |
| Harry's parents              | `harry-potter.parents` (books, PS:1)   |
```

- `kind`: one of the five kinds. `family-portrait` and `family-tree` need the lineage
  module (§9.6). A `map` that shows journey times needs travel (§9.4).
- `subjects`: what the picture shows, or, for a `family-tree`, the entity it starts
  from. Each MUST be a slug in the stack's roster, or, for a `map` or `location`, a
  place id in `places.md`.
- `cutoff` and `position`: where the snapshot is taken (§7.2). In an established
  project, the cutoff defaults to the project's, and MUST be a valid point on the
  stack's ruler. In a project with no stack, only `position` applies.
- `date`: a date in the stack's calendar. Without it, a family portrait is dated at
  its cutoff's date.
- `## Gaps` is required, and MAY be empty. `## Sources` is required: one row per fact
  the prompt states about a subject.

**Example cases:** [M4](../examples/README.md#case-m4).

## 10.30 `export/` (chapters for readers)

Written by the `export` skill (§13.13), one folder per audience:

```
export/
├── early-access/           # what early readers have
│   ├── work.yaml
│   ├── chapter-03.md
│   └── chapter-03.yaml
└── public/                 # what everyone has (serials)
    ├── work.yaml
    ├── chapter-01.md
    └── chapter-01.yaml
```

**`chapter-<NN>.md`** is the chapter as readers get it: plain Markdown, with

- no front matter, and no HTML comment of any kind (`<!-- … -->`), markers included;
- a first line `# <title>`, or `# Chapter <n>` when the chapter has no `title`;
- `publishing.scene_break` (default `* * *`) on a line of its own in place of each
  scene marker but the first (§10.18), so the scenes stay apart;
- runs of blank lines collapsed to one, and one newline at the end.

The text is otherwise exactly the chapter's. **`chapter-<NN>.yaml`**, only with a
`publishing` block (§10.1):

```yaml
chapter: 1
title: "Narendra"
audience: public            # public | early-access
date: 2026-09-04            # the step's date: released, re-released, or early access
words: 69                   # words in chapter-<NN>.md, less its heading and scene breaks
characters: [Lt. Mira Oduya, Rachel Garrett]
content_notes: [The death of a character]
notes_before: "…"           # from references/chapter-notes/chapter-01.md
notes_after: "…"
revision_note: "…"          # the latest revisions.md row's Reader note for this audience (§10.22)
```

**`work.yaml`** describes the work as that audience has it:

```yaml
title: "The Long Way Back"  # the project's name
authors: [Ade, Kit]         # the authors' names (§11.13)
fandoms: [Star Trek]        # the names of the stack's base packages; absent when original
summary: "…"                # publishing.summary
rating: teen                # publishing.rating
language: en                # publishing.language
tags: […]                   # publishing.tags
relationships: [Lt. Mira Oduya & Rachel Garrett]
characters: [Lt. Mira Oduya, Rachel Garrett, Tasha Yar (altered timeline)]
content_notes: [Grief and mourning, The death of a character]
chapters: {count: 3, planned: 12}   # chapters this audience has; the outline's count
credits: ["…"]              # the credit of each layer in the stack that has one (§2.10)
```

- **Names, not slugs.** Characters and relationships are given by their roster `Name`
  (§10.9): `a+b` as `A & B`, and `a/b` as `A/B`. Lists are in order of first appearance.
- **A chapter's characters** are the roster slugs in the `Entities` of its rows in
  `timeline.md` (§10.15). The work's are those of every chapter the audience has.
- **The work's content notes** are those of every chapter the audience has, in the
  readers' words from `content_notes`.
- **`date`** is when this audience got the chapter: for early readers, its
  `early-access` date, or its release date if it never had one; for the public, its
  `re-released` date, or else its `released` one.
- **`planned`** is the number of chapters in the outline (§10.23), or absent if it has
  none.
- A key with no value is left out.

**`references/chapter-notes/chapter-<NN>.md`** holds the author's notes to readers for
one chapter: a `## Before` section and an `## After` section, both optional, in free
Markdown. The author writes it; no agent does, and no agent reads it.

**Example cases:** [P5](../examples/README.md#case-p5).
