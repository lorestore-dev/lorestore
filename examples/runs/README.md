# Runs of the tool-less loop

Each directory here is a copy of an example project with a run of
[tools/loop.py](../../tools/loop.py) recorded in it, to show the model-agnostic claim of
[§11.1](../../spec/11-agent-contract.md#111-the-loop) at work. The checker
doesn't read these copies; the projects it checks are in [projects/](../projects/).
Each copy keeps the spec version and pins it was run at, so `three-brothers` stays at
0.3 (D131).

## `three-brothers`, run 1

The `short-story` workflow with the established-world overlay, run end to end on a copy
of [three-brothers](../projects/three-brothers/) in exchange mode, from the seed in
`project.yaml` to a chapter with `status: final`. For each step,
`runs/run-1/<n>-<step>.prompt.md` is exactly what the model was given: the agent file,
the step's inputs resolved to slices, and the standing instruction. Beside it,
`<n>-<step>.reply.md` is the reply, written from the prompt alone. The run's own record
is in `runs/run-1/log.md`; the prompts and replies of steps that were later re-run are
in `runs/run-1/superseded/pass-<n>/`.

```
python tools/loop.py examples/runs/three-brothers --approve \
  --skip "E1=the story stays at one cutoff, DH:36 (judged from the outline: one scene)"
python tools/loop.py examples/runs/three-brothers --approve --from <step>   # a scheduled re-run
```

`--approve` passes every gate; the log records it as a demonstration, not an author's
signal.

### How it went

1. **Foundation.**
   - E0 composes the stack.
   - The architect writes the premise (1) and the outline (2).
   - E1, E1a, E1b, E2b, and step 4 are skipped, each with its reason in the log.
   - The worldbuilder confirms the ledger (E2).
   - The canon-keeper's theory audit (E2a) finds no new conflicts.
2. **First draft: blocked.**
   - The story is set in DH ch.35, which the abridged `harry-potter` package didn't
     cover, so the drafter marked six `needs bible` gaps rather than invent canon.
   - The showrunner routed the canon gaps to a package update.
   - The loop stopped at step 13, as §11.9 requires.
3. **The author's part, outside the loop.**
   - The package gained DH ch.35: `albus-dumbledore`, `places.md` (`kings-cross-limbo`),
     two secrets in `knowledge.md`, and the Hallows terms.
   - The chain gained step 9 (D128), which wrote the style guide.
   - The draft was re-run, with no markers.
4. **Reviews: two fixes, both in the package.**
   - Continuity (13) and canon (E3) found the draft at odds with two stale or missing
     rows: Dumbledore's hands at King's Cross, and Voldemort's body after GoF.
   - The showrunner (E4) surfaced them to the author.
   - The package gained both rows, and 13, E3, and E4 re-ran clean.
   - E5 marked D1's consequence absorbed.
5. **Critique and revision.**
   - The critic (16) found three structural problems, and the showrunner (18) sent them
     back to the drafter.
   - The drafter revised, with the draft and the showrunner's notes among its inputs
     (D130).
   - The reviews re-ran, and the critic's two remaining notes went to the line-editor.
6. **Finish.** The line-editor polished the chapter (14), then made the finishing pass
   (19).

### What it found

Recorded in [DECISIONS.md](../../DECISIONS.md), D124 to D130:
- three chain gaps: short-story's numbering, its missing style step, and its missing
  routing step;
- two reads gaps: the drafter's ledger in an established world, and the consequences E5
  needs;
- the rule for scheduled revisions;
- a gap in the checker's snapshot, which ignored `places.md`.

One limit stays in the loop: it finds the cast by name, so after the revision referred to
Voldemort only as "he", his snapshot dropped out of the reviews' inputs. The canon-keeper
said so. A host needs better cast resolution than name matching.
