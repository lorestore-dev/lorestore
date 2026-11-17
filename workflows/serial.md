---
id: serial
kind: chain
context: project
---
# Workflow: serial

A story released in installments, planned and reviewed arc by arc (§13.3).

## Steps

### Phase 1 — Foundation

| Step | Agent              | Reads                                                                                                                                  | Writes                                           | Gate      | Repeat        |
| ---- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | --------- | ------------- |
| 1    | architect          | `project.yaml`; `references/…` (background)                                                                                            | `bible/premise.md`                               | milestone |               |
| 2    | architect          | `project.yaml`; `bible/premise.md`; `bible/characters/_roster.md`; `bible/world.md` (summary)                                          | `bible/outline.md`                               | milestone |               |
| 3    | worldbuilder       | `project.yaml`; `bible/index.md`; `bible/premise.md`; `bible/outline.md`; `bible/<file>`                                               | `bible/<file>` (inventor mode)                   |           | per-file      |
| 4    | character-designer | `bible/premise.md`; `bible/outline.md`; `bible/world.md` (summary); `bible/characters/_roster.md`; the sheets the character relates to | `bible/characters/<slug>.md`                     |           | per-character |
| 5    | character-designer | `bible/characters/*.md`; `bible/characters/_roster.md`                                                                                 | `bible/characters/_roster.md`                    |           |               |
| 6    | character-designer | `bible/premise.md`; `bible/outline.md`; `bible/characters/*.md`                                                                        | `bible/relationships.md`, `bible/voice-guide.md` |           | per-file      |
| 7    | architect          | `bible/premise.md`; `bible/outline.md`; `bible/characters/_roster.md`; `bible/knowledge.md`                                            | `bible/knowledge.md`, `bible/mysteries.md`       |           | per-file      |
| 8    | researcher         | `bible/premise.md`; `bible/world.md` and the catalogs; `bible/timeline.md`; `bible/glossary.md`                                        | `reviews/research.md`                            |           |               |
| 9    | line-editor        | `project.yaml` (parameters); `bible/premise.md`; `bible/voice-guide.md`; `bible/glossary.md`                                           | `bible/style.md`                                 | milestone |               |

### Phase 2 — Arc planning (repeat: per-arc)

| Step | Agent     | Reads                                                                                         | Writes                 | Gate      | Repeat |
| ---- | --------- | --------------------------------------------------------------------------------------------- | ---------------------- | --------- | ------ |
| A1   | architect | `bible/premise.md`; `bible/outline.md`; the `## Priorities` of the last arc's reviews         | `bible/outline.md`     | milestone |        |
| A2   | architect | `bible/outline.md`; `bible/sync-points.md`; `bible/canon-timeline.md`; `bible/divergences.md` | `bible/sync-points.md` |           |        |

### Phase 3 — Installment (repeat: per-chapter)

| Step | Agent             | Reads                                                                                                                                                                                                                                                                                                     | Writes                       | Gate      | Repeat   |
| ---- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------- | -------- |
| 10   | drafter           | the chapter's `bible/outline.md` rows; `bible/style.md`; the cast's snapshots at the chapter's cutoff and position; viewpoint characters' `bible/knowledge.md` rows; `bible/glossary.md`; recent `bible/timeline.md` rows; the end of `manuscript/chapter-<NN-1>.md`; the module rows the chapter touches | `manuscript/chapter-<NN>.md` |           |          |
| 11   | showrunner        | `project.yaml`; `showrunner-log.md`; `manuscript/chapter-<NN>.md` (`TODO` markers)                                                                                                                                                                                                                        | `showrunner-log.md`          |           |          |
| 12   | chronicler        | `manuscript/chapter-<NN>.md`; `bible/<ledger>`; `showrunner-log.md` (decisions)                                                                                                                                                                                                                           | `bible/<ledger>`             |           | per-file |
| 13   | continuity-editor | `manuscript/chapter-<NN>.md`; the cast's snapshots; `bible/timeline.md`; `bible/glossary.md`; the module rows the chapter touches                                                                                                                                                                         | `reviews/continuity.md`      |           |          |
| 14   | line-editor       | `manuscript/chapter-<NN>.md`; `bible/style.md`; `bible/glossary.md`; `project.yaml` (`content_notes`)                                                                                                                                                                                                     | `manuscript/chapter-<NN>.md` | milestone |          |
| R1   | `release`         | `manuscript/chapter-<NN>.md` (front matter); `project.yaml`                                                                                                                                                                                                                                               | `manuscript/chapter-<NN>.md` |           |          |
| R2   | `export`          | `manuscript/*`; `project.yaml`; `bible/timeline.md`; `bible/characters/_roster.md`; `revisions.md`; `references/chapter-notes/…`                                                                                                                                                                          | `export/…`                   |           |          |

### Phase 4 — Arc review (repeat: per-arc)

| Step | Agent          | Reads                                                                                          | Writes                   | Gate      | Repeat |
| ---- | -------------- | ---------------------------------------------------------------------------------------------- | ------------------------ | --------- | ------ |
| V1   | pacing-analyst | `bible/premise.md`; `bible/outline.md`; the arc's chapters, in order                           | `reviews/pacing.md`      |           |        |
| V2   | critic         | `bible/premise.md`; `bible/outline.md`; the arc's chapters; the `## Priorities` of `reviews/*` | `reviews/critique.md`    |           |        |
| V3   | beta-reader    | `bible/premise.md`; the arc's chapters, in order; `references/feedback/…`                      | `reviews/beta-reader.md` | milestone |        |
| V4   | showrunner     | `showrunner-log.md`; the `## Priorities` of `reviews/*`; `project.yaml` (`serial`)             | `showrunner-log.md`      |           |        |

## Notes

- Step 3 runs once per world-layer file the premise needs. In a project with a stack,
  steps 3, 6, and 7 write only the project's own additions, and each is skipped when the
  story has none: original places, systems, and terms, and the ruler's inserts in a
  series begun by a self-contained book (step 3); relationships between original
  characters (step 6); the project's secrets, what original characters know, and its
  own mysteries (step 7). Step 6 writes `voice-guide.md` only in a self-contained
  project; step 7 writes `mysteries.md` only with the mysteries module.
- The gate at step 9 puts the whole plan in front of the author before any prose is
  written.
- The outline at step 2 covers only the first arc. A1 adds each later arc, taking in the
  previous arc review's priorities, and is skipped for the first. A2 runs only in an
  established world.
- Step 11 scans the draft for `TODO` markers. It routes each `needs bible` marker to a
  builder and re-runs step 10, so that none is left before step 13. It surfaces each
  `hidden canon` and `seam conflict` marker to the author; the chapter goes on to steps
  12 and 13, but the marker blocks step 14 until the author has decided, the curator has
  recorded the decision, and the drafter has redrafted the passage.
- Step 12 runs for `timeline.md` always; for `game-state.md`, `timelines.md`,
  `branches.md`, and `mysteries.md` when their modules are enabled; and for each file of
  the project's own entities whose state the chapter changes, for its story-dated rows.
- If step 13 reports problems, the showrunner routes fixes to the drafter and re-runs
  steps 12 and 13 before step 14.
- Approving step 14's gate makes the installment **ready**. R1 runs only at the author's
  word, which may be immediately or months later, and R2 follows every R1. Drafting
  the next installment waits for neither.
- Phase 4 runs when an arc's last installment is ready, released or not. V4 schedules
  revisions of unreleased chapters, sends fixes touching a released chapter forward to
  A1 or an upcoming installment, and, under `serial.released: revisable`, schedules
  revisions of released installments, each followed by R1 (a re-release), a chronicler
  step on `revisions.md`, and R2.
- Under `serial.released: locked`, nothing revises a released installment: a consequence
  that invalidates one is absorbed forward, or accepted by the author.
- **On demand,** beyond the steps above: R1, the `release` skill, runs whenever the author sends chapters to early
  access (or, in a serial, releases, schedules, re-releases, or withdraws them), and R2,
  the `export` skill, after it or whenever the author asks for an export (§13.12,
  §13.13). Renumbering (§13.10), a dialogue pass, a research check, and image prompts
  are inserted by the showrunner when the author or a review asks for them.
