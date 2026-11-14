# 8. Crossovers: universes and the bridge

A **universe** composes one or more world packages and a **bridge** that reconciles
them. Because worlds are separate packages, a crossover is **composition, not
duplication**: extract each world once, then cross them over in as many ways as you
like.

```
universes/<universe-id>/
├── universe.yaml     # the manifest (§10.2.1)
├── brief.md          # the author's crossover brief (free prose, human-written)
└── bridge.md         # the reconciliation (§10.14), drafted by the bridge-builder
```

## 8.1 The manifest

`universe.yaml` has its own semantic version, bumped by the same rules as a world
package (§2.8) whenever the manifest or the bridge changes. It lists the member worlds,
pins each one's version, and gives each an **offset** that aligns its calendar to the
universe's shared "now":

```yaml
spec_version: "0.1"
id: wizards-and-warp
name: "Wizards and Warp"
version: 1.0.0
worlds:
  - { id: harry-potter, version: 2.1.0, offset: "+373y" }
  - { id: star-trek,    version: 1.4.0, offset: "+0y" }
bridge: bridge.md
```

`offset` is `[+-]<n><y|m|d>`: how far the world's own internal calendar is shifted to
line up with the universe's. Here Harry Potter is moved forward 373 years, so that
Hogwarts in 1991 lines up with the Enterprise-D in 2364. Offsets relate in-world dates;
they do not make canon points from different worlds comparable (§4.2).

This pairing is the clearest test of a bridge: a **magic** world and a **technology**
world have to agree on what happens when a spell meets a tricorder.

## 8.2 The bridge

`bridge.md` holds four kinds of content (format: §10.14):

1. **Concept mappings** between worlds:

   | Relation | Meaning                         | Example                                                          |
   | -------- | ------------------------------- | ---------------------------------------------------------------- |
   | `≡`      | Same thing                      | `harry-potter:muggle ≡ star-trek:human` (non-magical humans)     |
   | `→`      | One is explained by the other   | `harry-potter:apparition → star-trek:subspace` (it is a fold in subspace) |
   | `∥`      | Deliberately kept separate      | `harry-potter:magic ∥ star-trek:technology` (neither explains the other) |

2. **Crossover-only canon**: facts that exist in neither source world. Their source is
   the universe's bridge source (tier `crossover`), and characters created here have
   `origin: crossover`.
3. **Collisions and disambiguation**: names that clash between worlds, and how each
   resolves.
4. **Consistency rules**: constraints that hold across the composition.

## 8.3 Rules

- **Per-world resolution.** Every entity belongs to exactly one world and resolves
  against that world's ruler, cutoff, and profile (§7.4).
- **World-qualified references.** In a universe project, world-layer agent paths are
  world-qualified (`bible/@<world-id>/…`, §2.6), and slugs referenced from the story layer
  are qualified as `<world-id>:<slug>`.
- **Crossover canon never leaks back.** Bridge facts MUST NOT appear in a single-world
  project set in either world. The canon-keeper flags them as a crossover leak (§6.9).
- **The bridge is world-layer.** Projects set in the universe read it but MUST NOT write
  it. A project's own departures go in its divergence ledger as usual.
- **Reveal and identity joins stay with agents.** The bridge maps concepts and resolves
  name collisions. It never merges two worlds' entities into one; a character who is
  "the same person" in both worlds is two entities linked by a concept mapping.

## 8.4 Building the bridge

The **bridge-builder** agent (§12.19) drafts `bridge.md` in the crossover workflow
(§13.7). It reads the author's `brief.md` (what the crossover is about, how the worlds
meet, any crossover-only facts wanted) and the member worlds. It then proposes concept
mappings, collisions, and consistency rules. A human approves the draft at a milestone
gate, revises it, or sends it back. The agent proposes and the author decides: crossover
canon is added only when the brief asks for it.
