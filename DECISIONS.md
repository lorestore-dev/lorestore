# Decisions

This log records the design decisions behind the spec, most recent first. Each entry
says what was unclear or contradictory, what was decided, and where the rule now lives.

## 0.3: in-world time

**D119. The spec links to its examples.** The example cases cited the spec by `§` in
plain text, and no spec section pointed back to a case, so a reader of a rule could
not find the case that shows it. Every case now has an anchor; each spec section that a
case shows ends with an **Example cases** line linking to them; the cases' `§`
citations are links. The examples stay in this repository, so the links are relative.
`tools/refs.py` checks that every relative link and anchor resolves, and that every
case is linked from at least one spec section. → every chapter with cases; §14.2

**D118. Viewpoints, and narrators who look back.** `parameters.pov` named a narrative
mode for the whole project, and the drafter was told to respect what "the POV
character" knows, but nothing recorded who that was. A project now sets
`parameters.viewpoints` to `none` (the default), `chapter`, or `scene`, and a chapter
overrides it in the outline, which becomes a structured table for every workflow so
that agents can read the plan row by row. A viewpoint limits what the narration knows
to the character's knowledge at the scene; `none` means no character limits it. The
reader-facing rules (hidden canon, mystery reveals, reveal aliases) hold in every mode.
`Told from` lets a narrator look back from a later chapter or the end: it moves what
they know, never when the reader learns it. A viewpoint leak is the continuity-editor's
finding, not an error, and a drafted viewpoint that differs from the plan is a warning.
→ §1.6, §3.3, §7.7, §10.1, §10.18, §10.23, §12.6, §12.10, §12.12, §13.10, §14.2

**D117. Text an agent reads is data, never instructions.** Agents read a great deal
written by other people: shared packages, source texts, readers' feedback. Nothing
said what an agent should do with text in that material that reads as an instruction
to it. It is content: an agent never follows it, never records it as fact, and reports
it where its output has a place for problems, for the showrunner to surface. The host
keeps material apart from instructions, and shows the author instruction-like text in
untrusted input before an agent reads it. Characters giving each other orders are
story, not instructions. → §11.12, §14.1

**D116. Spec versions.** Every manifest declared `spec_version: "0.2"`, but nothing said
what a host does with another version, and 0.3 adds fields a 0.2 host does not know.
A host lists the versions it supports and refuses a stack with any other. A stack may
mix supported versions, each directory read by its own version's rules. Before 1.0 any
minor version may break; from 1.0 a minor version only adds. Moving to a new spec
version is a human change, and a patch bump for a package. The examples move to 0.3,
and each package takes a patch bump. → §2.8, §10.0, §14.1

**D115. The prompter: image prompts from the bible.** Authors wanted pictures of their
characters, families, maps, and places, and a picture drawn from the bible can leak as
easily as a paragraph. A nineteenth agent, the prompter, writes one prompt per step to
`prompts/<id>.md`: a character, a family portrait, a family tree, a map, or a location,
each from the snapshot at a cutoff the author chooses. It depicts only what the
snapshot returns: parentage and dates as the reader knows them, places as they stand
then, revealed identities only from their reveal. Composition and mood are the
prompter's to choose; facts are not, and a detail the bible lacks is listed under
`## Gaps` rather than invented. Prompts are plain prose for no particular model, are
never canon, and are read by no agent. They never describe an actor's likeness or ask
for a living artist's style by name. → §2.5, §2.6, §3.3, §10.29, §12.1, §12.2, §12.20,
§14.2

**D114. Lineage: parentage, ancestry, and titles.** Relationships are pairwise, so the
spec could not hold a family tree, a dynasty, or a succession. The lineage module adds
the reserved attributes `parents`, `guardians`, and `descends-from` (slug lists, on any
entity) and `titles.md`, a state history of titles whose `holder` changes over time.
Being ordinary attributes, they inherit reveals by `As of`, correction by later rows, and
the ledger for changes. Two chronology checks join §4.13, `born-before-parent` and
`ancestry-cycle`, and are accepted in the same way, so a time traveller can be their own
grandparent; one acceptance excuses a whole cycle. Implausible ages and holders are
warnings. A family tree is a view at a cutoff, never stored, so it cannot leak a
parentage reveal. → §1.6, §2.7, §3.3, §9.6, §10.5, §10.28, §12.7, §12.12, §14.2

**D113. Mysteries: clues, reveals, and fair play.** `plot-architecture.md` held running
mysteries as prose, and nothing tied a mystery's answer to its clues. The mysteries
module adds `mysteries.md`: each mystery's question, its reveal point, and its clues
and red herrings, each with where it is planted and whether the reader needs it. The
answer is a secret in `knowledge.md`, so the snapshot already keeps it hidden. Fair-play
problems are warnings, since a writer may cheat on purpose. A higher layer adds clues to
a lower layer's mystery but never changes them. The drafter must not let narration
answer a mystery early, and the canon-keeper's order and divergence audits list canon
mysteries a change makes unfair. → §2.7, §3.3, §9.5, §10.27, §12.6, §12.10, §12.11,
§12.13, §13.1, §13.10, §14.2

**D112. Travel: routes and journey times.** With in-world dates, the spec could say when
scenes happen but not whether a character could get from one to the next. The travel
module adds `routes.md`, which holds modes of travel and routes between `places.md`
entries, each route a state history whose values are durations, and a `Place` column
in `timeline.md`. A journey faster than the shortest path allows is a warning, never an
error, because the story may mean it. Only known modes count, and an approximate
duration counts as instant, so the check warns only when the routes rule a journey
out. → §9.4, §10.0, §10.15, §10.26, §12.7, §12.10, §12.11, §12.12, §14.2

**D111. Re-pinning to a new minor or patch version is a patch bump.** §2.8 required a
bump on every change but did not say which one a re-pin is. Adding the calendar to the
two example bases bumped them to minor versions, so every package relying on them had to
re-pin. A re-pin to a new major version stays a major bump; any other re-pin is a patch.
→ §2.8

**D110. Chronology contradictions, and accepting them.** A date can contradict the
ruler on purpose: a flashback chapter outside its book's years, a prophecy shown before
its event, a time traveller who dies before being born. Three checks
(`outside-parent`, `in-world-after`, `born-died`) make a package or project invalid
unless an `## Accepted` row, in the file that holds the row or node, excuses that check
on that subject with a reason. A package's acceptance records what the source does and
cites it; a project's is the author's decision. A layer can accept only a contradiction
that involves its own rows or nodes. Format errors (a date that does not parse, a date
with no calendar, an event with no date, an offset across calendars) can never be
accepted. Story-level problems (an event outside a participant's lifetime, an age the
dates rule out, an event before the cutoff's date) are warnings the continuity-editor
raises. → §1.6, §4.13, §10.5, §12.4, §12.12, §14.2

**D109. World history is a file of events, and events are entities.** Backstory and
off-page events had nowhere structured to go. `history.md` is a multi-entity state
history whose entities are events, with the reserved attributes `date` (required),
`summary`, and `participants`. Treating events as entities rather than giving them a
table of their own reuses visibility by `As of`, hidden truths, layering, resolution
modes, and the ledger unchanged; the chronology is a view, sorted by date. A universe's
chronology merges its bases' histories in universe time. → §2.7, §3.3, §4.13, §8.1,
§10.5

**D108. Where dates are recorded.** Four optional places: a `## Dates` table in
`canon-timeline.md`, sparse and never interpolated, written by whoever owns the works it
dates; an `In-world` column on state-history rows; the date-valued attributes `born`,
`died`, and an event's `date`; and a `Date` column in `timeline.md`. `True from` stays a
ruler point, because the snapshot compares it with the cutoff to find hidden truths
(§7.2), and a sparse `## Dates` table could not always turn a cutoff into a date. The
snapshot returns the cutoff's date. → §4.4, §4.13, §7.2, §10.4, §10.5, §10.6, §10.15,
§12.3, §12.7, §13.6

**D107. Dates are spans, and comparisons can't always tell.** Canon rarely gives an
exact day. A date is a span: a year, a month, a day, a range with optional open ends, or
an approximate `~` date. One date is before another only if its span ends before the
other's begins; otherwise the answer may be "can't tell", which is never a
contradiction. An approximate date always can't tell, but sorts at its stated date, so
that extraction never invents bounds the source does not give. Relative times stay free
text. Ages are ranges. → §4.13, §10.0

**D106. In-world time has a calendar of its own.** The ruler orders reading, and the
spec had no structured in-world date: `Story time` was free text, `True from` a ruler
point, and universe offsets shifted a calendar nothing defined. The owner of the ruler
(a base, or an original project) MAY now declare a calendar. `iso` stores every
real-world date as ISO 8601, whatever calendar the work uses, with an optional
`notation` (a BCP 47 calendar identifier, such as `japanese`) telling agents how the
work writes dates; the name is ISO, not Gregorian, so that no culture's calendar is the
default by name. A custom calendar declares eras on one line of years, and optional
fixed months, with no leap rules. Universe offsets apply only between bases with the
same calendar. → §1.6, §4.1, §4.7, §4.13, §8.1, §10.1, §10.2, `schemas/`

**D105. Fan works insert their own works.** Only `official` packages could insert into
the base's ruler, so a fan work set after the books end, or between them, had no points
of its own: every row it gave fell on the base's last point, and two values of one
attribute there were a tie (§4.4). A `fanfic` package may now insert its works, exactly
as an official one does. An adaptation still may not, because it retells the base's own
works and dates even its added scenes on their paths (§4.9); fanon and theories have no
works. The example fan work inserts `FIC` after `DH`. → §2.3, §4.2, §4.10, §6.8, §10.4,
§13.6, §14.2

## 0.2: layered packages

**D104. Book 1's story-dated rows are anchored, not time-filtered.** §4.12 dated a
self-contained book's story-dated rows `<id>:<n>` on the series ruler, and §7.2's time
filter then dropped any ahead of the cutoff before the seam step saw them, so a later
book set before book 1 could never carry one back, though §6.14 treats them as items. The
as-of now only orders them: like the book's timeless rows, they are anchored items,
held ahead of their anchor only when the author carries them back. → §4.12, §7.2

**D103. The series ruler's own segments count everywhere.** The valid-point rule and the
project-order rule named only the base's segments and an official package's inserts, so
a later book's own inserts (`youth`, the cutoff of `lantern-road-before`) were not valid
points by the letter of §4.2. Both rules now cover a project layer's work and the inserts
of the project layers and the project itself; adding or removing one also calls for a
new project order, and an inserted work may not repeat any work on the ruler. → §4.2,
§4.10, §6.8

**D102. An original project has no layers.** The schema required layers of an established
project but let an original one have them too, which nothing could serve: an original
setting has no cutoff or sync points to read packages at (D98), no ledger to record a
change to them (W3), and no canon-keeper, and a follow-up to an earlier book is already
established (D90). `setting.type` and `layers` now always agree, in the schema and in
§6.1; the field stays, since the overlays and the curator key on it. A project that uses a
world loosely is established with `fidelity: au`. → §6.1, §14.2

**D101. Errata replace source conflicts.** A source conflict needed two sources tying
within one package, and the only real case was an error the source later corrected:
*Goblet of Fire*'s first printings. That is not the author's to decide. A package now
records one intended value per attribute, tier, and point: the corrected text, with the
error kept under a new tier, `erratum`, which never resolves (like `theory`); the fan
consensus in a fanon package; and a deliberate revision or recut as its own package.
Two rows that still tie are an extraction error, which the merger flags for a human. The
canon-keeper flags prose relying on an erratum as **erratum use**, a fix item, and marks
erratum evidence in a theory audit. Source conflicts are removed: the ledger table, the
marker, the snapshot step, and the author-only decision. This supersedes D77 and the
tie and `Layer` parts of D95. The seam conflicts section becomes §6.14.
→ §1.6, §2.3, §4.4, §5.2, §6.9, §6.13, §7.2, §10.8, §12.3, §12.4, §12.13

**D100. The retelling audit runs for every logged divergence.** The list of decisions
that re-run the divergence audit omitted a source conflict decided `other` and a seam
conflict decided `keep-earlier` or `other`, which also log divergences. → §6.6

**D99. Promotion writes the ruler and establishes the project.** No step of §2.9 wrote
the new base's `canon-timeline.md` when the book had no eras. Promotion now writes the
book as a work, after any eras, and the promoted project becomes established, with one
sync point per chapter on that work. → §2.9

**D98. A self-contained project's cutoff.** Nothing said what `X` was for a
self-contained project with a ruler of eras. It is the end of the ruler: the story is
set after its backstory, so `setting.cutoff` is invalid in an original setting (also in
the schema). A materialized snapshot in a series begun by a self-contained book is
named by the first book's id. → §4.7, §7.1, §7.6, §10.1

**D97. Review formats for inversion candidates and the seam audit.** The order audit's
`## Inversion candidates` table and the seam audit's `## Seam conflicts` entries were
used but never defined. → §10.19

**D96. Frames: the world point is the scene's cutoff.** Nothing said how a scene's world
point relates to its chapter's sync point. Within a scene the world point is `X`; the
sync point covers everything outside scenes and is the drafter's starting point. A host
SHOULD warn when a scene with no travelers is set later than its sync point. Snapshot
and composed-bible headers now record the project order, its source if inherited, the
sync points, the world point, and seam decisions. → §7.1, §7.5, §7.6

**D95. Quotations: ties, layers, and project lines.** Two sources tying on a quotation's
`Speaker` or `Line` were not a source conflict; they now are, recorded under the
quotation's qualified id. Every Source conflicts row gains a `Layer` column, so a
decision cannot match another package's source of the same id. A project keeps no
`quotations.md`: its lines stay in its manuscript, which a later book reads through
`manuscript/@<project>/…`. Promotion re-cites `project` rows to the new source. A
quotation MAY have several rows. → former 6.14, §10.8, §10.13, §2.6, §2.9

**D94. A stack change proposes a new order.** Adding or removing an official package
silently broke `setting.order`. The host now refuses to run, proposes an order with each
new segment after its predecessor on the new ruler, and the author accepts or edits it
before the order audit runs again. → §6.8

**D93. Inversion candidates.** The order check compared rows of one attribute only, so a
dependency across attributes (the Firebolt in the first task) went unflagged. The host
SHOULD list, for each pair of segments the order swaps, every entity with rows in both,
and the order audit MUST address each. → §6.8, §12.13, §14.1

**D92. A series is promoted after two books.** Every book stacked as a project layer
adds a ledger, sync points, and seam decisions that each later book must carry. Once a
project stacks two or more project layers, the host SHOULD suggest promoting the
earlier books into a package: a base for a self-contained series, a `fanfic` package
for an established one. Promotion dates each row at its anchor, so the seams become
ordinary dates. → §2.9

**D91. Seam conflicts: prequels and split frames.** A later book could be set before
the earlier one, or partly before and partly after, and settings alone cannot tell a
prequel from a wrong pin. Everything an earlier book brings in is now anchored where
that book established it. At a chapter set before the anchor, the item is ahead, and
the author decides: carry back, not yet, or other, by item or by pattern. A seam audit
(E1b) first checks the pin, then raises the items ahead and any value seam, where the
later book's stack resolves a canon attribute differently. The decisions are a sixth
author-only type, recorded in a Seam conflicts table and inherited as of the pin. A
branch's sequel MUST be a branch diverging no later, and a later book with no order
inherits its layer's. → §6.14, §7.2, §10.8, §13.4

**D90. The series ruler.** D85 left a sequel to a self-contained book with no ruler,
so it could not be set before or after book 1. Book 1's manuscript is now a work on
the ruler of every later book, counted to the pin, after any eras book 1 defined. Its
story-dated rows are dated on it. Later books insert their own segments before or after
it (`After: —` for before everything), and then set cutoffs and sync points as over a
base. → §4.12, §6.3, §7.1

**D89. `adopt` reconstructs the whole bible.** Adopting a self-contained story never
wrote relationships, the voice guide, or knowledge; adopting into a stack never wrote
the project's own places and systems; no step checked the imported chapters' internal
consistency; nothing audited the canon still ahead once the walk ended; and P8 used a
double repeat that §11.7 does not allow. `adopt` now has a reconstruct phase with
P4a and P4b, P5 for the project's own additions in a stack, and a per-chapter phase
with a continuity step (P8a). When the walk ends, an established project runs E1a and
E2a–E2b for the canon ahead. → §13.8

**D88. Serial arcs run the established-world audits.** The overlay hooked only into the
foundation, so a serial's later arcs logged no planned divergences, and their new sync
points were never audited. E6 now logs each later arc's planned divergences after A1,
and E6a and E6b audit and log what the arc's new sync points reach after A2, gated for
the author. → §13.3, §13.4

**D87. Earlier books' decisions carry over.** Only source-conflict decisions were said to
bind a sequel, and not as of the pin. Now an earlier book's Hidden canon and Source
conflicts rows decided at or before the pin, and the Theory conflicts of the theories
its divergences in force adopt, all bind the later book, and the later ledger wins
where two decide the same question. → §6.4, §6.12, §6.13, former 6.14, §7.2, §12.10

**D86. Renumbering chapters.** Chapter ids are referenced from sync points, the ledger,
story-dated rows, the story ledgers, revisions, feedback, and other projects' pins, but
nothing said what happens when the outline inserts or moves a chapter. A deterministic
`renumber` skill now rewrites every chapter id in the project in one step. It refuses
to move a chapter readers have seen, or one at or before another project's pin. →
§3.3, §11.10, §13.10, §14.2

**D85. An established project needs a layer.** A world known only from `references/`
had no ruler, so no cutoff, and no step wrote its curated files. It is now built into a
package first, by extraction or promotion, and `references/` is background only. An
established project MUST have a package or project layer (now also in the schema). A
sequel to a self-contained book has no ruler unless that book defined one: it sets no
cutoff, divergence point, order, or sync points, and its project layers' pins bound it.
The §6.4 example's D2, a divergence on an original character, is now Hermione
befriending Mara, the case §6.2 names. → §6.1, §6.3, §6.4, §7.1, §12.13, §14.2

**D84. Story-dated rows, and a project's own additions in a stack.** Nothing recorded
what the manuscript does to a project's own entities: the chronicler wrote only story
ledgers, so an original character who changed in chapter 7 had the same snapshot in
chapter 9, and ruler points could not date it, since the change happens on the story's
clock. A project's rows about its own entities may now carry a `From chapter`. Such a
row cites `project`, leaves `As of` empty, is visible from its chapter on, and sorts
after every ruler point. The chronicler appends these rows to original characters'
sheets, `relationships.md`, and `knowledge.md`. Changes to canon entities stay
divergences. Projects with a stack also had no step for their own places, systems,
relationships between original characters, or their knowledge: steps 3, 6, and 7 were
skipped, and E1 replaced step 3. Those steps now run in such projects for the project's
own additions only, and E1 runs after step 2. → §4.7, §4.11, §2.7, §3.3, §7.2, §10.5,
§12.6, §12.7, §12.8, §12.11, §13.1, §13.4, §14.2

**D83. Author markers block the chapter.** The showrunner and `novel` said every TODO is
resolved before continuity runs, but `hidden canon` and `source conflict` markers wait
for the author, who may take a long time. Only `needs bible` markers must clear before
continuity. The other two count as pending decide items: the chapter goes on through
the chronicler and continuity, and its step-14 gate waits for the author. →
§11.8, §12.2, §13.1, §14.1

**D82. Consistency after D78–D81.** Stale text fixed:
- the project order permutes the stack's segments, inserted ones included, not only
  the base's;
- §5.5 no longer calls fanon a lower tier;
- the ledger has up to five tables, not two;
- the bridge is base-qualified, and universe Overrides qualify slugs by base;
- the workflow `context` is `package`, not `world`;
- `compose` runs before step 1, where the architect first reads the composed bible;
- the canon-keeper runs outside established projects for frames checks.

§1.6 also gains the terms divergence conflict, order inversion, and source conflict. →
§1.6, §5.1, §5.5, §6.4, §6.8, §10.8, §10.14, §11.7, §12.13, §13.4, §14.2

**D81. Every divergence is audited.** The divergence audit ran for planned divergences
and for emergent ones logged at E5, but not for the divergences that carry out an
author's decisions, though a resolution can reach further than what it resolves; and
nothing said it covered an earlier book's divergences, which reach into a sequel's
canon. Now every divergence in force is audited, the project layers' included, and the
audit re-runs whenever a divergence is logged, until it finds nothing new. Hosts SHOULD
also list **reach candidates**, the canon rows on the attributes a divergence
overrides that it meets ahead, which the canon-keeper must address. The list is a floor
the checker can test; the audit still reads ahead for conflicts on other attributes.
→ §6.6, §6.11, §12.13, §13.4, §14.1

**D80. Adherence settings, sync points, and ruler points.** `canon.md`, the adherence
contract, mostly restated `project.yaml`: the divergence point and fidelity were already
settings, the scope is the stack and cutoff, and original additions are marked in the
roster. It also put the curator in charge of what is the author's call. The file is
gone. `project.yaml` holds the adherence settings, with two new keys: `fidelity_notes`
for latitude of the project's own, and `order`, the project order, which moves out of
the track because reordering is the author's decision. The architect still maintains
the chapter-to-cutoff map, which grows as chapters are planned, so it stays a file,
renamed `sync-points.md`. Canon points are now **ruler points**, since they are
addresses on the ruler, not claims about canon; `canon_point`, `canon_points`, and
`canon_mode` become `cutoff`, `cutoffs`, and `follow` (not `mode`, which would read as
the resolution mode). In the established-world overlay,
E1 is now the architect's sync points and E1a the order audit; step P5 runs only in
self-contained projects. §10.17 is removed and later §10 sections renumbered.
→ §1.6, §2.2, §3.3, §4.2, §6.3, §6.7, §6.8, §6.11, §7.1, §10.1, §10.21, §12.6, §12.7,
§12.13, §13.4, §13.8, §14.2

**D79. The base is `base`, not `canon`.** A base lived in `worlds/<fandom>/canon/`, with
`kind: canon`, so the layout itself called it canon, when what counts as canon is each
project's decision. Its folder is now `worlds/<fandom>/base/` and its kind `base`, both
named for its place at the bottom of the stack. Its id stays the bare `<fandom>`.
→ §1.6, §2.2, §2.3, §2.9, §5.2, §5.3, §10.2

**D78. Position words.** "Lowest precedence first" described the stack, but under
`fill` the lowest layer wins, so the phrase was wrong for one mode in three. And tiers
ran the other way from layers: the base was the lowest layer but held the highest
tiers. Now **lower** and **higher** mean position only, nearer the base or nearer the
project, and never which row wins; the mode decides that. Tiers are ordered the same
way, so `primary` is the lowest tier, and within one layer the lowest tier wins. This
changes no result. **Earlier** and **later** describe only a row's as-of, never a layer.
→ §1.6, §2.2, §4.10, §5.2, §5.4, §7.2, §10.1, §14.3

**D77. Source conflicts are the author's.** Two sources in one layer, of one tier, can
set an attribute at the same point to different values: two editions of *Goblet of
Fire* disagree about the order of the echoes in the graveyard. Resolution had no rule
for the tie, so a host would have picked one arbitrarily. Such a tie is now a **source
conflict**: the snapshot leaves the attribute unresolved and returns the tied rows, and
the author decides, under every gate policy, which source to follow or what else to do.
The curator records the decision in a new Source conflicts table in the ledger, and
later books inherit it. A package never resolves the tie, which keeps the registry
neutral. → §6.9, §6.11, former 6.14, §7.2, §10.8, §10.18, §10.19, §11.8, §11.9, §12.2,
§12.7, §12.10, §12.13, §13.8, §14.1, §14.2

**D76. Quotations resolve across layers.** The films often give a line from the books
to another character (in *Prisoner of Azkaban*, Ron's stand against Black goes to
Hermione), but a quotation's `ID` was a key, so a films package could only add a
competing quotation. A higher layer now gives a lower package's quotation a row by
qualifying the ID, `<package-id>:<ID>`, and `Speaker` and `Line` resolve by the
project's mode like attributes. With the films stacked, `precedence` gives the line to
Hermione and `fill` keeps it Ron's. → §2.7, §5.4, §10.13, §14.2

**D75. Official works outside the base.** Star Trek's animated series is official, but
whether it is canon is disputed, and with `excluded` sources gone it had nowhere to go.
The spec should not settle such disputes, so a new package kind, `official`, holds
`secondary-official` material whose canon status is disputed. The base keeps only what
is not in dispute, and each project decides by its stack and resolution mode. An official package with works of its own **inserts** their
segments into the base's ruler with an `## Insert` table, each after a named segment;
the base's ruler never changes. Points on an inserted work are valid only with the
package in the stack. The example is `star-trek/animated`, inserted after TOS season 3.
→ §2.3, §4.2, §4.10, §5.2, §5.3, §10.4, §13.6, §14.2

**D74. Fill resolution.** With layers listed lowest first, `precedence` lets a fan
layer override canon, and the old enriched behaviour (fan rows only fill gaps) could no
longer be expressed. A third mode, `fill`, picks the lowest layer with a row: canon
stands wherever it speaks, and higher layers supply only what it leaves blank. This is
how an author makes a thinly drawn canon character, such as Daphne Greengrass, their own
without contradicting canon. → §5.4, §7.1, §7.2, §10.1

**D73. Adopting an existing story.** Authors bring work written before they used
LoreStore, sometimes already published, and the workflows only built a bible before the
prose. A new `adopt` chain runs once: the chapters are imported with their real
statuses, the architect and character-designer reconstruct premise, outline, and cast,
the curator writes the adherence contract, and then the chapters are walked in order,
with the chronicler backfilling the ledgers and the canon-keeper surfacing departures
from canon as emergent divergences for the author. Adoption never rewrites a chapter.
The project then continues in its own workflow. → §13.8

**D72. Early access, revisions, and human feedback.** Authors share chapters with beta
readers and patrons before release, and the spec had no state between finished and
released. A new status, `early-access`, is set only by the author (through the
`release` skill), in order, in any workflow. An early-access chapter stays editable,
and every change to it is logged in `revisions.md`, which gains `Audience` and `Date`,
with a reader note. Human readers' notes go in `references/feedback/chapter-NN/
<reader>.md`; the beta-reader folds them into its priorities marked `(human: …)`. →
§10.18, §10.19, §10.22, §10.25, §11.8, §11.10, §12.2, §12.11, §12.18, §13.9, §14.2

**D71. Theories are numbered claims, adopted through the ledger.** Theories were opt-in
by profile, so a theory could only be on or off, with no record of how well it fit the
story. Theories now live in a `theories` package as numbered claims. A project adopts
some or all of a theory's claims as a divergence whose `Basis` names them. Before that,
the canon-keeper lists every piece of evidence in the stack, at any point, that
contradicts a claim: a **theory conflict**. The author alone decides to keep, adapt, or
discard each one, and the curator records the decisions in a Theory conflicts table.
Theory rows never resolve into state. Theory conflicts join the author-only decisions.
→ §6.9, §6.13, §10.8, §10.13, §11.8, §12.5, §12.13, §13.4

**D70. The composed bible.** With several layers, an agent would have to know where each
package lives and merge their files itself. The `compose` skill now builds
`derived/bible/`: the union of every layer's files, each row tagged with its `Layer`.
It is a union, not a resolution, and a rebuildable cache. Agents in project context read
`bible/…` through it. → §7.6, §2.6, §11.6, §11.10, §13.4

**D69. Universes are layers.** A universe was a separate kind of thing that a project
named in its own field, with per-world profiles. It is now a layer that relies on two or
more bases, stacked above them. More than one base in a stack requires a universe.
Cutoffs and divergence points are keyed by base, and world-layer paths are qualified
`bible/@<base-id>/…`. → §8, §2.2, §7.4, §10.1, §10.2.1

**D68. Project layers, relisted.** A sequel had no way to inherit the earlier book's
divergences and original cast. A project can now stack another project as a read-only
layer, `project:<id>@chapter-NN`, whose ledger applies as of that chapter, before the
project's own, and transitively through its own project layers. Its package layers are
not inherited: the sequel relists each one, at the same major version and the same or a
later version, so every package pin is visible in one file. The host warns when a
project used as a layer changes at or before its pinned chapter. → §2.2, §6.4, §7.1,
§14.2

**D67. Adaptations get their own tier and timecodes.** Films and other adaptations were
either canon or excluded, with no way to place a film scene against the book it adapts.
`adaptation` is a new tier, between secondary-official and fanon. An adaptation package
maps its works onto the base's ruler in an `## Adapts` table, and its facts are dated
`book:chapter:scene+<film-timecode>`. The book path decides order; the timecode orders
only rows at the same path, with untimed rows first. A timecode is valid only if an
adaptation in the stack covers the path. A film that takes scenes out of the book's
order, as the *Deathly Hallows* films do with chapter 24, has one `Adapts` row per
contiguous range. → §4.2, §4.9, §5.2, §10.4

**D66. Union across layers, and extension sheets.** It was unclear how a fanon package
could add a house to a canon character without editing the base. A layer adds keys but
never redefines a lower layer's. To add rows to a lower layer's entity, a package uses
an **extension sheet**, with `extends: <package-id>`. Projects cannot hold extension
sheets; they change lower layers only through the ledger, and may add entities of
their own. → §2.7, §10.5, §12.4

**D65. Resolution is the project's choice.** Profiles lived in the world package and
mixed two questions: which sources are active, and how they combine. The stack now
answers the first, and the project's `resolution` the second. `precedence`: the highest
layer with a row wins, then the higher tier within it, then the latest as-of.
`recency`: the latest as-of wins, with ties going to the higher layer, then the higher
tier. Ledgers apply after resolution. Profiles, `active_profile(s)`, `canon_basis`, and
the `excluded` source flag are removed; a same-fandom package not in the stack is a
source leak. → §5, §7, §10.1, §10.2, §14.2

**D64. Pure bases.** A world package mixed books, films, fanon, and fan works in one
registry, so every project paid for the whole fandom. A fandom's canon package (its
**base**) now holds only canon-tier sources, and everything else moves to its own
package. Each package's manifest has a `kind` and pins what it relies on. It is renamed
from `world-config.yaml` to `package.yaml`, since it now describes any package, and to
match `project.yaml` and `universe.yaml`. For the same reason, the `world-index` skill
is renamed `indexer`.
The Harry Potter base is 3.0.0 and the Star Trek base 2.0.0. → §2.3, §5.1, §5.3, §10.2

**D63. Folders by fandom.** Several packages per fandom needed a layout. Packages live
under `worlds/<fandom>/`: the base in `canon/` with the bare id `<fandom>`, other
packages at `<fandom>/<package>`, and fan works at `<fandom>/fanfic/<work>`. Extraction
workspaces mirror the same paths. → §2.1, §2.3, §2.4

**D62. Canon is layered.** A project read exactly one world, through a profile, so it
could not combine an adaptation with fan conventions, build on an earlier book, or
cross over without special cases. A project now lists its **layers**, lowest
precedence first: packages, universes, and other projects. Each package pins the
packages it relies on, and a stack MUST list them below it. The host MUST NOT add a
missing layer. `spec_version` is `"0.2"`. → §1, §2.2, §3, §10.1

## 0.1: review round 9

**D61. Time travel declares its mechanisms.** The frames module handled a fixed loop
(the Time-Turner) and a branch (Yesterday's Enterprise), but had no way to say which
kind of time travel a story uses, and so no way to check a trip against its rules. A new
world-layer file, `time-travel.md`, declares one entry per mechanism. Each entry has a
**model**: `dilation`, `fixed`, `loop`, `mutable`, `branching`, or `feedback`. Models
are told apart by two questions: was the traveler already there the first time, and
whose actions can change history? Each entry also gives its free will, what it carries,
and its limits. The model decides the checks: a closure check for `fixed`, overwritten
or abandoned branches for `mutable` and `loop`, ripples for `feedback`. Legs and
branches name their mechanism, and branches gain a `Status`. A self-contained project
writes its own `time-travel.md`. The `the-long-way-back` example's paradox X1 is
removed, because remembering an overwritten branch is now part of a traveler's own
frame. → §9.1, §10.16, §10.24, §3.3, §6.9, §7.5, §12.11, §12.13, §13.5

**D60. Added columns are registered.** Tables could already carry extra columns, but
agents had no way to learn what they meant. `index.md` gains an optional `## Columns`
table (file, table, column, meaning, values). Agents read it with the index. The file's
writer fills registered columns, so the one-writer rule is untouched, and a host warns
about columns that are not registered. → §10.0, §10.3, §11.6, §14.2

**D59. Serials can draft ahead.** The step-14 gate was also the release decision, so a
serial could not hold a buffer of finished chapters. Writing and releasing are now
separate: step 14 makes an installment ready, and the author releases it, in order,
whenever they choose. The buffer has no size limit, which covers authors who stay
months ahead and authors bringing in work written before they used LoreStore.
Unreleased chapters are revisable as in `novel`; only released ones are fixed forward.
Releasing is always the author's call, even under `gates: none`, because it cannot be
undone. → §13.3, §10.18, §10.23, §12.2, §14.2

**D58. Sapient peoples and fauna are kept apart.** It was unclear whether `species.md`
held only sapient peoples or every kind of creature, since Star Trek's species and Harry
Potter's creatures overlap. A world SHOULD put sapient peoples in `species.md` and
non-sapient fauna in a creatures catalog, and record any borderline choice in
`index.md`. → §3.4

**D57. Scenes are defined.** "A change of location or a break in continuous time" did
not cover a scene that ends because its situation changes, nor cross-cutting within one
exchange. A new scene now starts at a dramatic shift in location, time, or circumstance.
Cross-cutting between linked places is one scene, and in prose, section breaks are the
default scene breaks. → §4.2, §12.3

**D56. Interleaving overlapping series is shown.** §4.1 said episode-level segments give
an exact order for overlapping series, but never showed how. It now works through
*Deep Space Nine* premiering during *The Next Generation*'s sixth season, at season and
at episode level, and notes that splitting a segment is a major version bump. → §4.1

**D55. `Units` is renamed `Children`.** A column named `Units` under a table named
`Counts`, alongside the separate idea of a "source unit" in extraction, was confusing.
The column says how many children a node has, so it is now called that, in both the
Order and Counts tables. Supersedes the column name in D41. → §4.1, §10.4,
`tools/check.py`

## 0.1: naming

**D54. The project is named LoreStore.** "World System" was already taken. LoreStore
names what the spec defines (a store of dated, sourced canon) and works as a noun ("the
Harry Potter lorestore"). Use "LoreStore" in prose, and lowercase `lorestore` for
package, CLI, and directory names. The GitHub organization is `lorestore-dev`
(`lorestore` was taken), and the spec repository is `lorestore-dev/lorestore`.
Historical references to `world-system.md` below name the original source document
and are unchanged. → README, §1.1

## 0.1: review round 8

**D53. The beta-reader flags leftover TODO markers.** Every `TODO` marker still in the
prose is listed under `## Leftover markers` in its review, which is present even when
empty, and put first in its priorities. The showrunner routes each one as usual. This is
a late safety net: markers should have been resolved before continuity runs (step 11).
→ §12.18, §10.19, §11.9

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
`no-horcruxes` branch. → §4.4, §6.12, §7.2, §10.6, §10.8, §10.18, §11.8, §11.9, §12

## 0.1: review round 6

**D51. Branch or retelling: `setting.canon_mode`.** A project says whether canon after
its divergence point still happens:
- **`retelling`** (the default, and the previous behavior): later canon is the default
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
→ §6.6, §6.9, §6.11, §7.1, §10.1, §10.19, §11.8, §12, §13.4, §14

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
→ §13.3, §10.1, §10.8, §10.18, §10.22, §10.23, §11.10, `schemas/`

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
and removes Cedric's PoA appearances. → §6.8, §6.9, §10.19, §11.8, §13.4, §14.1

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
divergence end when the story catches up. → §6.8, §10.8, §10.21

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
permissive, it covers prose, schemas, and future code with one license, and its patent grant
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
