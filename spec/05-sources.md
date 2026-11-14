# 5. Sources, tiers, and profiles

Every fact carries a **source id**. The source registry (`sources.md`) resolves the id
to a **tier** and an **attribution**. A world's **profiles** (`world-config.yaml`)
decide which sources a draft may draw on, and in what order of precedence.

## 5.1 The source registry

`sources.md` lists every source the world's rows cite (format: §10.7). Per source it
records:

- **id**: what rows cite;
- **tier** (§5.2);
- **title** or description;
- **author / origin**;
- **notes**;
- **bibliographic metadata** (author, year, title, container, volume, issue, pages,
  DOI or URL, edition, publisher), which the `cite` skill renders as APA, MLA, or
  Chicago references.

A row citing an id that is not in the registry is invalid, with two exceptions.

### Reserved source ids

| Id        | Tier        | Exists in                    | Meaning                                                                                  |
| --------- | ----------- | ---------------------------- | ---------------------------------------------------------------------------------------- |
| `project` | `story`     | every project                | Facts the project itself establishes in its story layer (for example, an original character's sheet). |
| `bridge`  | `crossover` | every universe               | Crossover-only canon defined in `bridge.md` (§8).                                        |

Reserved ids are never registered in `sources.md`, and MUST NOT be redefined there.
Both are **implicitly active**: in project context the snapshot treats `project` as
first in every profile, and in a universe it treats `bridge` as second. Neither can
override a world's facts. A project changes canon only through its ledger (§6), and
`project` rows only describe story-layer entities.

## 5.2 Tiers

| Tier                 | What it is                                                                     |
| -------------------- | ------------------------------------------------------------------------------ |
| `primary`            | The authoritative source (for example, the novels).                            |
| `secondary-official` | Other official material (author interviews, companion books, official sites). |
| `fanon`              | Widely shared fan conventions.                                                 |
| `fanfic`             | A specific imported fan work, credited to its author.                          |
| `theory`             | Interpretations produced by the theorist (§12.5). Opt-in only.                 |
| `crossover`          | Canon that exists only in a universe's bridge (§8). Universe projects only.    |
| `story`              | Facts a project establishes about its own story-layer entities. Reserved id `project` only. |

Default authority, from high to low:

```
primary > secondary-official > fanon > fanfic > theory
```

`crossover` and `story` are outside this order. Each is authoritative for the entities
it defines (bridge entities and story-layer entities respectively) and silent on
everything else.

**Tiers describe; profiles decide.** Snapshot resolution (§7) uses the profile's order,
not tier order. A profile SHOULD list sources in non-increasing tier order, and a host
SHOULD warn when one does not.

## 5.3 Canon basis

`world-config.yaml` declares the world's **canon basis**:

```yaml
canon_basis:
  primary: books        # the authoritative source id
  also_canon: []        # lower-precedence ids allowed where they do not conflict
  excluded: [films]     # ids treated as non-canon
```

Excluded sources are still registered, so that a detail unique to them can be
recognized and flagged as a **source leak**. An excluded id MUST NOT appear in any
profile.

For example, Harry Potter excludes the films (`excluded: [films]`), so a detail found
only in the films, such as Hermione's use of *Oculus Reparo* on the train, is a leak.
Star Trek excludes the animated series (`excluded: [tas]`), following its long-standing
treatment as non-canon.

## 5.4 Profiles

A **profile** is a named, ordered list of active source ids, highest precedence first,
together with a **resolution mode**:

```yaml
canon_profiles:
  book-purist:  { order: [books] }
  interpretive: { order: [books, theory] }
  enriched:     { order: [books, fanon-hp, fanfic-example] }
  enhanced:     { order: [books, fanon-hp, fanfic-example], resolution: recency }

active_profile: book-purist   # the world's default
```

### Resolution modes

The mode decides what happens when two active sources disagree about the same
attribute (§7.2, step 4):

| `resolution`             | Rule                                                                                                 | Use for                                                           |
| ------------------------ | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `precedence` *(default)* | The source earliest in `order` wins. A lower source only fills attributes the higher ones leave empty. | Faithful drafting: lower tiers add detail but never overrule canon. |
| `recency`                | The **latest** row wins, whichever source it comes from. `order` only breaks ties at the same point. | **Enhanced** drafting: fanon and fan works can move a character on from where canon left them. |

*Example.* The books set Harry's glasses at `PS:2`. An imported fan work gives him
contact lenses at `PoA:1`. At a `GoF` cutoff, `book-purist` cannot see the fan work, and
`enriched` sees it but lets the books win: both resolve to the books' glasses.
`enhanced` lists the same sources as `enriched`, but resolves by recency, so the fan
work's later row wins and Harry wears contact lenses.

The project's own changes are not part of this choice. A divergence in the project's
ledger (§6) overrides the resolved value under **every** profile.

- Profiles are defined **only** by the world, in `world-config.yaml`. A project
  **selects** one (`setting.active_profile` in `project.yaml`) and MUST NOT define or
  modify one. A self-contained project defines its profiles in its own
  `bible/world-config.yaml`.
- If a project selects none, the world's `active_profile` applies.
- A profile lists source **ids**. Including a `theory`-tier source opts the draft into
  theories.
- A universe project selects a profile per world (`setting.active_profiles`, §8).

This is the "same files, different lens" mechanism: one bible resolves to different
characters under `book-purist` and under `enhanced`.

## 5.5 Coexistence, not overwriting

Lower-tier facts sit **beside** higher-tier ones; they never replace them in the file.
A thin-canon character gets fanon and fanfic rows next to her few canon rows. Daphne
Greengrass is little more than a name in the books, and fanon supplies her house and
personality. Star Trek's background crew, the security officers who never get a line,
get the same treatment. Which value wins is decided only at query time, by the profile
(§7).

## 5.6 Attribution

Provenance is also attribution. Imported fan works MUST be registered with their
authors credited. The extractor records facts **in its own words**, never by copying a
source's prose. The only exception is `quotations.md`, which holds short verbatim lines
with precise citations.
