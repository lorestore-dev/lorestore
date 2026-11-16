# 7. The snapshot query

The snapshot answers: **what is true of this entity, as of cutoff X, through this stack
of layers, at this point in the manuscript?** It is the only view of canon the prose may
use. It is computed by the `temporal-snapshot` skill, and a host MUST implement it
exactly as specified here.

## 7.1 Inputs

| Input        | Meaning                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| entity `E`   | A character slug, a relationship pair, or another entity in a state-bearing file. It belongs to one base: the base whose fandom defines it, or the project itself |
| position `C` | Optional: the manuscript chapter being written or checked. Defaults to "after the last chapter".           |
| cutoff `X`   | A ruler point of `E`'s base: the cutoff of the sync point for `C` (§6.7), else `setting.cutoff` (or that base's entry in `setting.cutoffs`). In a **branch** (§6.6), never later than the divergence point: if the sync points or setting give a later point, `X` is the divergence point and the host reports the error. In a self-contained project, `X` is the end of its ruler of eras, if it has one (§4.7). In a series begun by a self-contained book, the points are on the series ruler (§4.12). In a frames project, a scene's world point is its `X` (§7.5) |
| order `O`    | The order ruler points compare in: the project order (`setting.order`, §6.8) if there is one, else the highest project layer's order (§6.14), else the base's ruler, with any adaptation timecodes (§4.9) |
| stack `S`    | The project's layers (§2.2): the package layers of `E`'s fandom, any universe layer, and the project layers, in stack order, with the project itself on top |
| mode `M`     | The project's `resolution`: `precedence` (the default), `recency`, or `fill` (§5.4)                        |
| ledgers `L`  | The ledgers of the project layers, each with its pinned chapter, in stack order (§6.4); then the project's own `divergences.md`, if any |

Every comparison of ruler points in this chapter ("later", "latest", "at or before")
uses order `O`.

## 7.2 Algorithm

For entity `E`:

1. **Collect** every state-history row for `E` from the layers of `S`: the package
   layers of `E`'s fandom (the base and every package above it), the universe's
   crossover canon, and the `project` rows of the project and its project layers. Label
   each row with its layer's position in `S` and its source's tier. Packages not in `S`
   contribute nothing: the stack is the filter.
2. **Theory and erratum filter.** Discard rows of tier `theory` or `erratum` (§5.2).
3. **Time filter.** Discard rows whose as-of is later than `X` (§4.2 ordering). Rows
   with an empty as-of (timeless, §4.7) are kept, and so are a self-contained project
   layer's story-dated rows, whose as-of on the series ruler (§4.12) only orders them:
   like its timeless rows, they are anchored items, decided below. Discard story-dated
   rows (§4.11) whose `From chapter` is after `C`, or, for a project layer's rows, after
   its pinned chapter. Set aside a project layer's timeless and story-dated rows whose
   item is ahead of `X` (§6.14), unless the ledgers' Seam conflicts tables carry it
   back, and keep the undecided ones for step 8.
4. **Resolve each attribute**, by `M` (§5.4):
   - **`precedence`** (the default):
     1. Among the layers with at least one remaining row for the attribute, take the
        **highest in `S`**. Within it, take the rows of the **lowest tier** (§5.2).
     2. From those rows, take the one with the **latest as-of**.
   - **`recency`**:
     1. Take the row with the **latest as-of**, from any layer.
     2. If several rows share that as-of, take the one from the highest layer, then the
        lowest tier.
   - **`fill`**:
     1. Among the layers with at least one remaining row for the attribute, take the
        **lowest in `S`**. Within it, take the rows of the **lowest tier**.
     2. From those rows, take the one with the **latest as-of**.

   In every mode, timeless rows (empty as-of) sort before every ruler point, and
   story-dated rows after every ruler point, in chapter order (§4.11). If the
   chosen row's value is `(unset)`, the attribute is absent.

   **Ties.** A valid package never holds two rows with the chosen row's tier and as-of
   and a different value (§4.4). If the host finds such rows, it reports the package
   as invalid (§14.2) and does not resolve the attribute.
5. **Apply the ledgers**, in order: each project layer's ledger as of its pinned
   chapter, then the project's own as of `C`. For each divergence whose *first occurs*
   is at or before that chapter, and whose *until* (if any) is after it, apply each
   `Overrides` assignment for `E`, replacing the attribute's value. A project layer's
   divergence anchored after `X` applies only if the Seam conflicts tables carry it
   back (§6.14). Keep the undecided ones for step 8. Attach divergences
   without machine overrides (`Overrides` = `—`) that mention `E` to the result as
   notes, together with their open consequences.
6. **Return** the resolved attributes, each annotated with its provenance: layer,
   source, tier, as-of, and citation, or the divergence id (qualified by project for an
   earlier book's, `two-witnesses:D1`) for overridden values.
7. **Return hidden truths separately.** List the rows that passed the step 2 filter
   whose `True from` is at or before `X` but whose `As of` is after it: facts already
   true at the cutoff that the story has not yet revealed. They are marked hidden and
   are **not** part of the resolved state. Agents MUST NOT use them unless the author
   has decided how (§6.12). Rows already decided in a Hidden canon table of `L`
   (§6.4) carry that decision with them.
8. **Return seam conflicts separately.** List each item set aside in step 3 or 5 that
   no Seam conflicts table of `L` has decided, with its anchor and the rows or
   overrides it holds. Agents MUST NOT use them until the author decides (§6.14).

*Example.* The books set an attribute at `PS:2`, and a fanon package stacked above the
books changes it at `GoF:3`. At a `GoF:10` cutoff, `precedence` resolves to the fanon
value, because the fanon layer is higher. `recency` also resolves to the fanon value,
because it is later. Had the books changed the attribute again at `GoF:5`, `precedence`
would still give the fanon value, but `recency` would give the books' `GoF:5` value. At
a `PoA` cutoff both resolve to the books' value, because the fanon row has not happened
yet. `fill` gives the books' value at every cutoff, because the books have a row. Under
every mode, a ledger override from step 5 wins.

## 7.3 Relationships and knowledge

Relationships and knowledge are entities like any other, and resolve the same way:

- A **relationship** is keyed by its pair (§10.5). A scene at `PS:3` sees Harry and Ron as
  `strangers`, because they meet at `PS:6`. Using a bond before it forms is a temporal
  leak.
- **Knowledge** is keyed by character and secret. A character's state for a secret
  (`unaware`, `suspects`, `knows`) resolves at the cutoff like any attribute.

**Reveal aliases are never joined by the snapshot.** A surface identity (the Moody who
teaches in *Goblet of Fire*) and the true identity it conceals (Barty Crouch Jr.) are
separate entities, and each resolves only from its own rows, before and after the
reveal. Joining them is a judgment left to agents. The roster's `Reveal of` and
`Revealed at` columns (§10.9) tell the drafter and canon-keeper when the connection
becomes known, and to whom `knowledge.md` says it is known.

## 7.4 Crossovers: one cutoff per base

With a universe layer there is no single cutoff. `setting.cutoffs` maps each base
to its own cutoff:

```yaml
cutoffs: { harry-potter: "HBP:7", star-trek: "TNG:4:1" }
```

Here a Harry Potter entity resolves at `HBP:7` against the Harry Potter ruler, and a
Star Trek entity resolves at `TNG:4:1` against the Star Trek ruler. The two cutoffs are
never compared with each other.

Every entity belongs to exactly one base. Resolve it against **its own base's** ruler
and cutoff, through the layers of its own fandom: a Star Trek fanon package in the stack
never touches a Harry Potter entity. Then apply the bridge (§8): concept mappings, and
crossover-only canon (source tier `crossover`). The ledgers apply last.

## 7.5 Frames: two cutoffs at once

Everything above assumes that every character in a scene lives at the same moment, so
one cutoff serves them all. Time travel breaks that assumption. A character who has come
back from the future is physically present at the scene's moment, but **remembers**
events that, for everyone else in the scene, have not happened yet. The same holds for
anyone who crosses between timelines. Each such character has their own **frame of
reference**: the point in history their knowledge is bounded by. The frames module
(§9.1) records these frames, and the snapshot resolves a scene against more than one
cutoff at once.

A scene declares a **world point** `<ruler-point>@<branch>`, which is the frame of the
scene and of everyone native to it. It also declares its **travelers**: characters in
the scene who are not native to its moment. Each traveler carries a **personal cutoff**,
recorded in `timelines.md`, which is their own frame. Resolve in two passes:

1. **World pass:** every native and the setting resolve at the world point.
2. **Traveler pass:** each traveler's *knowledge and memory* resolve at their personal
   cutoff. Their *physical presence* follows the scene. Any ripples whose chapter has
   been reached (`feedback` mechanisms, §9.1) then apply to the traveler, before the
   ledger.

The composite: **natives are bounded by world time; travelers by their own personal
time.**

**The world point and the sync point.** Within a scene, the world point's ruler point is
`X`, and its branch selects the history (§10.16). The chapter's sync point (§6.7) gives
the cutoff for everything outside a scene, such as the outline and the ledger audits,
and is where a drafter starts when setting a scene's world point. A host SHOULD warn
when a scene with no travelers has a world point later than its chapter's sync-point
cutoff: that is legitimate only for a deliberate flash-forward.

*Examples.*
- **Magic.** In *Prisoner of Azkaban*, Harry and Hermione use a Time-Turner to relive
  the evening (PoA ch.21). At a scene during the replayed hours, the natives, including
  their own earlier selves, resolve at that point. The travelers carry a personal cutoff
  at the moment they turned the hourglass, so they already know how the evening ends.
- **Technology.** In TNG "Yesterday's Enterprise" (`TNG:3:15`), the Enterprise-C comes
  through a temporal rift into an altered timeline. The Enterprise-D crew are natives at
  `TNG:3:15@alt-war`. Captain Garrett is a traveler whose personal cutoff is the last
  ruler point before her ship left its own time, so she knows nothing of the war her
  disappearance caused.

## 7.6 The composed bible and materialized snapshots

Two caches save agents from reading every layer separately. Both are **rebuildable,
never canon** (§3.1, W5), and both MUST be regenerated, or treated as stale, when any
input they record changes.

### The composed bible

`derived/bible/` is the whole stack merged into one bible, built by the `compose` skill
(§11.10). Agents in project context read it through `bible/<path>` (§2.6).

- **One file per world-layer path** that any layer holds, plus the project's own
  story-layer files. Each file is the union of that path across the stack (§2.7): the
  base's rows first, then each higher layer's in stack order, then the project's own.
- **Every row keeps its provenance.** Tables gain a final `Layer` column naming the
  layer each row came from (`harry-potter`, `harry-potter/fanon`,
  `project:two-witnesses`, or `project` for the project itself). Entry blocks gain a
  `- layer:` key. An extension sheet's rows are merged into the sheet of the layer that
  defines the character.
- **It is a union, not a resolution.** Every row of every layer appears, including
  rows that lose. The snapshot (§7.2) still decides what is true at a cutoff; the
  composed bible only saves the reads. Project-layer ledgers are composed into
  `divergences.md` as read-only rows, with their ids qualified by project.
- **Key collisions are errors.** A key defined by two layers (§2.7) is reported, not
  composed.
- **Its header records every input.** `derived/bible/_composed.md` lists each layer
  reference with its version or pinned chapter, the resolution mode, the project order
  and the project layer it is inherited from, if it is (§6.14), and the revision of the
  project's own `bible/`, including its sync points and ledger.
- **It is rebuilt** when a pin changes, when a layer it records changes, or when the
  project's own bible changes. The chronicler's step and every step that writes the
  project's bible trigger a rebuild; a host MAY instead rebuild on the next read.

### Materialized snapshots

A host MAY materialize a snapshot to a file, by running the `temporal-snapshot` skill
(§11.10), so the drafter can read it directly, which gives a smaller context and no
temporal reasoning per call:

```
derived/as-of-<base-id>-<point>[-<chapter>].md
```

`<base-id>` is the entity's base or, in a series begun by a self-contained book, the
first book's id (§4.12).

The file MUST begin with a header recording every input: the stack (each layer with its
version or pinned chapter), the resolution mode, the project order (and where it is
inherited from), the cutoff and the sync point it came from, the world point (frames),
the position, and the revision of each ledger, seam decisions included.
