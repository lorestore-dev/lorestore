# 9. Optional modules

Modules are dormant unless a project enables them in `project.yaml`. A world package
MAY ship a module's world-layer files (`game-system.md`, `languages.md`) whether or not
a given project uses them.

| Module        | Enabled by                        | World-layer files            | Story-layer files              |
| ------------- | --------------------------------- | ---------------------------- | ------------------------------ |
| **Frames**    | `setting.temporal_model: frames`  | `time-travel.md`             | `timelines.md`, `branches.md`  |
| **LitRPG**    | `modules.litrpg: true`            | `game-system.md`             | `game-state.md`                |
| **Languages** | `modules.languages: true`         | `languages.md`, `lang/*.md`  | —                              |

## 9.1 Frames: time travel and parallel worlds

Frames separate two kinds of time:

- the **world frame**: where and when a scene happens, written
  `<canon-point>@<branch>` (for example `PoA:21@main`, or down to scene and timecode,
  `TNG:3:15:7+00:31:10@alt-war`);
- each traveler's **personal frame**: the cutoff they carry with them, which is how
  much they know.

Three files carry the module:

- `time-travel.md` (world layer) declares **how time travel works**: one entry per
  mechanism, with its model, reach, and limits (format: §10.25). It is canon like any
  other world rule. A world package ships it when its canon has time travel, and a
  self-contained project writes its own.
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

Each scene in a frames project declares its world point and its travelers (§10.19). The
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

## 9.2 LitRPG and GameLit

- `game-system.md` holds **the System's rules**: stats, levels, skills, inventory, and
  quests. It is a catalog, like `magic/` (§10.11).
- `game-state.md` holds **the protagonist's live state**, recorded per chapter and
  append-only (§10.18).

The continuity-editor checks the game state for consistency:

- **monotonic levelling**: no level goes backwards without a stated cause;
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
