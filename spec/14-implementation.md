# 14. Implementing the system

This chapter states what a host (the IWE, or any orchestrator) must do to conform, and
summarizes the contracts the rest of the spec defines.

## 14.1 Host requirements

1. **The folder tree is the source of truth.** Packages, universes, and projects are
   directories. A host MUST be able to open, diff, and version them without a database.
   Any index it builds is a rebuildable cache (§11.6).
2. **Resolve paths and enforce the write boundary.** Resolve agent paths as in §2.6.
   Refuse writes into any layer of the stack from project context. Render layer files
   as read-only, and route any "change canon" action to the project's divergence ledger
   (§3.1).
3. **Implement the snapshot exactly** (§7). Given a stack, a resolution mode, a cutoff,
   and a manuscript position, resolve each entity, applying the ledgers of project
   layers and then the project's own. Offer `compose` and "materialize" actions that
   write `derived/` as a rebuildable cache.
4. **Offer the point list; don't make the writer type notation** (§4.3). Wherever a
   ruler point is chosen, offer the list derived from the ruler, and flag a typed point
   the ruler cannot name.
5. **Surface provenance.** Every displayed fact traces to its source, tier, as-of, and
   citation, and to the layer it came from, or to the divergence that overrides it. Let
   the user try another stack or resolution mode and see the resolved view change,
   without changing `project.yaml`.
6. **List reach candidates** in a retelling (§6.6): for each divergence in force, the
   canon rows on the attributes it overrides that it meets ahead. Show them beside the
   divergence audit, and mark each one the audit does not address. Likewise, for a project
   order, list the inversion candidates (§6.8) beside the order audit.
7. **Treat classifications as first-class states** (§6.9). Fix items, decide items, and
   leaks are distinct states with distinct resolutions. Block advancing past a chapter
   while a decide item for it is pending.
8. **Present author decisions as choices.** Order inversions (§6.8), divergence
   conflicts (§6.6), hidden canon (§6.12), theory conflicts (§6.13), and seam
   conflicts (§6.14) are the author's alone, and so are early access
   and release (§13.9, §13.3). Show the canon rows involved and the options with their
   fallout (§10.19), and let the author pick one or write their own. Never let an agent
   or `gates: none` resolve one. Keep the chosen resolution's open consequences in front
   of the author until each is absorbed.
9. **Be the orchestrator, not a participant.** Wire files in and out, honor gates, and
   surface artifacts. Never depend on what an agent does internally.
10. **Validate agent files** against the anatomy in §11.3, and check every output path
   against the file catalog in §3.3.
11. **Enforce one writer per file in the scheduler.** Refuse to run two steps that write
   the same file concurrently, and surface the conflict.
12. **Gates are a first-class state** with exactly three transitions: `approve`,
    `revise: <notes>`, `back: <step>` (§11.8).
13. **Collect review priorities** into a revision queue for the showrunner or the human.
14. **Route TODOs.** Find `TODO` markers in drafted prose. Offer to route each
    `needs bible` marker to the right builder before continuity runs, and present each
    `hidden canon` and `seam conflict` marker to the author as a
    decision (item 8),
    blocking the chapter until it is decided (§11.8).
15. **Budget context per step.** Estimate tokens (about characters ÷ 4) and warn when a
    slice would overflow the target model's window. Prefer snapshots to raw ledgers, one
    entity to a folder, and only the speakers and actors in a scene.
16. **Stay model-agnostic.** The same workflow must run against a cloud API, a local
    model in a loop, or a human with the files, without changing the agents or the
    store.
17. **Keep material apart from instructions** (§11.12). Pass what an agent reads to it
    as content, marked off from its agent file and the step's request, never merged
    into them. Treat a package, universe, or project layer from outside the author's
    workspace, source texts, and human feedback as untrusted: before an agent first
    reads one, SHOULD show the author any text in it that reads as an instruction to an
    agent.
18. **Check spec versions** (§10.0). Refuse a stack with a manifest whose
    `spec_version` the host does not support, and read each directory by its own
    version's rules.
19. **Show licenses and credit** (§2.10). When the author adds a package or universe to
    a stack, and wherever the host lists a stack's layers, show each layer's `license`
    and `credit`, and say plainly when a layer states no license.
20. **Know which author is acting** (§11.13). In a project with `authors`, take
    author-only decisions and gate signals only from a listed author, and record which
    one.

## 14.2 Validation

A host MUST detect and report each of the following. The column shows where each rule
is defined.

| Check                                                                            | Spec      |
| -------------------------------------------------------------------------------- | --------- |
| A manifest fails its JSON Schema                                                 | §10.1–2   |
| A ruler point is invalid for its ruler (its base's, or the series ruler)         | §4.2, §4.12 |
| Two points must be compared but are incomparable (timecode-only vs scene-only)   | §4.2      |
| Ruler segments overlap (one lies inside another)                                 | §4.1      |
| A row cites a source missing from `sources.md`                                   | §5.1      |
| A package's id does not match its folder, or its kind does not match its id's form | §2.3    |
| A package cites a source whose tier its kind does not allow (an `erratum` source in a fanon, fanfic, or theories package, say) | §2.3, §5.2 |
| A layer sits below a package it relies on, or a stack omits one                   | §2.2      |
| A project layer's package layer is not relisted, or is relisted at another major version or an older version | §2.2 |
| A universe's `relies-on` pins differ from its bases' pins in the stack, or two bases are stacked without a universe | §8.1 |
| A key in one layer collides with a lower layer's key                              | §2.7      |
| An extension sheet extends a package below it that is not in its `relies-on`, or names a slug that package does not define | §10.5 |
| A project holds an extension sheet                                                | §2.7      |
| A qualified quotation `ID` names a package below it in the stack that lacks that quotation | §10.13 |
| A project file shadows a layer path                                               | §2.6      |
| A write from project context resolves into a package, a universe, or a project layer | §3.1   |
| A package's version differs from the stack's pin                                  | §2.8      |
| An adaptation timecode on a point that no adaptation in the stack covers           | §4.9      |
| An `## Insert` row placed after an unknown segment, or an inserted work that repeats a work already on the ruler | §4.10, §4.12 |
| An `## Insert` table in a package that is not an `official` or `fanfic` package    | §4.10     |
| A point on a project layer's work past its pinned chapter                         | §4.12     |
| Two rows of one package share entity, attribute, tier, and point with different values (state rows or quotation columns) | §4.4 |
| A divergence has no consequence row                                              | §6.4      |
| An `Overrides` assignment names an unknown slug                                  | §6.4      |
| A consequence is `absorbed` without `Absorbed in`                                | §10.8     |
| A divergence's `Until` is not after its `First occurs`                           | §10.8     |
| A project order (`setting.order`) is not a permutation of the stack's segments, inserted ones included; the host also proposes a corrected order | §6.8 |
| A project order reverses two rows of one attribute's history (an order inversion) with no covering divergence | §6.8 |
| A sync point's cutoff is not a valid ruler point                                 | §6.7      |
| A branch's sync points or cutoff go past its divergence point                    | §6.6      |
| A branch has no divergence point (also rejected by the schema)                   | §6.6      |
| An established project with no package or project layer (also rejected by the schema) | §6.1 |
| An original project with any layer (also rejected by the schema)                  | §6.1      |
| A project layer is a branch, and the project is not a branch with a divergence point no later than the layer's | §6.14 |
| A Seam conflicts row whose item matches no item of an earlier book, a decision that does not fit its item, `other` with no note, or `keep-earlier` or `other` with no divergence | §10.8 |
| A chapter uses an earlier book's item that is ahead of it, with no seam decision | §6.14 |
| A row's `True from` is later than its `As of`, or not a valid ruler point        | §4.4      |
| A calendar that breaks §4.13 (no era, an era counting down that is not first or is last, an era counting up with no `years` that is not last, a month of no days), or a `calendar` or `notation` in a package that is not a base or a project that is not original, or a `notation` with a custom calendar | §4.13 |
| A date that does not parse, or names an era, month, or day its calendar lacks, or a range whose first date is after its second | §4.13 |
| A date in `## Dates`, `In-world`, or a timeline `Date` where the stack has no calendar | §4.13 |
| A `## Dates` node that is not on the file's own works, or appears twice; or a `## Dates` table in an adaptation | §10.4 |
| An event in `history.md` with no `date` row                                      | §4.13     |
| A chronology contradiction (`outside-parent`, `in-world-after`, `born-died`) with no `## Accepted` row for it in a layer that holds one of its rows or nodes | §4.13 |
| A route that names a place missing from `places.md` or is not in alphabetical order (`+`), a route attribute that is neither a mode nor `distance`, a mode defined twice, or a route value that is not a duration, `—`, or `(unset)` | §9.4, §10.26 |
| A timeline `Place` that is not in `places.md`                                    | §10.15    |
| A mystery that is not a secret in `knowledge.md`; a `Planted at` or `Revealed at` that is not a valid point or chapter; a clue with an unknown mystery or kind, or a duplicate id; a red herring marked needed | §10.27 |
| A higher layer that changes or removes a lower layer's clue                     | §10.27    |
| A `parents`, `guardians`, `descends-from`, or title `holder` value that is not a slug in the stack's roster | §9.6 |
| A lineage contradiction (`born-before-parent`, `ancestry-cycle`) with no `## Accepted` row for it in a layer that holds one of its rows | §9.6 |
| An `## Accepted` row with an unknown check, a subject the file does not hold, no reason, or, in a package, no citation | §10.5 |
| A universe offset between bases that do not declare the same calendar, or in a unit the calendar lacks | §8.1 |
| A story-dated row (`From chapter`) that has an `As of`, cites a source other than `project`, or describes an entity the project does not define | §4.11 |
| A Hidden canon decision of `reveal-early` with no divergence, or `other` with no note | §10.8 |
| A divergence's `Basis` cites a theory not in the stack, an unknown claim, or a discarded claim, or omits a kept or adapted one | §6.13 |
| A theory-conflict decision of `adapt` with no note                               | §10.8     |
| A write to a released installment in a serial whose releases are locked          | §13.3     |
| A chapter is released, re-released, sent to early access, or scheduled out of order, or with a pending decide item, a `TODO` marker, or (with `content_notes`) unconfirmed notes; any step in a run of chapters taken when one of them fails | §13.12 |
| A status or front-matter key outside its workflow (`released`, `re-released`, `withdrawn`, or `release-on` outside a serial); a `withdrawn` chapter that was never released; a re-release under locked releases of a chapter that was not withdrawn; a schedule key that is not a date or a date and time with its offset | §10.18, §13.12 |
| An `export/` folder that holds a chapter its audience does not have; an exported chapter with a comment or front matter left in; metadata without a `publishing` block, or naming a true identity before its reveal | §13.13, §10.30 |
| A `publishing.relationships` entry that is not two roster slugs joined by `+` or `/` | §10.1 |
| A renumbering moves a released or early-access chapter, or a chapter at or before another project's pin, or leaves a chapter id unrewritten | §13.10 |
| A change to an early-access chapter, or a revisable released one, with no `revisions.md` row or no reader note | §10.22 |
| A feedback file's `chapter` does not match its folder                            | §10.25    |
| A `license` that is not a valid SPDX license expression, or a `LicenseRef-` with no `LICENSE.md` beside the manifest | §2.10 |
| Two `authors` with the same id; a `By`, `early-access-by`, or `released-by` that is not an author's id; or, with two or more authors, one of them missing where it is required | §11.13, §10.8 |
| A content note in a project without `content_notes`; a `content-notes` id not in `content_notes`, or a `content-notes-suggested` entry that is neither an id there nor `new:<id>`; an early-access or released chapter with no `content-notes` | §13.11, §10.18 |
| An outline row with an unknown `Viewpoints` mode, or one not on its chapter's first row; a chapter in `chapter` mode without exactly one row and one viewpoint; a scene in `scene` mode without a viewpoint or `—`, or scenes not numbered from 1; a viewpoint in a `none` chapter; a viewpoint that is not a slug in the stack's roster | §10.23 |
| A `Told from` (in the outline, `parameters.told_from`, or a chapter) that is not a chapter id or `end`, is before its chapter, or is given where there is no viewpoint character | §7.7, §10.23 |
| A prompt file with an unknown `kind`, a subject that is not in the roster or `places.md`, an invalid `cutoff`, `position`, or `date`, or no `## Gaps` or `## Sources` | §10.29 |
| A `time-travel.md` entry has no `model`, or an unknown model or free-will value  | §10.24    |
| A traveler leg names a mechanism missing from `time-travel.md`                   | §10.16    |
| A world point names a branch missing from `branches.md`, or a branch has an unknown status | §10.16 |
| A `## Columns` row repeats a required column of its table                        | §10.3     |
| A consequence is `accepted` without a `Note`, or outside a locked serial         | §10.8     |
| Two concurrent steps write the same file                                         | §11.5     |
| An agent writes a file that §3.3 does not list it as writing                     | §3.3      |
| A universe project uses an unqualified world-layer path                          | §2.6      |

A host SHOULD also warn when a project used as a layer changes at or before its pinned
chapter (§2.2), when the composed bible or a materialized snapshot is
stale (§7.6), when a project's sync points go backwards
(§6.7), when a scene with no travelers is set later than its chapter's sync point
(§7.5), when a story event's date falls outside the lifetime of an entity it lists, or
before its chapter's cutoff date (§4.13), when timecodes in one episode or film
contradict its scene order (§4.2), when a table has an added column that `index.md`
does not register (§10.0), when a chapter as drafted records a different viewpoint mode
or viewpoint from its outline row (§7.7), when a journey is faster than the routes allow (§9.4), when
a mystery is unfair (§9.5), when a parent is under 12 at a birth, a child is born more
than a year after a parent's death, or a title is held outside its holder's lifetime
(§9.6), when a chapter readers have lacks a listed note its
`content-notes-suggested` names (§13.11), and when the author releases a serial chapter that is not
ready, or sends one to early access that is not `line-edited` (§13.3, §13.9).

**Example cases:** the [validation cases](../examples/README.md#validation-cases).

## 14.3 The contracts, summarized

| Contract                 | Rule                                                                                                           | Enforced by                                              | Spec  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ----- |
| **Golden rule**          | The bible is canon; the manuscript is derived; reviews are advisory.                                           | Every agent; the host's precedence model                 | §1.4  |
| **Write boundary**       | Layers are read-only to projects; only extraction writes packages; projects fork through the ledger.           | The host; agent guardrails                               | §3.1  |
| **Layers**               | A stack lists every layer with its pin, from the base up; a layer adds keys but never redefines a lower layer's.  | The host; merger; `compose`                              | §2.2, §2.7 |
| **Provenance**           | Every fact carries value, as-of, source, and citation.                                                         | Extractor, merger, canon-keeper                          | §4.4  |
| **Temporal**             | Append-only state histories; "true when writing" is a query.                                                   | The snapshot; drafter; canon-keeper                      | §4, §7 |
| **Resolution**           | The project's resolution mode combines the stack's rows; packages outside the stack are leaks.                 | `project.yaml`; the snapshot; canon-keeper               | §5    |
| **Divergence**           | The ledger overrides source canon from the chapter it first occurs; every entry lists consequences.           | Canon-keeper detects; showrunner or human decides; curator logs | §6 |
| **One output**           | Each step writes exactly one file.                                                                             | The orchestrator; agent `Writes`                         | §11.4 |
| **One writer per file**  | Steps that write the same file run sequentially.                                                               | The orchestrator; showrunner                             | §11.5 |
| **Retrieval**            | Load the slice, not the whole bible.                                                                           | The orchestrator; context budgeting                      | §11.6 |
| **Gate**                 | A gate stops for `approve`, `revise`, or `back`; decide items block regardless of policy.                      | The orchestrator; `project.yaml`                         | §11.8 |
| **Diagnose vs. rewrite** | Reviewers write `reviews/`; only a file's owner rewrites it.                                                   | Agent guardrails                                         | §12   |
| **Model-agnostic**       | The orchestrator wires files and honors gates without understanding agents.                                   | The host                                                 | §11.1 |
