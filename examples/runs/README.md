# Runs of the tool-less loop

Each directory here is a copy of an example project with a run of
[tools/loop.py](../../tools/loop.py) recorded in it, to show the model-agnostic claim of
[§11.1](../../spec/11-agent-contract.md#111-the-loop) at work. The checker
doesn't read these copies; the projects it checks are in [projects/](../projects/).

## `three-brothers`, run 1

The `short-story` workflow with the established-world overlay, run on a copy of
[three-brothers](../projects/three-brothers/) in exchange mode. For each step,
`runs/run-1/<n>-<step>.prompt.md` is exactly what the model was given: the agent file,
the step's inputs resolved to slices, and the standing instruction. Beside it,
`<n>-<step>.reply.md` is the reply, written from the prompt alone. The run's own record
is in `runs/run-1/log.md`.

```
python tools/loop.py examples/runs/three-brothers --approve \
  --skip "E1=the story stays at one cutoff, DH:36 (judged from the outline: one scene)"
```

`--approve` passes every gate; the log records it as a demonstration, not an author's
signal. The steps:

| Step | Agent             | Result                                                                     |
| ---- | ----------------- | -------------------------------------------------------------------------- |
| E0   | `compose`         | `derived/bible/`, from the two layers                                       |
| 1    | architect         | `bible/premise.md`                                                         |
| 2    | architect         | `bible/outline.md`: one chapter, one scene                                 |
| E1   | architect         | skipped, by judgment (`--skip`)                                            |
| E1a  | canon-keeper      | skipped: the project has no order of its own                               |
| E1b  | canon-keeper      | skipped: the project has no project layers                                 |
| E2   | worldbuilder      | `bible/divergences.md`, unchanged: the planned divergence was already logged |
| E2a  | canon-keeper      | `reviews/canon.md`: the theory audit, with no new conflicts                |
| E2b  | worldbuilder      | skipped: E2a raised nothing for the author                                 |
| 4    | character-designer | skipped: no original characters                                           |
| 10   | drafter           | `manuscript/chapter-01.md`, with six `needs bible` markers                 |
| 11   | showrunner        | `showrunner-log.md`: the canon gaps routed to an extraction run            |
| 13   | continuity-editor | blocked: the markers must be resolved first (§11.9)                        |

The run stops at step 13, as the spec requires. The story is set in DH ch.35, which
the abridged `harry-potter` package does not cover, so the drafter could not use canon
it does not have, and marked the gaps instead. What the run found is recorded as D124
to D127 in [DECISIONS.md](../../DECISIONS.md).
