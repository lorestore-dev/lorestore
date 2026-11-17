---
id: crossover
kind: chain
context: universe
---
# Workflow: crossover

Builds or revises a universe's bridge (§13.7).

## Steps

| Step | Agent          | Reads                                                                                                                                          | Writes      | Gate      | Repeat |
| ---- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------- | ------ |
| X1   | bridge-builder | `universe.yaml`; `brief.md`; each base's `index.md`, `glossary.md`, and roster; the world-layer slices behind each mapped concept; `bridge.md` | `bridge.md` | milestone |        |

## Notes

- Before X1, a human writes `universe.yaml` and a short `brief.md`.
- At the gate the author approves the draft, revises it, or rewrites the brief and starts
  again. When the bridge is approved, a human bumps the universe's `version`, and
  projects that stack it re-pin.
