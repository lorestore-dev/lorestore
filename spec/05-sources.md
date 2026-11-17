# 5. Sources, tiers, and resolution

Every fact carries a **source id**. The id is local to the package that holds the row,
and that package's source registry (`sources.md`) resolves it to a **tier** and an
**attribution**. Which packages a draft can see is decided by the project's **stack**
(§2.2). How their rows combine is decided by the project's **resolution mode** (§5.4).

## 5.1 The source registry

`sources.md` lists every source the package's rows cite (format: §10.7). Per source it
records:

- **id**: what rows cite;
- **tier** (§5.2);
- **title** or description;
- **author / origin**;
- **notes**;
- **bibliographic metadata** (author, year, title, container, volume, issue, pages,
  DOI or URL, edition, publisher), which the `cite` skill renders as APA, MLA, or
  Chicago references.

A row citing an id that is not in its own package's registry is invalid, except for the
two reserved ids below. Because ids are local, two packages MAY use the same id;
provenance always names the layer as well as the source
(`harry-potter/fanon:conventions`).

### Reserved source ids

| Id        | Tier        | Exists in                    | Meaning                                                                                  |
| --------- | ----------- | ---------------------------- | ---------------------------------------------------------------------------------------- |
| `project` | `story`     | every project                | Facts a project establishes about its own entities: original characters, places, systems (§2.7). |
| `bridge`  | `crossover` | every universe               | Crossover-only canon defined in `bridge.md` (§8).                                        |

Reserved ids are never registered in `sources.md`, and MUST NOT be redefined there.
Each belongs to its own layer. Neither can override a lower layer's facts: `project`
rows describe only the project's own entities, `bridge` rows only crossover entities,
and a project changes anything else only through its ledger (§6).

## 5.2 Tiers

| Tier                 | What it is                                                                     | Package kind  |
| -------------------- | ------------------------------------------------------------------------------ | ------------- |
| `primary`            | The authoritative source (for example, the novels).                            | `base`        |
| `secondary-official` | Other official material (author interviews, companion books, official sites, an animated series). | `base`, `official` |
| `adaptation`         | An official retelling in another medium (the films of the novels).             | `adaptation`  |
| `fanon`              | Widely shared fan conventions.                                                 | `fanon`       |
| `fanfic`             | A specific imported fan work, credited to its author.                          | `fanfic`      |
| `theory`             | Interpretations, from fans or the theorist (§12.5), with numbered claims.      | `theories`    |
| `erratum`            | A source's acknowledged error, which the source later corrected (§4.4).        | `base`, `official`, `adaptation` |
| `crossover`          | Canon that exists only in a universe's bridge (§8).                            | universe      |
| `story`              | Facts a project establishes about its own entities. Reserved id `project` only. | project      |

A package MUST register only the tiers of its kind (§2.3). Tiers are ordered like the
stack, from the base up, so the base's tiers are the lowest:

```
primary < secondary-official < adaptation < fanon < fanfic < theory
(lowest)                                                    (highest)
```

`crossover`, `story`, and `erratum` are outside this order. `crossover` and `story` are
each authoritative for the entities they define (bridge entities and a project's own
entities respectively) and silent on everything else. `erratum` defines nothing and
never resolves (below).

**Tiers describe; the stack decides.** Across layers, the resolution mode uses the
stack's order (§5.4). Tier order only breaks ties between sources **within one layer**,
and there the **lowest tier wins**, in every mode: in a base, `primary` beats
`secondary-official`.

**Theories never resolve.** Rows of tier `theory` are interpretations, never state. The
snapshot ignores them (§7.2). A theory reaches a story only when the project adopts its
claims through a divergence (§6.13).

**Errata never resolve.** A source's error that it later corrected, such as a passage
of a first printing that later printings fixed, is kept for completeness. The package
registers the erroneous edition as its own source, of tier `erratum`, and records only
the passages that differ. The corrected text is recorded as usual. The snapshot ignores
erratum rows (§7.2), but agents read them: the canon-keeper flags prose that relies on
an erratum (§6.9), and a theory may cite one as evidence (§6.13).

**Example cases:** [E1](../examples/README.md#case-e1).

## 5.3 Pure bases and source leaks

A base (`base` package) holds only `primary` and `secondary-official` sources whose
place in canon is not in dispute, and the errata of those sources. Official material
whose status is disputed, such as Star Trek's animated series (§2.3), adaptations, such
as the films, and everything fan-made are separate packages of the same fandom. A
project sees it only by stacking it.

That makes **source leaks** checkable. A detail that appears only in a package of the
same fandom that is **not** in the project's stack is a leak (§6.9). For example, in
the films Hermione mends Harry's glasses with *Oculus Reparo* on the train, a detail the
novel does not have. It lives in `harry-potter/films`. A project whose stack is
`harry-potter` alone is a book project, so a draft that uses the spell has leaked the
films. A project that stacks the films can use it.

**Example cases:** [I1](../examples/README.md#case-i1), [A1](../examples/README.md#case-a1).

## 5.4 Resolution

The project's `resolution` (in `project.yaml`, §10.1) decides what happens when rows
from different layers disagree about the same attribute (§7.2, step 4). It applies to
the whole stack.

| `resolution`             | Rule                                                                                                 | Use for                                                           |
| ------------------------ | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `precedence` *(default)* | The **highest layer** with a row for the attribute wins; within it, the lowest tier, then the row with the latest as-of. Lower layers fill only what the higher ones leave empty. | Reading a work through its adaptation, fanon, or fan work: the higher layer's version is the one the story uses. |
| `recency`                | The row with the **latest as-of** wins, from whichever layer. At the same point, the higher layer, then the lower tier, breaks the tie. | **Enhanced** drafting: a fan layer can move a character on, and later canon can move them on again. |
| `fill`                   | The **lowest layer** with a row for the attribute wins; within it, the lowest tier, then the row with the latest as-of. Higher layers supply only what the lower ones leave empty. | **Enriched** drafting: canon stands wherever it speaks, and fan layers flesh out what it leaves blank. |

**Overriding is a choice too.** The films often give Hermione a line that the books
give Ron: in *Prisoner of Azkaban* ch.17, it is Ron who tells Black he will have to
kill them all to kill Harry, and in the film it is Hermione. The films package
re-attributes the line (§2.7). A project that stacks the films with `precedence` gives
the line to Hermione, and so does `recency` (both rows are dated at the same point,
so the higher layer wins); with `fill` it stays Ron's.

`fill` is how an author makes a thinly drawn canon character their own without
contradicting canon. Canon gives Daphne Greengrass little more than her year. With
`fill`, a stack of `harry-potter` and `harry-potter/fanon` gives her the fanon house,
Slytherin, while her year still comes from the books. To go further and change what
canon does say, the author logs a divergence (§6).

*Example.* The books give Harry round glasses at `PS:2`, a Nimbus Two Thousand at
`PS:10`, and a Firebolt at `PoA:11`. An imported fan work, stacked above them, gives
him a Cleansweep Seven at `PS:10` and contact lenses at `PoA:1`.

| Stack, cutoff `PoA:11`                     | glasses        | broom            | Why                                                      |
| ------------------------------------------ | -------------- | ---------------- | -------------------------------------------------------- |
| `harry-potter`                             | round          | Firebolt         | The books alone                                          |
| `harry-potter`, fan work; `precedence`     | contact lenses | Cleansweep Seven | The fan work is the higher layer, and has a row for both |
| `harry-potter`, fan work; `recency`        | contact lenses | Firebolt         | The fan work's lenses are the latest glasses row; the books' Firebolt is the latest broom row |
| `harry-potter`, fan work; `fill`           | round          | Firebolt         | The books have a row for both, so the fan work adds nothing here |

The project's own changes are not part of this choice. Divergences in the ledgers (§6)
override the resolved value under **every** mode.

Quotations resolve the same way: each column of a quotation (`Speaker`, `Line`) is
resolved like an attribute, from the rows the stack's layers give for it.

This is the "same files, different lens" mechanism: the same packages resolve to
different characters under different stacks and modes, and no package changes.

**Example cases:** [3](../examples/README.md#case-3), [3a](../examples/README.md#case-3a), [4](../examples/README.md#case-4).

## 5.5 Coexistence, not overwriting

Facts from higher tiers (fanon, fan works) sit **beside** primary canon, in their own
packages; they never replace it. A thin-canon character gets fanon rows in the fanon
package, next to her few canon rows in the base. Daphne Greengrass is little more than a
name in the books, and `harry-potter/fanon` supplies her house in an extension sheet
(§2.7). Star Trek's background crew, the security officers who never get a line, get the
same treatment. Which value wins is decided only at query time, by the stack and the
resolution mode (§7).

## 5.6 Attribution

Provenance is also attribution. Imported fan works MUST be registered with their
authors credited. A theory or convention whose origin cannot be traced (forum posts
long offline, an idea that spread before anyone recorded it) is credited to "the fan
community (origin untraced)", with the earliest known reference where there is one.

The extractor records facts **in its own words**, never by copying a source's prose.
The only exception is `quotations.md`, which holds short verbatim lines with precise
citations.
