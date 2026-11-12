# 11. The agent contract

This chapter defines the one convention every agent obeys. It is what makes the
framework model-agnostic: an orchestrator never needs to understand what an agent
does, only which files it reads and writes.

If you can (a) read a text file, (b) send text to a language model, and (c) save the
reply to a file, you can run this framework. No tool calling, function APIs, or
vendor-specific features are required.

## 11.1 The loop

An **orchestrator** (a human, a short script, or the IWE) executes a **workflow**: an
ordered list of **steps**. Each step names one agent, the agent paths it reads, and the
one agent path it writes. For each step the orchestrator:

1. Reads the agent file (`agents/<agent>.md`).
2. Resolves the step's reads to concrete files (§2.6) and selects the slice it needs
   (§11.6).
3. Sends the model the agent file, then the inputs, then the **standing instruction**:
   > Produce the artifact described in your **Writes** section. Output only the file
   > contents.
4. Checks the write is permitted (§3.1), then saves the reply to the resolved output path.
5. Applies the gate policy (§11.8).

```
project  = load("projects/<p>/project.yaml")
workflow = compose(load_workflow(project.workflow), overlays_for(project))
for step in workflow.steps:
    for instance in expand(step.repeat):           # per chapter, per character, …
        agent  = read("agents/" + step.agent + ".md")
        inputs = slice(resolve(step.reads, instance))
        reply  = model(agent + inputs + STANDING_INSTRUCTION)
        path   = resolve(step.writes, instance)
        assert writable(path, context)              # §3.1
        write(path, reply)
        if gate_applies(step, project.gates):
            wait_for_gate_signal()                  # approve | revise | back
```

## 11.2 Contexts

Every step runs in exactly one context (§2.6): **project context**, rooted at a
project; **world context**, rooted at a world package and its extraction workspace; or
**universe context**, rooted at a universe.
The workflow declares its context. Paths in agent files and workflow files are agent
paths, never workspace paths.

## 11.3 Anatomy of an agent file

Every file in `agents/` has these sections, in this order:

| Section            | Purpose                                                                       |
| ------------------ | ----------------------------------------------------------------------------- |
| `# Agent: <name>`  | Identifier. Matches the filename.                                             |
| `## Role`          | One paragraph: the agent's mandate and nothing beyond it.                     |
| `## Reads`         | Agent paths or globs, each with a reason. A retrieval spec (§11.6).           |
| `## Writes`        | The output path. One per mode; exactly one per step (§11.4).                  |
| `## Done when`     | Checkable conditions that mean the artifact is complete.                      |
| `## Process`       | The step-by-step method.                                                      |
| `## Output format` | The template the output must follow, referencing §10 where one applies.       |
| `## Guardrails`    | What the agent must *not* do.                                                 |

An agent with several modes (the worldbuilder, for example) lists its possible outputs
under `## Writes`. The workflow step chooses which one that step produces.

## 11.4 The one-output rule

**Each step writes exactly one file.** Steps then compose cleanly, and re-running a step
overwrites one predictable target. Work that spans many files (polishing every chapter,
merging every bible file) is a **repeated step** (`Repeat`, §11.7): one instance per
file.

## 11.5 One writer per file

When several agents can write the same file (the drafter, line-editor, and dialogue
agent all touch a chapter), the orchestrator MUST schedule their steps
**sequentially, never concurrently**. Agents that only diagnose write to `reviews/` and
hand their fixes to the agent that owns the file. Each file's owners are listed in §3.3.

Parallel instances of a repeated step are safe only when each writes a different file,
as in extraction (§13.6).

## 11.6 Retrieval: load the slice, not the whole bible

An agent pulls only the data its step needs. This keeps each call small, focused, and
cheap, and lets the framework scale to long novels and multi-season serials.

The bible is decomposed into small addressable units (one file per character, ledger
entries as rows) precisely so a slice can be loaded without its neighbours. A `Reads`
section is a **retrieval spec, not a "load everything" list**:

- Prefer the narrowest path that covers the job: `bible/characters/hermione-granger.md`,
  not `bible/characters/**`, when only she is in the scene.
- Prefer a **snapshot** (§7) to raw state histories.
- Prefer the rows that apply (the open consequences touching this chapter) to the whole
  ledger.
- Read `bible/index.md` first to learn which files exist.

Two ways to retrieve, both file-only:

- **Tool-capable runtime:** the agent fetches its own slice at run time with read or
  search tools, guided by its `Reads`.
- **Tool-less loop:** the orchestrator resolves the `Reads` to the concrete slice and
  passes only that.

**Sanctioned exception:** the whole-book reviewers (pacing-analyst, critic,
beta-reader) read the manuscript in full and in order, because judging the whole is
their job. They still do not load the bible.

> **Derived index.** Cross-cutting queries that globbing handles poorly, such as "every
> open consequence touching a scene after chapter 10" or "every scene these two
> characters share", justify an optional derived index (SQLite or JSON) built from the
> files by the host. It is a rebuildable cache (§3.1, W5); agents still read files.
> Defer it until a project's scale demands it.

## 11.7 Workflow files

A workflow is a markdown file, `workflows/<id>.md`, with front matter and a steps table:

```markdown
---
id: novel
kind: chain          # chain | overlay
context: project     # project | world | universe
---
## Steps
| Step | Agent     | Reads                      | Writes             | Gate      | Repeat |
| ---- | --------- | -------------------------- | ------------------ | --------- | ------ |
| 1    | architect | project.yaml               | bible/premise.md   | milestone |        |
```

- `Gate`: `milestone` or empty (§11.8).
- `Repeat`: empty, or one of `per-arc`, `per-chapter`, `per-character`, `per-file`, `per-unit`,
  `per-target`. The instance value substitutes into placeholders in `Reads` and
  `Writes` (`<NN>`, `<slug>`, `<file>`, `<work>`, `<target>`).
- A **phase** is a group of steps that repeats together (the per-chapter drafting loop).
  Mark it with a `### Phase <n> — <name> (repeat: <kind>)` heading above its table.

An **overlay** adds a `Position` column after `Repeat`, with the value
`before <step>`, `after <step>`, or `replace <step>`. Overlays apply in the order
established-world, then frames.

## 11.8 Gates

`project.yaml` sets the gate policy:

| `gates`      | The orchestrator stops after                  |
| ------------ | --------------------------------------------- |
| `none`       | no step                                       |
| `milestones` | every step whose `Gate` is `milestone`        |
| `all`        | every step                                    |

At a gate, the orchestrator surfaces the new artifact and waits for one of exactly
three signals:

- **`approve`**: continue to the next step.
- **`revise: <notes>`**: re-run the same step with the notes appended to its inputs.
- **`back: <step>`**: return to an earlier step (for example, the outline needs
  rework).

Gates are separate from **decisions** (§6.9): a pending decide item blocks progress
past its chapter under every gate policy. Under `gates: none` the showrunner makes the
decision; otherwise a human does. **Order inversions** (§6.8), **divergence
conflicts** (§6.6), and **hidden canon** (§6.12) are the exception: they are always the
author's decision, and wait for the author even under `gates: none`.

## 11.9 Signals between agents

Agents communicate only through files, using these conventions:

| Signal               | Written by          | Form                                         | Consumed by                                   |
| -------------------- | ------------------- | -------------------------------------------- | --------------------------------------------- |
| Missing canon        | drafter             | `<!-- TODO: needs bible: … -->` (§10.19)     | showrunner, which routes it to a builder      |
| Hidden canon         | drafter             | `<!-- TODO: hidden canon: … -->` (§10.19)    | showrunner, which surfaces it to the author   |
| Leftover markers     | beta-reader         | `## Leftover markers` (§10.20)               | showrunner, which routes each marker as above |
| Review priorities    | every reviewer      | `## Priorities` (§10.20)                     | showrunner, which schedules revisions         |
| Canon findings       | canon-keeper        | `## Findings` with a class (§10.20)          | showrunner and the human, for decide items    |
| Needs a human        | extractor           | `## Needs a human` (§10.6)                   | the human at the next extraction gate         |
| Merge conflicts      | merger              | `## Unresolved conflicts` in its target      | the human at the next extraction gate         |
| Chapter status       | drafter, line-editor | front-matter `status` (§10.19)              | the host and the showrunner                   |

## 11.10 Skills

**Skills** are deterministic procedures the orchestrator runs as steps. They are not
language-model agents, but they obey the same one-output rule:

| Skill               | Writes                     | Does                                                         |
| ------------------- | -------------------------- | ------------------------------------------------------------ |
| `temporal-snapshot` | `derived/as-of-….md`       | Materializes a snapshot (§7.6)                               |
| `world-index`       | `bible/index.md`           | Lists every file on its side, with its layer from §3.3       |
| `cite`              | the requested output file  | Renders `sources.md` bibliography entries as APA, MLA, or Chicago |
| `release`           | `manuscript/chapter-<NN>.md` | Serial only: sets the chapter's front matter to `status: released` and `released: <date>` (§13.3) |

## 11.11 Writing a new agent

Add a file to `agents/` following §11.3, add it to the file catalog (§3.3) for every
file it writes, and reference it from a workflow step. Keep the mandate narrow.

Checklist:

- [ ] `# Agent: <name>` matches the filename.
- [ ] `## Role` is one paragraph.
- [ ] `## Reads` names concrete paths or narrow globs, each with a reason.
- [ ] `## Writes` names one path per mode, and each is in §3.3 with this agent as a
      writer.
- [ ] `## Done when` states checkable conditions.
- [ ] `## Output format` references §10 wherever a format exists.
- [ ] `## Guardrails` states what the agent must not do.
- [ ] Some workflow step uses it.
- [ ] If it writes a file another agent also writes, every workflow schedules them
      sequentially.
