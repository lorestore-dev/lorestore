# 2. Layout and path resolution

## 2.1 The workspace

A workspace is a directory with up to six top-level folders:

```
<workspace>/
├── worlds/<fandom>/<package>/        # packages: reusable bibles, read-only to projects (§2.3)
├── universes/<universe-id>/          # crossover layers over two or more bases (§8)
├── projects/<project-id>/            # stories
├── extraction/<fandom>/<package>/    # extraction workspace: source texts + extraction records
├── agents/                           # agent files (§11.3)
└── workflows/                        # workflow files (§11.7)
```

Fandom ids, project ids, universe ids, character slugs, and source ids MUST match
`^[a-z0-9]+(-[a-z0-9]+)*$`. Package ids are paths of such segments (§2.3).

## 2.2 Layers and stacks

A project reads canon through a **stack** of **layers**, listed in `project.yaml` from
the base up. The project itself is always the top layer and is never listed.

```
  ┌──────────────────────────────────────────────┐
  │ PROJECT  projects/my-book-2/                 │  its own files and ledger (implicit top)
  ├──────────────────────────────────────────────┤
  │ project:my-book-1@chapter-30                 │  an earlier book: read-only
  │ harry-potter/fanfic/harry-crowe@1.0.0        │  a fan work
  │ harry-potter/fanon@1.3.0                     │  fan conventions
  │ harry-potter/films@1.0.0                     │  an adaptation
  │ harry-potter@3.0.0                           │  the base: holds the ruler
  └──────────────────────────────────────────────┘
                    ▲ bottom: the base, which everything is built on
```

```yaml
layers:                                   # from the base up
  - harry-potter@3.0.0
  - harry-potter/films@1.0.0
  - harry-potter/fanon@1.3.0
  - harry-potter/fanfic/harry-crowe@1.0.0
  - project:my-book-1@chapter-30
resolution: precedence                    # or recency, or fill (§5.4)
```

**Position words.** The spec uses these words in one sense only:

- **Lower**, **below**, and **bottom** mean nearer the base; **higher**, **above**, and
  **top** mean nearer the project. They describe a layer's position in the stack and
  nothing else. Which layer's row wins is decided by the resolution mode (§5.4): under
  `precedence` the highest layer with a row wins, under `fill` the lowest.
- Tiers are ordered the same way, from the base up (§5.2): `primary` is the lowest
  tier.
- **Earlier**, **later**, and **latest** describe rows: their as-of on the ruler
  (§4.2). They never describe layers, tiers, or the order of the `layers:` list.

A layer is one of:

| Layer reference                | Is                                                         | Pinned to            |
| ------------------------------ | ---------------------------------------------------------- | -------------------- |
| `<package-id>@<version>`       | A package (§2.3)                                           | its version (§2.8)   |
| `universe:<id>@<version>`      | A universe: a bridge over two or more bases (§8)           | its version (§8.1)   |
| `project:<id>@chapter-<NN>`    | Another project, read through the end of that chapter      | a chapter            |

Rules:

- **Dependencies sit below.** Every package or base a layer relies on (§2.3) MUST appear
  lower in the stack, at the pinned version. The host MUST report a stack that breaks
  this. It MUST NOT add a missing layer itself, so that the order is always written
  down.
- **One base per fandom.** A stack holds at most one `base` package per fandom. A stack
  with two or more bases MUST include a universe layer that relies on them (§8).
- **Project layers are read-only.** A project layer brings in that project's ledger and
  its own files (original characters, places, systems), as of its pinned chapter. It
  brings in that project's own project layers too, so book 3, listing book 2, also gets
  book 1. The referencing project MUST NOT change any of it; to depart from an earlier
  book, it logs its own divergence (§6).
- **Package layers are relisted, not inherited.** A project layer does not bring in its
  project's package layers. The referencing project MUST list each of them itself, at
  the same major version and the same or a later version. The host MUST report one that
  is missing or older. This keeps every package pin visible in one place.
- **Project-layer pins.** The host MUST warn when a project used as a layer changes at
  or before the pinned chapter: a chapter up to the pin, a ledger row whose
  `First occurs` is at or before it, or one of its own bible files.
- **Self-contained projects.** A project with no layers owns its world layer (§3.1,
  W4). A sequel to a self-contained book lists it as `project:book-1@chapter-NN`, and is
  then established (§6.1), on the series ruler (§4.12).

The same packages read through different stacks give different bibles, without any
package changing:

| Stack (from the base up)                                     | Reads as                                                   |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| `harry-potter`                                               | The books alone                                            |
| `harry-potter`, `harry-potter/films`                         | The films, with the books filling what the films leave out |
| `harry-potter`, `harry-potter/fanon`, `harry-potter/fanfic/…` | The books, enriched by fan conventions and one fan work    |
| `harry-potter`, `star-trek`, `universe:wizards-and-warp`     | A crossover (§8)                                           |

## 2.3 Packages

A **package** is a reusable bible. Packages are grouped by fandom, and each package has
one **kind**:

```
worlds/harry-potter/
├── base/                   # id harry-potter                     kind base
├── films/                  # id harry-potter/films               kind adaptation
├── fanon/                  # id harry-potter/fanon               kind fanon
├── theories/               # id harry-potter/theories            kind theories
└── fanfic/
    └── harry-crowe/        # id harry-potter/fanfic/harry-crowe  kind fanfic
```

A package's id is `<fandom>` for its base, `<fandom>/<package>` for every other kind
except fan works, and `<fandom>/fanfic/<work>` for a fan work. The id MUST match the
folder: the base lives in `base/`, and every other package in the folder its id names.
The folder is named for its place in the stack, not for its status: what counts as
canon is each project's decision (§5.4), not the layout's.

| Kind         | Holds                                                          | Source tiers (§5.2)            | Relies on                 |
| ------------ | -------------------------------------------------------------- | ------------------------------ | ------------------------- |
| `base`       | The base: the authoritative works and other official material  | `primary`, `secondary-official`, `erratum` | nothing       |
| `official`   | Official works whose place in canon is not settled, which a project opts into: an animated series, a line of tie-in novels | `secondary-official`, `erratum` | its base |
| `adaptation` | Another medium's telling of the base: films, a TV series, a stage play | `adaptation`, `erratum` | its base                  |
| `fanon`      | Widely shared fan conventions: the consensus, one value each   | `fanon`                        | its base, and MAY others  |
| `fanfic`     | One imported fan work, credited to its author                  | `fanfic`                       | its base, and MAY others  |
| `theories`   | Cited interpretations, each with numbered claims (§6.13)       | `theory`                       | its base, and MAY others  |

**A base is always pure.** A `base` package MUST register only `primary`,
`secondary-official`, and `erratum` sources. Everything else goes in its own package, so
that a project gets fan material only by stacking it.

Every package has a `package.yaml` (§10.2) declaring its `kind` and its
`relies-on` list, pinned. A package that relies on another describes the entities of
the packages below it, using their slugs and their base's ruler, and MAY add entities of
its own:

```
worlds/<fandom>/<package>/
├── package.yaml            # identity, kind, version, status, relies-on (§10.2)
├── index.md                # endpoint registry (§10.3)
├── canon-timeline.md       # base: the ruler (§4). Official: works it inserts (§4.10). Adaptation: what it adapts (§4.9)
├── sources.md              # source registry (§5)
├── glossary.md
├── …                       # the rest of the world layer (§3.3)
└── characters/
    ├── _roster.md          # the characters this package defines
    └── <slug>.md           # one sheet per character, or an extension sheet (§2.7)
```

Only a base has a ruler. Every other package dates its rows on its base's ruler. An
`official` package with works of its own MAY insert them into that ruler (§4.10).

**The base holds what is not in dispute.** Official material whose canon status fans or
the rights holders dispute goes in an `official` package, so that the package never has
to settle the question. Each project settles it for itself, through its stack and
resolution mode (§5.4): leave the package out, and the material is not canon for that
story; stack it with `fill`, and it adds what only it covers but loses every conflict
with the base; stack it with `precedence`, and it counts in full.

*Example.* Whether Star Trek's animated series is canon has been argued over for
decades. It is the package `star-trek/animated`, of kind `official`, and inserts its two
seasons after The Original Series' third.

A package contains **only** world-layer files (§3). It never contains source texts,
extraction records, manuscripts, or anything story-specific. The one place source
wording appears is `quotations.md`, which holds short, important lines (Hagrid's
*"Yer a wizard, Harry"*, PS ch.4) with precise citations (§5.6), never passages.

## 2.4 Extraction workspace

```
extraction/<fandom>/<package>/        # mirrors the package's path under worlds/
├── texts/                  # the source material being extracted. Never shipped.
│   └── <work>/…
└── extractions/
    └── <work>/
        └── ch<NN>.md       # one extraction record per source unit (§10.6)
```

The extraction workspace sits outside the package so that a package can be shared
without its source texts. Extraction records are the provenance trail behind the
package; they SHOULD be retained but are not part of it.

## 2.5 Project

```
projects/<project-id>/
├── project.yaml            # configuration and the stack (§10.1)
├── showrunner-log.md       # the showrunner's running plan (control file, never canon)
├── revisions.md            # changes to chapters readers have already seen (§10.22)
├── bible/                  # the project's own layer: story files, and its own world-layer additions
│   ├── premise.md
│   ├── outline.md
│   ├── style.md
│   ├── divergences.md      # established worlds: the divergence ledger (§6.4)
│   ├── sync-points.md      # established worlds: cutoff per chapter (§6.7)
│   ├── timeline.md         # story-time events
│   └── characters/
│       ├── _roster.md      # this project's own (original) characters only
│       └── <slug>.md       # one sheet per original character
├── manuscript/
│   └── chapter-<NN>.md
├── reviews/                # advisory diagnostics, never canon
├── derived/                # rebuildable caches, never canon (§7.6)
│   └── bible/              # the composed bible: every layer merged (§7.6)
├── references/             # user-supplied input
│   └── feedback/           # human readers' notes, per chapter (§10.25)
└── runs/                   # orchestrator run records (format implementation-defined)
```

## 2.6 Agent paths and how they resolve

Agents name files with **agent paths**, which are relative to a **context**. There are
three contexts.

**Project context** (every workflow except extraction and crossover). Agent paths are
rooted at the project, with these prefixes:

| Agent path prefix   | Resolves to                                |
| ------------------- | ------------------------------------------ |
| `project.yaml`      | `projects/<p>/project.yaml`                |
| `showrunner-log.md` | `projects/<p>/showrunner-log.md`           |
| `revisions.md`      | `projects/<p>/revisions.md`                |
| `bible/…`           | see the resolution rules below             |
| `manuscript/…`      | `projects/<p>/manuscript/…`                |
| `manuscript/@<q>/…` | `projects/<q>/manuscript/…`, for a project layer `q`, up to its pinned chapter (read-only) |
| `reviews/…`         | `projects/<p>/reviews/…`                   |
| `derived/…`         | `projects/<p>/derived/…`                   |
| `references/…`      | `projects/<p>/references/…`                |

**Package context** (the extraction workflow, §13.6). Agent paths are rooted at the
package being built:

| Agent path prefix        | Resolves to                                           |
| ------------------------ | ----------------------------------------------------- |
| `bible/…`                | `worlds/<package path>/…`                             |
| `bible/@<package-id>/…`  | a package this one relies on (read-only)              |
| `texts/…`                | `extraction/<package path>/texts/…`                   |
| `extractions/…`          | `extraction/<package path>/extractions/…`             |

**Universe context** (the crossover workflow, §13.7). Agent paths are rooted at the
universe:

| Agent path prefix      | Resolves to                       |
| ---------------------- | --------------------------------- |
| `universe.yaml`        | `universes/<u>/universe.yaml`     |
| `bridge.md`            | `universes/<u>/bridge.md`         |
| `brief.md`             | `universes/<u>/brief.md`          |
| `bible/@<base-id>/…`   | the base package (read-only)      |

In universe context only `bridge.md` is writable. The bases are read-only, as they are
to projects (§3.1).

### Resolving `bible/<path>` in project context

**Reads** resolve to the **composed bible**, `derived/bible/<path>` (§7.6): one view of
every layer in the stack plus the project's own `bible/`, with each row labeled with the
layer and source it came from. Agents therefore see one bible, whatever the stack. The
host MUST make sure the composed bible is current (rebuilt, or rebuilt on demand)
before an agent reads it.

- **One base.** `bible/<path>` is the composed file.
- **Two or more bases** (a universe layer, §8). World-layer paths MUST be qualified by
  base: `bible/@<base-id>/<path>` is the composed file for that base and the layers of
  its fandom. `bible/bridge.md` resolves to the universe's bridge. The project's own
  story-layer files are unqualified. An unqualified world-layer path is an error.

`bible/@<base-id>/<path>` is also valid with one base, and is equivalent to the
unqualified form.

### Writes

A write to `bible/<path>` goes to the project's own `projects/<p>/bible/<path>`. The
host MUST refuse any write that resolves into `worlds/`, `universes/`, another project,
or `derived/bible/`, which only the `compose` skill writes (§7.6).

A project's own file at a world-layer path is the project's contribution to that file's
union (§2.7): it can add new entries, never redefine a lower layer's.

## 2.7 Union across layers

Every world-layer file is read as a **union** across the stack: the base's rows first,
then each higher layer's, in stack order, then the project's own. Each row keeps a label
naming its layer.

Each file has a **key**: the slug in a roster, the term in a glossary, the entry id in a
catalog or `time-travel.md`, the place id in `places.md`, the path in `index.md`.

- **A layer adds keys; it never redefines one.** A key already defined by a lower layer
  MUST NOT be defined again by a higher one, and the host MUST report it. A Harry Potter
  fanon package cannot redefine `harry-potter`; a project cannot redefine a canon name.
- **Packages add rows to lower layers' entities.** A package describes an entity defined
  lower in its stack by adding state-history rows that cite its own sources. For a
  character, it does this in an **extension sheet**: a `characters/<slug>.md` whose
  front matter holds the `slug` and `extends: <package-id>`, naming the package that
  defines the slug. An extension sheet holds a state history and notes, never the
  identity fields of the roster.
- **Packages re-attribute lower layers' quotations.** In `quotations.md`, a row whose
  `ID` is qualified as `<package-id>:<ID>` is a row for that package's quotation, not
  a new key (§10.13). A film that gives a line to another character says so this way.
- **Projects change lower layers only through the ledger.** A project MUST NOT hold an
  extension sheet. To change an entity it did not define, it logs a divergence (§6).
- **Projects add their own entities to any file.** A project MAY add original
  characters, places, spells, mechanisms, and terms to the matching world-layer files
  in its own `bible/`. Their rows cite the reserved source `project` (§5.1). What the
  story then establishes about them is dated by chapter (§4.11).
- **Bases stay apart.** With two or more bases, keys keep their base qualifier
  (`<base-id>:<slug>`), and collisions between bases are resolved by the bridge (§8.3).

`index.md` is a union in the same way: each layer registers its own files.

## 2.8 Package lifecycle and versioning

`package.yaml` carries a `status` and a `version`.

- **`status: open-for-extraction`**: the extraction pipeline is still adding to it.
- **`status: locked`**: extraction is complete.

A package is read-only to every consuming project **in both states** (§3.1).

`version` is a semantic version. The extraction pipeline MUST bump it on every change
to a package:

| Bump      | When                                                                                               |
| --------- | -------------------------------------------------------------------------------------------------- |
| **major** | The ruler is reordered, a ruler point is removed, a slug is renamed or removed, a source is removed, a relied-on package is re-pinned to a new major version |
| **minor** | Facts, works, sources, or files are added                                                          |
| **patch** | Values or citations are corrected without adding or removing anything                              |

Every pin names an exact version: a project's layers, a package's `relies-on`, and a
universe's `relies-on`. When a package's version differs from a pin, the host MUST warn,
and SHOULD schedule a canon-keeper pass before further drafting. After a major bump the
host SHOULD NOT proceed until a human has re-pinned. Re-pinning a project's layers
changes its composed bible, which is rebuilt (§7.6).

Keeping several versions of a package side by side is left to version control and is
out of scope.

## 2.9 Promoting a self-contained world

A self-contained project's world layer can become a shared base:

1. Copy every world-layer file (§3.3) from `projects/<p>/bible/` to
   `worlds/<fandom>/base/`.
2. Add `package.yaml` with `kind: base`, `version: 1.0.0`, and a `sources.md`
   registering the project as a `primary` source.
3. Write the base's ruler, `canon-timeline.md` (§10.4): the book's manuscript as a
   work, with the project's id, the one level `chapter`, and its chapters as
   `Children`, as the last segment, after any eras the book defined (§4.12).
4. Re-cite every copied row that cites the reserved source `project` (§5.1) to that
   source, keeping its citation. Give each story-dated row (§4.11) the as-of of its
   chapter on the book's work, `<id>:<n>`, and drop the `From chapter` column.
5. Remove the copied files from the project, and add the base to its stack:
   `layers: [<fandom>@1.0.0]`. The project is now established (§6.1): set
   `setting.type: established`, and give each chapter its own point as a sync point
   (`chapter-<NN>` at `<id>:<NN>`, §10.21), so each row becomes visible at the chapter
   it did before.

Promote a book once its chapters are written: a chapter added later is past the work's
`Children` until a new version of the base counts it (§2.8).

From then on the package is read-only, including to the project it came from. The
base's ruler is the series ruler a later book would use (§4.12): the book's manuscript
as a work, after any eras it defined.

**Promoting a series.** Each book stacked as a project layer brings its ledger, its
sync points, and its seam decisions (§6.14), and every later book adds more. Once a
project stacks two or more project layers, the host SHOULD suggest promoting the
earlier books into a package. A self-contained series becomes a base, as above, with
every book's manuscript on its ruler. An established series becomes a `fanfic` package
that relies on its base (§2.3), registering each book as a `fanfic` source. Either
way, every row citing `project` is re-cited to its book's source, and the promotion
dates each row the books brought in at its anchor (§6.14): an
override or a story-dated row at its book's cutoff at the chapter, and an original
entity's starting state at its book's first cutoff, earlier where a seam decision
carried it back. The author reviews the result before the package is locked, and the
project then stacks the package in place of the project layers.
