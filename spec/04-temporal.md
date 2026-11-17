# 4. The temporal model

Facts extracted from source media are **stateful over the source timeline**. Harry
sleeps in the cupboard under the stairs, then in Dudley's second bedroom. Picard is a
starship captain, then Locutus of Borg, then a captain again. The world layer records
such facts as **append-only state histories**, each row dated against the ruler.

## 4.1 The ruler

A base's `canon-timeline.md` is the **ruler**. It describes the source material as a
**tree** (works divided into seasons, episodes, chapters, scenes) and fixes the
**order** in which that tree is read. Its format is in §10.4. It has three tables. Only
a base has a ruler: every package that relies on the base, and every project that
stacks it, dates its rows on the base's ruler (§2.3). The one exception is a series
begun by a self-contained book, whose ruler is built from the book itself (§4.12).

**Works** lists each top-level work, the levels it divides into, and which level, if
any, is continuous video or audio that a timecode can point into:

```
| Work | Title                         | Levels                   | Timed level | Notes |
| ---- | ----------------------------- | ------------------------ | ----------- | ----- |
| PS   | Philosopher's Stone           | chapter › scene          |             |       |
| TOS  | The Original Series           | season › episode › scene | episode     |       |
| TMP  | Star Trek: The Motion Picture | scene                    | work        |       |
| TNG  | The Next Generation           | season › episode › scene | episode     |       |
```

**Order** lists **segments**: nodes of the tree, in reading order. A segment can be a
whole work (a novel, a film) or any node inside one (a season), so series can be
interleaved with each other and with films:

```
| Order | Segment | Title                         | Children | Notes                       |
| ----- | ------- | ----------------------------- | -------- | --------------------------- |
| 1     | TOS:1   | The Original Series, season 1 | 29       | Episodes in broadcast order |
| 2     | TOS:2   | The Original Series, season 2 | 26       |                             |
| 3     | TOS:3   | The Original Series, season 3 | 24       |                             |
| 4     | TMP     | Star Trek: The Motion Picture |          | Released 1979               |
| 5     | TNG:1   | The Next Generation, season 1 | —        | Not divided                 |
| 6     | TNG:2   | The Next Generation, season 2 | 22       |                             |
```

**Counts** (optional) gives the number of children of nodes below the segments, for
example how many scenes the world's extraction divides an episode into:

```
| Node    | Children |
| ------- | -------- |
| TOS:3:2 | 14       |
```

`Children`, in both tables, is the number of children a node divides into at the next
level (the episodes of a season, the scenes of an episode):

| `Children`  | Meaning                                                                         |
| ----------- | ------------------------------------------------------------------------------- |
| an integer  | **Counted**: children `1 … Children` exist.                                     |
| empty       | **Uncounted**: the node is divided, but any positive index is valid.            |
| `—`         | **Undivided**: no point below this node is valid.                               |

A node the ruler gives no count for is uncounted, down to the work's last level.

Segment rules:

- No segment may lie inside another (neither may be a prefix of the other).
- A point is valid only if it lies inside a segment, or contains one (§4.2). Everything
  a world can date must therefore be covered by its segments.

The order is an **editorial choice**, made once per base. Broadcast or release order is
usually best, because it matches what someone following the source could know at each
point. In-universe chronology is recorded as in-world dates (§4.13), never by the
ruler's order.

Where series overlap, their segments interleave. *Deep Space Nine* premiered midway
through the sixth season of *The Next Generation*. **Season-level** segments give an
approximation:

```
| Order | Segment | Title                         | Children | Notes                          |
| ----- | ------- | ----------------------------- | -------- | ------------------------------ |
| 9     | TNG:6   | The Next Generation, season 6 | 26       |                                |
| 10    | DS9:1   | Deep Space Nine, season 1     | 19       | "Emissary" counted as one      |
| 11    | TNG:7   | The Next Generation, season 7 | 25       | "All Good Things…" as one      |
| 12    | DS9:2   | Deep Space Nine, season 2     | 26       |                                |
```

This places all of TNG season 6 before DS9's premiere, so a project set late in TNG
season 6 cannot see DS9 episodes that had already aired. **Episode-level** segments give
the exact broadcast order. Each episode in the overlap becomes its own segment, because
a segment is a single node and cannot be a run of episodes. Seasons outside the overlap
stay whole:

```
| Order | Segment  | Title                       | Children | Notes                      |
| ----- | -------- | --------------------------- | -------- | -------------------------- |
| 9     | TNG:6:1  | "Time's Arrow, Part II"     |          | TNG:6 is split by episode  |
| …     | …        | …                           |          |                            |
| 19    | TNG:6:11 | "Chain of Command, Part II" |          | Aired 19 Dec 1992          |
| 20    | DS9:1:1  | "Emissary"                  |          | Aired 3 Jan 1993           |
| 21    | DS9:1:2  | "Past Prologue"             |          | Aired 10 Jan 1993          |
| 22    | DS9:1:3  | "A Man Alone"               |          | Aired 17 Jan 1993          |
| 23    | TNG:6:12 | "Ship in a Bottle"          |          | Aired 23 Jan 1993          |
| …     | …        | …                           |          | Merged by first air date   |
```

Episode numbering is itself an editorial choice. Sources disagree on whether a
feature-length premiere or finale is one episode or two, so the world records its
choice (here, in `Notes`) and numbers consistently from then on.

Splitting is local. A world can start with season-level segments and later split only
the seasons where precision matters. Splitting a segment reorders the ruler, so it is a
major version bump (§2.8).

## 4.2 Ruler points

A **ruler point** is a path down the ruler's tree, optionally ending in a timecode:

```
point    = work { ":" index } [ "+" timecode ]
index    = positive integer
timecode = HH ":" MM ":" SS [ "." fraction ]
```

| Point                 | Meaning                                                              |
| --------------------- | -------------------------------------------------------------------- |
| `PS`                  | *Philosopher's Stone* as a whole, positioned at its **start**        |
| `PS:6`                | Chapter 6                                                            |
| `PS:6:2`              | Scene 2 of chapter 6                                                 |
| `TOS`                 | *The Original Series* as a whole, positioned at its start            |
| `TOS:3`               | Season 3                                                             |
| `TOS:3:2`             | Season 3, episode 2                                                  |
| `TOS:3:2:14`          | Scene 14 of that episode                                             |
| `TOS:3:2:14+00:12:31` | 12 minutes 31 seconds into that episode, in scene 14                 |
| `TMP+01:10:05`        | 1 hour 10 minutes 5 seconds into the film                            |

**Timecodes** are measured from the start of the **timed node**: the node at the work's
timed level that the point passes through (the episode, or the film). They are not
measured from the start of the scene. A timecode is allowed only when the path reaches
the timed level, or when an adaptation in the stack covers the path (§4.9). Fractional
seconds are allowed. Frame numbers are not used, because
frame rates vary between releases.

**Scenes** are rarely numbered by the source itself, so the scene level is the world's
own breakdown, made during extraction. A **scene** is a stretch of continuous action. A
new scene starts at a dramatic shift in any of:

- **location**: the action cuts to somewhere else;
- **time**: a jump forward or back, rather than continuous time;
- **circumstance**: the situation the characters are in changes, even when place and
  time run on unbroken.

Following a character continuously from one room to another is one scene. Cross-cutting
between places that are linked within one exchange is also one scene. In Star Trek, for
example, an away team on a planet and the bridge talking by communicator form one scene
for as long as the exchange lasts. When the link ends, the circumstance has changed and a
new scene starts. In prose, the author's section breaks are the default scene breaks; a
section that contains a dramatic shift is split there.

The extraction pipeline MUST number scenes consistently within a world, and MAY record
the counts in the Counts table.

A point is **valid** if:

1. its work is on the stack's ruler: in the Works table of the base, or of an official
   or fanfic package in the stack that inserts it (§4.10); or, in a series begun by a
   self-contained book, the work of a project layer, or a work that a project layer or
   the project itself inserts (§4.12);
2. it has no more indices than the work has levels;
3. it lies inside exactly one segment, or contains at least one;
4. each index is within its parent's count where that count is known, and no index
   falls below an undivided (`—`) node;
5. any timecode follows a path that reaches the timed level, or is an adaptation
   timecode on a path an adaptation in the stack covers (§4.9), and has minutes and
   seconds below 60.

A host MUST flag an invalid point. A point naming a work or segment the ruler lacks is a
typo or a missing ruler row, never an implicit new work.

### Ordering

1. **A point inside a segment** is placed at that segment's `Order`. Among points in the
   same segment, compare the indices below the segment one by one. A shorter path (the
   containing node) sorts **before** the nodes it contains.
2. **A point that contains segments** (a whole series when the segments are its
   seasons) sorts at the start of its earliest segment, before that segment's own point.
   Nested containers sort outermost first.
3. **Within one timed node**, if both points have timecodes, they compare by timecode.
   Otherwise they compare by index as in rule 1, and with equal indices the point
   without a timecode sorts first.
4. **Incomparable points.** In the same timed node, a point with only a timecode
   (`TOS:3:2+00:12:31`) and a point with only a scene (`TOS:3:2:14`) cannot be ordered
   without knowing when the scene starts. A host MUST report such a pair rather than
   guess. Extractors giving a timecode SHOULD also give the scene
   (`TOS:3:2:14+00:12:31`). A host SHOULD warn when timecodes contradict scene order.

So:

```
PS < PS:1 < PS:6 < PS:6:2 < PS:7 < PS:17 < CoS < CoS:1
TOS < TOS:1 < TOS:1:29 < TOS:3:2 < TOS:3:2:14 < TOS:3:2:14+00:12:31 < TOS:3:2:15
    < TMP < TMP+01:10:05 < TNG < TNG:1 < TNG:2 < TNG:2:16
```

Ruler points are comparable **only within one base**. Points from different bases are
related only through a universe's offsets (§8).

A project that rearranges canon supplies its own order of the same segments,
`setting.order` (§6.8). Within that project, rules 1–4 apply with each segment's place
in that list in place of the ruler's `Order`.

### The whole-node rule

A point that names a node (a work, a season, an episode, a chapter) is positioned at
the node's **start**, so a row dated at that node is visible throughout it. An extractor
MUST date a fact at a node only if the fact holds from the node's opening. A fact
established partway through MUST carry the finest point at which it is established.
Otherwise an end-of-book reveal leaks into chapter 1, or a season finale leaks into
its premiere.

When the ruler cannot express that point (the work is undivided), the fact is dated at
the **next** node from whose opening it holds. For example, with `TNG:1` undivided, a
death late in season 1 is dated `TNG:2`.

**Example cases:** [8](../examples/README.md#case-8), [9](../examples/README.md#case-9), [11](../examples/README.md#case-11).

## 4.3 The point list

Read as a list, the ruler yields every ruler point a world can offer for picking, in
ruler order:

```
PS · PS:1 · PS:2 … PS:17 · CoS · CoS:1 … CoS:18 · PoA · PoA:1 …
TOS · TOS:1 · TOS:1:1 … TOS:1:29 · TOS:2 … TMP · TNG · TNG:1 · TNG:2 · TNG:2:1 …
```

- Walk the segments in `Order`. Before each segment, list any containing nodes not yet
  listed (the work, then intermediate levels), then the segment, then its counted
  children, recursively, as far down as counts are known.
- An uncounted level contributes nothing: those points are typed, not picked. The same
  goes for timecodes.
- The list is **derived, never stored**. Editing the ruler changes it.

Wherever a user chooses a ruler point (a project's cutoff, a row's as-of), a host
SHOULD offer the point list rather than free text, presented as a tree (work, then
season, then episode) when it is long (§14).

## 4.4 State histories

A state history is a table of rows, each giving an attribute's value from a ruler point
on. The full row format, with the entity column used in multi-entity files, is in
§10.5:

Harry Potter (`characters/harry-potter.md`):

```
| Attribute | Value                                     | As of  | Source | Citation                                 |
| --------- | ----------------------------------------- | ------ | ------ | ---------------------------------------- |
| residence | cupboard under the stairs, 4 Privet Drive | PS:2   | books  | PS ch.2                                  |
| residence | Dudley's second bedroom                   | PS:3   | books  | PS ch.3                                  |
| broom     | Nimbus Two Thousand                       | PS:10  | books  | PS ch.10                                 |
| broom     | (unset)                                   | PoA:9  | books  | PoA ch.9, destroyed by the Whomping Willow |
| broom     | Firebolt                                  | PoA:11 | books  | PoA ch.11                                |
```

Jean-Luc Picard (`characters/jean-luc-picard.md`):

```
| Attribute | Value                           | As of   | Source | Citation                            |
| --------- | ------------------------------- | ------- | ------ | ----------------------------------- |
| status    | captain of the USS Enterprise-D | TNG     | canon  | TNG "Encounter at Farpoint"         |
| status    | assimilated as Locutus of Borg  | TNG:3:26 | canon  | TNG "The Best of Both Worlds, Part I"  |
| status    | captain of the USS Enterprise-D | TNG:4:1  | canon  | TNG "The Best of Both Worlds, Part II" |
```

Rules:

- **Append-only over canon time.** A change is a new row at a later point. The earlier
  row stays: it is true for the span before the change.
- **Every row is dated** with a valid ruler point (§4.2), except a timeless row
  (empty `As of`): a row of a self-contained world with no ruler (§4.7), or a row of a
  project's own entity (§10.5). A story-dated row (§4.11) is timeless on the ruler, and
  dated by its `From chapter` instead.
- **Every row has a source** registered in its own package's `sources.md` (§5) and a
  **citation** that locates the evidence.
- **One value per attribute, tier, and point.** Two rows in one package with the same
  entity, attribute, tier, and as-of but different values are a conflict, whether
  they cite one source or two. The merger MUST flag them rather than write both, and a
  human settles them at extraction (§12.4). A package records one intended value:
  - **an error the source itself corrected** is an erratum (§5.2): the corrected text
    is the row, and the error is kept under an `erratum` source;
  - **fan conventions** are recorded as the consensus: the value most fan works use;
  - **a deliberate revision**, such as an author's revised edition or a recut film,
    is a separate package, which a project chooses by stacking it (§2.3).
- **Rows are ordered by as-of** within each attribute. File order carries no meaning
  beyond that.

### True from

`As of` records when the source **establishes** a fact: when a reader could first know
it. Some facts were true long before that. Snape's love for Lily is true throughout the
series, but the books reveal it only in *Deathly Hallows*. An optional `True from`
column, after `Citation`, records when a fact became **true** in-world:

```
| Attribute | Value                                     | As of | Source | Citation  | True from |
| --------- | ----------------------------------------- | ----- | ------ | --------- | --------- |
| loyalty   | loves Lily Potter; protects Harry for her | DH:33 | books  | DH ch.33  | PS        |
```

- `True from` MUST NOT be later than `As of`. Empty means the same as `As of`.
- A fact true from before canon begins uses the first work's own point (`PS`), which
  sorts at the very start of canon. When it became true in-world, if the source says,
  goes in the `In-world` column (§4.13).
- **`As of` still governs visibility.** The snapshot resolves a row only once its
  `As of` is reached. `True from` does not reveal anything early. It lets the system
  recognize a **hidden truth**: a fact that is already true at the cutoff but not yet
  revealed (§7.2, §6.12).
- Extractors SHOULD record `True from` whenever a source reveals backstory, even if no
  current project needs it. It is cheap to record and impossible to reconstruct later.

**Example cases:** [1](../examples/README.md#case-1), [21](../examples/README.md#case-21), [E1](../examples/README.md#case-e1).

## 4.5 Ending a fact

To record that an attribute stops holding (a character dies and loses an office, an
item is lost, a scar heals completely), append a row whose value is the reserved token
`(unset)`. From that point the attribute resolves to absent (§7). A later row MAY set it
again.

**Example cases:** [2](../examples/README.md#case-2).

## 4.6 Corrections

Append-only governs **canon time**, not editorial correction. If a row is wrong (a
misread passage, a bad citation, a value the source never states), the extraction
pipeline fixes or removes the row itself and bumps the package's patch version (§2.8).
It MUST NOT "correct" a wrong row by appending a later row, because that would assert a
change the source never made.

## 4.7 Self-contained worlds without a ruler

A self-contained original world has no source works, so it MAY omit the ruler. Its state
rows then leave `As of` empty, meaning **timeless**: always visible. Change during the
story is recorded as story-time events in `timeline.md` and, for the state of its
entities, as story-dated rows (§4.11). A self-contained world that needs dated backstory
(eras, a prior war) SHOULD declare a calendar and record its past in `history.md`
(§4.13). It MAY instead, or as well, define a ruler whose works are eras; all rules in
this chapter then apply. The book's own chapters are set after every era, so its cutoff is the end of
that ruler (§7.1): every era row is visible, and it has no `setting.cutoff` and no sync
points.

## 4.8 Facts are self-dating

Every extracted fact carries its own ruler point, so its place on the timeline never
depends on the order in which it was extracted. Source units can be extracted in any order,
including in parallel, and the merger assembles history by **sorting on ruler point**
(§13.6). Sequential extraction is the one-worker case of the same pipeline and gives the
same result.

## 4.9 Adaptations: base points with the adaptation's timecode

An adaptation (§2.3) retells the base in another medium: films of novels, a TV series of
a comic. It does not get a ruler of its own. Its rows are dated on the **base's**
ruler, so that a project's cutoff stays one point on one ruler, and an adaptation's
facts compare directly with the base's.

The adaptation's `canon-timeline.md` (§10.4) lists its own **works**, each timed at the
work level, and an **Adapts** table mapping each work to the range of base nodes it
covers:

```
## Adapts
| Work     | From    | To      | Notes                                                  |
| -------- | ------- | ------- | ------------------------------------------------------ |
| PS-film  | PS:1    | PS:17   |                                                        |
| DH1-film | DH:1    | DH:24:1 | Ends with Dobby's burial                               |
| DH1-film | DH:24:6 | DH:24:6 | Then Voldemort taking the Elder Wand, the film's last scene |
| DH2-film | DH:24:2 | DH:24:5 | Opens at Dobby's grave: Griphook, Ollivander           |
| DH2-film | DH:25   | DH:36   |                                                        |
```

The *Deathly Hallows* films split chapter 24 out of order. In the book, Harry's vision
of Voldemort opening Dumbledore's tomb and taking the Elder Wand is the chapter's last
scene, after the burial and the talks with Griphook and Ollivander. Part 1 ends with
the burial and then the tomb; Part 2 opens at the grave and goes on to Griphook and
Ollivander. A work that takes scenes out of the book's order has one `Adapts` row per
contiguous range. (The table assumes an extraction that divides chapter 24 into six
scenes, the first the arrival and burial and the last the vision; the scene level is
always the extraction's own, §4.2.)

A row can then carry the base path **and** a timecode into the film that adapts it, the
way a TV point carries `series:season:episode:scene+timecode`:

```
PS:6:2+00:41:10      book scene PS:6:2, 41 minutes 10 seconds into the film that adapts it
```

- **The timecode belongs to the adaptation's work** that covers the path in the Adapts
  table. A path covered by more than one work (a book chapter split across two films)
  needs a scene-level path, so that each scene falls in only one work's range.
- **The base path decides the order.** An adaptation timecode orders only rows at
  exactly the same path; it never moves a row past another path. Films reorder scenes
  freely, and the base's order is the one every layer shares: a row from the end of
  *Deathly Hallows Part 1* at `DH:24:6` sorts after the *Part 2* rows at `DH:24:2`.
- **At the same path**, a row without a timecode sorts before one with a timecode, and
  timecodes compare as numbers.
- **Valid only with the adaptation in the stack.** An adaptation timecode on a path no
  adaptation in the stack covers is an invalid point (§4.2, rule 5).
- **Adaptation-only material** (a scene the films invent) is dated at the base path it
  sits beside, with a timecode, and cites the adaptation.

*Example.* With `harry-potter/films` in the stack, `PS:6:2+00:41:10` sorts after
`PS:6:2` and before `PS:6:2+00:42:00`, and `PS:6:3+00:10:00` sorts after
`PS:6:2+00:50:00`, because the book path decides. Without the films package, all four
points are invalid except `PS:6:2`.

**Example cases:** [A1](../examples/README.md#case-a1).

## 4.10 Inserted works

An `official` or `fanfic` package (§2.3) MAY have works of its own that retell nothing
in the base but sit beside it in canon time: an official animated series or line of
novels, or a fan work set between the base's works or after them. They need places on
the ruler, but the ruler belongs to the base, which MUST NOT change to suit a package
that some projects leave out. So the package **inserts** segments into the base's
ruler. No other kind inserts: an adaptation retells the base's own works, so its
material is dated on their paths (§4.9), and fanon and theories have no works.

The package's `canon-timeline.md` (§10.4) lists its works in a `## Works` table, as a
base does, and its segments in an `## Insert` table, each placed **after** a segment of
the base or an earlier inserted one:

```
## Insert
| Segment | After | Title                         | Children | Notes |
| ------- | ----- | ----------------------------- | -------- | ----- |
| TAS:1   | TOS:3 | The Animated Series, season 1 | 16       |       |
| TAS:2   | TAS:1 | The Animated Series, season 2 | 6        |       |
```

- **The stack's ruler is the base's, with the inserts.** In a stack with the package,
  `TAS:1:2` is a valid point, sorting after every point in `TOS:3` and before `TMP`.
  The base's own segments keep their relative order.
- **Valid only with the package in the stack.** A point on an inserted work is invalid
  in a stack without it (§4.2, rule 1), and a draft that uses the package's facts
  anyway has leaked it (§5.3).
- **Placement is an editorial choice**, like the base's own order (§4.1): here, the
  animated series is placed in the last part of the five-year mission, before *The
  Motion Picture*.
- **A fan work inserts only what the base cannot hold.** Most fan works retell or
  depart from canon inside the base's works, and date their rows on the base's points.
  A fan work set after the base ends, or in a stretch between its works, has no points
  of its own there: without an insert, all its rows would fall on one point and tie
  (§4.4). It inserts its own work instead, such as one set after *Deathly Hallows*
  (`After: DH`), so that its chapters order its rows.
- Inserted work ids MUST NOT repeat a work already on the ruler: the base's, or one that
  another package, a project layer, or the project inserts. Two packages inserting after
  the same segment are placed in stack order, the lower layer first.
- A project order (§6.8) is a permutation of the stack's segments, inserted ones
  included.

**Example cases:** [4a](../examples/README.md#case-4a), [I1](../examples/README.md#case-i1).

## 4.11 Story-dated rows

The ruler dates what the sources establish. What a story establishes about its own
entities happens on the story's clock, so a project dates those rows by **manuscript
position** instead: a `From chapter` column holding the chapter id from which the row
holds (format: §10.5).

```
| Attribute | Value                                         | As of | Source  | Citation | From chapter |
| --------- | --------------------------------------------- | ----- | ------- | -------- | ------------ |
| role      | operations officer, USS Enterprise-C          |       | project | premise  |              |
| role      | displaced officer aboard the USS Enterprise-D |       | project | ch.3     | chapter-03   |
```

- **Only for the project's own entities.** A story-dated row cites the reserved source
  `project` (§5.1) and describes an entity the project defines (§2.7): an original
  character, a relationship between two original characters, what an original
  character knows, or another original entity. A change the story makes to a canon
  entity, including its relationship to an original character, is a divergence (§6.2).
- **`As of` is empty.** A story-dated row is not a point on the ruler. Backstory the
  project gives its own entities stays ruler-dated or timeless, as before.
- **Visible from its chapter.** The snapshot keeps the row at positions at or after its
  chapter. For a project layer, the position is its pinned chapter (§7.2).
- **Later than every ruler point.** Among an attribute's rows, story-dated rows sort
  after every ruler point, and among themselves in chapter order. Chapter ids compare
  only within one project, and every story-dated row of an entity comes from the
  project that defines it.
- **Written by the chronicler** (§12.11), from what each chapter states. The foundation
  steps write the entity's starting state without `From chapter`.

**Example cases:** [26](../examples/README.md#case-26).

## 4.12 The ruler of a series

A self-contained book (§4.7) has no ruler from source works. Once a later book stacks
it, though, it is the later book's source: what a reader of book 1 knows. So in the
stack of a later book, a self-contained project layer's **manuscript is a work on the
ruler**, exactly as promoting the book would make it (§2.9):

- **Its id is the project's id.** Its only level is `chapter`, counted up to the pinned
  chapter: in a stack with `project:lantern-road@chapter-12`, `lantern-road:9` is
  chapter 9, and `lantern-road:13` is invalid.
- **Its place.** It is the ruler's only segment or, if the book defined a ruler of eras
  (§4.7), it comes after the last of them.
- **Its rows are dated on it.** In the later book, each of the book's story-dated rows
  (§4.11) has the as-of `<id>:<n>`, from its `From chapter`, which places it in the
  order of the attribute's rows. Its timeless rows stay timeless. Neither kind is
  time-filtered: each is an item anchored in the earlier book (§6.14), which holds at a
  later chapter set before its anchor only if the author carries it back (§7.2, step 3).
- **Later books insert around it.** A later book places what it needs before or after
  book 1: an era before it for a prequel, the years after it for a sequel. It lists
  them in its own `bible/canon-timeline.md`, in `## Works` and `## Insert` tables, as an
  official package does (§4.10, §10.4). `After: —` places a segment before every other
  one. A project layer's inserts are on the ruler of every project that stacks it.

```
## Works
| Work  | Title                     | Levels | Timed level | Notes |
| ----- | ------------------------- | ------ | ----------- | ----- |
| youth | Ines's apprenticeship     |        |             |       |
| after | The winter after the road |        |             |       |

## Insert
| Segment | After        | Title                     | Children | Notes |
| ------- | ------------ | ------------------------- | -------- | ----- |
| youth   | —            | Ines's apprenticeship     | —        |       |
| after   | lantern-road | The winter after the road | —        |       |
```

The later book is then an established project like any other (§6.1). It sets a cutoff
and sync points on this ruler and, if it wants them, a divergence point and an order. A
project layer whose own stack already has a ruler (a base, or an earlier book) is not a
work. Its chapters sit on that ruler through its sync points (§6.7).

**Example cases:** [L2](../examples/README.md#case-l2).

## 4.13 In-world time

The ruler orders **reading**: what someone following the source could know at each
point (§4.1). It does not say when things happen in the world. *Philosopher's Stone*
opens in 1981 and jumps ten years in its second chapter, and a flashback is read after
the events that follow it. **In-world time** is this second axis. A world records it as
**dates** in a **calendar** it declares. Both are optional: without a calendar, in-world
time stays free text, like `Story time` in `timeline.md` (§10.15), and the rest of this
section does not apply.

Dates never decide visibility. A fact is visible from its `As of`, on the ruler,
whatever its date (§7.2).

### Calendars

The package or project that owns the ruler declares the calendar, in its manifest:

- a **base** package, in `package.yaml` (§10.2), for every stack built on it;
- an **original** project, in `project.yaml` (§10.1), for itself and for every later
  book that stacks it (§4.12).

No other package and no established project declares one. They date in their stack's
calendar, as they date on its ruler. A fan work whose world counts time differently
keeps its own dates as free text. A calendar is one of two kinds.

**`iso`: real-world dates.** Dates are those of ISO 8601: the proleptic Gregorian
calendar, with a year 0 and negative years before it. It suits any world set on Earth,
whatever calendar its characters use:

```yaml
calendar: iso
notation: japanese     # optional
```

`notation` names the calendar the work itself writes dates in, as a Unicode BCP 47
calendar identifier: `gregory` (the default), `japanese`, `chinese`, `dangi`, `hebrew`,
`islamic`, `persian`, `buddhist`, `ethiopic`, and so on. It tells agents how to read the
source's dates and how to write dates in prose. It never changes how dates are stored:
every date is ISO, converted from the work's own form. A row MAY keep the work's own
form (Shōwa 64, a Julian date) as free text in its `Citation`. So MAY a notation that
does not convert exactly, such as a stardate, beside an ISO date as precise as the
source allows.

**Custom: a world's own calendar**, declared as a mapping:

```yaml
calendar:
  eras:
    - { id: BL, name: before the Lamps, counts: down }
    - { id: OR, name: the Old Road, years: 300 }
    - { id: NR, name: the New Road }
  months:
    - { name: Thaw, days: 90 }
    - { name: Bloom, days: 92 }
    - { name: Ember, days: 91 }
    - { name: Dark, days: 92 }
```

- `eras` (required, at least one) lie end to end on one line of years, in the order
  listed, each beginning where the one before it ends. There is no year 0 between eras.
  - `id` is capital letters and digits, starting with a letter (`AC`, `TA`), and is
    unique in the calendar.
  - `counts: down` marks an era counted backward, like BC. Only the first era MAY count
    down, and another era MUST follow it. Its year 1 is the year just before the next
    era begins.
  - `years` is an era's length. Every era that counts up MUST give it, except the last,
    which is open-ended. An era that counts down has none.
- `months` (optional) lists the months of every year in order, each with a `name` and a
  fixed number of `days`. Without months, a date names a year and nothing finer.
- There are no leap rules, weeks, or hours.

Here `BL 2` and `OR 5` are six years apart, and `OR 300` is the year before `NR 1`.

### Dates

A **date** names a span of time:

| Form                    | `iso`              | Custom        | Covers                                                  |
| ----------------------- | ------------------ | ------------- | ------------------------------------------------------- |
| `<year>`                | `1991`             | `NR 12`       | the whole year                                          |
| `<year>-<MM>`           | `1991-07`          | `NR 12-02`    | the whole month                                         |
| `<year>-<MM>-<DD>`      | `1991-07-31`       | `NR 12-02-14` | the day                                                 |
| `<date>..<date>`        | `1971..1978`       | `BL 5..OR 3`  | from the start of the first date to the end of the second |
| `..<date>`, `<date>..`  | `..1991`, `1998..` | `..NR 12`     | open at one end: in or before, or in or after           |
| `~<date>`               | `~1975`            | `~OR 120`     | about then (below)                                      |

- In `iso`, a year is an integer with no leading zeros, and a `-` before year 0
  (`991`, `-43`). In a custom calendar, a year is an era id, a space, and a positive
  integer. Months and days are two digits, numbered from `01`.
- A date MUST name a month and day its calendar has: `1991-02-30` is invalid, and so is
  `NR 12-05`, in a calendar of four months. A range's first date MUST NOT be after its
  second.
- `~` marks a single date, never a range, as approximate. It records a source that says
  "about", without inventing bounds the source does not give.

**Comparing dates.** A date is **before** another if its span ends before the other's
begins, and **after** it if its span begins after the other's ends. Otherwise the
comparison **can't tell**: `1991` against `1991-09-01`, say. An approximate date can't
tell against any date, and sorts at the date it states. The checks below report only
definite contradictions. Can't tell is never one.

**Ages and durations.** The age, on a date, of someone born on another is the number of
whole years from the second to the first, in the calendar's own years. Where either date
is a span, the age is a range: every age that some moment of each could give. Someone
born on `1980-07-31` is 10 or 11 in `1991`. Durations are counted the same way.

Relative times ("three days later", "the next spring") are not dates. They stay free
text, and placing them is a judgment for agents. The cell type `date` (§10.0) is a date
in the stack's calendar.

### Where dates are recorded

Each of these is optional.

1. **On the ruler.** A `## Dates` table in `canon-timeline.md` (§10.4) dates nodes of
   the ruler: when the events that a node shows take place.

   ```
   | Node  | Date       | Notes                                      |
   | ----- | ---------- | ------------------------------------------ |
   | PS:1  | 1981-11    | The night Harry is left with the Dursleys  |
   | PS:2  | 1991-06    |                                            |
   | DH    | 1997..1998 |                                            |
   | DH:33 | ..1998     | Mostly memories, reaching back to childhood |
   ```

   - A base dates its own works. An official or fanfic package dates the works it
     inserts (§4.10). An original project dates the works of its own ruler of eras
     (§4.7) and, for the books that stack it, its own chapters (`lantern-road:9`,
     §4.12). A later book dates the works it inserts. An adaptation dates nothing: its
     material is on base paths (§4.9), which carry the base's dates.
   - Dates are sparse and never interpolated. A point's date is the date of the deepest
     dated node that contains it, if any.
   - Order and date need not agree. A flashback chapter is dated before the chapter
     that precedes it.
   - A node dated outside the date of a dated node above it is a contradiction (below).

2. **On rows: `In-world`.** A state-history row (§10.5) MAY add an `In-world` column,
   after `True from`: the date on which the fact became true. It holds what the ruler
   cannot. A fact true since before canon begins has `True from: PS`, the first work's
   point, and its date goes here: `~1975`. `As of` still governs visibility, and
   `True from` still finds hidden truths (§4.4). `In-world` changes neither.

3. **Date-valued attributes.** In a stack with a calendar, the attributes `born` and
   `died`, of any entity, and `date`, of an event, hold dates. Their rows leave
   `In-world` empty: the value is the date. Without a calendar, they are free text, like
   any attribute.

4. **World history.** Events of the world's past, or off the page (a war, a founding, a
   treaty), are entities in `history.md` (§10.5). An event is an entity like any other,
   so the rest of the model applies unchanged: it is visible from its `As of`; higher
   layers add rows to it; a ledger can override or unset it (§6.4). Three of its
   attributes are reserved:
   - `date` (required): when the event took place;
   - `summary`: what happened, in a sentence;
   - `participants`: the slugs of those involved, separated by `; `.

   The **chronology** at a cutoff lists the events that resolve there (§7.2), sorted by
   their resolved `date`: by the start of its span, or by the date stated for an
   approximate date, with ties kept in the composed bible's order (§7.6). An event that
   takes place on the page needs no entry unless other facts refer to it: `## Dates`
   already dates the canon itself.

5. **Story events.** `timeline.md` (§10.15) MAY add a `Date` column after its required
   columns.

With a universe layer, a date of one base is moved by that base's offset into the
universe's time (§8.1).

### Checks

**Format errors** make a package or project invalid (§14.2), and nothing excuses them:

- a date that does not parse, or names an era, month, or day its calendar does not have;
- a date where the stack has no calendar (in `## Dates`, `In-world`, or `Date`);
- an event in `history.md` with no `date` row;
- a calendar that breaks the rules above, or a calendar or `notation` declared where
  this section does not allow one;
- a universe offset between bases without the same calendar (§8.1).

**Chronology contradictions** also make a package or project invalid, unless they are
accepted:

| Check            | Fails when                                                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `outside-parent` | A `## Dates` node's date is definitely outside the date of the nearest dated node above it                                             |
| `in-world-after` | A row's `In-world`, or an event's `date`, is definitely after the date of its `True from` point or its `As of` point: the fact becomes true only after the ruler shows it |
| `born-died`      | An entity's `born` is definitely after its `died`                                                                                      |

Each can be what the story means: a flashback chapter, a prophecy shown before its
event, a time traveller who dies before being born. An **`## Accepted`** table (§10.5),
in the file that holds the node or row, excuses one check on one subject and gives the
reason:

- It excuses only that check, on that subject. Any other contradiction, on the same
  entity or node, is still an error.
- In a **package**, an acceptance records what the source does, and cites it. A
  contradiction found at extraction is flagged, and a human settles it, by accepting it
  or correcting the row, before it is written (§12.4).
- In a **project**, an acceptance is the author's decision, which the file's writer
  (§3.3) records. Agents MAY surface the contradiction, but MUST NOT accept it
  themselves.
- A layer accepts only a contradiction that involves one of its own rows or nodes. A
  fan work cannot excuse a mistake inside its base.

**Warnings** concern the story, where a flashback or an unreliable narrator can be
deliberate. The continuity-editor raises them, and the author decides (§12.12):

- a `timeline.md` event dated before the `born`, or after the `died`, of an entity it
  lists;
- an age stated in the manuscript, or in a row, outside the range the dates give;
- in an established project, a story event dated before the date of its chapter's
  cutoff.

A traveler's age counts their personal time, not the world's (§9.1), so an age check on
a traveler is left to the continuity-editor's judgment.

**Example cases:** [W1](../examples/README.md#case-w1), [W2](../examples/README.md#case-w2), [W3](../examples/README.md#case-w3), [W4](../examples/README.md#case-w4), [W5](../examples/README.md#case-w5), [W6](../examples/README.md#case-w6), [W7](../examples/README.md#case-w7).
