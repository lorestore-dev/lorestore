---
id: novel
kind: chain
context: project
---
# Workflow: novel

A complete book, planned whole, drafted chapter by chapter, reviewed whole, and
finished (§13.1).

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

### Phase 2 — Draft (repeat: per-chapter)

| Step | Agent             | Reads                                                                                                                                                                                                                                                                                                     | Writes                       | Gate      | Repeat   |
| ---- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------- | -------- |
| 10   | drafter           | the chapter's `bible/outline.md` rows; `bible/style.md`; the cast's snapshots at the chapter's cutoff and position; viewpoint characters' `bible/knowledge.md` rows; `bible/glossary.md`; recent `bible/timeline.md` rows; the end of `manuscript/chapter-<NN-1>.md`; the module rows the chapter touches | `manuscript/chapter-<NN>.md` |           |          |
| 11   | showrunner        | `project.yaml`; `showrunner-log.md`; `manuscript/chapter-<NN>.md` (`TODO` markers)                                                                                                                                                                                                                        | `showrunner-log.md`          |           |          |
| 12   | chronicler        | `manuscript/chapter-<NN>.md`; `bible/<ledger>`; `showrunner-log.md` (decisions)                                                                                                                                                                                                                           | `bible/<ledger>`             |           | per-file |
| 13   | continuity-editor | `manuscript/chapter-<NN>.md`; the cast's snapshots; `bible/timeline.md`; `bible/glossary.md`; the module rows the chapter touches                                                                                                                                                                         | `reviews/continuity.md`      |           |          |
| 14   | line-editor       | `manuscript/chapter-<NN>.md`; `bible/style.md`; `bible/glossary.md`; `project.yaml` (`content_notes`)                                                                                                                                                                                                     | `manuscript/chapter-<NN>.md` | milestone |          |

### Phase 3 — Whole-book review

| Step | Agent          | Reads                                                                                                | Writes                   | Gate      | Repeat |
| ---- | -------------- | ---------------------------------------------------------------------------------------------------- | ------------------------ | --------- | ------ |
| 15   | pacing-analyst | `bible/premise.md`; `bible/outline.md`; `manuscript/*` (in full, in order)                           | `reviews/pacing.md`      |           |        |
| 16   | critic         | `bible/premise.md`; `bible/outline.md`; `manuscript/*` (in full); the `## Priorities` of `reviews/*` | `reviews/critique.md`    |           |        |
| 17   | beta-reader    | `bible/premise.md`; `manuscript/*` (in full, in order); `references/feedback/…`                      | `reviews/beta-reader.md` | milestone |        |
| 18   | showrunner     | `showrunner-log.md`; the `## Priorities` of `reviews/*`                                              | `showrunner-log.md`      |           |        |

### Phase 4 — Finish

| Step | Agent       | Reads                                                               | Writes                                         | Gate      | Repeat      |
| ---- | ----------- | ------------------------------------------------------------------- | ---------------------------------------------- | --------- | ----------- |
| 19   | line-editor | `manuscript/chapter-<NN>.md`; `bible/style.md`; `bible/glossary.md` | `manuscript/chapter-<NN>.md` (`status: final`) | milestone | per-chapter |

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
- Step 18 reads every review's priorities, schedules a revision pass, and loops the
  relevant Phase 2 and 3 steps until the priorities are cleared.
- Step 19's gate applies once, after its last instance. Before step 19, the author MAY
  send line-edited chapters to early access (§13.9); step 19 moves an early-access
  chapter to `final` like any other.
- **On demand:** R1, the `release` skill, runs whenever the author sends chapters to early
  access (or, in a serial, releases, schedules, re-releases, or withdraws them), and R2,
  the `export` skill, after it or whenever the author asks for an export (§13.12,
  §13.13). Renumbering (§13.10), a dialogue pass, a research check, and image prompts
  are inserted by the showrunner when the author or a review asks for them.
