# 6. Divergence: the living-canon mechanism

A story set in an established world forks from canon. The fork is **recorded in the
project's story layer**, never by editing a lower layer (§3.1, W3). The manuscript
obeys:

> **The project's stack, read at its sync points, overridden by the ledgers of its
> project layers and then by its own.**

Three things carry this: the adherence settings in `project.yaml` (§6.3), which the
author writes; the ledger, written by the worldbuilder in curator mode (§12.7); and the
sync points, written by the architect (§12.6).

## 6.1 When this applies

This chapter applies to projects with `setting.type: established`: any project set in a
world it did not invent, whether the world comes from packages, a universe, or an
earlier book. An established project MUST have at least one package or project layer,
and an original project MUST have none: `setting.type` and `layers` always agree. A
self-contained original project has nothing to diverge from. A project that borrows a
world only loosely, its places or its magic but not its plot, is established with
`fidelity: au` (§6.10), so its ledger still records what it changes.

A world known only from material in `references/` is not yet canon the snapshot can
read. It is first built into a package by the extraction workflow (§13.6), from texts
or notes a human supplies, or, if it was invented in a project, promoted (§2.9). Files
in `references/` stay background reading for the agents, never a source of rows.

## 6.2 What counts as a divergence

A divergence is **any difference between the state of a canon entity in this story and
its state in canon**, at the same point in the story. That includes:

- **Changes**: canon says one thing, and the story says another (Cedric survives).
- **Additions to canon entities**: canon is silent, and the story adds something.
  If Harry gains a burn scar on his left hand in an original scene, that is a
  divergence, even if the plot then follows canon exactly. Harry is now physically
  different from canon Harry, and every later chapter must honor it.
- **Removals**: something canon establishes never happens.
- **Structural changes**: canon events happen in a different order (§6.8), or the story
  skips a stretch of canon.

Things that are **not** divergences:

- **New entities.** Original characters, places, and institutions are story-layer
  entities (`origin: original`). They are recorded in the project's own sheets and
  roster, not in the ledger. A canon entity's relationship *to* an original character
  (Hermione befriends Mara) is a divergence, because it changes a canon entity's state.
- **Story-time events that change no canon state.** A conversation canon never shows,
  but which alters nothing canon records, goes in `timeline.md` (§10.15).

Every divergence that can be expressed as attribute values SHOULD be, so that the
snapshot applies it mechanically (§6.4, `Overrides`).

## 6.3 Adherence: how the story relates to its stack

How a story relates to its stack is the author's to say, so it lives in `project.yaml`
(§10.1), which only the author writes:

| What                   | Where                                                                                     |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| **What is in scope**   | The stack (`layers:`, §2.2) and the cutoff (`setting.cutoff`, moved by sync points, §6.7). Agents read the rows in scope from the composed bible (§7.6). |
| **Where it departs**   | `setting.divergence_point`, if it departs, and `setting.follow`: whether later canon still happens (§6.6). |
| **Order**              | `setting.order`, if the story rearranges canon (§6.8).                                    |
| **Fidelity**           | `setting.fidelity` (§6.10), and `setting.fidelity_notes`: free text for any latitude of the project's own, such as what is load-bearing and must hold. |

The story's original additions are not restated anywhere: they are its own entities,
marked `origin: original` in its roster (§10.9) and labeled with the project's layer in
the composed bible.

**A series begun by a self-contained book.** A later book's only layers are project
layers. Its ruler is the series ruler (§4.12): the first book's manuscript, with
whatever the later books insert before and after it. The settings above then work as
they do over a base.

**Where the books meet.** A later book may be set after the earlier one, before it, or
partly each. What the earlier book brings in holds only from where it was established;
anything earlier is the author's decision (§6.14). A later book that sets no order uses
its highest project layer's order, if one has an order (§6.14).

## 6.4 `divergences.md`: the ledger

The ledger has two tables, **Divergences** and **Consequences**, and up to three
optional ones recording the author's decisions: **Hidden canon** (§6.12), **Theory
conflicts** (§6.13), and **Seam conflicts** (§6.14).
Format: §10.8.

**Divergences**

```
| ID | Canon establishes                          | This story changes it to          | Overrides                                         | Kind     | First occurs |
| -- | ------------------------------------------ | --------------------------------- | ------------------------------------------------- | -------- | ------------ |
| D1 | Cedric is killed in the graveyard (GoF:32) | Cedric survives, badly injured    | cedric-diggory.status=alive                       | planned  | chapter-01   |
| D2 | (silent) Hermione and Mara have never met  | Hermione befriends Mara           | hermione-granger+mara-quill.bond=friends          | emergent | chapter-07   |
| D3 | (silent) Harry's only scar is the lightning bolt | Harry also has a burn scar on his left hand | harry-potter.scars=lightning bolt; burn on left hand | emergent | chapter-09 |
```

A technology world forks the same way. In a Star Trek project:

```
| D1 | Picard is rescued from the Borg (TNG:4:1) | Picard remains Locutus | jean-luc-picard.status=assimilated | planned | chapter-01 |
```

- **Canon establishes** states the canon position, or `(silent)` for an addition where
  canon says nothing.
- **Overrides** is the machine-applicable part: a `;`-separated list of
  `<slug>.<attribute>=<value>` assignments the snapshot applies (§7). It is `—` when the
  divergence cannot be expressed as attribute values. The prose columns then carry it,
  and the drafter and canon-keeper apply it by judgment. An override **replaces** the
  attribute's whole value, so an addition restates what canon already has (D3 keeps the
  lightning bolt).
- **Kind** is `planned` (decided before drafting) or `emergent` (found in drafted
  prose and accepted).
- **First occurs** is the **manuscript position** where the divergence takes effect: a
  chapter id (`chapter-07`). Divergences live on the story's clock, not the source's,
  because they are events in this story.
- **Until** (optional) is the chapter from which the divergence **stops** applying.
  Most divergences are permanent and leave it empty. It is used when a divergence
  covers a temporary gap, such as a knock-on of rearranged canon (§6.8) that ends once
  the story catches up.
- **Basis** (optional) names the theory a divergence adopts, and which of its claims:
  `harry-potter/theories:T1 (claims 1, 3, 4)` (§6.13).

**Consequences**

```
| Divergence | Consequence                                                                     | Status   | Absorbed in |
| ---------- | ------------------------------------------------------------------------------- | -------- | ----------- |
| D1         | Cedric is a living witness to Voldemort's return; the Ministry cannot dismiss two witnesses so easily | open |  |
| D1         | Cho and Cedric's relationship continues                                         | absorbed | chapter-04  |
| D2         | Every later scene with both of them treats them as friends                      | open     |             |
| D3         | Every later scene that shows Harry's hands must show the burn                   | open     |             |
```

Every divergence MUST list at least one consequence, or a single row stating `none`
with a reason.

### Ledgers of earlier books

A project that stacks another project (§2.2) reads that project's ledger, read-only, as
of the pinned chapter: a divergence applies if its `First occurs` is at or before the
pinned chapter and its `Until`, if any, is after it, and, where the later book is set
earlier than the earlier book established it, the author has carried it back (§6.14).
Project-layer ledgers apply in
stack order, each after the ones it brings in itself, and the project's own ledger
applies last. Book 2 therefore starts from everything book 1 changed: if Cedric
survives book 1 (`D1`), he is alive in book 2 without book 2 logging anything.

**The author's decisions carry over too.** An earlier book's Hidden canon and
Seam conflicts rows whose `Decided in` is at or before the pinned chapter
bind the later book, and so do the Theory conflicts rows of a theory its divergences in
force at the pin adopt. The later book does not raise those questions again. Where two
ledgers decide the same question, the later one in the order above wins.

The later book cannot edit an earlier book's ledger. To change one of its divergences,
it logs its own, which overrides it from its `First occurs`. To decide one of its
questions differently, it records its own row, and logs a divergence if the new
decision needs one. An earlier book's open
consequence that the later book honors is tracked in the later book's Consequences
table, with the divergence qualified by project: `two-witnesses:D1`.

## 6.5 Ledger rules

1. **Binding forward.** Once logged, an entry is canon for every chapter from its first
   occurrence until its `Until` chapter, if any. Those chapters obey the ledger, not the
   source, for anything the entry covers.
2. **Consequences are binding too.** A character who dies cannot appear alive later; a
   war averted changes its fallout.
3. **Retroactive effects are consequences.** If a divergence invalidates an
   already-written chapter (an earlier "Muggle" reference that is now wrong), that is
   an `open` consequence naming the chapter to revise.
4. **Open consequences are tracked** until each is `absorbed`, with the chapter that
   absorbed it. In a serial whose released installments are locked, a consequence that
   would invalidate a released installment is absorbed forward, or `accepted` by the
   author (§13.3).
5. **The ledger is the only route to changing canon state.** No agent may edit a lower
   layer, or restate canon differently anywhere else in the project, to achieve a fork.

## 6.6 Branch or retelling: how strictly later canon binds

A divergence changes canon at some point. The project must also say what happens to
the canon that comes **after** that point. `setting.follow` sets this, and
`setting.divergence_point` names the point (§10.1).

| `follow`                   | Canon after the divergence point                                                            | Example                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `retelling` *(the default)* | **Still happens**, by default, as the story moves through its sync points. Divergences change it only where they reach. | Harry is blinded by the curse at Godric's Hollow. The canon storyline still unfolds, and the story is how he meets it. |
| `branch`                   | **Never happens.** Canon is frozen at the divergence point, and from there the story writes its own. | There are no Horcruxes, so when Harry defeats Voldemort at the end of *Philosopher's Stone*, Voldemort dies. Most of later canon can no longer occur. |

### Branch

- **The cutoff stops at the divergence point.** The snapshot never resolves past it
  (§7.1), and no sync point may advance beyond it (§6.7). Canon dated later
  never becomes visible, however far the story runs, and using it is a temporal leak.
- **From the divergence point on, the story is its own canon.** Changes the story makes
  to canon entities are still divergences (§6.2), usually with `Canon establishes` set
  to `(silent)`. Over time the ledger becomes the record of the branch's own history.
- **Checks narrow.** The canon-keeper checks faithfulness only against canon up to the
  divergence point, and self-consistency everywhere. An event that differs from later
  canon is not a divergence, because later canon does not apply.

### Retelling

- **Later canon is the default script.** The sync points advance the cutoff (§6.7), and
  canon events happen unless the ledger changes them. Departing from later canon
  without a ledger entry is a faithfulness break or an emergent divergence, judged by
  `fidelity` (§6.10).
- **Divergences reach forward, and the author decides how far.** A divergence can make
  later canon events impossible, or change them. A blind Harry cannot simply become
  Gryffindor's Seeker in `PS:9`. Each such event is a **divergence conflict** (§6.9).
  The canon-keeper finds it ahead of time and sets out options; the author decides:

  | Option         | What happens                                       | Harry made Seeker (`PS:9`)                                          |
  | -------------- | -------------------------------------------------- | ------------------------------------------------------------------- |
  | **Keep**       | The canon event happens as written                 | He is made Seeker anyway. The author owns how that works            |
  | **Adapt**      | It happens, changed to fit the divergence          | McGonagall sees him fly by sound and feel, and makes him Seeker     |
  | **Remove**     | It doesn't happen                                  | He is never on the team; the Nimbus Two Thousand never arrives      |
  | **Substitute** | Something else happens in its place                | Someone else is made Seeker, and Harry finds another way in         |

  The curator logs every choice except **keep** as a divergence, and its fallout as
  open consequences (§6.4). As with order inversions, no agent chooses, even under
  `gates: none` (§11.8).
- **Every divergence is audited, wherever it comes from.** The divergence audit covers
  each divergence in force: the project's own, and those of its project layers (§2.2),
  since an earlier book's change reaches into this book's canon too. It runs again
  whenever a divergence is logged, for whatever reason: a planned one, an accepted
  emergent one, or one logged to carry out an author's decision (a divergence conflict,
  a hidden-canon reveal, an order inversion, an adopted theory, or a seam conflict
  decided `keep-earlier` or `other`). A resolution can
  reach further than the divergence it resolves: removing Harry's Nimbus changes every
  later match. The audit repeats until it finds no new conflict.
- **Reach candidates.** The host SHOULD list, for each divergence, every canon row in
  the stack on an attribute it overrides, dated at or after the cutoff where the
  divergence first occurs (§6.7). Each candidate is a likely divergence conflict, and
  the canon-keeper MUST address it in the audit, as a conflict or with a note saying why
  it is not one. The list is a floor, not the whole audit: most conflicts fall on other
  attributes (a blind Harry's `sight` meets no canon row, but his `role` does), so the
  canon-keeper still reads ahead.

`fidelity` and `follow` are independent. `follow` decides whether later canon
applies at all. `fidelity` decides how strictly unplanned departures from the canon
that does apply are judged.

## 6.7 Following canon: sync points

A long story often **keeps following canon** while it adds to it. A fanfic can run
alongside the books from first year to seventh, adding scenes and characters along the
way. Its cutoff cannot be one fixed point: what Harry knows in chapter 40 is not what he
knows in chapter 1.

**Sync points** (`bible/sync-points.md`, format §10.21) tie manuscript chapters to
cutoffs:

```
## Sync points
| From chapter | Cutoff  |
| ------------ | ------- |
| chapter-01   | PS:6    |
| chapter-08   | PS:17   |
| chapter-12   | CoS:1   |
```

- The cutoff for a chapter is the row with the latest `From chapter` at or before it.
  Before the first row, and in projects with no sync points, `setting.cutoff`
  applies.
- A universe project adds a `Base` column after `Cutoff`, and gives each base its own
  sync points.
- Cutoffs SHOULD advance through the story. A host SHOULD warn when a later row's
  cutoff is earlier, which is legitimate only for a deliberate jump back, such as a
  flashback.
- In a **branch**, no sync point's cutoff may be later than `setting.divergence_point`
  (§6.6).
- Sync points say **where in canon** each chapter sits. What the story **changes** is
  still the ledger's job: additions and changes made while following canon are
  divergences (§6.2).

## 6.8 Rearranging canon

A story can also **change the order** in which canon happens. For example, a fanfic
might move the Triwizard Tournament from fourth year to second year. The original
*Chamber of Secrets* then becomes year three, and *Prisoner of Azkaban* year four. Harry
has not met Sirius during the Tournament, because in this story the events of *Prisoner
of Azkaban* have not happened yet.

The project's own **order** of the base's ruler segments (§4.1) is `setting.order` in
`project.yaml` (§10.1). Like the rest of the adherence settings (§6.3), only the author
sets it:

```yaml
setting:
  order: [PS, GoF, CoS, PoA, OotP, HBP, DH]
```

Rules:

1. **A permutation of the segments.** The project order MUST list every one of the
   segments of the stack's ruler exactly once: the base's, and any that official or
   fanfic packages in the stack insert (§4.10); or, in a series begun by a
   self-contained book, each project layer's work and every segment the project layers
   and the project itself insert (§4.12). Leaving canon out is a removal, logged as a
   divergence, not an omission from the order. Moving something smaller than a segment
   requires the base's ruler to have finer segments.

   **When the stack changes.** Adding or removing a package that inserts segments, a
   base version that splits one (§4.1), or a project layer or a project
   `canon-timeline.md` that inserts or removes one (§4.12), leaves the order no longer a
   permutation. The host MUST NOT run any step until the order is fixed, and proposes
   one: each new segment placed in the project order right after the segment it follows
   on the new ruler, in ruler order, and each segment the ruler no longer has dropped.
   The author accepts the proposal or edits it, in `setting.order`, and the order audit
   then runs again (§13.4, E1a). A later book that inherits its order (§6.14) and
   changes its stack sets its own.
2. **The project order replaces the ruler's order** for every comparison in this
   project: cutoffs, the time filter, and recency (§4.2, §7). Under the order above,
   `GoF:20` sorts before `PoA:17`, so at a mid-Tournament cutoff Harry and Sirius are
   still strangers.
3. **The reordering is itself a divergence.** It is logged in the ledger (`Overrides`:
   `—`, kind `planned`), with its consequences. For example, Harry is twelve, not
   fourteen, during the Tournament.
4. **Order inversions are knock-ons.** Canon rows can depend on earlier canon that now
   comes later. For example, at `GoF:2` Harry writes to Sirius, which presumes they met
   in `PoA:17`. Whenever the project order reverses two rows of the same attribute's
   history that have **different values**, the host MUST report an **order inversion**
   (§6.9). Rows with the same value (a fact confirmed in both works) are not
   inversions.

   **Inversion candidates.** Dependencies also cross attributes. In the first task
   (`GoF:20`) Harry summons the Firebolt he was given in `PoA:11`, but *Goblet of Fire*
   has no `broom` row, so no two rows of one attribute are reversed. The host SHOULD
   list, for each pair of segments the project order swaps, every entity with rows in
   both. Each candidate is a likely inversion, and the canon-keeper MUST address it in
   the order audit, as an inversion or with a note saying why it is not one. Like reach
   candidates (§6.6), the list is a floor: the canon-keeper still reads the reordered
   canon for dependencies between entities.
5. **The author decides every inversion.** An inversion is a story problem, not a
   bookkeeping one, and only the author can say how the story handles it. The
   canon-keeper flags each one and sets out options, each with its likely fallout
   (§10.19). The author chooses one of them, or something else entirely:

   | Option        | What happens                                                   | Harry's letters to Sirius                                        |
   | ------------- | -------------------------------------------------------------- | ---------------------------------------------------------------- |
   | **Remove**    | The dependent event does not happen                            | Harry doesn't write to anyone about his scar                     |
   | **Substitute** | The event happens with someone or something already known     | Harry writes to Dumbledore instead                               |
   | **Supply**    | The story establishes the dependency earlier, itself           | An original scene has Harry meet Sirius before the Tournament    |
   | **Reorder**   | Change the project order so the dependency comes first         | Put *Prisoner of Azkaban* back before *Goblet of Fire*           |

   No agent chooses for the author: the showrunner does not decide inversions, even
   under `gates: none` (§11.8).
6. **The choice is logged as a divergence, and its fallout is the author's.** The
   curator records the author's choice in the ledger. That usually includes `Overrides`
   that keep the inverted canon row from applying, often with an `Until` for when the
   story catches up. The fallout goes in as `open` consequences. The author decides how
   each one plays out; agents track the consequences and draft what the author decides,
   but no agent decides it.

   ```
   | D2 | Harry writes to Sirius about his scar (GoF:2), having met him (PoA:17) | Harry writes to Dumbledore instead; he and Sirius stay strangers until the Shrieking Shack | harry-potter+sirius-black.bond=strangers | planned | chapter-01 | chapter-40 |
   ```

   ```
   | D2 | Dumbledore hears about Harry's scar directly, months earlier than in canon | open | |
   | D2 | Sirius's advice before the first task has no source; replace it or cut it | open | |
   ```

   Here `chapter-40` is where the story reaches the Shrieking Shack (`PoA:17`). From
   there the canon rows apply in the project's order.

## 6.9 Classifications

The canon-keeper (§12.13) classifies every problem it finds. Each class has a fixed
resolution type, which a host MUST surface distinctly (§14):

| Class                         | Definition                                                                                      | Resolution                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Faithfulness break**        | Contradicts source canon, and no ledger entry covers it.                                        | **Fix**: route to the owning agent.                                |
| **Emergent divergence**       | A new fork the prose introduces that the ledger does not yet record, including an addition to a canon entity (§6.2). | **Decide**: intended (log it, with consequences) or mistake (fix). |
| **Self-consistency break**    | Contradicts the story's own ledger, for example by ignoring a consequence.                      | **Fix**.                                                           |
| **Divergence conflict**       | Retellings: a later canon event that an active divergence makes impossible or changes (§6.6). | **Author decides**: keep, adapt, remove, or substitute. Never decided by an agent. |
| **Hidden canon**              | A hidden truth (§7.2) bears on the chapter or audit at hand, and the author has not yet decided about it (§6.12). | **Author decides**: reveal early, keep hidden, or the author's own choice. Never decided by an agent. |
| **Order inversion**           | The project's order puts a canon row before the canon it depends on (§6.8).                    | **Author decides** (§6.8, rule 5): remove, substitute, supply, reorder, or the author's own resolution. Never decided by an agent. |
| **Theory conflict**           | Evidence in the stack, at any point, contradicts a claim of a theory the project adopts or proposes to adopt (§6.13). | **Author decides**: keep, adapt, or discard each claim. Never decided by an agent. |
| **Seam conflict**             | An earlier book's item is ahead of the chapter, or a canon attribute resolves differently from the earlier book, and the author has not yet decided (§6.14). | **Author decides**: carry back, not yet, keep earlier, accept, or the author's own choice. Never decided by an agent. |
| **Temporal leak**             | Uses a fact whose as-of is later than the chapter's cutoff.                                     | **Fix**.                                                           |
| **Source leak**               | Uses a fact found only in a package of the same fandom that is not in the stack (§5.3).         | **Fix**.                                                           |
| **Erratum use**               | Relies on an erratum's value (§5.2), such as a corrected printing's, and no divergence covers it. | **Fix**: use the corrected text. An author who wants the erratum's version logs a divergence. |
| **Crossover leak**            | Uses bridge-only canon in a project whose stack does not include that universe.                 | **Fix**.                                                           |
| **Frame violation**           | A character knows something outside their own frame, or a trip breaks its mechanism's rules (§9.1). | **Fix**.                                                       |
| **Paradox**                   | A causal contradiction between frames, including a failed closure check (§9.1).                 | **Decide**: fix, or accept and record in `branches.md`.            |

Faithfulness and leak checks run against the **composite**: the stack, read at the
sync points, overridden by the ledgers. A story is never flagged for obeying a logged
divergence, its own or an earlier book's.

## 6.10 Fidelity

`setting.fidelity` in `project.yaml` tunes how the canon-keeper treats emergent
divergences:

| Value      | Behavior                                                                     |
| ---------- | ---------------------------------------------------------------------------- |
| `strict`   | Presume emergent divergences are mistakes; recommend fixing.                 |
| `flexible` | Allow minor forks; guard load-bearing canon.                                 |
| `au`       | Expect forks; concentrate on self-consistency and on declared intent.        |

## 6.11 The loop

```
canon-keeper classifies a problem (§6.9)
  fix class        → showrunner routes a fix to the owning agent, then re-check
  decide class     → a human decides (or the showrunner, under gates: none)
      mistake      → fix, then re-check
      intended     → worldbuilder (curator) logs it in divergences.md,
                     with its consequences
  divergence conflict → the author decides, under every gate policy (§6.6)
      keep         → nothing is logged; canon proceeds
      otherwise    → curator logs the author's choice; fallout becomes open consequences
  hidden canon     → the author decides, under every gate policy (§6.12)
      curator records the decision in the Hidden canon table;
      reveal early, and other that changes canon state, also log a divergence
  order inversion  → the author decides, under every gate policy (§6.8)
      reorder      → the author revises setting.order, the architect
                     revises the sync points to match, then re-check
      otherwise    → curator logs the author's choice in divergences.md;
                     its fallout becomes open consequences the author resolves
  theory conflict  → the author decides each claim, under every gate policy (§6.13)
      curator records the decisions in the Theory conflicts table, and logs
      the adoption of the kept and adapted claims as a divergence
  seam conflict    → the author decides, under every gate policy (§6.14)
      curator records the decision in the Seam conflicts table;
      keep earlier and other also log a divergence
then re-audit (retellings, §6.6):
  any divergence logged above → the canon-keeper re-runs the divergence audit
      for the canon still ahead; new conflicts go back to the author
then propagate:
  for each open consequence
    invalidates an already-written chapter? → schedule a revision of that chapter
      (serial, chapter released and locked → decide: absorb forward or accept, §13.3)
    otherwise                               → leave it open for later chapters to honor
  repeat until no consequence is open that an existing chapter should already reflect
```

A host MUST NOT advance past a chapter while a **decide** item for it is pending (§14).

## 6.12 Hidden canon: true before it is revealed

A **hidden truth** is a canon fact that is already true at the story's cutoff, but that
the source has not yet revealed (`True from` ≤ cutoff < `As of`, §4.4). Snape's love for
Lily is one throughout the early books. In a branch frozen at `PS:17` (§6.6) it is never
revealed at all.

Whether the story uses such a fact is the **author's** decision, raised at the point it
becomes relevant:

- **When it is raised.** The snapshot lists hidden truths for each entity (§7.2). When a
  chapter's beat touches one, the drafter marks it
  (`<!-- TODO: hidden canon: … -->`, §10.18) and drafts as if the fact were unknown. The
  canon-keeper raises the same in its audits and chapter reviews. Each fact is raised
  once per project; after a decision it is not raised again.
- **What the author can decide.** The author may choose any resolution. The common ones:

  | Decision        | What happens                                                                                        |
  | --------------- | --------------------------------------------------------------------------------------------------- |
  | **reveal early** | The story reveals the fact before canon does. The curator logs a divergence whose `Overrides` makes the fact visible from the chosen chapter. |
  | **keep hidden** | The story proceeds as if the fact were unknown, as canon does at that point. Nothing changes in the snapshot. |
  | **other**       | Anything else the author wants, such as subtext the reader can sense but no character states. Recorded with a note, and logged as a divergence if it changes canon state. |

- **Who decides.** Only the author, under every gate policy, as for order inversions and
  divergence conflicts (§11.8).
- **Where it is recorded.** The curator records every decision in the ledger's
  `## Hidden canon` table (§10.8), with the divergence it produced, if any. A decision
  binds later books that stack the project, as of their pin (§6.4).

## 6.13 Adopting a theory: theory conflicts

A theory (§10.13) is an interpretation: a set of numbered **claims**, with the evidence
for them. Its rows never resolve into the snapshot (§5.2). A project uses a theory by
**adopting** some or all of its claims, and adoption is a divergence like any other.

1. **The theories package is in the stack.** A project can adopt only a theory it can
   see (§2.2).
2. **The canon-keeper checks every claim** against the stack before anything is logged.
   Each piece of evidence that contradicts a claim is a **theory conflict** (§6.9). The
   canon-keeper lists evidence from **any** point:
   - **at or before the cutoff**, where the story's canon already contradicts the
     claim;
   - **after the cutoff**, where later canon contradicts it. A retelling will reach that
     point, and even a branch's author needs to know how well the theory holds up.

   Sources often contradict themselves, and a theory built on one passage can be
   contradicted by another. Old theories in particular may rest on evidence no one can
   now trace (§5.6). The canon-keeper reports the contradiction; it never decides which
   passage is right. Evidence that is an erratum (§5.2) is still evidence, but the
   canon-keeper says so: the claim then rests on text the source itself corrected.
3. **The author decides each conflicting claim**, under every gate policy, as for the
   other author-only decisions (§11.8):

   | Decision    | What happens                                                                         |
   | ----------- | ------------------------------------------------------------------------------------ |
   | **keep**    | The claim is adopted as it stands. If the contradicting evidence is at or before the cutoff, the adoption must also change that canon, through `Overrides` or its prose columns. |
   | **adapt**   | A changed claim is adopted. The change is recorded in the conflict's note.            |
   | **discard** | The claim is not adopted.                                                            |

   Claims with no conflict are adopted as proposed.
4. **The curator logs the result.** The decisions go in the ledger's `## Theory
   conflicts` table (§10.8), and bind later books along with the adoption (§6.4). The
   adoption is one divergence whose `Basis` lists every claim adopted (kept, adapted, or
   without conflict), and whose `Overrides` carries any claim that can be expressed as
   attribute values (otherwise `—`).

A discarded claim MUST NOT appear in any `Basis`, and a kept or adapted claim MUST. A
theory whose claims are all discarded is not adopted, and no divergence is logged.

*Example.* A fan theory holds that the Tale of the Three Brothers (DH ch.21) is about
the main cast: the eldest brother is Voldemort, the middle brother Snape, the youngest
Harry, and Death is Dumbledore. A short story set at King's Cross (cutoff `DH:36`)
adopts it. The canon-keeper finds two conflicts in *Deathly Hallows* ch.35. There it is
Dumbledore, not Snape, who once used the Resurrection Stone to try to reach his dead
(against claim 2), and Dumbledore himself once sought the Hallows, which the tale's
Death never does (against claim 4). The author discards claim 2 and adapts claim 4:
Dumbledore is Death as the tale's last page casts him, not throughout. The curator logs
`D1` with `Basis: harry-potter/theories:T1 (claims 1, 3, 4)`.

## 6.14 Where books meet: seam conflicts

A later book (§6.4) can be set after the earlier one, before it (a **prequel**), or
partly each (a **split frame**: some chapters after book 1, some before it). Comparing
settings cannot tell an intended prequel from a mistaken pin, and a split frame is both
at once. So wherever the books meet, the host raises the question and the author
decides.

**Anchors.** Everything an earlier book brings in was established somewhere in it. Its
**anchor** is the ruler point of that chapter in the earlier book: the earlier book's
cutoff at the chapter (§6.7), or, for a self-contained book, the point `<id>:<n>` of
the chapter (§4.12).

| Item                                                                 | Id                                       | Anchored at                  |
| -------------------------------------------------------------------- | ---------------------------------------- | ---------------------------- |
| A divergence                                                         | `<project>:D<n>`                         | its `First occurs`           |
| A story-dated row (§4.11)                                            | `<project>:<slug>.<attribute>@<chapter>` | its `From chapter`           |
| The starting state of an entity the earlier book defines: its timeless rows for one attribute | `<project>:<slug>.<attribute>` | `chapter-01` |

An earlier book's ruler-dated rows have no anchor: they are on the ruler already, and
the time filter places them (§7.2). Its decisions about hidden canon and theories
have none either. They bind as of the pin (§6.4), wherever the later
book's chapters are set.

**Items ahead.** At a chapter of the later book with cutoff `X`:

- An item anchored at or before `X` holds, as §6.4 says. A sequel set after the earlier
  book raises nothing.
- An item anchored after `X` is **ahead**: the chapter is set before the point where the
  earlier book established it. It does not hold until the author decides:

  | Decision       | What happens                                                                           |
  | -------------- | -------------------------------------------------------------------------------------- |
  | **carry back** | It holds at this chapter too: a description, a place, or a relationship that already existed before the earlier book. |
  | **not yet**    | It does not hold here. The later book may lead into it.                                |
  | **other**      | Anything else, recorded with a note, and logged as a divergence of the later book that sets it. |

**Value seams.** The later book may stack the world differently: an added package, a
newer minor version (§2.2), or another resolution mode or order. A canon attribute the
earlier book showed may then resolve differently at the same point. The canon-keeper's
**seam audit** compares each attribute of the entities the earlier book's manuscript
uses, as the earlier book resolved it at its pin, with what the later book's stack
gives at the same cutoff, and raises each difference, with the item
`<slug>.<attribute>`:

| Decision         | What happens                                                                         |
| ---------------- | ------------------------------------------------------------------------------------ |
| **keep earlier** | The later book logs a divergence restoring the earlier book's value.                 |
| **accept**       | The new value stands: a retcon, which the later book's readers may notice.           |
| **other**        | Anything else, recorded with a note, and logged as a divergence that sets it.        |

How seam conflicts are handled:

- **When they are raised.** The snapshot returns the undecided items ahead of a chapter
  separately (§7.2, step 8). The canon-keeper raises them, and the value seams, in the
  **seam audit** (§13.4, E1b), and again whenever the sync points or a layer's pin
  change. When a chapter's beat needs an undecided item, the drafter writes around it
  and marks it (`<!-- TODO: seam conflict: <item> -->`, §10.18). Each item is raised
  once per project; after a decision it is not raised again.
- **A wrong pin is not a seam.** If the later book's first chapter is set before the
  earlier book's cutoff at its pin, the seam audit says so before raising any item. The
  author then either fixes the pin or the sync points, or confirms that the book is
  set, in whole or in part, earlier, and the items are raised.
- **Patterns.** A decision may name a pattern, with `*` in place of a whole slug,
  attribute, chapter, or divergence number: `two-witnesses:mara-quill.*` (all of Mara's
  starting state), `lantern-road:*.*@*` (everything that happened during book 1),
  `two-witnesses:D*`. An exact item beats a pattern. Between patterns, the later row
  wins.
- **Split frames need nothing more.** A decision applies at every chapter where its item
  is ahead, and nowhere else. Chapters set after the earlier book raise nothing.
- **Who decides.** Only the author, under every gate policy (§11.8).
- **Where it is recorded.** The curator records every decision in the ledger's
  `## Seam conflicts` table (§10.8), with the divergence it produced, if any. A
  decision binds later books that stack the project, as of their pin (§6.4).

Two rules are not the author's to waive:

- **A branch stays a branch.** If a project layer is a branch (§6.6), the later book
  MUST be a branch too, with a divergence point no later than the layer's. Otherwise
  its chapters would see canon that the earlier book's world never has.
- **The order is inherited.** A later book that sets no `setting.order` uses the order
  of its highest project layer that has one. A later book that sets a different order
  runs the order audit (§6.8, §13.4 E1a), as any new order does.

*Example.* `lantern-road-before` stacks the self-contained `lantern-road` at
`chapter-12`, and is set on both sides of it: chapters 1 to 5 in `youth`, before book 1,
and chapter 6 on in `after`. Book 1 gives Ines grey eyes and makes her an apprentice
lamplighter from the start, and a master in chapter 9 (`lantern-road:9`). In chapters 1
to 5, every one of those items is ahead. The author carries back
`lantern-road:ines-varga.*`, her starting state, and decides `not-yet` for
`lantern-road:*.*@*`, everything that happens during book 1. So young Ines has grey
eyes and is an apprentice. From chapter 6 nothing is ahead: she is a master, and
nothing is raised.
