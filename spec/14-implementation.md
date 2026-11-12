# 14. Implementing the system

This chapter states what a host (the IWE, or any orchestrator) must do to conform, and
summarizes the contracts the rest of the spec defines.

## 14.1 Host requirements

1. **The folder tree is the source of truth.** Worlds, universes, and projects are
   directories. A host MUST be able to open, diff, and version them without a database.
   Any index it builds is a rebuildable cache (§11.6).
2. **Resolve paths and enforce the write boundary.** Resolve agent paths as in §2.6.
   Refuse writes into world packages from project context. Render world-layer files as
   read-only, and route any "change canon" action to the project's divergence ledger
   (§3.1).
3. **Implement the snapshot exactly** (§7). Given a cutoff, a profile, and a manuscript
   position, resolve each entity. Offer a "materialize" action that writes `derived/` as
   a rebuildable cache.
4. **Offer the point list; don't make the writer type notation** (§4.3). Wherever a
   canon point is chosen, offer the list derived from the ruler, and flag a typed point
   the ruler cannot name.
5. **Surface provenance.** Every displayed fact traces to its source, tier, as-of, and
   citation, or to the divergence that overrides it. Let the user switch the active
   profile and see the resolved view change.
6. **Treat classifications as first-class states** (§6.9). Fix items, decide items, and
   leaks are distinct states with distinct resolutions. Block advancing past a chapter
   while a decide item for it is pending.
7. **Present author decisions as choices.** Order inversions (§6.8), divergence
   conflicts (§6.6), and hidden canon (§6.12) are the author's alone. Show the canon
   rows involved and the options with their fallout (§10.20), and let the author pick
   one or write their own. Never let an agent or `gates: none` resolve one. Keep the
   chosen resolution's open consequences in front of the author until each is absorbed.
8. **Be the orchestrator, not a participant.** Wire files in and out, honour gates, and
   surface artifacts. Never depend on what an agent does internally.
9. **Validate agent files** against the anatomy in §11.3, and check every output path
   against the file catalog in §3.3.
10. **Enforce one writer per file in the scheduler.** Refuse to run two steps that write
   the same file concurrently, and surface the conflict.
11. **Gates are a first-class state** with exactly three transitions: `approve`,
    `revise: <notes>`, `back: <step>` (§11.8).
12. **Collect review priorities** into a revision queue for the showrunner or the human.
13. **Route TODOs.** Find `TODO: needs bible` markers in drafted prose and offer to route
    each to the right builder before continuity runs.
14. **Budget context per step.** Estimate tokens (about characters ÷ 4) and warn when a
    slice would overflow the target model's window. Prefer snapshots to raw ledgers, one
    entity to a folder, and only the speakers and actors in a scene.
15. **Stay model-agnostic.** The same workflow must run against a cloud API, a local
    model in a loop, or a human with the files, without changing the agents or the
    store.

## 14.2 Validation

A host MUST detect and report each of the following. The column shows where each rule
is defined.

| Check                                                                            | Spec      |
| -------------------------------------------------------------------------------- | --------- |
| A manifest fails its JSON Schema                                                 | §10.1–2   |
| A canon point is invalid for its world's ruler                                   | §4.2      |
| Two points must be compared but are incomparable (timecode-only vs scene-only)   | §4.2      |
| Ruler segments overlap (one lies inside another)                                 | §4.1      |
| A row cites a source missing from `sources.md`                                   | §5.1      |
| A profile includes an excluded source                                            | §5.3      |
| A project defines or modifies a profile                                          | §5.4      |
| A union-file key collides with the world side                                    | §2.7      |
| A project file shadows a world-layer path                                        | §2.6      |
| A write from project context resolves into a world package or universe           | §3.1      |
| The world package's version differs from the project's pin                       | §2.8      |
| Two state rows share entity, attribute, source, and point with different values  | §4.4      |
| A divergence has no consequence row                                              | §6.4      |
| An `Overrides` assignment names an unknown slug                                  | §6.4      |
| A consequence is `absorbed` without `Absorbed in`                                | §10.8     |
| A divergence's `Until` is not after its `First occurs`                           | §10.8     |
| A project order is not a permutation of the world's segments                     | §6.8      |
| A project order reverses two rows of one attribute's history (an order inversion) with no covering divergence | §6.8 |
| A canon-track cutoff is not a valid canon point                                  | §6.7      |
| A branch's canon track or cutoff goes past its divergence point                  | §6.6      |
| A branch has no divergence point (also rejected by the schema)                   | §6.6      |
| A row's `True from` is later than its `As of`, or not a valid canon point        | §4.4      |
| A Hidden canon decision of `reveal-early` with no divergence, or `other` with no note | §10.8 |
| A write to a released installment in a serial whose releases are locked          | §13.3     |
| A consequence is `accepted` without a `Note`, or outside a locked serial         | §10.8     |
| Two concurrent steps write the same file                                         | §11.5     |
| An agent writes a file that §3.3 does not list it as writing                     | §3.3      |
| A universe project uses an unqualified world-layer path                          | §2.6      |

A host SHOULD also warn when a profile's order inverts tier order (§5.2) and when a
materialized snapshot is stale (§7.6), when a canon track's cutoffs go backwards
(§6.7), and when timecodes in one episode or film
contradict its scene order (§4.2).

## 14.3 The contracts, summarized

| Contract                 | Rule                                                                                                           | Enforced by                                              | Spec  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ----- |
| **Golden rule**          | The bible is canon; the manuscript is derived; reviews are advisory.                                           | Every agent; the host's precedence model                 | §1.4  |
| **Write boundary**       | Worlds are read-only to projects; only the extraction pipeline writes them; projects fork through the ledger.  | The host; agent guardrails                               | §3.1  |
| **Provenance**           | Every fact carries value, as-of, source, and citation.                                                         | Extractor, merger, canon-keeper                          | §4.4  |
| **Temporal**             | Append-only state histories; "true when writing" is a query.                                                   | The snapshot; drafter; canon-keeper                      | §4, §7 |
| **Precedence**           | Profiles order active sources; inactive sources are leaks.                                                     | `world-config.yaml`; the snapshot; canon-keeper          | §5    |
| **Divergence**           | The ledger overrides source canon from the chapter it first occurs; every entry lists consequences.           | Canon-keeper detects; showrunner or human decides; curator logs | §6 |
| **One output**           | Each step writes exactly one file.                                                                             | The orchestrator; agent `Writes`                         | §11.4 |
| **One writer per file**  | Steps that write the same file run sequentially.                                                               | The orchestrator; showrunner                             | §11.5 |
| **Retrieval**            | Load the slice, not the whole bible.                                                                           | The orchestrator; context budgeting                      | §11.6 |
| **Gate**                 | A gate stops for `approve`, `revise`, or `back`; decide items block regardless of policy.                      | The orchestrator; `project.yaml`                         | §11.8 |
| **Diagnose vs. rewrite** | Reviewers write `reviews/`; only a file's owner rewrites it.                                                   | Agent guardrails                                         | §12   |
| **Model-agnostic**       | The orchestrator wires files and honours gates without understanding agents.                                   | The host                                                 | §11.1 |
