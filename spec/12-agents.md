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
| `theorist`           | World learning  | Synthesizes cited, falsifiable theories                                 | `bible/theories.md`                                                        |
| `architect`          | Foundation      | Premise, structure, beat-level outline, the canon track                 | see §12.6                                                                  |
| `worldbuilder`       | Foundation      | Setting and systems (inventor), canon adherence (curator), the ruler    | see §12.7                                                                  |
| `character-designer` | Foundation      | Cast, voices, wants, arcs, relationships                                | see §12.8                                                                  |
| `researcher`         | Foundation      | Real-world grounding and internal plausibility                          | `reviews/research.md`                                                      |
| `drafter`            | Drafting        | The only agent that generates prose from scratch                        | `manuscript/chapter-<NN>.md`                                               |
| `chronicler`         | Drafting        | Records what each chapter establishes in the story-layer ledgers        | `bible/timeline.md`, `bible/game-state.md`, `bible/timelines.md`, `bible/branches.md`, or `revisions.md` |
| `continuity-editor`  | Review          | Internal consistency: manuscript against bible and against itself       | `reviews/continuity.md`                                                    |
| `canon-keeper`       | Review          | External fidelity and leaks (established worlds only)                   | `reviews/canon.md`                                                         |
| `line-editor`        | Polish          | Sentence-level polish; owns the style guide                             | `manuscript/chapter-<NN>.md` or `bible/style.md`                           |
| `dialogue`           | Polish          | Distinct voices; drafts or repairs conversation                         | `reviews/dialogue.md`, or the chapter on an explicit rewrite step          |
| `pacing-analyst`     | Review          | The tension curve                                                       | `reviews/pacing.md`                                                        |
| `critic`             | Review          | Structural developmental feedback                                       | `reviews/critique.md`                                                      |
| `beta-reader`        | Review          | A target reader's felt experience                                       | `reviews/beta-reader.md`                                                   |
| `bridge-builder`     | Crossover       | Drafts the bridge that reconciles a universe's worlds                   | `bridge.md`                                                                |

Each specification below gives the agent's **Reads** as a retrieval spec (§11.6). "The
chapter's cast" means the entities the chapter's outline beat names, plus anyone the
drafted text introduces.

## 12.2 `showrunner`: the dynamic router

Walking a fixed list of steps is mechanical. The showrunner handles the *branches*:
deciding what happens next when the happy path forks.

- **Context:** project.
- **Reads:** `project.yaml`; the active workflow files; `showrunner-log.md`; the output
  of the step just finished; the `## Priorities` of each review; the `## Findings` of
  `reviews/canon.md`; TODO markers found by searching `manuscript/`.
- **Writes:** `showrunner-log.md`.
- **Duties:**
  - After each draft step, route every `TODO: needs bible` marker to the right builder
    (worldbuilder for settings and rules, character-designer for people, architect for
    plot), then re-run the draft. Resolve every TODO before the continuity-editor runs.
  - Read review priorities and schedule revision steps before advancing.
  - Insert on-demand steps the chain lacks (a dialogue pass, a research check), and decide
    which chapters a changed outline invalidates.
  - **Decide items** (§6.9): under `gates: none`, make the call and log the reasoning;
    otherwise surface it to the human. **Order inversions** and **divergence
    conflicts** are never the showrunner's call, and nor is **hidden canon**. Always
    surface them to the author, with the canon-keeper's options or the drafter's
    marker, and wait.
  - **Serials** (§13.3): never schedule a revision of a released installment when releases
    are locked. Route the fix forward to an upcoming installment or the next arc. When a
    consequence invalidates a released installment, absorb it forward or surface it to
    the author. Only the author may accept an inconsistency. Route an *intended* divergence to the
    worldbuilder (curator) to log, and an *accepted* paradox to the chronicler to record.
- **Guardrails:** never writes `bible/`, `manuscript/`, or `reviews/`; never skips a
  gate the policy requires; one agent per step.

## 12.3 `extractor`: source to dated, cited facts

- **Context:** world.
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
    scene, and timecode for video), observing the whole-node rule (§4.2). Number scenes
    using the world's scene breakdown.
  - Record `True from` whenever the unit reveals backstory: when a fact became true
    before the point that reveals it (§4.4).
  - Name every character through the roster. File facts under a **reveal alias's**
    surface slug until the reveal (§10.9). Give canon-distinct **versions** their own
    slug. List unknown names under `## New names`, with a proposed slug that the facts
    then use.
  - Record notable lines under `## Quotations`.
  - Put anything ambiguous under `## Needs a human` rather than guessing canon into
    existence.
- **Guardrails:** never copy source prose: own words plus a citation, always (quotations
  are the only exception). Credit imported fan works through the registry. Never write
  the bible.

## 12.4 `merger`: facts to ordered history

- **Context:** world.
- **Reads:** the rows of every extraction record whose `Target` is its target file;
  `bible/canon-timeline.md`; the existing target file; `bible/characters/_roster.md`;
  `bible/sources.md`.
- **Writes:** one world-layer file per step: its target.
- **Duties:**
  - **Sort by canon point** (§4.2), never by arrival order.
  - **Keep confirmations:** the earliest point is the establishing row, and a later
    confirmation of the same value is kept as its own row. These rows change nothing
    in the ruler's order, but they keep a fact visible to a project that rearranges canon
    (§6.8). Exact duplicates (same point, value, and source) are merged, with their
    citations combined (`; `-separated).
  - **Flag conflicts:** rows with the same entity, attribute, source, and point but
    different values are left out and listed under `## Unresolved conflicts`.
  - **Validate:** points against the ruler, sources against the registry, slugs against
    the roster, and that `True from` is not later than `As of`. Carry `True from` through
    unchanged. Invalid rows go to `## Unresolved conflicts`.
  - **Roster target:** accept `New names` that are unambiguous; record a proposed slug
    that duplicates an existing character as an alias of the existing slug, so that the
    other mergers map it.
- **Guardrails:** adds no facts of its own; append-only except for corrections
  (§4.6) a human has approved; writes only its target. The sole writer for its target,
  so parallel merge instances never collide.

## 12.5 `theorist`: facts to cited interpretations

- **Context:** world.
- **Reads:** `bible/theories.md`; the slices of the bible each theory draws on (state
  histories, `quotations.md`, `knowledge.md`, `plot-architecture.md`);
  `bible/canon-timeline.md`; `bible/sources.md`.
- **Writes:** `bible/theories.md` (§10.13).
- **Duties:** find patterns that explain several facts at once; **cite or cut**; rate
  kind and confidence; state the falsifier; set status, and retire theories that
  higher-tier canon contradicts.
- **Guardrails:** never present a theory as canon. Theories are tier `theory`, the
  lowest, and are opt-in by profile.

## 12.6 `architect`: structure

Turns a one-line seed into a structural blueprint: the premise, the central dramatic
question, and a beat-level outline in which every scene earns its place. It owns story
**structure** (cause and effect, escalation, setup and payoff), including where the
story sits in canon, but not prose.

- **Writes (one per step):** `bible/premise.md`; `bible/outline.md`;
  `bible/canon-track.md` (established worlds, §6.7–6.8); `bible/knowledge.md`
  (self-contained projects).
- **Reads:** `project.yaml` (seed, parameters, `setting`); `bible/premise.md` when writing
  the outline; the roster and `world.md` summary sections; for established worlds,
  `bible/canon.md`, `bible/divergences.md`, the ruler, and `plot-architecture.md` rows
  for the stretch of canon the story covers.
- **Duties:**
  - Interrogate the seed into a logline; find the **central dramatic question**.
  - Break the story into acts, chapters, and scenes. Each scene is **goal, conflict,
    turn**; a scene with no turn is description, so cut or merge it.
  - Track setups and payoffs in the outline's ledger so nothing is planted and
    forgotten.
  - **Canon track:** map chapters to the cutoffs they follow, never past
    `setting.divergence_point` in a branch (§6.6); when the story rearranges
    canon, write the project order, and hand the reordering to the curator to log. When
    the author resolves an inversion by reordering, revise the order (§6.8).
- **Guardrails:** no prose or dialogue; don't over-specify the world; respect the fixed
  parameters (POV, tense, length); prefer fewer, load-bearing scenes. The canon track
  says where the story is in canon, never what it changes. Changes belong in the
  ledger.

## 12.7 `worldbuilder`: setting, adherence, and the ruler

Three modes. The workflow step selects one.

| Mode         | When                                | Writes                                                                                                                                                                              |
| ------------ | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **inventor** | Self-contained projects             | One of `bible/world.md`, `places.md`, `society.md`, `culture.md`, `languages.md`, `lang/<language>.md`, `magic/<catalog>.md`, `game-system.md`, `glossary.md`, `canon-timeline.md` |
| **curator**  | `setting.type: established`         | `bible/canon.md` or `bible/divergences.md`                                                                                                                                          |
| **ruler**    | Extraction, step F0 (world context) | `bible/canon-timeline.md`                                                                                                                                                           |

- **Reads:** `project.yaml` (`setting`); `bible/premise.md`; `bible/outline.md`; the
  index; and per mode: the existing world-layer file being written (inventor); the world
  layer by slice and `references/` (curator); a listing of `texts/` (ruler).
- **Duties:**
  - Give every system a **cost and a limit**. An unbounded system removes tension and
    breaks later plotting.
  - Build factions as engines of conflict; give recurring locations a sensory signature
    and a dramatic function.
  - **Curator:** do not invent. Write the adherence contract (§6.3) by pointing into the
    world layer. Log divergences and their consequences in `divergences.md` (§6.4) when
    planned during foundation, or when the showrunner or a human accepts an emergent one.
    Mark consequences absorbed when the chronicler or continuity-editor reports them
    honoured. Log every change and addition to a canon entity (§6.2), and the reordering
    of canon. For each order inversion or divergence conflict, log **the author's chosen
    resolution** (nothing, if the author keeps the canon event), with the fallout as open
    consequences (§6.6, §6.8). Record every hidden-canon decision in the Hidden canon
    table, and for **reveal early** log the divergence that reveals it (§6.12). Never
    pick a resolution yourself.
- **Guardrails:** don't invent lore the story never uses; don't set rules the plot
  needs to break; never write a world package from project context (§3.1).

## 12.8 `character-designer`: the cast

- **Writes (one per step):** `bible/characters/<slug>.md`; `bible/characters/_roster.md`;
  and, in self-contained projects, `bible/relationships.md` or `bible/voice-guide.md`.
  In world context (extraction step F0b): `bible/characters/_roster.md` (the seed).
- **Reads:** `bible/premise.md`; `bible/outline.md`; `bible/world.md` (summary sections);
  the union roster; the sheets of the characters the new one relates to. In world context,
  a listing of `texts/` and any cast list a human provides.
- **Duties:** separate **want** from **need** (the gap is the arc); name the **lie** the
  character believes; build the voice concretely (rhythm, diction, tics, and one sample
  line); wire relationships as tensions, not labels.
- **Guardrails:** no backstory tourism; antagonists get wants and reasons; voices must
  be mutually distinguishable. In a project referencing a world, writes only original
  characters (`origin: original`) and only project roster rows.

## 12.9 `researcher`: grounding

- **Reads:** the claims under review: `bible/world.md` and the relevant catalogs;
  `bible/timeline.md`; `bible/glossary.md`; `bible/premise.md`; and, when checking prose,
  the chapters named by the step.
- **Writes:** `reviews/research.md`.
- **Duties:** extract the load-bearing factual and logical claims; check real-world
  claims for accuracy and anachronism, calibrated to the genre's promise of rigour;
  audit invented systems for consistency with their own costs and limits; rank findings
  by immersion impact, each with a fix.
- **Guardrails:** advise, don't rewrite; distinguish "wrong" from "couldn't verify";
  flag, don't fabricate.

## 12.10 `drafter`: the only prose generator

- **Reads:**
  - this chapter's beat from `bible/outline.md`;
  - `bible/style.md`;
  - the **snapshot** (§7) of each entity in the chapter's cast, and of each relationship
    between them, at this chapter's cutoff (from the canon track) and position (from
    `derived/`, or computed);
  - the roster's reveal aliases for the cast (§10.9), to decide what the POV character
    can know about who is who;
  - the divergences and open consequences that touch the cast (established worlds);
  - the union `bible/glossary.md`;
  - recent events from `bible/timeline.md`, and the end of the previous chapter;
  - per module: the latest `bible/game-state.md` rows and the relevant
    `game-system.md` entries (LitRPG); the travelers' rows in `timelines.md` and the
    branch in `branches.md` (frames); entries in `languages.md` and `lang/` for languages
    spoken in the chapter (languages);
  - `bible/theories.md` only if the active profile includes a `theory` source.
- **Writes:** `manuscript/chapter-<NN>.md`, with `status: drafted`.
- **Duties:**
  - Render each scene as **goal, rising conflict, turn**; enter late, leave early.
  - Keep POV and tense discipline; plant and pay off per the outline's ledger; use
    glossary spellings.
  - **Respect the snapshot:** use only canon true at the chapter's cutoff, from active
    sources, as amended by the ledger.
  - **Don't add to canon entities silently.** A new physical detail, possession, or
    relationship for a canon character is a divergence (§6.2). Flag it with a
    `TODO: needs bible` marker so the curator can log it.
  - **Hidden truths** (§7.2) are not usable. If the beat touches one that the ledger's
    Hidden canon table has not decided, write as if it were unknown and mark it with
    `TODO: hidden canon` (§6.12). If it has been decided, follow the decision.
  - **Frames:** mark each scene's world point and travelers (§10.19); write each
    character to their own frame.
- **Guardrails:** don't invent canon: mark gaps with `TODO: needs bible`. Don't drift POV
  or tense; don't summarize the exciting parts; write the beat given, raising
  structural concerns to the showrunner; never reproduce source passages.

## 12.11 `chronicler`: what the story has established

Records the story-layer consequences of each chapter so that later chapters, the
snapshot, and the reviewers can rely on them.

- **Reads:** the chapter just drafted (or revised); the target ledger; the showrunner's
  logged decisions (for paradoxes).
- **Writes (one per step):** `bible/timeline.md`; `bible/game-state.md` (LitRPG);
  `bible/timelines.md` or `bible/branches.md` (frames); `revisions.md` (serials with
  revisable releases, §10.23).
- **Duties:** append the chapter's story-time events; append game-state changes with
  their causes; append traveler legs and personal cutoffs; register new branches; record
  paradox decisions with their rationale; log each revision of a released installment,
  with a reader note.
- **Guardrails:** records only what the manuscript states; invents nothing; when
  re-run for a revised chapter, replaces that chapter's rows rather than appending
  duplicates; never writes the world layer or the divergence ledger.

## 12.12 `continuity-editor`: internal consistency

- **Reads:** the chapter under review; snapshots for its cast; `bible/timeline.md`; the
  union glossary; earlier chapters only where a check needs them (found by search);
  relevant `relationships.md` and `languages.md` rows; `game-state.md` and
  `game-system.md` (LitRPG).
- **Writes:** `reviews/continuity.md`.
- **Duties:** flag **manuscript vs. bible**, **manuscript vs. manuscript**, and
  **drift** (spelling or terminology); for LitRPG, check the game-state invariants
  (§9.2); rank by severity (a reader-breaking contradiction outranks a minor slip, which
  outranks cosmetic drift).
- **Guardrails:** internal consistency only (fidelity to the source is the
  canon-keeper's job); report, never rewrite or edit the bible; distinguish a genuine
  contradiction from a deliberate mystery or an unreliable narrator.

## 12.13 `canon-keeper`: external fidelity

Runs only when `setting.type: established`. It diagnoses; it never rewrites.

- **Reads:** the chapter under review; `bible/canon.md`; `bible/divergences.md`;
  `bible/canon-track.md`; snapshots for the cast; `bible/canon-timeline.md`; `bible/sources.md`; the relevant
  `quotations.md` rows; `references/` where there is no world package; `project.yaml`
  (cutoffs, profiles, fidelity); `bible/bridge.md` (universes); `timelines.md` and
  `branches.md` (frames).
- **Writes:** `reviews/canon.md`, with a `## Findings` table (§10.20).
- **Duties:** classify every problem using the classes in §6.9, applying the fidelity
  setting (§6.10). Check rules, characterization, geography, and the canon timeline
  against the **composite**: source canon read along the canon track, overridden by the
  ledger. Treat any unlogged addition to a canon entity as an emergent divergence.
  **Order audit:** when the canon track's order changes, list every order inversion
  (§6.8) as an entry with the options (remove, substitute, supply, reorder) and the
  likely fallout of each, in story terms (§10.20). **Divergence audit** (retellings,
  §6.6): when divergences are logged, read ahead along the canon track and list every
  later canon event a divergence makes impossible or changes, with the options (keep,
  adapt, remove, substitute) and their fallout. Present options; never recommend one as
  the answer. **Branches:** check faithfulness only up to `setting.divergence_point`;
  flag any use of later canon as a temporal leak. **Hidden canon** (§6.12): when a
  chapter or an audit touches a hidden truth the author has not decided about, raise it
  once, with the options (reveal early, keep hidden, other) and what each would mean
  for the story. Flag a chapter that uses a hidden truth without a decision as a
  temporal leak. Join reveal aliases to their true identities from the
  `Revealed at` point (§10.9) when judging what characters could know. Report
  consequences the chapter honours, so the curator can mark them absorbed.
- **Guardrails:** never flag the story for obeying its own logged divergence; never
  silently "correct" an emergent divergence back to canon.

## 12.14 `line-editor`: sentence-level polish

- **Reads:** the chapter; `bible/style.md`; the union glossary.
- **Writes:** `manuscript/chapter-<NN>.md` (status `line-edited`, or `final` on the
  finishing pass), or `bible/style.md` when a step asks it to codify the emerging voice.
- **Duties:** cut filler, hedges, clichés, and repetition; vary rhythm; choose precise
  verbs; enforce POV distance and filtering rules; enforce the style guide's
  text-and-speech formatting (dialogue, thought, marked languages, telepathy, written
  text, reveal-gated markers).
- **Guardrails:** never change what happens (flag plot or continuity changes instead);
  don't homogenize voices; preserve intentional style; edit towards the style guide,
  not its own taste.

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
  full, in order.
- **Writes:** `reviews/beta-reader.md`.
- **Duties:**
  - React moment by moment as the target reader; mark the hook, the sags, the payoffs,
    any confusion, and any loss of trust; give the bottom line (would they finish it,
    recommend it, remember it?).
  - **Flag leftover markers.** List every `TODO` marker still in the prose
    (`TODO: needs bible`, `TODO: hidden canon`, or any other) under
    `## Leftover markers` (§10.20), with its chapter and text. Leftover markers always
    go first in the priorities, because no marked chapter is ready for readers.
- **Guardrails:** react, don't diagnose, except for leftover markers, which are reported
  as found; stay in persona; be honest about boredom.

## 12.19 `bridge-builder`: reconciling a universe

Drafts the bridge that lets two or more worlds share one universe (§8). It proposes;
a human approves at the gate.

- **Context:** universe (§2.6).
- **Reads:** `universe.yaml`; each world's `index.md`, `glossary.md`, and roster; the
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
- **Guardrails:** never edits a world package; never contradicts either world's canon
  (a reconciliation explains differences, it does not overwrite them); prefers `∥` when
  a mapping would force one world to change; flags open questions for the human instead
  of settling them.

