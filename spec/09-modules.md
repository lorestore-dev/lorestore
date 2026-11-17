# 9. Optional modules

Modules are dormant unless a project enables them in `project.yaml`. A package MAY
ship a module's world-layer files (`game-system.md`, `languages.md`, `routes.md`,
`mysteries.md`, `titles.md`) whether or not a given project uses them. A host
validates a module's files and reserved attributes wherever they appear. Agents read
them, and the host raises the module's warnings, only in a project that enables it.

| Module        | Enabled by                        | World-layer files            | Story-layer files              |
| ------------- | --------------------------------- | ---------------------------- | ------------------------------ |
| **Frames**    | `setting.temporal_model: frames`  | `time-travel.md`             | `timelines.md`, `branches.md`  |
| **LitRPG**    | `modules.litrpg: true`            | `game-system.md`             | `game-state.md`                |
| **Languages** | `modules.languages: true`         | `languages.md`, `lang/*.md`  | —                              |
| **Travel**    | `modules.travel: true`            | `routes.md`                  | — (a `Place` column in `timeline.md`) |
| **Mysteries** | `modules.mysteries: true`         | `mysteries.md`               | —                              |
| **Lineage**   | `modules.lineage: true`           | `titles.md`                  | —                              |

## 9.1 Frames: time travel and parallel worlds

Frames separate two kinds of time:

- the **world frame**: where and when a scene happens, written
  `<ruler-point>@<branch>` (for example `PoA:21@main`, or down to scene and timecode,
  `TNG:3:15:7+00:31:10@alt-war`);
- each traveler's **personal frame**: the cutoff they carry with them, which is how
  much they know.

Three files carry the module:

- `time-travel.md` (world layer) declares **how time travel works**: one entry per
  mechanism, with its model, reach, and limits (format: §10.24). It is canon like any
  other world rule. A base ships it when its canon has time travel. Any higher layer,
  including a project, MAY add mechanisms of its own, as new entries (§2.7).
- `branches.md` (story layer) registers world-lines (branches), with each one's status,
  and keeps the **paradox ledger**.
- `timelines.md` (story layer) records each traveler's legs: the mechanism used, where
  they departed from, where they arrived, and their personal cutoff on each leg. It also
  records **ripples** (below). Format: §10.16.

### Mechanisms and models

Fiction handles time travel in very different ways, and which checks make sense
depends on which way a story uses. Two questions separate the kinds:

1. **Was the traveler already there the first time history happened?** If so, history
   is self-consistent and travel cannot change it. If not, arriving in the past puts
   history on a new course.
2. **Whose actions can change history?** Everyone's; only the traveler's, while past
   selves replay exactly what they did before; or no one's.

Each mechanism in `time-travel.md` declares one **model**:

| Model       | History                                                                                         | Example                                                    | What the module does                                                                                                          |
| ----------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `dilation`  | One history. The traveler moves forward only, at a different rate from the world.               | A crew returns from near-light travel, having aged months while years passed at home | No branch. On arrival the traveler's personal cutoff lags behind the world point.                                |
| `fixed`     | One history, which always included the traveler.                                                | The Time-Turner in *Prisoner of Azkaban* (PoA ch.21)       | No branch. **Closure check:** what the traveler does in the overlap must match what the first pass showed.                   |
| `loop`      | The world resets to an anchor point. Only the traveler, and anything declared `immune`, remembers. | The Enterprise caught in a repeating loop (TNG "Cause and Effect") | Each iteration is a branch from the anchor. The last one continues; the rest are `abandoned`. Natives start each iteration fresh. |
| `mutable`   | Arriving or acting in the past **replaces** history from that point.                            | The Enterprise-C's trip through the rift (TNG "Yesterday's Enterprise") | The new history is a branch that replaces its parent, which becomes `overwritten`.                                 |
| `branching` | Arriving starts a new history. The old one carries on, untouched.                               | The Kelvin timeline (*Star Trek*, 2009)                    | The new history is a branch; its parent stays `live`. Nothing done on the new branch reaches the parent.                     |
| `feedback`  | As `mutable`, and what happens to a past self reaches the traveler at once: a wound becomes an old scar, an act becomes a memory. | A traveler whose younger self is changed in front of them | As `mutable`, plus **ripples**: dated changes to the traveler, recorded in `timelines.md`.                     |

A mechanism also declares **free will**: `everyone` (the default), `traveler` (past
selves replay their first pass exactly; only the traveler can depart from it), or
`none` (nobody can change anything, as in `fixed`). It declares what crosses with the
traveler (body, memory, objects) and any **limits**: how far it reaches, how long the
journey takes, or an earliest reachable point, such as a machine that cannot send anyone
back before it was first switched on.

A world can have several mechanisms with different models, and canon is not always
consistent between them. Each traveler leg names the mechanism it used, so each trip is
checked against its own rules.

**Ripples** (`feedback` only) are changes to a traveler that their past self causes:
each row records the traveler, the attribute, the new value, the world point that caused
it, and the chapter from which it applies. The traveler pass of the snapshot applies
them (§7.5). A ripple on a canon character changes a canon entity, so it is also a
divergence (§6.2), logged in the ledger as usual.

**Branches and versions are different things.** Star Trek shows both:

- A **branch** is a timeline that splits from another, such as the altered war timeline
  of "Yesterday's Enterprise" or the Kelvin timeline of the 2009 film. Branches go in
  `branches.md`, and scenes on them are written `<point>@<branch>`.
- A **version** is a canon-distinct instance of a character, such as the Mirror
  Universe's bearded Spock (TOS "Mirror, Mirror"). A version gets its own roster row and
  its own sheet, with `Version of: spock` (§10.9). It needs no frames module unless the
  story moves people between timelines.

A Time-Turner copy of Harry is neither: it is the same person at a different personal
time, and stays on one sheet.

Each scene in a frames project declares its world point and its travelers (§10.18). The
snapshot resolves natives at the world point and travelers at their personal cutoffs
(§7.5). The canon-keeper checks **each character against their own frame**, and each
trip against its mechanism:

- A native who knows future or other-branch information is a **frame violation**.
- A traveler who knows something from after their departure is a **frame violation**.
  A traveler's memories of a branch that has since been `overwritten` or `abandoned`
  are part of their own frame, and are not a violation.
- A trip the mechanism does not allow (beyond its reach, against its limits, or
  carrying what it cannot carry) is a **frame violation**.
- Under `fixed`, an overlap that does not match the first pass fails the closure check.
  Under free will `traveler`, a past self who acts differently from their first pass
  does too. Both are **paradoxes**.
- Any other causal contradiction between frames is a **paradox**, which is a decision:
  fix it, or accept it and record it in `branches.md` with a rationale (§6.9).

The chronicler (§12.11) maintains `timelines.md` and `branches.md`, including branch
statuses, ripples, and paradox decisions made by a human or the showrunner.

**Example cases:** [23](../examples/README.md#case-23).

## 9.2 LitRPG and GameLit

- `game-system.md` holds **the System's rules**: stats, levels, skills, inventory, and
  quests. It is a catalog, like `magic/` (§10.11).
- `game-state.md` holds **the protagonist's live state**, recorded per chapter and
  append-only (§10.17).

The continuity-editor checks the game state for consistency:

- **monotonic leveling**: no level goes backwards without a stated cause;
- **inventory balance**: no item appears from nowhere or disappears without trace;
- **quest progression**: quests move only forward through their stages;
- **stat arithmetic**: totals match their components.

How the game UI is rendered in prose (status windows, notifications) belongs in
`style.md`.

## 9.3 Languages and accents

- A **foreign accent in the default language** is dialect. It lives in the character's
  voice signature, with cast-wide conventions in `voice-guide.md`.
- An **actual other language** lives in `languages.md`: who speaks it, how it is
  **rendered** on the page (in-language, tagged, or described, which can depend on the
  POV character), and how it is **translated**.
- A **constructed language** gets a dictionary, `lang/<language>.md` (§10.12).

## 9.4 Travel

A story that moves its characters across a map can break its own geography: a journey
that takes a week in one chapter takes two days in another, or a character reaches a
town faster than any road allows. The travel module records how long journeys take, so
that, with in-world dates (§4.13), the time between two scenes can be checked against
the distance between their places.

- `places.md` already holds the places: one entity per place (§10.5).
- `routes.md` (world layer) holds the **routes** between them, and the **modes** of
  travel the world has (format: §10.26). A route is an entity, so it has a state
  history like any other: a bridge washes out, a railway opens, a Floo connection is
  made. Each of its attributes is a mode, and each value is a **duration**: how long
  that mode takes over that route.
- `timeline.md` gains an optional `Place` column: the place where each story event
  happens (§10.15).

A **duration** is a number and a unit, `min`, `h`, `d`, or `w`: `30min`, `9h`, `4d`. It
takes the same forms as a date (§4.13): a range (`4d..6d`), open at either end
(`..12h`), or approximate (`~8h`). `0` is instant. A day is 24 hours. A route's value
`—` means that the mode cannot make the journey at all: no Apparating into Hogwarts.
A mode with no row on a route is unknown, not impossible, and the check below leaves it
out.

**The check.** For each entity that `timeline.md` events list, the continuity-editor
takes the events that have both a `Date` and a `Place`, in date order. Where the place
changes between two consecutive events, the most time that can have passed (from the
start of the first date to the end of the second) MUST be at least the shortest journey
between the two places: the quickest path over the routes as they stand at the second
event's chapter, taking on each route its fastest known mode at the lower end of its
duration. A journey that is definitely too fast is a **warning** (§4.13), because the
story may mean it: a secret road, a magic the routes do not record.

- An approximate duration counts as instant, and so does a route with no known mode.
  A route on which every known mode is `—` cannot be used.
- It never warns where either date is approximate or open-ended, or where no path joins
  the two places.

**Example cases:** [M1](../examples/README.md#case-m1).

## 9.5 Mysteries

A mystery is a question the reader is invited to answer before the story does: who
the impostor is, why the lamps keep going out. The module records each mystery's
**clues**, where they are planted, and where the answer is revealed, so that a mystery
can be checked for **fair play**: every clue the reader needs is on the page before the
reveal.

- A mystery's answer is a **secret** (`knowledge.md`, §10.5). The secret's `Truth` is
  the solution, and its knowledge rows say which characters know it, and from when. The
  snapshot already keeps it from leaking (§7.3).
- `mysteries.md` (world layer) adds the mystery itself: its question, where the answer
  is revealed to the reader, and its clues (format: §10.27). A package records the
  canon's mysteries, and a project adds its own. The architect plans a project's clues
  in the outline and records them here; the chronicler moves a clue's `Planted at` if
  the chapter that plants it changes.
- A clue is **needed** if a reader must have it to reach the answer. A **red herring**
  points somewhere else, and is never needed.

**The checks.** Each is a warning, because a mystery may be unfair on purpose:

- a needed clue planted at or after the reveal;
- a mystery with no needed clue before its reveal;
- in an established project, a project order (§6.8) or a divergence that moves a
  canon mystery's needed clue to after its reveal, or removes it. The canon-keeper
  raises it in its audit.

The drafter MUST NOT let the narration answer a mystery before its `Revealed at`,
even where a viewpoint character already knows the answer.

**Example cases:** [M2](../examples/README.md#case-m2).

## 9.6 Lineage

Relationships are pairwise (§10.5), so they cannot hold a family tree, a dynasty, or a
line of succession. The lineage module adds three reserved attributes to any entity's
state history, and a file of titles:

- `parents`: the entity's birth parents, as slugs separated by `; `;
- `guardians`: those who raise it, if not its parents, in the same form;
- `descends-from`: distant ancestors, when the generations between are unknown (the
  Gaunts, from Salazar Slytherin);
- `titles.md` (world layer, format §10.28): offices and titles that pass from one
  holder to the next, each an entity whose `holder` attribute names the current holder
  and whose `rule` says, in free text, how it passes on.

They are ordinary attributes, so everything else applies unchanged. Parentage is
visible from its `As of`, which keeps a parentage reveal from leaking. A later row can
correct a belief that a story has overturned. A project changes canon parentage
through the ledger (§6.4). Each value MUST name a slug in the stack's roster (§10.9).

**Chronology contradictions.** With in-world dates (§4.13), two more checks join
those of §4.13, and an `## Accepted` row can excuse them in the same way:

| Check                | Fails when                                                                                     |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| `born-before-parent` | An entity's `born` is definitely before the `born` of one of its `parents` or `descends-from` ancestors |
| `ancestry-cycle`     | Following `parents` and `descends-from` leads back to the entity itself                        |

A time traveller who becomes their own grandparent is both, on purpose. `ancestry-cycle`
needs no dates, so it applies in every world. Its subject is any one of the `parents`
or `descends-from` rows on the cycle: one acceptance excuses the whole cycle.

**Warnings**, raised by the continuity-editor:

- a parent definitely younger than 12 at the child's `born`;
- a child born definitely more than a year after a birth parent's `died`;
- a title's `holder` row dated (by the date of its `As of` point) definitely before the
  holder's `born` or after their `died`.

A family tree is a view, never stored: start from an entity and follow `parents` and
`descends-from` at a cutoff, which shows only the parentage a reader knows by then.

**Example cases:** [M3](../examples/README.md#case-m3).
