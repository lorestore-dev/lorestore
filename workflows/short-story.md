---
id: short-story
kind: chain
context: project
---
# Workflow: short-story

A compressed chain for a single scene or arc: one chapter, a lighter foundation (§13.2).
Its steps are a selection of `novel`'s, under the same numbers, so the overlays apply
unchanged. The table's order is the order the steps run in.

## Steps

| Step | Agent              | Reads                                                                                                  | Writes                                       | Gate      | Repeat        |
| ---- | ------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------------- | --------- | ------------- |
| 1    | architect          | `project.yaml`; `references/…` (background)                                                            | `bible/premise.md`                           | milestone |               |
| 2    | architect          | `project.yaml`; `bible/premise.md`                                                                     | `bible/outline.md`                           |           |               |
| 4    | character-designer | `bible/premise.md`; `bible/outline.md`; `bible/characters/_roster.md`                                  | `bible/characters/<slug>.md`                 |           | per-character |
| 9    | line-editor        | `project.yaml` (parameters); `bible/premise.md`; `bible/voice-guide.md`; `bible/glossary.md`           | `bible/style.md`                             | milestone |               |
| 10   | drafter            | `bible/outline.md`; `bible/style.md`; the cast's snapshots; `bible/knowledge.md`; `bible/glossary.md`  | `manuscript/chapter-01.md`                   |           |               |
| 11   | showrunner         | `project.yaml`; `showrunner-log.md`; `manuscript/chapter-01.md` (`TODO` markers)                       | `showrunner-log.md`                          |           |               |
| 13   | continuity-editor  | `manuscript/chapter-01.md`; the cast's snapshots; `bible/glossary.md`                                  | `reviews/continuity.md`                      |           |               |
| 16   | critic             | `bible/premise.md`; `bible/outline.md`; `manuscript/chapter-01.md`; the `## Priorities` of `reviews/*` | `reviews/critique.md`                        |           |               |
| 18   | showrunner         | `showrunner-log.md`; the `## Priorities` of `reviews/*`                                                | `showrunner-log.md`                          |           |               |
| 14   | line-editor        | `manuscript/chapter-01.md`; `bible/style.md`; `bible/glossary.md`; `project.yaml` (`content_notes`)    | `manuscript/chapter-01.md`                   | milestone |               |
| 19   | line-editor        | `manuscript/chapter-01.md`; `bible/style.md`; `bible/glossary.md`                                      | `manuscript/chapter-01.md` (`status: final`) | milestone |               |

## Notes

- Self-contained short stories that need a setting add worldbuilder steps (inventor
  mode) after step 2, one per world-layer file, as step 3 of `novel`.
- Step 4 runs once per original character; a story whose cast is all canon skips it.
- Step 9 sets the voice contract before the draft, as in `novel`: the drafter writes to
  it, and the line-editor polishes to it.
- Step 11 routes `TODO` markers as in `novel`: each `needs bible` marker to a builder,
  then a re-draft, before step 13; each `hidden canon` and `seam conflict` marker to
  the author, blocking step 14 until decided.
- The critic (step 16) reads the chapter before it is polished. The showrunner (step
  18) reads every review's priorities and, if step 13 or 16 reports problems, routes
  fixes to the drafter and re-runs the reviews before step 14.
- Step 19 is the finishing pass. The author MAY send the story to early access before it
  (§13.9).
- **On demand:** R1, the `release` skill, runs whenever the author sends chapters to early
  access (or, in a serial, releases, schedules, re-releases, or withdraws them), and R2,
  the `export` skill, after it or whenever the author asks for an export (§13.12,
  §13.13). Renumbering (§13.10), a dialogue pass, a research check, and image prompts
  are inserted by the showrunner when the author or a review asks for them.
