# 1. Overview

## 1.1 Purpose

LoreStore is a **file-based, model-agnostic canon store** for fiction, together
with the **agent framework** that reads and writes it. It represents a fictional world,
and the stories set in it, as a tree of small, addressable markdown files plus a few YAML
manifests. It needs no database, no API, and no vendor-specific model feature. The only
capabilities it assumes are: read a text file, send text to a language model, save the
reply to a file.

This specification is written for anyone implementing the system: in particular the
teams building **Integrated Writing Environments (IWEs)**, which host the files,
orchestrate the agents, and enforce the contracts defined here.

## 1.2 Scope

| Part                         | Chapters | Defines                                                                    |
| ---------------------------- | -------- | -------------------------------------------------------------------------- |
| **Canon store**              | 2–10     | Layout, layers, time, sources, divergence, the snapshot query, file formats |
| **Agent framework**          | 11–13    | The agent I/O contract, the agent roster, the workflows                    |
| **Implementation guidance**  | 14       | What a host application (the IWE) must do to conform                       |

Out of scope: the prose of individual agent files (`agents/*.md`), skill
implementations, model selection, and version-control tooling. This spec defines what
those artifacts must do, not their wording.

## 1.3 Defining properties

1. **Everything is a file.** Canon, state, provenance, and configuration are markdown or
   YAML. A host can treat the whole system as a folder tree it can diff, version, and
   ship.
2. **Facts are stateful and dated.** A world is a set of **append-only state histories**
   ordered along a source timeline. "What is true when I am writing" is a *query*
   (§7), not a stored value.
3. **Provenance is first-class.** Every fact carries the source it came from, which
   resolves to a tier and an attribution. This keeps a story blind to facts established
   after its cutoff.
4. **Canon is layered.** Canon, adaptations, fanon, fan works, theories, crossovers, and
   earlier books in a series are separate packages. A project stacks the ones it wants,
   so one world can be read through different stacks without any package changing.

## 1.4 The golden rule

> **The bible is canon. The manuscript is derived. Reviews are advisory.**
> When anything conflicts, the bible wins. If the story has outgrown the bible, the
> owning agent updates the bible *first*, then the prose follows.

For a project set in a shared world, "the bible" means **its stack of layers, resolved in
order, overridden going forward by the divergence ledgers** of any earlier books it
builds on and then its own (§6).

## 1.5 Conformance language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be
interpreted as described in RFC 2119. Text marked *Note* or *Example* is informative.

Examples throughout use two widely known franchises that represent the two main kinds
of world:

- **Harry Potter**, a **magic** world: seven novels with numbered chapters, spells and
  magical systems, and secrets revealed over time.
- **Star Trek**, a **technology** world: several series, with seasons and episodes,
  starships and species, and alternate timelines.

Together they exercise every feature: book and episode rulers, magic catalogs and
technology files, reveals, versions of characters, and time travel. They are
illustrative only.

## 1.6 Terms

| Term                    | Meaning                                                                                                                        | Defined in |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| **Package**             | A reusable, read-only bible in `worlds/<fandom>/<package>/`, of one kind: base, official, adaptation, fanon, fanfic, or theories. | §2.3       |
| **Base**                | A fandom's `base` package (id `<fandom>`). It relies on nothing and holds the ruler.                                           | §2.3       |
| **Layer**               | One entry in a project's stack: a package, a universe, or another project, each pinned.                                        | §2.2       |
| **Stack**               | A project's ordered list of layers, from the base up (`layers:` in `project.yaml`).                                            | §2.2       |
| **Lower / higher**      | Of layers: position in the stack. The base is the bottom, the project the top. Position alone never says which row wins.       | §2.2       |
| **Earlier / later**     | Of rows: position on the ruler, by as-of (§4.2). Never used of layers or tiers.                                                 | §2.2       |
| **Composed bible**      | `derived/bible/`: every layer of the stack merged into one view, each row keeping its layer and source.                       | §7.6       |
| **Universe**            | A layer that relies on two or more bases and reconciles them with a bridge.                                                    | §8         |
| **Bridge**              | The universe file holding concept mappings and crossover-only canon.                                                           | §8         |
| **Project**             | One story, in `projects/<project-id>/`.                                                                                        | §2         |
| **Self-contained project** | A project with no layers, which owns its own world layer.                                                                   | §2         |
| **Bible**               | The canonical files a project reads: its own files plus every layer in its stack.                                              | §2, §3     |
| **World layer**         | Files describing the world (characters, places, systems), in any package or project.                                           | §3         |
| **Story layer**         | Files specific to one story.                                                                                                   | §3         |
| **Ruler**               | A base's `canon-timeline.md`: the ordered list of source works and their chapter counts.                                       | §4         |
| **Ruler point**         | A path down the ruler's tree, optionally with a timecode: `PS:6`, `TOS:3:2:14`, `TOS:3:2:14+00:12:31`.                       | §4         |
| **Cutoff**              | The ruler point a project is set at (`setting.cutoff`). Facts dated later are invisible to it.                                 | §4, §7     |
| **Sync points**         | `bible/sync-points.md`: the cutoff for each manuscript chapter, for a story that keeps following its source.                   | §6.7       |
| **Adaptation timecode** | A timecode in an adaptation's own work, attached to a base ruler point: `PS:6:2+00:41:10`.                                     | §4.9       |
| **In-world date**       | When something happens in the world's own chronology, in the calendar its base or original project declares (`iso`, or a custom one). Separate from the ruler, which orders reading. | §4.13      |
| **World history**       | `history.md`: the world's past and off-page events, each an entity with a reserved `date`.                                    | §4.13      |
| **State history**       | An append-only table of dated attribute values for one entity.                                                                 | §4         |
| **Source**              | A registered origin of facts (`books`, `films`, …) with a tier and an attribution, local to its package.                       | §5         |
| **Tier**                | A source's class, ordered like the stack from the base up: `primary` (lowest), `secondary-official`, `adaptation`, `fanon`, `fanfic`, `theory`; also `crossover`, `story`, and `erratum`, outside that order. | §5.2       |
| **Resolution**          | How rows from different layers combine: `precedence` (the higher layer wins), `recency` (the later row wins), or `fill` (the lower layer wins; higher ones fill gaps). | §5.4       |
| **Snapshot**            | The resolved state of an entity at a cutoff, through the project's stack, with the divergence ledgers applied.                | §7         |
| **Leak**                | A detail the snapshot hides that appears anyway: too late, from a package not in the stack, or from another frame or world.    | §6.9       |
| **Divergence**          | A logged, intended departure from source canon. Binding on the story from the chapter where it first occurs.                  | §6         |
| **Hidden truth**        | A canon fact already true at the cutoff (`True from`) but not yet revealed (`As of`). Only the author decides whether to use it. | §6.12      |
| **Branch / retelling**  | Whether canon after the divergence point never happens (branch) or still happens by default (retelling).                    | §6.6       |
| **Consequence**         | A ripple a divergence imposes on the rest of the story, tracked until absorbed.                                                | §6         |
| **Theory conflict**     | Evidence that contradicts one claim of a theory a project adopts. Only the author decides which claims to keep.                | §6.13      |
| **Divergence conflict** | A later canon event, in a retelling, that a divergence in force makes impossible or changes. Only the author decides.          | §6.6       |
| **Order inversion**     | Two rows of one attribute's history that a project order reverses. Only the author decides how the story handles it.           | §6.8       |
| **Erratum**             | A source's acknowledged error, such as a corrected printing, kept for completeness under tier `erratum`. Never part of the lore. | §5.2       |
| **Chronology contradiction** | A date that contradicts its parent node, the ruler point that shows it, or a death before a birth. Invalid unless accepted; in a project, only the author accepts one. | §4.13      |
| **Seam conflict**       | An earlier book's item that a later book's chapter is set before, or a canon value the books' stacks resolve differently. Only the author decides. | §6.14      |
| **Extraction pipeline** | The agents and steps that build a package from source texts. The only writer of a package.                                    | §3, §13    |
| **Orchestrator**        | Whatever runs workflows: a human, a script, or the IWE.                                                                        | §11        |
| **Agent**               | A markdown file defining one narrow role with exactly one output per step.                                                     | §11, §12   |
| **Workflow**            | An ordered list of steps, each naming one agent and its inputs and output.                                                     | §11, §13   |
| **Author**              | The person a project belongs to, or any of the `authors` its `project.yaml` lists. Only the author makes the author-only decisions. | §11.13     |
| **Gate**                | A step after which the orchestrator stops for human approval.                                                                  | §11        |
| **Viewpoint**           | The character a chapter or scene is seen through, which limits what its narration may know. A narrator looking back is `told from` a later point. | §7.7       |
| **Module**              | An optional feature set enabled per project: frames, LitRPG, languages, travel, mysteries, lineage.                             | §9         |
| **Frame**               | The temporal context a character is bound by: the world frame (scene time and branch) or a traveler's personal frame.          | §9.1       |
