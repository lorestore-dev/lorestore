---
id: short-story
kind: chain
context: project
---
# Workflow: short-story

A compressed chain for a single scene or arc: one chapter, a lighter foundation (§13.2).

## Steps

| Step | Agent              | Reads                                                                                               | Writes                                       | Gate      | Repeat        |
| ---- | ------------------ | --------------------------------------------------------------------------------------------------- | -------------------------------------------- | --------- | ------------- |
| 1    | architect          | `project.yaml`; `references/…` (background)                                                         | `bible/premise.md`                           | milestone |               |
| 2    | architect          | `project.yaml`; `bible/premise.md`                                                                  | `bible/outline.md`                           |           |               |
| 3    | character-designer | `bible/premise.md`; `bible/outline.md`; `bible/characters/_roster.md`                               | `bible/characters/<slug>.md`                 |           | per-character |
| 4    | drafter            | `bible/outline.md`; `bible/style.md`; the cast's snapshots; `bible/glossary.md`                     | `manuscript/chapter-01.md`                   |           |               |
| 5    | showrunner         | `project.yaml`; `showrunner-log.md`; `manuscript/chapter-01.md` (`TODO` markers)                    | `showrunner-log.md`                          |           |               |
| 6    | continuity-editor  | `manuscript/chapter-01.md`; the cast's snapshots; `bible/glossary.md`                               | `reviews/continuity.md`                      |           |               |
| 7    | critic             | `bible/premise.md`; `bible/outline.md`; `manuscript/chapter-01.md`                                  | `reviews/critique.md`                        |           |               |
| 8    | line-editor        | `manuscript/chapter-01.md`; `bible/style.md`; `bible/glossary.md`; `project.yaml` (`content_notes`) | `manuscript/chapter-01.md`                   | milestone |               |
| 9    | line-editor        | `manuscript/chapter-01.md`; `bible/style.md`; `bible/glossary.md`                                   | `manuscript/chapter-01.md` (`status: final`) | milestone |               |

## Notes

- Self-contained short stories that need a setting add worldbuilder steps (inventor
  mode) after step 2, one per world-layer file, as step 3 of `novel`.
- Step 5 routes `TODO` markers as step 11 of `novel` does.
- Step 9 is the finishing pass. The author MAY send the story to early access before it
  (§13.9).
- **On demand:** R1, the `release` skill, runs whenever the author sends chapters to early
  access (or, in a serial, releases, schedules, re-releases, or withdraws them), and R2,
  the `export` skill, after it or whenever the author asks for an export (§13.12,
  §13.13). Renumbering (§13.10), a dialogue pass, a research check, and image prompts
  are inserted by the showrunner when the author or a review asks for them.
