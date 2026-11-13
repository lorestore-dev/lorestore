# 4. The temporal model

Facts extracted from source media are **stateful over the source timeline**. Harry
sleeps in the cupboard under the stairs, then in Dudley's second bedroom. Picard is a
starship captain, then Locutus of Borg, then a captain again. The world layer records
such facts as **append-only state histories**, each row dated against the ruler.

## 4.1 The ruler

`canon-timeline.md` is the **ruler**. It describes the source material as a **tree**
(works divided into seasons, episodes, chapters, scenes) and fixes the **order** in which
that tree is read. Its format is in §10.4. It has three tables.

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
| Order | Segment | Title                        | Units | Notes                       |
| ----- | ------- | ---------------------------- | ----- | --------------------------- |
| 1     | TOS:1   | The Original Series, season 1 | 29   | Episodes in broadcast order |
| 2     | TOS:2   | The Original Series, season 2 | 26   |                             |
| 3     | TOS:3   | The Original Series, season 3 | 24   |                             |
| 4     | TMP     | Star Trek: The Motion Picture |      | Released 1979               |
| 5     | TNG:1   | The Next Generation, season 1 | —    | Not divided                 |
| 6     | TNG:2   | The Next Generation, season 2 | 22   |                             |
```

**Counts** (optional) gives the number of children of nodes below the segments, for
example how many scenes the world's extraction divides an episode into:

```
| Node    | Units |
| ------- | ----- |
| TOS:3:2 | 14    |
```

`Units` is the number of children a node divides into at the next level:

| `Units`     | Meaning                                                                         |
| ----------- | ------------------------------------------------------------------------------- |
| an integer  | **Counted**: children `1 … Units` exist.                                        |
| empty       | **Uncounted**: the node is divided, but any positive index is valid.            |
| `—`         | **Undivided**: no point below this node is valid.                               |

A node the ruler gives no count for is uncounted, down to the work's last level.

Segment rules:

- No segment may lie inside another (neither may be a prefix of the other).
- A point is valid only if it lies inside a segment, or contains one (§4.2). Everything
  a world can date must therefore be covered by its segments.

The order is an **editorial choice**, made once per world. Broadcast or release order is
usually best, because it matches what someone following the source could know at each
point. Where series overlap (*Deep Space Nine* premiered during the sixth season of *The
Next Generation*), season-level segments give a good approximation, and episode-level
segments give an exact one. In-universe chronology belongs to story time, not the ruler.

## 4.2 Canon points

A **canon point** is a path down the ruler's tree, optionally ending in a timecode:

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
the timed level. Fractional seconds are allowed. Frame numbers are not used, because
frame rates vary between releases.

**Scenes** are rarely numbered by the source itself, so the scene level is the world's
own breakdown, made during extraction. A new scene starts at a change of location or a
break in continuous time. The extraction pipeline MUST number scenes consistently within
a world, and MAY record the counts in the Counts table.

A point is **valid** if:

1. its work is in the Works table;
2. it has no more indices than the work has levels;
3. it lies inside exactly one segment, or contains at least one;
4. each index is within its parent's count where that count is known, and no index
   falls below an undivided (`—`) node;
5. any timecode follows a path that reaches the timed level, and has minutes and seconds
   below 60.

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

Canon points are comparable **only within one world**. Points from different worlds
are related only through a universe's offsets (§8).

A project that rearranges canon supplies its own order of the same segments (§6.8).
Within that project, rules 1–4 apply with the project's `Order` in place of the
ruler's.

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

## 4.3 The point list

Read as a list, the ruler yields every canon point a world can offer for picking, in
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

Wherever a user chooses a canon point (a project's cutoff, a row's as-of), a host
SHOULD offer the point list rather than free text, presented as a tree (work, then
season, then episode) when it is long (§14).

## 4.4 State histories

A state history is a table of rows, each giving an attribute's value from a canon point
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
- **Every row is dated** with a valid canon point (§4.2), except in a self-contained
  world with no ruler (§4.7).
- **Every row has a source** registered in `sources.md` (§5) and a **citation** that
  locates the evidence.
- **One value per attribute, source, and point.** Two rows with the same entity,
  attribute, source, and as-of but different values are a conflict. The merger MUST
  flag them rather than write both (§12.4).
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
  sorts at the very start of canon.
- **`As of` still governs visibility.** The snapshot resolves a row only once its
  `As of` is reached. `True from` does not reveal anything early. It lets the system
  recognize a **hidden truth**: a fact that is already true at the cutoff but not yet
  revealed (§7.2, §6.12).
- Extractors SHOULD record `True from` whenever a source reveals backstory, even if no
  current project needs it. It is cheap to record and impossible to reconstruct later.

## 4.5 Ending a fact

To record that an attribute stops holding (a character dies and loses an office, an
item is lost, a scar heals completely), append a row whose value is the reserved token
`(unset)`. From that point the attribute resolves to absent (§7). A later row MAY set it
again.

## 4.6 Corrections

Append-only governs **canon time**, not editorial correction. If a row is wrong (a
misread passage, a bad citation, a value the source never states), the extraction
pipeline fixes or removes the row itself and bumps the package's patch version (§2.8).
It MUST NOT "correct" a wrong row by appending a later row, because that would assert a
change the source never made.

## 4.7 Self-contained worlds without a ruler

A self-contained original world has no source works, so it MAY omit the ruler. Its
state rows then leave `As of` empty, meaning **timeless**: always visible. Change during
the story is recorded as story-time events in `timeline.md`, not as dated world-layer
rows. A self-contained world that needs dated backstory (eras, a prior war) MAY define
a ruler whose works are eras; all rules in this chapter then apply.

## 4.8 Facts are self-dating

Every extracted fact carries its own canon point, so its place on the timeline never
depends on the order in which it was extracted. Source units can be extracted in any order,
including in parallel, and the merger assembles history by **sorting on canon point**
(§13.6). Sequential extraction is the one-worker case of the same pipeline and gives the
same result.
