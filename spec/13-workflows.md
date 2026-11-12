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
| `extraction`         | chain   | world   | run against a world, not a project   |
| `crossover`          | chain   | universe | run against a universe, to build its bridge |

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
| 7    | architect          | `bible/knowledge.md`                         |           |               |
| 8    | researcher         | `reviews/research.md`                        |           |               |
| 9    | line-editor        | `bible/style.md`                             | milestone |               |

Step 3 runs once per world-layer file the premise needs (§3.3). Steps 3, 6, and 7 write
world-layer files, so they run only when the project references no world or universe.
Otherwise those files come from the world package. The gate at step 9
puts the whole plan (premise, outline, world, cast, voice) on the table before any prose
is written: the cheapest place to change direction.

### Phase 2 — Draft (repeat: per-chapter)

| Step | Agent             | Writes                          | Gate      | Repeat   |
| ---- | ----------------- | ------------------------------- | --------- | -------- |
| 10   | drafter           | `manuscript/chapter-<NN>.md`    |           |          |
| 11   | showrunner        | `showrunner-log.md`             |           |          |
| 12   | chronicler        | `bible/<ledger>`                |           | per-file |
| 13   | continuity-editor | `reviews/continuity.md`         |           |          |
| 14   | line-editor       | `manuscript/chapter-<NN>.md`    | milestone |          |

- Step 11 scans the draft for `TODO: needs bible` markers, routes each to a builder, and
  re-runs step 10. Every TODO is resolved before step 13.
- Step 12 runs for `timeline.md` always, and for `game-state.md`, `timelines.md`, and
  `branches.md` when their modules are enabled.
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

For stories **released in installments as they are written**: web serials, fanfics
posted chapter by chapter, episodic fiction. Unlike `novel`, there is no whole-book
revision before readers see the work: each installment is released when its gate is
approved, and the story is planned and reviewed arc by arc.

### Released installments

`project.yaml` sets what happens to an installment once it is released (§10.1):

| `serial.released`        | Released installments                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------- |
| `locked` *(the default)* | Never change. The host MUST refuse any write to a chapter whose status is `released`.                   |
| `revisable`              | May be revised. Every change is re-released and recorded in `revisions.md` (§10.23), so readers can be told. |

Under `locked`, anything that would normally revise an earlier chapter is handled
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
| A2   | architect | `bible/canon-track.md` |           |

- **A1** adds the next arc to the outline (§10.24), taking in the previous arc review's
  priorities. It is skipped for the first arc, which step 2 already planned.
- **A2** extends the canon track over the arc's installments (established worlds only,
  §6.7).

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
established-world and frames overlays apply unchanged. The gate at step 14 is the
**release decision**. When it is approved, **R1** (the `release` skill, §11.10) marks
the chapter `status: released`.

### Phase 4 — Arc review (after each arc)

| Step | Agent          | Writes                    | Gate      |
| ---- | -------------- | ------------------------- | --------- |
| V1   | pacing-analyst | `reviews/pacing.md`       |           |
| V2   | critic         | `reviews/critique.md`     |           |
| V3   | beta-reader    | `reviews/beta-reader.md`  | milestone |
| V4   | showrunner     | `showrunner-log.md`       |           |

The reviewers read the arc just released, plus earlier arcs where they need context.
**V4** turns the priorities into work for the next arc: notes for A1, and fix-forward
items for upcoming installments. Under `revisable`, it may also schedule revisions of
released installments. Each one re-runs the owning agent, then R1, then a chronicler
step on `revisions.md`.

There is no finishing phase: an installment is final when it is released.

## 13.4 `established-world` (overlay)

Applies to any chain when `setting.type: established`. It makes the worldbuilder a
curator, adds the canon-keeper to review, and runs the living-canon loop (§6.11).

| Step | Agent             | Writes                     | Gate      | Position          |
| ---- | ----------------- | -------------------------- | --------- | ----------------- |
| E1   | worldbuilder      | `bible/canon.md`           | milestone | replace 3         |
| E1a  | architect         | `bible/canon-track.md`     | milestone | after E1          |
| E1b  | canon-keeper      | `reviews/canon.md`         | milestone | after E1a         |
| E2   | worldbuilder      | `bible/divergences.md`     |           | after E1b         |
| E2a  | canon-keeper      | `reviews/canon.md`         | milestone | after E2          |
| E2b  | worldbuilder      | `bible/divergences.md`     |           | after E2a         |
| E3   | canon-keeper      | `reviews/canon.md`         |           | after 13          |
| E4   | showrunner        | `showrunner-log.md`        |           | after E3          |
| E5   | worldbuilder      | `bible/divergences.md`     |           | after E4          |

- **E1** writes the adherence contract (§6.3) instead of inventing a world.
- **E1a** maps chapters to cutoffs and, if the story rearranges canon, writes the
  project order (§6.7–6.8). It is skipped when the story stays at one cutoff in canon
  order.
- **E1b** runs only when the project has its own order: the canon-keeper's **order
  audit** lists every inversion, with options and their fallout (§10.20). The gate
  after it waits for the **author** to decide each inversion, under every gate policy.
  An author who chooses to reorder sends the run `back: E1a`.
- **E2a** and **E2b** run only in a **retelling** with planned divergences (§6.6). E2a,
  the canon-keeper's **divergence audit**, reads ahead along the canon track and lists
  each divergence conflict, with options and their fallout. The gate waits for the
  **author** to decide each one, under every gate policy. E2b logs the author's choices.
  When a later chapter's E5 logs a new divergence, the showrunner re-runs E2a and E2b
  for the canon still ahead.
- **E2** logs the **planned** divergences from the premise and outline, with their
  consequences: changes and additions to canon entities (§6.2), the reordering itself,
  and the author's chosen resolution for each order inversion, with its fallout as open
  consequences.
- **E3** classifies the chapter's problems (§6.9). **E4** routes fix items and resolves
  or surfaces decide items. A pending decide item blocks step 14 (§11.8).
- **E5** runs only when E4 accepted an emergent divergence or consequences were
  absorbed. It logs the divergence and updates consequence statuses. The showrunner then
  schedules revisions for any already-written chapter an open consequence invalidates.
- Step 4 (character-designer) writes original characters only.
- When the world is extracted, a `temporal-snapshot` step MAY precede step 10 to
  materialize the cast's snapshots (§7.6).

## 13.5 `frames` (overlay)

Applies when `setting.temporal_model: frames`.

- Step 12 (chronicler) also maintains `timelines.md` and `branches.md`.
- The drafter marks every scene's world point and travelers (§10.19).
- The canon-keeper runs its frame and paradox checks. In a project that is not
  established-world, the overlay inserts the canon-keeper after step 13 for those checks
  only.
- An accepted paradox is recorded by a chronicler step on `branches.md`, scheduled by
  the showrunner.

## 13.6 `extraction` (world context)

Builds or grows a world package from source texts. It solves one core problem: **many
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
| F4   | `world-index`      | `bible/index.md`                        | milestone |            |          |

- Before F0, a human creates `world-config.yaml` (with `status: open-for-extraction`) and
  registers the sources in `sources.md`.
- **F2a** merges the roster first, so that every `New names` slug is either accepted or
  recorded as an alias before the other targets merge. Its gate is where a human
  resolves the extractors' `Needs a human` items.
- **F2b** runs one instance per target file named in any record's `Target` column.
  Each instance is the sole writer of its target, so all instances can run in parallel.
- **F3** is optional.
- After F4, a human bumps `version` (§2.8) and, when extraction is complete, sets
  `status: locked`.

**Ordering principle:** facts are self-dating (§4.8). Units can be extracted in any order
and history is assembled by sorting on canon point, so running F1 and F2b sequentially
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
projects set in the universe re-pin it.

