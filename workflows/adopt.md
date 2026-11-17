---
id: adopt
kind: chain
context: project
---
# Workflow: adopt

Brings an existing story into LoreStore, reconstructing the bible from the manuscript,
and then hands over to the project's own workflow (§13.8). It runs once.

## Steps

### Phase 1 — Reconstruct

| Step | Agent              | Reads                                                                                     | Writes                                           | Gate      | Repeat        |
| ---- | ------------------ | ----------------------------------------------------------------------------------------- | ------------------------------------------------ | --------- | ------------- |
| P0   | `compose`          | `project.yaml`; the stack's layers                                                        | `derived/bible/…`                                |           |               |
| P1   | architect          | `project.yaml`; `manuscript/*`                                                            | `bible/premise.md`                               | milestone |               |
| P2   | architect          | `bible/premise.md`; `manuscript/*`                                                        | `bible/outline.md`                               | milestone |               |
| P3   | character-designer | `bible/premise.md`; `bible/outline.md`; `manuscript/*` (the character's scenes)           | `bible/characters/<slug>.md`                     |           | per-character |
| P4   | character-designer | `bible/characters/*.md`; `bible/characters/_roster.md`                                    | `bible/characters/_roster.md`                    |           |               |
| P4a  | character-designer | `bible/characters/*.md`; `manuscript/*`                                                   | `bible/relationships.md`, `bible/voice-guide.md` |           | per-file      |
| P4b  | architect          | `bible/premise.md`; `bible/outline.md`; `bible/characters/_roster.md`; `manuscript/*`     | `bible/knowledge.md`, `bible/mysteries.md`       |           | per-file      |
| P5   | worldbuilder       | `bible/index.md`; `bible/premise.md`; `bible/outline.md`; `manuscript/*`; `bible/<file>`  | `bible/<file>` (inventor)                        | milestone | per-file      |
| P6   | architect          | `project.yaml` (`setting`); `bible/outline.md`; `bible/canon-timeline.md`; `manuscript/*` | `bible/sync-points.md`                           | milestone |               |
| P7   | line-editor        | `manuscript/*`; `bible/glossary.md`                                                       | `bible/style.md`                                 | milestone |               |

### Phase 2 — Walk the chapters (repeat: per-chapter)

| Step | Agent             | Reads                                                                                                              | Writes                           | Gate | Repeat   |
| ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------- | ---- | -------- |
| P8   | chronicler        | `manuscript/chapter-<NN>.md`; `bible/<ledger>`                                                                     | `bible/<ledger>`                 |      | per-file |
| P8a  | continuity-editor | `manuscript/chapter-<NN>.md`; the cast's snapshots; `bible/timeline.md`; `bible/glossary.md`                       | `reviews/continuity.md`          |      |          |
| P9   | canon-keeper      | `manuscript/chapter-<NN>.md`; `bible/divergences.md`; `bible/sync-points.md`; the cast's snapshots; `project.yaml` | `reviews/canon.md`               |      |          |
| P10  | showrunner        | `showrunner-log.md`; `reviews/canon.md` (`## Findings`); `reviews/continuity.md`                                   | `showrunner-log.md`              |      |          |
| P11  | worldbuilder      | `bible/divergences.md`; `showrunner-log.md` (what the author accepted)                                             | `bible/divergences.md` (curator) |      |          |

## Notes

- Before it runs, a human writes `project.yaml` and imports the chapters into
  `manuscript/`, each with the status it really has. The host checks the order rules on
  import.
- **P1–P2** reconstruct the premise and outline from what the chapters do; the outline
  MAY plan ahead. **P3–P4b** write the original characters, their relationships, and
  what they know as chapter 1 opens; P8 adds what each chapter changes. **P5** writes
  the world-layer files the chapters rely on. **P6** runs only in an established world.
  **P7** codifies the voice the chapters already have.
- **P8–P11** walk the chapters in order. P9–P11 run only in an established world. The
  canon-keeper reports every departure from canon as an emergent divergence; the
  showrunner surfaces them to the author, who normally accepts them, but no agent
  decides that. The curator logs what the author accepts.
- Adoption never rewrites an imported chapter.
- After the last chapter, an established project runs the overlay's audits for the
  canon ahead (E1a, E1b and E2, then E2a and E2b, as they apply), and the project
  continues in its own workflow.
