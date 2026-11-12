# Examples

A small conforming workspace built on two well-known franchises: a **magic** world and a
**technology** world. The world packages are heavily abridged: just enough rows to
exercise every rule. Facts are recorded in our own words, with citations.

```
examples/
├── worlds/
│   ├── harry-potter/            # magic: novels and chapters; magic/ catalog; a reveal
│   └── star-trek/               # technology: series, seasons, episodes, a film; technology.md,
│                                #   species.md; character versions; an undivided season
├── universes/
│   └── wizards-and-warp/        # a crossover of both: the author's brief and the bridge
└── projects/
    ├── two-witnesses/           # Harry Potter, established, enhanced profile, divergences
    ├── second-year-tournament/  # Harry Potter with canon rearranged: the Tournament in year two
    ├── no-horcruxes/            # a branch: Voldemort dies in year one, later canon never happens
    ├── blind-harry/             # a retelling: Harry is blind, canon still unfolds around him
    ├── the-long-way-back/       # Star Trek, established, frames module (time travel)
    └── hogwarts-at-warp/        # the crossover: one cutoff and one profile per world
```

The cases below state inputs and the result a conforming snapshot (§7) MUST produce. "No
ledger" means the world alone, with no project's divergences applied.

## Harry Potter

**1. Time filter.** `harry-potter`, `book-purist`. At `PS:2`, `residence` = `cupboard
under the stairs, 4 Privet Drive`. At `PS:3`, `residence` = `Dudley's second bedroom`.

**2. Ending a fact.** `harry-potter.broom`, `book-purist`:

| Cutoff  | Result                | Why                                   |
| ------- | --------------------- | ------------------------------------- |
| `PS:9`  | *(absent)*            | No row yet                            |
| `PS:10` | `Nimbus Two Thousand` |                                       |
| `PoA:10` | *(absent)*           | The `PoA:9` row is `(unset)`          |
| `PoA:11` | `Firebolt`           |                                       |

**3. Resolution modes.** `harry-potter.glasses`. The books say `round` at `PS:2`; the
placeholder fan work says `contact lenses` at `PoA:1`.

| Profile       | Mode       | At `PS:5` | At `GoF:37`      | Why                                                    |
| ------------- | ---------- | --------- | ---------------- | ------------------------------------------------------ |
| `book-purist` | precedence | `round`   | `round`          | The fan work is not active                             |
| `enriched`    | precedence | `round`   | `round`          | The fan work is active but can only fill gaps          |
| `enhanced`    | recency    | `round`   | `contact lenses` | The fan work's row is later, so it wins                |

**4. Filling gaps.** `daphne-greengrass`. Under `book-purist`, `house` is absent: only
fanon supplies it. Under `enriched` or `enhanced`, `house` = `Slytherin`. Under every
profile, `year` is absent at `OotP:30` and `Harry's year` at `OotP:31`.

**5. The ledger.** Project `two-witnesses` (cutoff `GoF:37`, `enhanced`), entity
`cedric-diggory`:
- no ledger: `status` = `dead` (`GoF:32`);
- position `chapter-01`, ledger applied: `status` = `alive`, provenance D1;
- no ledger, cutoff `GoF:20`: `status` = `alive`, `role` = `Hogwarts Triwizard
  champion`.

**6. Relationships.** `harry-potter+hermione-granger`: `bond` = `acquaintances` at
`PS:8`, `friends` at `PS:10`.

**7. Knowledge and reveal aliases.** `harry-potter`'s state for `moody-identity` is
`unaware` at `GoF:34` and `knows` at `GoF:35`. Before `GoF:35`, facts about the
Moody who teaches in GoF are filed under `moody-impostor`, never under
`barty-crouch-jr`.

## Star Trek

**8. Episodes as units.** `jean-luc-picard.status`, `canon-only`:

| Cutoff     | Result                            | Why                                          |
| ---------- | --------------------------------- | -------------------------------------------- |
| `TNG:3:25` | `captain of the USS Enterprise-D` | Whole-series row dated `TNG`                 |
| `TNG:3:26` | `assimilated as Locutus of Borg`  |                                              |
| `TNG:4`    | `assimilated as Locutus of Borg`  | `TNG:4` sorts before `TNG:4:1`               |
| `TNG:4:1`  | `captain of the USS Enterprise-D` |                                              |

**9. An undivided segment.** The ruler marks `TNG:1` as undivided (`—`), so nothing
inside season 1 can be dated more finely than `TNG:1`. Tasha Yar dies late in season 1,
which the whole-node rule forbids dating `TNG:1`, so her death is dated `TNG:2`: the
first point from whose opening it holds. `tasha-yar.status` is `chief of security, USS
Enterprise-D` at `TNG:1` and `dead` at `TNG:2`.

**10. Versions.** `spock-mirror` is a separate entity from `spock`, linked by `Version
of`. At `TOS:2:3` it has no attributes; at `TOS:2:4`, `appearance` = `bearded`.
Resolving `spock` never returns the mirror version's rows.

**11. Gap before a segment.** `borg.known-to-federation` is absent at `TNG:2:15` and
`yes…` at `TNG:2:16`.

## Canon points

These cases test the point notation against the Star Trek ruler (§4.2). They make no
claims about what happens in any episode.

**Validity.**

| Point                  | Valid? | Why                                                        |
| ---------------------- | ------ | ---------------------------------------------------------- |
| `TOS:3:2:14`           | yes    | Scenes are uncounted, so any positive scene index is valid |
| `TOS:3:2:14+00:12:31`  | yes    | The path reaches the timed level (episode)                 |
| `TMP+01:10:05`         | yes    | The film itself is the timed level                         |
| `TOS:3:25`             | no     | Season 3 has 24 episodes                                   |
| `TNG:1:5`              | no     | `TNG:1` is undivided                                       |
| `TOS:3+00:01:00`       | no     | A season is not timed                                      |
| `TOS:3:2:14:1`         | no     | TOS has only three levels                                  |
| `TOS:3:2+00:61:00`     | no     | Minutes must be below 60                                   |
| `DS9:1`                | no     | `DS9` is not on this ruler                                 |

**Ordering.** Each point sorts before the next:

```
TOS < TOS:1 < TOS:3:2 < TOS:3:2:14 < TOS:3:2:14+00:12:31 < TOS:3:2:15
    < TMP < TMP+01:10:05 < TNG < TNG:1 < TNG:2 < TNG:2:16
```

**Timecodes over scenes.** `TOS:3:2:14+00:20:00` sorts after `TOS:3:2:15+00:10:00`,
because both have timecodes and timecodes win (§4.2, rule 3). A host SHOULD warn that the
timecodes contradict the scene order.

**Incomparable.** `TOS:3:2+00:12:31` and `TOS:3:2:14` cannot be ordered: one has only a
timecode and the other only a scene. A host MUST report the pair rather than guess.

## Crossover

**12. Per-world cutoffs.** In project `hogwarts-at-warp`, Harry Potter entities resolve
at `HBP:7` under `book-purist` and Star Trek entities at `TNG:4:1` under `canon-only`:
`harry-potter.broom` = `Firebolt`, and `jean-luc-picard.status` = `captain of the USS
Enterprise-D`. The two cutoffs are never compared with each other.

## Divergence by addition

**13. A new scar.** In `two-witnesses`, canon is silent on Cedric having scars; D2 adds
one (§6.2). At `chapter-02`, `cedric-diggory.scars` = `curse scar across his chest`.

## Rearranged canon

Project `second-year-tournament` moves *Goblet of Fire* to second year. Its canon track
advances the cutoff by chapter and reorders the books: PS, GoF, CoS, PoA, and so on
(§6.7–6.8). All cases use `book-purist`.

**14. The canon track.** The cutoff is `PS:17` before chapter 1 (`setting.canon_point`),
`GoF:1` at `chapter-05`, `GoF:20` at `chapter-10`, and `GoF:37` at `chapter-15`.

**15. The project order.** In this project, `GoF:20` sorts **before** `PoA:17`. On the
ruler it sorts after.

**16. Harry and Sirius.** `harry-potter+sirius-black.bond`:

| Position     | Without the ledger | With the ledger              | Why                                                        |
| ------------ | ------------------ | ---------------------------- | ---------------------------------------------------------- |
| `chapter-05` | `strangers`        | `strangers`                  | The `GoF:2` row is after the cutoff `GoF:1`                |
| `chapter-15` | `correspondents`   | `strangers`                  | An order inversion: `GoF:2` presumes `PoA:17`. The author chose to substitute (D2) |
| `chapter-40` | —                  | `met in the Shrieking Shack` | D2 ends (`Until`), and `PoA:17` is now the latest row      |

At `chapter-15`, `sirius-black.status` is absent: his escape (`PoA:3`) has not happened
yet in this story.

**17. Cedric.** At `chapter-10`, `status` = `alive` and `house` = `Hufflepuff`. The
house comes from the `GoF:16` confirmation row, which the merger keeps (§12.4); the
`PoA:9` row now comes later. At `chapter-14` he is `dead` (`GoF:32`). At `chapter-40`
(cutoff `PoA:17`), without the ledger the `PoA:9` row would make him `alive` again. D3
keeps him `dead` and unsets his `role`.

**18. Order inversions.** A conforming host reports exactly three inversions for this
project: `harry-potter+sirius-black.bond`, `cedric-diggory.status`, and
`cedric-diggory.role`. The canon-keeper's order audit (`reviews/canon.md`) sets out the
options for each without choosing. The author chose: for I1, substitute (Harry writes
to Dumbledore, D2); for I2 and I3, remove (Cedric's PoA appearances don't happen, D3).
The fallout of each choice is listed as open consequences for the author to work
through. Each inversion ends up covered by a divergence's `Overrides`. `cedric-diggory.house`
is not an inversion, because both rows have the same value. `two-witnesses`, which keeps
canon order, has none.

## Branch and retelling

**19. A branch.** Project `no-horcruxes` (`canon_mode: branch`, divergence point
`PS:17`):
- `lord-voldemort.status` = `dead` from `chapter-01` (D1);
- at `chapter-50`, `harry-potter.broom` is still `Nimbus Two Thousand`, and Harry and
  Sirius are still `strangers`: canon after `PS:17` never happens.

Asking for a cutoff of `PoA:11` in this project is an error: the host reports it and
resolves at `PS:17` instead.

**20. A retelling.** Project `blind-harry` (`canon_mode: retelling`) retells year one
with Harry blind (D1). The canon-keeper's divergence audit (`reviews/canon.md`) finds
three conflicts and sets out options without choosing. The author decided:

| Conflict                | Author's choice | Result at its chapter                                                   |
| ----------------------- | --------------- | ----------------------------------------------------------------------- |
| C1 glasses (`PS:2`)     | remove (D2)     | `glasses` absent                                                        |
| C2 Seeker (`PS:9`)      | adapt (D3)      | `role` = `Gryffindor Seeker, flying by sound and feel` from `chapter-09` |
| C3 Nimbus (`PS:10`)     | keep (no entry) | `broom` = `Nimbus Two Thousand` from `chapter-10`, as in canon          |

Canon the divergence doesn't reach still happens: `house` = `Gryffindor` at
`chapter-09`.

## Hidden canon

**21. True from.** Snape's `loyalty` row is dated `As of: DH:33` (its reveal) and `True
from: PS` (true from the start of canon):
- At `PS:17` it is not resolved, but the snapshot lists it as a **hidden truth**. The
  same holds at `PS:1`.
- At `DH:33` it resolves normally, and is no longer hidden.

**22. The author decides.** In the `no-horcruxes` branch, canon never reaches `DH:33`.
When the story touched Snape in chapter 18, the hidden truth was raised with the author,
who chose **reveal early**. The ledger's Hidden canon table records the decision, and
D2 reveals it:
- `severus-snape.loyalty` is absent at `chapter-05`;
- it is `loves Lily Potter, and protects Harry for her sake` from `chapter-20`.

## Validation cases

A conforming host MUST report each of these if introduced:

- adding `films` to any Harry Potter profile (an excluded source, §5.3);
- any invalid point from the table above, used as a row's as-of (§4.2);
- a `two-witnesses` roster row with slug `cedric-diggory` (a union collision, §2.7);
- changing `two-witnesses`' `world.version` to `2.2.0` (a version mismatch, §2.8);
- deleting the consequence rows for D1 (a divergence with no consequences, §6.4);
- giving `hogwarts-at-warp` a single `canon_point` (rejected by the schema, §10.1);
- removing a book from `second-year-tournament`'s order (not a permutation, §6.8);
- deleting D2 or D3 from `second-year-tournament` (an uncovered order inversion, §6.8);
- setting D2's `Until` to `chapter-01` (not after `First occurs`, §10.8);
- removing `divergence_point` from `no-horcruxes` (a branch needs one; rejected by the schema, §6.6);
- adding a `no-horcruxes` track row with cutoff `CoS:1` (past a branch's divergence point, §6.6);
- giving Snape's `loyalty` row a `True from` of `DH:34`, later than its `As of` (`DH:33`) (§4.4);
- deleting D2 from `no-horcruxes` while its Hidden canon row still says `reveal-early` (§10.8).
