# Decisions

This log records the design decisions behind the spec, most recent first. Each entry
says what was unclear or contradictory, what was decided, and where the rule now lives.

## 0.1: naming

**D54. The project is named LoreStore.** "World System" was already taken. LoreStore
names what the spec defines (a store of dated, sourced canon) and works as a noun ("the
Harry Potter lorestore"). Use "LoreStore" in prose, and lowercase `lorestore` for
package, CLI, and directory names. The GitHub organisation is `lorestore-dev`
(`lorestore` was taken), and the spec repository is `lorestore-dev/lorestore`.
Historical references to `world-system.md` below name the original source document
and are unchanged. → README, §1.1

## 0.1: review round 8

**D53. The beta-reader flags leftover TODO markers.** Every `TODO` marker still in the
prose is listed under `## Leftover markers` in its review, which is present even when
empty, and put first in its priorities. The showrunner routes each one as usual. This is
a late safety net: markers should have been resolved before continuity runs (step 11).
→ §12.18, §10.20, §11.9

## 0.1: review round 7

**D52. `True from`, hidden truths, and the author's call (resolves Q8).**
- **Data.** State rows gain an optional `True from` column: when a fact became true
  in-world, as opposed to `As of`, when the source reveals it. Extractors record it
  whenever a source reveals backstory, for resilience, whether or not any project needs
  it yet. `As of` still governs visibility.
- **Hidden truths.** The snapshot lists them separately: facts true at the cutoff but
  not yet revealed. Agents may not use them unprompted.
- **Raised when relevant.** When a chapter or audit touches one, the drafter
  (`TODO: hidden canon`) or the canon-keeper raises it with the author once.
- **The author decides.** Reveal early (logged as a divergence), keep hidden, or
  anything else, under every gate policy. The curator records each decision in a new
  `## Hidden canon` ledger table, so it is not raised again.

Example: Snape's love for Lily (`As of DH:33`, `True from PS`) is revealed early in the
`no-horcruxes` branch. → §4.4, §6.12, §7.2, §10.6, §10.8, §10.19, §11.8, §11.9, §12

## 0.1: review round 6

**D51. Branch or retelling: `setting.canon_mode`.** A project says whether canon after
its divergence point still happens:
- **`retelling`** (the default, and the previous behaviour): later canon is the default
  script along the canon track. Later canon events that a divergence makes impossible
  or changes are **divergence conflicts**. The canon-keeper finds them ahead of time
  (new audit step E2a) and sets out options: keep, adapt, remove, substitute. The
  author decides, even under `gates: none`, and the curator logs the choice (nothing,
  for keep).
- **`branch`**: canon is frozen at the divergence point. The cutoff never passes it, and
  later canon is a leak. From then on the story's own history accumulates in the
  ledger.

`setting.divergence_point` (`divergence_points` for universes) makes the point
machine-readable; a branch requires it. `fidelity` is unchanged and independent. The
new examples are `no-horcruxes` (a branch) and `blind-harry` (a retelling).
→ §6.6, §6.9, §6.11, §7.1, §10.1, §10.20, §11.8, §12, §13.4, §14

## 0.1: review round 5

**D50. The serial workflow is defined (resolves Q6).** It is for stories released in
installments as they are written:
- **Phases.** Foundation runs once. Then each arc is planned (A1–A2), released
  installment by installment (steps 10–14, then the new `release` skill), and reviewed
  as an arc (V1–V4). Installment steps keep `novel`'s numbers, so overlays apply
  unchanged.
- **Released installments** are `locked` by default. A project can set
  `serial.released: revisable`.
- **Under `locked`,** fixes go forward. A consequence that would invalidate a released
  installment is absorbed in a later one, or `accepted` by the author (a new consequence
  status, author-only).
- **Under `revisable`,** each change is re-released and logged in `revisions.md`, with a
  reader note, by the chronicler.
- **Arcs** are headings in the outline. A new repeat kind, `per-arc`, is added.
→ §13.3, §10.1, §10.8, §10.19, §10.23, §10.24, §11.10, `schemas/`

## 0.1: review round 4

**D49. Order inversions are the author's decision.** Previously the curator resolved
each inversion itself, usually by holding the earlier state with `Until`. An inversion
is a story problem, and only the author can say how the story handles it. Now:
- **The canon-keeper sets out options.** Its order audit (new step E1b) lists each
  inversion with options and their likely fallout: remove the event, substitute someone
  or something already known, supply the dependency earlier, or reorder. It never
  recommends one.
- **Only the author decides.** That holds even under `gates: none`; the showrunner may
  not decide inversions.
- **The curator logs the author's choice,** and its fallout becomes open consequences
  that the author resolves. Agents track them and draft what the author decides.

In the example, the author substitutes Dumbledore for Sirius as Harry's correspondent,
and removes Cedric's PoA appearances. → §6.8, §6.9, §10.20, §11.8, §13.4, §14.1

## 0.1: review round 3

**D42. Any change to a canon entity is a divergence (resolves Q2).** This includes
additions where canon is silent. A new scar is a divergence even if the plot then
follows canon, because the character is physically different from canon from that point
on. New entities (original characters) are not divergences; their relationships with
canon characters are. The drafter flags such additions, and the canon-keeper treats
unlogged ones as emergent divergences. Ledger rows use `(silent)` for "Canon
establishes". → §6.2, §6.4

**D43. The snapshot never joins reveal aliases (resolves Q3).** The surface and true
identities stay separate entities. Agents decide when and to whom the connection is
known, using the roster's `Reveal of` and `Revealed at` and `knowledge.md`. → §7.3,
§10.9

**D44. New agent: `bridge-builder` (resolves Q4).** It drafts `bridge.md` in a new
universe context, from the author's `brief.md` and the member worlds, and a human
approves it at a milestone gate in the new `crossover` workflow. It proposes mappings,
collisions, and consistency rules, and adds crossover canon only on request.
→ §8.4, §12.19, §13.7

**D45. The canon track: the cutoff advances by chapter (resolves Q5).** A long story can
follow canon while adding to it. `bible/canon-track.md` maps chapters to cutoffs, and
additions along the way are divergences (D42). Written by the architect. → §6.7, §7.1

**D46. Projects can rearrange canon.** The canon track can hold a project order: a
permutation of the world's segments that replaces the ruler's order for every comparison
in the project. For example, moving *Goblet of Fire* to second year means Harry hasn't
met Sirius during the Tournament. The reordering is logged as a divergence. Where canon
rows now precede the canon they depend on (order inversions), the host reports them and
the curator covers each with a divergence. A new optional `Until` column lets such a
divergence end when the story catches up. → §6.8, §10.8, §10.22

**D48. The merger keeps confirmations as rows.** Folding a later confirmation into
the citation of the earliest row lost information that a reordered project needs. For
example, *Goblet of Fire* establishes Cedric's house too, not only *Prisoner of
Azkaban*. Same-value rows are not order inversions, and `Overrides` may assign
`(unset)`. → §12.4, §6.8, §10.8

**D47. Added the missing `architect` specification.** It was in the roster but had no
section. It is now §12.6, and it also owns the canon track. Later agent sections were
renumbered.

## 0.1: review round 2

**D41. Canon points are paths down a ruler tree, with optional timecodes.** The flat
`work[:unit[.sub]]` form could not express a scene in a TV episode
(series:season:episode:scene), nor a timecode within video. Now:
- **The ruler is a tree.** Each work declares its levels (`season › episode › scene`,
  `chapter › scene`) and its timed level (an episode, or a whole film).
- **Reading order is a list of segments.** A segment can be any node, so series can
  interleave by season, and with films.
- **Points are paths with an optional timecode,** such as `TOS:3:2:14+00:12:31`.
  Timecodes are measured from the start of the episode or film and use `+`, because `@`
  stays the frames branch marker (`TNG:3:15@alt-war`).
- **Scene indices replace sub-points.** `PS:6.2` became `PS:6:2`. Scene numbering is the
  world's own extraction breakdown.
- **Counts have three states.** `Units` can be counted (an integer), uncounted (empty),
  or undivided (`—`). An optional Counts table covers deeper nodes.
- **Points are partially ordered.** A timecode-only point and a scene-only point in the
  same episode are incomparable, and a host reports the pair instead of guessing.
- **The whole-work rule becomes the whole-node rule,** and applies at every level.

Supersedes D12, D13, and the point grammar in D14. → §4.1–4.3, §10.4, `schemas/`

## 0.1: review round 1

**D36. Profiles choose a resolution mode (resolves Q1).** A profile now has
`resolution: precedence` (the default: the highest source wins, and lower sources only
fill gaps) or `resolution: recency` (the latest row wins, whichever source it comes
from). An **enhanced** profile uses `recency`, so fanon and imported fan works can move a
character on from where canon left them. The project's own changes are unaffected: the
divergence ledger overrides the result under every profile. → §5.4, §7.2

**D37. Harry Potter and Star Trek throughout (replaces D35).** Both franchises are
widely known and represent the two main kinds of world: magic (novels, chapters,
spells) and technology (seasons, episodes, starships, species). The invented fixture
world was replaced with abridged packages for both, a project in each, and a crossover
universe. Facts are paraphrased with citations.

**D38. Universes are versioned.** A universe project pins `universe.version`, but
`universe.yaml` had no version. It now has one, bumped like a world package's. → §8.1

**D39. Corrected the ledger example.** The original example said canon has Cedric
survive and the story kills him. Canon is the reverse (he is killed in the graveyard,
GoF ch.32), so the example now has the story save him. → §6.4

**D40. Apache License 2.0 (resolves Q7).** Chosen for a spec meant to be implemented: it is
permissive, it covers prose, schemas, and future code with one licence, and its patent grant
protects implementers (the OpenAPI specification uses it for the same reasons). The README
records the copyright and attributes the Harry Potter and Star Trek properties to their
owners; there is no separate NOTICE file. → `LICENSE`, README

## 0.1: consolidation into a spec repository

The spec began as three overlapping documents (`world-system.md`, `contract.md`,
`agents.md`) that restated the same rules and had drifted apart. They were merged into
numbered chapters, each concept defined in exactly one place. The decisions below
resolve the contradictions and gaps found while doing so.

### Structure

**D1. One concept, one chapter.** The orchestration loop, agent anatomy, gates, the write
boundary, and the temporal model were each stated in two or three documents. Each now
lives in one chapter, and the others link to it. → README

**D2. The file catalog is the authority on layers and writers.** The layer lists in the
three documents disagreed (`timeline.md`, `relationships.md`, and the frames files sat
in different layers in different places). The catalog in §3.3 is now the single
answer, and agents and workflows must match it. → §3.3

### The canon store

**D3. The divergence ledger is its own story-layer file, `bible/divergences.md`.**
Previously the ledger lived "inside `canon.md`", while `canon.md` was also listed as a
read-only world-layer file: a project could not fork canon without editing the world.
→ §6.4

**D4. `canon.md` is a story-layer adherence contract.** Its content (canon in scope,
point of divergence, original additions) was always specific to one story. The world's
source canon is its state histories. → §6.3

**D5. `timeline.md` is story-layer.** It was described as a ledger "filled as a
manuscript starts", but listed in the world package. → §3.3

**D6. `bible/` paths resolve by layer.** Agent paths were relative to a project, yet
world files live in `worlds/<id>/`. Story-layer paths now resolve to the project and
world-layer paths to the package. Universe projects use `bible/@<world-id>/…`. A project
may not shadow a world file. → §2.6

**D7. Roster, glossary, and index are union files.** Projects need to register original
characters and terms without editing the world's files. A project's rows are appended to
the world's; a collision is an error. → §2.7

**D8. Profiles are defined only in `world-config.yaml`.** `contract.md` placed them in
`project.yaml`; `world-system.md` said a project only selects one. The latter won.
Self-contained projects define theirs in `bible/world-config.yaml`. → §5.4

**D9. World status and version live in `world-config.yaml`.** `status` was previously
"marked in `index.md`". Packages now carry a semantic version, projects pin it, and a
mismatch is reported. → §2.8

**D10. Corrections are made in place and bump the version.** Append-only applies to
canon time, not editorial error. Fixing a wrong row by appending a later row would
assert a change the source never made. → §4.6

**D11. `(unset)` ends a fact.** There was no way to record that an attribute stops
holding. → §4.5

**D12. The whole-work rule.** A row dated with a work's own point (`PS`) is visible from
the work's start, so only facts true from the opening may use it. → §4.2

**D13. Ruler units are a plain integer.** The forms `17`, `1–17`, and `ch. 1–17` were
all allowed. Only an integer, or empty, remains. → §10.4

**D14. As-of is always a canon point.** In-world dates were "legal and comparable", but
nothing defined how they compare with canon points. They are now kept out of state
histories; they appear in story-time events and universe offsets. The crossover example
episode codes such as `S10E05` became season-and-episode points such as `TNG3:15`. → §4.2, §8.1

**D15. Original worlds may omit the ruler.** Their rows are timeless (empty as-of), and
story-time change goes in `timeline.md`. → §4.7

**D16. New tiers and reserved sources.** The `theory` tier was used but missing from the
tier list. `crossover` (bridge canon) and `story` were added, with reserved source ids
`bridge` and `project`, so that original-character rows and bridge rows validate. → §5.1–5.2

**D17. Precedence is resolved before recency** by default. This was implicit before and is
now stated explicitly. D36 adds recency as a per-profile alternative. → §7.2

**D18. Ledger dates use the manuscript's clock.** Divergences are events in the story, so
*First occurs* is a chapter id, not a canon point. The snapshot takes a manuscript
position as an input. → §6.4, §7.1

**D19. The ledger is machine-applicable.** A new `Overrides` column
(`slug.attribute=value`) lets the snapshot apply divergences. Previously the snapshot
ignored the ledger entirely. Consequences moved to their own table with a status. → §6.4, §7.2

**D20. Source leaks and crossover leaks are named classes.** Both were described but were
missing from the canon-keeper's taxonomy. → §6.9

**D21. Theory fields unified.** `well-supported` had been a *kind* in one document and a
*confidence* in another. Now: kind = `authorial-intent` | `reading-beyond-text`;
confidence = `speculative` | `plausible` | `well-supported`. → §10.13

### Extraction

**D22. One extraction workspace path.** The extractor's output appeared in three
different forms. It is now `extraction/<world>/extractions/<work>/ch<NN>.md`, outside
the package, with the source texts in `extraction/<world>/texts/`. → §2.4

**D23. Project `sources/` became `references/`.** It sat next to `sources.md` (the
registry) and `extraction-sources/`. → §2.5

**D24. The merger is the only merge writer.** The worldbuilder and character-designer
each had a "merge mode" writing the same files. Those modes were removed. → §12.4

**D25. The roster is seeded, then merged first.** The extractor needs slugs, but nothing
created the roster. Step F0b seeds it, extractors propose new names, and F2a merges the
roster before any other target. → §13.6

**D26. The extractor reads one unit.** It previously read "the rest of the world", which
undermined parallel extraction and the retrieval rule. → §12.3

### Agents and workflows

**D27. New agent: `chronicler`.** Nothing maintained `timeline.md`, `game-state.md`,
`timelines.md`, or `branches.md`, and the showrunner was told to write `branches.md`
while forbidden from writing the bible. → §12.11

**D28. Every file has a writer.** Writers were assigned for files that had none:
- the architect writes `knowledge.md`;
- the character-designer writes `relationships.md` and `voice-guide.md`;
- the worldbuilder (inventor mode) writes the other world-layer files;

these assignments apply in self-contained projects. → §3.3

**D29. `Reads` are retrieval specs.** Several agents read `bible/**` or "the full
bible", contrary to the retrieval rule. Their reads now name slices. The whole-book
reviewers are an explicit exception for the manuscript only. → §11.6, §12

**D30. Repeated steps, not multi-file outputs.** The final polish wrote
`manuscript/**`. It is now one step per chapter. → §11.4, §13.1

**D31. Gates: three policies, one gate level.** `✅ always` matched no policy and was
dropped. Decide items now block under every policy. → §11.8

**D32. Workflow files have a defined format,** and overlays follow from `setting`
instead of being configured. → §11.7, §13

**D33. Small fixes:** the "gate after step 6" note pointed at the wrong step; "all four
review priorities" referred to three reviewers; the relative links were broken.

### Repository

**D34. JSON Schemas for the three manifests**, with `spec_version: "0.1"`. → `schemas/`

**D35.** *Superseded by D37.*

## Open questions

**Q1.** *Resolved by D36.*

**Q2.** *Resolved by D42.*

**Q3.** *Resolved by D43.*

**Q4.** *Resolved by D44.*

**Q5.** *Resolved by D45 and D46.*

**Q6.** *Resolved by D50.*

**Q7.** *Resolved by D40.*

**Q8.** *Resolved by D52.*
