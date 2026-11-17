# Examples

A small conforming workspace built on two well-known franchises: a **magic** world and a
**technology** world. The packages are heavily abridged: just enough rows to exercise
every rule. Facts are recorded in our own words, with citations.

```
examples/
├── worlds/
│   ├── harry-potter/
│   │   ├── base/                # the base: novels and chapters; magic/ catalog; a reveal;
│   │   │                        #   an iso calendar, ruler dates, and world history;
│   │   │                        #   a mystery, parentage, and a title
│   │   ├── films/               # an adaptation: the first film, with adaptation timecodes
│   │   ├── fanon/               # community conventions, as extension sheets; CC-BY-4.0
│   │   ├── theories/            # a fan theory, as numbered claims
│   │   └── fanfic/
│   │       └── example/         # a placeholder fan work, with its own work inserted after the books,
│   │                            #   under its author's own terms (LICENSE.md)
│   └── star-trek/
│       ├── base/                # the base: series, seasons, episodes, a film; technology.md,
│       │                        #   species.md; character versions; an undivided season; dates
│       └── animated/            # official: the animated series, inserted into the ruler
├── runs/                      # copies of projects with a recorded run of tools/loop.py
├── universes/
│   └── wizards-and-warp/        # a crossover of both: the author's brief and the bridge
└── projects/
    ├── two-witnesses/           # Harry Potter with fan layers, recency, divergences, two modules,
    │                            #   and an image prompt
    ├── two-witnesses-ii/        # its sequel: book 1 as a project layer
    ├── second-year-tournament/  # Harry Potter with canon rearranged: the Tournament in year two
    ├── no-horcruxes/            # a branch: Voldemort dies in year one, later canon never happens
    ├── blind-harry/             # a retelling: Harry is blind, canon still unfolds around him
    ├── three-brothers/          # a short story adopting a fan theory
    ├── the-long-way-back/       # Star Trek, established, a serial with a buffer and early access, frames;
    │                            #   two authors, content notes, a scheduled release,
    │                            #   and its export for readers
    ├── lantern-road/            # a self-contained book, with a story-dated row and its own calendar;
    │                            #   routes and journey times, a mystery, a map prompt, and
    │                            #   viewpoints, told from the end
    ├── lantern-road-before/     # its split-frame follow-up: before and after book 1, on the series ruler
    └── hogwarts-at-warp/        # the crossover: two bases and the universe layer, a cutoff per base
```

The cases below state inputs and the result a conforming snapshot ([§7](../spec/07-snapshot.md#7-the-snapshot-query)) MUST produce. "No
ledger" means the stack alone, with no project's divergences applied. They use these
stacks, from the base up:

| Name     | Layers                                                                      | Resolution |
| -------- | --------------------------------------------------------------------------- | ---------- |
| canon    | `harry-potter@3.2.2`                                                         | precedence |
| fan      | `harry-potter@3.2.2`, `harry-potter/fanon@1.0.5`, `harry-potter/fanfic/example@1.2.4` | precedence |
| fan, recency | the same layers                                                         | recency    |
| fan, fill    | the same layers                                                         | fill       |
| trek     | `star-trek@2.1.2`                                                            | precedence |
| animated | `star-trek@2.1.2`, `star-trek/animated@1.0.3`                                | precedence |

`two-witnesses` uses the fan stack with recency.

## Harry Potter

<a id="case-1"></a>**1. Time filter.** `harry-potter`, canon stack. At `PS:2`, `residence` = `cupboard
under the stairs, 4 Privet Drive`. At `PS:3`, `residence` = `Dudley's second bedroom`.

<a id="case-2"></a>**2. Ending a fact.** `harry-potter.broom`, canon stack:

| Cutoff  | Result                | Why                                   |
| ------- | --------------------- | ------------------------------------- |
| `PS:9`  | *(absent)*            | No row yet                            |
| `PS:10` | `Nimbus Two Thousand` |                                       |
| `PoA:10` | *(absent)*           | The `PoA:9` row is `(unset)`          |
| `PoA:11` | `Firebolt`           |                                       |

<a id="case-3"></a>**3. Resolution modes.** `harry-potter.broom`. The books give `Nimbus Two Thousand` at
`PS:10`, `(unset)` at `PoA:9`, and `Firebolt` at `PoA:11`; the placeholder fan work
says `Cleansweep Seven` at `PS:10`.

| Stack        | At `PS:10`         | At `PoA:10` | At `PoA:11`        | Why                                                         |
| ------------ | ------------------ | ----------- | ------------------ | ----------------------------------------------------------- |
| canon        | `Nimbus Two Thousand` | *(absent)* | `Firebolt`       | The fan work is not in the stack                            |
| fan          | `Cleansweep Seven` | `Cleansweep Seven` | `Cleansweep Seven` | Precedence: the highest layer with a row wins, however old |
| fan, recency | `Cleansweep Seven` | *(absent)*  | `Firebolt`         | Recency: the latest row wins; at the same point, the higher layer |
| fan, fill    | `Nimbus Two Thousand` | *(absent)* | `Firebolt`       | Fill: the books have a row, so they stand; the fan work only fills gaps |

In the fan, fill stack, `glasses` stays `round` at every cutoff from `PS:2`.

<a id="case-3a"></a>**3a. A re-attributed line.** The base's quotation `q1` (PoA ch.17) has speaker
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

<a id="case-4"></a>**4. Filling gaps.** `daphne-greengrass`. In the canon stack, `house` is absent: only
the fanon package supplies it, through an extension sheet. In every fan stack,
including fill, `house` = `Slytherin`: canon is silent, so fanon fills the gap. In
every stack, `year` is absent at `OotP:30` and `Harry's year` at `OotP:31`.

<a id="case-4a"></a>**4a. A fan work after the books.** The placeholder fan work is set after *Deathly
Hallows*, so it inserts its own work, `FIC`, after `DH` ([§4.10](../spec/04-temporal.md#410-inserted-works)), and dates its two
`harry-potter.role` rows `FIC:3` (`Auror`) and `FIC:20` (`head of the Auror Office`).
In the fan stack:
- `FIC:20` is valid, and sorts after every point of `DH`; `FIC:25` is invalid (24
  chapters), and in the canon stack every `FIC` point is invalid;
- `role` = `Gryffindor Seeker` at `DH:36`, `Auror` at `FIC:10`, and `head of the Auror
  Office` at `FIC:20`;
- dated on `DH:36` instead, the two rows would tie ([§4.4](../spec/04-temporal.md#44-state-histories)), and the package would be
  invalid.

<a id="case-5"></a>**5. The ledger.** Project `two-witnesses` (cutoff `GoF:37`, fan stack, recency), entity
`cedric-diggory`:
- no ledger: `status` = `dead` (`GoF:32`);
- position `chapter-01`, ledger applied: `status` = `alive`, provenance D1;
- no ledger, cutoff `GoF:20`: `status` = `alive`, `role` = `Hogwarts Triwizard
  champion`.

<a id="case-6"></a>**6. Relationships.** `harry-potter+hermione-granger`: `bond` = `acquaintances` at
`PS:8`, `friends` at `PS:10`.

<a id="case-7"></a>**7. Knowledge and reveal aliases.** `harry-potter`'s state for `moody-identity` is
`unaware` at `GoF:34` and `knows` at `GoF:35`. Before `GoF:35`, facts about the
Moody who teaches in GoF are filed under `moody-impostor`, never under
`barty-crouch-jr`.

## Star Trek

<a id="case-8"></a>**8. Episodes as units.** `jean-luc-picard.status`, trek stack:

| Cutoff     | Result                            | Why                                          |
| ---------- | --------------------------------- | -------------------------------------------- |
| `TNG:3:25` | `captain of the USS Enterprise-D` | Whole-series row dated `TNG`                 |
| `TNG:3:26` | `assimilated as Locutus of Borg`  |                                              |
| `TNG:4`    | `assimilated as Locutus of Borg`  | `TNG:4` sorts before `TNG:4:1`               |
| `TNG:4:1`  | `captain of the USS Enterprise-D` |                                              |

<a id="case-9"></a>**9. An undivided segment.** The ruler marks `TNG:1` as undivided (`—`), so nothing
inside season 1 can be dated more finely than `TNG:1`. Tasha Yar dies late in season 1,
which the whole-node rule forbids dating `TNG:1`, so her death is dated `TNG:2`: the
first point from whose opening it holds. `tasha-yar.status` is `chief of security, USS
Enterprise-D` at `TNG:1` and `dead` at `TNG:2`.

<a id="case-10"></a>**10. Versions.** `spock-mirror` is a separate entity from `spock`, linked by `Version
of`. At `TOS:2:3` it has no attributes; at `TOS:2:4`, `appearance` = `bearded`.
Resolving `spock` never returns the mirror version's rows.

<a id="case-i1"></a>**I1. An inserted work.** In the animated stack, `star-trek/animated` inserts the
animated series' two seasons after `TOS:3` ([§4.10](../spec/04-temporal.md#410-inserted-works)):
- `TAS:1:2` is valid, and sorts after `TOS:3:24` and before `TMP`; `TAS:1:17` is
  invalid (season 1 has 16 episodes);
- in the trek stack, `TAS:1:2` is invalid;
- `spock.childhood-pet` = `I-Chaya, a sehlat, put to sleep after a le-matya wounded
  him` from `TAS:1:2`, through an extension sheet. In the trek stack it is absent, and
  a draft that uses it has leaked the package ([§5.3](../spec/05-sources.md#53-pure-bases-and-source-leaks)).

<a id="case-11"></a>**11. Gap before a segment.** `borg.known-to-federation` is absent at `TNG:2:15` and
`yes…` at `TNG:2:16`.

## Ruler points

These cases test the point notation against the Star Trek ruler ([§4.2](../spec/04-temporal.md#42-ruler-points)). They make no
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
because both have timecodes and timecodes win ([§4.2](../spec/04-temporal.md#42-ruler-points), rule 3). A host SHOULD warn that the
timecodes contradict the scene order.

**Incomparable.** `TOS:3:2+00:12:31` and `TOS:3:2:14` cannot be ordered: one has only a
timecode and the other only a scene. A host MUST report the pair rather than guess.

## Adaptations

<a id="case-a1"></a>**A1. Adaptation timecodes.** The `harry-potter/films` package adapts PS ch.1–17 as the
work `PS-film` ([§4.9](../spec/04-temporal.md#49-adaptations-base-points-with-the-adaptations-timecode)). In a stack with it:
- `PS:6:2+00:41:10` is valid; without the films layer it is not;
- at one book path, the timecode orders rows, and an untimed row comes first:
  `PS:6:2` < `PS:6:2+00:00:01` < `PS:6:2+00:41:10` < `PS:6:2+00:42:00`;
- across paths, the book path decides: `PS:6:2+00:50:00` < `PS:6:3+00:10:00`, and
  `PS:6+00:59:00` < `PS:6:1`;
- the film's `oculus-reparo` row resolves on the book ruler. In a stack without the
  films package, using it is a source leak ([§5.3](../spec/05-sources.md#53-pure-bases-and-source-leaks)).

## Crossover

<a id="case-12"></a>**12. Per-base cutoffs.** Project `hogwarts-at-warp` stacks both bases and the universe
`wizards-and-warp`. Harry Potter entities resolve at `HBP:7` against the Harry Potter
ruler, and Star Trek entities at `TNG:4:1` against the Star Trek ruler:
`harry-potter.broom` = `Firebolt`, and `jean-luc-picard.status` = `captain of the USS
Enterprise-D`. The two cutoffs are never compared with each other. The universe's
`relies-on` pins match the bases' pins in the stack.

## Divergence by addition

<a id="case-13"></a>**13. A new scar.** In `two-witnesses`, canon is silent on Cedric having scars; D2 adds
one ([§6.2](../spec/06-divergence.md#62-what-counts-as-a-divergence)). At `chapter-02`, `cedric-diggory.scars` = `curse scar across his chest`.

## Rearranged canon

Project `second-year-tournament` moves *Goblet of Fire* to second year. Its sync points
advance the cutoff by chapter, and its `setting.order` reorders the books: PS, GoF, CoS,
PoA, and so on ([§6.7](../spec/06-divergence.md#67-following-canon-sync-points)–6.8). All cases use the canon stack.

<a id="case-14"></a>**14. Sync points.** The cutoff is `PS:17` before chapter 1 (`setting.cutoff`),
`GoF:1` at `chapter-05`, `GoF:20` at `chapter-10`, and `GoF:37` at `chapter-15`.

<a id="case-15"></a>**15. The project order.** In this project, `GoF:20` sorts **before** `PoA:17`. On the
ruler it sorts after.

<a id="case-16"></a>**16. Harry and Sirius.** `harry-potter+sirius-black.bond`:

| Position     | Without the ledger | With the ledger              | Why                                                        |
| ------------ | ------------------ | ---------------------------- | ---------------------------------------------------------- |
| `chapter-05` | `strangers`        | `strangers`                  | The `GoF:2` row is after the cutoff `GoF:1`                |
| `chapter-15` | `correspondents`   | `strangers`                  | An order inversion: `GoF:2` presumes `PoA:17`. The author chose to substitute (D2) |
| `chapter-40` | —                  | `met in the Shrieking Shack` | D2 ends (`Until`), and `PoA:17` is now the latest row      |

At `chapter-15`, `sirius-black.status` is absent: his escape (`PoA:3`) has not happened
yet in this story.

<a id="case-17"></a>**17. Cedric.** At `chapter-10`, `status` = `alive` and `house` = `Hufflepuff`. The
house comes from the `GoF:16` confirmation row, which the merger keeps ([§12.4](../spec/12-agents.md#124-merger-facts-to-ordered-history)); the
`PoA:9` row now comes later. At `chapter-14` he is `dead` (`GoF:32`). At `chapter-40`
(cutoff `PoA:17`), without the ledger the `PoA:9` row would make him `alive` again. D3
keeps him `dead` and unsets his `role`.

<a id="case-18"></a>**18. Order inversions.** A conforming host reports exactly three inversions for this
project: `harry-potter+sirius-black.bond`, `cedric-diggory.status`, and
`cedric-diggory.role`. The canon-keeper's order audit (`reviews/canon.md`) sets out the
options for each without choosing. The author chose: for I1, substitute (Harry writes
to Dumbledore, D2); for I2 and I3, remove (Cedric's PoA appearances don't happen, D3).
The fallout of each choice is listed as open consequences for the author to work
through. Each inversion ends up covered by a divergence's `Overrides`. `cedric-diggory.house`
is not an inversion, because both rows have the same value. `two-witnesses`, which keeps
canon order, has none.

<a id="case-18a"></a>**18a. Inversion candidates.** The order moves *Goblet of Fire* before *Chamber of
Secrets* and *Prisoner of Azkaban*. Four candidates have rows on both sides of a swap
([§6.8](../spec/06-divergence.md#68-rearranging-canon)): `cedric-diggory`, `harry-potter`, and `harry-potter+sirius-black` across `PoA`
and `GoF`, and `harry-potter` across `CoS` and `GoF`. The order audit addresses each
under `## Inversion candidates`. Two are I1 to I3. The third, `harry-potter` (PoA,
GoF), has no reversed attribute, but the first task (`GoF:20`) has Harry summon the
Firebolt he gets at `PoA:11`: the audit raises it as I4, and the author chose to
substitute his Nimbus Two Thousand (D4, `Overrides`: `—`). The fourth is Harry's single
`born` row (`CoS:8`): one row reverses nothing, so the audit records no finding.
`two-witnesses` has no candidates.

<a id="case-18b"></a>**18b. A stack change.** A Star Trek project order that swaps `TOS:3` and `TMP` is no
longer a permutation once `star-trek/animated@1.0.3` joins the stack. The host refuses
to run and proposes `TOS:1, TOS:2, TMP, TOS:3, TAS:1, TAS:2, …`: each inserted segment
right after the one it follows on the new ruler. Removing the package again proposes
the original order.

## Branch and retelling

<a id="case-19"></a>**19. A branch.** Project `no-horcruxes` (`follow: branch`, divergence point
`PS:17`):
- `lord-voldemort.status` = `dead` from `chapter-01` (D1);
- at `chapter-50`, `harry-potter.broom` is still `Nimbus Two Thousand`, and Harry and
  Sirius are still `strangers`: canon after `PS:17` never happens.

Asking for a cutoff of `PoA:11` in this project is an error: the host reports it and
resolves at `PS:17` instead.

<a id="case-20"></a>**20. A retelling.** Project `blind-harry` (`follow: retelling`) retells year one
with Harry blind (D1). The canon-keeper's divergence audit (`reviews/canon.md`) finds
three conflicts and sets out options without choosing. The author decided:

| Conflict                | Author's choice | Result at its chapter                                                   |
| ----------------------- | --------------- | ----------------------------------------------------------------------- |
| C1 glasses (`PS:2`)     | remove (D2)     | `glasses` absent                                                        |
| C2 Seeker (`PS:9`)      | adapt (D3)      | `role` = `Gryffindor Seeker, flying by sound and feel` from `chapter-09` |
| C3 Nimbus (`PS:10`)     | keep (no entry) | `broom` = `Nimbus Two Thousand` from `chapter-10`, as in canon          |

Canon the divergence doesn't reach still happens: `house` = `Gryffindor` at
`chapter-09`.

<a id="case-20a"></a>**20a. Reach candidates.** For each divergence, the host lists the canon rows on the
attributes it overrides, at or after the cutoff where it first occurs:
- D2 (`glasses`, from `chapter-01`, cutoff `PS:1`) meets `harry-potter.glasses` at `PS:2`;
- D3 (`role`, from `chapter-09`, cutoff `PS:9`) meets `harry-potter.role` at `PS:9`;
- D1 (`sight`) meets no canon row.

Both candidates are addressed in the audit, as C1 and C2. C3 (the Nimbus) is on an
attribute no divergence overrides: the canon-keeper found it by reading ahead, which
the candidate list never replaces. D2 and D3, logged to carry out the author's
decisions, were audited in their turn and raised nothing new.

## Hidden canon

<a id="case-21"></a>**21. True from.** Snape's `loyalty` row is dated `As of: DH:33` (its reveal) and `True
from: PS` (true from the start of canon):
- At `PS:17` it is not resolved, but the snapshot lists it as a **hidden truth**. The
  same holds at `PS:1`.
- At `DH:33` it resolves normally, and is no longer hidden.

<a id="case-22"></a>**22. The author decides.** In the `no-horcruxes` branch, canon never reaches `DH:33`.
When the story touched Snape in chapter 18, the hidden truth was raised with the author,
who chose **reveal early**. The ledger's Hidden canon table records the decision, and
D2 reveals it:
- `severus-snape.loyalty` is absent at `chapter-05`;
- it is `loves Lily Potter, and protects Harry for her sake` from `chapter-20`.

## Errata

<a id="case-e1"></a>**E1. A corrected printing.** The Harry Potter base registers `gof-first-printing` as an
`erratum` source: the first printings of *Goblet of Fire* got the order of the echoes
in ch.34 wrong, and later printings corrected it. Harry's `graveyard-echoes` has the
corrected row from `books` and the error from `gof-first-printing`, both at `GoF:34`:
- `PURIST` at `GoF:37`, in every mode: `his mother's echo emerges first, then his
  father's`. The erratum row never resolves;
- the quotation `q2` resolves the same way: `Speaker` = `lily-potter`;
- no package in the examples holds two rows of one tier, entity, attribute, and point
  with different values. Registering `gof-first-printing` as `primary` instead makes
  the base invalid ([§4.4](../spec/04-temporal.md#44-state-histories)).

<a id="case-e2"></a>**E2. Erratum use.** Prose in which the father's echo emerges first relies on the
erratum, and is flagged as erratum use ([§6.9](../spec/06-divergence.md#69-classifications)) unless a divergence sets that order. Prose
that follows the corrected text is not flagged.

<a id="case-e3"></a>**E3. A theory resting on an erratum.** `harry-potter/theories` holds T2, an illustrative
theory that Lily is held in stasis, not dead. Its only evidence, `GoF:34`, is the
erratum, so a theory audit marks it `(erratum: gof-first-printing)` ([§6.13](../spec/06-divergence.md#613-adopting-a-theory-theory-conflicts)). T1's
evidence has no erratum.

## Series

<a id="case-l1"></a>**L1. A project layer.** Project `two-witnesses-ii` is book 2. Its stack relists book
1's three package layers, then adds `project:two-witnesses@chapter-02`. At its own
cutoff, `OotP:1`:
- `cedric-diggory.status` = `alive` and `scars` = `curse scar across his chest`: book
  1's D1 and D2 apply, though book 2 logs no divergence of its own;
- without the project layer, `status` = `dead`, as in canon;
- the composed roster includes book 1's original character `mara-quill`, with layer
  `project:two-witnesses`.
- book 1's Hidden canon row keeps Snape's `loyalty` hidden (`keep-hidden`, decided in
  `chapter-01`). At `OotP:1` it is still a hidden truth, and book 2 inherits the
  decision rather than raising it again ([§6.4](../spec/06-divergence.md#64-divergencesmd-the-ledger)). Had book 1 decided it after
  `chapter-02`, the pin, book 2 would not inherit it.

<a id="case-l2"></a>**L2. The series ruler.** `lantern-road` is self-contained, with no ruler. In the
stack of `lantern-road-before`, which pins it at `chapter-12`, its manuscript is the
work `lantern-road` ([§4.12](../spec/04-temporal.md#412-the-ruler-of-a-series)): `lantern-road:9` and `lantern-road:12` are valid points,
and `lantern-road:13` is not. Book 2's `canon-timeline.md` inserts `youth` before it
and `after` after it, so `youth < lantern-road:1 < lantern-road:12 < after`. Those two
points are not on the ruler of a stack without book 2. In book 2's stack they are
valid points, and its project order would list all three segments: `youth`,
`lantern-road`, `after` ([§4.2](../spec/04-temporal.md#42-ruler-points), [§6.8](../spec/06-divergence.md#68-rearranging-canon)).

<a id="case-l3"></a>**L3. A split frame.** `lantern-road-before`'s sync points set chapters 1 to 5 in
`youth` and chapter 6 on in `after` ([§6.14](../spec/06-divergence.md#614-where-books-meet-seam-conflicts)). Ines's sheet in book 1 gives her grey eyes
and the role of apprentice lamplighter from the start, and makes her a master from
`chapter-09`.
- At `chapter-01`, all of that is ahead. The Seam conflicts table carries back
  `lantern-road:ines-varga.*` and decides `not-yet` for `lantern-road:*.*@*`, so Ines
  is `eyes` = `grey`, `role` = `apprentice lamplighter`, with no seam conflict.
- At `chapter-06`, nothing is ahead: `role` = `master lamplighter`, and nothing is
  raised.
- Book 1's `chapter-09` row is dated `lantern-road:9`, after `youth`, but it is an
  anchored item, not a row the time filter drops ([§7.2](../spec/07-snapshot.md#72-algorithm), step 3): had the author also
  carried back `lantern-road:ines-varga.role@chapter-09`, an exact item that beats the
  `not-yet` pattern, `role` would be `master lamplighter` at `chapter-01`.
- Promoting `lantern-road` to a base ([§2.9](../spec/02-layout.md#29-promoting-a-self-contained-world)) re-cites its three rows from `project` to
  `lantern-road`, and dates the `master lamplighter` row `lantern-road:9`. Its ruler is
  the one segment `lantern-road`, chapters 1 to 12, the same as the series ruler without
  book 2's inserts, and the promoted project's sync points put `chapter-<NN>` at
  `lantern-road:<NN>`.
- `lantern-road-before`'s seam audit (`reviews/canon.md`) notes the earlier start under
  `- pin:`, and raises S1 to S3, each covered by a Seam conflicts row; every row covers
  one of them.
- The seam audit's first question flags `lantern-road-before` as starting before book
  1's end, and `two-witnesses-ii` as not.

<a id="case-l4"></a>**L4. Undecided seams.** Read `two-witnesses-ii`'s stack at `GoF:20`, before book 1's
`GoF:37`, and everything book 1 brings is ahead, with no decision:
- `mara-quill` has no attributes, and the seam conflicts are
  `two-witnesses:mara-quill.house` and `two-witnesses:mara-quill.year`;
- `cedric-diggory` is canon at `GoF:20` (`status` = `alive`, `role` = `Hogwarts
  Triwizard champion`, with no scar), and the seam conflicts are `two-witnesses:D1`
  and `two-witnesses:D2`;
- at book 2's own cutoff, `OotP:1`, nothing is ahead (L1).

<a id="case-l5"></a>**L5. Value seams.** `two-witnesses-ii` has book 1's stack and mode, so the seam audit
finds no value seam for Harry, Cedric, Hermione, or Snape. Switched to `precedence`, it
finds one: `harry-potter.broom`. Book 1 (`recency`) gave the Firebolt from the books,
and `precedence` gives the fan work's Cleansweep Seven.

<a id="case-l6"></a>**L6. Inherited settings.** A stack of `harry-potter@3.2.2` and
`project:second-year-tournament@chapter-03` sets no order, and so uses book 1's: `GoF:1`
sorts before `CoS:1`. A sequel to the `no-horcruxes` branch MUST be a branch, with a
divergence point no later than `PS:17`.

## Theories

<a id="case-q1"></a>**Q1. Adopting a theory.** Project `three-brothers` (cutoff `DH:36`) stacks
`harry-potter/theories`, whose T1 has four numbered claims. Its D1 has `Basis:
harry-potter/theories:T1 (claims 1, 3, 4)`. The Theory conflicts table records two
conflicts at `DH:35`: claim 2 discarded, and claim 4 adapted with a note. Claim 2
appears in no `Basis`; claim 4 does. The theory's rows never resolve into state:
`albus-dumbledore`'s snapshot is the base's alone, with none of it from the theory.
The base's own rows for him (DH ch.35) resolve as usual, and so does a place in
`places.md`: `kings-cross-limbo` has a snapshot like any entity
([§10.5](../spec/10-formats.md#105-state-histories)).

## Frames and serials

Project `the-long-way-back` is a serial set in Star Trek, using the frames module.

<a id="case-22a"></a>**22a. World points.** A scene's world point is its cutoff ([§7.5](../spec/07-snapshot.md#75-frames-two-cutoffs-at-once)). With the project's
cutoff `TNG:3:15`, a scene in `chapter-03` with world point `TNG:4:1@main` and no
travelers draws a warning (a flash-forward, or a mistake). The same scene with Mira as
a traveler, or a scene at `TNG:3:14@main`, does not.

<a id="case-23"></a>**23. A mechanism and its model.** The Star Trek world declares one mechanism,
`temporal-rift`, with model `mutable` ([§9.1](../spec/09-modules.md#91-frames-time-travel-and-parallel-worlds), [§10.24](../spec/10-formats.md#1024-time-travelmd-frames)). Both of Mira's legs name it. Under
`mutable`, the Enterprise-C's absence replaces history, so `alt-war` splits from `main`
at `TNG:1`. When the ship goes back, `main` is restored and `alt-war` is `overwritten`.
Mira's memories of `alt-war` belong to her own frame, so they are not a frame violation,
and no paradox is recorded.

<a id="case-24"></a>**24. The buffer and early access.** Chapters 1 and 2 are `released`, chapter 3 is in
`early-access`, and chapter 4 is `drafted`, so the buffer is two chapters deep. The
author may release chapter 3. Releasing chapter 4 first MUST be refused ([§13.3](../spec/13-workflows.md#133-serial)), and so
MUST sending it to early access while it is drafted, here, since the example treats
`line-edited` as required ([§13.9](../spec/13-workflows.md#139-early-access)). Chapters 3 and 4 may be revised; chapters 1 and 2 are
locked. Chapter 3's change after it went to early access is logged in `revisions.md`
with audience `early-access` and a reader note, and `reader-a`'s feedback on it is
filed under `references/feedback/chapter-03/`.

<a id="case-25"></a>**25. A registered column.** `timelines.md`'s `## Legs` table adds a `Notes` column
after the required ones. The story-side `index.md` registers it under `## Columns`, so
no warning is raised ([§10.0](../spec/10-formats.md#100-conventions), [§10.3](../spec/10-formats.md#103-indexmd)).

<a id="case-26"></a>**26. A story-dated row.** Mira's sheet gives her starting role without a
`From chapter`, and a second `role` row with `From chapter: chapter-03`, when she
stays behind ([§4.11](../spec/04-temporal.md#411-story-dated-rows)). At `chapter-02` her role is `operations officer, USS
Enterprise-C`; at `chapter-03`, and after the last chapter, it is `displaced officer
aboard the USS Enterprise-D`. The row cites `project` and leaves `As of` empty.

<a id="case-27"></a>**27. Renumbering.** In `the-long-way-back`, chapter 3 is in early access, so
`renumber` may move only chapter 4 onwards: a new chapter inserted before chapter 3 MUST
be refused ([§13.10](../spec/13-workflows.md#1310-inserting-and-renumbering-chapters)). In `two-witnesses`, which `two-witnesses-ii` pins at `chapter-02`,
chapters 1 and 2 keep their ids. `three-brothers` has no readers and no pins, so any of
its chapters may move.

## In-world time

<a id="case-w1"></a>**W1. Calendars.** `harry-potter` and `star-trek` declare `calendar: iso`.
`lantern-road` declares its own ([§4.13](../spec/04-temporal.md#413-in-world-time)): `BL` counts down, `OR` lasts 300 years, `NR`
is open-ended, and a year has four months. `BL 2` and `OR 5` are six years apart, `BL 1`
is the year before `OR 1`, and `OR 300` the year before `NR 1`. `NR 12-05` is invalid
(there are four months), and so are `1991-02-30` and `1900-02-29`; `2000-02-29` is
valid. `lantern-road-before` dates in `lantern-road`'s calendar. A calendar with only
years takes no months: `AC 298-03` is invalid.

<a id="case-w2"></a>**W2. Comparing dates.** `1991` against `1991-09-01`: can't tell. `1990` is before
`1991-09-01`, and `..1991` before `1998..`. `~1975` can't tell against any date, but
sorts at 1975.

<a id="case-w3"></a>**W3. Ruler dates.** Canon stack. The date of `PS:6` is `1991-09-01`, and so is that of
`PS:6:2`, from the deepest dated node. `PS:7` takes `PS`'s `1991..1992`, and `GoF:37`
is `1994..1995`. In the fan stack, `FIC:20` is `1998..`, from the fan work's own
`## Dates`. Trek stack: `TNG:3:15` is `2366`. `PS:1` (`1981-11`) is read before `PS:2`
(`1991-06`) and dated before it, ten years earlier.

<a id="case-w4"></a>**W4. An accepted contradiction.** `PS:1` falls outside `PS` (`outside-parent`), and
the base's `## Accepted` table excuses it. Without that row, the package is invalid.
`DH:33` (`..1998`) against `DH` (`1997..1998`) can't tell, so it is no contradiction.
No stack in the examples has an unaccepted contradiction.

<a id="case-w5"></a>**W5. In-world dates and ages.** Snape's `loyalty` has `True from: PS` and `In-world:
..1971`. Harry's `born` is `1980-07-31`, as of `CoS:8`: he is 11 at `PS:5` and 10 at
`PS:2`, and at `PS:5` his `born` row is not yet visible. Mira's `born` is `2318`: by
world dates she is 47 or 48 at `TNG:3:15`, but she is a traveler, so her own age is the
continuity-editor's judgment ([§4.13](../spec/04-temporal.md#413-in-world-time)). Ines, born `NR 12-02-14`, is 17 or 18 in `NR 30`.

<a id="case-w6"></a>**W6. World history.** In the canon stack, the chronology ([§4.13](../spec/04-temporal.md#413-in-world-time)) at `PS:5` is
`voldemort-falls`; at `PS:6`, `grindelwald-defeated` (`1945`) then `voldemort-falls`;
at `CoS:9`, `hogwarts-founded` (`..991`) first. `grindelwald-defeated` resolves like any
entity: at `PS:5` it has no rows yet. `lantern-road`'s history is `lamps-first-lit`
(`OR 1`), then `road-rebuilt` (`NR 1`). No event has a participant outside their
lifetime.

<a id="case-w7"></a>**W7. Universe time.** `wizards-and-warp` moves Harry Potter by `+373y`, and both bases
are `iso`, so the offset is valid ([§8.1](../spec/08-crossovers.md#81-the-manifest)). Harry's first journey to Hogwarts (`PS:6`) is
`2364-09-01` in universe time, and Grindelwald's defeat (`1945`) is `2318`, before
*The Next Generation*'s first season (`2364`).

## Modules

<a id="case-m1"></a>**M1. Travel.** `lantern-road` enables travel ([§9.4](../spec/09-modules.md#94-travel)). Its routes join `highcairn` and
`lowmere` through `the-halfway-inn`, two days each by cart at the fastest, so the
shortest journey between the towns is four days, either way. Ines is in `highcairn` on
`NR 30-01-10` (chapter 1), at the inn on `NR 30-01-15` (chapter 3), and in `lowmere` on
`NR 30-01-21` (chapter 5): no journey is too fast. An event putting her in `lowmere` on
`NR 30-01-12` would be a warning (at most three days for a four-day journey), but not if
its date were `~NR 30-01-12` or `..NR 30-01-12`.

<a id="case-m2"></a>**M2. Mysteries.** The `harry-potter` base records one mystery ([§9.5](../spec/09-modules.md#95-mysteries)): `moody-identity`,
whose answer is the secret of the same name, revealed at `GoF:35`. Its needed clues are
planted at `GoF:13` and `GoF:25`, and a red herring at `GoF:27`, so it is fair. Harry is
`unaware` at `GoF:34` and `knows` at `GoF:35`. `lantern-road`'s mystery,
`lamps-going-out`, is revealed in chapter 11, with needed clues in chapters 3 and 7 and
a red herring in chapter 5: fair too. A higher layer may add a clue to `moody-identity`,
never redefine `c1`. A mystery whose needed clue is planted in *Chamber of Secrets* and
revealed in *Goblet of Fire* is fair in the ruler's order, and unfair in
`second-year-tournament`'s: the canon-keeper's order audit raises it.

<a id="case-m3"></a>**M3. Lineage.** In the canon stack, Harry's `parents` are `james-potter; lily-potter`
and his `guardians` `petunia-dursley; vernon-dursley`, both from `PS:1`; he has no
guardians from `DH:7`. The family tree of `lord-voldemort` ([§9.6](../spec/09-modules.md#96-lineage)) is just himself at
`GoF:37`; at `HBP:10` it is `merope-gaunt` (whose parent is `marvolo-gaunt`, descended
from `salazar-slytherin`) and `tom-riddle-sr`. The `headmaster-of-hogwarts` is
`albus-dumbledore` at `PS:5`, `dolores-umbridge` at `OotP:30`, `albus-dumbledore` again
at `OotP:38`, and `severus-snape` at `DH:36`. James and Lily, born in 1960 and dead on
`1981-10-31`, raise no lineage warning, and the examples have no lineage contradiction.

<a id="case-m4"></a>**M4. Image prompts.** `two-witnesses/prompts/potter-family-tree.md` is a family tree
from `harry-potter` at `GoF:37` ([§10.29](../spec/10-formats.md#1029-promptsidmd-image-prompts), [§12.20](../spec/12-agents.md#1220-prompter-image-prompts)). The tree at that cutoff is Harry,
James, and Lily, so the prompt names those three and no one else. It gives Harry's
date of birth (known from `CoS:8`), and leaves his parents' dates blank, because their
rows are as of `DH:16`. Asked again at `DH:16`, it could give them.
`lantern-road/prompts/road-map.md` maps the three places, with Highcairn to the north
and Lowmere to the south, from `places.md`, and the two halves of the road the same
length, from the routes. Both prompts list what the bible does not give under
`## Gaps`.

## Viewpoints

<a id="case-v1"></a>**V1. Modes and overrides.** `lantern-road` records a viewpoint per chapter
(`viewpoints: chapter`, [§7.7](../spec/07-snapshot.md#77-viewpoints)). Its outline ([§10.23](../spec/10-formats.md#1023-outlinemd)) overrides chapter 2 to `none` (a
lamp going out on an empty road, seen by no one) and chapter 6 to `scene`: scene 1 is
Ines's, scene 2 the innkeeper's (`tomas-hale`). Every other chapter is Ines's.

<a id="case-v2"></a>**V2. Told from the end.** Ines tells the story from its end (`told_from: end`). Her
knowledge point in chapter 3 is the end, so she knows `lamps-going-out`, which she
learns in chapter 11. In the moment (`Told from: —`) she would not, and told from
chapter 7 she still would not. Either way, chapter 3 may not tell the reader the
answer: the mystery is revealed in chapter 11 ([§9.5](../spec/09-modules.md#95-mysteries)), and `Told from` never moves a
reveal. Chapter 11 may.

<a id="case-v3"></a>**V3. A viewpoint who knows.** The innkeeper knows the answer all along, and his scene
in chapter 6 is told in the moment. His narration still may not state it before
chapter 11.

<a id="case-v4"></a>**V4. Drafted against planned.** Chapter 6 drafted with the scene markers
`viewpoint=ines-varga` and `viewpoint=tomas-hale told-from=—` matches its outline. With
Ines in both scenes, the host warns ([§7.7](../spec/07-snapshot.md#77-viewpoints)).

## Sharing and publishing

<a id="case-u1"></a>**U1. Licenses and credit.** `harry-potter/fanon` is `CC-BY-4.0`, with a
credit line ([§2.10](../spec/02-layout.md#210-licenses-and-credit)). `harry-potter/fanfic/example` uses
`LicenseRef-fan-author-terms`, so its terms are in a `LICENSE.md` beside its manifest. The
`harry-potter` base states no license: a host shows that plainly, and never reads it as
permission. Either license covers the package's own records, never the novels.

<a id="case-u2"></a>**U2. Two authors.** `the-long-way-back` lists two authors, `ade` and
`kit` ([§11.13](../spec/11-agent-contract.md#1113-more-than-one-author)). Either may release a chapter or make an author-only decision, and
the record names who did: Ade released chapter 1 (`released-by: ade`), Kit chapter 2,
and Kit sent chapter 3 to early access (`early-access-by: kit`) ([§10.18](../spec/10-formats.md#1018-manuscript-chapters)). Its
`divergences.md` carries a `By` column in both tables ([§10.8](../spec/10-formats.md#108-divergencesmd)). A hidden-canon row
or an `accepted` consequence with no `By` would be an error here; a divergence with
none is not.

<a id="case-u3"></a>**U3. Content notes.** `the-long-way-back` lists two notes, `death` and
`grief` ([§13.11](../spec/13-workflows.md#1311-content-notes)). For chapter 1 the line-editor suggested `death` and `new:peril`;
the author confirmed `death` only, so `content-notes: [death]`, and the `peril` they
did not keep raises nothing. Chapter 2 needs none (`content-notes: []`), and chapter 3,
in early access, carries `grief`. Chapter 4 is drafted, with no notes yet. If a
revision of chapter 3 led the line-editor to suggest `death` too, the host would warn
until the author confirmed or declined it.

## Releasing and exports

<a id="case-p1"></a>**P1. Releasing.** In `the-long-way-back`, chapters 1 and 2 are released and
chapter 3 is in early access ([§13.12](../spec/13-workflows.md#1312-releasing)). Releasing chapter 3 sets `status: released`
and `released`, keeps its `early-access` date, and, with two authors, records who
released it. Chapter 4 cannot be released before chapter 3, nor while it is drafted
unless the author insists, nor ever while it has a pending decide item, a `TODO`
marker, or unconfirmed content notes. Released together, as the run "3 to 4", the two
chapters share one date, and if chapter 4 fails a check, neither is released.

<a id="case-p2"></a>**P2. A scheduled release.** Ade has scheduled chapter 3 for
`2026-12-01T18:00+00:00` (`release-on`, `release-on-by: ade`). Nothing happens before
then. A host that next runs on 2 December releases it, dated `2026-12-01` and by Ade,
after re-checking: had a `TODO` marker appeared in the meantime, it would remove the
schedule and tell the authors instead. Chapter 4 may be scheduled for 8 December, but
not for 30 November, before chapter 3.

<a id="case-p3"></a>**P3. Withdrawing.** If the authors withdraw chapter 2, it becomes
`withdrawn` and keeps its `released` date. Chapters 1 and 3 are untouched, chapter 3 may
still be released, and the run of released chapters is unbroken. Released again on 8
December, chapter 2 takes `re-released: 2026-12-08` and keeps its first release date.
Under locked releases, only a withdrawn chapter may be re-released.

<a id="case-p4"></a>**P4. A short story's finish.** A short story ends with step 19, the
line-editor's finishing pass, which sets `status: final`, as it does in a novel
([§13.12](../spec/13-workflows.md#1312-releasing)). A `released` status, or a `release-on` schedule, in a novel or a short
story is an error.

<a id="case-p5"></a>**P5. The export.** `the-long-way-back/export/` is what the `export`
skill writes ([§13.13](../spec/13-workflows.md#1313-exporting-for-readers), [§10.30](../spec/10-formats.md#1030-export-chapters-for-readers)). `public/` holds chapters 1 and 2, and
`early-access/` chapters 1 to 3. `chapter-01.md` is headed `# Narendra`, keeps the
prose, and loses the front matter, both scene markers (the second becomes `* * *`),
and the line-editor's comment. `chapter-01.yaml` lists the characters from
`timeline.md` by name (Lt. Mira Oduya, Rachel Garrett, Tasha Yar (altered timeline)),
the readers' words for its content note, and the authors' notes from
`references/chapter-notes/`. The public `work.yaml` knows two chapters and no Picard;
the early-access one knows three, and him. Withdrawing chapter 1 would drop it from
`public/`. A character's true identity behind a reveal alias, such as Barty Crouch Jr.
behind `moody-impostor`, is left out until the audience reaches `GoF:35`.

## Validation cases

A conforming host MUST report each of these if introduced:

- citing the `films` source from the Harry Potter base (a tier its kind does
  not allow, [§2.3](../spec/02-layout.md#23-packages));
- removing `harry-potter/fanon@1.0.5` from `two-witnesses-ii` (a package layer not
  relisted, [§2.2](../spec/02-layout.md#22-layers-and-stacks));
- moving `harry-potter/fanon@1.0.5` below `harry-potter@3.2.2` in any stack (a layer
  below what it relies on, [§2.2](../spec/02-layout.md#22-layers-and-stacks));
- a `PS:6:2+00:41:10` as-of in a stack without `harry-potter/films` ([§4.9](../spec/04-temporal.md#49-adaptations-base-points-with-the-adaptations-timecode));
- changing the animated package's `TAS:1` row to insert after `TOS:4` (an unknown
  segment, [§4.10](../spec/04-temporal.md#410-inserted-works));
- adding claim 2 to `three-brothers`' `Basis` while its decision is `discard` ([§6.13](../spec/06-divergence.md#613-adopting-a-theory-theory-conflicts));
- any invalid point from the table above, used as a row's as-of ([§4.2](../spec/04-temporal.md#42-ruler-points));
- a `two-witnesses` roster row with slug `cedric-diggory` (a union collision, [§2.7](../spec/02-layout.md#27-union-across-layers));
- changing `two-witnesses`' pin to `harry-potter@2.2.0` (a version mismatch, [§2.8](../spec/02-layout.md#28-package-lifecycle-and-versioning));
- deleting the consequence rows for D1 (a divergence with no consequences, [§6.4](../spec/06-divergence.md#64-divergencesmd-the-ledger));
- giving `hogwarts-at-warp` a single `cutoff` (rejected by the schema, [§10.1](../spec/10-formats.md#101-projectyaml));
- removing a book from `second-year-tournament`'s order (not a permutation, [§6.8](../spec/06-divergence.md#68-rearranging-canon));
- deleting D2 or D3 from `second-year-tournament` (an uncovered order inversion, [§6.8](../spec/06-divergence.md#68-rearranging-canon));
- setting D2's `Until` to `chapter-01` (not after `First occurs`, [§10.8](../spec/10-formats.md#108-divergencesmd));
- removing `divergence_point` from `no-horcruxes` (a branch needs one; rejected by the schema, [§6.6](../spec/06-divergence.md#66-branch-or-retelling-how-strictly-later-canon-binds));
- adding a `no-horcruxes` sync point with cutoff `CoS:1` (past a branch's divergence point, [§6.6](../spec/06-divergence.md#66-branch-or-retelling-how-strictly-later-canon-binds));
- giving Snape's `loyalty` row a `True from` of `DH:34`, later than its `As of` (`DH:33`) ([§4.4](../spec/04-temporal.md#44-state-histories));
- deleting D2 from `no-horcruxes` while its Hidden canon row still says `reveal-early` ([§10.8](../spec/10-formats.md#108-divergencesmd));
- releasing `the-long-way-back`'s chapter 4 while chapter 3 is unreleased ([§13.3](../spec/13-workflows.md#133-serial));
- deleting the reader note from its `revisions.md` row ([§10.22](../spec/10-formats.md#1022-revisionsmd));
- changing the `temporal-rift` model to anything outside [§10.24](../spec/10-formats.md#1024-time-travelmd-frames)'s list, or naming an unknown mechanism in a leg ([§10.16](../spec/10-formats.md#1016-timelinesmd-and-branchesmd-frames));
- a world point on a branch that `branches.md` does not register ([§10.16](../spec/10-formats.md#1016-timelinesmd-and-branchesmd-frames));
- removing `layers` from `two-witnesses` while it is `established`, or giving `lantern-road` (`original`) any layer (rejected by the schema, [§6.1](../spec/06-divergence.md#61-when-this-applies));
- giving Mira's `chapter-03` role row an `As of`, or another source than `project` ([§4.11](../spec/04-temporal.md#411-story-dated-rows));
- a `lantern-road:13` point in `lantern-road-before`, past its pin ([§4.12](../spec/04-temporal.md#412-the-ruler-of-a-series));
- a `lantern-road-before` Seam conflicts row with decision `accept` for a project item, or `other` with no note ([§10.8](../spec/10-formats.md#108-divergencesmd));
- a sequel to `no-horcruxes` that is a retelling, or a branch diverging after `PS:17` ([§6.14](../spec/06-divergence.md#614-where-books-meet-seam-conflicts));
- adding `star-trek/animated@1.0.3` to a Star Trek project with a `setting.order` that lacks `TAS:1` and `TAS:2` ([§6.8](../spec/06-divergence.md#68-rearranging-canon));
- `lantern-road` with a `setting.cutoff` ([§4.7](../spec/04-temporal.md#47-self-contained-worlds-without-a-ruler), rejected by the schema);
- registering `gof-first-printing` as `primary` (two tied rows in one package, [§4.4](../spec/04-temporal.md#44-state-histories)), or an `erratum` source in `harry-potter/fanon` ([§2.3](../spec/02-layout.md#23-packages));
- a `calendar` in `harry-potter/fanon` or `two-witnesses`, a `notation` beside `lantern-road`'s custom calendar, or `calendar: gregorian` (rejected by the schema, [§4.13](../spec/04-temporal.md#413-in-world-time));
- `lantern-road`'s `OR` era without `years`, or `BL` (counting down) moved after it ([§4.13](../spec/04-temporal.md#413-in-world-time));
- a date of `1991-02-30` in `## Dates`, or `NR 12-05` in `lantern-road` ([§4.13](../spec/04-temporal.md#413-in-world-time));
- deleting the base's `## Accepted` row for `PS:1` (`outside-parent`, [§4.13](../spec/04-temporal.md#413-in-world-time)), or adding it to `harry-potter/fanon` instead, which holds no part of it;
- an `In-world` of `1999` on a row as of `PS:7`, or an event dated `2001` as of `PS:7` (`in-world-after`, [§4.13](../spec/04-temporal.md#413-in-world-time));
- a character with `born` `2051` and `died` `1990` and no acceptance (`born-died`, [§4.13](../spec/04-temporal.md#413-in-world-time));
- an event in `history.md` with no `date` row ([§4.13](../spec/04-temporal.md#413-in-world-time));
- removing `star-trek`'s calendar while `wizards-and-warp` gives offsets ([§8.1](../spec/08-crossovers.md#81-the-manifest));
- in `lantern-road`'s `routes.md`, the route `the-halfway-inn+highcairn` (not in alphabetical order), a route to a place not in `places.md`, an attribute `boat` (not a mode), or a value `three days` ([§10.26](../spec/10-formats.md#1026-routesmd-travel));
- in the base's `mysteries.md`, the mystery `who-is-it` (not a secret), a red herring marked needed, a clue of kind `hint`, a second clue `c1`, or a clue planted at `GoF:38` ([§10.27](../spec/10-formats.md#1027-mysteriesmd-mysteries)), or a higher layer that moves `c1` ([§10.27](../spec/10-formats.md#1027-mysteriesmd-mysteries));
- a `parents` value that is not in the roster, or two characters each the other's parent, or one descended from herself, with no acceptance (`ancestry-cycle`, [§9.6](../spec/09-modules.md#96-lineage));
- a character born in 2051 whose parent is born in 2070, with no acceptance (`born-before-parent`, [§9.6](../spec/09-modules.md#96-lineage));
- `modules.romance`, or `lineage: "yes"`, in `project.yaml` (rejected by the schema);
- a prompt of kind `poster`, cut off at `GoF:38`, or with a subject `neville-longbottom`, who is not in the stack's roster ([§10.29](../spec/10-formats.md#1029-promptsidmd-image-prompts));
- in `lantern-road`'s outline: a mode `all`; chapter 3 with no viewpoint, or with two rows; a scene of chapter 6 with no viewpoint, or its scenes numbered from 2; a viewpoint in chapter 2; `harry-potter` as a viewpoint (not in the roster); chapter 5 told from `chapter-03`; or a `Told from` on a scene whose viewpoint is `—` ([§10.23](../spec/10-formats.md#1023-outlinemd), [§7.7](../spec/07-snapshot.md#77-viewpoints));
- `viewpoints: all` or `told_from: later` in `project.yaml` (rejected by the schema);
- `license: free to use`, or `MIT OR`, in a manifest, or removing the fan work's `LICENSE.md` ([§2.10](../spec/02-layout.md#210-licenses-and-credit));
- a third author with id `ade`; `released-by: sam` (not an author); or chapter 1 with no `released-by` ([§11.13](../spec/11-agent-contract.md#1113-more-than-one-author));
- `content-notes: [violence]` (not on the list) on chapter 3, `violence` without `new:` among its suggestions, or chapter 3 with no `content-notes`; or any note on a chapter of a project without `content_notes` ([§13.11](../spec/13-workflows.md#1311-content-notes));
- an author with no `name`, an empty `authors` list, or a content note id `Self Harm` (rejected by the schema);
- releasing `the-long-way-back`'s chapter 3 with a `TODO` marker left in it, or the run of chapters 3 and 4 while 4 has a pending decide item; re-releasing chapter 1 under locked releases; withdrawing chapter 3, which was never released; `release-on: next Friday`; or `status: released` in `two-witnesses` ([§13.12](../spec/13-workflows.md#1312-releasing));
- an `export/public/chapter-03.md`, which the public does not have; a comment left in an exported chapter; or a `relationships` entry `mira-oduya&rachel-garrett` ([§13.13](../spec/13-workflows.md#1313-exporting-for-readers), rejected by the schema).

A conforming host SHOULD warn if `the-long-way-back`'s `## Columns` row for `Notes` is
deleted (an unregistered column, [§10.0](../spec/10-formats.md#100-conventions)), if a `timeline.md` event dated `1975` lists
`harry-potter`, born in 1980 ([§4.13](../spec/04-temporal.md#413-in-world-time)), if Ines reaches `lowmere` too fast (M1, [§9.4](../spec/09-modules.md#94-travel)), if a
mystery's needed clue comes after its reveal or it has none before ([§9.5](../spec/09-modules.md#95-mysteries)), or if a
parent is under 12 at a birth, a child is born more than a year after a parent's death,
or a title is held outside its holder's lifetime ([§9.6](../spec/09-modules.md#96-lineage)), or if a chapter readers
have lacks a listed note that the line-editor suggests (U3, [§13.11](../spec/13-workflows.md#1311-content-notes)).
