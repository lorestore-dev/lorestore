"""LoreStore conformance checker for the examples in this repository.

Validates the example workspace in examples/ against the JSON schemas, and runs a
reference implementation of layer stacks (§2.2), the snapshot algorithm (§7), canon
points and adaptation timecodes (§4.2, §4.9), sync points and the project order
(§6.7-6.8), branch and retelling modes (§6.6), hidden truths (§4.4, §6.12), theory
conflicts (§6.13), in-world dates and world history (§4.13), the travel, mysteries,
and lineage modules (§9.4-9.6), image prompts (§10.29), viewpoints (§7.7), and chapter statuses (§10.18), comparing each result
with the
expected answers in examples/README.md.

Usage:
    pip install -r tools/requirements.txt
    python tools/check.py [repo-root]     # repo-root defaults to this file's parent's parent

Prints one line per check, then a failure count; exits 1 if any check fails.

Limitations: it checks the bundled examples only (paths and expected values are
hard-coded), so it is not a validator for arbitrary workspaces. It does not check
markdown links or § references, the agent and workflow chapters, or prose formats
beyond the tables it parses.
"""
import json, re, sys, pathlib, copy, functools, yaml, jsonschema

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
EX = ROOT / "examples"
fails = 0
def check(label, got, want):
    global fails
    ok = got == want; fails += not ok
    print(("ok  " if ok else "FAIL"), label, "" if ok else f": got {got!r}, want {want!r}")
def raises_ok(fn, exc):
    try: fn()
    except exc: return True
    return False

def raises(label, fn, exc=ValueError):
    try: fn(); check(label, "no error", "error")
    except exc: check(label, "error", "error")

def schema(name): return jsonschema.Draft202012Validator(json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text()))
def valid(name, doc):
    try: schema(name).validate(doc); return True
    except jsonschema.ValidationError as e: print("   ", e.message); return False
def load(p): return yaml.safe_load(p.read_text())
def pyaml(p): return load(EX/"projects"/p/"project.yaml")

# --- schemas -----------------------------------------------------------------
PKG_FILES = sorted((EX/"worlds").rglob("package.yaml"))
PROJECTS = sorted(p.parent.name for p in (EX/"projects").glob("*/project.yaml"))
for f in PKG_FILES:
    check(f"schema package {f.parent.relative_to(EX/'worlds').as_posix()}", valid("package", load(f)), True)
for p in PROJECTS:
    check(f"schema project {p}", valid("project", pyaml(p)), True)
check("schema universe", valid("universe", load(EX/"universes/wizards-and-warp/universe.yaml")), True)
for f, idx, name in [("10-formats", 0, "project"), ("10-formats", 2, "package"), ("08-crossovers", 1, "universe")]:
    block = re.findall(r"```yaml\n(.*?)```", (ROOT/f"spec/{f}.md").read_text(), re.S)[idx]
    check(f"schema spec example {f}[{idx}]", valid(name, yaml.safe_load(block)), True)
bad = pyaml("hogwarts-at-warp"); bad["setting"]["cutoff"] = "HBP:7"
check("schema rejects cutoff beside a universe layer", schema("project").is_valid(bad), False)
bad = pyaml("two-witnesses"); bad["setting"]["cutoffs"] = {"harry-potter": "GoF:37"}
check("schema rejects cutoffs without a universe layer", schema("project").is_valid(bad), False)
for ref, ok in [("harry-potter@3.2.1", True), ("harry-potter/fanfic/example@1.2.3", True), ("universe:wizards-and-warp@2.0.3", True),
                ("project:two-witnesses@chapter-02", True), ("harry-potter", False), ("project:two-witnesses@1.0.0", False),
                ("harry-potter/a/b/c@1.0.0", False), ("fanon-hp@latest", False)]:
    d = pyaml("blind-harry"); d["layers"] = [ref]
    if ref.startswith("universe:"): d["setting"]["cutoffs"] = {"harry-potter": d["setting"].pop("cutoff")}; d["setting"]["divergence_points"] = {"harry-potter": d["setting"].pop("divergence_point")}
    check(f"schema layer ref {ref}", schema("project").is_valid(d), ok)
d = pyaml("two-witnesses"); d["resolution"] = "newest"; check("schema rejects unknown resolution", schema("project").is_valid(d), False)
d = pyaml("two-witnesses"); d["setting"]["active_profile"] = "enhanced"; check("schema rejects 0.1 active_profile", schema("project").is_valid(d), False)
d = load(EX/"worlds/harry-potter/fanon/package.yaml"); d["relies-on"] = []
check("schema non-base package must rely on something", schema("package").is_valid(d), False)
d = load(EX/"worlds/harry-potter/base/package.yaml"); d["relies-on"] = ["star-trek@2.1.1"]
check("schema base package relies on nothing", schema("package").is_valid(d), False)
d = load(EX/"worlds/harry-potter/fanfic/example/package.yaml"); d["id"] = "harry-potter/example"
check("schema fanfic id under <fandom>/fanfic/", schema("package").is_valid(d), False)
ser = pyaml("the-long-way-back")
check("schema serial project, default release policy", (ser["workflow"], "serial" in ser, schema("project").is_valid(ser)), ("serial", False, True))
ser["serial"] = {"released": "revisable"}; check("schema serial revisable accepted", schema("project").is_valid(ser), True)
ser["serial"] = {"released": "frozen"}; check("schema serial unknown policy rejected", schema("project").is_valid(ser), False)
for name, doc in [("project", pyaml("two-witnesses")), ("package", load(EX/"worlds/harry-potter/base/package.yaml")), ("universe", load(EX/"universes/wizards-and-warp/universe.yaml"))]:
    check(f"schema {name}: spec version 0.3", doc["spec_version"], "0.3")
    doc["spec_version"] = "0.2"; check(f"schema {name}: a 0.2 manifest is not 0.3", schema(name).is_valid(doc), False)
check("schema: this document is version 0.3", "This document is version `0.3`." in (ROOT/"spec/10-formats.md").read_text(), True)
nov = pyaml("two-witnesses"); nov["serial"] = {"released": "locked"}
check("schema serial block on novel rejected", schema("project").is_valid(nov), False)

# --- parsing -------------------------------------------------------------------
def table(path, heading):
    lines = path.read_text().splitlines(); out, started = [], False
    for l in lines[lines.index(heading)+1:]:
        if l.startswith("|"): started = True; out.append(l)
        elif started: break
    cells = [[c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]] for l in out]
    return [dict(zip(cells[0], r)) for r in cells[2:]]
def has(path, heading): return path.exists() and heading in path.read_text().splitlines()
def front(p): return yaml.safe_load(p.read_text().split("---")[1])
def entries(path):
    out, cur = {}, None
    for l in path.read_text().splitlines():
        m = re.match(r"### ([A-Za-z0-9-]+) — ", l)
        if m: cur = out.setdefault(m.group(1), {}); continue
        m = re.match(r"- ([a-z0-9-]+): (.*?)\s*(#.*)?$", l)
        if cur is not None and m: cur[m.group(1)] = m.group(2)
    return out
def chap(c): return int(c.split("-")[1])

# --- packages and stacks (§2.2, §2.3) -------------------------------------------
TIERS = ["primary", "secondary-official", "adaptation", "fanon", "fanfic", "theory", "erratum"]
UNRESOLVED = {"theory", "erratum"}            # never resolve into state (§5.2)
KIND_TIERS = {"base": {"primary", "secondary-official", "erratum"}, "official": {"secondary-official", "erratum"}, "adaptation": {"adaptation", "erratum"}, "fanon": {"fanon"},
              "fanfic": {"fanfic"}, "theories": {"theory"}}
def pkg_dir(pid):
    fandom, *rest = pid.split("/")
    return EX/"worlds"/fandom/("/".join(rest) if rest else "base")

def entity_rows(d, entity):
    """An entity's state rows in one bible directory (§10.5)."""
    f = d/"characters"/f"{entity}.md"
    out = table(f, "## State history") if f.exists() else []
    if (d/"relationships.md").exists(): out += [r for r in table(d/"relationships.md", "## State history") if r["Pair"] == entity]
    for multi in ("species.md", "history.md", "titles.md"):
        if (d/multi).exists(): out += [r for r in table(d/multi, "## State history") if r["Entity"] == entity]
    if (d/"knowledge.md").exists():
        out += [dict(r, Attribute=r["Secret"], Value=r["State"]) for r in table(d/"knowledge.md", "## Knowledge") if r["Character"] == entity]
    return out

class Package:
    def __init__(self, pid):
        self.id, self.dir = pid, pkg_dir(pid)
        self.cfg = load(self.dir/"package.yaml"); self.kind = self.cfg["kind"]
        self.base = pid.split("/")[0]
        self.sources = {r["ID"]: r["Tier"] for r in table(self.dir/"sources.md", "## Sources")} if (self.dir/"sources.md").exists() else {}
    def roster(self):
        f = self.dir/"characters/_roster.md"
        return table(f, "## Characters") if f.exists() else []
    def rows(self, entity): return entity_rows(self.dir, entity)
    def all_rows(self):
        d = self.dir; out = []
        for f in (d/"characters").glob("[!_]*.md") if (d/"characters").exists() else []:
            out += [dict(r, _entity=f.stem) for r in table(f, "## State history")]
        if (d/"relationships.md").exists(): out += [dict(r, _entity=r["Pair"]) for r in table(d/"relationships.md", "## State history")]
        return out

class Incomparable(Exception): pass

def ruler_works(f):
    """A canon-timeline's ## Works table: {work: (levels, timed level index)} (§10.4)."""
    out = {}
    for r in table(f, "## Works"):
        levels = [l.strip() for l in r["Levels"].split("›")] if r["Levels"] else []
        tl = r["Timed level"]
        out[r["Work"]] = (levels, None if not tl else 0 if tl == "work" else levels.index(tl) + 1)
    return out

def insert_segments(ruler, f, label):
    """Apply a file's ## Works and ## Insert tables to a ruler (§4.10, §4.12). `After: —` goes first."""
    for w, v in ruler_works(f).items():
        assert w not in ruler.works, f"inserted work {w} already on the ruler"
        ruler.works[w] = v
    order = sorted(ruler.segments, key=ruler.segments.get)
    for r in table(f, "## Insert"):
        seg = Ruler.split(r["Segment"])
        if r["After"] == "—": order.insert(0, seg)
        else:
            after = Ruler.split(r["After"])
            assert after in order, f"{label}: inserts after unknown segment {r['After']}"
            order.insert(order.index(after) + 1, seg)
        ruler.counts[seg] = r["Children"]
    ruler.segments = {s: i + 1 for i, s in enumerate(order)}

class Ruler:
    """A base's ruler (§4), plus any adaptation maps (§4.9) and inserted works (§4.10) in the stack."""
    def __init__(self, base, adaptations=(), officials=()):
        self.base = base; ruler = base.dir/"canon-timeline.md"
        self.works = ruler_works(ruler)
        self.segments = {}; self.counts = {}
        for r in table(ruler, "## Order"):
            path = self.split(r["Segment"]); self.segments[path] = int(r["Order"]); self.counts[path] = r["Children"]
        if has(ruler, "## Counts"):
            for r in table(ruler, "## Counts"): self.counts[self.split(r["Node"])] = r["Children"]
        for o in officials:                       # inserted works: official and fanfic packages (§4.10)
            f = o.dir/"canon-timeline.md"
            if has(f, "## Insert"): insert_segments(self, f, o.id)
        self.check_segments()
        self.adapted = []          # (from, to, film work): base ranges an adaptation's timecodes may attach to
        for a in adaptations:
            for r in table(a.dir/"canon-timeline.md", "## Adapts"):
                self.adapted.append((self.split(r["From"]), self.split(r["To"]), r["Work"]))
    def check_segments(self):
        segs = list(self.segments)
        assert not any(a != b and a == b[:len(a)] for a in segs for b in segs), "overlapping segments"
    def reordered(self, order):
        if not order: return self
        segs = {self.split(s): i + 1 for i, s in enumerate(order)}
        assert set(segs) == set(self.segments) and len(order) == len(self.segments), "order must be a permutation"
        w = copy.copy(self); w.segments = segs; return w
    @staticmethod
    def split(s):
        w, *idx = s.split(":"); return (w, *map(int, idx))
    def adaptation_of(self, path):
        """The adaptation work whose range covers path, if any (§4.9)."""
        for lo, hi, work in self.adapted:
            if lo[0] == path[0] and lo[1:] <= path[1:len(lo)] <= hi[1:]: return work
        return None
    def parse(self, pt):
        m = re.fullmatch(r"([A-Za-z][A-Za-z0-9-]*)((?::[1-9]\d*)*)(?:\+(\d{2,}):([0-5]\d):([0-5]\d(?:\.\d+)?))?", pt)
        if not m: raise ValueError(pt)
        path = (m[1], *[int(x) for x in m[2].split(":")[1:]])
        tc = None if m[3] is None else int(m[3])*3600 + int(m[4])*60 + float(m[5])
        if m[1] not in self.works: raise ValueError(pt)
        levels, timed = self.works[m[1]]
        if len(path) - 1 > len(levels): raise ValueError(pt)
        inside = [s for s in self.segments if path[:len(s)] == s]
        contains = [s for s in self.segments if s[:len(path)] == path and s != path]
        if not inside and not contains: raise ValueError(pt)
        for d in range(1, len(path)):
            c = self.counts.get(path[:d], "")
            if c == "—": raise ValueError(pt)
            if c and path[d] > int(c): raise ValueError(pt)
        if tc is not None:
            if timed is not None:                        # the work's own timecode (§4.2)
                if len(path) - 1 < timed: raise ValueError(pt)
            elif len(path) < 2 or not self.adaptation_of(path): raise ValueError(pt)   # an adaptation timecode (§4.9)
            else: timed = len(path) - 1                  # it only orders rows at this exact path
        return path, tc, inside, contains, timed
    def pos(self, pt):
        path, tc, inside, contains, timed = self.parse(pt)
        if inside: s = inside[0]; return (self.segments[s], 1, path[len(s):]), path, tc, timed
        return (min(self.segments[s] for s in contains), 0, (len(path),)), path, tc, timed
    def cmp(self, a, b):
        """-1/0/1 per §4.2; raises Incomparable. Empty = timeless, sorts first."""
        if not a or not b: return (bool(a) > bool(b)) - (bool(a) < bool(b))
        (ka, pa, ta, timed), (kb, pb, tb, timed_b) = self.pos(a), self.pos(b)
        if ka[:2] != kb[:2] or ka[1] == 0: return (ka > kb) - (ka < kb)
        if timed is None: timed = timed_b
        if self.works[pa[0]][1] is None and pa != pb: timed = None    # adaptation timecodes never cross paths
        same_timed = timed is not None and len(pa) - 1 >= timed and len(pb) - 1 >= timed and pa[:timed+1] == pb[:timed+1]
        if same_timed and ta is not None and tb is not None and ta != tb: return (ta > tb) - (ta < tb)
        if same_timed and (ta is None) != (tb is None):
            withtc, other = (pa, pb) if ta is not None else (pb, pa)
            if len(other) > len(withtc): raise Incomparable(f"{a} vs {b}")
        if ka[2] != kb[2]: return (ka[2] > kb[2]) - (ka[2] < kb[2])
        return (ta is not None) - (tb is not None)
    def key(self, pt):
        if pt: self.parse(pt)          # validate
        return pt

class SeriesRuler(Ruler):
    """The ruler of a series begun by a self-contained book (§4.12): the book's own eras, if any,
    then its manuscript as a work counted to the pin, then each later book's inserts."""
    def __init__(self, root, pin, inserters):
        self.base, self.works, self.segments, self.counts, self.adapted = None, {}, {}, {}, []
        f = EX/"projects"/root/"bible/canon-timeline.md"; order = []
        if has(f, "## Order"):
            self.works.update(ruler_works(f))
            for r in sorted(table(f, "## Order"), key=lambda r: int(r["Order"])):
                order.append(self.split(r["Segment"])); self.counts[order[-1]] = r["Children"]
        self.works[root] = (["chapter"], None); order.append((root,)); self.counts[(root,)] = str(chap(pin))
        self.segments = {s: i + 1 for i, s in enumerate(order)}
        for p in inserters:
            g = EX/"projects"/p/"bible/canon-timeline.md"
            if has(g, "## Insert"): insert_segments(self, g, p)
        self.check_segments()

class StackError(Exception): pass

class Stack:
    """A project's layers, from the base up (§2.2). _rank = (layer index, -tier index): the lower tier ranks first."""
    def __init__(self, layers, resolution="precedence", project=None):
        self.refs, self.resolution, self.project = list(layers), resolution, project
        self.packages, self.projects, self.universe = [], [], None   # packages: (index, Package)
        self.project_index = {}
        for i, ref in enumerate(self.refs):
            kind, ident, pin = self.parse_ref(ref)
            if kind == "package":
                p = Package(ident); self.packages.append((i, p))
                if p.cfg["version"] != pin: raise StackError(f"{ref}: package is at {p.cfg['version']}")
                for dep in p.cfg["relies-on"]:
                    if dep not in self.refs[:i]: raise StackError(f"{ref} relies on {dep}, which is not below it")
            elif kind == "universe":
                self.universe = load(EX/"universes"/ident/"universe.yaml")
                if self.universe["version"] != pin: raise StackError(ref)
                for dep in self.universe["relies-on"]:
                    if dep not in self.refs[:i]: raise StackError(f"{ref} relies on {dep}, which is not below it")
            else:
                self.projects.append((ident, pin)); self.project_index[ident] = i
        self.bases = {p.id: p for _, p in self.packages if p.kind == "base"}
        if len(self.bases) > 1 and not self.universe: raise StackError("two bases need a universe layer")
    @staticmethod
    def parse_ref(ref):
        if ref.startswith("project:"): ident, pin = ref[8:].split("@"); return "project", ident, pin
        if ref.startswith("universe:"): ident, pin = ref[9:].split("@"); return "universe", ident, pin
        ident, pin = ref.split("@"); return "package", ident, pin
    @classmethod
    def of(cls, project):
        y = pyaml(project); return cls(y.get("layers", []), y.get("resolution", "precedence"), project)
    def ledgers(self):
        """Read-only project-layer ledgers in stack order, transitively (§6.4): [(project, pinned chapter)]."""
        out = []
        for p, pin in self.projects:
            for q in Stack.of(p).ledgers() + [(p, pin)]:
                if q not in out: out.append(q)
        return out
    def ruler(self, base=None, ordered=True):
        """The stack's ruler, with its inserts (§4.10, §4.12), in the project order unless `ordered` is false."""
        if not self.bases: r = self.series_ruler(); return r.reordered(self.order()) if ordered else r
        b = self.bases[base] if base else next(iter(self.bases.values()))
        r = Ruler(b, [p for _, p in self.packages if p.kind == "adaptation" and p.base == b.id],
                  [p for _, p in self.packages if p.kind in ("official", "fanfic") and p.base == b.id])
        return r.reordered(self.order()) if ordered else r
    def order(self):
        """The project order, else the highest project layer's (§6.14)."""
        own = pyaml(self.project)["setting"].get("order") if self.project else None
        if own: return own
        for p, _ in reversed(self.projects):
            o = Stack.of(p).order()
            if o: return o
        return None
    def series_ruler(self):
        """§4.12: the self-contained book at the root of the stack, and every later book's inserts."""
        layers = self.ledgers(); pins = dict(layers); pins.update(dict(self.projects))
        roots = [p for p, _ in layers if not Stack.of(p).refs]
        if not roots: raise StackError("no ruler")
        inserters = [p for p, _ in layers if p != roots[0]] + ([self.project] if self.project else [])
        return SeriesRuler(roots[0], pins[roots[0]], list(dict.fromkeys(inserters)))
    def layer_rows(self, entity, base):
        out = []
        for i, p in self.packages:
            if p.base != base: continue
            for r in p.rows(entity):
                tier = p.sources.get(r["Source"])
                if tier is None: raise StackError(f"{p.id}: unregistered source {r['Source']}")
                if tier in UNRESOLVED: continue                 # theories and errata never resolve (§5.2)
                out.append(dict(r, _rank=(i, -TIERS.index(tier)), _layer=p.id))
        return out
    def project_rows(self, entity, position=None, cutoff=None, ruler=None, pending=None):
        """The project's own rows, and its project layers', for an entity it defines (§2.7),
        with story-dated rows (§4.11) kept only from their chapter on. A layer's timeless and
        story-dated rows are anchored (§6.14): ahead of the cutoff, they need the author's carry-back,
        and undecided ones go to `pending`. A self-contained layer's story-dated rows are dated on
        its work (§4.12). Ruler-dated rows are time-filtered at the cutoff."""
        out = []
        layers = [(p, pin, self.project_index[p]) for p, pin in self.projects]
        if self.project: layers.append((self.project, position, len(self.refs)))
        for p, pos, i in layers:
            layer = p != self.project; root = layer and not Stack.of(p).refs
            for r in entity_rows(EX/"projects"/p/"bible", entity):
                fc = r.get("From chapter")
                if fc and pos and chap(fc) > chap(pos): continue
                r = dict(r, _rank=(i, -len(TIERS)), _layer=f"project:{p}")
                if layer and not r["As of"]:
                    item = f"{p}:{entity}.{r['Attribute']}" + (f"@{fc}" if fc else "")
                    if root and fc: r["As of"] = f"{p}:{chap(fc)}"; r["From chapter"] = ""
                    if cutoff and ruler and ahead(ruler, p, fc or "chapter-01", cutoff):
                        d = seam_decision(self, item)
                        if d is None and pending is not None: pending.add(item)
                        if d != "carry-back": continue
                elif r["As of"] and cutoff and ruler and ruler.cmp(r["As of"], cutoff) > 0: continue
                out.append(r)
        return out

def rcmp(ruler, a, b):
    """Row order on the ruler: timeless first, then ruler points, then story-dated rows by chapter (§4.11)."""
    ca, cb = a.get("From chapter") or "", b.get("From chapter") or ""
    if ca or cb:
        if not (ca and cb): return 1 if ca else -1
        return (chap(ca) > chap(cb)) - (chap(ca) < chap(cb))
    return ruler.cmp(a["As of"], b["As of"])

BRANCH_ERRORS = []

def track_cutoff(project, position, default):
    f = EX/"projects"/project/"bible/sync-points.md"
    if not has(f, "## Sync points"): return default
    cut = default
    for r in table(f, "## Sync points"):
        if chap(r["From chapter"]) <= chap(position): cut = r["Cutoff"]
    return cut

def active(d, position):
    return position is None or (chap(d["First occurs"]) <= chap(position) and not (d.get("Until") and chap(d["Until"]) <= chap(position)))

def anchor(p, chapter):
    """Where an earlier book established an item (§6.14): its cutoff at the chapter, or, for a
    self-contained book, the chapter on its own work (§4.12). None for per-base cutoffs."""
    if not Stack.of(p).refs: return f"{p}:{chap(chapter)}"
    return track_cutoff(p, chapter, pyaml(p)["setting"].get("cutoff"))

def ahead(ruler, p, chapter, cutoff):
    a = anchor(p, chapter); return a is not None and ruler.cmp(a, cutoff) > 0

def seam_rules(stack):
    """Seam conflicts rows: project-layer ledgers as of their pins, then the project's own (§6.4)."""
    out = []
    for p, pin in stack.ledgers() + ([(stack.project, None)] if stack.project else []):
        f = EX/f"projects/{p}/bible/divergences.md"
        if has(f, "## Seam conflicts"):
            out += [r for r in table(f, "## Seam conflicts") if pin is None or chap(r["Decided in"]) <= chap(pin)]
    return out

def seam_match(pattern, item):
    """`*` stands for a whole slug, attribute, chapter, or divergence number (§6.14)."""
    return re.fullmatch("".join("[^.:@]+" if c == "*" else re.escape(c) for c in pattern), item) is not None

def seam_decision(stack, item):
    """An exact item beats a pattern; between patterns, the later row wins (§6.14)."""
    rules = seam_rules(stack)
    exact = [r for r in rules if r["Item"] == item]
    if exact: return exact[-1]["Decision"]
    pats = [r for r in rules if "*" in r["Item"] and seam_match(r["Item"], item)]
    return pats[-1]["Decision"] if pats else None

def apply_ledger(out, project, position, entity, stack=None, cutoff=None, ruler=None, pending=None):
    """Apply one ledger's overrides for an entity. For a project layer's ledger, a divergence
    anchored ahead of the cutoff applies only if carried back (§6.14)."""
    f = EX/f"projects/{project}/bible/divergences.md"
    for d in table(f, "## Divergences") if f.exists() else []:
        if d["Overrides"] != "—" and active(d, position):
            mine = [a for a in d["Overrides"].split("; ") if a.split("=", 1)[0].rsplit(".", 1)[0] == entity]
            if mine and stack and cutoff and ahead(ruler, project, d["First occurs"], cutoff):
                item = f"{project}:{d['ID']}"; dec = seam_decision(stack, item)
                if dec is None and pending is not None: pending.add(item)
                if dec != "carry-back": continue
            for a in d["Overrides"].split("; "):
                lhs, v = a.split("=", 1); ent, att = lhs.rsplit(".", 1)
                if ent == entity:
                    if v == "(unset)": out.pop(att, None)
                    else: out[att] = v

def reach_candidates(stack):
    """Divergence reach (§6.6): for every divergence in the project's ledgers, its own and
    its project layers', each canon row on an attribute it overrides, dated at or after the
    cutoff where the divergence first occurs. Returns sorted (divergence, entity.attribute, as-of)."""
    project = stack.project; base = next(iter(stack.bases)); ruler = stack.ruler(base)
    st = pyaml(project)["setting"]; out = []
    for p, qual in [(q, f"{q}:") for q, _ in stack.ledgers()] + [(project, "")]:
        f = EX/f"projects/{p}/bible/divergences.md"
        for d in table(f, "## Divergences") if f.exists() else []:
            if d["Overrides"] == "—": continue
            first = d["First occurs"] if p == project else None
            cut = track_cutoff(project, first, st["cutoff"]) if first else st["cutoff"]
            for a in d["Overrides"].split("; "):
                ent, att = a.split("=", 1)[0].rsplit(".", 1)
                for r in stack.layer_rows(ent, base):
                    if r["Attribute"] == att and r["As of"] and ruler.cmp(r["As of"], cut) >= 0:
                        out.append((qual + d["ID"], f"{ent}.{att}", r["As of"]))
    return sorted(set(out))

def snapshot(stack, entity, cutoff=None, position=None, base=None, ledger=True):
    return resolve(stack, entity, cutoff, position, base, ledger)[0]

def ties(stack, entity, cutoff=None, position=None, base=None):
    """Tied rows in one package (§4.4, §7.2): an invalid package. {attribute: sorted source ids}."""
    return resolve(stack, entity, cutoff, position, base)[1]

def seams(stack, entity, cutoff=None, position=None, base=None):
    """Earlier books' items ahead of the cutoff that no seam decision covers (§6.14, §7.2 step 8)."""
    return resolve(stack, entity, cutoff, position, base)[2]

def decisions(stack, entity, heading, value=lambda r: r["Decision"]):
    """The author's decisions in one ledger table, from project-layer ledgers as of their pins,
    then the project's own; a later ledger wins (§6.4)."""
    out = {}
    for p, pin in stack.ledgers() + ([(stack.project, None)] if stack.project else []):
        f = EX/f"projects/{p}/bible/divergences.md"
        if has(f, heading):
            for r in table(f, heading):
                if r["Entity"] == entity and (pin is None or chap(r["Decided in"]) <= chap(pin)):
                    out[r["Attribute"]] = value(r)
    return out
def hidden_decisions(stack, entity): return decisions(stack, entity, "## Hidden canon")       # §6.12

def resolve(stack, entity, cutoff=None, position=None, base=None, ledger=True):
    base = base or next(iter(stack.bases), None)
    ruler = stack.ruler(base); project = stack.project
    if project:
        st = pyaml(project)["setting"]
        if cutoff is None:
            cutoff = track_cutoff(project, position, st["cutoff"] if "cutoff" in st else st["cutoffs"][base])
        if st.get("follow") == "branch" and ruler.cmp(cutoff, st["divergence_point"]) > 0:
            BRANCH_ERRORS.append((project, cutoff)); cutoff = st["divergence_point"]
    pending = set()
    rows = [r for r in stack.layer_rows(entity, base) if ruler.cmp(r["As of"], cutoff) <= 0]
    rows += stack.project_rows(entity, position, cutoff, ruler, pending)
    out, open_conflicts = {}, {}
    for attr in {r["Attribute"] for r in rows}:
        cand = [r for r in rows if r["Attribute"] == attr]
        win = pick(cand, stack.resolution, ruler)
        tied = [r for r in cand if r["_rank"] == win["_rank"] and rcmp(ruler, r, win) == 0]
        if len({r["Value"] for r in tied}) > 1:                  # an invalid package (§4.4)
            open_conflicts[attr] = sorted(r["Source"] for r in tied); continue
        if win["Value"] != "(unset)": out[attr] = win["Value"]
    if ledger:
        for p, pin in stack.ledgers(): apply_ledger(out, p, pin, entity, stack, cutoff, ruler, pending)
        if project: apply_ledger(out, project, position, entity)
    return out, open_conflicts, pending

def pick(cand, mode, ruler):
    """The winning row among one attribute's candidates, by resolution mode (§5.4)."""
    K = functools.cmp_to_key(lambda a, b: rcmp(ruler, a, b))
    if mode == "precedence":
        best = max(r["_rank"] for r in cand)
    elif mode == "fill":                         # the lowest layer with a row wins
        low = min(r["_rank"][0] for r in cand)
        best = max(r["_rank"] for r in cand if r["_rank"][0] == low)
    else:                                        # recency
        latest = max(cand, key=K)
        return max((r for r in cand if rcmp(ruler, r, latest) == 0), key=lambda r: r["_rank"])
    return max((r for r in cand if r["_rank"] == best), key=K)

def quote(stack, owner, qid, cutoff, attr="Speaker"):
    """A quotation's resolved Speaker or Line (§2.7, §10.13): the owner's row, plus higher
    layers' rows for `<owner>:<qid>`. Erratum rows never resolve (§5.2); a tie is an invalid package (§4.4)."""
    return quote_resolve(stack, owner, qid, cutoff, attr)[0]

def quote_resolve(stack, owner, qid, cutoff, attr="Speaker"):
    """(value, tied sources if the package is invalid)."""
    ruler = stack.ruler(owner); cand = []
    for i, p in stack.packages:
        f = p.dir/"quotations.md"
        if p.base != owner or not f.exists(): continue
        for r in table(f, "## Quotations"):
            if (r["ID"] == qid and p.id == owner) or r["ID"] == f"{owner}:{qid}":
                if r[attr] and ruler.cmp(r["As of"], cutoff) <= 0 and p.sources[r["Source"]] not in UNRESOLVED:
                    cand.append(dict(r, _rank=(i, -TIERS.index(p.sources[r["Source"]])), _layer=p.id))
    if not cand: return None, []
    win = pick(cand, stack.resolution, ruler)
    tied = [r for r in cand if r["_rank"] == win["_rank"] and ruler.cmp(r["As of"], win["As of"]) == 0]
    if len({r[attr] for r in tied}) > 1: return None, sorted(r["Source"] for r in tied)
    return win[attr], []

def hidden(stack, entity, cutoff, base=None):
    base = base or next(iter(stack.bases)); ruler = stack.ruler(base)
    return {r["Attribute"] for r in stack.layer_rows(entity, base) if r.get("True from")
            and ruler.cmp(r["True from"], cutoff) <= 0 < ruler.cmp(r["As of"], cutoff)}

PURIST  = Stack(["harry-potter@3.2.1"])
ENRICH  = Stack(["harry-potter@3.2.1", "harry-potter/fanon@1.0.4", "harry-potter/fanfic/example@1.2.3"])
ENHANCE = Stack(ENRICH.refs, "recency")
FILL    = Stack(ENRICH.refs, "fill")
TREK    = Stack(["star-trek@2.1.1"])
TAS     = Stack(["star-trek@2.1.1", "star-trek/animated@1.0.2"])
HP, ST = PURIST.ruler(), TREK.ruler()
g = lambda s, e, c, a, **k: snapshot(s, e, c, **k).get(a)

# --- Harry Potter ---------------------------------------------------------------
check("1 residence PS:2", g(PURIST, "harry-potter", "PS:2", "residence"), "cupboard under the stairs, 4 Privet Drive")
check("1 residence PS:3", g(PURIST, "harry-potter", "PS:3", "residence"), "Dudley's second bedroom")
for c, want in [("PS:9", None), ("PS:10", "Nimbus Two Thousand"), ("PoA:10", None), ("PoA:11", "Firebolt")]:
    check(f"2 broom {c}", g(PURIST, "harry-potter", c, "broom"), want)
for n, s, early, late in [("canon only", PURIST, "round", "round"), ("precedence", ENRICH, "round", "contact lenses"), ("recency", ENHANCE, "round", "contact lenses")]:
    check(f"3 glasses {n} PS:5", g(s, "harry-potter", "PS:5", "glasses"), early)
    check(f"3 glasses {n} GoF:37", g(s, "harry-potter", "GoF:37", "glasses"), late)
check("3 broom precedence PoA:11: the top layer wins though older", g(ENRICH, "harry-potter", "PoA:11", "broom"), "Cleansweep Seven")
check("3 broom recency PoA:11: the later canon row wins", g(ENHANCE, "harry-potter", "PoA:11", "broom"), "Firebolt")
check("3 broom recency PoA:10: canon's later (unset) wins", g(ENHANCE, "harry-potter", "PoA:10", "broom"), None)
check("3 broom recency PS:10: same point, higher layer breaks the tie", g(ENHANCE, "harry-potter", "PS:10", "broom"), "Cleansweep Seven")
check("3 broom fill PS:10: the base has a row, so it stands", g(FILL, "harry-potter", "PS:10", "broom"), "Nimbus Two Thousand")
check("3 broom fill PoA:10: the base's (unset) stands", g(FILL, "harry-potter", "PoA:10", "broom"), None)
check("3 broom fill PoA:11", g(FILL, "harry-potter", "PoA:11", "broom"), "Firebolt")
check("3 glasses fill: canon's round stands", g(FILL, "harry-potter", "GoF:37", "glasses"), "round")
FILMS = Stack(["harry-potter@3.2.1", "harry-potter/films@1.0.3"])
check("3 quote: the books give the line to Ron", quote(PURIST, "harry-potter", "q1", "GoF:1"), "ron-weasley")
check("3 quote: precedence with the films gives it to Hermione", quote(FILMS, "harry-potter", "q1", "GoF:1"), "hermione-granger")
check("3 quote: recency, same point, the higher layer", quote(Stack(FILMS.refs, "recency"), "harry-potter", "q1", "GoF:1"), "hermione-granger")
check("3 quote: fill keeps the book's speaker", quote(Stack(FILMS.refs, "fill"), "harry-potter", "q1", "GoF:1"), "ron-weasley")
check("3 quote: the film row leaves the line to the book", quote(FILMS, "harry-potter", "q1", "GoF:1", "Line").startswith("[to kill Harry"), True)
check("3 quote: not yet said at PoA:16", quote(FILMS, "harry-potter", "q1", "PoA:16"), None)
check("V qualified quotation ids name a lower package's quotation", all(
    r["ID"].rsplit(":", 1)[1] in {q["ID"] for q in table(pkg_dir(r["ID"].rsplit(":", 1)[0])/"quotations.md", "## Quotations")}
    for f in (EX/"worlds").rglob("quotations.md") for r in table(f, "## Quotations") if ":" in r["ID"]), True)
check("4 daphne house canon only", g(PURIST, "daphne-greengrass", "GoF:37", "house"), None)
check("4 daphne house with fanon (fill: canon is silent)", g(FILL, "daphne-greengrass", "GoF:37", "house"), "Slytherin")
check("4 daphne year (fill: canon's row)", g(FILL, "daphne-greengrass", "OotP:31", "year"), "Harry's year")
check("4 daphne house with fanon (precedence)", g(ENRICH, "daphne-greengrass", "GoF:37", "house"), "Slytherin")
check("4 daphne house with fanon (recency)", g(ENHANCE, "daphne-greengrass", "GoF:37", "house"), "Slytherin")
check("4 daphne year OotP:30", g(ENHANCE, "daphne-greengrass", "OotP:30", "year"), None)
check("4 daphne year OotP:31", g(PURIST, "daphne-greengrass", "OotP:31", "year"), "Harry's year")
TW = Stack.of("two-witnesses")
check("5 cedric no ledger", g(ENHANCE, "cedric-diggory", "GoF:37", "status"), "dead")
check("5 cedric ledger ch1", g(TW, "cedric-diggory", "GoF:37", "status", position="chapter-01"), "alive")
check("5 cedric GoF:20", (g(ENHANCE, "cedric-diggory", "GoF:20", "status"), g(ENHANCE, "cedric-diggory", "GoF:20", "role")), ("alive", "Hogwarts Triwizard champion"))
check("6 bond PS:8", g(PURIST, "harry-potter+hermione-granger", "PS:8", "bond"), "acquaintances")
check("6 bond PS:10", g(PURIST, "harry-potter+hermione-granger", "PS:10", "bond"), "friends")
check("7 knowledge GoF:34", g(PURIST, "harry-potter", "GoF:34", "moody-identity"), "unaware")
check("7 knowledge GoF:35", g(PURIST, "harry-potter", "GoF:35", "moody-identity"), "knows")
roster = {r["Slug"]: r for r in Package("harry-potter").roster()}
check("7 reveal alias", (roster["moody-impostor"]["Reveal of"], roster["moody-impostor"]["Revealed at"]), ("barty-crouch-jr", "GoF:35"))

# --- Star Trek ------------------------------------------------------------------
for c, want in [("TNG:3:25", "captain of the USS Enterprise-D"), ("TNG:3:26", "assimilated as Locutus of Borg"),
                ("TNG:4", "assimilated as Locutus of Borg"), ("TNG:4:1", "captain of the USS Enterprise-D")]:
    check(f"8 picard {c}", g(TREK, "jean-luc-picard", c, "status"), want)
check("9 tasha TNG:1", g(TREK, "tasha-yar", "TNG:1", "status"), "chief of security, USS Enterprise-D")
check("9 tasha TNG:2", g(TREK, "tasha-yar", "TNG:2", "status"), "dead")
check("10 mirror TOS2:3", snapshot(TREK, "spock-mirror", "TOS:2:3"), {})
check("10 mirror TOS2:4", g(TREK, "spock-mirror", "TOS:2:4", "appearance"), "bearded")
check("10 spock has no mirror rows", "appearance" in snapshot(TREK, "spock", "TNG:4:26"), False)
check("species borg TNG2:15", g(TREK, "borg", "TNG:2:15", "known-to-federation"), None)

# --- Crossover: the universe is a layer (§8) --------------------------------------
HW = Stack.of("hogwarts-at-warp")
check("12 universe stack has two bases", sorted(HW.bases), ["harry-potter", "star-trek"])
check("12 harry broom", g(HW, "harry-potter", None, "broom", base="harry-potter"), "Firebolt")
check("12 picard", g(HW, "jean-luc-picard", None, "status", base="star-trek"), "captain of the USS Enterprise-D")
check("12 each base has its own ruler", (HW.ruler("harry-potter").base.id, HW.ruler("star-trek").base.id), ("harry-potter", "star-trek"))
raises("12 two bases without a universe rejected", lambda: Stack(["harry-potter@3.2.1", "star-trek@2.1.1"]), StackError)
raises("12 universe below its bases rejected", lambda: Stack(["universe:wizards-and-warp@2.0.3", "harry-potter@3.2.1", "star-trek@2.1.1"]), StackError)
u = load(EX/"universes/wizards-and-warp/universe.yaml")
check("V universe pins", sorted(u["relies-on"]), sorted(f"{b}@{Package(b).cfg['version']}" for b in ["harry-potter", "star-trek"]))
check("V universe offsets name its bases", set(u["offsets"]) <= {d.split("@")[0] for d in u["relies-on"]}, True)

# --- ruler points (§4.2) ---------------------------------------------------------
def isvalid(r, pt):
    try: r.parse(pt); return True
    except ValueError: return False
for pt, want in [("TOS:3:2:14", True), ("TOS:3:2:14+00:12:31", True), ("TMP+01:10:05", True), ("TOS:3:25", False),
                 ("TNG:1:5", False), ("TOS:3+00:01:00", False), ("TOS:3:2:14:1", False), ("TOS:3:2+00:61:00", False), ("DS9:1", False),
                 ("TOS", True), ("TNG", True), ("TMP:4", True)]:
    check(f"P valid {pt}", isvalid(ST, pt), want)
chain = "TOS TOS:1 TOS:3:2 TOS:3:2:14 TOS:3:2:14+00:12:31 TOS:3:2:15 TMP TMP+01:10:05 TNG TNG:1 TNG:2 TNG:2:16".split()
check("P ordering chain", all(ST.cmp(a, b) < 0 for a, b in zip(chain, chain[1:])), True)
check("P ordering transitive sample", all(ST.cmp(chain[i], chain[j]) < 0 for i in range(len(chain)) for j in range(i+1, len(chain))), True)
check("P timecodes win over scenes", ST.cmp("TOS:3:2:14+00:20:00", "TOS:3:2:15+00:10:00"), 1)
raises("P incomparable reported", lambda: ST.cmp("TOS:3:2+00:12:31", "TOS:3:2:14"), Incomparable)
check("P different episodes comparable", ST.cmp("TOS:3:2+00:12:31", "TOS:3:3:1"), -1)
check("P HP chapter scene", HP.cmp("PS:6", "PS:6:2") < 0 and HP.cmp("PS:6:2", "PS:7") < 0, True)
raises("P untimed work rejects timecode", lambda: HP.parse("PS:6+00:00:01"))

# --- inserted works: the animated series (§4.10) -----------------------------------
TR = TAS.ruler()
check("I TAS points need the animated package", isvalid(ST, "TAS:1:2"), False)
check("I TAS point valid with it", isvalid(TR, "TAS:1:2"), True)
check("I TAS:1 has 16 episodes", isvalid(TR, "TAS:1:17"), False)
check("I TAS sorts after TOS season 3", TR.cmp("TOS:3:24", "TAS:1:1"), -1)
check("I TAS sorts before TMP", TR.cmp("TAS:2:6", "TMP"), -1)
check("I TAS season order", TR.cmp("TAS:1:16", "TAS:2:1"), -1)
check("I TOS order unchanged", TR.cmp("TOS:3:2", "TMP"), -1)
check("I spock childhood pet with the package", g(TAS, "spock", "TNG:4:1", "childhood-pet"), "I-Chaya, a sehlat, put to sleep after a le-matya wounded him")
check("I spock childhood pet absent at TOS:3:24", g(TAS, "spock", "TOS:3:24", "childhood-pet"), None)
check("I spock without the package: no pet (a source leak if used)", g(TREK, "spock", "TNG:4:1", "childhood-pet"), None)
check("I animated is an official package of secondary-official sources", (Package("star-trek/animated").kind, set(Package("star-trek/animated").sources.values())), ("official", {"secondary-official"}))

# --- adaptation timecodes (§4.9) ---------------------------------------------------
FILMS = Stack(["harry-potter@3.2.1", "harry-potter/films@1.0.3"]); HF = FILMS.ruler()
for pt, want in [("PS:6:2+00:41:10", True), ("PS:6+00:41:10", True), ("PS+00:41:10", False), ("CoS:1+00:01:00", False), ("PS:6:2", True)]:
    check(f"A valid with films {pt}", isvalid(HF, pt), want)
check("A timecode needs the films layer", isvalid(HP, "PS:6:2+00:41:10"), False)
check("A same path: timecode orders", HF.cmp("PS:6:2+00:41:10", "PS:6:2+00:42:00"), -1)
check("A same path: untimed row first", HF.cmp("PS:6:2", "PS:6:2+00:00:01"), -1)
check("A book path decides across scenes", HF.cmp("PS:6:3+00:10:00", "PS:6:2+00:50:00"), 1)
check("A book path decides chapter vs scene", HF.cmp("PS:6+00:59:00", "PS:6:1"), -1)
check("A adaptation work for PS:6:2", HF.adaptation_of(("PS", 6, 2)), "PS-film")
check("A film rows resolve on the book ruler", [k for k in entries(pkg_dir("harry-potter/films")/"magic/spells.md")], ["oculus-reparo"])
HF.key(entries(pkg_dir("harry-potter/films")/"magic/spells.md")["oculus-reparo"]["as-of"])

# --- sync points and rearranged canon (§6.6–6.8) ----------------------------------------
R = "second-year-tournament"; SYT = Stack.of(R)
def snap_r(e, a, ch, ledger=True):
    return snapshot(SYT, e, None, position=ch, ledger=ledger).get(a)
check("T sync point cutoff ch05", track_cutoff(R, "chapter-05", "PS:17"), "GoF:1")
check("T sync point cutoff ch15", track_cutoff(R, "chapter-15", "PS:17"), "GoF:37")
check("T track before first row", track_cutoff(R, "chapter-00", "PS:17"), "PS:17")
check("T order: GoF before PoA", HP.reordered(pyaml(R)["setting"]["order"]).cmp("GoF:20", "PoA:17"), -1)
check("T ruler order unchanged", HP.cmp("GoF:20", "PoA:17"), 1)
check("T sirius bond ch05 (no ledger needed)", snap_r("harry-potter+sirius-black", "bond", "chapter-05", ledger=False), "strangers")
check("T sirius bond ch15 without ledger = inversion leak", snap_r("harry-potter+sirius-black", "bond", "chapter-15", ledger=False), "correspondents")
check("T sirius bond ch15 with D2", snap_r("harry-potter+sirius-black", "bond", "chapter-15"), "strangers")
check("T sirius bond ch40, D2 ended", snap_r("harry-potter+sirius-black", "bond", "chapter-40"), "met in the Shrieking Shack")
check("T sirius status ch15 (escape not yet)", snap_r("sirius-black", "status", "chapter-15"), None)
check("T cedric ch10 alive", snap_r("cedric-diggory", "status", "chapter-10"), "alive")
check("T cedric ch14 dead", snap_r("cedric-diggory", "status", "chapter-14"), "dead")
check("T cedric ch40 without D3 resurrects", snap_r("cedric-diggory", "status", "chapter-40", ledger=False), "alive")
check("T cedric ch40 with D3", (snap_r("cedric-diggory", "status", "chapter-40"), snap_r("cedric-diggory", "role", "chapter-40")), ("dead", None))
check("T cedric house kept via confirmation row", snap_r("cedric-diggory", "house", "chapter-10"), "Hufflepuff")

def inversions(stack):
    ruler, w = stack.ruler(ordered=False), stack.ruler()    # ruler order, project order
    out = set(); groups = {}
    for _, p in stack.packages:
        for r in p.all_rows(): groups.setdefault((r["_entity"], r["Attribute"]), []).append(r)
    for (e, a), rows in groups.items():
        for x in rows:
            for y in rows:
                if x["Value"] != y["Value"] and x["As of"] and y["As of"] and ruler.cmp(x["As of"], y["As of"]) < 0 and w.cmp(x["As of"], y["As of"]) > 0:
                    out.add(f"{e}.{a}")
    return out
inv = inversions(SYT)
check("T inversions found", inv, {"harry-potter+sirius-black.bond", "cedric-diggory.status", "cedric-diggory.role"})
covered = set()
for d in table(EX/f"projects/{R}/bible/divergences.md", "## Divergences"):
    if d["Overrides"] != "—": covered |= {a.split("=")[0] for a in d["Overrides"].split("; ")}
check("T every inversion covered by a divergence", inv - covered, set())
check("T no inversions in two-witnesses (canon order)", inversions(TW), set())
def inversion_candidates(stack):
    """§6.8: for each pair of segments the project order swaps, every entity with rows in both."""
    base, w = stack.ruler(ordered=False), stack.ruler()
    segs = sorted(base.segments, key=base.segments.get)
    def seg(pt):
        p = Ruler.split(pt.split("+")[0]); return next((s for s in segs if p[:len(s)] == s), None)
    swapped = [(a, b) for i, a in enumerate(segs) for b in segs[i+1:] if w.segments[a] > w.segments[b]]
    by = {}
    for _, p in stack.packages:
        for r in p.all_rows():
            if r["As of"]: by.setdefault(r["_entity"], set()).add(seg(r["As of"]))
    name = lambda s: ":".join(map(str, s))
    return sorted((e, name(b), name(a)) for e, m in by.items() for a, b in swapped if a in m and b in m)
IC = inversion_candidates(SYT)
check("T inversion candidates: entities with rows on both sides of a swap", IC,
      [("cedric-diggory", "GoF", "PoA"), ("harry-potter", "GoF", "CoS"), ("harry-potter", "GoF", "PoA"), ("harry-potter+sirius-black", "GoF", "PoA")])
review = table(EX/f"projects/{R}/reviews/canon.md", "## Inversion candidates")
check("T every inversion candidate is addressed in the order audit", sorted(r["Candidate"] for r in review), sorted(f"{e} ({b}, {a})" for e, a, b in IC))
check("T the Firebolt candidate became I4, covered by D4", any(d["ID"] == "D4" and "I4" in d["This story changes it to"] for d in table(EX/f"projects/{R}/bible/divergences.md", "## Divergences")), True)
check("T no candidates in canon order", inversion_candidates(TW), [])
def propose_order(order, ruler):
    """§6.8 rule 1: keep the old order's segments the ruler still has; place each new one right
    after the segment it follows on the new ruler, in ruler order."""
    have = sorted(ruler.segments, key=ruler.segments.get); name = lambda s: ":".join(map(str, s))
    out = [s for s in order if Ruler.split(s) in ruler.segments]
    for i, s in enumerate(have):
        if name(s) in out: continue
        out.insert(out.index(name(have[i - 1])) + 1 if i else 0, name(s))
    return out
TREK_ORDER = [":".join(map(str, s)) for s in sorted(ST.segments, key=ST.segments.get)]
TREK_ORDER[2], TREK_ORDER[3] = TREK_ORDER[3], TREK_ORDER[2]          # a project order swapping TOS:3 and TMP
NEW = propose_order(TREK_ORDER, TAS.ruler())
check("T adding a package: inserted segments follow theirs in the project order", NEW[:6], ["TOS:1", "TOS:2", "TMP", "TOS:3", "TAS:1", "TAS:2"])
check("T the proposal is a permutation of the new stack's segments", sorted(NEW) == sorted(":".join(map(str, s)) for s in TAS.ruler().segments), True)
check("T removing it again drops them", propose_order(NEW, ST), TREK_ORDER)
check("T Q2 addition D2 (scar)", snapshot(TW, "cedric-diggory", "GoF:37", position="chapter-02").get("scars"), "curse scar across his chest")
for d in table(EX/f"projects/{R}/bible/divergences.md", "## Divergences"):
    if d.get("Until"): check(f"V Until after First occurs {d['ID']}", chap(d["Until"]) > chap(d["First occurs"]), True)

# --- branch and retelling (§6.6) -------------------------------------------------------
B, T = Stack.of("no-horcruxes"), Stack.of("blind-harry")
check("B voldemort dead from chapter-01", snapshot(B, "lord-voldemort", position="chapter-01").get("status"), "dead")
check("B broom at chapter-50 stays Nimbus (no later canon)", snapshot(B, "harry-potter", position="chapter-50").get("broom"), "Nimbus Two Thousand")
check("B sirius never met", snapshot(B, "harry-potter+sirius-black", position="chapter-50").get("bond"), "strangers")
check("B no branch errors from fixture track", BRANCH_ERRORS, [])
check("B cutoff past divergence point is clamped and reported", (BRANCH_ERRORS, snapshot(B, "harry-potter", "PoA:11", position="chapter-50").get("broom")), ([("no-horcruxes", "PoA:11")], "Nimbus Two Thousand"))
BRANCH_ERRORS.clear()
sr = lambda a, ch: snapshot(T, "harry-potter", position=ch).get(a)
check("R sight blind from chapter-01", sr("sight", "chapter-01"), "blind")
check("R glasses removed (C1 remove)", sr("glasses", "chapter-05"), None)
check("R role at chapter-08 absent (PS:9 not reached)", sr("role", "chapter-08"), None)
check("R role adapted at chapter-09 (C2 adapt)", sr("role", "chapter-09"), "Gryffindor Seeker, flying by sound and feel")
check("R broom kept at chapter-10 (C3 keep)", sr("broom", "chapter-10"), "Nimbus Two Thousand")
check("R canon still happens: house at chapter-09", sr("house", "chapter-09"), "Gryffindor")
check("R reach: canon rows each divergence's overrides meet ahead", reach_candidates(T),
      [("D2", "harry-potter.glasses", "PS:2"), ("D3", "harry-potter.role", "PS:9")])
check("R reach: every candidate is a decided divergence conflict", all(
    f"— {e} (" in (EX/"projects/blind-harry/reviews/canon.md").read_text() for _, e, _ in reach_candidates(T)), True)
br = pyaml("no-horcruxes"); del br["setting"]["divergence_point"]
check("schema branch without divergence point rejected", schema("project").is_valid(br), False)
og = pyaml("blind-harry"); og["setting"]["type"] = "original"; og["setting"].pop("fidelity")
check("schema follow on original rejected", schema("project").is_valid(og), False)
og = pyaml("second-year-tournament"); og["setting"] = {"type": "original", "order": og["setting"]["order"]}
check("schema order on original rejected", schema("project").is_valid(og), False)
og = pyaml("two-witnesses"); og["setting"] = {k: v for k, v in og["setting"].items() if k != "fidelity"}; og["setting"]["type"] = "original"
check("schema fidelity_notes on original rejected", schema("project").is_valid(og), False)
og = pyaml("two-witnesses"); og.pop("layers")
check("schema established without layers rejected", schema("project").is_valid(og), False)
og["layers"] = []
check("schema established with empty layers rejected", schema("project").is_valid(og), False)
og = pyaml("lantern-road"); check("schema original without layers accepted", schema("project").is_valid(og), True)
og["layers"] = pyaml("two-witnesses")["layers"]
check("schema original with layers rejected", schema("project").is_valid(og), False)
bad = pyaml("hogwarts-at-warp"); bad["setting"]["order"] = ["PS"]
check("schema rejects order beside a universe layer", schema("project").is_valid(bad), False)
bad = pyaml("second-year-tournament"); bad["setting"]["orders"] = {"harry-potter": bad["setting"].pop("order")}
check("schema rejects orders without a universe layer", schema("project").is_valid(bad), False)
check("V no project keeps an adherence file; the settings are in project.yaml", sorted(f.parent.parent.name for f in (EX/"projects").glob("*/bible/canon.md")), [])

# --- True from and hidden canon (§4.4, §6.12, §7.2) ----------------------------------------
check("H snape loyalty not resolved at PS:17", g(PURIST, "severus-snape", "PS:17", "loyalty"), None)
check("H snape loyalty is a hidden truth at PS:17", hidden(PURIST, "severus-snape", "PS:17"), {"loyalty"})
check("H hidden truth even at PS:1", hidden(PURIST, "severus-snape", "PS:1"), {"loyalty"})
check("H not hidden once revealed (DH:33)", (hidden(PURIST, "severus-snape", "DH:33"), g(PURIST, "severus-snape", "DH:33", "loyalty")), (set(), "loves Lily Potter, and protects Harry for her sake"))
check("H branch: hidden at chapter-05", snapshot(B, "severus-snape", position="chapter-05").get("loyalty"), None)
check("H branch: revealed early at chapter-20 (D2)", snapshot(B, "severus-snape", position="chapter-20").get("loyalty"), "loves Lily Potter, and protects Harry for her sake")
for r in Package("harry-potter").all_rows():
    if r.get("True from"): assert HP.cmp(r["True from"], r["As of"]) <= 0, r
check("V True from never later than As of", True, True)
for r in table(EX/"projects/no-horcruxes/bible/divergences.md", "## Hidden canon"):
    ok = (r["Decision"] != "reveal-early" or r["Divergence"] not in ("", "—")) and (r["Decision"] != "other" or r["Note"])
    check(f"V hidden canon decision {r['Entity']}.{r['Attribute']}", ok, True)

# --- series: a project layer (§2.2, §6.4) -----------------------------------------------
S2 = Stack.of("two-witnesses-ii")
check("L hidden truth decided in book 1 binds book 2", (hidden(S2, "severus-snape", "OotP:1"), hidden_decisions(S2, "severus-snape")), ({"loyalty"}, {"loyalty": "keep-hidden"}))
EARLY = Stack(S2.refs[:-1] + ["project:two-witnesses@chapter-00"])
check("L a decision made after the pin does not carry over", hidden_decisions(EARLY, "severus-snape"), {})

# --- errata (§4.4, §5.2, §6.9, §6.13) --------------------------------------------------
CORRECT, ERROR = "his mother's echo emerges first, then his father's", "his father's echo emerges first, then his mother's"
check("E erratum rows never resolve, in every mode", [g(Stack(PURIST.refs, m), "harry-potter", "GoF:37", "graveyard-echoes") for m in ("precedence", "recency", "fill")], [CORRECT] * 3)
check("E the corrected quotation resolves", (quote(PURIST, "harry-potter", "q2", "GoF:37"), quote_resolve(PURIST, "harry-potter", "q2", "GoF:37", "Line")[1]), ("lily-potter", []))
check("E no ties anywhere", ties(PURIST, "harry-potter", "GoF:37"), {})
def package_ties(p, tiers=None):
    """§4.4: rows of one package sharing entity, attribute, tier, and point with different values."""
    tiers = tiers or p.sources; groups = {}
    for r in p.all_rows():
        groups.setdefault((r["_entity"], r["Attribute"], r["As of"], tiers[r["Source"]]), set()).add(r["Value"])
    f = p.dir/"quotations.md"
    if f.exists():
        for r in table(f, "## Quotations"):
            for col in ("Speaker", "Line"):
                if r[col]: groups.setdefault((r["ID"], col, r["As of"], tiers[r["Source"]]), set()).add(r[col])
    return sorted(k for k, v in groups.items() if len(v) > 1)
check("E no package in the examples holds tied rows", [p for f in PKG_FILES for p in [Package(f.parent.relative_to(EX/"worlds").as_posix().replace("/base", "", 1) if f.parent.name == "base" else f.parent.relative_to(EX/"worlds").as_posix())] if package_ties(p)], [])
HPB = Package("harry-potter")
check("E the first printing registered as primary would tie", package_ties(HPB, dict(HPB.sources, **{"gof-first-printing": "primary"})),
      [("harry-potter", "graveyard-echoes", "GoF:34", "primary"), ("q2", "Line", "GoF:34", "primary"), ("q2", "Speaker", "GoF:34", "primary")])
# --- fan works insert their own works (§4.10) ---------------------------------------
FW = ENRICH.ruler(); FIC = Package("harry-potter/fanfic/example")
check("FI a fan work's inserted work is valid only with it in the stack", (isvalid(FW, "FIC:20"), isvalid(HP, "FIC:20"), isvalid(FW, "FIC:25")), (True, False, False))
check("FI the fan work sorts after the books", (FW.cmp("DH:36", "FIC"), FW.cmp("FIC:3", "FIC:20")), (-1, -1))
check("FI its post-canon rows are ordered by its chapters", [g(ENRICH, "harry-potter", c, "role") for c in ("DH:36", "FIC:10", "FIC:20")],
      ["Gryffindor Seeker", "Auror", "head of the Auror Office"])
check("FI dated on one point instead, the same rows would tie (§4.4)",
      bool(package_ties(type("P", (), {"sources": FIC.sources, "dir": FIC.dir, "all_rows": lambda s: [dict(r, **{"As of": "DH:36"}) for r in FIC.all_rows() if r["Attribute"] == "role"]})())), True)
INSERTS = {f.parent for f in (EX/"worlds").rglob("canon-timeline.md") if has(f, "## Insert")}
check("FI only official and fanfic packages insert", sorted({load(d/"package.yaml")["kind"] for d in INSERTS}), ["fanfic", "official"])
check("E only base, official, and adaptation packages may register errata", sorted(k for k, v in KIND_TIERS.items() if "erratum" in v), ["adaptation", "base", "official"])
def errata(stack, entity, cutoff, base=None):
    """The stack's erratum rows for an entity, at or before the cutoff: {attribute: {values}}."""
    base = base or next(iter(stack.bases)); ruler = stack.ruler(base); out = {}
    for _, p in stack.packages:
        if p.base != base: continue
        for r in p.rows(entity):
            if p.sources.get(r["Source"]) == "erratum" and ruler.cmp(r["As of"], cutoff) <= 0:
                out.setdefault(r["Attribute"], set()).add(r["Value"])
    return out
def erratum_use(snap, err, attr, value):
    """§6.9: prose relying on an erratum's value that the snapshot (divergences applied) does not give."""
    return value in err.get(attr, set()) and snap.get(attr) != value
ERR = errata(PURIST, "harry-potter", "GoF:37"); SNAP = snapshot(PURIST, "harry-potter", "GoF:37")
check("E prose using the error is erratum use", erratum_use(SNAP, ERR, "graveyard-echoes", ERROR), True)
check("E prose following the corrected text is not", erratum_use(SNAP, ERR, "graveyard-echoes", CORRECT), False)
check("E a divergence that sets the erratum's value covers it", erratum_use(dict(SNAP, **{"graveyard-echoes": ERROR}), ERR, "graveyard-echoes", ERROR), False)
check("L project layer ledgers", S2.ledgers(), [("two-witnesses", "chapter-02")])
check("L book 1's D1 applies in book 2", snapshot(S2, "cedric-diggory").get("status"), "alive")
check("L book 1's D2 applies in book 2", snapshot(S2, "cedric-diggory").get("scars"), "curse scar across his chest")
check("L without the project layer, canon", snapshot(Stack(S2.refs[:-1]), "cedric-diggory", "OotP:1").get("status"), "dead")
check("L book 2 resolves at its own cutoff", track_cutoff("two-witnesses-ii", "chapter-01", pyaml("two-witnesses-ii")["setting"]["cutoff"]), "OotP:1")
def relisted(stack):
    """Every package layer of a project layer is relisted at the same major version (§2.2)."""
    mine = {Stack.parse_ref(r)[1]: Stack.parse_ref(r)[2] for r in stack.refs if Stack.parse_ref(r)[0] != "project"}
    for p, _ in stack.projects:
        for r in Stack.of(p).refs:
            kind, ident, pin = Stack.parse_ref(r)
            if kind == "project": continue
            if ident not in mine or mine[ident].split(".")[0] != pin.split(".")[0] or tuple(map(int, mine[ident].split("."))) < tuple(map(int, pin.split("."))): return False
    return True
check("L book 1's package layers relisted", relisted(S2), True)
check("L dropping a relisted layer fails", relisted(Stack([r for r in S2.refs if "fanon" not in r], "recency", "two-witnesses-ii")), False)
check("L pinned chapter exists in book 1's ledger range", chap(S2.projects[0][1]) >= min(chap(d["First occurs"]) for d in table(EX/"projects/two-witnesses/bible/divergences.md", "## Divergences")), True)

# --- union across layers and the composed bible (§2.7, §7.6) ---------------------------
def compose_roster(stack):
    """The compose skill's roster view: (slug, layer) per row; a repeated key is an error."""
    out = {}
    layers = [(p.id, p.roster()) for _, p in stack.packages]
    for proj, _ in stack.ledgers() + ([(stack.project, None)] if stack.project else []):
        f = EX/"projects"/proj/"bible/characters/_roster.md"
        layers.append((f"project:{proj}", table(f, "## Characters") if f.exists() else []))
    for layer, rows in layers:
        for r in rows:
            if r["Slug"] in out: raise StackError(f"{layer} redefines {r['Slug']} from {out[r['Slug']]}")
            out[r["Slug"]] = layer
    return out
for p in PROJECTS:
    s = Stack.of(p); check(f"V union keys unique {p}", isinstance(compose_roster(s), dict), True)
cr = compose_roster(S2)
check("L composed roster: book 1's original cast, with provenance", cr.get("mara-quill"), "project:two-witnesses")
check("L composed roster: canon cast from the base", cr.get("cedric-diggory"), "harry-potter")
def extensions_ok(stack):
    """An extension sheet (front matter `extends`) names a lower layer that defines the slug (§2.7)."""
    seen = {}
    for i, p in stack.packages:
        for f in (p.dir/"characters").glob("[!_]*.md") if (p.dir/"characters").exists() else []:
            fm = front(f)
            if "extends" in fm:
                if fm["extends"] not in seen or f.stem not in seen[fm["extends"]]: return False
            elif f.stem not in {r["Slug"] for r in p.roster()}: return False
        seen[p.id] = {r["Slug"] for r in p.roster()}
    return True
check("V extension sheets extend a lower layer", extensions_ok(ENRICH), True)
raises("V fanon below its base rejected", lambda: Stack(["harry-potter/fanon@1.0.4", "harry-potter@3.2.1"]), StackError)
raises("V wrong package pin rejected", lambda: Stack(["harry-potter@2.1.0"]), StackError)

# --- packages: kinds, ids, sources, points ------------------------------------------
for f in PKG_FILES:
    p = Package(f.parent.relative_to(EX/"worlds").as_posix().replace("/base", "", 1) if f.parent.name == "base" else f.parent.relative_to(EX/"worlds").as_posix())
    check(f"V id matches folder {p.id}", p.cfg["id"], p.id)
    check(f"V source tiers fit kind {p.id}", set(p.sources.values()) <= KIND_TIERS[p.kind], True)
    for dep in p.cfg["relies-on"]:
        did, ver = dep.split("@"); check(f"V relies-on pin {p.id} -> {did}", Package(did).cfg["version"], ver)
    s = Stack([*p.cfg["relies-on"], f"{p.id}@{p.cfg['version']}"]); r = s.ruler(p.base)
    for row in p.all_rows():
        assert row["Source"] in p.sources, (p.id, row); r.key(row["As of"])
    check(f"V sources and points valid {p.id}", True, True)
for proj in ["two-witnesses", "the-long-way-back", "three-brothers"]:
    divs = {d["ID"] for d in table(EX/f"projects/{proj}/bible/divergences.md", "## Divergences")}
    cons = {c["Divergence"] for c in table(EX/f"projects/{proj}/bible/divergences.md", "## Consequences")}
    check(f"V consequences {proj}", divs <= cons, True)
for t in table(EX/"projects/the-long-way-back/bible/timelines.md", "## Legs"):
    for pt in (t["Departs"], t["Arrives"]): ST.key(pt.split("@")[0])
    ST.key(t["Personal cutoff"])
check("V frames points valid", True, True)

# --- theories and theory conflicts (§6.13, §10.13) ------------------------------------
TB = "three-brothers"; TBS = Stack.of(TB)
theories = entries(pkg_dir("harry-potter/theories")/"theories.md")
claims = {t: {int(k.split("-")[1]) for k in e if k.startswith("claim-")} for t, e in theories.items()}
check("Q theory claims numbered", claims["T1"], {1, 2, 3, 4})
check("Q theories never resolve into state", snapshot(TBS, "albus-dumbledore"), {})
def basis(d):
    m = re.fullmatch(r"(\S+):(T\d+) \(claims? ([\d, ]+)\)", d.get("Basis", ""))
    return (m[1], m[2], {int(x) for x in m[3].split(", ")}) if m else None
DV = EX/f"projects/{TB}/bible/divergences.md"
adopted = [basis(d) for d in table(DV, "## Divergences") if basis(d)]
check("Q basis parsed", adopted, [("harry-potter/theories", "T1", {1, 3, 4})])
check("Q basis package is a layer", all(any(r.startswith(pk + "@") for r in TBS.refs) for pk, _, _ in adopted), True)
check("Q basis claims exist", all(c <= claims[t] for _, t, c in adopted), True)
tc = table(DV, "## Theory conflicts")
check("Q conflict decisions valid", all(r["Decision"] in {"keep", "adapt", "discard"} for r in tc), True)
check("Q conflict points valid", all(TBS.ruler().key(r["At"]) for r in tc), True)
used = {(pk + ":" + t, c) for pk, t, cs in adopted for c in cs}
check("Q discarded claims not adopted", all((r["Theory"], int(r["Claim"])) not in used for r in tc if r["Decision"] == "discard"), True)
check("Q kept or adapted claims adopted", all((r["Theory"], int(r["Claim"])) in used for r in tc if r["Decision"] != "discard"), True)
check("Q adapt needs a note", all(r["Note"] for r in tc if r["Decision"] == "adapt"), True)
check("Q conflict after cutoff still listed", any(TBS.ruler().cmp(r["At"], "DH:30") > 0 for r in tc), True)
def erratum_evidence(theory, stack=PURIST):
    """§6.13: a theory's evidence items that cite an erratum row: its point, and a citation
    that begins with the erratum row's. [(point, erratum source)]."""
    items = [re.fullmatch(r"(\S+) \((.*)\)", e.strip()) for e in theories[theory].get("evidence", "").split(";")]
    err = {(r["As of"], r["Citation"], r["Source"]) for _, p in stack.packages for r in p.all_rows() if p.sources.get(r["Source"]) == "erratum"}
    return sorted({(m[1], s) for m in items if m for pt, cit, s in err if m[1] == pt and m[2].startswith(cit)})
check("Q a theory resting on an erratum is marked", (erratum_evidence("T2"), erratum_evidence("T1")), ([("GoF:34", "gof-first-printing")], []))

# --- time-travel mechanisms (§9.1, §10.24) and branches (§10.16) ------------------
MODELS = {"dilation", "fixed", "loop", "mutable", "branching", "feedback"}
mech = entries(pkg_dir("star-trek")/"time-travel.md")
check("M star-trek mechanisms", sorted(mech), ["temporal-rift"])
check("M models and free will valid", all(e.get("model") in MODELS and e.get("free-will", "everyone") in {"everyone", "traveler", "none"} for e in mech.values()), True)
check("M spec example model valid", entries(ROOT/"spec/10-formats.md")["time-turner"]["model"], "fixed")
check("M time-travel.md indexed", "time-travel.md" in {r["Path"] for r in table(pkg_dir("star-trek")/"index.md", "## Files")}, True)
TLB = EX/"projects/the-long-way-back"
legs = table(TLB/"bible/timelines.md", "## Legs")
check("M every leg names a known mechanism", all(t["Mechanism"] in mech for t in legs), True)
br = {b["Branch"]: b for b in table(TLB/"bible/branches.md", "## Branches")}
check("M branch statuses valid", all(b["Status"] in {"live", "overwritten", "abandoned"} for b in br.values()), True)
check("M branch parents and mechanisms known", all((b["Splits from"] in br and b["Mechanism"] in set(mech) | {"—"}) or (n == "main" and not b["Splits from"]) for n, b in br.items()), True)
check("M mutable rift overwrote alt-war, main live", (br["alt-war"]["Status"], br["main"]["Status"]), ("overwritten", "live"))
used = {t["Arrives"].split("@")[1] for t in legs} | {t["Departs"].split("@")[1] for t in legs}
check("M every branch a leg uses is registered", used <= set(br), True)

# --- renumbering chapters (§13.10) ---------------------------------------------------
def first_movable(project):
    """The lowest chapter number renumber may move: after every chapter readers have seen,
    and after every pin another project in the workspace holds on this one."""
    seen = [front(f)["chapter"] for f in (EX/"projects"/project/"manuscript").glob("chapter-*.md")
            if front(f).get("status") in {"released", "early-access"}] if (EX/"projects"/project/"manuscript").exists() else []
    pins = [chap(pin) for q in (EX/"projects").iterdir() if (q/"project.yaml").exists()
            for p, pin in Stack.of(q.name).projects if p == project]
    return max(seen + pins, default=0) + 1
check("RN early-access chapter 3 keeps its id; chapter 4 may move", first_movable("the-long-way-back"), 4)
check("RN a pinned chapter keeps its id (two-witnesses-ii pins chapter-02)", first_movable("two-witnesses"), 3)
check("RN nothing seen or pinned: any chapter may move", first_movable("three-brothers"), 1)

# --- story-dated rows (§4.11) ----------------------------------------------------
TLBS = Stack.of("the-long-way-back")
check("SD before its chapter, the starting state", snapshot(TLBS, "mira-oduya", position="chapter-02")["role"], "operations officer, USS Enterprise-C")
check("SD from its chapter, the story-dated row", snapshot(TLBS, "mira-oduya", position="chapter-03")["role"], "displaced officer aboard the USS Enterprise-D")
check("SD after the last chapter", snapshot(TLBS, "mira-oduya")["role"], "displaced officer aboard the USS Enterprise-D")
def story_dated_ok(d):
    """Every story-dated row cites project, has no As of, and describes the project's own entity."""
    own = {r["Slug"] for r in table(d/"characters/_roster.md", "## Characters") if r.get("Origin", "original") == "original"} if (d/"characters/_roster.md").exists() else set()
    rows = []
    for f in (d/"characters").glob("[!_]*.md") if (d/"characters").exists() else []:
        rows += [(r, front(f).get("origin") == "original") for r in table(f, "## State history")]
    if (d/"relationships.md").exists():
        rows += [(r, all(s in own for s in r["Pair"].split("+"))) for r in table(d/"relationships.md", "## State history")]
    if (d/"knowledge.md").exists():
        rows += [(r, r["Character"] in own) for r in table(d/"knowledge.md", "## Knowledge")]
    return all(r["Source"] == "project" and not r["As of"] and mine for r, mine in rows if r.get("From chapter"))
check("SD story-dated rows valid in every project", all(story_dated_ok(d/"bible") for d in (EX/"projects").iterdir()), True)

# --- the series ruler (§4.12) and seam conflicts (§6.14) ----------------------------------
LRB = Stack.of("lantern-road-before"); LR = LRB.ruler()
check("SR book 1's chapters are points, to the pin", [isvalid(LR, p) for p in ("lantern-road:9", "lantern-road:12", "lantern-road:13")], [True, True, False])
check("SR inserts before and after book 1", [LR.cmp("youth", "lantern-road:1"), LR.cmp("lantern-road:12", "after")], [-1, -1])
check("SR the inserts are only on the later book's ruler", isvalid(Stack(["project:lantern-road@chapter-12"]).ruler(), "youth"), False)
check("SR a self-contained stack has no ruler of its own", raises_ok(lambda: Stack.of("lantern-road").ruler(), StackError), True)
check("SE prequel side: book 1's starting state carried back", snapshot(LRB, "ines-varga", position="chapter-01"),
      {"eyes": "grey", "role": "apprentice lamplighter", "born": "NR 12-02-14"})
check("SE prequel side: what happens in book 1 has not happened yet", seams(LRB, "ines-varga", position="chapter-01"), set())
check("SE sequel side: book 1's chapter 9 holds", snapshot(LRB, "ines-varga", position="chapter-06")["role"], "master lamplighter")
check("SE sequel side raises nothing", seams(LRB, "ines-varga", position="chapter-06"), set())
check("SR the later book's own inserts are valid points, and on its order", ([isvalid(LR, p) for p in ("youth", "after")],
      sorted(LR.segments, key=LR.segments.get)), ([True, True], [("youth",), ("lantern-road",), ("after",)]))
_seam_rules = seam_rules
seam_rules = lambda stack: _seam_rules(stack) + [{"Item": "lantern-road:ines-varga.role@chapter-09", "Decision": "carry-back",
                                                  "Divergence": "—", "Decided in": "chapter-01", "Note": ""}]
check("SE a carried-back book-1 row holds before its anchor, not time-filtered (§7.2 step 3)",
      snapshot(LRB, "ines-varga", position="chapter-01")["role"], "master lamplighter")
seam_rules = _seam_rules
check("SE patterns: exact beats pattern, later pattern wins", [seam_match("lantern-road:ines-varga.*", "lantern-road:ines-varga.role@chapter-09"),
      seam_match("lantern-road:*.*@*", "lantern-road:ines-varga.role@chapter-09"), seam_match("two-witnesses:D*", "two-witnesses:D12")], [False, True, True])
check("SE undecided items ahead are set aside and returned", (snapshot(S2, "mara-quill", "GoF:20"), seams(S2, "mara-quill", "GoF:20")),
      ({}, {"two-witnesses:mara-quill.house", "two-witnesses:mara-quill.year"}))
check("SE an undecided divergence ahead does not apply", (snapshot(S2, "cedric-diggory", "GoF:20"), seams(S2, "cedric-diggory", "GoF:20")),
      ({"status": "alive", "house": "Hufflepuff", "role": "Hogwarts Triwizard champion"}, {"two-witnesses:D1", "two-witnesses:D2"}))
check("SE a sequel set after book 1 raises nothing", seams(S2, "cedric-diggory"), set())
def earlier_start(project):
    """The seam audit's first question (§6.14): is the first chapter set before a layer's cutoff at its pin?"""
    s = Stack.of(project); r = s.ruler(); st = pyaml(project)["setting"]
    first = track_cutoff(project, "chapter-01", st.get("cutoff"))
    return [p for p, pin in s.projects if r.cmp(first, anchor(p, pin)) < 0]
check("SE the seam audit flags an earlier start", (earlier_start("lantern-road-before"), earlier_start("two-witnesses-ii")), (["lantern-road"], []))
def value_seams(stack, entities):
    """Value seams (§6.14): attributes the later book's stack resolves differently from the
    earlier book, at the earlier book's cutoff at its pin."""
    out = []
    for p, pin in stack.projects:
        later = Stack(stack.refs, stack.resolution)
        for e in entities:
            a, b = snapshot(Stack.of(p), e, position=pin), snapshot(later, e, anchor(p, pin))
            out += [(e, k) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    return out
CANON = ["harry-potter", "cedric-diggory", "hermione-granger", "severus-snape"]
check("SE same stack and mode: no value seams", value_seams(S2, CANON), [])
VS = value_seams(Stack(S2.refs, "precedence", "two-witnesses-ii"), CANON)
check("SE another resolution mode raises a value seam", VS, [("harry-potter", "broom")])
def branch_ok(setting, layers):
    """A branch stays a branch (§6.14): the later book is a branch, diverging no later."""
    s = Stack(layers)
    if not s.projects: return True
    r = s.ruler()
    for p, _ in s.projects:
        q = pyaml(p)["setting"]
        if q.get("follow") == "branch" and (setting.get("follow") != "branch" or r.cmp(setting["divergence_point"], q["divergence_point"]) > 0): return False
    return True
check("SE every project keeps its layers' branches", all(branch_ok(pyaml(p)["setting"], pyaml(p).get("layers", [])) for p in PROJECTS), True)
NH = ["harry-potter@3.2.1", "project:no-horcruxes@chapter-01"]
check("SE a retelling sequel to a branch is rejected", branch_ok({"cutoff": "CoS:1"}, NH), False)
check("SE a branch sequel diverging later is rejected", branch_ok({"follow": "branch", "divergence_point": "CoS:1"}, NH), False)
check("SE a branch sequel diverging no later is accepted", branch_ok({"follow": "branch", "divergence_point": "PS:17"}, NH), True)
INH = Stack(["harry-potter@3.2.1", "project:second-year-tournament@chapter-03"])
check("SE the order is inherited from a project layer", (INH.order() == pyaml("second-year-tournament")["setting"]["order"], INH.ruler().cmp("GoF:1", "CoS:1")), (True, -1))
check("V seam decisions fit their items", all(r["Decision"] in ({"keep-earlier", "accept", "other"} if ":" not in r["Item"] else {"carry-back", "not-yet", "other"})
      and (r["Decision"] != "other" or r["Note"]) for f in (EX/"projects").glob("*/bible/divergences.md") if has(f, "## Seam conflicts") for r in table(f, "## Seam conflicts")), True)

def promote(project):
    """§2.9 step 4: a self-contained book's rows re-cited to its own source, story-dated rows dated on its work."""
    out = []
    for f in (EX/"projects"/project/"bible/characters").glob("[!_]*.md"):
        for r in table(f, "## State history"):
            fc = r.get("From chapter", "")
            r = {k: v for k, v in r.items() if k != "From chapter"}
            if r["Source"] == "project": r["Source"] = project
            if fc: r["As of"] = f"{project}:{chap(fc)}"
            out.append((f.stem, r["Attribute"], r["Value"], r["As of"], r["Source"]))
    return out
check("P promotion re-cites project rows and dates story-dated ones on the book's work", sorted(promote("lantern-road")),
      [("ines-varga", "born", "NR 12-02-14", "", "lantern-road"), ("ines-varga", "eyes", "grey", "", "lantern-road"), ("ines-varga", "role", "apprentice lamplighter", "", "lantern-road"),
       ("ines-varga", "role", "master lamplighter", "lantern-road:9", "lantern-road")])
check("P the promoted rows are valid on the series ruler", all(not a or isvalid(LR, a) for *_, a, _ in promote("lantern-road")), True)
def scene_warnings(project, scenes):
    """§7.5: a scene with no travelers set later than its chapter's sync-point cutoff. scenes: [(chapter, world point, travelers)]."""
    s = Stack.of(project); r = s.ruler(); st = pyaml(project)["setting"]
    return [(c, wp) for c, wp, trav in scenes if not trav and r.cmp(wp.split("@")[0], track_cutoff(project, c, st.get("cutoff"))) > 0]
check("F a flash-forward with no travelers is warned about", scene_warnings("the-long-way-back",
      [("chapter-01", "TNG:3:15@main", ["mira-oduya"]), ("chapter-02", "TNG:3:14@main", []), ("chapter-03", "TNG:4:1@main", [])]), [("chapter-03", "TNG:4:1@main")])
def promote_ruler(project, last):
    """§2.9 step 3: the book as a work, the last segment after any eras; step 5: one sync point per chapter."""
    segs = [(project,)]; counts = {(project,): str(last)}
    syncs = [(f"chapter-{n:02d}", f"{project}:{n}") for n in range(1, last + 1)]
    return segs, counts, syncs
segs, counts, syncs = promote_ruler("lantern-road", 12)
SER = SeriesRuler("lantern-road", "chapter-12", [])
check("P the promoted ruler is the series ruler without later books' inserts",
      (sorted(SER.segments, key=SER.segments.get), {s: SER.counts[s] for s in SER.segments}), (segs, counts))
check("P the promoted project's sync points are book 1's anchors", all(anchor("lantern-road", c) == pt for c, pt in syncs), True)
og = pyaml("lantern-road"); og["setting"]["cutoff"] = "lantern-road:3"
check("schema cutoff on original rejected", schema("project").is_valid(og), False)
def seam_entries(project):
    """§10.19: the seam audit's `### S<n> — <item>` entries, and its `- pin:` line."""
    lines = (EX/"projects"/project/"reviews/canon.md").read_text(encoding="utf-8").splitlines()
    i = lines.index("## Seam conflicts"); body = []
    for l in lines[i + 1:]:
        if l.startswith("## "): break
        body.append(l)
    items = [l.split(" — ", 1)[1] for l in body if re.match(r"### S\d+ — ", l)]
    return items, any(l.startswith("- pin:") for l in body)
SI, PIN = seam_entries("lantern-road-before")
ROWS = [r["Item"] for r in table(EX/"projects/lantern-road-before/bible/divergences.md", "## Seam conflicts")]
check("SE the seam audit notes the earlier start", PIN, bool(earlier_start("lantern-road-before")))
check("SE every seam entry is decided, and every decision answers an entry",
      (all(any(seam_match(p, i) for p in ROWS) for i in SI), all(any(seam_match(p, i) for i in SI) for p in ROWS), len(SI)), (True, True, 3))
check("T the inversion candidates table has its required columns",
      list(table(EX/"projects/second-year-tournament/reviews/canon.md", "## Inversion candidates")[0])[:2], ["Candidate", "Addressed"])
check("F a traveler may be set later", scene_warnings("the-long-way-back", [("chapter-03", "TNG:4:1@main", ["mira-oduya"])]), [])

# --- registered columns (§10.0, §10.3) -------------------------------------------
REQUIRED = {("timelines.md", "## Legs"): ["Traveler", "Leg", "Mechanism", "Departs", "Arrives", "Personal cutoff", "Chapter"],
            ("branches.md", "## Branches"): ["Branch", "Splits from", "At", "Cause", "Mechanism", "Status"]}
idx = TLB/"bible/index.md"   # ## Columns is optional (§10.3)
reg = {(c["File"], c["Table"], c["Column"]) for c in table(idx, "## Columns")} if has(idx, "## Columns") else set()
for (f, h), req in REQUIRED.items():
    hdr = list(table(TLB/"bible"/f, h)[0]) if table(TLB/"bible"/f, h) else req
    check(f"C required columns in order {f} {h}", hdr[:len(req)], req)
    check(f"C added columns registered {f} {h}", {(f, h, c) for c in hdr[len(req):]} <= reg, True)
check("C registry does not repeat a required column", any(c in REQUIRED.get((f, h), []) for f, h, c in reg), False)

# --- in-world time (§4.13) ----------------------------------------------------------
class Calendar:
    """A world's calendar: `iso`, or a custom mapping of eras and months. Dates become spans of
    (year on one line, month, day) tuples; a calendar without months uses (year, 0|1, 0)."""
    def __init__(self, spec):
        self.iso = spec == "iso"; self.months = []
        if self.iso: return
        eras = spec.get("eras") or []
        if not eras: raise ValueError("a calendar needs an era")
        ids = [e["id"] for e in eras]
        if len(set(ids)) != len(ids) or not all(re.fullmatch(r"[A-Z][A-Z0-9]*", i) for i in ids): raise ValueError("era ids")
        self.eras, start = {}, 1
        for i, e in enumerate(eras):
            if e.get("counts") == "down":
                if i != 0 or len(eras) == 1 or "years" in e: raise ValueError("only a first era, followed by another, counts down")
                self.eras[e["id"]] = ("down", 0)
            else:
                if i < len(eras) - 1 and not e.get("years"): raise ValueError(f"era {e['id']} needs years")
                self.eras[e["id"]] = ("up", start); start += e.get("years", 0)
        self.months = [m["days"] for m in spec.get("months", [])]
        if any(d < 1 for d in self.months): raise ValueError("a month of no days")
    def days(self, y, m):
        if not self.iso: return self.months[m - 1]
        if m == 2: return 29 if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0 else 28
        return 31 if m in (1, 3, 5, 7, 8, 10, 12) else 30
    def nmonths(self): return 12 if self.iso else len(self.months)
    def single(self, s):
        """One date, without range or ~: (start, end) tuples."""
        if self.iso:
            m = re.fullmatch(r"(-?[1-9]\d*|0)(?:-(\d{2})(?:-(\d{2}))?)?", s)
            if not m or m[1] == "-0": raise ValueError(s)
            y = int(m[1])
        else:
            m = re.fullmatch(r"([A-Z][A-Z0-9]*) ([1-9]\d*)(?:-(\d{2})(?:-(\d{2}))?)?", s)
            if not m or m[1] not in self.eras: raise ValueError(s)
            kind, start = self.eras[m[1]]; n = int(m[2])
            y = 1 - n if kind == "down" else start + n - 1
            m = [None, None, m[3], m[4]]
        mo, d = m[2], m[3]
        if not self.nmonths():
            if mo: raise ValueError(f"{s}: this calendar has no months")
            return (y, 0, 0), (y, 1, 0)
        if mo is None: return (y, 1, 1), (y, self.nmonths(), self.days(y, self.nmonths()))
        mo = int(mo)
        if not 1 <= mo <= self.nmonths(): raise ValueError(s)
        if d is None: return (y, mo, 1), (y, mo, self.days(y, mo))
        d = int(d)
        if not 1 <= d <= self.days(y, mo): raise ValueError(s)
        return (y, mo, d), (y, mo, d)
    def parse(self, s):
        """A date (§4.13): (start or None, end or None, approximate)."""
        if s.startswith("~"):
            lo, hi = self.single(s[1:]); return lo, hi, True
        if ".." in s:
            a, b = s.split("..", 1)
            if not a and not b: raise ValueError(s)
            lo = self.single(a)[0] if a else None; hi = self.single(b)[1] if b else None
            if lo and hi and lo > hi: raise ValueError(f"{s}: reversed")
            return lo, hi, False
        lo, hi = self.single(s); return lo, hi, False

def dcmp(a, b):
    """-1 before, 1 after, None can't tell (§4.13)."""
    if a[2] or b[2]: return None
    if a[1] is not None and b[0] is not None and a[1] < b[0]: return -1
    if a[0] is not None and b[1] is not None and a[0] > b[1]: return 1
    return None
def dkey(a): return (0,) if a[0] is None else (1, *a[0])
def shift(a, years): return tuple(None if t is None else (t[0] + years, *t[1:]) for t in a[:2]) + (a[2],)
def age(born, on):
    """The range of ages, in whole years, from one date to another (§4.13)."""
    def whole(b, d): return d[0] - b[0] - ((d[1], d[2]) < (b[1], b[2]))
    return whole(born[1], on[0]), whole(born[0], on[1])

def calendar_of(stack, base=None):
    """The stack's calendar: its base's, else the original project at the root of its series (§4.13)."""
    if stack.bases: spec = (stack.bases[base] if base else next(iter(stack.bases.values()))).cfg.get("calendar")
    else:
        roots = [p for p, _ in stack.ledgers() if not Stack.of(p).refs] or [stack.project]
        spec = pyaml(roots[0]).get("calendar")
    return Calendar(spec) if spec else None

def ruler_files(stack, base=None):
    """(layer, canon-timeline) pairs whose ## Dates the stack reads: the base's and the inserting packages'."""
    b = stack.bases[base] if base else next(iter(stack.bases.values()))
    return [(p.id, p.dir/"canon-timeline.md") for _, p in stack.packages
            if p.base == b.id and p.kind in ("base", "official", "fanfic") and has(p.dir/"canon-timeline.md", "## Dates")]

def node_dates(stack, base=None):
    cal = calendar_of(stack, base); out = {}
    for layer, f in ruler_files(stack, base):
        for r in table(f, "## Dates"):
            node = Ruler.split(r["Node"])
            if node in out: raise ValueError(f"{r['Node']} dated twice")
            out[node] = (cal.parse(r["Date"]), layer)
    return out

def point_date(stack, pt, base=None):
    """The date of the deepest dated node containing a point, if any (§4.13)."""
    if not pt: return None
    path = stack.ruler(base, ordered=False).parse(pt)[0]; dates = node_dates(stack, base)
    for n in range(len(path), 0, -1):
        if path[:n] in dates: return dates[path[:n]][0]
    return None

def accepted(f):
    return [(r["Check"], r["Subject"], r) for r in table(f, "## Accepted")] if has(f, "## Accepted") else []

STATE_FILES = ("relationships.md", "species.md", "history.md", "titles.md")
def state_tables(d):
    """(file, key column or None, rows) for each state-history table in a bible directory."""
    out = [(f, None, table(f, "## State history")) for f in sorted((d/"characters").glob("[!_]*.md"))] if (d/"characters").exists() else []
    for name in STATE_FILES:
        f = d/name
        if f.exists(): out.append((f, "Pair" if name == "relationships.md" else "Entity", table(f, "## State history")))
    return out

def contradictions(stack, base=None, extra=()):
    """Chronology contradictions in a stack's packages (§4.13), less those an `## Accepted` row
    excuses in a layer that holds one of their rows or nodes. `extra`: (layer, dir) to add."""
    cal = calendar_of(stack, base); found, acc = [], set()
    layers = [(p.id, p.dir) for _, p in stack.packages if p.base == (base or next(iter(stack.bases)))] + list(extra)
    dates = node_dates(stack, base)
    for layer, f in ruler_files(stack, base):                    # outside-parent
        acc |= {(c, s, layer) for c, s, _ in accepted(f)}
        for r in table(f, "## Dates"):
            node = Ruler.split(r["Node"])
            for n in range(len(node) - 1, 0, -1):
                if node[:n] in dates:
                    if dcmp(dates[node][0], dates[node[:n]][0]) is not None:
                        found.append(("outside-parent", r["Node"], {layer, dates[node[:n]][1]}))
                    break
    born, died, edges = {}, {}, {}
    for layer, d in layers:
        for f, key, rows in state_tables(d):
            acc |= {(c, s, layer) for c, s, _ in accepted(f)}
            for r in rows:
                subj = r["Attribute"] if key is None else f"{r[key]}.{r['Attribute']}"
                ent = f.stem if key is None else r[key]
                if r["Attribute"] in ("born", "died") and r["Value"] != "(unset)":
                    (born if r["Attribute"] == "born" else died).setdefault(ent, []).append((cal.parse(r["Value"]), layer, subj.rsplit(".", 1)[0] + ".born" if key else "born"))
                if r["Attribute"] in ("parents", "descends-from") and r["Value"] != "(unset)":
                    edges.setdefault(ent, []).extend((p, layer, subj) for p in r["Value"].split("; "))
                when = r["Value"] if (r["Attribute"] == "date" and f.name == "history.md") else r.get("In-world")
                if not when: continue
                for pt in {r.get("True from") or r["As of"], r["As of"]} - {""}:
                    pd = point_date(stack, pt, base)
                    if pd and dcmp(cal.parse(when), pd) == 1: found.append(("in-world-after", subj, {layer}))
    for ent in born:
        for b, lb, subj in born[ent]:
            for dd, ld, _ in died.get(ent, []):
                if dcmp(b, dd) == 1: found.append(("born-died", subj, {lb, ld}))
    for ent, ups in edges.items():                               # lineage (§9.6)
        for p, le, _ in ups:
            for b, lb, subj in born.get(ent, []):
                for pb, lp, _ in born.get(p, []):
                    if dcmp(b, pb) == -1: found.append(("born-before-parent", subj, {lb, lp, le}))
    graph = {e: {p for p, *_ in ups} for e, ups in edges.items()}
    def reach(a):
        seen, todo = set(), [a]
        while todo:
            for y in graph.get(todo.pop(), ()):
                if y not in seen: seen.add(y); todo.append(y)
        return seen
    cycles = {}
    for ent, ups in edges.items():
        for p, le, subj in ups:
            if ent in reach(p) or p == ent:
                comp = frozenset(x for x in reach(ent) | {ent} if x == ent or ent in reach(x))
                cycles.setdefault(comp, []).append((subj, le))
    for items in cycles.values():                                # one acceptance excuses the whole cycle
        if not any(("ancestry-cycle", s, l) in acc for s, l in items): found.append(("ancestry-cycle", min(s for s, _ in items), set()))
    return sorted({(c, s) for c, s, ls in found if not any((c, s, l) in acc for l in ls)})

def chronology(stack, cutoff, base=None):
    """The events that resolve at a cutoff, sorted by date (§4.13)."""
    cal = calendar_of(stack, base); events = []
    for _, p in stack.packages:
        f = p.dir/"history.md"
        if f.exists(): events += [r["Entity"] for r in table(f, "## State history")]
    out = []
    for e in dict.fromkeys(events):
        s = snapshot(stack, e, cutoff, base=base)
        if "date" in s: out.append((dkey(cal.parse(s["date"])), len(out), e))
    return [e for *_, e in sorted(out)]

ISO = Calendar("iso"); LRC = calendar_of(Stack.of("lantern-road"))
P = ISO.parse
for s, ok in [("1991", True), ("1991-07-31", True), ("-43", True), ("991", True), ("0991", False), ("-0", False), ("1991-02-29", False),
              ("1992-02-29", True), ("1900-02-29", False), ("2000-02-29", True), ("1991-13", False), ("..1991", True), ("1998..", True),
              ("1971..1978", True), ("1978..1971", False), ("~1975", True), ("~1971..1978", False), ("..", False), ("NR 12", False)]:
    check(f"D iso date {s!r} {'valid' if ok else 'invalid'}", not raises_ok(lambda: P(s), ValueError), ok)
for s, ok in [("NR 12", True), ("NR 12-02-14", True), ("NR 12-05", False), ("NR 12-02-93", False), ("BL 5..OR 3", True), ("XX 5", False), ("NR 0", False), ("1991", False)]:
    check(f"D custom date {s!r} {'valid' if ok else 'invalid'}", not raises_ok(lambda: LRC.parse(s), ValueError), ok)
check("D 1991 vs 1991-09-01: can't tell", dcmp(P("1991"), P("1991-09-01")), None)
check("D 1990 before 1991-09-01", dcmp(P("1990"), P("1991-09-01")), -1)
check("D ..1991 before 1998..", dcmp(P("..1991"), P("1998..")), -1)
check("D ..1991 vs 1985: can't tell", dcmp(P("..1991"), P("1985")), None)
check("D ~1975 vs 2000: can't tell, approximate", dcmp(P("~1975"), P("2000")), None)
check("D ~1975 sorts at 1975", sorted(["2000", "~1975", "1980"], key=lambda s: dkey(P(s))), ["~1975", "1980", "2000"])
check("D eras: BL 2 and OR 5 are six years apart", LRC.parse("OR 5")[0][0] - LRC.parse("BL 2")[0][0], 6)
check("D eras: OR 300 is the year before NR 1", LRC.parse("NR 1")[0][0] - LRC.parse("OR 300")[0][0], 1)
check("D eras: BL 1 is just before OR 1", (dcmp(LRC.parse("BL 1"), LRC.parse("OR 1")), LRC.parse("OR 1")[0][0] - LRC.parse("BL 1")[0][0]), (-1, 1))
check("D age: born 1980-07-31, in 1991", age(P("1980-07-31"), P("1991")), (10, 11))
check("D age: on 1991-07-31 exactly", age(P("1980-07-31"), P("1991-07-31")), (11, 11))
check("D age in a custom calendar: born NR 12-02-14, in NR 30", age(LRC.parse("NR 12-02-14"), LRC.parse("NR 30")), (17, 18))
YEARS = Calendar({"eras": [{"id": "AC", "name": "after the Conquest"}]})
check("D a calendar without months: years only", (raises_ok(lambda: YEARS.parse("AC 298-03"), ValueError), age(YEARS.parse("AC 280"), YEARS.parse("AC 298"))), (True, (17, 18)))
for label, spec in [("no era", {"eras": []}), ("a down era not first", {"eras": [{"id": "A", "name": "a", "years": 5}, {"id": "B", "name": "b", "counts": "down"}]}),
                    ("a down era alone", {"eras": [{"id": "B", "name": "b", "counts": "down"}]}), ("an up era with no years, not last", {"eras": [{"id": "A", "name": "a"}, {"id": "B", "name": "b"}]}),
                    ("a month of no days", {"eras": [{"id": "A", "name": "a"}], "months": [{"name": "m", "days": 0}]}), ("a repeated era id", {"eras": [{"id": "A", "name": "a", "years": 3}, {"id": "A", "name": "b"}]})]:
    raises(f"D calendar rejected: {label}", lambda: Calendar(spec))
blocks = re.findall(r"```yaml\n(.*?)```", (ROOT/"spec/04-temporal.md").read_text(), re.S)
check("D the spec's calendars are valid", [bool(Calendar(yaml.safe_load(b)["calendar"])) for b in blocks], [True, True])
check("D the example's calendar is the spec's", pyaml("lantern-road")["calendar"], yaml.safe_load(blocks[1])["calendar"])

# schemas: who may declare a calendar
d = load(EX/"worlds/harry-potter/base/package.yaml"); d["notation"] = "japanese"; check("D schema: a base with iso and a notation", schema("package").is_valid(d), True)
d["calendar"] = yaml.safe_load(blocks[1])["calendar"]; check("D schema: a notation with a custom calendar rejected", schema("package").is_valid(d), False)
d = load(EX/"worlds/harry-potter/fanon/package.yaml"); d["calendar"] = "iso"; check("D schema: a fanon package's calendar rejected", schema("package").is_valid(d), False)
d = pyaml("two-witnesses"); d["calendar"] = "iso"; check("D schema: an established project's calendar rejected", schema("project").is_valid(d), False)
d = pyaml("lantern-road"); d["notation"] = "gregory"; check("D schema: a notation without iso rejected", schema("project").is_valid(d), False)
d = pyaml("lantern-road"); d["calendar"] = "gregorian"; check("D schema: an unknown calendar name rejected", schema("project").is_valid(d), False)

# every date in the examples parses in its stack's calendar
def example_dates(d):
    out = []
    for f, key, rows in state_tables(d):
        for r in rows:
            if r.get("In-world"): out.append(r["In-world"])
            if r["Attribute"] in ("born", "died") or (r["Attribute"] == "date" and f.name == "history.md"): out.append(r["Value"])
    f = d/"canon-timeline.md"
    if has(f, "## Dates"): out += [r["Date"] for r in table(f, "## Dates")]
    return out
for pid, cal in [("harry-potter", ISO), ("harry-potter/fanfic/example", ISO), ("star-trek", ISO)]:
    check(f"D every date in {pid} parses", all(not raises_ok(lambda: cal.parse(s), ValueError) for s in example_dates(pkg_dir(pid))), True)
for proj in ["lantern-road", "the-long-way-back"]:
    cal = calendar_of(Stack.of(proj)); ds = example_dates(EX/"projects"/proj/"bible")
    check(f"D every date in {proj} parses", (len(ds) > 0, all(not raises_ok(lambda: cal.parse(s), ValueError) for s in ds)), (True, True))
check("D the calendar is the base's, or the series root's", (calendar_of(PURIST).iso, calendar_of(TREK).iso, calendar_of(Stack.of("lantern-road-before")).iso), (True, True, False))

# the ruler's dates, and the cutoff's date
check("D the cutoff's date: PS:6", point_date(PURIST, "PS:6"), P("1991-09-01"))
check("D the deepest dated node: PS:6:2 is PS:6's", point_date(PURIST, "PS:6:2"), P("1991-09-01"))
check("D PS:7 falls back to PS", point_date(PURIST, "PS:7"), P("1991..1992"))
check("D GoF:37", point_date(PURIST, "GoF:37"), P("1994..1995"))
check("D an inserted work is dated by its package: FIC:20", point_date(ENRICH, "FIC:20"), P("1998.."))
check("D TNG:3:15", point_date(TREK, "TNG:3:15"), P("2366"))
check("D no dates, no date: a timeless row", point_date(PURIST, ""), None)
check("D order and date need not agree: PS:1 is ten years before PS:2", (HP.cmp("PS:1", "PS:2"), dcmp(point_date(PURIST, "PS:1"), point_date(PURIST, "PS:2"))), (-1, -1))

# ages
hb = P(snapshot(PURIST, "harry-potter", "GoF:37")["born"])
check("D harry's age at PS:5", age(hb, point_date(PURIST, "PS:5")), (11, 11))
check("D harry's age at PS:2", age(hb, point_date(PURIST, "PS:2")), (10, 10))
check("D harry's birth year is not known at PS:5", "born" in snapshot(PURIST, "harry-potter", "PS:5"), False)
TLW = Stack.of("the-long-way-back")
mb = P(snapshot(TLW, "mira-oduya", "TNG:3:15", position="chapter-03")["born"])
check("D mira by world dates at TNG:3:15 (a traveler: her own years are fewer)", age(mb, point_date(TLW, "TNG:3:15")), (47, 48))

# world history
check("D an event is an entity: its date resolves", snapshot(PURIST, "grindelwald-defeated", "PS:6")["date"], "1945")
check("D an event is visible only from its as-of", snapshot(PURIST, "grindelwald-defeated", "PS:5"), {})
check("D chronology at PS:5", chronology(PURIST, "PS:5"), ["voldemort-falls"])
check("D chronology at PS:6, sorted by date", chronology(PURIST, "PS:6"), ["grindelwald-defeated", "voldemort-falls"])
check("D chronology at CoS:9", chronology(PURIST, "CoS:9"), ["hogwarts-founded", "grindelwald-defeated", "voldemort-falls"])
hist = table(pkg_dir("harry-potter")/"history.md", "## State history")
check("D every event has a date row", {r["Entity"] for r in hist} <= {r["Entity"] for r in hist if r["Attribute"] == "date"}, True)
lr = table(EX/"projects/lantern-road/bible/history.md", "## State history")
check("D lantern-road's events in its own calendar", [r["Entity"] for r in sorted((r for r in lr if r["Attribute"] == "date"), key=lambda r: dkey(LRC.parse(r["Value"])))], ["lamps-first-lit", "road-rebuilt"])
def participant_warnings(stack, cutoff, base=None):
    cal = calendar_of(stack, base); out = []
    for e in chronology(stack, cutoff, base):
        s = snapshot(stack, e, cutoff, base=base); when = cal.parse(s["date"])
        for who in filter(None, s.get("participants", "").split("; ")):
            w = snapshot(stack, who, cutoff, base=base)
            if "born" in w and dcmp(when, cal.parse(w["born"])) == -1: out.append((e, who, "before born"))
            if "died" in w and dcmp(when, cal.parse(w["died"])) == 1: out.append((e, who, "after died"))
    return out
check("D no participant warnings in the example", participant_warnings(PURIST, "DH:36"), [])

# chronology contradictions and acceptances
check("D no unaccepted contradictions: the books", contradictions(PURIST), [])
check("D no unaccepted contradictions: with fanon and the fan work", contradictions(ENRICH), [])
check("D no unaccepted contradictions: Star Trek", contradictions(TREK), [])
check("D DH:33 (..1998) inside DH (1997..1998) can't tell, so no contradiction", dcmp(P("..1998"), P("1997..1998")), None)
_acc = accepted
accepted = lambda f: [a for a in _acc(f) if a[1] != "PS:1"]
check("D without its acceptance, PS:1 is outside PS", contradictions(PURIST), [("outside-parent", "PS:1")])
accepted = _acc
import tempfile, shutil
def scratch_layer(files):
    d = pathlib.Path(tempfile.mkdtemp()); (d/"characters").mkdir()
    for name, text in files.items(): (d/name).write_text(text)
    return d
HDR = "## State history\n| Attribute | Value | As of | Source | Citation | True from | In-world |\n| - | - | - | - | - | - | - |\n"
t = scratch_layer({"characters/time-traveller.md": HDR + "| born | 2051 | PS:7 | books | x | | |\n| died | 1990 | PS:7 | books | x | | |\n"})
check("D born-died: born 2051, died 1990", contradictions(PURIST, extra=[("x", t)]), [("born-died", "born")])
(t/"characters/time-traveller.md").write_text((t/"characters/time-traveller.md").read_text() + "\n## Accepted\n| Check | Subject | Reason | Citation |\n| - | - | - | - |\n| born-died | born | travels back from 2070 | x |\n")
check("D born-died accepted by the layer that holds the rows", contradictions(PURIST, extra=[("x", t)]), [])
u = scratch_layer({"characters/time-traveller.md": "## State history\n| Attribute | Value | As of | Source | Citation |\n| - | - | - | - | - |\n\n## Accepted\n| Check | Subject | Reason | Citation |\n| - | - | - | - |\n| outside-parent | PS:1 | not ours | x |\n"})
accepted = lambda f: [a for a in _acc(f) if a[1] != "PS:1"] + (_acc(f) if f.parent.parent == u else [])
check("D a layer cannot accept a contradiction it holds no part of", contradictions(PURIST, extra=[("y", u)]), [("outside-parent", "PS:1")])
accepted = _acc
v = scratch_layer({"characters/seer.md": HDR + "| fate | dies in the war | PS:7 | books | x | | 1999 |\n"})
check("D in-world-after: a fact dated after the point that shows it", contradictions(PURIST, extra=[("x", v)]), [("in-world-after", "fate")])
w = scratch_layer({"history.md": "## State history\n| Entity | Attribute | Value | As of | Source | Citation |\n| - | - | - | - | - | - |\n| omen | date | 2001 | PS:7 | books | x |\n"})
check("D in-world-after: an event dated after its as-of", contradictions(PURIST, extra=[("x", w)]), [("in-world-after", "omen.date")])
for x in (t, u, v, w): shutil.rmtree(x)
vals = {"outside-parent", "in-world-after", "born-died", "born-before-parent", "ancestry-cycle"}
for f in [pkg_dir("harry-potter")/"canon-timeline.md"]:
    check("D acceptances name a known check, a held subject, a reason, and a citation", all(
        c in vals and s in {r["Node"] for r in table(f, "## Dates")} and r["Reason"] and r["Citation"] for c, s, r in accepted(f)), True)

# universe offsets need the same calendar (§8.1)
def offsets_ok(universe):
    cals = [Package(b.split("@")[0]).cfg.get("calendar") for b in universe["relies-on"]]
    return not universe.get("offsets") or (cals[0] is not None and all(c == cals[0] for c in cals))
check("D the universe's offsets: both bases are iso", offsets_ok(u_ := load(EX/"universes/wizards-and-warp/universe.yaml")), True)
_cfg = Package.__init__
def no_trek_calendar(self, pid):
    _cfg(self, pid)
    if pid == "star-trek": self.cfg.pop("calendar", None)
Package.__init__ = no_trek_calendar
check("D offsets with a base that has no calendar are invalid", offsets_ok(u_), False)
Package.__init__ = _cfg
off = int(u_["offsets"]["harry-potter"][:-1])
check("D universe time: Harry's first journey to Hogwarts is in 2364", shift(point_date(PURIST, "PS:6"), off), P("2364-09-01"))
check("D universe time: Grindelwald's defeat comes before TNG season 1", dcmp(shift(P("1945"), off), point_date(TREK, "TNG:1")), -1)

# --- travel (§9.4, §10.26) ------------------------------------------------------------
UNITS = {"min": 1, "h": 60, "d": 1440, "w": 10080}
def duration(s):
    """A duration (§9.4): (low minutes or None, high minutes or None, approximate)."""
    def one(x):
        if x == "0": return 0
        m = re.fullmatch(r"([1-9]\d*)(min|h|d|w)", x)
        if not m: raise ValueError(x)
        return int(m[1]) * UNITS[m[2]]
    if s.startswith("~"): v = one(s[1:]); return v, v, True
    if ".." in s:
        a, b = s.split("..", 1)
        if not a and not b: raise ValueError(s)
        lo, hi = (one(a) if a else None), (one(b) if b else None)
        if lo is not None and hi is not None and lo > hi: raise ValueError(s)
        return lo, hi, False
    v = one(s); return v, v, False

def day_number(cal, t):
    """Days since a fixed epoch, for a (year, month, day) in a calendar with months."""
    y, m, d = t
    if cal.iso:
        y -= m <= 2; era = (y if y >= 0 else y - 399) // 400; yoe = y - era * 400
        doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
        return era * 146097 + yoe * 365 + yoe // 4 - yoe // 100 + doy
    return y * sum(cal.months) + sum(cal.months[:m - 1]) + d

def routes(d):
    """(modes, places, edges): edges {(from, to): fastest lower bound in minutes}, both ways for `+` (§9.4)."""
    f = d/"routes.md"; modes = [r["Mode"] for r in table(f, "## Modes")]
    places = {r["Entity"] for r in table(d/"places.md", "## State history")}
    state = {}
    for r in table(f, "## State history"):
        if r["Value"] == "(unset)": state.pop((r["Route"], r["Attribute"]), None)
        else: state[(r["Route"], r["Attribute"])] = r["Value"]
    edges = {}
    for route in dict.fromkeys(k for k, _ in state):
        known = [state[(route, m)] for m in modes if (route, m) in state]
        lows = [0 if dur[2] or dur[0] is None else dur[0] for dur in map(duration, (v for v in known if v != "—"))]
        if known and not lows: continue                     # every known mode is impossible
        w = min(lows) if lows else 0                        # no known mode: instant
        a, b = re.split(r"[+>]", route)
        edges[(a, b)] = min(w, edges.get((a, b), w))
        if "+" in route: edges[(b, a)] = min(w, edges.get((b, a), w))
    return modes, places, edges

def shortest(edges, a, b):
    import heapq
    dist, todo = {a: 0}, [(0, a)]
    while todo:
        w, x = heapq.heappop(todo)
        if x == b: return w
        if w > dist[x]: continue
        for (p, q), e in edges.items():
            if p == x and w + e < dist.get(q, float("inf")): dist[q] = w + e; heapq.heappush(todo, (w + e, q))
    return None

def route_errors(d):
    """§9.4, §10.26: known places, alphabetical two-way routes, attributes that are modes or distance, valid values."""
    out = []; modes = [r["Mode"] for r in table(d/"routes.md", "## Modes")]
    places = {r["Entity"] for r in table(d/"places.md", "## State history")}
    if len(set(modes)) != len(modes): out.append("a mode defined twice")
    for r in table(d/"routes.md", "## State history"):
        route, att, v = r["Route"], r["Attribute"], r["Value"]
        parts = re.split(r"[+>]", route)
        if len(parts) != 2 or not set(parts) <= places: out.append(f"{route}: unknown place")
        elif "+" in route and parts != sorted(parts): out.append(f"{route}: not in alphabetical order")
        if att not in modes and att != "distance": out.append(f"{route}: unknown mode {att}")
        elif att in modes and v not in ("—", "(unset)") and raises_ok(lambda: duration(v), ValueError): out.append(f"{route}: bad duration {v}")
    return out

def travel_warnings(events, edges, cal):
    """Journeys definitely faster than the routes allow (§9.4): (entity, from chapter, to chapter)."""
    out, by = [], {}
    for e in events:
        if not (e.get("Date") and e.get("Place")): continue
        for who in e["Entities"].split("; "): by.setdefault(who, []).append(e)
    for who, evs in by.items():
        evs = sorted(evs, key=lambda e: dkey(cal.parse(e["Date"])))
        for a, b in zip(evs, evs[1:]):
            if a["Place"] == b["Place"]: continue
            da, db = cal.parse(a["Date"]), cal.parse(b["Date"])
            if da[2] or db[2] or da[0] is None or db[1] is None: continue
            most = (day_number(cal, db[1]) - day_number(cal, da[0]) + 1) * 1440
            need = shortest(edges, a["Place"], b["Place"])
            if need is not None and most < need: out.append((who, a["Chapter"], b["Chapter"]))
    return out

LRD = EX/"projects/lantern-road/bible"
check("T durations", [duration(s) for s in ("3d", "4d..6d", "..12h", "~8h", "0", "30min", "2w")],
      [(4320, 4320, False), (5760, 8640, False), (None, 720, False), (480, 480, True), (0, 0, False), (30, 30, False), (20160, 20160, False)])
for s in ("3 days", "0d", "6d..4d", "..", "3", "~1d..2d"):
    raises(f"T duration {s!r} invalid", lambda: duration(s))
check("T lantern-road's routes are valid", route_errors(LRD), [])
modes, places, edges = routes(LRD)
check("T shortest journey: highcairn to lowmere by cart, 4 days", shortest(edges, "highcairn", "lowmere"), 4 * 1440)
check("T the route runs both ways", shortest(edges, "lowmere", "highcairn"), 4 * 1440)
check("T no route, no journey", shortest(edges, "highcairn", "nowhere"), None)
e2 = dict(edges); e2[("lowmere", "highcairn")] = 1440
check("T a one-way route: downstream only", (shortest(e2, "lowmere", "highcairn"), shortest(e2, "highcairn", "lowmere")), (1440, 4 * 1440))
tl = table(LRD/"timeline.md", "## Events")
check("T the timeline's places are in places.md", {e["Place"] for e in tl} <= places, True)
check("T the timeline's dates parse", all(not raises_ok(lambda: LRC.parse(e["Date"]), ValueError) for e in tl), True)
check("T no journey too fast in lantern-road", travel_warnings(tl, edges, LRC), [])
fast = {"Chapter": "chapter-02", "Story time": "", "Event": "x", "Entities": "ines-varga", "Date": "NR 30-01-12", "Place": "lowmere"}
check("T warns: highcairn to lowmere in at most 3 days", travel_warnings(tl + [fast], edges, LRC), [("ines-varga", "chapter-01", "chapter-02")])
check("T an approximate date never warns", travel_warnings(tl + [dict(fast, Date="~NR 30-01-12")], edges, LRC), [])
check("T an open-ended date never warns", travel_warnings(tl + [dict(fast, Date="..NR 30-01-12")], edges, LRC), [])
check("T days in an iso date: 1991-02-28 to 1991-03-01, and across 1992's leap day",
      (day_number(ISO, (1991, 3, 1)) - day_number(ISO, (1991, 2, 28)), day_number(ISO, (1992, 3, 1)) - day_number(ISO, (1992, 2, 28))), (1, 2))
def lr_routes(text, places_extra=""):
    d = scratch_layer({"routes.md": "## Modes\n| Mode | Name | Notes |\n| - | - | - |\n| foot | On foot | |\n| cart | By cart | |\n\n## State history\n| Route | Attribute | Value | As of | Source | Citation |\n| - | - | - | - | - | - |\n" + text,
                       "places.md": (LRD/"places.md").read_text() + places_extra})
    try: errs = route_errors(d); return errs, None if errs else routes(d)[2]
    finally: shutil.rmtree(d)
for label, row in [("not in alphabetical order", "| the-halfway-inn+highcairn | foot | 3d | | project | x |\n"),
                   ("an unknown place", "| highcairn+nowhere | foot | 3d | | project | x |\n"),
                   ("an unknown mode", "| highcairn+the-halfway-inn | boat | 3d | | project | x |\n"),
                   ("a bad duration", "| highcairn+the-halfway-inn | foot | three days | | project | x |\n")]:
    check(f"T route error: {label}", len(lr_routes(row)[0]), 1)
check("T a route that every known mode cannot make is not a path", lr_routes("| highcairn+the-halfway-inn | foot | — | | project | x |\n")[1], {})
check("T an approximate duration, or no known mode, counts as instant",
      (lr_routes("| highcairn+the-halfway-inn | foot | ~3d | | project | x |\n")[1][("highcairn", "the-halfway-inn")],
       lr_routes("| highcairn+the-halfway-inn | distance | far | | project | x |\n")[1][("highcairn", "the-halfway-inn")]), (0, 0))
check("T a closed mode is left out", lr_routes("| highcairn+the-halfway-inn | foot | 3d | | project | x |\n| highcairn+the-halfway-inn | cart | 2d | | project | x |\n| highcairn+the-halfway-inn | cart | (unset) | | project | x |\n")[1][("highcairn", "the-halfway-inn")], 3 * 1440)

# --- mysteries (§9.5, §10.27) ---------------------------------------------------------
def mystery_layers(dirs):
    """[(label, secrets, mysteries, clues)] for each bible directory, in stack order."""
    out = []
    for label, d in dirs:
        k, m = d/"knowledge.md", d/"mysteries.md"
        out.append((label, {r["Secret"] for r in table(k, "## Secrets")} if has(k, "## Secrets") else set(),
                    table(m, "## Mysteries") if has(m, "## Mysteries") else [], table(m, "## Clues") if has(m, "## Clues") else []))
    return out

def mystery_errors(layers, point_ok):
    out, secrets, owner, clues = [], set(), {}, {}
    for label, sec, mys, cls in layers:
        secrets |= sec
        for r in mys:
            if r["Mystery"] not in secrets: out.append(f"{r['Mystery']}: not a secret")
            if r["Mystery"] in owner: out.append(f"{r['Mystery']}: defined twice")
            if not point_ok(r["Revealed at"]): out.append(f"{r['Mystery']}: bad Revealed at")
            owner.setdefault(r["Mystery"], label)
        for r in cls:
            key = (r["Mystery"], r["Clue"])
            if r["Mystery"] not in owner: out.append(f"{key}: unknown mystery")
            if r["Kind"] not in ("clue", "red-herring"): out.append(f"{key}: unknown kind")
            if r["Needed"] not in ("yes", "no") or (r["Kind"] == "red-herring" and r["Needed"] == "yes"): out.append(f"{key}: bad Needed")
            if not point_ok(r["Planted at"]): out.append(f"{key}: bad Planted at")
            if key in clues: out.append(f"{key}: " + ("duplicate" if clues[key] == label else f"redefines {clues[key]}'s clue"))
            clues.setdefault(key, label)
    return out

def fair_play(layers, cmp):
    """Unfair mysteries (§9.5): a needed clue at or after the reveal, or no needed clue before it."""
    reveal = {r["Mystery"]: r["Revealed at"] for *_, mys, _ in layers for r in mys}
    clues = [r for *_, cls in layers for r in cls]
    out = [("late clue", r["Mystery"], r["Clue"]) for r in clues if r["Needed"] == "yes" and cmp(r["Planted at"], reveal[r["Mystery"]]) >= 0]
    out += [("no needed clue", m, "") for m, at in reveal.items()
            if not any(r["Mystery"] == m and r["Needed"] == "yes" and cmp(r["Planted at"], at) < 0 for r in clues)]
    return out

chapter_ok = lambda c: re.fullmatch(r"chapter-\d{2,}", c) is not None
chapter_cmp = lambda a, b: (chap(a) > chap(b)) - (chap(a) < chap(b))
HPM = mystery_layers([("harry-potter", pkg_dir("harry-potter"))])
LRM = mystery_layers([("lantern-road", LRD)])
check("M Harry Potter's mysteries are valid", mystery_errors(HPM, lambda p: isvalid(HP, p)), [])
check("M lantern-road's mysteries are valid", mystery_errors(LRM, chapter_ok), [])
check("M the moody mystery is fair: two needed clues before GoF:35", fair_play(HPM, HP.cmp), [])
check("M lantern-road's mystery is fair", fair_play(LRM, chapter_cmp), [])
check("M the answer is the secret, hidden from Harry until the reveal",
      (g(PURIST, "harry-potter", "GoF:34", "moody-identity"), g(PURIST, "harry-potter", "GoF:35", "moody-identity")), ("unaware", "knows"))
def mutate(layers, i, which, row_i, **kw):
    out = copy.deepcopy(layers); rows = out[i][2 if which == "m" else 3]; rows[row_i] = dict(rows[row_i], **kw); return out
for label, bad, want in [
        ("a mystery that is not a secret", mutate(HPM, 0, "m", 0, Mystery="who-is-it"), 1),
        ("a red herring marked needed", mutate(HPM, 0, "c", 2, Needed="yes"), 1),
        ("an unknown kind", mutate(HPM, 0, "c", 0, Kind="hint"), 1),
        ("a duplicate clue", mutate(HPM, 0, "c", 1, Clue="c1"), 1),
        ("an invalid Planted at", mutate(HPM, 0, "c", 0, **{"Planted at": "GoF:38"}), 1)]:
    check(f"M error: {label}", len(mystery_errors(bad, lambda p: isvalid(HP, p))) >= want, True)
higher = copy.deepcopy(HPM) + [("fanfic", set(), [], [dict(HPM[0][3][0], **{"Planted at": "GoF:36"}), dict(HPM[0][3][0], Clue="c4", **{"Planted at": "GoF:20"})])]
check("M a higher layer may add a clue, never redefine one", mystery_errors(higher, lambda p: isvalid(HP, p)), ["('moody-identity', 'c1'): redefines harry-potter's clue"])
late = mutate(HPM, 0, "c", 1, **{"Planted at": "GoF:36"})
check("M unfair: a needed clue after the reveal", fair_play(late, HP.cmp), [("late clue", "moody-identity", "c2")])
none = mutate(mutate(HPM, 0, "c", 0, Needed="no"), 0, "c", 1, Needed="no")
check("M unfair: no needed clue before the reveal", fair_play(none, HP.cmp), [("no needed clue", "moody-identity", "")])
heir = [("x", {"chamber-heir"}, [{"Mystery": "chamber-heir", "Question": "q", "Revealed at": "GoF:30", "Notes": ""}],
         [{"Mystery": "chamber-heir", "Clue": "c1", "Kind": "clue", "Points to": "p", "Planted at": "CoS:10", "Needed": "yes", "Citation": "x"},
          {"Mystery": "chamber-heir", "Clue": "c2", "Kind": "clue", "Points to": "p", "Planted at": "GoF:20", "Needed": "yes", "Citation": "x"}])]
SYT = Stack.of("second-year-tournament")
check("M fair in the ruler's order", fair_play(heir, HP.cmp), [])
check("M the order audit: moving GoF before CoS puts a needed clue after its reveal", fair_play(heir, SYT.ruler().cmp), [("late clue", "chamber-heir", "c1")])

# --- lineage (§9.6, §10.28) -----------------------------------------------------------
LINEAGE = ("parents", "guardians", "descends-from")
def lineage_values(d):
    """Every slug that a lineage attribute or a title's holder names in one bible directory."""
    out = set()
    for f, key, rows in state_tables(d):
        for r in rows:
            if (r["Attribute"] in LINEAGE or (f.name == "titles.md" and r["Attribute"] == "holder")) and r["Value"] != "(unset)":
                out |= set(r["Value"].split("; "))
    return out
def family_tree(stack, entity, cutoff, seen=()):
    """The family-tree view (§9.6): an entity's parents and named ancestors, as the reader knows them at the cutoff."""
    s = snapshot(stack, entity, cutoff)
    up = [p for a in ("parents", "descends-from") for p in s.get(a, "").split("; ") if p]
    return (entity, [family_tree(stack, p, cutoff, seen + (entity,)) for p in up if p not in seen + (entity,)])
def lineage_warnings(people, titles, cal):
    """§9.6 warnings. people: {slug: resolved state}; titles: [(title, holder, date of its As of)]."""
    out = []; P_ = lambda s: cal.parse(s)
    for child, s in people.items():
        if "born" not in s: continue
        cb = P_(s["born"])
        for p in s.get("parents", "").split("; "):
            ps = people.get(p, {})
            if "born" in ps and age(P_(ps["born"]), cb)[1] < 12: out.append(("young parent", child, p))
            if "died" in ps and dcmp(cb, shift(P_(ps["died"]), 1)) == 1: out.append(("born after death", child, p))
    for title, holder, when in titles:
        h = people.get(holder, {})
        if when and (("born" in h and dcmp(when, P_(h["born"])) == -1) or ("died" in h and dcmp(when, P_(h["died"])) == 1)):
            out.append(("holder outside lifetime", title, holder))
    return out

HPR = {r["Slug"] for r in Package("harry-potter").roster()}
check("L every lineage value and title holder is in the roster", lineage_values(pkg_dir("harry-potter")) <= HPR, True)
check("L Harry's parents and guardians at PS:2", (g(PURIST, "harry-potter", "PS:2", "parents"), g(PURIST, "harry-potter", "PS:2", "guardians")),
      ("james-potter; lily-potter", "petunia-dursley; vernon-dursley"))
check("L Harry has no guardians once he comes of age (DH:7)", g(PURIST, "harry-potter", "DH:7", "guardians"), None)
check("L family tree: Voldemort's parentage is unknown at GoF:37", family_tree(PURIST, "lord-voldemort", "GoF:37"), ("lord-voldemort", []))
check("L family tree: from HBP:10, back to Slytherin", family_tree(PURIST, "lord-voldemort", "HBP:10"),
      ("lord-voldemort", [("merope-gaunt", [("marvolo-gaunt", [("salazar-slytherin", [])])]), ("tom-riddle-sr", [])]))
check("L family tree: Harry at PS:1", family_tree(PURIST, "harry-potter", "PS:1"), ("harry-potter", [("james-potter", []), ("lily-potter", [])]))
for c, want in [("PS:5", "albus-dumbledore"), ("OotP:30", "dolores-umbridge"), ("OotP:38", "albus-dumbledore"), ("DH:36", "severus-snape")]:
    check(f"L the headship of Hogwarts at {c}", g(PURIST, "headmaster-of-hogwarts", c, "holder"), want)
people = {s: snapshot(PURIST, s, "DH:36") for s in HPR}
trows = [(r["Entity"], r["Value"], point_date(PURIST, r["As of"])) for r in table(pkg_dir("harry-potter")/"titles.md", "## State history") if r["Attribute"] == "holder"]
check("L no lineage warnings in Harry Potter", lineage_warnings(people, trows, ISO), [])
check("L Harry was born 1 to 2 years before his parents died", age(P(people["harry-potter"]["born"]), P(people["james-potter"]["died"])), (1, 1))
check("L warning: a parent under 12", lineage_warnings({"a": {"born": "1990", "parents": "b"}, "b": {"born": "1980"}}, [], ISO), [("young parent", "a", "b")])
check("L warning: born more than a year after a parent died", lineage_warnings({"a": {"born": "1983", "parents": "b"}, "b": {"born": "1950", "died": "1981-10-31"}}, [], ISO), [("born after death", "a", "b")])
check("L no warning: born months after a father's death", lineage_warnings({"a": {"born": "1982-03", "parents": "b"}, "b": {"born": "1950", "died": "1981-10-31"}}, [], ISO), [])
check("L warning: a title held before its holder's birth", lineage_warnings({"h": {"born": "1990"}}, [("t", "h", P("1985"))], ISO), [("holder outside lifetime", "t", "h")])
CH = "## State history\n| Attribute | Value | As of | Source | Citation |\n| - | - | - | - | - |\n"
t = scratch_layer({"characters/ann.md": CH + "| born | 2051 | PS:7 | books | x |\n| parents | bob | PS:7 | books | x |\n",
                   "characters/bob.md": CH + "| born | 2070 | PS:7 | books | x |\n| parents | ann | PS:7 | books | x |\n"})
check("L born-before-parent and ancestry-cycle: her own grandparent", contradictions(PURIST, extra=[("x", t)]),
      [("ancestry-cycle", "parents"), ("born-before-parent", "born")])
(t/"characters/ann.md").write_text((t/"characters/ann.md").read_text() + "\n## Accepted\n| Check | Subject | Reason | Citation |\n| - | - | - | - |\n| born-before-parent | born | she travels back | x |\n| ancestry-cycle | parents | she travels back | x |\n")
check("L both accepted, one acceptance excusing the cycle", contradictions(PURIST, extra=[("x", t)]), [])
shutil.rmtree(t)
t = scratch_layer({"characters/ann.md": CH + "| descends-from | ann | PS:7 | books | x |\n"})
check("L ancestry-cycle needs no dates: descended from herself", contradictions(PURIST, extra=[("x", t)]), [("ancestry-cycle", "descends-from")])
shutil.rmtree(t)
check("L no lineage contradictions in the examples", contradictions(PURIST), [])

# schemas: the modules a project enables
check("L schema: lantern-road enables travel and mysteries", (pyaml("lantern-road")["modules"], schema("project").is_valid(pyaml("lantern-road"))), ({"travel": True, "mysteries": True}, True))
d = pyaml("two-witnesses"); d["modules"]["romance"] = True; check("L schema: an unknown module rejected", schema("project").is_valid(d), False)
d = pyaml("two-witnesses"); d["modules"]["lineage"] = "yes"; check("L schema: a module flag is a boolean", schema("project").is_valid(d), False)

# --- image prompts (§10.29, §12.20) ----------------------------------------------------
KINDS = {"character", "family-portrait", "family-tree", "map", "location"}
def names_of(stack):
    """{slug: display name} across the stack's rosters."""
    out = {r["Slug"]: r["Name"] for _, p in stack.packages for r in p.roster()}
    for proj, _ in stack.ledgers() + ([(stack.project, None)] if stack.project else []):
        f = EX/"projects"/proj/"bible/characters/_roster.md"
        if f.exists(): out.update({r["Slug"]: r["Name"] for r in table(f, "## Characters")})
    return out
def prompt_errors(project, f):
    fm, text, stack = front(f), f.read_text(), Stack.of(project)
    lines = text.splitlines(); out = []
    if fm.get("kind") not in KINDS: out.append("kind")
    if not ("## Gaps" in lines and "## Sources" in lines): out.append("sections")
    if fm.get("cutoff") and not isvalid(stack.ruler(), fm["cutoff"]): out.append("cutoff")
    if fm.get("position") and not chapter_ok(fm["position"]): out.append("position")
    places = {r["Entity"] for r in table(EX/"projects"/project/"bible/places.md", "## State history")} if (EX/"projects"/project/"bible/places.md").exists() else set()
    pool = places if fm.get("kind") in ("map", "location") else set(names_of(stack))
    if not set(fm.get("subjects", [])) <= pool: out.append("subjects")
    return out
PROMPTS = [(p.parent.parent.name, p) for p in sorted((EX/"projects").glob("*/prompts/*.md"))]
check("P the examples have prompts", [f"{a}/{p.name}" for a, p in PROMPTS], ["lantern-road/road-map.md", "two-witnesses/potter-family-tree.md"])
for proj, f in PROMPTS:
    check(f"P prompt valid: {proj}/{f.name}", prompt_errors(proj, f), [])
TW = Stack.of("two-witnesses"); NAMES = names_of(TW)
def members(t): return [t[0]] + [m for c in t[1] for m in members(c)]
tree = members(family_tree(TW, "harry-potter", "GoF:37"))
body = (EX/"projects/two-witnesses/prompts/potter-family-tree.md").read_text().split("## Gaps")[0]
check("P the family tree at GoF:37: Harry and his parents", sorted(tree), ["harry-potter", "james-potter", "lily-potter"])
check("P the tree prompt names exactly the tree, and no one else in the roster",
      sorted(s for s, n in NAMES.items() if n in body), sorted(tree))
check("P the tree prompt gives no date the snapshot lacks", ("1960" in body, "1981" in body, "1980" in body), (False, False, True))
bad = EX/"projects/two-witnesses/prompts/potter-family-tree.md"
_front = front
for label, change, want in [("an unknown kind", {"kind": "poster"}, ["kind"]), ("a cutoff off the ruler", {"cutoff": "GoF:38"}, ["cutoff"]),
                            ("a subject not in the roster", {"subjects": ["harry-potter", "neville-longbottom"]}, ["subjects"])]:
    front = lambda p, c=change: dict(_front(p), **c)
    check(f"P prompt error: {label}", prompt_errors("two-witnesses", bad), want)
front = _front

# --- viewpoints (§7.7, §10.23, §10.18) -----------------------------------------------
MODES = ("none", "chapter", "scene")
def chapter_plan(project):
    """{chapter: (mode, [(scene, viewpoint, told from)])} from the outline, overrides applied (§10.23)."""
    params = pyaml(project).get("parameters", {}); default = params.get("viewpoints", "none")
    out = {}
    for r in table(EX/"projects"/project/"bible/outline.md", "## Chapters"):
        c = r["Chapter"]
        if c not in out: out[c] = [r.get("Viewpoints") or default, []]
        elif r.get("Viewpoints"): raise ValueError(f"{c}: Viewpoints off its first row")
        out[c][1].append((r.get("Scene", ""), r.get("Viewpoint", ""), r.get("Told from", "")))
    return {c: tuple(v) for c, v in out.items()}
def outline_errors(project, plan=None, roster=None):
    params = pyaml(project).get("parameters", {}); out = []
    try: plan = plan or chapter_plan(project)
    except ValueError as e: return [str(e)]
    roster = roster or {r["Slug"] for r in table(EX/"projects"/project/"bible/characters/_roster.md", "## Characters")}
    told_ok = lambda c, t: t == "end" or (chapter_ok(t) and chap(t) >= chap(c))
    if params.get("told_from") and params["told_from"] != "end" and not chapter_ok(params["told_from"]): out.append("parameters.told_from")
    for c, (mode, rows) in plan.items():
        if mode not in MODES: out.append(f"{c}: unknown mode {mode}"); continue
        if mode == "chapter" and (len(rows) != 1 or rows[0][1] in ("", "—") or rows[0][0]): out.append(f"{c}: chapter mode needs one row and one viewpoint")
        if mode == "scene" and ([s for s, _, _ in rows] != [str(i) for i in range(1, len(rows) + 1)] or any(v == "" for _, v, _ in rows)): out.append(f"{c}: scenes")
        if mode == "none" and any(v for _, v, _ in rows): out.append(f"{c}: a viewpoint in a none chapter")
        for _, v, t in rows:
            if v not in ("", "—") and v not in roster: out.append(f"{c}: {v} not in the roster")
            if t and t != "—" and (v in ("", "—") or not told_ok(c, t)): out.append(f"{c}: bad Told from {t}")
    return out
def knowledge_point(project, chapter, told):
    """The chapter whose knowledge a viewpoint narrates with (§7.7); None for the end."""
    told = told or pyaml(project).get("parameters", {}).get("told_from") or "—"
    return chapter if told == "—" else None if told == "end" else told
def knows(project, who, point):
    """The secrets a character knows at a knowledge point, from the project's knowledge.md (§7.3, §4.11)."""
    rows = table(EX/"projects"/project/"bible/knowledge.md", "## Knowledge")
    return sorted(r["Secret"] for r in rows if r["Character"] == who and r["State"] == "knows"
                  and (not r.get("From chapter") or point is None or chap(r["From chapter"]) <= chap(point)))
def may_tell(project, chapter, who, told=""):
    """What the narration may state: the viewpoint's knowledge, less the mysteries not yet revealed (§7.7, §9.5)."""
    unrevealed = {r["Mystery"] for r in table(EX/"projects"/project/"bible/mysteries.md", "## Mysteries") if chapter_cmp(chapter, r["Revealed at"]) < 0}
    return [s for s in knows(project, who, knowledge_point(project, chapter, told)) if s not in unrevealed]
def drafted_viewpoints(text, default):
    """(mode, [(viewpoint, told from)]) recorded in a chapter: its front matter, or its scene markers (§10.18)."""
    fm = yaml.safe_load(text.split("---")[1]); mode = fm.get("viewpoints", default)
    if mode != "scene": return mode, [(fm.get("viewpoint", ""), fm.get("told-from", ""))] if mode == "chapter" else []
    marks = [dict(kv.split("=", 1) for kv in m.split()) for m in re.findall(r"<!-- scene: (.*?) -->", text)]
    return mode, [(m.get("viewpoint", ""), m.get("told-from", "")) for m in marks]
def viewpoint_warnings(project, chapter, text):
    default = pyaml(project).get("parameters", {}).get("viewpoints", "none")
    mode, rows = chapter_plan(project)[chapter]
    planned = (mode, [(v, t) for _, v, t in rows] if mode != "none" else [])
    return [] if drafted_viewpoints(text, default) == planned else [chapter]

LRP = chapter_plan("lantern-road")
check("V the project's mode, and the outline's overrides", {c: m for c, (m, _) in LRP.items()},
      {"chapter-01": "chapter", "chapter-02": "none", "chapter-03": "chapter", "chapter-05": "chapter", "chapter-06": "scene", "chapter-07": "chapter", "chapter-11": "chapter"})
check("V chapter 6: two scenes, two viewpoints", [v for _, v, _ in LRP["chapter-06"][1]], ["ines-varga", "tomas-hale"])
check("V lantern-road's outline is valid", outline_errors("lantern-road"), [])
check("V the knowledge point: told from the end, in the moment, or the project default",
      (knowledge_point("lantern-road", "chapter-03", ""), knowledge_point("lantern-road", "chapter-03", "—"), knowledge_point("lantern-road", "chapter-03", "chapter-07")), (None, "chapter-03", "chapter-07"))
check("V told from the end, Ines knows the answer in chapter 3", knows("lantern-road", "ines-varga", knowledge_point("lantern-road", "chapter-03", "")), ["lamps-going-out"])
check("V in the moment, she does not", knows("lantern-road", "ines-varga", knowledge_point("lantern-road", "chapter-03", "—")), [])
check("V told from chapter 7, still not: she learns it in chapter 11", knows("lantern-road", "ines-varga", "chapter-07"), [])
check("V told from never moves a reveal: chapter 3 may not tell it", may_tell("lantern-road", "chapter-03", "ines-varga"), [])
check("V chapter 11 may", may_tell("lantern-road", "chapter-11", "ines-varga"), ["lamps-going-out"])
check("V the innkeeper knows all along, and his scene may not tell it", (knows("lantern-road", "tomas-hale", "chapter-06"), may_tell("lantern-road", "chapter-06", "tomas-hale", "—")), (["lamps-going-out"], []))
def bad_plan(**changes):
    p = dict(LRP)
    for c, v in changes.items(): p[c] = v
    return outline_errors("lantern-road", plan=p)
for label, plan, want in [
        ("an unknown mode", {"chapter-02": ("all", [])}, 1),
        ("a chapter-mode chapter with no viewpoint", {"chapter-03": ("chapter", [("", "", "")])}, 1),
        ("a chapter-mode chapter with two rows", {"chapter-03": ("chapter", [("", "ines-varga", ""), ("", "ines-varga", "")])}, 1),
        ("a scene without a viewpoint", {"chapter-06": ("scene", [("1", "ines-varga", ""), ("2", "", "")])}, 1),
        ("scenes not numbered from 1", {"chapter-06": ("scene", [("2", "ines-varga", ""), ("3", "tomas-hale", "—")])}, 1),
        ("a viewpoint in a none chapter", {"chapter-02": ("none", [("", "ines-varga", "")])}, 1),
        ("a viewpoint not in the roster", {"chapter-03": ("chapter", [("", "harry-potter", "")])}, 1),
        ("told from an earlier chapter", {"chapter-05": ("chapter", [("", "ines-varga", "chapter-03")])}, 1),
        ("told from where no one narrates", {"chapter-06": ("scene", [("1", "ines-varga", ""), ("2", "—", "end")])}, 1)]:
    check(f"V outline error: {label}", len(bad_plan(**plan)), want)
check("V a scene with no viewpoint character (—) is valid", bad_plan(**{"chapter-06": ("scene", [("1", "ines-varga", ""), ("2", "—", "")])}), [])
d = pyaml("lantern-road")
for k, v, ok in [("viewpoints", "scene", True), ("viewpoints", "all", False), ("told_from", "chapter-12", True), ("told_from", "later", False)]:
    d2 = copy.deepcopy(d); d2["parameters"][k] = v; check(f"V schema: {k} {v!r}", schema("project").is_valid(d2), ok)
DRAFT6 = "---\nchapter: 6\nstatus: drafted\nviewpoints: scene\n---\n<!-- scene: viewpoint=ines-varga -->\n...\n<!-- scene: viewpoint=tomas-hale told-from=— -->\n...\n"
check("V chapter 6 as drafted matches its outline", viewpoint_warnings("lantern-road", "chapter-06", DRAFT6), [])
check("V a drafted viewpoint that differs from the outline warns", viewpoint_warnings("lantern-road", "chapter-06", DRAFT6.replace("viewpoint=tomas-hale", "viewpoint=ines-varga")), ["chapter-06"])
check("V chapter 2 drafted with no viewpoint matches", viewpoint_warnings("lantern-road", "chapter-02", "---\nchapter: 2\nstatus: drafted\nviewpoints: none\n---\n"), [])
check("V a frames marker carries the viewpoint too", drafted_viewpoints("---\nchapter: 1\nviewpoints: scene\n---\n<!-- scene: at=PoA:21@main travelers=harry-potter viewpoint=harry-potter -->\n", "none"), ("scene", [("harry-potter", "")]))

# --- serial buffer and early access (§13.3, §13.9, §10.18) ---------------------------
STATUS = ["drafted", "line-edited", "final", "early-access", "released"]
chs = sorted((front(p) for p in (TLB/"manuscript").glob("chapter-*.md")), key=lambda d: d["chapter"])
st = [c["status"] for c in chs]
check("S chapter statuses valid", all(s in STATUS for s in st), True)
check("S serial has no final status", "final" in st, False)
rank = lambda s: 2 if s == "released" else 1 if s == "early-access" else 0
check("S released, then early access, each an unbroken run from chapter 1", all(rank(a) >= rank(b) for a, b in zip(st, st[1:])), True)
check("S every released chapter has a release date", all(("released" in c) == (c["status"] == "released") for c in chs), True)
check("S every early-access chapter has its date", all(("early-access" in c) for c in chs if c["status"] in ("early-access",)), True)
check("S buffer depth (not yet released)", sum(s != "released" for s in st), 2)
check("S early-access depth", st.count("early-access"), 1)
def can_release(n): return st[n - 1] in ("line-edited", "early-access") and (n == 1 or st[n - 2] == "released")
def can_early(n): return st[n - 1] == "line-edited" and (n == 1 or st[n - 2] in ("early-access", "released"))
check("S may release chapter 3 (next in order)", can_release(3), True)
check("S may not release chapter 4 before 3", can_release(4), False)
check("S may not send chapter 4 to early access (still drafted)", can_early(4), False)
st4 = st[:]; st4[3] = "line-edited"; st, keep = st4, st
check("S line-edited chapter 4 may go to early access after 3", can_early(4), True); st = keep
rev = table(TLB/"revisions.md", "## Revisions")
check("S revision audiences valid", all(r["Audience"] in {"early-access", "public"} for r in rev), True)
check("S early-access revisions are for early-access or released chapters", all(st[chap(r["Chapter"]) - 1] in ("early-access", "released") for r in rev if r["Audience"] == "early-access"), True)
check("S every revision has a reader note", all(r["Reader note"] for r in rev), True)
fb = sorted((TLB/"references/feedback").glob("chapter-*/*.md"))
check("S feedback filed per chapter and reader", [(p.parent.name, p.stem) for p in fb], [("chapter-03", "reader-a")])
check("S feedback only on chapters readers have", all(st[chap(p.parent.name) - 1] in ("early-access", "released") for p in fb), True)
# --- licenses, authors, and content notes (§2.10, §11.13, §13.11) ---------------------
SPDX_ID = re.compile(r"^(LicenseRef-)?[A-Za-z0-9][A-Za-z0-9.\-+]*$")
def spdx_ok(expr):
    """A small SPDX expression parser: ids joined by AND, OR, and WITH, with brackets (§2.10)."""
    toks = re.findall(r"\(|\)|[^\s()]+", expr or ""); pos = 0
    def term():
        nonlocal pos
        if pos < len(toks) and toks[pos] == "(":
            pos += 1
            if not compound() or pos >= len(toks) or toks[pos] != ")": return False
            pos += 1; return True
        if pos < len(toks) and SPDX_ID.match(toks[pos]) and toks[pos] not in ("AND", "OR", "WITH"):
            pos += 1
            if pos < len(toks) and toks[pos] == "WITH":
                pos += 1
                if pos >= len(toks) or not SPDX_ID.match(toks[pos]): return False
                pos += 1
            return True
        return False
    def compound():
        nonlocal pos
        if not term(): return False
        while pos < len(toks) and toks[pos] in ("AND", "OR"):
            pos += 1
            if not term(): return False
        return True
    return bool(toks) and compound() and pos == len(toks)
def license_errors(manifest):
    doc = load(manifest); lic = doc.get("license")
    if lic is None: return []
    if not spdx_ok(lic): return ["license"]
    if "LicenseRef-" in lic and not (manifest.parent/"LICENSE.md").exists(): return ["LICENSE.md"]
    return []
HPW = EX/"worlds/harry-potter"
check("U fanon is CC-BY-4.0, with a credit", (load(HPW/"fanon/package.yaml").get("license"), bool(load(HPW/"fanon/package.yaml").get("credit"))), ("CC-BY-4.0", True))
check("U the base states no license", "license" in load(HPW/"base/package.yaml"), False)
check("U every manifest's license is valid", [str(p.relative_to(EX)) for p in EX.rglob("*.yaml") if p.name in ("package.yaml", "universe.yaml") and license_errors(p)], [])
check("U the fan work's own terms have their LICENSE.md", load(HPW/"fanfic/example/package.yaml")["license"].startswith("LicenseRef-") and (HPW/"fanfic/example/LICENSE.md").exists(), True)
for expr, ok in [("CC-BY-4.0", True), ("CC-BY-SA-4.0 OR MIT", True), ("(MIT AND CC0-1.0) OR Apache-2.0", True), ("GPL-2.0-or-later WITH Classpath-exception-2.0", True),
                 ("LicenseRef-fan-author-terms", True), ("MIT OR", False), ("(MIT", False), ("free to use", False), ("", False), ("AND MIT", False)]:
    check(f"U SPDX {expr!r}", spdx_ok(expr), ok)
for name, path in [("package", HPW/"fanon/package.yaml"), ("universe", EX/"universes/wizards-and-warp/universe.yaml")]:
    d = load(path); d["license"] = "MIT"; d["credit"] = "x"
    check(f"U schema: {name} takes license and credit", schema(name).is_valid(d), True)
    d["credit"] = ""; check(f"U schema: {name} credit may not be empty", schema(name).is_valid(d), False)

TLBY = pyaml("the-long-way-back")
AUTHORS = [a["id"] for a in TLBY.get("authors", [])]
check("U the-long-way-back has two authors", AUTHORS, ["ade", "kit"])
for label, change, ok in [("an author with no name", lambda d: d["authors"].append({"id": "sam"}), False),
                          ("an author id that is not an id", lambda d: d["authors"].append({"id": "Sam W", "name": "Sam"}), False),
                          ("an empty authors list", lambda d: d.__setitem__("authors", []), False),
                          ("a content note id that is not an id", lambda d: d["content_notes"].__setitem__("Self Harm", "x"), False),
                          ("an empty content note", lambda d: d["content_notes"].__setitem__("peril", ""), False),
                          ("an empty content_notes map", lambda d: d.__setitem__("content_notes", {}), False),
                          ("a third author", lambda d: d["authors"].append({"id": "sam", "name": "Sam"}), True)]:
    d = copy.deepcopy(TLBY); change(d); check(f"U schema: {label}", schema("project").is_valid(d), ok)

BY_REQUIRED = ("## Hidden canon", "## Theory conflicts", "## Seam conflicts")
def author_errors(project_yaml, chapters, ledgers):
    """§11.13: unique ids; By and -by values are authors; with two or more, required where §10.8, §10.5, §10.18 say."""
    ids = [a["id"] for a in project_yaml.get("authors", [])]; many = len(ids) >= 2; out = []
    if len(set(ids)) != len(ids): out.append("duplicate author")
    ok = lambda v: v in ids
    for c in chapters:
        for step in ("early-access", "released"):
            by = c.get(f"{step}-by")
            if by is not None and not ok(by): out.append(f"chapter {c['chapter']}: {step}-by {by}")
            if many and step in c and by is None: out.append(f"chapter {c['chapter']}: no {step}-by")
    for heading, rows in ledgers.items():
        for r in rows:
            by = r.get("By", "")
            if by and not ok(by): out.append(f"{heading}: By {by}")
            need = heading in BY_REQUIRED or heading == "## Accepted" or (heading == "## Consequences" and r.get("Status") == "accepted")
            if many and need and not by: out.append(f"{heading}: no By")
    return out
TLB_LEDGERS = {h: table(TLB/"bible/divergences.md", h) for h in ("## Divergences", "## Consequences")}
check("U the-long-way-back's authors are valid", author_errors(TLBY, chs, TLB_LEDGERS), [])
check("U each release and early access names its author", [(c["chapter"], c.get("released-by") or c.get("early-access-by")) for c in chs if c["status"] != "drafted"], [(1, "ade"), (2, "kit"), (3, "kit")])
HID = {"## Hidden canon": [{"Entity": "x", "Decision": "keep-hidden", "By": ""}]}
ACC = {"## Consequences": [{"Status": "accepted", "Note": "n", "By": ""}, {"Status": "open", "By": ""}]}
for label, y, c, led, want in [
        ("a duplicate author id", {"authors": [{"id": "ade"}, {"id": "ade"}]}, [], {}, 1),
        ("a release by someone not listed", TLBY, [{"chapter": 1, "released": "d", "released-by": "sam"}], {}, 1),
        ("a release that names no author, with two", TLBY, [{"chapter": 1, "released": "d"}], {}, 1),
        ("the same, with one author", {"authors": [{"id": "ade"}]}, [{"chapter": 1, "released": "d"}], {}, 0),
        ("the same, with none listed", {}, [{"chapter": 1, "released": "d"}], {}, 0),
        ("a hidden-canon decision with no By, with two", TLBY, [], HID, 1),
        ("an accepted consequence with no By; an open one needs none", TLBY, [], ACC, 1),
        ("a project acceptance with no By, with two", TLBY, [], {"## Accepted": [{"Check": "born-died", "By": ""}]}, 1),
        ("a divergence By that is not an author", TLBY, [], {"## Divergences": [{"ID": "D1", "By": "sam"}]}, 1),
        ("a divergence with no By (SHOULD, not MUST)", TLBY, [], {"## Divergences": [{"ID": "D1", "By": ""}]}, 0)]:
    check(f"U author error: {label}", len(author_errors(y, c, led)), want)

def note_errors(project_yaml, chapters):
    """§13.11, §10.18."""
    notes = project_yaml.get("content_notes"); out = []
    for c in chapters:
        n = c["chapter"]
        if notes is None:
            if "content-notes" in c or "content-notes-suggested" in c: out.append(f"{n}: notes without content_notes")
            continue
        if any(x not in notes for x in c.get("content-notes") or []): out.append(f"{n}: unknown note")
        if any(x not in notes and not re.fullmatch(r"new:[a-z0-9]+(-[a-z0-9]+)*", x) for x in c.get("content-notes-suggested") or []): out.append(f"{n}: bad suggestion")
        if c["status"] in ("early-access", "released") and "content-notes" not in c: out.append(f"{n}: unconfirmed")
    return out
def note_warnings(project_yaml, chapters):
    notes = project_yaml.get("content_notes") or {}
    return [c["chapter"] for c in chapters if c["status"] in ("early-access", "released")
            and any(x in notes and x not in (c.get("content-notes") or []) for x in c.get("content-notes-suggested") or [])]
check("U the-long-way-back's content notes are valid", note_errors(TLBY, chs), [])
check("U the notes readers see", {c["chapter"]: c.get("content-notes") for c in chs}, {1: ["death"], 2: [], 3: ["grief"], 4: None})
check("U a new: suggestion the author did not keep raises nothing", note_warnings(TLBY, chs), [])
ch3 = next(c for c in chs if c["chapter"] == 3)
for label, chapter, y, want in [
        ("a confirmed note not on the list", dict(ch3, **{"content-notes": ["violence"]}), TLBY, 1),
        ("a suggestion neither listed nor new:", dict(ch3, **{"content-notes-suggested": ["violence"]}), TLBY, 1),
        ("an early-access chapter with no notes", {k: v for k, v in ch3.items() if k != "content-notes"}, TLBY, 1),
        ("a drafted chapter with no notes", {"chapter": 4, "status": "drafted"}, TLBY, 0),
        ("notes in a project without content_notes", ch3, {k: v for k, v in TLBY.items() if k != "content_notes"}, 1)]:
    check(f"U content-note error: {label}", len(note_errors(y, [chapter])), want)
check("U a revision's listed suggestion missing from the confirmed notes warns",
      note_warnings(TLBY, [dict(ch3, **{"content-notes-suggested": ["grief", "death"]})]), [3])
check("U the line-editor only suggests; the release skill confirms",
      [c["chapter"] for c in chs if "content-notes" in c and c["status"] not in ("early-access", "released")], [])
# --- releasing and exports (§13.12, §13.13, §10.18, §10.30) ---------------------------
SCHED = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?(Z|[+-]\d{2}:\d{2}))?$")
SERIAL_KEYS = ("released", "re-released", "withdrawn", "release-on")
def front_errors(chapters, workflow, locked=True):
    """§10.18: keys in their workflow, withdrawn only after a release, schedules well formed."""
    out = []
    for c in chapters:
        n = c["chapter"]
        if workflow != "serial" and (c["status"] in ("released", "withdrawn") or any(k in c for k in SERIAL_KEYS)): out.append(f"{n}: serial only")
        if c["status"] == "withdrawn" and "released" not in c: out.append(f"{n}: withdrawn, never released")
        if "re-released" in c and "released" not in c: out.append(f"{n}: re-released, never released")
        for k in ("release-on", "early-access-on"):
            if k in c and not SCHED.match(str(c[k])): out.append(f"{n}: {k}")
    st = [c["status"] for c in sorted(chapters, key=lambda c: c["chapter"])]
    rank = lambda s: 2 if s in ("released", "withdrawn") else 1 if s == "early-access" else 0
    if any(rank(a) < rank(b) for a, b in zip(st, st[1:])): out.append("out of order")
    return out
FROM = {"early access": ("line-edited",), "release": ("line-edited", "early-access")}
KEY = {"early access": "early-access", "release": "released", "re-release": "re-released", "withdraw": "withdrawn"}
def taken(step, c):
    return c["status"] in (("early-access", "released", "withdrawn") if step == "early access" else ("released", "withdrawn"))
def release(chapters, step, run, *, workflow="serial", locked=True, notes=False, pending=(), texts=None,
            date="2026-12-01", by=None, insist=False):
    """One release-skill step for a run of chapters (§13.12): (chapters after, None), or (None, the refusal)."""
    chs = {c["chapter"]: dict(c) for c in chapters}; texts = texts or {}
    for n in run:
        c = chs[n]
        if step != "early access" and workflow != "serial": return None, f"{n}: serial only"
        if step == "withdraw":
            if c["status"] != "released": return None, f"{n}: not released"
            continue
        if any(not taken(step, chs[m]) for m in chs if m < n and m not in run): return None, f"{n}: out of order"
        if n in pending or "<!-- TODO:" in texts.get(n, ""): return None, f"{n}: a pending decision or marker"
        if notes and "content-notes" not in c: return None, f"{n}: notes not confirmed"
        frm = (("withdrawn",) if locked else ("released", "withdrawn")) if step == "re-release" else FROM[step]
        if c["status"] not in frm and not (insist and step != "re-release" and c["status"] == "drafted"): return None, f"{n}: from {c['status']}"
    for n in run:
        c = chs[n]; c["status"] = {"early access": "early-access", "withdraw": "withdrawn"}.get(step, "released")
        c[KEY[step]] = date
        if by: c[KEY[step] + "-by"] = by
    return [chs[n] for n in sorted(chs)], None
def schedule_ok(chapters, step, n, when):
    """§13.12: every earlier chapter that has not taken the step is scheduled no later."""
    k = "release-on" if step == "release" else "early-access-on"
    return all(taken(step, c) or (k in c and str(c[k]) <= when) for c in chapters if c["chapter"] < n)
def run_schedules(chapters, now, **kw):
    """At `now`, take every scheduled step that is due, re-checking the refusals; a refused one is unscheduled (§13.12)."""
    chs = [dict(c) for c in chapters]; told = []
    for k, step in (("early-access-on", "early access"), ("release-on", "release")):
        for c in sorted(chs, key=lambda c: c["chapter"]):
            if k in c and str(c[k]) <= now:
                when = str(c.pop(k)); by = c.pop(k + "-by", None)
                after, why = release(chs, step, [c["chapter"]], date=when[:10], by=by, **kw)
                if why: told.append(why)
                else: chs = after
    return chs, told

def clean(text, title, n, brk="* * *"):
    """The chapter as readers get it (§10.30)."""
    body = text.split("---", 2)[2]
    marks = re.findall(r"<!-- scene:.*?-->", body)
    for i, m in enumerate(marks): body = body.replace(m, "" if i == 0 else f"\n{brk}\n", 1)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    lines = [l.rstrip() for l in body.split("\n")]
    out = []
    for l in lines:
        if l or (out and out[-1]): out.append(l)
    body = "\n".join(out).strip()
    head = f"# {title or f'Chapter {n}'}"
    return head + ("\n\n" + body if body else "") + "\n"
def words(md, brk="* * *"):
    return sum(len(l.split()) for l in md.split("\n")[1:] if l.strip() != brk)
def stack_layers(project):
    return [l.split("@")[0] for l in pyaml(project).get("layers") or [] if not l.startswith(("project:", "universe:"))]
def names_in(project):
    names, aliases = {}, {}
    for d in [pkg_dir(l) for l in stack_layers(project)] + [EX/"projects"/project/"bible"]:
        f = d/"characters/_roster.md"
        if f.exists():
            for r in table(f, "## Characters"):
                names[r["Slug"]] = r["Name"]
                if r.get("Reveal of"): aliases[r["Reveal of"]] = r["Revealed at"]
    return names, aliases
def sections(path):
    if not path.exists(): return {}
    out, cur = {}, None
    for l in path.read_text().split("\n"):
        if l.startswith("## "): cur = l[3:].strip(); out[cur] = []
        elif cur: out[cur].append(l)
    return {k: "\n".join(v).strip() for k, v in out.items() if "\n".join(v).strip()}
def shown_names(project, slugs, reached):
    """Roster names for slugs, leaving out a true identity whose reveal the audience has not reached (§13.13)."""
    names, aliases = names_in(project)
    return [names[s] for s in slugs if s in names and (s not in aliases or reached(aliases[s]))]
def export(project, chapters=None, texts=None, reached=lambda point: True, y=None):
    """{audience: {file name: text or dict}} as the export skill writes it (§13.13, §10.30)."""
    P = EX/"projects"/project; y = y or pyaml(project); pub = y.get("publishing"); brk = (pub or {}).get("scene_break", "* * *")
    files = sorted((P/"manuscript").glob("chapter-*.md"))
    chapters = chapters or [front(p) for p in files]
    texts = texts or {front(p)["chapter"]: p.read_text() for p in files}
    names, aliases = names_in(project)
    tl = table(P/"bible/timeline.md", "## Events") if (P/"bible/timeline.md").exists() else []
    rev = table(P/"revisions.md", "## Revisions") if (P/"revisions.md").exists() else []
    cn = y.get("content_notes") or {}
    uniq = lambda xs: list(dict.fromkeys(xs))
    out = {}
    for aud, statuses in (("public", ("released",)), ("early-access", ("early-access", "released"))):
        chs = sorted((c for c in chapters if c["status"] in statuses), key=lambda c: c["chapter"])
        if aud == "public" and y["workflow"] != "serial": continue
        folder, all_chars, all_notes = {}, [], []
        for c in chs:
            n = c["chapter"]; cid = f"chapter-{n:02d}"
            md = clean(texts[n], c.get("title"), n, brk); folder[f"{cid}.md"] = md
            chars = uniq(shown_names(project, [s for r in tl if r["Chapter"] == cid for s in r["Entities"].split("; ")], reached))
            notes = [cn[x] for x in c.get("content-notes") or []]
            all_chars += chars; all_notes += notes
            if pub is None: continue
            date = c.get("early-access") if aud == "early-access" and c.get("early-access") else c.get("re-released") or c.get("released")
            sec = sections(P/"references/chapter-notes"/f"{cid}.md")
            rows = [r for r in rev if r["Chapter"] == cid and r["Audience"] == ("public" if aud == "public" else "early-access")]
            meta = {"chapter": n, "title": c.get("title"), "audience": aud, "date": date, "words": words(md, brk),
                    "characters": chars, "content_notes": notes, "notes_before": sec.get("Before"), "notes_after": sec.get("After"),
                    "revision_note": rows[-1]["Reader note"] if rows else None}
            folder[f"{cid}.yaml"] = {k: v for k, v in meta.items() if v not in (None, [], "")}
        if pub is not None:
            bases = [l for l in stack_layers(project) if "/" not in l]
            outline = P/"bible/outline.md"
            planned = len({r["Chapter"] for r in table(outline, "## Chapters")}) if has(outline, "## Chapters") else None
            rel = [" & ".join(names[s] for s in r.split("+")) if "+" in r else "/".join(names[s] for s in r.split("/")) for r in pub.get("relationships", [])]
            work = {"title": y["name"], "authors": [a["name"] for a in y.get("authors", [])],
                    "fandoms": [load(pkg_dir(b)/"package.yaml")["name"] for b in bases],
                    "summary": pub.get("summary"), "rating": pub.get("rating"), "language": pub.get("language"), "tags": pub.get("tags"),
                    "relationships": rel, "characters": uniq(all_chars), "content_notes": uniq(all_notes),
                    "chapters": {k: v for k, v in {"count": len(chs), "planned": planned}.items() if v is not None},
                    "credits": [load(pkg_dir(l)/"package.yaml")["credit"] for l in stack_layers(project) if load(pkg_dir(l)/"package.yaml").get("credit")]}
            folder["work.yaml"] = {k: v for k, v in work.items() if v not in (None, [], "", {})}
        out[aud] = folder
    return out
def export_on_disk(project):
    root = EX/"projects"/project/"export"; out = {}
    for d in sorted(p for p in root.iterdir() if p.is_dir()) if root.exists() else []:
        out[d.name] = {f.name: (f.read_text() if f.suffix == ".md" else load(f)) for f in sorted(d.iterdir())}
    return out

TLBX = export("the-long-way-back")
check("R the export on disk is what the skill writes", export_on_disk("the-long-way-back") == TLBX, True)
check("R public holds the released chapters; early access adds chapter 3",
      {a: sorted(f for f in fs if f.endswith(".md")) for a, fs in TLBX.items()},
      {"public": ["chapter-01.md", "chapter-02.md"], "early-access": ["chapter-01.md", "chapter-02.md", "chapter-03.md"]})
X1 = TLBX["public"]["chapter-01.md"]
check("R the clean chapter keeps no comment and no front matter", ("<!--" in X1, "---" in X1, "status:" in X1), (False, False, False))
check("R the clean chapter: its title, then scene one, a scene break, and scene two",
      [l for l in X1.split("\n") if l.startswith("#") or l == "* * *"], ["# Narendra", "* * *"])
check("R blank lines collapse, and trailing space goes", ("\n\n\n" in X1, " \n" in X1, X1.endswith("war.\n")), (False, False, True))
check("R an untitled chapter is headed by its number", clean("---\nchapter: 9\n---\nText.\n", None, 9), "# Chapter 9\n\nText.\n")
check("R the scene break is the project's to choose", clean("---\n---\n<!-- scene: a=1 -->\nA.\n<!-- scene: a=2 -->\nB.\n", "T", 1, "~"), "# T\n\nA.\n\n~\n\nB.\n")
M1 = TLBX["public"]["chapter-01.yaml"]
check("R chapter 1's metadata", {k: M1.get(k) for k in ("title", "audience", "characters", "content_notes")},
      {"title": "Narendra", "audience": "public", "characters": ["Lt. Mira Oduya", "Rachel Garrett", "Tasha Yar (altered timeline)"], "content_notes": ["The death of a character"]})
check("R chapter 1: the author's notes to readers, and a word count", (M1["notes_before"][:9], M1["notes_after"][:9], M1["words"]), ("The story", "Thank you", words(X1)))
check("R chapter 1's date is its release", str(M1["date"]), "2026-09-04")
M3 = TLBX["early-access"]["chapter-03.yaml"]
check("R chapter 3, for early readers: its date, notes, and the latest revision note",
      (str(M3["date"]), M3["content_notes"], M3["revision_note"][:20]), ("2026-09-14", ["Grief and mourning"], "Chapter 3 revised: M"))
WP, WE = TLBX["public"]["work.yaml"], TLBX["early-access"]["work.yaml"]
check("R the work: names, authors, fandom, relationship", (WP["title"], WP["authors"], WP["fandoms"], WP["relationships"]),
      ("The Long Way Back", ["Ade", "Kit"], ["Star Trek"], ["Lt. Mira Oduya & Rachel Garrett"]))
check("R the public work knows two chapters and no Picard; early readers know three", (WP["chapters"], "Jean-Luc Picard" in WP["characters"], WE["chapters"], "Jean-Luc Picard" in WE["characters"]),
      ({"count": 2}, False, {"count": 3}, True))
check("R the work's notes are its chapters' notes, for each audience", (WP["content_notes"], WE["content_notes"]),
      (["The death of a character"], ["The death of a character", "Grief and mourning"]))
check("R a work with no credited layer lists no credits", "credits" in WP, False)
check("R a romance is A/B", "/".join(names_in("the-long-way-back")[0][s] for s in "mira-oduya/rachel-garrett".split("/")), "Lt. Mira Oduya/Rachel Garrett")
wd, _ = release(chs, "withdraw", [1])
check("R a withdrawn chapter leaves the public folder", sorted(f for f in export("the-long-way-back", chapters=wd)["public"] if f.endswith(".md")), ["chapter-02.md"])
noPub = copy.deepcopy(TLBY); noPub.pop("publishing")
check("R without publishing, clean chapters but no metadata", sorted(f for fs in export("the-long-way-back", y=noPub).values() for f in fs), ["chapter-01.md", "chapter-01.md", "chapter-02.md", "chapter-02.md", "chapter-03.md"])
check("R metadata never names a true identity before its reveal (Crouch, revealed at GoF:35)",
      (shown_names("two-witnesses", ["moody-impostor", "barty-crouch-jr"], lambda point: point != "GoF:35"),
       len(shown_names("two-witnesses", ["moody-impostor", "barty-crouch-jr"], lambda point: True))), (['"Mad-Eye Moody" (GoF)'], 2))
for k, v, ok in [("relationships", ["mira-oduya/rachel-garrett"], True), ("relationships", ["mira-oduya&rachel-garrett"], False),
                 ("language", "en-GB", True), ("language", "English", False), ("scene_break", "", False), ("colour", "red", False)]:
    d = copy.deepcopy(TLBY); d["publishing"][k] = v; check(f"R schema: publishing.{k} {v!r}", schema("project").is_valid(d), ok)

check("R the-long-way-back's front matter is valid", front_errors(chs, "serial"), [])
for label, chapters, wf, want in [
        ("released in a novel", [{"chapter": 1, "status": "released", "released": "d"}], "novel", 1),
        ("a schedule in a novel", [{"chapter": 1, "status": "line-edited", "release-on": "2026-12-01"}], "novel", 1),
        ("withdrawn, never released", [{"chapter": 1, "status": "withdrawn"}], "serial", 1),
        ("a schedule that is not a date", [{"chapter": 1, "status": "line-edited", "release-on": "next Friday"}], "serial", 1),
        ("a schedule with a time and offset", [{"chapter": 1, "status": "line-edited", "release-on": "2026-12-01T18:00+00:00"}], "serial", 0),
        ("a withdrawn chapter keeps the run unbroken", [{"chapter": 1, "status": "withdrawn", "released": "d"}, {"chapter": 2, "status": "released", "released": "d"}], "serial", 0)]:
    check(f"R front-matter error: {label}", len(front_errors(chapters, wf)), want)

T3 = {3: (TLB/"manuscript/chapter-03.md").read_text()}
after, why = release(chs, "release", [3], notes=True, by="kit")
check("R releasing chapter 3: released, dated, by Kit", (why, after[2]["status"], after[2]["released"], after[2]["released-by"], after[2]["early-access"]),
      (None, "released", "2026-12-01", "kit", chs[2]["early-access"]))
for label, args, kw, want in [
        ("chapter 4 before chapter 3", ("release", [4]), {"insist": True}, "4: out of order"),
        ("chapter 4, drafted, even in a run with 3", ("release", [3, 4]), {}, "4: from drafted"),
        ("a run refused whole when one fails", ("release", [3, 4]), {"pending": (4,), "insist": True}, "4: a pending decision or marker"),
        ("a TODO marker left in the text", ("release", [3]), {"texts": {3: "<!-- TODO: needs bible: the date -->"}}, "3: a pending decision or marker"),
        ("a release in a novel", ("release", [3]), {"workflow": "novel"}, "3: serial only"),
        ("a re-release under locked of a released chapter", ("re-release", [1]), {}, "1: from released"),
        ("withdrawing an unreleased chapter", ("withdraw", [3]), {}, "3: not released")]:
    got, why = release(chs, *args, **kw); check(f"R refused: {label}", why, want)
nb = [dict(c) for c in chs]; nb[2].pop("content-notes")
check("R refused: a chapter whose notes the author has not confirmed", release(nb, "release", [3], notes=True)[1], "3: notes not confirmed")
chs34 = [dict(c) for c in chs]; chs34[3].update({"status": "line-edited", "content-notes": []})
after, why = release(chs34, "release", [3, 4], notes=True)
check("R a run of chapters 3 and 4: one decision, one date", (why, [c.get("released") for c in after[2:]]), (None, ["2026-12-01", "2026-12-01"]))
check("R the not-ready SHOULD: the author may insist", release(chs34[:3] + [dict(chs34[3], status="drafted")], "release", [3, 4], insist=True)[1], None)
wd, why = release(chs, "withdraw", [2], by="ade")
check("R withdrawing chapter 2: kept its release date; 1 and 3 untouched", (why, wd[1]["status"], wd[1]["released"], wd[1]["withdrawn"], wd[0]["status"], wd[2]["status"]),
      (None, "withdrawn", chs[1]["released"], "2026-12-01", "released", "early-access"))
check("R chapter 3 may still be released after a withdrawn chapter 2", release(wd, "release", [3])[1], None)
rr, why = release(wd, "re-release", [2], date="2026-12-08")
check("R re-releasing the withdrawn chapter keeps its first release", (why, rr[1]["status"], rr[1]["released"], rr[1]["re-released"]), (None, "released", chs[1]["released"], "2026-12-08"))
check("R under revisable, a released chapter may be re-released", release(chs, "re-release", [1], locked=False)[1], None)

check("R chapter 3's schedule is in order", schedule_ok(chs, "release", 3, str(chs[2]["release-on"])), True)
check("R chapter 4 may not be scheduled before chapter 3's", schedule_ok(chs, "release", 4, "2026-11-30"), False)
check("R chapter 4 may be scheduled after chapter 3's", schedule_ok(chs, "release", 4, "2026-12-08"), True)
check("R chapter 4 may not be scheduled while 3 is unscheduled", schedule_ok([dict(c) for c in chs[:2]] + [{k: v for k, v in chs[2].items() if k != "release-on"}], "release", 4, "2026-12-08"), False)
due, told = run_schedules(chs, "2026-11-30T00:00")
check("R before its time, nothing happens", (due[2]["status"], told), ("early-access", []))
due, told = run_schedules(chs, "2026-12-02T09:00", notes=True)
check("R run late, the release takes the scheduled date and author", (due[2]["status"], due[2]["released"], due[2]["released-by"], "release-on" in due[2], told),
      ("released", "2026-12-01", "ade", False, []))
due, told = run_schedules(chs, "2026-12-02T09:00", texts={3: "<!-- TODO: seam conflict: x -->"})
check("R a schedule that fails its re-check is removed, and the author told", (due[2]["status"], "release-on" in due[2], told), ("early-access", False, ["3: a pending decision or marker"]))
print("\nFAILURES:", fails)
sys.exit(1 if fails else 0)
