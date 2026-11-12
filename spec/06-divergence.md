# 6. Divergence: the living-canon mechanism

A story set in an established world forks from canon. The fork is **recorded in the
project's story layer**, never by editing the world (§3.1, W3). The manuscript obeys:

> **Source canon, read along the project's canon track, overridden by the divergence
> ledger.**

Three story-layer files carry this: the adherence contract and the ledger, written by
the worldbuilder in curator mode (§12.7), and the canon track, written by the architect
(§12.6).

## 6.1 When this applies

This chapter applies to projects with `setting.type: established`: any project set in a
world it did not invent, whether the world comes from a world package, a universe, or
only from `references/`. A self-contained original project has nothing to diverge from.

## 6.2 What counts as a divergence

A divergence is **any difference between the state of a canon entity in this story and
its state in canon**, at the same point in the story. That includes:

- **Changes**: canon says one thing, and the story says another (Cedric survives).
- **Additions to canon entities**: canon is silent, and the story adds something.
  If Harry gains a burn scar on his left hand in an original scene, that is a
  divergence, even if the plot then follows canon exactly. Harry is now physically
  different from canon Harry, and every later chapter must honour it.
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

## 6.3 `canon.md`: the adherence contract

`bible/canon.md` states how this story relates to its source:

- **Canon in scope**: which works, characters, and systems the story leans on, with
  pointers into the world layer (not copies of it).
- **Point of divergence**: the canon point where the story departs, if it departs. It
  restates `setting.divergence_point`, which is the machine-readable value (§6.6).
- **Original additions**: the new entities the story introduces (§6.2).
- **Fidelity**: restates `setting.fidelity` (§6.10) and any project-specific latitude.

For a project with only `references/` and no world package, `canon.md` also holds the
curated canon facts themselves, since there is no world layer to point at.

## 6.4 `divergences.md`: the ledger

The ledger has two tables (format: §10.8).

**Divergences**

```
| ID | Canon establishes                          | This story changes it to          | Overrides                                         | Kind     | First occurs |
| -- | ------------------------------------------ | --------------------------------- | ------------------------------------------------- | -------- | ------------ |
| D1 | Cedric is killed in the graveyard (GoF:32) | Cedric survives, badly injured    | cedric-diggory.status=alive                       | planned  | chapter-01   |
| D2 | (OC) Mara has no magical lineage           | Mara is a half-blood              | mara-quill.blood-status=half-blood                | emergent | chapter-07   |
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

**Consequences**

```
| Divergence | Consequence                                                                     | Status   | Absorbed in |
| ---------- | ------------------------------------------------------------------------------- | -------- | ----------- |
| D1         | Cedric is a living witness to Voldemort's return; the Ministry cannot dismiss two witnesses so easily | open |  |
| D1         | Cho and Cedric's relationship continues                                         | absorbed | chapter-04  |
| D3         | Every later scene that shows Harry's hands must show the burn                   | open     |             |
```

Every divergence MUST list at least one consequence, or a single row stating `none`
with a reason.

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
5. **The ledger is the only route to changing canon state.** No agent may edit the
   world, or restate canon differently in `canon.md`, to achieve a fork.

## 6.6 Branch or retelling: how strictly later canon binds

A divergence changes canon at some point. The project must also say what happens to
the canon that comes **after** that point. `setting.canon_mode` sets this, and
`setting.divergence_point` names the point (§10.1).

| `canon_mode`               | Canon after the divergence point                                                            | Example                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `retelling` *(the default)* | **Still happens**, by default, as the story moves along the canon track. Divergences change it only where they reach. | Harry is blinded by the curse at Godric's Hollow. The canon storyline still unfolds, and the story is how he meets it. |
| `branch`                   | **Never happens.** Canon is frozen at the divergence point, and from there the story writes its own. | There are no Horcruxes, so when Harry defeats Voldemort at the end of *Philosopher's Stone*, Voldemort dies. Most of later canon can no longer occur. |

### Branch

- **The cutoff stops at the divergence point.** The snapshot never resolves past it
  (§7.1), and the canon track MUST NOT advance beyond it (§6.7). Canon dated later
  never becomes visible, however far the story runs, and using it is a temporal leak.
- **From the divergence point on, the story is its own canon.** Changes the story makes
  to canon entities are still divergences (§6.2), usually with `Canon establishes` set
  to `(silent)`. Over time the ledger becomes the record of the branch's own history.
- **Checks narrow.** The canon-keeper checks faithfulness only against canon up to the
  divergence point, and self-consistency everywhere. An event that differs from later
  canon is not a divergence, because later canon does not apply.

### Retelling

- **Later canon is the default script.** The canon track advances the cutoff (§6.7), and
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

`fidelity` and `canon_mode` are independent. `canon_mode` decides whether later canon
applies at all. `fidelity` decides how strictly unplanned departures from the canon
that does apply are judged.

## 6.7 Following canon: the canon track

A long story often **keeps following canon** while it adds to it. A fanfic can run
alongside the books from first year to seventh, adding scenes and characters along the
way. Its cutoff cannot be one fixed point: what Harry knows in chapter 40 is not what he
knows in chapter 1.

The **canon track** (`bible/canon-track.md`, format §10.22) maps manuscript chapters to
cutoffs:

```
## Track
| From chapter | Cutoff  |
| ------------ | ------- |
| chapter-01   | PS:6    |
| chapter-08   | PS:17   |
| chapter-12   | CoS:1   |
```

- The cutoff for a chapter is the row with the latest `From chapter` at or before it.
  Before the first row, and in projects with no track, `setting.canon_point` applies.
- A universe project adds a `World` column after `Cutoff`, and tracks each world
  separately.
- Cutoffs SHOULD advance through the story. A host SHOULD warn when a later row's
  cutoff is earlier, which is legitimate only for a deliberate jump back, such as a
  flashback.
- In a **branch**, no track cutoff may be later than `setting.divergence_point` (§6.6).
- The track says **where in canon** each chapter sits. What the story **changes** is
  still the ledger's job: additions and changes made while following canon are
  divergences (§6.2).

## 6.8 Rearranging canon

A story can also **change the order** in which canon happens. For example, a fanfic
might move the Triwizard Tournament from fourth year to second year. The original
*Chamber of Secrets* then becomes year three, and *Prisoner of Azkaban* year four. Harry
has not met Sirius during the Tournament, because in this story the events of *Prisoner
of Azkaban* have not happened yet.

The canon track holds the project's own **order** of the world's ruler segments (§4.1):

```
## Order
| Order | Segment |
| ----- | ------- |
| 1     | PS      |
| 2     | GoF     |
| 3     | CoS     |
| 4     | PoA     |
| 5     | OotP    |
| 6     | HBP     |
| 7     | DH      |
```

Rules:

1. **A permutation of the segments.** The project order MUST list every one of the
   world's segments exactly once. Leaving canon out is a removal, logged as a divergence,
   not an omission from the order. Moving something smaller than a segment requires the
   world's ruler to have finer segments.
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
5. **The author decides every inversion.** An inversion is a story problem, not a
   bookkeeping one, and only the author can say how the story handles it. The
   canon-keeper flags each one and sets out options, each with its likely fallout
   (§10.20). The author chooses one of them, or something else entirely:

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
| **Temporal leak**             | Uses a fact whose as-of is later than the chapter's cutoff.                                     | **Fix**.                                                           |
| **Source leak**               | Uses a fact found only in a source outside the active profile, or in an excluded source.        | **Fix**.                                                           |
| **Crossover leak**            | Uses bridge-only canon in a project not set in that universe.                                   | **Fix**.                                                           |
| **Frame violation**           | A character knows something outside their own frame (§9.1).                                     | **Fix**.                                                           |
| **Paradox**                   | A causal contradiction between frames (§9.1).                                                   | **Decide**: fix, or accept and record in `branches.md`.            |

Faithfulness and leak checks run against the **composite**: source canon, read along the
canon track, overridden by the ledger. A story is never flagged for obeying its own
logged divergence.

## 6.10 Fidelity

`setting.fidelity` in `project.yaml` tunes how the canon-keeper treats emergent
divergences:

| Value      | Behaviour                                                                    |
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
      reveal early also logs a divergence
  order inversion  → the author decides, under every gate policy (§6.8)
      reorder      → architect revises the project order, then re-check
      otherwise    → curator logs the author's choice in divergences.md;
                     its fallout becomes open consequences the author resolves
then propagate:
  for each open consequence
    invalidates an already-written chapter? → schedule a revision of that chapter
      (serial, chapter released and locked → decide: absorb forward or accept, §13.3)
    otherwise                               → leave it open for later chapters to honour
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
  (`<!-- TODO: hidden canon: … -->`, §10.19) and drafts as if the fact were unknown. The
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
  `## Hidden canon` table (§10.8), with the divergence it produced, if any.

