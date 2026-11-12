# 3. Layers and the write boundary

This chapter is the single authority on which layer each file belongs to and who may
write it. Agent specifications (§12) and workflows (§13) MUST agree with it.

## 3.1 The write boundary

**W1. A world package is read-only to every project.** This holds whether the world is
`open-for-extraction` or `locked`. In project context the host MUST refuse any write
that resolves into `worlds/` or `universes/`.

**W2. Only the extraction pipeline writes a world package.** The pipeline consists of
the steps of the extraction workflow (§13.6), run in world context: the worldbuilder
(the ruler), the character-designer (seeding the roster), the merger (every other
state-bearing file), the theorist (`theories.md`), and the `world-index` skill
(`index.md`). Humans write `world-config.yaml` and `sources.md`. Every change bumps
the package version (§2.8).

**W2a. Only the crossover workflow writes a universe's bridge.** The bridge-builder
drafts `bridge.md` in universe context (§13.7), and a human approves it at the gate.
Every change bumps the universe's version (§8.1).

**W3. A project changes canon only through its divergence ledger.** If a story needs
canon to be different, it does **not** edit the world: it logs a divergence in
`bible/divergences.md` (§6). The shared world stays pristine; the fork lives with the
story that made it.

**W4. A self-contained project owns its world layer.** With no world referenced, the
project's builder agents (worldbuilder, character-designer, architect) write its
world-layer files directly. Promotion (§2.9) turns them into a read-only package.

**W5. Reviews and caches are never canon.** `reviews/` is advisory and `derived/` is
rebuildable. No agent may treat either as a source of facts that overrides the bible.

**W6. One writer per file per step.** At most one step writes a given file at a time
(§11.5).

> **IWE rule:** when a project references a world or universe, present world-layer
> files as read-only, and route any "change canon" action to the project's divergence
> ledger.

## 3.2 Layers

| Layer          | Meaning                                                                         |
| -------------- | ------------------------------------------------------------------------------- |
| **world**      | Describes the world; reusable by every story set in it.                         |
| **story**      | Specific to one story.                                                          |
| **union**      | Exists on both sides and is read as a union (§2.7).                             |
| **config**     | YAML manifests.                                                                 |
| **manuscript** | The prose.                                                                      |
| **review**     | Advisory diagnostics.                                                           |
| **cache**      | Derived from other files and rebuildable at any time.                           |
| **control**    | Orchestration state (`showrunner-log.md`, run records).                         |
| **input**      | Material supplied by a human for agents to read (`texts/`, `references/`).      |

## 3.3 File catalog

The **Writer** columns name the only agent or actor that may write the file.
"Extracted world" means a world package built by the extraction pipeline.
"Self-contained" means a project with no world reference (W4). A dash means the file is
not used in that setting.

### World layer

| File (under `bible/`)        | Layer  | Holds                                                                                              | Writer: extracted world        | Writer: self-contained |
| ---------------------------- | ------ | -------------------------------------------------------------------------------------------------- | ------------------------------ | ---------------------- |
| `world-config.yaml`          | config | Identity, version, status, canon basis, profiles (§10.2)                                           | human                          | human                  |
| `index.md`                   | union  | Endpoint registry: which files exist, what each holds, each file's layer (§10.3)                   | `world-index` skill            | `world-index` skill    |
| `canon-timeline.md`          | world  | The ruler (§4)                                                                                     | worldbuilder (step F0)         | worldbuilder (optional, §4.7) |
| `sources.md`                 | world  | Source registry (§5)                                                                               | human                          | human                  |
| `glossary.md`                | union  | Canonical names and terms; the anti-drift file                                                     | merger                         | worldbuilder           |
| `world.md`                   | world  | Setting, era, rules and systems (each with cost and limit), as a state history                     | merger                         | worldbuilder           |
| `places.md`                  | world  | Atlas: places, connectivity, access control, state over time                                       | merger                         | worldbuilder           |
| `society.md`                 | world  | Law, institutions, politics, economy, customs                                                      | merger                         | worldbuilder           |
| `culture.md`                 | world  | Food, holidays, fashion, media, sayings                                                            | merger                         | worldbuilder           |
| `languages.md`               | world  | Languages: speakers, on-page rendering, translation (languages module, §9.3)                       | merger                         | worldbuilder           |
| `lang/<language>.md`         | world  | Dictionary for one constructed language                                                            | merger                         | worldbuilder           |
| `magic/<catalog>.md`         | world  | Catalogs (spells, potions, creatures, artifacts, games): theory vs. practice, definition level     | merger                         | worldbuilder           |
| `game-system.md`             | world  | LitRPG: the System's rules (§9.2)                                                                  | merger                         | worldbuilder           |
| `plot-architecture.md`       | world  | Canon setups and payoffs, prophecies, foreshadowing, running mysteries                             | merger                         | — (the outline's ledger serves) |
| `knowledge.md`               | world  | Who knows what, dated: secrets and reveals                                                         | merger                         | architect              |
| `relationships.md`           | world  | Pairwise relationship state histories                                                              | merger                         | character-designer     |
| `voice-guide.md`             | world  | Cast-wide dialect-rendering conventions                                                            | merger                         | character-designer     |
| `quotations.md`              | world  | Key verbatim lines with citation-grade provenance and an importance rank                           | merger                         | —                      |
| `theories.md`                | world  | Cited, falsifiable interpretations (tier `theory`)                                                 | theorist                       | —                      |
| `characters/_roster.md`      | union  | Cast roster and name registry: slugs, aliases, reveal-aliases, versions                            | character-designer (seed, F0b), then merger | character-designer |
| `characters/<slug>.md` (`origin: canon`) | world | One character sheet with an append-only state history                                | merger                         | —                      |

### Story layer

| File (under `bible/`)                       | Holds                                                                                | Writer             |
| ------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------ |
| `premise.md`                                | Logline, central dramatic question, promised experience                              | architect          |
| `outline.md`                                | Acts, chapters, scene beats, and the setup/payoff ledger                             | architect          |
| `style.md`                                  | The voice contract and the text-and-speech formatting table                          | line-editor        |
| `canon.md`                                  | Established worlds: the adherence contract (§6.3)                                    | worldbuilder (curator mode) |
| `divergences.md`                            | Established worlds: the divergence ledger and its consequences (§6.4)                | worldbuilder (curator mode) |
| `canon-track.md`                            | Established worlds: the cutoff for each chapter, and any project order (§6.7–6.8)   | architect          |
| `timeline.md`                               | Story-time events, in manuscript order                                               | chronicler         |
| `game-state.md`                             | LitRPG: the protagonist's live game state (§9.2)                                     | chronicler         |
| `timelines.md`                              | Frames: travelers' personal timelines (§9.1)                                         | chronicler         |
| `branches.md`                               | Frames: world-line registry and paradox ledger (§9.1)                                | chronicler         |
| `characters/<slug>.md` (`origin: original`) | One sheet per original character                                                     | character-designer |

### Project files outside the bible

| Path                           | Layer      | Writer                                                       |
| ------------------------------ | ---------- | ------------------------------------------------------------ |
| `project.yaml`                 | config     | human                                                        |
| `showrunner-log.md`            | control    | showrunner                                                   |
| `manuscript/chapter-<NN>.md`   | manuscript | drafter; line-editor; dialogue (explicit rewrite step only); `release` skill (front matter only, serials) |
| `revisions.md`                 | control    | chronicler (serials with revisable releases)                 |
| `reviews/<reviewer>.md`        | review     | the named reviewer (§12)                                     |
| `derived/…`                    | cache      | `temporal-snapshot` skill                                    |
| `references/…`                 | input      | human                                                        |
| `runs/…`                       | control    | orchestrator                                                 |

### Universe and extraction files

| Path                                         | Layer  | Writer    |
| -------------------------------------------- | ------ | --------- |
| `universes/<u>/universe.yaml`                | config | human     |
| `universes/<u>/bridge.md`                    | world  | bridge-builder (human-approved) |
| `universes/<u>/brief.md`                     | input  | human     |
| `extraction/<w>/texts/…`                     | input  | human     |
| `extraction/<w>/extractions/<work>/ch<NN>.md` | record | extractor |

## 3.4 Genre-specific files

Worlds differ in which files they use. Harry Potter has `magic/spells.md`,
`magic/potions.md`, and `magic/creatures.md`. Star Trek has `technology.md` (warp drive,
transporters, replicators) and `species.md` (Vulcans, Klingons, the Borg). Neither has
the other's. A world MAY
add world-layer files not listed above. Every such file MUST be registered in
`index.md` with its layer and purpose, and SHOULD use the structured formats of §10 so
that hosts can parse it. Agents discover files through `index.md` (read it first, then
retrieve only what the step needs).
