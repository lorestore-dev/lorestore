# 9. Optional modules

Modules are dormant unless a project enables them in `project.yaml`. A world package
MAY ship a module's world-layer files (`game-system.md`, `languages.md`) whether or not
a given project uses them.

| Module        | Enabled by                        | World-layer files            | Story-layer files              |
| ------------- | --------------------------------- | ---------------------------- | ------------------------------ |
| **Frames**    | `setting.temporal_model: frames`  | —                            | `timelines.md`, `branches.md`  |
| **LitRPG**    | `modules.litrpg: true`            | `game-system.md`             | `game-state.md`                |
| **Languages** | `modules.languages: true`         | `languages.md`, `lang/*.md`  | —                              |

## 9.1 Frames: time travel and parallel worlds

Frames separate two kinds of time:

- the **world frame**: where and when a scene happens, written
  `<canon-point>@<branch>` (for example `PoA:21@main`, or down to scene and timecode,
  `TNG:3:15:7+00:31:10@alt-war`);
- each traveler's **personal frame**: the cutoff they carry with them, which is how
  much they know.

`branches.md` registers world-lines (branches) and keeps the **paradox ledger**.
`timelines.md` records each traveler's legs: where they departed from, where they
arrived, and their personal cutoff on each leg (format: §10.16).

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
(§7.5). The canon-keeper checks **each character against their own frame**:

- A native who knows future or other-branch information is a **frame violation**.
- A traveler who knows something from after their departure is a **frame violation**.
- A causal contradiction between frames is a **paradox**, which is a decision: fix it,
  or accept it and record it in `branches.md` with a rationale (§6.9).

The chronicler (§12.11) maintains `timelines.md` and `branches.md`, including paradox
decisions made by a human or the showrunner.

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
