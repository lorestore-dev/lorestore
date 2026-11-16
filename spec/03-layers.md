# 3. Layers and the write boundary

This chapter is the single authority on which layer each file belongs to and who may
write it. Agent specifications (§12) and workflows (§13) MUST agree with it.

## 3.1 The write boundary

**W1. Every layer below a project is read-only to it.** Packages, universes, and
project layers alike, whether a package is `open-for-extraction` or `locked`. In
project context the host MUST refuse any write that resolves into `worlds/`,
`universes/`, another project, or `derived/bible/` (§2.6).

**W2. Only the extraction pipeline writes a package.** The pipeline consists of the
steps of the extraction workflow (§13.6), run in package context: the worldbuilder (a
base's ruler, an adaptation's map, or an official package's or a fan work's inserts), the
character-designer (seeding the roster), the merger (every other state-bearing file),
the theorist (`theories.md`, in a `theories` package), and the `indexer` skill
(`index.md`). Humans write `package.yaml` and `sources.md`. A package never writes to
the packages it relies on. Every change bumps the package version (§2.8).

**W2a. Only the crossover workflow writes a universe's bridge.** The bridge-builder
drafts `bridge.md` in universe context (§13.7), and a human approves it at the gate.
Every change bumps the universe's version (§8.1).

**W3. A project changes lower layers only through its divergence ledger.** If a story
needs canon, fanon, or an earlier book to be different, it does **not** edit that
layer: it logs a divergence in `bible/divergences.md` (§6). The shared packages stay
pristine; the fork lives with the story that made it.

**W4. A project owns its own layer.** The project's builder agents (worldbuilder,
character-designer, architect) write its story layer and its own world-layer additions
(original characters, places, systems, and, in a later book of a series begun by a
self-contained book, the ruler's inserts; §2.7, §4.12) directly. A project with no
layers is **self-contained**, and those additions are its whole world layer. Promotion
(§2.9) turns them into a read-only base.

**W5. Reviews and caches are never canon.** `reviews/` is advisory and `derived/` is
rebuildable. No agent may treat either as a source of facts that overrides the bible.
The composed bible in `derived/bible/` is a view of the layers, not a layer: when it
disagrees with them, it is stale (§7.6).

**W6. One writer per file per step.** At most one step writes a given file at a time
(§11.5).

> **IWE rule:** present every row from a lower layer as read-only, labeled with its
> layer, and route any "change canon" action to the project's divergence ledger.

## 3.2 Layers

| Layer          | Meaning                                                                         |
| -------------- | ------------------------------------------------------------------------------- |
| **world**      | Describes the world. Read as a union across the stack (§2.7).                   |
| **story**      | Specific to one story.                                                          |
| **union**      | A world-layer file that nearly every layer holds part of: the roster, the glossary, and `index.md` (§2.7). |
| **config**     | YAML manifests.                                                                 |
| **manuscript** | The prose.                                                                      |
| **review**     | Advisory diagnostics.                                                           |
| **cache**      | Derived from other files and rebuildable at any time.                           |
| **control**    | Orchestration state (`showrunner-log.md`, run records).                         |
| **input**      | Material supplied by a human for agents to read (`texts/`, `references/`).      |

## 3.3 File catalog

The **Writer** columns name the only agent or actor that may write the file.
"Package" means a package built by the extraction pipeline (W2). "Project" means a
project's own additions to the file (W4). A dash means the file is not used in that
setting. One exception spans the catalog: the `renumber` skill rewrites chapter ids in
any project file (§13.10).

### World layer

| File (under `bible/`)        | Layer  | Holds                                                                                              | Writer: package                | Writer: project        |
| ---------------------------- | ------ | -------------------------------------------------------------------------------------------------- | ------------------------------ | ---------------------- |
| `package.yaml`               | config | Identity, kind, version, status, relies-on (§10.2)                                                 | human                          | — (`project.yaml`)     |
| `index.md`                   | union  | Endpoint registry: which files exist, what each holds, each file's layer (§10.3)                   | `indexer` skill                | `indexer` skill        |
| `canon-timeline.md`          | world  | Base: the ruler (§4). Official, fanfic, or a later book of a series: works it inserts (§4.10, §4.12). Adaptation: its works and the base nodes each adapts (§4.9) | worldbuilder (step F0)         | worldbuilder (self-contained, optional, §4.7; a later book's inserts, §4.12) |
| `sources.md`                 | world  | Source registry (§5)                                                                               | human                          | human (self-contained only) |
| `glossary.md`                | union  | Canonical names and terms; the anti-drift file                                                     | merger                         | worldbuilder           |
| `world.md`                   | world  | Setting, era, rules and systems (each with cost and limit), as a state history                     | merger                         | worldbuilder           |
| `places.md`                  | world  | Atlas: places, connectivity, access control, state over time                                       | merger                         | worldbuilder           |
| `society.md`                 | world  | Law, institutions, politics, economy, customs                                                      | merger                         | worldbuilder           |
| `culture.md`                 | world  | Food, holidays, fashion, media, sayings                                                            | merger                         | worldbuilder           |
| `languages.md`               | world  | Languages: speakers, on-page rendering, translation (languages module, §9.3)                       | merger                         | worldbuilder           |
| `lang/<language>.md`         | world  | Dictionary for one constructed language                                                            | merger                         | worldbuilder           |
| `magic/<catalog>.md`         | world  | Catalogs (spells, potions, creatures, artifacts, games): theory vs. practice, definition level     | merger                         | worldbuilder           |
| `game-system.md`             | world  | LitRPG: the System's rules (§9.2)                                                                  | merger                         | worldbuilder           |
| `time-travel.md`             | world  | Frames: time-travel mechanisms, each with its model, reach, and limits (§9.1)                      | merger                         | worldbuilder           |
| `plot-architecture.md`       | world  | Canon setups and payoffs, prophecies, foreshadowing, running mysteries                             | merger                         | — (the outline's ledger serves) |
| `knowledge.md`               | world  | Who knows what, dated: secrets and reveals                                                         | merger                         | architect; chronicler (story-dated rows, §4.11) |
| `relationships.md`           | world  | Pairwise relationship state histories                                                              | merger                         | character-designer; chronicler (story-dated rows, §4.11) |
| `voice-guide.md`             | world  | Cast-wide dialect-rendering conventions                                                            | merger                         | character-designer     |
| `quotations.md`              | world  | Key verbatim lines with citation-grade provenance and an importance rank                           | merger                         | —                      |
| `theories.md`                | world  | Theories package: cited, falsifiable interpretations with numbered claims (§10.13)                 | theorist                       | —                      |
| `characters/_roster.md`      | union  | Cast roster and name registry: slugs, aliases, reveal-aliases, versions                            | character-designer (seed, F0b), then merger | character-designer |
| `characters/<slug>.md` (`origin: canon`) | world | One character sheet, or an extension sheet (§2.7), with an append-only state history | merger                         | —                      |

### Story layer

| File (under `bible/`)                       | Holds                                                                                | Writer             |
| ------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------ |
| `premise.md`                                | Logline, central dramatic question, promised experience                              | architect          |
| `outline.md`                                | Acts, chapters, scene beats, and the setup/payoff ledger                             | architect          |
| `style.md`                                  | The voice contract and the text-and-speech formatting table                          | line-editor        |
| `divergences.md`                            | Established worlds: the divergence ledger and its consequences (§6.4)                | worldbuilder (curator mode) |
| `sync-points.md`                            | Established worlds: the cutoff for each chapter (§6.7)                               | architect          |
| `timeline.md`                               | Story-time events, in manuscript order                                               | chronicler         |
| `game-state.md`                             | LitRPG: the protagonist's live game state (§9.2)                                     | chronicler         |
| `timelines.md`                              | Frames: travelers' personal timelines (§9.1)                                         | chronicler         |
| `branches.md`                               | Frames: world-line registry and paradox ledger (§9.1)                                | chronicler         |
| `characters/<slug>.md` (`origin: original`) | One sheet per original character                                                     | character-designer; chronicler (story-dated rows, §4.11) |

### Project files outside the bible

| Path                           | Layer      | Writer                                                       |
| ------------------------------ | ---------- | ------------------------------------------------------------ |
| `project.yaml`                 | config     | human (the author), including the adherence settings (§6.3)  |
| `showrunner-log.md`            | control    | showrunner                                                   |
| `manuscript/chapter-<NN>.md`   | manuscript | drafter; line-editor; dialogue (explicit rewrite step only); `release` skill (front matter only, serials) |
| `revisions.md`                 | control    | chronicler (early-access chapters; released installments of serials with revisable releases) |
| `reviews/<reviewer>.md`        | review     | the named reviewer (§12)                                     |
| `derived/bible/…`              | cache      | `compose` skill (§7.6)                                       |
| `derived/as-of-…`              | cache      | `temporal-snapshot` skill (§7.6)                             |
| `references/…`                 | input      | human; `references/feedback/…` holds human readers' notes (§10.25) |
| `runs/…`                       | control    | orchestrator                                                 |

### Universe and extraction files

`<pkg>` is the package's path under `worlds/`, for example `harry-potter/fanon`.

| Path                                            | Layer  | Writer    |
| ----------------------------------------------- | ------ | --------- |
| `universes/<u>/universe.yaml`                   | config | human     |
| `universes/<u>/bridge.md`                       | world  | bridge-builder (human-approved) |
| `universes/<u>/brief.md`                        | input  | human     |
| `extraction/<pkg>/texts/…`                      | input  | human     |
| `extraction/<pkg>/extractions/<work>/ch<NN>.md` | record | extractor |

## 3.4 Genre-specific files

Worlds differ in which files they use. Harry Potter has `magic/spells.md`,
`magic/potions.md`, and `magic/creatures.md`. Star Trek has `technology.md` (warp drive,
transporters, replicators) and `species.md` (Vulcans, Klingons, the Borg). Neither has
the other's.

Where a world has both peoples and animals, it SHOULD keep them apart by **sapience**.
`species.md` holds sapient peoples: beings with their own society, culture, or language,
which other files (`society.md`, `languages.md`, `relationships.md`) can refer to.
Non-sapient fauna goes in a creatures catalog (`magic/creatures.md`, or `creatures.md` in
a world without magic), which uses the catalog format (§10.11). Harry Potter draws the
same line in its own canon, between "beings" and "beasts". House-elves, giants, and
merpeople go in `species.md`; hippogriffs and nifflers go in the creatures catalog. A
world whose canon blurs the line records its choice in `index.md`, under the file's
purpose.

A package or project MAY add world-layer files not listed above. Every such file MUST be
registered in `index.md` with its layer and purpose, and SHOULD use the structured
formats of §10 so that hosts can parse it. Agents discover files through `index.md`
(read it first, then retrieve only what the step needs).
