# 13. Workflows

Workflows are the agent chains for each kind of output. Chains are complete workflows;
overlays modify a chain (§11.7). A project names its chain in `workflow`. Overlays
apply automatically from its `setting` (§10.1).

| Workflow             | Kind    | Context | Applies when                         |
| -------------------- | ------- | ------- | ------------------------------------ |
| `novel`              | chain   | project | `workflow: novel`                    |
| `short-story`        | chain   | project | `workflow: short-story`              |
| `serial`             | chain   | project | `workflow: serial`                   |
| `established-world`  | overlay | project | `setting.type: established`          |
| `frames`             | overlay | project | `setting.temporal_model: frames`     |
| `adopt`              | chain   | project | run once, to bring chapters written elsewhere into a project (§13.8) |
| `extraction`         | chain   | package | run against a package, not a project |
| `crossover`          | chain   | universe | run against a universe, to build its bridge |

Early access (§13.9) is not a workflow: it is a step the author may take in any chain.
Nor is renumbering chapters (§13.10).

The tables below show each step's agent, its output, its gate, and its repeat.
Workflow files (§11.7) add each step's `Reads`, as given in §12.

## 13.1 `novel`

### Phase 1 — Foundation

| Step | Agent              | Writes                                       | Gate      | Repeat        |
| ---- | ------------------ | -------------------------------------------- | --------- | ------------- |
| 1    | architect          | `bible/premise.md`                           | milestone |               |
| 2    | architect          | `bible/outline.md`                           | milestone |               |
| 3    | worldbuilder       | `bible/<file>` (inventor mode)               |           | per-file      |
| 4    | character-designer | `bible/characters/<slug>.md`                 |           | per-character |
| 5    | character-designer | `bible/characters/_roster.md`                |           |               |
| 6    | character-designer | `bible/relationships.md`, `bible/voice-guide.md` |       | per-file      |
| 7    | architect          | `bible/knowledge.md`, `bible/mysteries.md`   |           | per-file      |
| 8    | researcher         | `reviews/research.md`                        |           |               |
| 9    | line-editor        | `bible/style.md`                             | milestone |               |

Step 3 runs once per world-layer file the premise needs (§3.3). Steps 3, 6, and 7 write
world-layer files. In a project with a stack, the world comes from the stack's packages
(§2.2), and these steps write only the project's own additions (§2.7): original places,
systems, and terms, and, in a series begun by a self-contained book, the ruler's inserts
(`canon-timeline.md`, §4.12) (step 3); relationships between original characters (step
6); and the project's secrets and what original characters know (step 7). Each is
skipped when the story has none. The gate at step 9 puts the whole plan (premise,
outline, world, cast, voice) on the table before any prose is written: the cheapest
place to change direction.

### Phase 2 — Draft (repeat: per-chapter)

| Step | Agent             | Writes                          | Gate      | Repeat   |
| ---- | ----------------- | ------------------------------- | --------- | -------- |
| 10   | drafter           | `manuscript/chapter-<NN>.md`    |           |          |
| 11   | showrunner        | `showrunner-log.md`             |           |          |
| 12   | chronicler        | `bible/<ledger>`                |           | per-file |
| 13   | continuity-editor | `reviews/continuity.md`         |           |          |
| 14   | line-editor       | `manuscript/chapter-<NN>.md`    | milestone |          |

- Step 11 scans the draft for `TODO` markers. It routes each `needs bible` marker to a
  builder and re-runs step 10, so that none is left before step 13. It surfaces each
  `hidden canon` and `seam conflict` marker to the author. The
  chapter goes on to steps 12 and 13, but the marker blocks step 14 until the author has
  decided, the curator has recorded the decision, and the drafter has redrafted the
  passage (§11.8).
- Step 12 runs for `timeline.md` always; for `game-state.md`, `timelines.md`,
  `branches.md`, and `mysteries.md` when their modules are enabled; and for each file of the project's own
  entities whose state the chapter changes, to append its story-dated rows (§4.11).
- If step 13 reports problems, the showrunner routes fixes to the drafter and re-runs
  steps 12 and 13 before step 14.

### Phase 3 — Whole-book review

| Step | Agent          | Writes                    | Gate      |
| ---- | -------------- | ------------------------- | --------- |
| 15   | pacing-analyst | `reviews/pacing.md`       |           |
| 16   | critic         | `reviews/critique.md`     |           |
| 17   | beta-reader    | `reviews/beta-reader.md`  | milestone |
| 18   | showrunner     | `showrunner-log.md`       |           |

Step 18 reads the priorities of every review (research, continuity, pacing, critique,
beta-reader, and canon under the overlay), schedules a revision pass, and loops the
relevant Phase 2 and 3 steps until the priorities are cleared.

### Phase 4 — Finish

| Step | Agent       | Writes                                       | Gate      | Repeat      |
| ---- | ----------- | -------------------------------------------- | --------- | ----------- |
| 19   | line-editor | `manuscript/chapter-<NN>.md` (`status: final`) | milestone | per-chapter |

The milestone gate applies once, after the last instance.

Before step 19, the author MAY send line-edited chapters to early access (§13.9). Step
19 moves an early-access chapter to `final` like any other.

## 13.2 `short-story`

A compressed chain for a single scene or arc: one chapter, a lighter foundation.

| Step | Agent              | Writes                         | Gate      | Repeat        |
| ---- | ------------------ | ------------------------------ | --------- | ------------- |
| 1    | architect          | `bible/premise.md`             | milestone |               |
| 2    | architect          | `bible/outline.md`             |           |               |
| 3    | character-designer | `bible/characters/<slug>.md`   |           | per-character |
| 4    | drafter            | `manuscript/chapter-01.md`     |           |               |
| 5    | showrunner         | `showrunner-log.md`            |           |               |
| 6    | continuity-editor  | `reviews/continuity.md`        |           |               |
| 7    | critic             | `reviews/critique.md`          |           |               |
| 8    | line-editor        | `manuscript/chapter-01.md`     | milestone |               |

Self-contained short stories that need setting add worldbuilder steps after step 2.

## 13.3 `serial`

For stories **released in installments**: web serials, fanfics posted chapter by
chapter, episodic fiction. Unlike `novel`, there is no whole-book revision before
readers see the work. The story is planned and reviewed arc by arc, and installments
reach readers one at a time.

### Drafting ahead

Writing and releasing are separate. An installment is **ready** when its step-14 gate is
approved (`status: line-edited`, §10.18), and **released** only when the author
releases it. The chapters that are ready or drafted but not yet released form the
**buffer**.

- The buffer has no size limit. An author may keep months of installments in hand, or
  bring a body of work written before the project used LoreStore and release it over
  time.
- Unreleased chapters are revisable exactly as in `novel`. Review findings, new
  divergences, and their consequences are fixed **in the buffer** wherever they land
  there. Only released chapters fall under the rules below.
- The author MAY send ready installments to **early access** first (§13.9): to
  patrons, say, a few chapters ahead of the public. Early-access chapters are still
  in the buffer and still revisable, but every change to one is logged in
  `revisions.md`, because someone has already read it.
- Releasing is always the **author's** decision, under every gate policy: it puts the
  installment in front of readers, which cannot be undone. Under `gates: none`, the
  showrunner prepares installments but never releases one.
- Installments are released in order. The host MUST refuse to release a chapter while
  an earlier chapter is unreleased, and SHOULD refuse to release one that is not ready.
- The showrunner reports the depth of the buffer in its log, and flags any open
  consequence or pending decide item touching a chapter the author is about to release.

### Released installments

`project.yaml` sets what happens to an installment once it is released (§10.1):

| `serial.released`        | Released installments                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------- |
| `locked` *(the default)* | Never change. The host MUST refuse any write to a chapter whose status is `released`.                   |
| `revisable`              | May be revised. Every change is re-released and recorded in `revisions.md` (§10.22), so readers can be told. |

Under `locked`, anything that would normally revise a released chapter is handled
**going forward** instead:

- **A consequence that invalidates a released installment** (§6.5, rule 3) becomes a
  decide item with two outcomes. **Absorb forward**: a later installment deals with it,
  for example by explaining it in-story, and the consequence stays `open` until then.
  **Accept**: the author accepts the inconsistency, and the consequence is marked
  `accepted` with a note. Only the author may accept; under `gates: none` the showrunner
  may only absorb forward.
- **Review findings** about released installments (continuity, canon, pacing, critique)
  are fixed in upcoming installments or the next arc's outline, never in the released
  text.

### Phase 1 — Foundation

Steps 1–9 of `novel` (§13.1), run once. The outline at step 2 needs to cover only the
first arc.

### Phase 2 — Arc planning (repeat: per-arc)

| Step | Agent     | Writes                 | Gate      |
| ---- | --------- | ---------------------- | --------- |
| A1   | architect | `bible/outline.md`     | milestone |
| A2   | architect | `bible/sync-points.md` |           |

- **A1** adds the next arc to the outline (§10.23), taking in the previous arc review's
  priorities. It is skipped for the first arc, which step 2 already planned.
- **A2** extends the sync points over the arc's installments (established worlds only,
  §6.7).
- In an established world, the overlay logs the arc's planned divergences after A1 and
  audits the canon the new sync points reach after A2 (E6–E6b, §13.4).

### Phase 3 — Installment (repeat: per-chapter, within the arc)

| Step | Agent / skill     | Writes                         | Gate      | Repeat   |
| ---- | ----------------- | ------------------------------ | --------- | -------- |
| 10   | drafter           | `manuscript/chapter-<NN>.md`   |           |          |
| 11   | showrunner        | `showrunner-log.md`            |           |          |
| 12   | chronicler        | `bible/<ledger>`               |           | per-file |
| 13   | continuity-editor | `reviews/continuity.md`        |           |          |
| 14   | line-editor       | `manuscript/chapter-<NN>.md`   | milestone |          |
| R1   | `release`         | `manuscript/chapter-<NN>.md`   |           |          |

Steps 10–14 are the same as in `novel`, with the same numbers, so the
established-world and frames overlays apply unchanged. Approving the gate at step 14
makes the installment ready. **R1** (the `release` skill, §11.10) runs when the author
releases it, which may be immediately or months later, and marks the chapter
`status: released`. If the author sends the installment to early access first, R1 runs
twice: once for early access, and again for the public release. Drafting the next
installment does not wait for R1.

### Phase 4 — Arc review (after each arc)

| Step | Agent          | Writes                    | Gate      |
| ---- | -------------- | ------------------------- | --------- |
| V1   | pacing-analyst | `reviews/pacing.md`       |           |
| V2   | critic         | `reviews/critique.md`     |           |
| V3   | beta-reader    | `reviews/beta-reader.md`  | milestone |
| V4   | showrunner     | `showrunner-log.md`       |           |

Phase 4 runs when an arc's last installment is ready, whether or not the arc has been
released. The reviewers read that arc, plus earlier arcs where they need context.
**V4** turns the priorities into work:

- revisions of **unreleased** chapters in the arc or the buffer, scheduled as in
  `novel`;
- notes for A1, and fix-forward items for upcoming installments, for anything that
  touches a **released** chapter;
- under `revisable`, revisions of released installments. Each one re-runs the owning
  agent, then R1, then a chronicler step on `revisions.md`.

There is no finishing phase: an installment is final when it is released.

**Example cases:** [24](../examples/README.md#case-24).

## 13.4 `established-world` (overlay)

Applies to any chain when `setting.type: established`. It makes the worldbuilder a
curator, adds the canon-keeper to review, and runs the living-canon loop (§6.11).

| Step | Agent             | Writes                     | Gate      | Position          |
| ---- | ----------------- | -------------------------- | --------- | ----------------- |
| E1   | architect         | `bible/sync-points.md`     | milestone | after 2           |
| E1a  | canon-keeper      | `reviews/canon.md`         | milestone | after E1          |
| E1b  | canon-keeper      | `reviews/canon.md`         | milestone | after E1a         |
| E2   | worldbuilder      | `bible/divergences.md`     |           | after E1b         |
| E2a  | canon-keeper      | `reviews/canon.md`         | milestone | after E2          |
| E2b  | worldbuilder      | `bible/divergences.md`     |           | after E2a         |
| E3   | canon-keeper      | `reviews/canon.md`         |           | after 13          |
| E4   | showrunner        | `showrunner-log.md`        |           | after E3          |
| E5   | worldbuilder      | `bible/divergences.md`     |           | after E4          |
| E6   | worldbuilder      | `bible/divergences.md`     |           | after A1          |
| E6a  | canon-keeper      | `reviews/canon.md`         | milestone | after A2          |
| E6b  | worldbuilder      | `bible/divergences.md`     |           | after E6a         |

- Steps 3, 6, and 7 write only the project's own additions (§13.1): the world comes from
  the stack, and the adherence settings are the author's, in `project.yaml` (§6.3).
- **E1** maps chapters to cutoffs (§6.7), in the project order if `setting.order` sets
  one (§6.8). It is skipped when the story stays at one cutoff.
- **E1a** runs only when the project has its own order: the canon-keeper's **order
  audit** lists every inversion, with options and their fallout, and addresses every
  inversion candidate (§6.8, §10.19). The gate
  after it waits for the **author** to decide each inversion, under every gate policy.
  An author who chooses to reorder changes `setting.order` and sends the run `back: E1`.
  A project that inherits its order from a project layer (§6.14) skips E1a unless it
  sets a different one.
- **E1b** runs only in a project with project layers: the canon-keeper's **seam audit**
  (§6.14) checks the pin, then lists the earlier books' items ahead of each chapter and
  the value seams (§10.19). The gate waits for the **author** to decide each one, under
  every gate policy. E2 records the decisions in the Seam conflicts table. When the sync
  points or a layer's pin change later, the showrunner re-runs E1b and E2.
- **E2a** and **E2b** run only in a **retelling** with divergences in force (§6.6). E2a,
  the canon-keeper's **divergence audit**, reads ahead through the sync points and lists
  each divergence conflict, with options and their fallout. The gate waits for the
  **author** to decide each one, under every gate policy. E2b logs the author's choices.
  E2b's own divergences are audited too: the showrunner repeats E2a and E2b until E2a
  finds no new conflict. Whenever a divergence is logged later, by E5 or to carry out
  any other author decision, the showrunner re-runs E2a and E2b for the canon still
  ahead (§6.6). In a project with project layers, E2a also runs with no planned
  divergences of its own, for the divergences the earlier books bring in.
- When a planned divergence adopts a theory (its `Basis` cites one), E2a also runs the
  **theory audit** (§6.13), and its gate waits for the author to keep, adapt, or
  discard each conflicting claim. E2b records the decisions in the Theory conflicts
  table. E2a and E2b run for this even outside a retelling.
- **E2** records the seam decisions from E1b, and logs the **planned** divergences from
  the premise and outline, with their consequences: changes and additions to canon
  entities (§6.2), the reordering itself, and the author's chosen resolution for each
  order inversion, with its fallout as open consequences.
- **E3** classifies the chapter's problems (§6.9). **E4** routes fix items and resolves
  or surfaces decide items. A pending decide item blocks step 14 (§11.8).
- **E5** runs only when E4 accepted an emergent divergence or consequences were
  absorbed. It logs the divergence and updates consequence statuses. The showrunner then
  schedules revisions for any already-written chapter an open consequence invalidates.
- **E6–E6b** run only in `serial`, once per arc after the first (§13.3). E6 logs the
  arc's planned divergences, as E2 does for the first arc. E6a audits what the arc's new
  sync points reach: the order audit, if the project order has changed since the last
  one, the seam audit, in a project with project layers, and the divergence and theory
  audits for the canon ahead, as E1a, E1b, and E2a do. Its
  gate waits for the author, under every gate policy. E6b logs the author's choices,
  and the showrunner repeats E6a and E6b until E6a finds nothing new.
- Steps 4 and 5 (character-designer) write original characters and their roster rows only.
- A `compose` step (§7.6) runs before step 1, and again whenever a layer's pin or the
  project's own `bible/` changes, so the agents read a current composed bible.
- When the stack's packages are extracted, a `temporal-snapshot` step MAY precede step
  10 to materialize the cast's snapshots (§7.6).

## 13.5 `frames` (overlay)

Applies when `setting.temporal_model: frames`.

- The rules of time travel come from `time-travel.md` (§9.1). In a self-contained
  project, the worldbuilder writes it at step 3, alongside the rest of the world.
- Step 12 (chronicler) also maintains `timelines.md` and `branches.md`.
- The drafter marks every scene's world point and travelers (§10.18).
- The canon-keeper runs its frame, mechanism, and paradox checks (§9.1). In a project
  that is not established-world, the overlay inserts the canon-keeper after step 13 for
  those checks only.
- An accepted paradox is recorded by a chronicler step on `branches.md`, scheduled by
  the showrunner.

## 13.6 `extraction` (package context)

Builds or grows one package from source texts. It runs once per package: a fandom's
canon, its films, its fanon, and each fan work are extracted separately, each into its
own package (§2.3). It solves one core problem: **many
extractors working at once must not write the same file.** Phase 1 emits dated fragments,
one per source unit, with no contention. Phase 2 assembles history from those fragments,
with one writer per output file.

| Step | Agent / skill      | Writes                                  | Gate      | Repeat     | Parallel |
| ---- | ------------------ | --------------------------------------- | --------- | ---------- | -------- |
| F0   | worldbuilder       | `bible/canon-timeline.md` (ruler mode)  | milestone |            |          |
| F0b  | character-designer | `bible/characters/_roster.md` (seed)    | milestone |            |          |
| F1   | extractor          | `extractions/<work>/ch<NN>.md`          |           | per-unit   | yes      |
| F2a  | merger             | `bible/characters/_roster.md`           | milestone |            |          |
| F2b  | merger             | `bible/<target>`                        |           | per-target | yes      |
| F3   | theorist           | `bible/theories.md`                     |           |            |          |
| F4   | `indexer`          | `bible/index.md`                        | milestone |            |          |

- Before F0, a human creates `package.yaml` (with its `kind`, its `relies-on`
  pins, and `status: open-for-extraction`) and registers the package's own sources in
  `sources.md`, with tiers its kind allows (§2.3).
- **F0** runs for a base, and for an adaptation, where it writes the `## Works` and `##
  Adapts` tables (§4.9), and for an official or fanfic package with works of its own,
  where it writes the `## Works` and `## Insert` tables (§4.10). Other packages use
  their base's ruler, and skip it. In a world with a calendar, F0 also writes the
  `## Dates` table for the package's own works (§4.13), and MAY re-run after F1 to add
  the dates the extraction records give.
- **F0b** seeds the package's own roster: for a package other than a base, only the
  entities that are new in it.
- In a package other than a base, extractors and mergers read the packages it relies
  on as lower layers. A fact about an entity one of them defines goes in an
  **extension sheet** (§10.5), never under a new slug (§2.7).
- **F2a** merges the roster first, so that every `New names` slug is either accepted or
  recorded as an alias before the other targets merge. Its gate is where a human
  resolves the extractors' `Needs a human` items.
- **F2b** runs one instance per target file named in any record's `Target` column.
  Each instance is the sole writer of its target, so all instances can run in parallel.
- **F3** runs only in a `theories` package, where it is the main step. F1 and F2 there
  extract only the fan sources the theories draw on, if any.
- After F4, a human bumps `version` (§2.8) and, when extraction is complete, sets
  `status: locked`.

**Ordering principle:** facts are self-dating (§4.8). Units can be extracted in any order
and history is assembled by sorting on ruler point, so running F1 and F2b sequentially
gives the same result as running them in parallel.

To grow an existing package, run F1 for the new units, then F2a onwards. F0 re-runs
only if new works are added to the ruler.

## 13.7 `crossover` (universe context)

Builds or revises a universe's bridge. Before it runs, a human writes `universe.yaml` and
a short `brief.md` describing the crossover.

| Step | Agent / skill  | Writes      | Gate      |
| ---- | -------------- | ----------- | --------- |
| X1   | bridge-builder | `bridge.md` | milestone |

At the gate the author approves the draft, revises it (`revise: <notes>`, for example
"keep magic and warp physics strictly separate"), or rewrites the brief and starts
again. When the bridge is approved, a human bumps the universe's `version` (§8.1), and
projects that stack the universe re-pin it.

## 13.8 `adopt`

Brings an existing story into LoreStore: chapters written before the project used it,
whether drafted, finished, or already published. It runs once. It reconstructs the
bible from the manuscript, rather than the other way round, and then hands over to the
project's own `workflow`.

Before it runs, a human writes `project.yaml` (with its stack) and imports the
chapters into `manuscript/`, giving each the status it really has: `released` or
`early-access` for a chapter readers have seen, with its date if known (§10.18). The
host checks the order rules on import.

### Phase 1 — Reconstruct

| Step | Agent / skill      | Writes                                   | Gate      | Repeat        |
| ---- | ------------------ | ---------------------------------------- | --------- | ------------- |
| P0   | `compose`          | `derived/bible/…`                        |           |               |
| P1   | architect          | `bible/premise.md`                       | milestone |               |
| P2   | architect          | `bible/outline.md`                       | milestone |               |
| P3   | character-designer | `bible/characters/<slug>.md`             |           | per-character |
| P4   | character-designer | `bible/characters/_roster.md`            |           |               |
| P4a  | character-designer | `bible/relationships.md`, `bible/voice-guide.md` |   | per-file      |
| P4b  | architect          | `bible/knowledge.md`, `bible/mysteries.md` |         | per-file      |
| P5   | worldbuilder       | `bible/<file>` (inventor)                | milestone | per-file      |
| P6   | architect          | `bible/sync-points.md`                   | milestone |               |
| P7   | line-editor        | `bible/style.md`                         | milestone |               |

### Phase 2 — Walk the chapters (repeat: per-chapter)

| Step | Agent / skill      | Writes                                   | Gate      | Repeat        |
| ---- | ------------------ | ---------------------------------------- | --------- | ------------- |
| P8   | chronicler         | `bible/<ledger>`                         |           | per-file      |
| P8a  | continuity-editor  | `reviews/continuity.md`                  |           |               |
| P9   | canon-keeper       | `reviews/canon.md`                       |           |               |
| P10  | showrunner         | `showrunner-log.md`                      |           |               |
| P11  | worldbuilder       | `bible/divergences.md` (curator)         |           |               |

- **P1–P2** reconstruct the premise and outline from what the chapters do. The outline
  records the written chapters as they are, and MAY plan ahead.
- **P3–P4b** write the story's original characters, their relationships to each other,
  and what they know, as they stand when chapter 1 opens; canon characters come from
  the stack. P8 then adds what each chapter changes, as story-dated rows (§4.11). In a
  self-contained project, P4a also writes the voice guide.
- **P5** writes the world-layer files the chapters rely on: the whole world in a
  self-contained project, and only the project's own additions in a project with a
  stack (§13.1). **P6** runs only in an established world. In an established
  world, the author fills in the adherence settings in `project.yaml` on import (§6.3).
- **P7** codifies the voice the chapters already have.
- **P8–P11** walk the chapters **in order**, one at a time. The chronicler backfills the
  story-layer ledgers and story-dated rows from what each chapter states. The
  continuity-editor reports the chapter's internal contradictions. The canon-keeper
  reports every departure from canon in the chapter as an **emergent divergence**
  (§6.9), and any order inversion, hidden canon, theory conflict, seam conflict, or
  erratum use it finds. The showrunner surfaces these to the author as usual: the
  departures are the author's own work, so they are normally accepted, but an agent
  never decides that. The curator logs what the author accepts. P9–P11 run only in an
  established world.
- Adoption **never rewrites** an imported chapter. Findings about a released chapter
  are handled as for released installments (§13.3); findings about any other chapter
  wait for the project's own workflow, which schedules revisions as usual. Changes to
  an early-access chapter are logged in `revisions.md` (§13.9).

When P11 has run for the last chapter, an established project runs the overlay's audits
for the canon still ahead of the story, so that its next chapters start with them
decided: E1a if it has its own order, E1b and E2 if it has project layers, then E2a and
E2b if it is a retelling with divergences in force or adopts a theory (§13.4). The
project then continues in its own workflow: the next chapter's draft phase in `novel`,
or arc planning in `serial`. Overlays apply from then on; `adopt` itself carries their
steps.

## 13.9 Early access

Early access puts a chapter in front of a small audience (beta readers, patrons,
advance-copy readers) before it is finished or released. It works the same in every
workflow.

- **The author sends a chapter.** Only the author may, under every gate policy: the
  `release` skill (§11.10) sets `status: early-access` and the date. The chapter SHOULD
  be `line-edited`. Chapters go to early access in order (§10.18), and the host MUST
  refuse one out of order.
- **It stays editable.** An early-access chapter can be revised, whatever
  `serial.released` says. The chronicler logs each change in `revisions.md` with
  `Audience: early-access` and a reader note (§10.22), so the early readers can be told
  what changed.
- **Human feedback comes in.** The author saves each reader's notes as
  `references/feedback/chapter-<NN>/<reader>.md` (§10.25). The showrunner schedules a
  beta-reader step, which folds the notes into its priorities marked `(human: …)`
  (§10.19), and then schedules revisions from those priorities like any others.
- **The chapter leaves early access** when the author releases it (serial: the
  `release` skill sets `status: released`) or approves it as finished (other workflows:
  step 19 sets `status: final`). A released chapter then falls under `serial.released`.

Agents never contact readers or publish anything. Early access, like release, is
recorded in the manuscript's front matter and nowhere else.

**Example cases:** [24](../examples/README.md#case-24).

## 13.10 Inserting and renumbering chapters

A chapter id (`chapter-<NN>`, §10.0) is a position in the manuscript, and the project's
files refer to chapters by id. When the outline adds, removes, or moves a chapter, the
chapters after it change ids, and every reference to them has to change in the same
step.

- **Only the `renumber` skill renumbers** (§11.10). It runs when the outline changes
  the order of chapters, before any agent reads the new order, and takes the mapping
  from old ids to new ones.
- **It rewrites every chapter id the project holds, at once:**
  - the manuscript files and their `chapter` front matter;
  - every column whose type is a chapter (§10.0), in every file of the project:
    sync points, the ledger's `First occurs`, `Until`, `Absorbed in`, and
    `Decided in`, story-dated rows' `From chapter`, and the chapters of `outline.md`,
    `timeline.md`, `game-state.md`, `timelines.md`, `branches.md`, and
    `revisions.md`, the `Planted at` and `Revealed at` cells of `mysteries.md`, the
    outline's `Told from` cells, the chapters' and scene markers' `told-from`, and
    `parameters.told_from`;
  - the folders and `chapter` fields of human feedback (§10.25).

  It does not rewrite `reviews/` or `showrunner-log.md`, which are advisory history; the
  next review replaces them. The composed bible and materialized snapshots are then
  stale (§7.6).
- **It refuses to move a chapter readers have seen.** A chapter that is `released` or
  `early-access` keeps its id, and so does every chapter before it. New chapters go
  after the last of them.
- **It refuses to move a chapter another project pins.** If any project in the
  workspace stacks this one as `project:<id>@chapter-<NN>`, chapters up to and including
  `chapter-<NN>` keep their ids, because those ids are referenced from outside the
  project.

**Example cases:** [27](../examples/README.md#case-27).

## 13.11 Content notes

Serials posted on fan sites, and books with early readers, usually warn readers of
what a chapter contains. A project that wants to track this lists its notes in
`project.yaml` under `content_notes` (§10.1), and each chapter records its own in its
front matter (§10.18). It works the same in every workflow.

- **The line-editor suggests.** Each time it edits a chapter (step 14), it sets
  `content-notes-suggested`: the project's notes that the chapter calls for, and
  `new:<id>` for one the list lacks (§12.14).
- **The author confirms.** Sending a chapter to early access or releasing it is the
  author's decision (§13.3, §13.9), and so are its notes. At that step the showrunner
  shows the author the suggestions, the author confirms the notes, adding to the
  project's list any new one they keep, and the `release` skill records them in
  `content-notes`. A chapter cannot reach early access or release without them: the
  host MUST refuse it.
- **Notes can change after readers have the chapter.** The author may change a
  released or early-access chapter's `content-notes`, even under
  `serial.released: locked`: the notes are not the text. The chronicler logs the change
  in `revisions.md` (§10.22), with a reader note, so readers can be told.
- **A revision may call for new notes.** After a revision, the line-editor's new
  suggestions may differ from the confirmed notes. The host SHOULD warn when a
  suggested note from the project's list is missing from `content-notes` on a chapter
  readers have. A `new:` suggestion the author did not keep raises nothing.

**Example cases:** [U3](../examples/README.md#case-u3).
