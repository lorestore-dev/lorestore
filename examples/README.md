# Examples

A small conforming workspace built on two well-known franchises: a **magic** world and a
**technology** world. The packages are heavily abridged: just enough rows to exercise
every rule. Facts are recorded in our own words, with citations.

```
examples/
├── worlds/
│   ├── harry-potter/
│   │   ├── base/                # the base: novels and chapters; magic/ catalog; a reveal
│   │   ├── films/               # an adaptation: the first film, with adaptation timecodes
│   │   ├── fanon/               # community conventions, as extension sheets
│   │   ├── theories/            # a fan theory, as numbered claims
│   │   └── fanfic/
│   │       └── example/         # a placeholder fan work
│   └── star-trek/
│       ├── base/                # the base: series, seasons, episodes, a film; technology.md,
│       │                        #   species.md; character versions; an undivided season
│       └── animated/            # official: the animated series, inserted into the ruler
├── universes/
│   └── wizards-and-warp/        # a crossover of both: the author's brief and the bridge
└── projects/
    ├── two-witnesses/           # Harry Potter with fan layers, recency, divergences
    ├── two-witnesses-ii/        # its sequel: book 1 as a project layer
    ├── second-year-tournament/  # Harry Potter with canon rearranged: the Tournament in year two
    ├── no-horcruxes/            # a branch: Voldemort dies in year one, later canon never happens
    ├── blind-harry/             # a retelling: Harry is blind, canon still unfolds around him
    ├── three-brothers/          # a short story adopting a fan theory
    ├── the-long-way-back/       # Star Trek, established, a serial with a buffer and early access, frames
    ├── lantern-road/            # a self-contained book, with a story-dated row
    ├── lantern-road-before/     # its split-frame follow-up: before and after book 1, on the series ruler
    └── hogwarts-at-warp/        # the crossover: two bases and the universe layer, a cutoff per base
```

The cases below state inputs and the result a conforming snapshot (§7) MUST produce. "No
ledger" means the stack alone, with no project's divergences applied. They use these
stacks, from the base up:

| Name     | Layers                                                                      | Resolution |
| -------- | --------------------------------------------------------------------------- | ---------- |
| canon    | `harry-potter@3.0.0`                                                         | precedence |
| fan      | `harry-potter@3.0.0`, `harry-potter/fanon@1.0.0`, `harry-potter/fanfic/example@1.0.0` | precedence |
| fan, recency | the same layers                                                         | recency    |
| fan, fill    | the same layers                                                         | fill       |
| trek     | `star-trek@2.0.0`                                                            | precedence |
| animated | `star-trek@2.0.0`, `star-trek/animated@1.0.0`                                | precedence |

`two-witnesses` uses the fan stack with recency.

## Harry Potter

**1. Time filter.** `harry-potter`, canon stack. At `PS:2`, `residence` = `cupboard
under the stairs, 4 Privet Drive`. At `PS:3`, `residence` = `Dudley's second bedroom`.

**2. Ending a fact.** `harry-potter.broom`, canon stack:

| Cutoff  | Result                | Why                                   |
| ------- | --------------------- | ------------------------------------- |
| `PS:9`  | *(absent)*            | No row yet                            |
| `PS:10` | `Nimbus Two Thousand` |                                       |
| `PoA:10` | *(absent)*           | The `PoA:9` row is `(unset)`          |
| `PoA:11` | `Firebolt`           |                                       |

**3. Resolution modes.** `harry-potter.broom`. The books give `Nimbus Two Thousand` at
`PS:10`, `(unset)` at `PoA:9`, and `Firebolt` at `PoA:11`; the placeholder fan work
says `Cleansweep Seven` at `PS:10`.

| Stack        | At `PS:10`         | At `PoA:10` | At `PoA:11`        | Why                                                         |
| ------------ | ------------------ | ----------- | ------------------ | ----------------------------------------------------------- |
| canon        | `Nimbus Two Thousand` | *(absent)* | `Firebolt`       | The fan work is not in the stack                            |
| fan          | `Cleansweep Seven` | `Cleansweep Seven` | `Cleansweep Seven` | Precedence: the highest layer with a row wins, however old |
| fan, recency | `Cleansweep Seven` | *(absent)*  | `Firebolt`         | Recency: the latest row wins; at the same point, the higher layer |
| fan, fill    | `Nimbus Two Thousand` | *(absent)* | `Firebolt`       | Fill: the books have a row, so they stand; the fan work only fills gaps |

In the fan, fill stack, `glasses` stays `round` at every cutoff from `PS:2`.

**3a. A re-attributed line.** The base's quotation `q1` (PoA ch.17) has speaker
`ron-weasley`. The films package gives it a row, `harry-potter:q1`, with speaker
`hermione-granger` and no `Line`. With `harry-potter` and `harry-potter/films`:

| Resolution | Speaker            | Why                                                     |
| ---------- | ------------------ | ------------------------------------------------------- |
| *(canon stack)* | `ron-weasley` | The films are not in the stack                          |
| precedence | `hermione-granger` | The films are the higher layer                          |
| recency    | `hermione-granger` | Both rows are at `PoA:17`; the higher layer breaks the tie |
| fill       | `ron-weasley`      | The books have a row, so they stand                     |

In every case the `Line` comes from the books, because the film's row leaves it empty.
Before `PoA:17` the quotation has not been said.

**4. Filling gaps.** `daphne-greengrass`. In the canon stack, `house` is absent: only
the fanon package supplies it, through an extension sheet. In every fan stack,
including fill, `house` = `Slytherin`: canon is silent, so fanon fills the gap. In
every stack, `year` is absent at `OotP:30` and `Harry's year` at `OotP:31`.

**5. The ledger.** Project `two-witnesses` (cutoff `GoF:37`, fan stack, recency), entity
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

**8. Episodes as units.** `jean-luc-picard.status`, trek stack:

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

**I1. An inserted work.** In the animated stack, `star-trek/animated` inserts the
animated series' two seasons after `TOS:3` (§4.10):
- `TAS:1:2` is valid, and sorts after `TOS:3:24` and before `TMP`; `TAS:1:17` is
  invalid (season 1 has 16 episodes);
- in the trek stack, `TAS:1:2` is invalid;
- `spock.childhood-pet` = `I-Chaya, a sehlat, put to sleep after a le-matya wounded
  him` from `TAS:1:2`, through an extension sheet. In the trek stack it is absent, and
  a draft that uses it has leaked the package (§5.3).

**11. Gap before a segment.** `borg.known-to-federation` is absent at `TNG:2:15` and
`yes…` at `TNG:2:16`.

## Ruler points

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

## Adaptations

**A1. Adaptation timecodes.** The `harry-potter/films` package adapts PS ch.1–17 as the
work `PS-film` (§4.9). In a stack with it:
- `PS:6:2+00:41:10` is valid; without the films layer it is not;
- at one book path, the timecode orders rows, and an untimed row comes first:
  `PS:6:2` < `PS:6:2+00:00:01` < `PS:6:2+00:41:10` < `PS:6:2+00:42:00`;
- across paths, the book path decides: `PS:6:2+00:50:00` < `PS:6:3+00:10:00`, and
  `PS:6+00:59:00` < `PS:6:1`;
- the film's `oculus-reparo` row resolves on the book ruler. In a stack without the
  films package, using it is a source leak (§5.3).

## Crossover

**12. Per-base cutoffs.** Project `hogwarts-at-warp` stacks both bases and the universe
`wizards-and-warp`. Harry Potter entities resolve at `HBP:7` against the Harry Potter
ruler, and Star Trek entities at `TNG:4:1` against the Star Trek ruler:
`harry-potter.broom` = `Firebolt`, and `jean-luc-picard.status` = `captain of the USS
Enterprise-D`. The two cutoffs are never compared with each other. The universe's
`relies-on` pins match the bases' pins in the stack.

## Divergence by addition

**13. A new scar.** In `two-witnesses`, canon is silent on Cedric having scars; D2 adds
one (§6.2). At `chapter-02`, `cedric-diggory.scars` = `curse scar across his chest`.

## Rearranged canon

Project `second-year-tournament` moves *Goblet of Fire* to second year. Its sync points
advance the cutoff by chapter, and its `setting.order` reorders the books: PS, GoF, CoS,
PoA, and so on (§6.7–6.8). All cases use the canon stack.

**14. Sync points.** The cutoff is `PS:17` before chapter 1 (`setting.cutoff`),
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

**18a. Inversion candidates.** The order swaps *Goblet of Fire* and *Prisoner of
Azkaban*, and three entities have rows in both: `cedric-diggory`,
`harry-potter`, and `harry-potter+sirius-black` (§6.8). The order audit addresses each
under `## Inversion candidates`. Two are I1 to I3. The third, `harry-potter`, has no
reversed attribute, but the first task (`GoF:20`) has Harry summon the Firebolt he gets
at `PoA:11`: the audit raises it as I4, and the author chose to substitute his Nimbus
Two Thousand (D4, `Overrides`: `—`). `two-witnesses` has no candidates.

**18b. A stack change.** A Star Trek project order that swaps `TOS:3` and `TMP` is no
longer a permutation once `star-trek/animated@1.0.0` joins the stack. The host refuses
to run and proposes `TOS:1, TOS:2, TMP, TOS:3, TAS:1, TAS:2, …`: each inserted segment
right after the one it follows on the new ruler. Removing the package again proposes
the original order.

## Branch and retelling

**19. A branch.** Project `no-horcruxes` (`follow: branch`, divergence point
`PS:17`):
- `lord-voldemort.status` = `dead` from `chapter-01` (D1);
- at `chapter-50`, `harry-potter.broom` is still `Nimbus Two Thousand`, and Harry and
  Sirius are still `strangers`: canon after `PS:17` never happens.

Asking for a cutoff of `PoA:11` in this project is an error: the host reports it and
resolves at `PS:17` instead.

**20. A retelling.** Project `blind-harry` (`follow: retelling`) retells year one
with Harry blind (D1). The canon-keeper's divergence audit (`reviews/canon.md`) finds
three conflicts and sets out options without choosing. The author decided:

| Conflict                | Author's choice | Result at its chapter                                                   |
| ----------------------- | --------------- | ----------------------------------------------------------------------- |
| C1 glasses (`PS:2`)     | remove (D2)     | `glasses` absent                                                        |
| C2 Seeker (`PS:9`)      | adapt (D3)      | `role` = `Gryffindor Seeker, flying by sound and feel` from `chapter-09` |
| C3 Nimbus (`PS:10`)     | keep (no entry) | `broom` = `Nimbus Two Thousand` from `chapter-10`, as in canon          |

Canon the divergence doesn't reach still happens: `house` = `Gryffindor` at
`chapter-09`.

**20a. Reach candidates.** For each divergence, the host lists the canon rows on the
attributes it overrides, at or after the cutoff where it first occurs:
- D2 (`glasses`, from `chapter-01`, cutoff `PS:1`) meets `harry-potter.glasses` at `PS:2`;
- D3 (`role`, from `chapter-09`, cutoff `PS:9`) meets `harry-potter.role` at `PS:9`;
- D1 (`sight`) meets no canon row.

Both candidates are addressed in the audit, as C1 and C2. C3 (the Nimbus) is on an
attribute no divergence overrides: the canon-keeper found it by reading ahead, which
the candidate list never replaces. D2 and D3, logged to carry out the author's
decisions, were audited in their turn and raised nothing new.

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

## Errata

**E1. A corrected printing.** The Harry Potter base registers `gof-first-printing` as an
`erratum` source: the first printings of *Goblet of Fire* got the order of the echoes
in ch.34 wrong, and later printings corrected it. Harry's `graveyard-echoes` has the
corrected row from `books` and the error from `gof-first-printing`, both at `GoF:34`:
- `PURIST` at `GoF:37`, in every mode: `his mother's echo emerges first, then his
  father's`. The erratum row never resolves;
- the quotation `q2` resolves the same way: `Speaker` = `lily-potter`;
- no package in the examples holds two rows of one tier, entity, attribute, and point
  with different values. Registering `gof-first-printing` as `primary` instead makes
  the base invalid (§4.4).

**E2. Erratum use.** Prose in which the father's echo emerges first relies on the
erratum, and is flagged as erratum use (§6.9) unless a divergence sets that order. Prose
that follows the corrected text is not flagged.

**E3. A theory resting on an erratum.** `harry-potter/theories` holds T2, an illustrative
theory that Lily is held in stasis, not dead. Its only evidence, `GoF:34`, is the
erratum, so a theory audit marks it `(erratum: gof-first-printing)` (§6.13). T1's
evidence has no erratum.

## Series

**L1. A project layer.** Project `two-witnesses-ii` is book 2. Its stack relists book
1's three package layers, then adds `project:two-witnesses@chapter-02`. At its own
cutoff, `OotP:1`:
- `cedric-diggory.status` = `alive` and `scars` = `curse scar across his chest`: book
  1's D1 and D2 apply, though book 2 logs no divergence of its own;
- without the project layer, `status` = `dead`, as in canon;
- the composed roster includes book 1's original character `mara-quill`, with layer
  `project:two-witnesses`.
- book 1's Hidden canon row keeps Snape's `loyalty` hidden (`keep-hidden`, decided in
  `chapter-01`). At `OotP:1` it is still a hidden truth, and book 2 inherits the
  decision rather than raising it again (§6.4). Had book 1 decided it after
  `chapter-02`, the pin, book 2 would not inherit it.

**L2. The series ruler.** `lantern-road` is self-contained, with no ruler. In the
stack of `lantern-road-before`, which pins it at `chapter-12`, its manuscript is the
work `lantern-road` (§4.12): `lantern-road:9` and `lantern-road:12` are valid points,
and `lantern-road:13` is not. Book 2's `canon-timeline.md` inserts `youth` before it
and `after` after it, so `youth < lantern-road:1 < lantern-road:12 < after`. Those two
points are not on the ruler of a stack without book 2. In book 2's stack they are
valid points, and its project order would list all three segments: `youth`,
`lantern-road`, `after` (§4.2, §6.8).

**L3. A split frame.** `lantern-road-before`'s sync points set chapters 1 to 5 in
`youth` and chapter 6 on in `after` (§6.14). Ines's sheet in book 1 gives her grey eyes
and the role of apprentice lamplighter from the start, and makes her a master from
`chapter-09`.
- At `chapter-01`, all of that is ahead. The Seam conflicts table carries back
  `lantern-road:ines-varga.*` and decides `not-yet` for `lantern-road:*.*@*`, so Ines
  is `eyes` = `grey`, `role` = `apprentice lamplighter`, with no seam conflict.
- At `chapter-06`, nothing is ahead: `role` = `master lamplighter`, and nothing is
  raised.
- Book 1's `chapter-09` row is dated `lantern-road:9`, after `youth`, but it is an
  anchored item, not a row the time filter drops (§7.2, step 3): had the author also
  carried back `lantern-road:ines-varga.role@chapter-09`, an exact item that beats the
  `not-yet` pattern, `role` would be `master lamplighter` at `chapter-01`.
- Promoting `lantern-road` to a base (§2.9) re-cites its three rows from `project` to
  `lantern-road`, and dates the `master lamplighter` row `lantern-road:9`. Its ruler is
  the one segment `lantern-road`, chapters 1 to 12, the same as the series ruler without
  book 2's inserts, and the promoted project's sync points put `chapter-<NN>` at
  `lantern-road:<NN>`.
- `lantern-road-before`'s seam audit (`reviews/canon.md`) notes the earlier start under
  `- pin:`, and raises S1 to S3, each covered by a Seam conflicts row; every row covers
  one of them.
- The seam audit's first question flags `lantern-road-before` as starting before book
  1's end, and `two-witnesses-ii` as not.

**L4. Undecided seams.** Read `two-witnesses-ii`'s stack at `GoF:20`, before book 1's
`GoF:37`, and everything book 1 brings is ahead, with no decision:
- `mara-quill` has no attributes, and the seam conflicts are
  `two-witnesses:mara-quill.house` and `two-witnesses:mara-quill.year`;
- `cedric-diggory` is canon at `GoF:20` (`status` = `alive`, `role` = `Hogwarts
  Triwizard champion`, with no scar), and the seam conflicts are `two-witnesses:D1`
  and `two-witnesses:D2`;
- at book 2's own cutoff, `OotP:1`, nothing is ahead (L1).

**L5. Value seams.** `two-witnesses-ii` has book 1's stack and mode, so the seam audit
finds no value seam for Harry, Cedric, Hermione, or Snape. Switched to `precedence`, it
finds one: `harry-potter.broom`. Book 1 (`recency`) gave the Firebolt from the books,
and `precedence` gives the fan work's Cleansweep Seven.

**L6. Inherited settings.** A stack of `harry-potter@3.0.0` and
`project:second-year-tournament@chapter-03` sets no order, and so uses book 1's: `GoF:1`
sorts before `CoS:1`. A sequel to the `no-horcruxes` branch MUST be a branch, with a
divergence point no later than `PS:17`.

## Theories

**Q1. Adopting a theory.** Project `three-brothers` (cutoff `DH:36`) stacks
`harry-potter/theories`, whose T1 has four numbered claims. Its D1 has `Basis:
harry-potter/theories:T1 (claims 1, 3, 4)`. The Theory conflicts table records two
conflicts at `DH:35`: claim 2 discarded, and claim 4 adapted with a note. Claim 2
appears in no `Basis`; claim 4 does. The theory's rows never resolve into state:
`albus-dumbledore` has no attributes from it.

## Frames and serials

Project `the-long-way-back` is a serial set in Star Trek, using the frames module.

**22a. World points.** A scene's world point is its cutoff (§7.5). With the project's
cutoff `TNG:3:15`, a scene in `chapter-03` with world point `TNG:4:1@main` and no
travelers draws a warning (a flash-forward, or a mistake). The same scene with Mira as
a traveler, or a scene at `TNG:3:14@main`, does not.

**23. A mechanism and its model.** The Star Trek world declares one mechanism,
`temporal-rift`, with model `mutable` (§9.1, §10.24). Both of Mira's legs name it. Under
`mutable`, the Enterprise-C's absence replaces history, so `alt-war` splits from `main`
at `TNG:1`. When the ship goes back, `main` is restored and `alt-war` is `overwritten`.
Mira's memories of `alt-war` belong to her own frame, so they are not a frame violation,
and no paradox is recorded.

**24. The buffer and early access.** Chapters 1 and 2 are `released`, chapter 3 is in
`early-access`, and chapter 4 is `drafted`, so the buffer is two chapters deep. The
author may release chapter 3. Releasing chapter 4 first MUST be refused (§13.3), and so
MUST sending it to early access while it is drafted, here, since the example treats
`line-edited` as required (§13.9). Chapters 3 and 4 may be revised; chapters 1 and 2 are
locked. Chapter 3's change after it went to early access is logged in `revisions.md`
with audience `early-access` and a reader note, and `reader-a`'s feedback on it is
filed under `references/feedback/chapter-03/`.

**25. A registered column.** `timelines.md`'s `## Legs` table adds a `Notes` column
after the required ones. The story-side `index.md` registers it under `## Columns`, so
no warning is raised (§10.0, §10.3).

**26. A story-dated row.** Mira's sheet gives her starting role without a
`From chapter`, and a second `role` row with `From chapter: chapter-03`, when she
stays behind (§4.11). At `chapter-02` her role is `operations officer, USS
Enterprise-C`; at `chapter-03`, and after the last chapter, it is `displaced officer
aboard the USS Enterprise-D`. The row cites `project` and leaves `As of` empty.

**27. Renumbering.** In `the-long-way-back`, chapter 3 is in early access, so
`renumber` may move only chapter 4 onwards: a new chapter inserted before chapter 3 MUST
be refused (§13.10). In `two-witnesses`, which `two-witnesses-ii` pins at `chapter-02`,
chapters 1 and 2 keep their ids. `three-brothers` has no readers and no pins, so any of
its chapters may move.

## Validation cases

A conforming host MUST report each of these if introduced:

- citing the `films` source from the Harry Potter base (a tier its kind does
  not allow, §2.3);
- removing `harry-potter/fanon@1.0.0` from `two-witnesses-ii` (a package layer not
  relisted, §2.2);
- moving `harry-potter/fanon@1.0.0` below `harry-potter@3.0.0` in any stack (a layer
  below what it relies on, §2.2);
- a `PS:6:2+00:41:10` as-of in a stack without `harry-potter/films` (§4.9);
- changing the animated package's `TAS:1` row to insert after `TOS:4` (an unknown
  segment, §4.10);
- adding claim 2 to `three-brothers`' `Basis` while its decision is `discard` (§6.13);
- any invalid point from the table above, used as a row's as-of (§4.2);
- a `two-witnesses` roster row with slug `cedric-diggory` (a union collision, §2.7);
- changing `two-witnesses`' pin to `harry-potter@2.2.0` (a version mismatch, §2.8);
- deleting the consequence rows for D1 (a divergence with no consequences, §6.4);
- giving `hogwarts-at-warp` a single `cutoff` (rejected by the schema, §10.1);
- removing a book from `second-year-tournament`'s order (not a permutation, §6.8);
- deleting D2 or D3 from `second-year-tournament` (an uncovered order inversion, §6.8);
- setting D2's `Until` to `chapter-01` (not after `First occurs`, §10.8);
- removing `divergence_point` from `no-horcruxes` (a branch needs one; rejected by the schema, §6.6);
- adding a `no-horcruxes` sync point with cutoff `CoS:1` (past a branch's divergence point, §6.6);
- giving Snape's `loyalty` row a `True from` of `DH:34`, later than its `As of` (`DH:33`) (§4.4);
- deleting D2 from `no-horcruxes` while its Hidden canon row still says `reveal-early` (§10.8);
- releasing `the-long-way-back`'s chapter 4 while chapter 3 is unreleased (§13.3);
- deleting the reader note from its `revisions.md` row (§10.22);
- changing the `temporal-rift` model to anything outside §10.24's list, or naming an unknown mechanism in a leg (§10.16);
- a world point on a branch that `branches.md` does not register (§10.16);
- removing `layers` from `two-witnesses` while it is `established`, or giving `lantern-road` (`original`) any layer (rejected by the schema, §6.1);
- giving Mira's `chapter-03` role row an `As of`, or another source than `project` (§4.11);
- a `lantern-road:13` point in `lantern-road-before`, past its pin (§4.12);
- a `lantern-road-before` Seam conflicts row with decision `accept` for a project item, or `other` with no note (§10.8);
- a sequel to `no-horcruxes` that is a retelling, or a branch diverging after `PS:17` (§6.14);
- adding `star-trek/animated@1.0.0` to a Star Trek project with a `setting.order` that lacks `TAS:1` and `TAS:2` (§6.8);
- `lantern-road` with a `setting.cutoff` (§4.7, rejected by the schema);
- registering `gof-first-printing` as `primary` (two tied rows in one package, §4.4), or an `erratum` source in `harry-potter/fanon` (§2.3).

A conforming host SHOULD warn if `the-long-way-back`'s `## Columns` row for `Notes` is
deleted (an unregistered column, §10.0).
