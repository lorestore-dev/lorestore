# Reviewing LoreStore

Thank you for reviewing the spec. You haven't seen it being written, and that's why
your review is useful: every rule here has so far been read only by the people who
wrote it. This guide says what to read, what to look for, and how to report what you
find.

## What LoreStore is

LoreStore stores a fictional world as small markdown and YAML files. Every fact about a
character or place is a dated row, with its source. Stories fork from canon without
editing it, and a team of narrow AI agents reads and writes the files. The core of it
is one query, the **snapshot**: what is true of this entity, as of this point in the
story, through this stack of layers ([§7](spec/07-snapshot.md)).

The spec is a draft (`0.4`). Breaking changes are still possible, so if a rule is
wrong, say so: nothing is fixed yet.

## Ground rules

- **The spec text is what's under review.** If a rule only makes sense once you've read
  [DECISIONS.md](DECISIONS.md) or the code in `tools/`, report that as a finding. The
  decisions are there if you want to know why a rule exists, but the text has to work
  without them.
- **Don't read [tools/check.py](tools/check.py) before you've finished.** It's one
  reading of the spec. If you implement from it, the review only tests whether you
  agree with that reading.
- **The examples are abridged on purpose.** The Harry Potter and Star Trek packages in
  `examples/` cover only what the cases need. Missing canon isn't a finding. A rule
  that gives the wrong answer on them is.

## Choose a track

### Track A: read the core

Read chapters 1–7 in order (about 2,600 lines), then skim chapter 10 for the file
formats. As you go, look for:

- **contradictions**: two rules that can't both hold;
- **gaps**: a case that no rule covers;
- **ambiguity**: a rule you could read two ways, where the two readings give different
  results;
- **unexplained terms**: a word used before it's defined, or never defined;
- **design doubts**: a rule that works but seems wrong, or too complex for what it buys.

### Track B: implement the snapshot

This track tests whether the spec can be implemented from the text alone. Write the
snapshot query ([§7.1–7.2](spec/07-snapshot.md#71-inputs)) in any language, against the
packages in [examples/worlds/](examples/worlds/). You'll need:

- ruler points and how they're ordered ([§4.2](spec/04-temporal.md#42-ruler-points));
- state histories ([§4.4](spec/04-temporal.md#44-state-histories)) and the table formats
  in [§10](spec/10-formats.md);
- source tiers and the three resolution modes ([§5.2](spec/05-sources.md#52-tiers),
  [§5.4](spec/05-sources.md#54-resolution));
- stacks and layers ([§2.2](spec/02-layout.md#22-layers-and-stacks)).

Then check your results against the expected answers in
[examples/README.md](examples/README.md). Work through the cases in this order, and stop
wherever you like:

1. Cases 1–11: one base, a time filter, resolution modes, relationships, and episodes as
   units.
2. Cases 14–17: a project order that rearranges canon (§6.7–6.8).
3. Cases 19–22: branches, retellings, and hidden canon (§6.6, §6.12).

Keep a list of every place where you had to guess. That list is the most useful part of
this track, and it matters more than how many cases you finish. When your answer
differs from an expected one, report it, even if you think the mistake is yours: one of
the spec, the example, or the expected answer needs to be clearer.

### Track C: the agent framework

This track is optional, and best taken after A. Read chapters 11–13 with one reference
agent from [agents/](agents/) and one workflow from [workflows/](workflows/). Then read
the recorded run in [examples/runs/](examples/runs/), where a model wrote a short story
from the files alone. Ask whether an agent given only its prompt could do its job, and
whether the gates leave the right decisions to the author.

## Already known

These aren't findings. Comments on them are still welcome.

- The checker covers only the bundled examples. It isn't a validator for other
  workspaces.
- The package registry in [CONTRIBUTING.md](CONTRIBUTING.md) doesn't exist yet, and its
  open questions are listed there.
- The tool-less loop finds a chapter's cast by name. A character the prose refers to
  only by pronoun drops out of the reviews' inputs
  ([examples/runs/](examples/runs/README.md)).

## Reporting

Open one [GitHub issue](https://github.com/lorestore-dev/lorestore/issues/new/choose)
per finding, using the **Review finding** form. It asks for:

- the `§` reference, and the rule quoted;
- what kind of problem it is;
- a concrete case: the files, the stack, the cutoff, what you expected, and what the
  spec gives.

A short finding is fine. "I couldn't tell what §4.4 means by X" is a good issue. If
you'd rather send all your notes as one document, open a single issue and attach it.

Findings go into draft 0.5. Each one that changes a rule gets an entry in
`DECISIONS.md`. Once you've responded, you'll be thanked by name in the README, unless
you'd rather not be.
