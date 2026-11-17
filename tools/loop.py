"""A minimal tool-less loop (§11.1, §11.6): runs a project's workflow with any model.

Usage:
    python tools/loop.py PROJECT_DIR [--worlds DIR] [--model CMD] [--approve]
                         [--skip STEP=REASON ...] [--signal SIGNAL]

For each step, the loop reads the agent file, resolves the step's Reads to concrete
slices, and sends the model the agent file, then the inputs, then the standing
instruction. The model gets no tools: everything it sees is in the prompt. The loop
checks the write (§3.1), saves the reply, and stops at the gates the policy requires
(§11.8).

The model is any command that reads a prompt on stdin and prints its reply (--model).
Without one, the loop runs in exchange mode: it writes each prompt to
runs/<run>/<n>-<step>.prompt.md and stops; a person, or any model, writes the reply
beside it as <n>-<step>.reply.md, and running the loop again picks it up.

It is a reference, not a host. It runs the chain straight through, once: when the
showrunner schedules a revision, re-run the loop with --from. Step conditions written
only in a workflow's notes are decided here by the predicates in WHEN, or by --skip.
Snapshots come from the checker's reference implementation (tools/check.py, §7), at the
project's cutoff, without its own ledger's overrides: the agents read the ledger.
"""
import argparse, contextlib, io, json, pathlib, re, shutil, subprocess, sys, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
STANDING = ("Produce the artifact described in your **Writes** section, for the step above. "
            "Output only the file contents.")
SKILLS = {"compose"}

# --- workflow files (§11.7) ------------------------------------------------------
def tables(text):
    out, cur = [], []
    for l in text.splitlines() + [""]:
        if l.startswith("|"): cur.append(l); continue
        if cur:
            cells = [[c.strip() for c in re.split(r"(?<!\\)\|", x)[1:-1]] for x in cur]
            out.append([dict(zip(cells[0], r)) for r in cells[2:]]); cur = []
    return out
def workflow(wid):
    text = (ROOT / "workflows" / f"{wid}.md").read_text(encoding="utf-8")
    steps = text.split("\n## Steps", 1)[1].split("\n## ", 1)[0]
    return [r for t in tables(steps) for r in t]
def compose_workflow(y):
    """The chain with its overlays applied, established-world first, then frames (§11.7)."""
    steps = workflow(y["workflow"]); setting = y.get("setting", {})
    overlays = (["established-world"] if setting.get("type") == "established" else []) + \
               (["frames"] if setting.get("temporal_model") == "frames" else [])
    for ov in overlays:
        for r in workflow(ov):
            how, anchor = r["Position"].split(" ", 1)
            at = next((i for i, s in enumerate(steps) if s["Step"] == anchor), None)
            if at is None: continue                       # a step only some chains have (§11.7)
            if how == "replace": steps[at] = r
            else: steps.insert(at + (how == "after"), r)
        text = (ROOT / "workflows" / f"{ov}.md").read_text(encoding="utf-8")
        if "\n## Added reads" in text:                    # the overlay's added reads (§11.7)
            for t in tables(text.split("\n## Added reads", 1)[1].split("\n## ", 1)[0]):
                for r in t:
                    for s in steps:
                        if s["Step"] == r["Step"]: s["Reads"] = f"{s['Reads']}; {r['Reads']}"
    return steps

# --- step conditions: what the workflows' notes say, as predicates ---------------------
def ledger_cites_theory(p):
    f = p / "bible" / "divergences.md"
    return f.exists() and any(r.get("Basis") for t in tables(f.read_text(encoding="utf-8")) for r in t)
def audit_entries(p):
    f = p / "reviews" / "canon.md"
    return f.exists() and re.search(r"^### [ICQS]\d+ ", f.read_text(encoding="utf-8"), re.M)
def decide_findings(p):
    f = p / "reviews" / "canon.md"
    return f.exists() and any(r.get("Resolution") == "decide" for t in tables(f.read_text(encoding="utf-8")) for r in t)
WHEN = {
    "E1a": (lambda y, p: "order" in y["setting"], "the project has its own order"),
    "E1b": (lambda y, p: any(str(l).startswith("project:") for l in y.get("layers", [])), "the project has project layers"),
    "E2a": (lambda y, p: y["setting"].get("follow") == "retelling" or ledger_cites_theory(p), "a retelling, or a divergence's Basis cites a theory"),
    "E2b": (lambda y, p: bool(audit_entries(p)), "E2a raised entries for the author"),
    "E5":  (lambda y, p: decide_findings(p), "E4 had a decide item to accept"),
    "T1":  (lambda y, p: y["setting"].get("type") != "established", "the project is not established-world"),
}

# --- the composed bible (§7.6) ------------------------------------------------------
def pkg_dir(worlds, ref):
    ident = ref.split("@")[0]; fandom, *rest = ident.split("/")
    return worlds / fandom / ("/".join(rest) if rest else "base"), ident
def with_layer(text, layer):
    out, in_table, header = [], False, False
    for l in text.splitlines():
        if l.startswith("|"):
            if not in_table: out.append(l + " Layer |"); in_table, header = True, True; continue
            if header: out.append(l + " ----- |"); header = False; continue
            out.append(l + f" {layer} |"); continue
        in_table = False
        out.append(l)
        if re.match(r"^### \S+ — ", l): out.append(f"- layer: {layer}")
    return out
def merge(chunks):
    """Union of one path across layers (§7.6): sections in order of first appearance; a
    table's rows join the first table under the same heading with the same header."""
    sections = {}                                         # heading -> items
    for lines in chunks:
        head, i = "", 0
        while i < len(lines):
            l = lines[i]
            if l.startswith("#") and not l.startswith("### "):
                head = l; sections.setdefault(head, []); i += 1; continue
            items = sections.setdefault(head, [])
            if l.startswith("|"):
                j = i
                while j < len(lines) and lines[j].startswith("|"): j += 1
                tab = next((x for x in items if isinstance(x, list) and x[0] == l), None)
                if tab: tab += lines[i + 2:j]
                else: items.append(lines[i:j])
                i = j; continue
            if l.strip() or (items and items[-1] != ""): items.append(l)
            i += 1
    out = []
    for head, items in sections.items():
        while items and items[-1] == "": items.pop()
        if head: out += ["", head] if out else [head]
        for n, x in enumerate(items):
            if isinstance(x, list): out += x + ([""] if n + 1 < len(items) and items[n + 1] != "" else [])
            else:
                if n == 0 and head and x.strip(): out.append("")
                out.append(x)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
def compose(project, y, worlds):
    """The compose skill (§11.10): derived/bible/, rebuilt from the stack and bible/."""
    layers = [pkg_dir(worlds, ref) for ref in y.get("layers", [])] + [(project / "bible", "project")]
    paths = {}
    for d, layer in layers:
        if not d.exists(): continue
        for f in sorted(d.rglob("*.md")):
            if f.name in ("LICENSE.md",): continue
            paths.setdefault(f.relative_to(d).as_posix(), []).append((f, layer))
    out = project / "derived" / "bible"
    if out.exists(): shutil.rmtree(out)
    for rel, srcs in paths.items():
        chunks = []
        for f, layer in srcs:
            text = f.read_text(encoding="utf-8")
            if text.startswith("---"): _, fm, text = text.split("---", 2); text = text.lstrip("\n")
            chunks.append(with_layer(text, layer))
        fm = ""
        first = srcs[0][0].read_text(encoding="utf-8")
        if first.startswith("---"): fm = "---" + first.split("---", 2)[1] + "---\n"
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        (out / rel).write_text(fm + merge(chunks), encoding="utf-8")
    head = ["# Composed bible", "", "| Layer | Version |", "| ----- | ------- |"]
    head += [f"| {ref.split('@')[0]} | {ref.split('@')[1]} |" for ref in y.get("layers", [])]
    head += ["| project | the project's own `bible/`, as of this build |", "",
             f"Resolution: {y.get('resolution', 'precedence')}. Order: {y['setting'].get('order', 'the ruler')}."]
    (out / "_composed.md").write_text("\n".join(head) + "\n", encoding="utf-8")
    return sorted(paths)

# --- snapshots, from the checker's reference implementation (§7) -----------------------
def checker():
    """check.py's helpers. It ends with sys.exit, so run it into a namespace we keep."""
    path = ROOT / "tools" / "check.py"
    saved, sys.argv = sys.argv, [str(path)]
    ns = {"__name__": "lorestore_check", "__file__": str(path)}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
    except SystemExit: pass
    finally: sys.argv = saved
    return ns
_CHECKER = None
def snapshots(y, cast):
    global _CHECKER
    _CHECKER = _CHECKER or checker()
    stack = _CHECKER["Stack"](y.get("layers", []), y.get("resolution", "precedence"))
    cutoff = y["setting"].get("cutoff"); out = []
    for slug in cast:
        snap = _CHECKER["snapshot"](stack, slug, cutoff)
        hidden = _CHECKER["hidden"](stack, slug, cutoff)
        out.append(f"### {slug}, at {cutoff}\n| Attribute | Value |\n| --------- | ----- |\n" +
                   "".join(f"| {a} | {v} |\n" for a, v in sorted(snap.items())) +
                   (f"\nHidden truths (true at the cutoff, not yet revealed; not usable): "
                    f"{', '.join(sorted(hidden))}\n" if hidden else ""))
    return "\n".join(out)
def roster_rows(project):
    roster = project / "derived" / "bible" / "characters" / "_roster.md"
    return [r for tb in tables(roster.read_text(encoding="utf-8")) for r in tb] if roster.exists() else []
def cast_of(project, text=None):
    """The roster slugs a text names (§12.1): by slug, name, alias, or a name word that
    only one character has. By default, the text is the outline and the chapters."""
    if text is None:
        text = " ".join(f.read_text(encoding="utf-8") for f in [project / "bible" / "outline.md",
                        *sorted((project / "manuscript").glob("*.md"))] if f.exists())
    rows = roster_rows(project)
    words = {}
    for r in rows:
        for w in re.findall(r"[A-Z][a-z]{3,}", r["Name"]): words.setdefault(w, set()).add(r["Slug"])
    out = []
    for r in rows:
        names = [r["Slug"], r["Name"]] + [a.strip() for a in r.get("Aliases", "").split(";") if a.strip()]
        names += [w for w, s in words.items() if s == {r["Slug"]} and w in r["Name"]]
        if any(n and re.search(rf"\b{re.escape(n)}\b", text) for n in names): out.append(r["Slug"])
    return out
def cited_theories(project):
    """The theory entries that the ledger's Basis column cites (§6.13)."""
    f, out = project / "bible" / "divergences.md", []
    th = project / "derived" / "bible" / "theories.md"
    if not (f.exists() and th.exists()): return out
    text = th.read_text(encoding="utf-8")
    for r in [r for tb in tables(f.read_text(encoding="utf-8")) for r in tb if r.get("Basis")]:
        m = re.match(r"([\w/-]+):(T\d+)", r["Basis"])
        e = m and re.search(rf"^### {m.group(2)} — .*?(?=^### |\Z)", text, re.M | re.S)
        if e: out.append((f"{m.group(1)}:{m.group(2)}, cited by {r['ID']}", e.group(0).strip()))
    return out
def canon_rows(project, slugs):
    """Every layer's rows, at any point, that name these entities: the canon ahead."""
    out = []
    for f in sorted((project / "derived" / "bible").rglob("*.md")):
        if f.name.startswith("_") or f.name in ("theories.md", "divergences.md", "outline.md", "premise.md"): continue
        lines, rows, head = f.read_text(encoding="utf-8").splitlines(), [], None
        for i, l in enumerate(lines):
            if not l.startswith("|") or l.startswith("| -"): continue
            if i + 1 < len(lines) and lines[i + 1].startswith("| -"): head = [l, lines[i + 1]]; continue
            cells = l.rstrip().rstrip("|").rsplit("|", 1)[0]   # not the Layer column
            if any(f.stem == s for s in slugs) or any(re.search(rf"\b{s}\b", cells) for s in slugs):
                if head: rows += [""] * bool(rows) + head; head = None
                rows.append(l)
        if rows: out.append(f"### {f.relative_to(project / 'derived').as_posix()}\n" + "\n".join(rows))
    return "\n\n".join(out)
# --- reads (§11.6) ---------------------------------------------------------------------
def section(text, heading):
    m = re.search(rf"^{re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else "(none)"
def resolve_reads(project, y, reads, chapter, target):
    blocks, unresolved = [], []
    if target.startswith("bible/"):                       # the step's own target (§11.6)
        own = project / target
        blocks.append((f"{target}, your target, as the project's own bible holds it",
                       own.read_text(encoding="utf-8") if own.exists() else "(absent: this step starts it)"))
    for item in [s.strip() for s in reads.split(";") if s.strip()]:
        paths = re.findall(r"`([^`]+)`", item)
        if "snapshots" in item:
            blocks.append(("the cast's snapshots (§7)", snapshots(y, cast_of(project)) or "(no cast named yet)")); continue
        if "theories' claims" in item or "cited theories" in item:
            blocks += cited_theories(project) or [("the cited theories' claims", "(no divergence cites a theory)")]; continue
        if "canon ahead" in item or "canon the arc reaches" in item:
            names = " ".join(e for _, e in cited_theories(project))
            slugs = cast_of(project, names) + [s for s in cast_of(project) if s not in cast_of(project, names)]
            blocks.append(("the canon ahead: every layer's rows, at any point, for " + ", ".join(slugs), canon_rows(project, slugs) or "(none)")); continue
        if "reach candidates" in item and y["setting"].get("follow") != "retelling":
            blocks.append(("the host's reach candidates", "(none: the project is not a retelling, §6.6)")); continue
        if "inversion candidates" in item and "order" not in y["setting"]:
            blocks.append(("the host's inversion candidates", "(none: the project has no order of its own, §6.8)")); continue
        if not paths: unresolved.append(item); continue
        p = paths[0].replace("chapter-<NN>", chapter)
        if p == target and not target.startswith("bible/"):   # a log or review: as it stands
            own = project / target
            blocks.append((target, own.read_text(encoding="utf-8") if own.exists() else "(absent: this step starts it)")); continue
        if p == target:
            composed = project / "derived" / target
            if composed.exists() and re.search(r"\| (?!project \|)[a-z][\w/-]* \|$", composed.read_text(encoding="utf-8"), re.M):
                blocks.append((f"{target}, composed across every layer", composed.read_text(encoding="utf-8")))
            continue
        if "## Priorities" in item:
            for f in sorted((project / "reviews").glob("*.md")):
                blocks.append((f"reviews/{f.name}, its ## Priorities", section(f.read_text(encoding="utf-8"), "## Priorities")))
            continue
        base = project / "derived" if p.startswith("bible/") else project
        hits = sorted(base.glob(p.replace("…", "**/*"))) if ("*" in p or "…" in p) else [base / p]
        hits = [h for h in hits if h.is_file()]
        if not hits: blocks.append((p, "(absent)")); continue
        for h in hits:
            text = h.read_text(encoding="utf-8")
            if "`TODO` markers" in item: text = "\n".join(l for l in text.splitlines() if "<!-- TODO" in l) or "(no markers)"
            blocks.append((h.relative_to(project).as_posix().replace("derived/bible", "bible"), text))
    return blocks, unresolved

# --- the loop (§11.1) -----------------------------------------------------------------
def writable(project, rel):
    """§3.1, for project context: inside the project, never a cache or input."""
    target = (project / rel).resolve()
    return project.resolve() in target.parents and not rel.startswith(("derived/", "references/", "project.yaml"))
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("--worlds", default=str(ROOT / "examples" / "worlds"))
    ap.add_argument("--model"); ap.add_argument("--approve", action="store_true", help="approve every gate (a demonstration, not an author)")
    ap.add_argument("--skip", action="append", default=[], metavar="STEP=REASON")
    ap.add_argument("--signal", help="the signal for the gate the run is waiting at")
    ap.add_argument("--run", default="run-1")
    ap.add_argument("--from", dest="start", metavar="STEP", help="re-run from this step, keeping the old files aside")
    a = ap.parse_args()
    project, worlds = pathlib.Path(a.project), pathlib.Path(a.worlds)
    y = yaml.safe_load((project / "project.yaml").read_text(encoding="utf-8"))
    run = project / "runs" / a.run; run.mkdir(parents=True, exist_ok=True)
    state_f = run / "state.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {"done": [], "log": []}
    skips = dict(s.split("=", 1) for s in a.skip)
    if a.start and a.start in state["done"]:
        later = state["done"][state["done"].index(a.start):]
        old = run / "superseded"; old.mkdir(exist_ok=True)
        for f in run.glob("*.md"):
            if f.name.split(".")[0].split("-", 1)[-1] in later: f.rename(old / f.name)
        state["done"] = state["done"][:state["done"].index(a.start)]
    def log(msg): state["log"].append(msg); print(msg)
    def save():
        state_f.write_text(json.dumps(state, indent=1), encoding="utf-8")
        (run / "log.md").write_text("# Run log\n\n" + "".join(f"- {l}\n" for l in state["log"]), encoding="utf-8")
    chapter = "chapter-01"
    for n, step in enumerate(compose_workflow(y), 1):
        sid, agent = step["Step"], step["Agent"]
        if sid in state["done"]: continue
        if sid in skips: log(f"{sid} skipped: {skips[sid]}"); state["done"].append(sid); save(); continue
        if sid in WHEN and not WHEN[sid][0](y, project):
            log(f"{sid} skipped: it runs only when {WHEN[sid][1]}"); state["done"].append(sid); save(); continue
        if agent.strip("`") in SKILLS:
            files = compose(project, y, worlds)
            log(f"{sid} `compose`: derived/bible/ built from {len(files)} paths"); state["done"].append(sid); save(); continue
        draft = project / "manuscript" / f"{chapter}.md"
        if agent == "continuity-editor" and draft.exists() and "TODO: needs bible" in draft.read_text(encoding="utf-8"):
            n_m = draft.read_text(encoding="utf-8").count("TODO: needs bible")
            msg = (f"{sid} blocked: {chapter} has {n_m} `needs bible` markers, and each must be resolved "
                   "before its continuity-editor step runs (§11.9); see showrunner-log.md for what is scheduled")
            if state["log"][-1:] != [msg]: state["log"].append(msg)
            save(); sys.exit(msg)
        if step.get("Repeat") == "per-character":
            log(f"{sid} skipped: no original characters to design (step instances: 0)"); state["done"].append(sid); save(); continue
        compose(project, y, worlds)                       # rebuilt before each read (§7.6)
        target = re.findall(r"`([^`]+)`", step["Writes"])[0].replace("chapter-<NN>", chapter)
        if not writable(project, target): sys.exit(f"{sid}: {target} is not writable here (§3.1)")
        stem = f"{n:02d}-{sid}"
        reply_f = run / f"{stem}.reply.md"
        if not reply_f.exists():
            blocks, unresolved = resolve_reads(project, y, step["Reads"], chapter, target)
            prompt = [(ROOT / "agents" / f"{agent}.md").read_text(encoding="utf-8"), "\n---\n\n# This step\n",
                      f"Workflow `{y['workflow']}`, step **{sid}** ({agent}). Write `{target}`"
                      + (f", {step['Writes'].split('`', 2)[2].strip()}" if step["Writes"].split("`", 2)[2].strip() else "") + ".\n",
                      "\n# Inputs\n"]
            for name, text in blocks: prompt.append(f"\n## {name}\n\n````\n{text.strip()}\n````\n")
            if unresolved: prompt.append("\nNot resolved by this loop, so not included: " + "; ".join(unresolved) + "\n")
            prompt.append(f"\n---\n\n{STANDING}\n")
            prompt = "".join(prompt)
            (run / f"{stem}.prompt.md").write_text(prompt, encoding="utf-8")
            if not a.model:
                save(); print(f"waiting for {reply_f.relative_to(project)}"); sys.exit(3)
            reply = subprocess.run(a.model, shell=True, input=prompt, capture_output=True, text=True, encoding="utf-8").stdout
            reply_f.write_text(reply, encoding="utf-8")
        reply = reply_f.read_text(encoding="utf-8").strip()
        m = re.fullmatch(r"```[a-z]*\n(.*)\n```", reply, re.S)
        if m: reply = m.group(1)
        (project / target).parent.mkdir(parents=True, exist_ok=True)
        (project / target).write_text(reply + "\n", encoding="utf-8")
        log(f"{sid} {agent} → {target}")
        gated = y.get("gates", "milestones") == "all" or (y.get("gates", "milestones") == "milestones" and step["Gate"] == "milestone")
        if gated:
            signal = "approve (by the --approve flag: a demonstration, not an author)" if a.approve else a.signal
            if not signal: save(); print(f"gate after {sid}: give --signal approve | 'revise: <notes>' | 'back: <step>'"); sys.exit(4)
            a.signal = None
            if not signal.startswith("approve"): sys.exit(f"{sid}: signal {signal!r} needs a host; re-run with --from")
            log(f"gate after {sid}: {signal}")
        state["done"].append(sid); save()
    (run / "log.md").write_text("# Run log\n\n" + "".join(f"- {l}\n" for l in state["log"]), encoding="utf-8")
    print("workflow complete")

if __name__ == "__main__": main()
