# 7. The snapshot query

The snapshot answers: **what is true of this entity, as of cutoff X, under profile P,
at this point in the manuscript?** It is the only view of canon the prose may use. It is
computed by the `temporal-snapshot` skill, and a host MUST implement it exactly as
specified here.

## 7.1 Inputs

| Input        | Meaning                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| entity `E`   | A character slug, a relationship pair, or another entity in a state-bearing file                           |
| position `C` | Optional: the manuscript chapter being written or checked. Defaults to "after the last chapter".           |
| cutoff `X`   | A canon point of `E`'s world: the canon track's cutoff for `C` (§6.7), else `setting.canon_point` (or that world's entry in `setting.canon_points`). In a **branch** (§6.6), never later than the divergence point: if the track or setting gives a later point, `X` is the divergence point and the host reports the error |
| order `O`    | The order canon points compare in: the project order from the canon track (§6.8) if there is one, else the ruler's |
| profile `P`  | The selected profile's ordered source list (§5.4)                                                          |
| ledger `L`   | The project's `divergences.md`, if any                                                                     |

Every comparison of canon points in this chapter ("later", "latest", "at or before")
uses order `O`.

## 7.2 Algorithm

For entity `E`:

1. **Collect** every state-history row for `E`.
2. **Source filter.** Discard rows whose source is not in `P`. A `book-purist` draft is
   blind to fanon and fanfic; an `enhanced` draft sees them. The reserved sources
   `project` and `bridge` are implicitly in `P` (§5.1).
3. **Time filter.** Discard rows whose as-of is later than `X` (§4.2 ordering). Rows
   with an empty as-of (timeless, §4.7) are kept.
4. **Resolve each attribute**, by the profile's resolution mode (§5.4):
   - **`precedence`** (the default):
     1. Among the sources with at least one remaining row for the attribute, take the
        one **earliest in `P`**.
     2. From that source's rows, take the one with the **latest as-of**.
   - **`recency`**:
     1. Take the row with the **latest as-of**, from any remaining source.
     2. If several rows share that as-of, take the one whose source is earliest in `P`.

   In both modes, timeless rows (empty as-of) sort before every canon point. If the
   chosen row's value is `(unset)`, the attribute is absent.
5. **Apply the ledger.** For each divergence in `L` whose *first occurs* is at or
   before `C`, and whose *until* (if any) is after `C`, apply each `Overrides`
   assignment for `E`, replacing the attribute's value. Attach divergences without machine overrides (`Overrides` = `—`) that mention
   `E` to the result as notes, together with their open consequences.
6. **Return** the resolved attributes, each annotated with its provenance: source, tier,
   as-of, and citation, or the divergence id for overridden values.
7. **Return hidden truths separately.** List the rows that passed the source filter
   whose `True from` is at or before `X` but whose `As of` is after it: facts already
   true at the cutoff that the story has not yet revealed. They are marked hidden and
   are **not** part of the resolved state. Agents MUST NOT use them unless the author
   has decided how (§6.12). Rows already decided in the ledger's Hidden canon table
   carry that decision with them.

*Example.* The books set an attribute at `PS:2`, and a fanon source changes it at
`GoF:3`. At a `GoF:10` cutoff, a `precedence` profile that ranks books first resolves to
the books' value, because the fanon row can only fill gaps. A `recency` profile resolves
to the fanon value, because it is later. At a `PoA` cutoff both resolve to the books'
value, because the fanon row has not happened yet. Under every profile, a ledger
override from step 5 wins over both.

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

## 7.4 Crossovers: one cutoff per world

In a universe project there is no single cutoff. `setting.canon_points` maps each world
to its own cutoff, and `setting.active_profiles` maps each world to its own profile:

```yaml
canon_points:    { harry-potter: "HBP:7", star-trek: "TNG:4:1" }
active_profiles: { harry-potter: book-purist, star-trek: canon-only }
```

Here a Harry Potter entity resolves at `HBP:7` against the Harry Potter ruler, and a
Star Trek entity resolves at `TNG:4:1` against the Star Trek ruler. The two cutoffs are
never compared with each other.

Every entity belongs to exactly one world. Resolve it against **its own world's** ruler,
cutoff, and profile. Then apply the bridge (§8): concept mappings, and crossover-only
canon (source tier `crossover`, always active in the universe). The ledger applies last.

## 7.5 Frames: two cutoffs at once

With the frames module (§9.1), a scene declares a **world point** `<canon-point>@<branch>`
and its **travelers**, each with a **personal cutoff** recorded in `timelines.md`.
Resolve in two passes:

1. **World pass:** every native and the setting resolve at the world point.
2. **Traveler pass:** each traveler's *knowledge and memory* resolve at their personal
   cutoff. Their *physical presence* follows the scene.

The composite: **natives are bounded by world time; travelers by their own personal
time.**

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

## 7.6 Materialization

A host or the worldbuilder MAY materialize a snapshot to a file so the drafter can read
it directly, which gives a smaller context and no temporal reasoning per call:

```
derived/as-of-<world-id>-<point>-<profile>[-<chapter>].md
```

- The file MUST begin with a header recording every input (`world`, `world version`,
  `cutoff`, `profile`, `position`, ledger revision).
- It is a **rebuildable cache, never canon** (§3.1, W5).
- It MUST be regenerated, or treated as stale, when any recorded input changes.
