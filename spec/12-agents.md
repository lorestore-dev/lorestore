# 12. The agents

The agent system is a **writers' room built from narrow, composable roles**. Agents
never call each other: they communicate only through files (§11.9).

A useful mental model: **builders write the bible, the drafter writes the manuscript,
reviewers write `reviews/`**, and the chronicler records what the manuscript has
established.

## 12.1 Roster

| Agent                | Group           | Mandate                                                                 | Writes (one per step)                                                      |
| -------------------- | --------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `showrunner`         | Orchestration   | Routes decisions, schedules revisions, inserts on-demand steps          | `showrunner-log.md`                                                        |
| `extractor`          | World learning  | Turns one source unit into dated, cited facts                           | `extractions/<work>/ch<NN>.md`                                             |
| `merger`             | World learning  | Assembles append-only state histories from extraction records           | one world-layer file                                                       |
| `theorist`           | World learning  | Synthesizes cited, falsifiable theories, as numbered claims             | `bible/theories.md` (a theories package)                                   |
| `architect`          | Foundation      | Premise, structure, beat-level outline, the sync points                 | see §12.6                                                                  |
| `worldbuilder`       | Foundation      | Setting and systems (inventor), canon adherence (curator), the ruler    | see §12.7                                                                  |
| `character-designer` | Foundation      | Cast, voices, wants, arcs, relationships                                | see §12.8                                                                  |
| `researcher`         | Foundation      | Real-world grounding and internal plausibility                          | `reviews/research.md`                                                      |
| `drafter`            | Drafting        | The only agent that generates prose from scratch                        | `manuscript/chapter-<NN>.md`                                               |
| `chronicler`         | Drafting        | Records what each chapter establishes: story-layer ledgers, and the state of the project's own entities | `bible/timeline.md`, `bible/game-state.md`, `bible/timelines.md`, `bible/branches.md`, `revisions.md`, or a project entity's file (§4.11) |
| `continuity-editor`  | Review          | Internal consistency: manuscript against bible and against itself       | `reviews/continuity.md`                                                    |
| `canon-keeper`       | Review          | External fidelity and leaks (established worlds only)                   | `reviews/canon.md`                                                         |
| `line-editor`        | Polish          | Sentence-level polish; owns the style guide                             | `manuscript/chapter-<NN>.md` or `bible/style.md`                           |
| `dialogue`           | Polish          | Distinct voices; drafts or repairs conversation                         | `reviews/dialogue.md`, or the chapter on an explicit rewrite step          |
| `pacing-analyst`     | Review          | The tension curve                                                       | `reviews/pacing.md`                                                        |
| `critic`             | Review          | Structural developmental feedback                                       | `reviews/critique.md`                                                      |
| `beta-reader`        | Review          | A target reader's felt experience                                       | `reviews/beta-reader.md`                                                   |
| `bridge-builder`     | Crossover       | Drafts the bridge that reconciles a universe's worlds                   | `bridge.md`                                                                |
| `prompter`           | Illustration    | Image prompts for characters, family portraits and trees, maps, and locations, as known at a cutoff | `prompts/<id>.md`                                         |

Each specification below gives the agent's **Reads** as a retrieval spec (§11.6). "The
chapter's cast" means the entities the chapter's outline beat names, plus anyone the
drafted text introduces.

## 12.2 `showrunner`: the dynamic router

Walking a fixed list of steps is mechanical. The showrunner handles the *branches*:
deciding what happens next when the happy path forks.

- **Context:** project.
- **Reads:** `project.yaml`; the active workflow files; `showrunner-log.md`; the output
  of the step just finished; the `## Priorities` of each review; the `## Findings` and
  `## Consequences honored` of `reviews/canon.md`; TODO markers found by searching
  `manuscript/`.
- **Writes:** `showrunner-log.md`.
- **Duties:**
  - After each draft step, route every `TODO: needs bible` marker to the right builder
    (worldbuilder for settings and rules, character-designer for people, architect for
    plot), then re-run the draft. Resolve every `needs bible` marker before the
    continuity-editor runs.
  - Surface every `TODO: hidden canon` and `TODO: seam conflict` marker to the author
    (§6.12, §6.14). Each one blocks the chapter's
    step-14 gate like a pending decide item (§11.8). Once the author decides, hand the
    decision to the curator to record, then re-run the draft for the marked passage.
  - Read review priorities and schedule revision steps before advancing.
  - Log the consequences the canon-keeper reports honored, by divergence id and chapter,
    so the curator can mark them absorbed (E5).
  - Insert on-demand steps the chain lacks (a dialogue pass, a research check, an image
    prompt the author asks for), and decide which chapters a changed outline
    invalidates.
  - **Decide items** (§6.9): under `gates: none`, make the call and log the reasoning;
    otherwise surface it to the human. **Order inversions**, **divergence conflicts**,
    **hidden canon**, **theory conflicts**, and **seam conflicts**
    are never the showrunner's call. Always surface them to the author, with the
    canon-keeper's options or the drafter's marker, and wait.
  - **Early access** (§13.9): never send a chapter to early access, which is always the
    author's call. When human feedback arrives (§10.25), schedule a beta-reader step so
    it is folded into the priorities, and schedule revisions of early-access chapters
    like any other, telling the chronicler to log each one.
  - **Serials** (§13.3): revise buffered (unreleased) chapters as in `novel`; never
    release, schedule, or withdraw an installment, which is always the author's call
    (§13.12); report the buffer's
    depth. Never schedule a revision of a released installment when releases are locked.
    Route the fix forward to an upcoming installment or the next arc. When a consequence
    invalidates a released installment, absorb it forward or surface it to the author.
    Only the author may accept an inconsistency. Route an *intended* divergence to the
    worldbuilder (curator) to log, and an *accepted* paradox to the chronicler to
    record.
- **Guardrails:** never writes `bible/`, `manuscript/`, or `reviews/`; never skips a
  gate the policy requires; one agent per step.

## 12.3 `extractor`: source to dated, cited facts

- **Context:** package.
- **Reads:** one source unit, `texts/<work>/<unit>`; `bible/canon-timeline.md`;
  `bible/characters/_roster.md`; `bible/sources.md`; `bible/glossary.md` (for spelling).
  It does **not** read other units or the rest of the world, which keeps parallel
  extraction independent.
- **Writes:** `extractions/<work>/ch<NN>.md` (§10.6).
- **Duties:**
  - Read for **state**, not just events. For every character and world element the unit
    touches, record what is true (appearance, possessions, relationships, knowledge,
    office, status) and whether it is new, a change, or a confirmation.
  - Date every fact at the finest point the source supports (chapter or scene; episode,
    scene, and timecode for video), observing the whole-node rule (§4.2). Break and
    number scenes as §4.2 defines them.
  - Record `True from` whenever the unit reveals backstory: when a fact became true
    before the point that reveals it (§4.4).
  - In a world with a calendar (§4.13), record in-world dates as precisely as the source
    gives them, and no more: the unit's own date, an `In-world` date for backstory,
    `born` and `died`, and past events as entities of `history.md`. Convert dates
    written in the work's notation to the calendar's form, keeping the original in the
    citation. Flag a fact that contradicts a date (a flashback, a prophecy) under
    `## Needs a human`.
  - Name every character through the roster. File facts under a **reveal alias's**
    surface slug until the reveal (§10.9). Give canon-distinct **versions** their own
    slug. List unknown names under `## New names`, with a proposed slug that the facts
    then use.
  - Record notable lines under `## Quotations`.
  - Record a passage that a later printing or cut corrected under the package's
    `erratum` source for that edition, beside the corrected fact (§5.2).
  - Put anything ambiguous under `## Needs a human` rather than guessing canon into
    existence.
- **Guardrails:** never copy source prose: own words plus a citation, always (quotations
  are the only exception). Cite only sources in the package's own registry, so each
  fact lands in the package it belongs to; credit fan works and their authors there.
  Never write the bible.

## 12.4 `merger`: facts to ordered history

- **Context:** package.
- **Reads:** the rows of every extraction record whose `Target` is its target file;
  `bible/canon-timeline.md`; the existing target file; `bible/characters/_roster.md`;
  `bible/sources.md`.
- **Writes:** one world-layer file per step: its target.
- **Duties:**
  - **Sort by ruler point** (§4.2), never by arrival order.
  - **Keep confirmations:** the earliest point is the establishing row, and a later
    confirmation of the same value is kept as its own row. These rows change nothing
    in the ruler's order, but they keep a fact visible to a project that rearranges canon
    (§6.8). Exact duplicates (same point, value, and source) are merged, with their
    citations combined (`; `-separated).
  - **Flag conflicts:** rows with the same entity, attribute, tier, and point but
    different values, from one source or two, are left out and listed under
    `## Unresolved conflicts`, for a human to settle as §4.4 says: the corrected text
    with the error as an erratum, the fan consensus, or a separate package.
  - **Validate:** points against the ruler, sources against the registry, slugs against
    the roster, and that `True from` is not later than `As of`. Carry `True from` through
    unchanged. Check dates against the calendar and for chronology contradictions
    (§4.13). Invalid rows go to `## Unresolved conflicts`. A human settles a
    contradiction by correcting the row or accepting it, with the source's citation;
    the merger then writes the acceptance in the target's `## Accepted` table.
  - **Roster target:** accept `New names` that are unambiguous; record a proposed slug
    that duplicates an existing character as an alias of the existing slug, so that the
    other mergers map it.
  - **Lower layers** (packages other than a base): a fact about an entity that a
    package the target relies on defines goes in an **extension sheet** (§10.5), never
    under a new slug; a new slug that collides with a lower layer's key is an
    unresolved conflict (§2.7).
- **Guardrails:** adds no facts of its own; append-only except for corrections
  (§4.6) a human has approved; writes only its target. The sole writer for its target,
  so parallel merge instances never collide.

**Example cases:** [17](../examples/README.md#case-17).

## 12.5 `theorist`: facts to cited interpretations

- **Context:** package (a `theories` package, §2.3).
- **Reads:** `bible/theories.md`; the slices of the packages it relies on that each
  theory draws on (state histories, `quotations.md`, `knowledge.md`,
  `plot-architecture.md`); `bible/canon-timeline.md`; `bible/sources.md`.
- **Writes:** `bible/theories.md` (§10.13).
- **Duties:** find patterns that explain several facts at once; break each theory into
  **numbered claims**, each one checkable on its own; **cite or cut**; rate kind and
  confidence; state the falsifier; set status, and retire theories that higher-tier
  canon contradicts. Record a theory gathered from fans under its registry source, with
  its origin as far as it can be traced, and say so when it cannot.
- **Guardrails:** never present a theory as canon. Theories are tier `theory`: they
  never resolve into state (§5.4), and reach a story only when its author adopts them
  (§6.13).

## 12.6 `architect`: structure

Turns a one-line seed into a structural blueprint: the premise, the central dramatic
question, and a beat-level outline in which every scene earns its place. It owns story
**structure** (cause and effect, escalation, setup and payoff), including where the
story sits in canon, but not prose.

- **Writes (one per step):** `bible/premise.md`; `bible/outline.md`;
  `bible/sync-points.md` (established worlds, §6.7); `bible/knowledge.md` (in a project
  with a stack, only the project's own secrets and what original characters know);
  `bible/mysteries.md` (mysteries, §9.5: the project's own mysteries, and clues it adds
  to canon ones).
- **Reads:** `project.yaml` (seed, parameters, `setting`); `bible/premise.md` when writing
  the outline; the roster and `world.md` summary sections; for established worlds,
  `bible/divergences.md`, the ruler, and `plot-architecture.md` rows
  for the stretch of canon the story covers.
- **Duties:**
  - Interrogate the seed into a logline; find the **central dramatic question**.
  - Break the story into acts, chapters, and scenes. Each scene is **goal, conflict,
    turn**; a scene with no turn is description, so cut or merge it.
  - **Viewpoints** (§7.7): where the project or a chapter records them, give each
    chapter or scene its viewpoint character in the outline's table (§10.23), and its
    `Told from` where the narrator looks back. Choose the viewpoint that serves the
    scene's turn, and set a chapter's override where its shape changes.
  - Track setups and payoffs in the outline's ledger so nothing is planted and
    forgotten.
  - **Mysteries** (§9.5): plan each mystery's clues and red herrings with the outline,
    so that every needed clue is planted before the reveal, and record them in
    `mysteries.md`. Each mystery's answer is a secret in `knowledge.md`.
  - **Sync points:** map chapters to the cutoffs they follow, never past
    `setting.divergence_point` in a branch (§6.6), and in the project order
    (`setting.order`) if there is one. The order is the author's (§6.8): when the story
    needs canon rearranged, propose an order for the author to set, and hand the
    reordering to the curator to log. When the author reorders to resolve an inversion,
    revise the sync points to match.
- **Guardrails:** no prose or dialogue; don't over-specify the world; respect the fixed
  parameters (POV, tense, length); prefer fewer, load-bearing scenes. Sync points say
  where the story is in canon, never what it changes. Changes belong in the
  ledger.

## 12.7 `worldbuilder`: setting, divergences, and the ruler

Three modes. The workflow step selects one.

| Mode         | When                                | Writes                                                                                                                                                                              |
| ------------ | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **inventor** | Self-contained projects; in a project with a stack, its own additions only (§2.7) | One of `bible/world.md`, `history.md`, `places.md`, `routes.md`, `society.md`, `culture.md`, `languages.md`, `lang/<language>.md`, `magic/<catalog>.md`, `game-system.md`, `time-travel.md`, `titles.md`, `glossary.md`, `canon-timeline.md` |
| **curator**  | `setting.type: established`         | `bible/divergences.md`                                                                                                                                                              |
| **ruler**    | Extraction, step F0 (package context) | `bible/canon-timeline.md`                                                                                                                                                         |

- **Reads:** `project.yaml` (`setting`); `bible/premise.md`; `bible/outline.md`; the
  index; and per mode: the existing world-layer file being written (inventor); the world
  layer by slice and `references/` (curator); a listing of `texts/` (ruler).
- **Duties:**
  - Give every system a **cost and a limit**. An unbounded system removes tension and
    breaks later plotting.
  - Build factions as engines of conflict; give recurring locations a sensory signature
    and a dramatic function.
  - **Ruler:** write the `## Dates` table from what the source states, and from the
    extraction records' `date` fields when F0 re-runs (§13.6). **Inventor:** in a world
    with a calendar, date its past in `history.md`, and date the eras of its ruler, if
    it has one (§4.13). With the travel module, give every route between places the
    story uses a duration for each mode that can make it (§9.4); with the lineage
    module, record the succession of titles in `titles.md` (§9.6).
  - **Curator:** do not invent. Log divergences and their consequences in
    `divergences.md` (§6.4) when planned during foundation, or when the showrunner or a
    human accepts an emergent one. Mark consequences absorbed when the chronicler or
    continuity-editor reports them honored. Log every change and addition to a canon
    entity (§6.2), and the reordering of canon. For each order inversion or divergence
    conflict, log **the author's chosen resolution** (nothing, if the author keeps the
    canon event), with the fallout as open consequences (§6.6, §6.8). Record every
    hidden-canon decision in the Hidden canon table, and for **reveal early** log the
    divergence that reveals it, and for **other** the divergence that carries it out, if
    it changes canon state (§6.12). Record the author's keep, adapt, or discard for
    each theory conflict in the Theory conflicts table, and log the adoption as a
    divergence whose `Basis` names the kept and adapted claims (§6.13). Record the
    author's choice for each seam conflict in the Seam conflicts table, and for **keep
    earlier** or **other** log the divergence that sets the value (§6.14). Never pick a
    resolution yourself.
- **Guardrails:** don't invent lore the story never uses; don't set rules the plot
  needs to break; never write a package from project context (§3.1).

## 12.8 `character-designer`: the cast

- **Writes (one per step):** `bible/characters/<slug>.md`; `bible/characters/_roster.md`;
  `bible/relationships.md`; and, in self-contained projects, `bible/voice-guide.md`.
  In package context (extraction step F0b): `bible/characters/_roster.md` (the seed).
- **Reads:** `bible/premise.md`; `bible/outline.md`; `bible/world.md` (summary sections);
  the union roster; the sheets of the characters the new one relates to. In package
  context, a listing of `texts/` and any cast list a human provides.
- **Duties:** separate **want** from **need** (the gap is the arc); name the **lie** the
  character believes; build the voice concretely (rhythm, diction, tics, and one sample
  line); wire relationships as tensions, not labels.
- **Guardrails:** no backstory tourism; antagonists get wants and reasons; voices must
  be mutually distinguishable. In a project with a stack, writes only original
  characters (`origin: original`), project roster rows, and relationships between
  original characters. A canon character's relationship to an original one is a
  divergence for the curator (§6.2).

## 12.9 `researcher`: grounding

- **Reads:** the claims under review: `bible/world.md` and the relevant catalogs;
  `bible/timeline.md`; `bible/glossary.md`; `bible/premise.md`; and, when checking prose,
  the chapters named by the step.
- **Writes:** `reviews/research.md`.
- **Duties:** extract the load-bearing factual and logical claims; check real-world
  claims for accuracy and anachronism, calibrated to the genre's promise of rigor;
  audit invented systems for consistency with their own costs and limits; rank findings
  by immersion impact, each with a fix.
- **Guardrails:** advise, don't rewrite; distinguish "wrong" from "couldn't verify";
  flag, don't fabricate.

## 12.10 `drafter`: the only prose generator

- **Reads:**
  - this chapter's rows from `bible/outline.md`: its beats, and its viewpoints (§7.7);
  - for each viewpoint character, their snapshot at the scene's knowledge point (§7.7),
    with their `knowledge.md` rows;
  - `bible/style.md`;
  - the **snapshot** (§7) of each entity in the chapter's cast, and of each relationship
    between them, at this chapter's cutoff (from the sync points) and position (from
    `derived/`, or computed);
  - the roster's reveal aliases for the cast (§10.9), to decide what the POV character
    can know about who is who;
  - the divergences and open consequences that touch the cast (established worlds);
  - the union `bible/glossary.md`;
  - recent events from `bible/timeline.md`, and the end of the previous chapter;
  - per module: the latest `bible/game-state.md` rows and the relevant
    `game-system.md` entries (LitRPG); the travelers' rows in `timelines.md` and the
    branch in `branches.md` (frames); entries in `languages.md` and `lang/` for languages
    spoken in the chapter (languages); the routes between the chapter's places
    (travel); the mysteries the chapter touches, with their clues (mysteries);
  - an adopted theory only through the divergences whose `Basis` cites it (§6.13);
    never `bible/theories.md` itself;
  - in a revision, the chapter as it stands and the notes for the revision (§11.8).
- **Writes:** `manuscript/chapter-<NN>.md`, with `status: drafted`.
- **Duties:**
  - Render each scene as **goal, rising conflict, turn**; enter late, leave early.
  - Keep POV and tense discipline; plant and pay off per the outline's ledger; use
    glossary spellings.
  - **Viewpoints** (§7.7): narrate each scene within its viewpoint character's knowledge
    at its knowledge point, and never past the reader-facing rules, however much a
    narrator who is told from later knows. Record the chapter's viewpoints, as drafted,
    in its front matter and scene markers (§10.18). A viewpoint that differs from the
    outline is the author's to keep or undo (§7.7).
  - **Respect the snapshot:** use only canon true at the chapter's cutoff, from the
    stack's layers, as amended by the ledgers.
  - **Don't add to canon entities silently.** A new physical detail, possession, or
    relationship for a canon character is a divergence (§6.2). Flag it with a
    `TODO: needs bible` marker so the curator can log it.
  - **Hidden truths** (§7.2) are not usable. If the beat touches one that no Hidden canon
    table of the ledgers has decided (§6.4), write as if it were unknown and mark it with
    `TODO: hidden canon` (§6.12). If it has been decided, follow the decision.
  - **Errata** (§5.2) are not canon. Where the corrected text and an erratum differ,
    write to the snapshot, which gives the corrected value.
  - **Seam conflicts** (§7.2) are not usable either. If the beat needs an earlier book's
    item that the snapshot returns as a seam conflict, draft around it and mark it with
    `TODO: seam conflict` (§6.14).
  - **Frames:** mark each scene's world point and travelers (§10.18); write each
    character to their own frame.
  - **Mysteries** (§9.5): plant the clues the outline gives this chapter. Never let the
    narration answer a mystery before its `Revealed at`, even through a viewpoint
    character who knows the answer.
- **Guardrails:** don't invent canon: mark gaps with `TODO: needs bible`. Don't drift POV
  or tense; don't summarize the exciting parts; write the beat given, raising
  structural concerns to the showrunner; never reproduce source passages.

## 12.11 `chronicler`: what the story has established

Records the story-layer consequences of each chapter so that later chapters, the
snapshot, and the reviewers can rely on them.

- **Reads:** the chapter just drafted (or revised); the target ledger or file; the
  showrunner's logged decisions (for paradoxes).
- **Writes (one per step):** `bible/timeline.md`; `bible/game-state.md` (LitRPG);
  `bible/timelines.md` or `bible/branches.md` (frames); the `Planted at` cells of the
  project's own clues in `bible/mysteries.md` (mysteries); `revisions.md` (early-access
  chapters, and serials with revisable releases, §10.22); or the story-dated rows of
  an original character's sheet, `bible/relationships.md`, or `bible/knowledge.md`
  (§4.11).
- **Duties:** append the chapter's story-time events; append game-state changes with
  their causes; append traveler legs, with the mechanism each used, and personal
  cutoffs; register new branches and update branch statuses as the mechanism's model
  dictates (§9.1); append ripples; record paradox decisions with their rationale;
  with the travel module, fill each event's `Place` (§9.4); with the mysteries module,
  move a clue's `Planted at` when a revision moves the clue to another chapter (§9.5); log
  each revision of a released or early-access chapter, with its audience, date, and a
  reader note (§10.22). Append a story-dated row, with the chapter's id as its
  `From chapter`, for each change the chapter makes to the state of an original
  character, of a relationship between two original characters, or of what an
  original character knows (§4.11).
- **Guardrails:** records only what the manuscript states; invents nothing; when
  re-run for a revised chapter, replaces that chapter's rows rather than appending
  duplicates; never writes canon entities' rows or the divergence ledger (a change to
  a canon entity is a divergence for the curator, §6.2); in a world-layer file, writes
  only story-dated rows.

## 12.12 `continuity-editor`: internal consistency

- **Reads:** the chapter under review; snapshots for its cast; `bible/timeline.md`; the
  union glossary; earlier chapters only where a check needs them (found by search);
  relevant `relationships.md` and `languages.md` rows; `game-state.md` and
  `game-system.md` (LitRPG); `routes.md` (travel); `mysteries.md` (mysteries); the
  cast's lineage rows and `titles.md` (lineage).
- **Writes:** `reviews/continuity.md`.
- **Duties:** flag **manuscript vs. bible**, **manuscript vs. manuscript**, and
  **drift** (spelling or terminology); for LitRPG, check the game-state invariants
  (§9.2); rank by severity (a reader-breaking contradiction outranks a minor slip, which
  outranks cosmetic drift). Where viewpoints are recorded, flag each **viewpoint
  leak** (§7.7): narration that states what its viewpoint character does not know at the
  scene's knowledge point. In a world with a calendar, raise the date warnings of
  §4.13: events outside a participant's lifetime, ages that the dates rule out, and
  story events dated before the cutoff's date. Raise the module warnings too: journeys
  faster than the routes allow (travel, §9.4), unfair mysteries (§9.5), and parents,
  births, and title holders that the dates rule out (lineage, §9.6). Each is the
  author's to decide, because a flashback or an unreliable narrator can be deliberate.
- **Guardrails:** internal consistency only (fidelity to the source is the
  canon-keeper's job); report, never rewrite or edit the bible; distinguish a genuine
  contradiction from a deliberate mystery or an unreliable narrator.

## 12.13 `canon-keeper`: external fidelity

Runs only when `setting.type: established`, except that the frames overlay also runs it
for its frame, mechanism, and paradox checks alone (§13.5). It diagnoses; it never
rewrites.

- **Reads:** the chapter under review; `bible/divergences.md`;
  `bible/sync-points.md`; snapshots for the cast; `bible/canon-timeline.md`;
  `bible/sources.md`; the relevant `quotations.md` rows; `references/` as background
  only (§6.1); `project.yaml` (layers, resolution, and the adherence settings, §6.3);
  `bible/bridge.md` (universes); the claims of any theory a divergence's `Basis` cites;
  `timelines.md`, `branches.md`, and the `time-travel.md` entries the chapter's legs use
  (frames).
- **Writes:** `reviews/canon.md`, with a `## Findings` table (§10.19).
- **Duties:** classify every problem using the classes in §6.9, applying the fidelity
  setting (§6.10). Check rules, characterization, geography, and the canon timeline
  against the **composite**: source canon read at the sync points, overridden by the
  ledger. Treat any unlogged addition to a canon entity as an emergent divergence.
  **Order audit:** when the project order (`setting.order`) changes, list every order
  inversion (§6.8) as an entry with the options (remove, substitute, supply, reorder)
  and the likely fallout of each, in story terms (§10.19). Address every inversion
  candidate the host lists, as an inversion or with a note saying why it is not one.
  **Divergence audit** (retellings, §6.6): whenever a divergence is logged, read ahead
  through the sync points and list every later canon event a divergence in force makes
  impossible or changes, including those of project layers, with the options (keep,
  adapt, remove, substitute) and their fallout. Address every reach candidate the host
  lists, as a conflict or with a note saying why it is not one. Present options; never
  recommend one as the answer. **Branches:** check faithfulness only up to
  `setting.divergence_point`; flag any use of later canon as a temporal leak. **Hidden
  canon** (§6.12): when a chapter or an audit touches a hidden truth the author has not
  decided about, raise it once, with the options (reveal early, keep hidden, other) and
  what each would mean for the story. Flag a chapter that uses a hidden truth without a
  decision as a temporal leak. **Theory audit** (§6.13): when a divergence's `Basis`
  cites a theory, list every piece of evidence in the stack, at any point, that
  contradicts a cited claim, with the options (keep, adapt, discard) and their fallout.
  Mark evidence that is an erratum (§5.2) as such. **Errata:** read the stack's
  erratum rows, and flag prose that relies on an erratum's value, with no divergence
  covering it, as erratum use (§6.9). **Seam audit** (§6.14): in a
  project with project layers, first say whether the first chapter is set before an
  earlier book's cutoff at its pin, so the author can fix a wrong pin. Then list every
  item of the earlier books ahead of a chapter that no Seam conflicts table decides,
  grouped where a pattern would cover them, with the options (carry back, not yet,
  other), and every value seam, with both values and the options (keep earlier, accept,
  other). Flag a chapter that uses an undecided item as a seam conflict. **Mysteries**
  (§9.5): in an order audit or a divergence audit, list each canon mystery whose needed
  clue the change moves to after its reveal, or removes. **Source
  leaks**: flag a fact found only in a same-fandom package the stack does not include
  (§5.3). Join reveal aliases to their true identities from the `Revealed at` point
  (§10.9) when judging what characters could know. Report consequences the chapter
  honors, so the curator can mark them absorbed.
- **Guardrails:** never flag the story for obeying its own logged divergence; never
  silently "correct" an emergent divergence back to canon.

## 12.14 `line-editor`: sentence-level polish

- **Reads:** the chapter; `bible/style.md`; the union glossary.
- **Writes:** `manuscript/chapter-<NN>.md` (status `line-edited`, or `final` on the
  finishing pass), or `bible/style.md` when a step asks it to codify the emerging voice.
- **Duties:** cut filler, hedges, clichés, and repetition; vary rhythm; choose precise
  verbs; enforce POV distance and filtering rules; enforce the style guide's
  text-and-speech formatting (dialogue, thought, marked languages, telepathy, written
  text, reveal-gated markers). In a project with `content_notes`, suggest the
  chapter's notes in `content-notes-suggested` (§13.11): every note on the project's
  list that the chapter calls for, and `new:<id>` for anything a reader would want
  warning of that the list lacks.
- **Guardrails:** never change what happens (flag plot or continuity changes instead);
  don't homogenize voices; preserve intentional style; edit towards the style guide,
  not its own taste. Never set `content-notes`: only the author confirms a chapter's
  notes.

## 12.15 `dialogue`: distinct voices

- **Reads:** the target scene; the voice signature, wants, and secrets of each speaker;
  `bible/voice-guide.md`; the speakers' relationship snapshots; `bible/style.md`.
- **Writes:** `reviews/dialogue.md` by default: an audit with specific rewrites, which
  the drafter or line-editor applies. Only on an explicit rewrite step does it write
  `manuscript/chapter-<NN>.md`, scheduled never concurrently with another writer of that
  chapter.
- **Duties:** give every line a purpose (to get something, hide something, or shift
  power); push feeling into subtext; vary rhythm by character; differentiate any two
  characters who could swap lines unnoticed.
- **Guardrails:** no stereotype or dialect caricature; characters don't explain the plot
  to each other; respect what each speaker knows (§7.3); on a rewrite, touch only
  dialogue and its immediate beats.

## 12.16 `pacing-analyst`: the tension curve

- **Reads:** `bible/outline.md`; `bible/premise.md`; the manuscript, in full and in
  order (§11.6 exception).
- **Writes:** `reviews/pacing.md`.
- **Duties:** rate each scene's tension and momentum; find **sags** and **rushes**;
  check that action alternates with reflection; prescribe concretely (cut, merge,
  expand, move).
- **Guardrails:** don't rewrite; judge against the promised experience; distinguish a
  quiet scene that builds from a dead one.

## 12.17 `critic`: developmental feedback

- **Reads:** `bible/premise.md`; `bible/outline.md`; the manuscript in full; the
  `## Priorities` of existing reviews (to synthesize rather than repeat them).
- **Writes:** `reviews/critique.md`.
- **Duties:** hold the manuscript to what it is reaching for; hunt the load-bearing
  failures first (concrete want, escalating stakes, a theme dramatized rather than
  lectured, a climax that answers the central question at a real cost); rank problems
  by how much they undermine the whole; name genuine strengths.
- **Guardrails:** spine before surface; directions, not rewrites; judge the book it is
  trying to be.

## 12.18 `beta-reader`: the felt experience

- **Reads:** `bible/premise.md` (to adopt the target-reader persona); the manuscript in
  full, in order; any human feedback under `references/feedback/` (§10.25).
- **Writes:** `reviews/beta-reader.md`.
- **Duties:**
  - React moment by moment as the target reader; mark the hook, the sags, the payoffs,
    any confusion, and any loss of trust; give the bottom line (would they finish it,
    recommend it, remember it?).
  - **Flag leftover markers.** List every `TODO` marker still in the prose
    (`TODO: needs bible`, `TODO: hidden canon`, `TODO: seam conflict`, or any
    other) under
    `## Leftover markers` (§10.19), with its chapter and text. Leftover markers always
    go first in the priorities, because no marked chapter is ready for readers.
  - **Fold in human feedback.** Turn each human reader's notes into priorities, each
    marked `(human: <reader>)` (§10.19), ranked with the agent's own. A point that
    several readers, or a reader and the persona, raise ranks higher.
- **Guardrails:** react, don't diagnose, except for leftover markers, which are reported
  as found; stay in persona; be honest about boredom. Never put words in a human
  reader's mouth: a `(human: …)` priority restates what that reader said.

## 12.19 `bridge-builder`: reconciling a universe

Drafts the bridge that lets two or more worlds share one universe (§8). It proposes;
a human approves at the gate.

- **Context:** universe (§2.6).
- **Reads:** `universe.yaml`; each base's `index.md`, `glossary.md`, and roster; the
  world-layer slices behind each concept it maps (`world.md`, `magic/*`, `technology.md`,
  `species.md`); the existing `bridge.md`; the author's crossover brief, if any.
- **Writes:** `bridge.md` (§10.14).
- **Duties:**
  - **Concept mappings:** for each system or institution that both worlds have in some
    form (magic and technology, governments, non-magical humans), propose a relation
    (`≡`, `→`, or `∥`) and the rule that follows from it. Explain each choice in a
    sentence, citing both worlds.
  - **Collisions:** find names that clash across the worlds' glossaries and rosters, and
    propose how each resolves.
  - **Consistency rules:** state the constraints the mappings imply, such as "magic never
    powers starship systems".
  - **Crossover canon:** add only the facts the author's brief asks for, with source
    `bridge`. Never infer them.
  - **Offsets:** check that `universe.yaml`'s offsets give the alignment the brief
    describes, and flag a mismatch.
- **Guardrails:** never edits a package; never contradicts either base's canon
  (a reconciliation explains differences, it does not overwrite them); prefers `∥` when
  a mapping would force one world to change; flags open questions for the human instead
  of settling them.

## 12.20 `prompter`: image prompts

Writes prompts for image generators: pictures of characters, family portraits, family
trees, maps, and locations, each drawn from the bible as a reader knows it at a chosen
point in the story. It runs only when the author asks for a picture. A prompt is
plain descriptive prose, for no particular image model (§1).

- **Context:** project.
- **Reads:** the author's request (the kind, the subjects, the cutoff or chapter, and
  any art direction); `references/art-direction.md`, if the author keeps one; the
  **snapshot** (§7) of each subject at the prompt's cutoff and position; the roster's
  reveal aliases for the subjects (§10.9); and per kind:
  - `character`: the subject's sheet, and `born`, for their age at the prompt's date
    (§4.13);
  - `family-portrait`: each sitter's snapshot, and their `parents`, `guardians`, and
    `born` and `died` rows (lineage, §9.6);
  - `family-tree`: the family-tree view (§9.6) from the subject, with each member's
    name and dates;
  - `map`: `places.md`, and `routes.md` (travel, §9.4), for the places the map shows;
  - `location`: the place's rows in `places.md`, and the `world.md`, `culture.md`,
    and catalog rows that the place's description names.
- **Writes:** `prompts/<id>.md` (§10.29).
- **Duties:**
  - **Respect the snapshot.** Depict only what the snapshot returns at the prompt's
    cutoff and position: a character's look, possessions, and age as they stand then,
    and a place as it stands then. Name a revealed identity only from its `Revealed at`
    (§10.9). Never depict a hidden truth (§7.2) or a seam conflict.
  - **Family portraits and trees** show only the parentage visible at the cutoff (§9.6).
    A portrait has a date, and leaves out anyone not alive on it: born after it or dead
    before it, by the dates (§4.13). A tree gives each member's name and the dates the
    snapshot knows. It never adds members to fill the tree out.
  - **Maps** show only places the snapshot knows at the cutoff. Their layout follows
    what `places.md` says about where places lie, and the routes' journey times, as
    relative distances. Where neither says, the map leaves the layout open and notes it.
  - **Locations** show the place's state at the cutoff (a ruin is a ruin only from its
    row on), with the culture and systems that are visible there.
  - **Facts, not flourishes.** Composition, lighting, framing, and mood are the
    prompt's to choose, within the author's art direction. Facts about a subject are
    not. A physical detail that the bible does not give goes under `## Gaps`, and the
    prompt either leaves it unstated or marks the choice as the prompter's.
  - Record where each fact comes from in `## Sources`, so the author can check the
    prompt against the bible.
- **Guardrails:** never writes the bible, the manuscript, or reviews. A prompt is never
  canon, and no agent reads one. Never copies source text: it describes in its own
  words (§5). Never describes a real person's likeness, such as an actor who played
  the character, and never asks for a living artist's style by name. Never goes past
  the prompt's cutoff, even when the author asks for "how they end up": that is a
  later cutoff, which the author chooses.

**Example cases:** [M4](../examples/README.md#case-m4).
