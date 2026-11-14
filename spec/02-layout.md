# 2. Layout and path resolution

## 2.1 The workspace

A workspace is a directory with up to six top-level folders:

```
<workspace>/
├── worlds/<world-id>/          # world packages: reusable canon, read-only to projects
├── universes/<universe-id>/    # crossover compositions of worlds (§8)
├── projects/<project-id>/      # stories
├── extraction/<world-id>/      # extraction workspace: source texts + extraction records
├── agents/                     # agent files (§11.3)
└── workflows/                  # workflow files (§11.7)
```

Ids (`<world-id>`, `<project-id>`, `<universe-id>`, character slugs, source ids) MUST
match `^[a-z0-9]+(-[a-z0-9]+)*$`. The id is the directory name.

## 2.2 The tiers: worlds, universes, projects

```
┌──────────────────────────────────────────────────────────────────────────┐
│  UNIVERSE  universes/<id>/   worlds + a bridge that reconciles them      │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │  WORLD    worlds/<id>/      reusable, READ-ONLY canon package     │   │
│   └──────────────────────────────────────────────────────────────────┘   │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │  PROJECT  projects/<id>/    one story: its story layer, prose,    │   │
│   │                             reviews, and divergence ledger        │   │
│   └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

A project's `project.yaml` MUST contain at most one of:

- `world:` a reference to one world package (the common case), or
- `universe:` a reference to a universe (a crossover), or
- neither, making it a **self-contained project** that owns its world layer in its own
  `bible/`.

A single-world project is the degenerate case of the universe model: one world, one
cutoff, no bridge.

## 2.3 World package

```
worlds/<world-id>/
├── world-config.yaml       # identity, version, status, canon basis, profiles (§10.2)
├── index.md                # endpoint registry (§10.3)
├── canon-timeline.md       # the ruler (§4)
├── sources.md              # source registry (§5)
├── glossary.md
├── world.md
├── …                       # the rest of the world layer (§3.3)
└── characters/
    ├── _roster.md          # cast + name registry
    └── <slug>.md           # one sheet per canon character
```

A world package contains **only** world-layer files (§3). It never contains source
texts, extraction records, manuscripts, or anything story-specific.

## 2.4 Extraction workspace

```
extraction/<world-id>/
├── texts/                  # the source material being extracted. Never shipped.
│   └── <work>/…
└── extractions/
    └── <work>/
        └── ch<NN>.md       # one extraction record per source unit (§10.6)
```

The extraction workspace sits outside the package so that a world package can be
shared without its source texts. Extraction records are the provenance trail behind
the package; they SHOULD be retained but are not part of it.

## 2.5 Project

```
projects/<project-id>/
├── project.yaml            # configuration (§10.1)
├── showrunner-log.md       # the showrunner's running plan (control file, never canon)
├── revisions.md            # serials only: changes to released installments (§10.23)
├── bible/                  # story layer (and, if self-contained, the world layer too)
│   ├── premise.md
│   ├── outline.md
│   ├── style.md
│   ├── canon.md            # established worlds: the adherence contract (§6.3)
│   ├── divergences.md      # established worlds: the divergence ledger (§6.4)
│   ├── canon-track.md      # established worlds: cutoff per chapter, project order (§6.7)
│   ├── timeline.md         # story-time events
│   └── characters/
│       ├── _roster.md      # this project's own (original) characters only
│       └── <slug>.md       # one sheet per original character
├── manuscript/
│   └── chapter-<NN>.md
├── reviews/                # advisory diagnostics, never canon
├── derived/                # rebuildable caches, never canon (§7.6)
├── references/             # user-supplied reference material for established worlds
└── runs/                   # orchestrator run records (format implementation-defined)
```

## 2.6 Agent paths and how they resolve

Agents name files with **agent paths**, which are relative to a **context**. There are
three contexts.

**Project context** (every workflow except extraction). Agent paths are rooted at the
project, with these prefixes:

| Agent path prefix   | Resolves to                                |
| ------------------- | ------------------------------------------ |
| `project.yaml`      | `projects/<p>/project.yaml`                |
| `showrunner-log.md` | `projects/<p>/showrunner-log.md`           |
| `bible/…`           | see the resolution rules below             |
| `manuscript/…`      | `projects/<p>/manuscript/…`                |
| `reviews/…`         | `projects/<p>/reviews/…`                   |
| `derived/…`         | `projects/<p>/derived/…`                   |
| `references/…`      | `projects/<p>/references/…`                |

**World context** (the extraction workflow, §13.6). Agent paths are rooted at the world:

| Agent path prefix | Resolves to                          |
| ----------------- | ------------------------------------ |
| `bible/…`         | `worlds/<w>/…`                       |
| `texts/…`         | `extraction/<w>/texts/…`             |
| `extractions/…`   | `extraction/<w>/extractions/…`       |

**Universe context** (the crossover workflow, §13.7). Agent paths are rooted at the
universe:

| Agent path prefix      | Resolves to                       |
| ---------------------- | --------------------------------- |
| `universe.yaml`        | `universes/<u>/universe.yaml`     |
| `bridge.md`            | `universes/<u>/bridge.md`         |
| `brief.md`             | `universes/<u>/brief.md`          |
| `bible/@<world-id>/…`  | `worlds/<world-id>/…` (read-only) |

In universe context only `bridge.md` is writable. The member worlds are read-only, as
they are to projects (§3.1).

### Resolving `bible/<path>` in project context

The host MUST resolve `bible/<path>` using the file catalog (§3.3), which gives every
path a layer:

1. **Self-contained project:** `projects/<p>/bible/<path>`.
2. **Project referencing one world** (`world:`):
   - a **story-layer** path resolves to `projects/<p>/bible/<path>`;
   - a **world-layer** path resolves to `worlds/<w>/<path>`;
   - `characters/<slug>.md` resolves to whichever side holds that slug. Slugs are
     unique across the union roster, so at most one side does;
   - a **union file** (§2.7) resolves to the union view.
3. **Project referencing a universe** (`universe:`):
   - world-layer paths MUST be world-qualified: `bible/@<world-id>/<path>` resolves to
     `worlds/<world-id>/<path>`, for any world in the universe;
   - `bible/bridge.md` resolves to `universes/<u>/bridge.md`;
   - story-layer paths resolve as in rule 2;
   - an unqualified world-layer path is an error.

`bible/@<world-id>/<path>` is also valid in a single-world project, and is equivalent to
the unqualified form.

### Writes

In project context, a write to an agent path that resolves into a world package or a
universe MUST be refused by the host (§3.1). A project MUST NOT hold a file at a
world-layer path in its own `bible/` when it references a world, because such a file
would shadow canon.

## 2.7 Union files

Three files exist on both sides of the boundary and are read as a **union**:

| File                    | World side holds                    | Project side holds                         |
| ----------------------- | ----------------------------------- | ------------------------------------------ |
| `characters/_roster.md` | canon characters (`origin: canon`)  | original characters (`origin: original`)   |
| `glossary.md`           | canon terms                         | terms the story introduces                 |
| `index.md`              | world-layer files                   | story-layer files                          |

The union view is the world's rows followed by the project's rows. A project row whose
key (slug, term, or path) already exists on the world side is an **error**, and the host
MUST report it. A project cannot redefine a canon name; to change what a canon name
means, it logs a divergence.

In a universe project the union spans every world in the universe. Rows from worlds
keep their world qualifier (`<world-id>:<slug>`), and collisions between worlds are
resolved by the bridge (§8.3).

## 2.8 World lifecycle and versioning

`world-config.yaml` carries a `status` and a `version`.

- **`status: open-for-extraction`**: the extraction pipeline is still adding canon.
- **`status: locked`**: extraction is complete.

A world package is read-only to every consuming project **in both states** (§3.1).

`version` is a semantic version. The extraction pipeline MUST bump it on every change
to a package:

| Bump      | When                                                                                               |
| --------- | -------------------------------------------------------------------------------------------------- |
| **major** | The ruler is reordered, a canon point is removed, a slug is renamed or removed, a source is removed |
| **minor** | Facts, works, sources, or files are added                                                          |
| **patch** | Values or citations are corrected without adding or removing anything                              |

A project pins the version it was written against (`world.version` in `project.yaml`).
When the package's version differs from the pin, the host MUST warn, and SHOULD
schedule a canon-keeper pass before further drafting. After a major bump the host
SHOULD NOT proceed until a human has re-pinned.

Keeping several versions of a package side by side is left to version control and is
out of scope.

## 2.9 Promoting a self-contained world

A self-contained project's world layer can become a shared package:

1. Copy every world-layer file (§3.3) from `projects/<p>/bible/` to `worlds/<w>/`.
2. Add `world-config.yaml` with `version: 1.0.0` and a `sources.md` registering the
   project as a `primary` source.
3. Replace the copied files in the project with a `world:` reference pinned to
   `1.0.0`.

From then on the package is read-only, including to the project it came from.
