# 10. File formats

This chapter defines the exact structure of every file a host needs to parse. Prose
sections (a character's backstory, a place's description) are free-form. The structures
below are what tools rely on.

## 10.0 Conventions

**Manifests** are YAML 1.2. Each has a JSON Schema in [`schemas/`](../schemas/).

**Structured markdown** uses two forms:

- **Tables.** A table is identified by the `##` heading it sits under and by its
  required header cells, which MUST appear in the order given, spelled exactly as
  given. A file MAY add columns **after** the required ones. Parsers MUST ignore columns
  they do not know.
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
| point       | a canon point, `work{:index}[+HH:MM:SS[.f]]` (§4.2), or empty when timeless (§4.7) |
| source      | a source id registered in `sources.md`                                      |
| citation    | free text that locates the evidence, for example `PS ch.6` or `TNG "Q Who"` |
| chapter     | a manuscript chapter id, `chapter-<NN>`                                     |

## 10.1 `project.yaml`

Schema: [`schemas/project.schema.json`](../schemas/project.schema.json).

```yaml
spec_version: "0.1"
id: two-witnesses
name: "Two Witnesses"
workflow: novel                 # novel | short-story | serial
gates: milestones               # none | milestones | all
seed: "Cedric survives the graveyard, and Harry is no longer the only witness to Voldemort's return."
parameters:
  pov: third-limited
  tense: past
  target_length: 90000          # words

world:                          # or `universe:`, or neither (self-contained)
  id: harry-potter
  version: 2.1.0

setting:
  type: established             # original | established
  fidelity: flexible            # strict | flexible | au   (established only)
  canon_point: "GoF:37"         # single-world cutoff
  canon_mode: retelling         # retelling (default) | branch   (established only)
  divergence_point: "GoF:32"    # required for a branch; recommended for a retelling
  active_profile: enhanced      # optional; defaults to the world's
  temporal_model: linear        # linear | frames

modules:
  litrpg: false
  languages: false
```

A serial project (`workflow: serial`) MAY add:

```yaml
serial:
  released: revisable           # locked (default) | revisable
```

The `serial` block is invalid for any other workflow (§13.3).

For a universe project, replace `world:` with `universe: { id, version }` and replace
`canon_point`, `divergence_point`, and `active_profile` with `canon_points`,
`divergence_points`, and `active_profiles`, maps keyed by world id (§7.4).

Overlay workflows are derived, not configured: `setting.type: established` applies
the established-world overlay, and `temporal_model: frames` applies the frames overlay
(§13).

## 10.2 `world-config.yaml`

Schema: [`schemas/world-config.schema.json`](../schemas/world-config.schema.json).

```yaml
spec_version: "0.1"
id: harry-potter
name: "Harry Potter"
version: 2.1.0
status: locked                  # open-for-extraction | locked

canon_basis:
  primary: books
  also_canon: []
  excluded: [films]

canon_profiles:
  book-purist:  { order: [books] }
  interpretive: { order: [books, theory] }
  enriched:     { order: [books, fanon-hp, fanfic-example] }
  enhanced:     { order: [books, fanon-hp, fanfic-example], resolution: recency }

active_profile: book-purist
```

`resolution` is `precedence` (the default) or `recency` (§5.4).

### 10.2.1 `universe.yaml`

Schema: [`schemas/universe.schema.json`](../schemas/universe.schema.json). Example in
§8.1. The bridge's source id is `bridge`, tier `crossover`, and it is implicitly active
in every profile within the universe.

## 10.3 `index.md`

```markdown
## Files
| Path           | Layer | Holds                                   |
| -------------- | ----- | --------------------------------------- |
| world.md       | world | Setting, era, rules and systems         |
| magic/spells.md | world | Spell catalog                          |
```

`Path` is relative to the side the index lives on. `Layer` is one of the layers in §3.2.
Every world-layer file in the package, and every story-layer file in the project, MUST
be listed.

## 10.4 `canon-timeline.md` (the ruler)

```markdown
## Works
| Work | Title               | Levels                   | Timed level | Notes |
| ---- | ------------------- | ------------------------ | ----------- | ----- |
| PS   | Philosopher's Stone | chapter › scene          |             |       |
| TOS  | The Original Series | season › episode › scene | episode     |       |

## Order
| Order | Segment | Title               | Units | Notes |
| ----- | ------- | ------------------- | ----- | ----- |
| 1     | PS      | Philosopher's Stone | 17    |       |

## Counts
| Node    | Units |
| ------- | ----- |
| TOS:3:2 | 14    |
```

- `Work`: unique. Matches `^[A-Za-z][A-Za-z0-9-]*$`; case is preserved, for familiar
  abbreviations.
- `Levels`: level names from the top down, separated by `›`. A work with no levels
  (`Levels` empty) cannot be divided.
- `Timed level`: one of the work's level names, `work` (the work itself is timed, as in
  a film), or empty (not timed).
- `Order`: a positive integer, unique, with no gaps.
- `Segment` and `Node`: a path, `work{:index}`, with no timecode.
- `Units`: an integer, empty, or `—` (§4.1).
- `## Counts` is optional. A node in it must lie inside a segment.

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

An original character (`origin: original`) uses project-defined sources. Its rows MAY
leave `As of` empty, and use `Source: project`.

## 10.6 Extraction record

`extraction/<w>/extractions/<work>/ch<NN>.md` is one record per source unit:

```markdown
---
world: harry-potter
point: PS:6            # the unit this record covers
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

- `Target`: the world-layer file the fact belongs in, for example `characters/harry-potter.md`.
- `Entity`: the slug or entity id (empty for a single-entity target).
- `Change`: `new`, `change`, or `confirm`.
- `True from` (optional): when the fact became true, if the passage reveals backstory (§4.4).
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
```

- `ID`: `D<n>`, never reused.
- `Overrides`: `<slug>.<attribute>=<value>` assignments, separated by `; `, or `—`. The
  value may be `(unset)`, which makes the attribute absent.
  For a relationship, use the pair as the slug (`harry+ron.bond=rivals`).
- `Kind`: `planned` or `emergent`.
- `First occurs`: a chapter id.
- `Until` (optional column, after `First occurs`): the chapter id from which the
  divergence stops applying. It MUST be after `First occurs`. Empty means permanent.
- `Status`: `open`, `absorbed`, or `accepted`. `Absorbed in` is a chapter id, required
  when absorbed. `accepted` (serials with locked releases only, §13.3) means the author
  accepts an inconsistency in a released installment. It requires an optional `Note`
  column, after `Absorbed in`, saying why.
- `## Hidden canon` (optional section, §6.12): one row per hidden truth the author has
  decided about. `Revealed at` is the canon row's `As of`. `Decision` is `reveal-early`,
  `keep-hidden`, or `other`. `Divergence` is the ID of the divergence a reveal produced,
  or `—`. `Decided in` is the chapter being written when the decision was made. `Note`
  is required for `other`.

## 10.9 `characters/_roster.md`

```markdown
## Characters
| Slug | Name | Origin | Aliases | Reveal of | Revealed at | Version of |
```

- `Aliases`: other names that refer openly to this character.
- `Reveal of` and `Revealed at`: for a **reveal alias**, a surface identity that is
  secretly someone else. The surface identity gets its own row and its own slug, and
  facts are filed under it. `Reveal of` names the true slug, and `Revealed at` is the
  canon point from which the identity is known. Extractors MUST NOT file facts under the
  true slug before the reveal, because that leaks it.
- The snapshot never joins a reveal alias to its true identity (§7.3); agents do.
- `Version of`: for a **version**, a canon-distinct instance of one identity (an
  alternate-universe self) with its own sheet. A time-traveling copy is not a version;
  it stays on one sheet.

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

Theories are entry blocks:

```markdown
### T3 — <short claim>
- kind: reading-beyond-text          # authorial-intent | reading-beyond-text
- confidence: plausible              # speculative | plausible | well-supported
- status: open                       # open | supported | contradicted | retired
- evidence: PS:6 (PS ch.6); CoS:17 (CoS ch.17)
- falsifier: <what would refute it>

<reasoning, in prose>
```

Theories are cited as source `theory` (tier `theory`).

Quotations:

```markdown
## Quotations
| ID | Line | Speaker | Rank | As of | Source | Citation |
```

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
```

Concepts and entities are world-qualified (`<world-id>:<id>`). Crossover canon rows use
source `bridge`. `As of` in crossover canon is a canon point qualified by world
(`harry-potter:HBP:7`) or empty.

## 10.15 `timeline.md` (story time)

```markdown
## Events
| Chapter | Story time | Event | Entities |
```

Rows are in manuscript order. `Story time` is free text (an in-world date or "three
days later"). `Entities` lists the slugs involved.

## 10.16 `timelines.md` and `branches.md` (frames)

```markdown
## Legs
| Traveler | Leg | Departs | Arrives | Personal cutoff | Chapter |
```

`Departs` and `Arrives` are world points (`<point>@<branch>`). `Personal cutoff` is the
latest point the traveler has lived through, which bounds what they know.

```markdown
## Branches
| Branch | Splits from | At | Cause |

## Paradoxes
| ID | Description | Decision | Rationale | Chapter |
```

`Decision` is `fixed` or `accepted`. The default branch is `main`.

## 10.17 `canon.md` (adherence contract)

Required headings, in this order: `## Canon in scope`, `## Point of divergence`,
`## Original additions`, `## Fidelity`. Content is prose with pointers into the world
layer (§6.3).

## 10.18 `game-state.md`

```markdown
## State history
| Chapter | Attribute | Value | Change | Cause |
```

`Attribute` covers stats (`stat.strength`), level (`level`), inventory
(`inventory.<item>`, value = quantity), skills (`skill.<id>`), and quests
(`quest.<id>`, value = stage). `Change` is the signed delta where numeric.

## 10.19 Manuscript chapters

```markdown
---
chapter: 7
status: drafted       # drafted | line-edited | final | released (serial only)
released: 2026-11-03  # serial only: set by the release skill
---
```

- **Frames projects** open each scene with a marker:
  `<!-- scene: at=PoA:21@main travelers=harry-potter,hermione-granger -->`
- **Missing canon** is marked where the drafter needed it:
  `<!-- TODO: needs bible: <what is missing> -->`
- **Hidden canon** is marked where a beat touches a hidden truth (§6.12):
  `<!-- TODO: hidden canon: <slug>.<attribute> -->`

## 10.20 Reviews

A review file is free-form but MUST end with:

```markdown
## Priorities
1. <the most important fix>
2. …
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
(order inversions, divergence conflicts, and hidden canon, which only the author may
decide).

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

The options set out choices and their consequences in story terms. The canon-keeper
MUST NOT mark one as the answer. The author decides, and the curator logs the decision
(§6.6, §6.8).

## 10.21 `showrunner-log.md`

Entries are in reverse-chronological order, each a `## <timestamp> — <summary>`
heading followed by the decisions taken and the steps scheduled. It is a control file,
never canon.

## 10.22 `canon-track.md`

Established-world projects only. Both sections are optional; an empty or missing file
means a fixed cutoff (`setting.canon_point`) and the ruler's order.

```markdown
## Track
| From chapter | Cutoff |
| ------------ | ------ |
| chapter-01   | PS:6   |

## Order
| Order | Segment |
| ----- | ------- |
| 1     | PS      |
```

- `## Track`: rows in manuscript order, one `From chapter` per row. `Cutoff` is a valid
  canon point (§4.2). Universe projects add a `World` column after `Cutoff`, holding a
  world id.
- `## Order`: a permutation of every segment in the world's ruler (§6.8, rule 1), with
  `Order` a positive integer, unique, with no gaps. Universe projects add a `World`
  column, and give a permutation per world that they reorder.

## 10.23 `revisions.md`

Serial projects with `serial.released: revisable` only. One row per change to a
released installment, appended by the chronicler:

```markdown
## Revisions
| Chapter    | Released again | Change                               | Reason                        | Reader note                                  |
| ---------- | -------------- | ------------------------------------ | ----------------------------- | -------------------------------------------- |
| chapter-03 | 2026-11-20     | Harry's letter now goes to Dumbledore | Order inversion I1 resolved (D2) | Chapter 3 updated: Harry writes to Dumbledore. |
```

`Reader note` is the text an author can publish to tell readers what changed.

## 10.24 `outline.md` in a serial

The outline groups installments into arcs, one heading per arc:

```markdown
## Arc 1 — <title>
| Chapter    | Beat |
| ---------- | ---- |
| chapter-01 | …    |
```

An arc's installments are the chapters in its table. The architect appends a new arc at
each planning step (A1, §13.3). Arcs already released are not rewritten.

