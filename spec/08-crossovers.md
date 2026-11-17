# 8. Crossovers: universes and the bridge

A **universe** is a layer that relies on two or more bases and reconciles them with a
**bridge**. Because bases are separate packages, a crossover is **composition, not
duplication**: extract each world once, then cross them over in as many ways as you
like.

```
universes/<universe-id>/
├── universe.yaml     # the manifest (§10.2.1)
├── brief.md          # the author's crossover brief (free prose, human-written)
└── bridge.md         # the reconciliation (§10.14), drafted by the bridge-builder
```

A project uses a universe by stacking it above its bases, like any other layer (§2.2):

```yaml
layers:
  - harry-potter@3.2.2
  - star-trek@2.1.2
  - universe:wizards-and-warp@2.0.4
```

Each base's other packages can be stacked too, in any order that keeps every package
above what it relies on. A Harry Potter fanon package only ever applies to Harry Potter
entities (§7.4).

## 8.1 The manifest

`universe.yaml` has its own semantic version, bumped by the same rules as a package
(§2.8) whenever the manifest or the bridge changes. It pins the bases it relies on, and
gives each an **offset** that aligns its calendar to the universe's shared "now":

```yaml
spec_version: "0.4"
id: wizards-and-warp
kind: universe
name: "Wizards and Warp"
version: 2.0.0
relies-on:
  - harry-potter@3.2.2
  - star-trek@2.1.2
offsets: { harry-potter: "+373y", star-trek: "+0y" }
bridge: bridge.md
```

`offset` is `[+-]<n><y|m|d>`: how far the base's dates (§4.13) are shifted to line up
with the universe's. A base with no entry has `+0y`. Here Harry Potter is moved forward
373 years, so that Hogwarts in 1991 lines up with the Enterprise-D in 2364.

- Offsets need dates to apply to. A universe MAY give offsets only if every base it
  relies on declares the same calendar: `iso`, or identical custom calendars. A unit
  MUST be one the calendar has: a custom calendar without months takes only `y`.
- A base's date plus its offset is a date in **universe time**. A universe's chronology
  merges every base's world history (§4.13), each event moved into universe time. Dates
  in the bridge are in universe time.
- Offsets relate in-world dates. They do not make ruler points from different bases
  comparable (§4.2).

A universe relies only on bases. Its `relies-on` pins MUST match the bases' pins in any
stack that uses it (§2.2).

This pairing is the clearest test of a bridge: a **magic** world and a **technology**
world have to agree on what happens when a spell meets a tricorder.

**Example cases:** [W7](../examples/README.md#case-w7).

## 8.2 The bridge

`bridge.md` holds four kinds of content (format: §10.14):

1. **Concept mappings** between bases:

   | Relation | Meaning                         | Example                                                          |
   | -------- | ------------------------------- | ---------------------------------------------------------------- |
   | `≡`      | Same thing                      | `harry-potter:muggle ≡ star-trek:human` (non-magical humans)     |
   | `→`      | One is explained by the other   | `harry-potter:apparition → star-trek:subspace` (it is a fold in subspace) |
   | `∥`      | Deliberately kept separate      | `harry-potter:magic ∥ star-trek:technology` (neither explains the other) |

2. **Crossover-only canon**: facts that exist in neither base. Their source is the
   reserved id `bridge` (tier `crossover`), and characters created here have
   `origin: crossover`.
3. **Collisions and disambiguation**: names that clash between bases, and how each
   resolves.
4. **Consistency rules**: constraints that hold across the composition.

## 8.3 Rules

- **Per-base resolution.** Every entity belongs to exactly one base and resolves
  against that base's ruler and cutoff, through the layers of its own fandom (§7.4).
- **Base-qualified references.** With a universe layer, world-layer agent paths are
  base-qualified (`bible/@<base-id>/…`, §2.6), and slugs referenced from the story layer
  are qualified as `<base-id>:<slug>`.
- **Crossover canon never leaks back.** Bridge facts MUST NOT appear in a project whose
  stack lacks the universe. The canon-keeper flags them as a crossover leak (§6.9).
- **The bridge is read-only to projects.** Projects that stack the universe read it but
  MUST NOT write it. A project's own departures go in its divergence ledger as usual.
- **Reveal and identity joins stay with agents.** The bridge maps concepts and resolves
  name collisions. It never merges two bases' entities into one; a character who is
  "the same person" in both worlds is two entities linked by a concept mapping.

## 8.4 Building the bridge

The **bridge-builder** agent (§12.19) drafts `bridge.md` in the crossover workflow
(§13.7). It reads the author's `brief.md` (what the crossover is about, how the worlds
meet, any crossover-only facts wanted) and the bases. It then proposes concept
mappings, collisions, and consistency rules. A human approves the draft at a milestone
gate, revises it, or sends it back. The agent proposes and the author decides: crossover
canon is added only when the brief asks for it.
