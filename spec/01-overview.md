# 1. Overview

## 1.1 Purpose

LoreStore is a **file-based, model-agnostic canon store** for fiction, together
with the **agent framework** that reads and writes it. It represents a fictional world,
and the stories set in it, as a tree of small, addressable markdown files plus a few YAML
manifests. It needs no database, no API, and no vendor-specific model feature. The only
capabilities it assumes are: read a text file, send text to a language model, save the
reply to a file.

This specification is written for anyone implementing the system: in particular the
team building the **Integrated Writing Environment (IWE)**, which hosts the files,
orchestrates the agents, and enforces the contracts defined here.

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
   resolves to a tier and an attribution. This lets one world be read under different
   lenses and keeps a story blind to facts established after its cutoff.

## 1.4 The golden rule

> **The bible is canon. The manuscript is derived. Reviews are advisory.**
> When anything conflicts, the bible wins. If the story has outgrown the bible, the
> owning agent updates the bible *first*, then the prose follows.

For a project set in a shared world, "the bible" means **source canon, overridden going
forward by the project's divergence ledger** (§6).

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
| **World package**       | A reusable, read-only canon package in `worlds/<world-id>/`.                                                                   | §2         |
| **Universe**            | A composition of one or more worlds plus a bridge that reconciles them.                                                        | §8         |
| **Bridge**              | The universe file holding concept mappings and crossover-only canon.                                                           | §8         |
| **Project**             | One story, in `projects/<project-id>/`.                                                                                        | §2         |
| **Self-contained project** | A project that references no world and owns its own world layer.                                                            | §2         |
| **Bible**               | The canonical files a project reads: its own story layer plus the world layer it references (or owns).                        | §2, §3     |
| **World layer**         | Files describing the world, reusable across every story set in it.                                                             | §3         |
| **Story layer**         | Files specific to one story.                                                                                                   | §3         |
| **Ruler**               | `canon-timeline.md`: the ordered list of source works and their chapter counts.                                                | §4         |
| **Canon point**         | A path down the ruler's tree, optionally with a timecode: `PS:6`, `TOS:3:2:14`, `TOS:3:2:14+00:12:31`.                       | §4         |
| **Cutoff**              | The canon point a project is set at (`setting.canon_point`). Facts dated later are invisible to it.                            | §4, §7     |
| **State history**       | An append-only table of dated attribute values for one entity.                                                                 | §4         |
| **Source**              | A registered origin of facts (`books`, `fanon-hp`, …) with a tier and an attribution.                                          | §5         |
| **Tier**                | A source's authority class: `primary`, `secondary-official`, `fanon`, `fanfic`, `theory`, `crossover`.                         | §5         |
| **Profile**             | A named, ordered list of active sources, defined by a world and selected by a project.                                         | §5         |
| **Snapshot**            | The resolved state of an entity at a cutoff, under a profile, with the divergence ledger applied.                              | §7         |
| **Leak**                | A detail the snapshot hides that appears anyway: too late, from an inactive source, or from another frame or world.            | §6.9       |
| **Divergence**          | A logged, intended departure from source canon. Binding on the story from the chapter where it first occurs.                  | §6         |
| **Hidden truth**        | A canon fact already true at the cutoff (`True from`) but not yet revealed (`As of`). Only the author decides whether to use it. | §6.12      |
| **Branch / retelling**  | Whether canon after the divergence point never happens (branch) or still happens by default (retelling).                    | §6.6       |
| **Consequence**         | A ripple a divergence imposes on the rest of the story, tracked until absorbed.                                                | §6         |
| **Extraction pipeline** | The agents and steps that build a world package from source texts. The only writer of a world package.                        | §3, §13    |
| **Orchestrator**        | Whatever runs workflows: a human, a script, or the IWE.                                                                        | §11        |
| **Agent**               | A markdown file defining one narrow role with exactly one output per step.                                                     | §11, §12   |
| **Workflow**            | An ordered list of steps, each naming one agent and its inputs and output.                                                     | §11, §13   |
| **Gate**                | A step after which the orchestrator stops for human approval.                                                                  | §11        |
| **Module**              | An optional feature set enabled per project: frames, LitRPG, languages.                                                        | §9         |
| **Frame**               | The temporal context a character is bound by: the world frame (scene time and branch) or a traveler's personal frame.          | §9.1       |
