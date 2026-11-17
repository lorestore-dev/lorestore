---
id: established-world
kind: overlay
context: project
---
# Workflow: established-world

Applies to any chain when `setting.type: established`. It makes the worldbuilder a
curator, adds the canon-keeper to review, and runs the living-canon loop (§13.4, §6.11).

## Steps

| Step | Agent        | Reads                                                                                                                                  | Writes                 | Gate      | Repeat | Position  |
| ---- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | --------- | ------ | --------- |
| E0   | `compose`    | `project.yaml`; the stack's layers; `bible/…`                                                                                          | `derived/bible/…`      |           |        | before 1  |
| E1   | architect    | `project.yaml` (`setting`); `bible/outline.md`; `bible/canon-timeline.md`; `plot-architecture.md` (the stretch the story covers)       | `bible/sync-points.md` | milestone |        | after 2   |
| E1a  | canon-keeper | `project.yaml` (`setting.order`); `bible/sync-points.md`; `bible/canon-timeline.md`; the host's inversion candidates                   | `reviews/canon.md`     | milestone |        | after E1  |
| E1b  | canon-keeper | `project.yaml` (layers); `bible/sync-points.md`; the earlier books' ledgers; `bible/divergences.md`                                    | `reviews/canon.md`     | milestone |        | after E1a |
| E2   | worldbuilder | `bible/premise.md`; `bible/outline.md`; `bible/divergences.md`; `reviews/canon.md` (the author's decisions)                            | `bible/divergences.md` |           |        | after E1b |
| E2a  | canon-keeper | `bible/divergences.md`; `bible/sync-points.md`; the canon ahead; the host's reach candidates; the cited theories' claims               | `reviews/canon.md`     | milestone |        | after E2  |
| E2b  | worldbuilder | `bible/divergences.md`; `reviews/canon.md` (the author's decisions)                                                                    | `bible/divergences.md` |           |        | after E2a |
| E3   | canon-keeper | `manuscript/chapter-<NN>.md`; `bible/divergences.md`; `bible/sync-points.md`; the cast's snapshots; `bible/sources.md`; `project.yaml` | `reviews/canon.md`     |           |        | after 13  |
| E4   | showrunner   | `showrunner-log.md`; `reviews/canon.md` (`## Findings`, `## Consequences honored`)                                                     | `showrunner-log.md`    |           |        | after E3  |
| E5   | worldbuilder | `bible/divergences.md`; `showrunner-log.md` (accepted divergences, absorbed consequences)                                              | `bible/divergences.md` |           |        | after E4  |
| E6   | worldbuilder | `bible/outline.md` (the new arc); `bible/divergences.md`                                                                               | `bible/divergences.md` |           |        | after A1  |
| E6a  | canon-keeper | `bible/sync-points.md`; `bible/divergences.md`; the canon the arc reaches; the host's candidates                                       | `reviews/canon.md`     | milestone |        | after A2  |
| E6b  | worldbuilder | `bible/divergences.md`; `reviews/canon.md` (the author's decisions)                                                                    | `bible/divergences.md` |           |        | after E6a |

## Added reads

Appended to these steps of the chain (§11.7), so that the plan and the prose know what
the story changes in canon:

| Step | Reads                                                                                                    |
| ---- | -------------------------------------------------------------------------------------------------------- |
| 2    | `bible/divergences.md`; `bible/canon-timeline.md`; `plot-architecture.md` (the stretch the story covers) |
| 10   | `bible/divergences.md` (the divergences and open consequences that touch the cast)                       |

## Notes

- Steps 3, 6, and 7 of the chain write only the project's own additions; steps 4 and 5
  write only original characters and their roster rows. The world comes from the stack,
  and the adherence settings are the author's, in `project.yaml`.
- **E0** runs before step 1, and the showrunner re-runs it whenever a layer's pin or the
  project's own `bible/` changes. A `temporal-snapshot` step MAY precede step 10 to
  materialize the cast's snapshots.
- **E1** is skipped when the story stays at one cutoff.
- **E1a** runs only when the project has its own order. Its gate waits for the author to
  decide each inversion, under every gate policy. An author who reorders changes
  `setting.order` and sends the run `back: E1`. A project that inherits its order from a
  project layer skips E1a unless it sets a different one.
- **E1b** runs only with project layers. Its gate waits for the author to decide each
  seam. When the sync points or a layer's pin change, the showrunner re-runs E1b and E2.
- **E2** records the seam decisions and logs the planned divergences, with their
  consequences, and the author's resolution of each order inversion.
- **E2a** and **E2b** run in a retelling with divergences in force, and, for the theory
  audit, whenever a planned divergence's `Basis` cites a theory. The showrunner repeats
  them until E2a finds nothing new, and re-runs them whenever a divergence is logged
  later. With project layers, E2a also runs for the earlier books' divergences.
- **E3** classifies the chapter's problems; **E4** routes fix items and resolves or
  surfaces decide items. A pending decide item blocks step 14.
- **E5** runs only when E4 accepted an emergent divergence or consequences were
  absorbed. The showrunner then schedules revisions for any written chapter an open
  consequence invalidates.
- **E6–E6b** run only in `serial`, once per arc after the first. The showrunner repeats
  E6a and E6b until E6a finds nothing new.
- Every decision of an order inversion, divergence conflict, hidden canon, theory
  conflict, or seam conflict is the author's, under every gate policy. No agent makes
  one.
