"""LoreStore conformance checker for the examples in this repository.

Validates the example workspace in examples/ against the JSON schemas, and runs a
reference implementation of the snapshot algorithm (§7), canon points (§4.2), the canon
track and project order (§6.7-6.8), branch and retelling modes (§6.6), and hidden truths
(§4.4, §6.12), comparing each result with the expected answers in examples/README.md.

Usage:
    pip install -r tools/requirements.txt
    python tools/check.py [repo-root]     # repo-root defaults to this file's parent's parent

Prints one line per check, then a failure count; exits 1 if any check fails.

Limitations: it checks the bundled examples only (paths and expected values are
hard-coded), so it is not a validator for arbitrary workspaces. It does not check
markdown links or § references, the agent and workflow chapters, or prose formats
beyond the tables it parses.
"""
import json, re, sys, pathlib, copy, yaml, jsonschema

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
EX = ROOT / "examples"
fails = 0
def check(label, got, want):
    global fails
    ok = got == want; fails += not ok
    print(("ok  " if ok else "FAIL"), label, "" if ok else f": got {got!r}, want {want!r}")

def schema(name): return jsonschema.Draft202012Validator(json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text()))
def valid(name, doc):
    try: schema(name).validate(doc); return True
    except jsonschema.ValidationError as e: print("   ", e.message); return False

# --- schemas -----------------------------------------------------------------
for w in ["harry-potter", "star-trek"]:
    check(f"schema world-config {w}", valid("world-config", yaml.safe_load((EX/f"worlds/{w}/world-config.yaml").read_text())), True)
for p in ["two-witnesses", "the-long-way-back", "hogwarts-at-warp"]:
    check(f"schema project {p}", valid("project", yaml.safe_load((EX/f"projects/{p}/project.yaml").read_text())), True)
check("schema universe", valid("universe", yaml.safe_load((EX/"universes/wizards-and-warp/universe.yaml").read_text())), True)
for f, idx, name in [("10-formats", 0, "project"), ("10-formats", 2, "world-config"), ("08-crossovers", 0, "universe")]:
    block = re.findall(r"```yaml\n(.*?)```", (ROOT/f"spec/{f}.md").read_text(), re.S)[idx]
    check(f"schema spec example {f}[{idx}]", valid(name, yaml.safe_load(block)), True)
bad = yaml.safe_load((EX/"projects/hogwarts-at-warp/project.yaml").read_text()); bad["setting"]["canon_point"] = "HBP:7"
check("schema rejects canon_point in universe project", schema("project").is_valid(bad), False)
ser = yaml.safe_load((EX/"projects/the-long-way-back/project.yaml").read_text())
check("schema serial project, default release policy", (ser["workflow"], "serial" in ser, schema("project").is_valid(ser)), ("serial", False, True))
ser["serial"] = {"released": "revisable"}; check("schema serial revisable accepted", schema("project").is_valid(ser), True)
ser["serial"] = {"released": "frozen"}; check("schema serial unknown policy rejected", schema("project").is_valid(ser), False)
nov = yaml.safe_load((EX/"projects/two-witnesses/project.yaml").read_text()); nov["serial"] = {"released": "locked"}
check("schema serial block on novel rejected", schema("project").is_valid(nov), False)
bad = yaml.safe_load((EX/"worlds/harry-potter/world-config.yaml").read_text()); bad["canon_profiles"]["x"] = {"order": ["books"], "resolution": "newest"}
check("schema rejects unknown resolution", schema("world-config").is_valid(bad), False)

# --- parsing -------------------------------------------------------------------
def table(path, heading):
    lines = path.read_text().splitlines(); out, started = [], False
    for l in lines[lines.index(heading)+1:]:
        if l.startswith("|"): started = True; out.append(l)
        elif started: break
    cells = [[c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]] for l in out]
    return [dict(zip(cells[0], r)) for r in cells[2:]]

class Incomparable(Exception): pass

class World:
    def __init__(self, wid):
        self.dir = EX / "worlds" / wid
        self.cfg = yaml.safe_load((self.dir/"world-config.yaml").read_text())
        ruler = self.dir/"canon-timeline.md"
        self.works = {}
        for r in table(ruler, "## Works"):
            levels = [l.strip() for l in r["Levels"].split("›")] if r["Levels"] else []
            tl = r["Timed level"]
            self.works[r["Work"]] = (levels, None if not tl else 0 if tl == "work" else levels.index(tl) + 1)
        self.segments = {}; self.counts = {}
        for r in table(ruler, "## Order"):
            path = self.split(r["Segment"]); self.segments[path] = int(r["Order"]); self.counts[path] = r["Units"]
        if "## Counts" in ruler.read_text():
            for r in table(ruler, "## Counts"): self.counts[self.split(r["Node"])] = r["Units"]
        segs = list(self.segments)
        assert not any(a != b and a == b[:len(a)] for a in segs for b in segs), "overlapping segments"
    def reordered(self, project):
        f = EX / "projects" / project / "bible/canon-track.md"
        if not f.exists() or "## Order" not in f.read_text(): return self
        rows = table(f, "## Order")
        segs = {self.split(r["Segment"]): int(r["Order"]) for r in rows}
        assert set(segs) == set(self.segments) and len(rows) == len(self.segments), "order must be a permutation"
        w = copy.copy(self); w.segments = segs; return w
    @staticmethod
    def split(s):
        w, *idx = s.split(":"); return (w, *map(int, idx))
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
        if tc is not None and (timed is None or len(path) - 1 < timed): raise ValueError(pt)
        return path, tc, inside, contains, timed
    def pos(self, pt):
        path, tc, inside, contains, timed = self.parse(pt)
        if inside: s = inside[0]; return (self.segments[s], 1, path[len(s):]), path, tc, timed
        return (min(self.segments[s] for s in contains), 0, (len(path),)), path, tc, timed
    def cmp(self, a, b):
        """-1/0/1 per §4.2; raises Incomparable. Empty = timeless, sorts first."""
        if not a or not b: return (bool(a) > bool(b)) - (bool(a) < bool(b))
        (ka, pa, ta, timed), (kb, pb, tb, _) = self.pos(a), self.pos(b)
        if ka[:2] != kb[:2] or ka[1] == 0: return (ka > kb) - (ka < kb)
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
    def rows(self, entity):
        f = self.dir / "characters" / f"{entity}.md"
        out = table(f, "## State history") if f.exists() else []
        if (self.dir/"relationships.md").exists():
            out += [r for r in table(self.dir/"relationships.md", "## State history") if r["Pair"] == entity]
        if (self.dir/"species.md").exists():
            out += [r for r in table(self.dir/"species.md", "## State history") if r["Entity"] == entity]
        if (self.dir/"knowledge.md").exists():
            out += [dict(r, Attribute=r["Secret"], Value=r["State"]) for r in table(self.dir/"knowledge.md", "## Knowledge") if r["Character"] == entity]
        return out

BRANCH_ERRORS = []

def track_cutoff(project, position, default):
    f = EX / "projects" / project / "bible/canon-track.md"
    if not f.exists() or "## Track" not in f.read_text(): return default
    chap = lambda c: int(c.split("-")[1]); cut = default
    for r in table(f, "## Track"):
        if chap(r["From chapter"]) <= chap(position): cut = r["Cutoff"]
    return cut

def snapshot(world, entity, cutoff, profile, position=None, project=None):
    if project:
        world = world.reordered(project)
        st = yaml.safe_load((EX/f"projects/{project}/project.yaml").read_text())["setting"]
        if cutoff is None:
            cutoff = track_cutoff(project, position, st["canon_point"])
        if st.get("canon_mode") == "branch" and world.cmp(cutoff, st["divergence_point"]) > 0:
            BRANCH_ERRORS.append((project, cutoff)); cutoff = st["divergence_point"]
    prof = world.cfg["canon_profiles"][profile]
    order = ["project", "bridge"] + prof["order"]; mode = prof.get("resolution", "precedence")
    import functools
    K = functools.cmp_to_key(world.cmp)
    rows = [r for r in world.rows(entity) if r["Source"] in order and world.cmp(r["As of"], cutoff) <= 0]
    out = {}
    for attr in {r["Attribute"] for r in rows}:
        cand = [r for r in rows if r["Attribute"] == attr]
        if mode == "precedence":
            best = min(order.index(r["Source"]) for r in cand)
            win = max((r for r in cand if order.index(r["Source"]) == best), key=lambda r: K(r["As of"]))
        else:
            latest = max((r["As of"] for r in cand), key=K)
            win = min((r for r in cand if world.cmp(r["As of"], latest) == 0), key=lambda r: order.index(r["Source"]))
        if win["Value"] != "(unset)": out[attr] = win["Value"]
    if project:
        chap = lambda c: int(c.split("-")[1])
        for d in table(EX/f"projects/{project}/bible/divergences.md", "## Divergences"):
            active = position is None or (chap(d["First occurs"]) <= chap(position) and not (d.get("Until") and chap(d["Until"]) <= chap(position)))
            if d["Overrides"] != "—" and active:
                for a in d["Overrides"].split("; "):
                    lhs, v = a.split("=", 1); ent, att = lhs.rsplit(".", 1)
                    if ent == entity:
                        if v == "(unset)": out.pop(att, None)
                        else: out[att] = v
    return out

HP, ST = World("harry-potter"), World("star-trek")
g = lambda w, e, c, p, a, **k: snapshot(w, e, c, p, **k).get(a)

# --- Harry Potter ---------------------------------------------------------------
check("1 residence PS:2", g(HP, "harry-potter", "PS:2", "book-purist", "residence"), "cupboard under the stairs, 4 Privet Drive")
check("1 residence PS:3", g(HP, "harry-potter", "PS:3", "book-purist", "residence"), "Dudley's second bedroom")
for c, want in [("PS:9", None), ("PS:10", "Nimbus Two Thousand"), ("PoA:10", None), ("PoA:11", "Firebolt")]:
    check(f"2 broom {c}", g(HP, "harry-potter", c, "book-purist", "broom"), want)
for p, early, late in [("book-purist", "round", "round"), ("enriched", "round", "round"), ("enhanced", "round", "contact lenses")]:
    check(f"3 glasses {p} PS:5", g(HP, "harry-potter", "PS:5", p, "glasses"), early)
    check(f"3 glasses {p} GoF:37", g(HP, "harry-potter", "GoF:37", p, "glasses"), late)
check("4 daphne house book-purist", g(HP, "daphne-greengrass", "GoF:37", "book-purist", "house"), None)
check("4 daphne house enriched", g(HP, "daphne-greengrass", "GoF:37", "enriched", "house"), "Slytherin")
check("4 daphne house enhanced", g(HP, "daphne-greengrass", "GoF:37", "enhanced", "house"), "Slytherin")
check("4 daphne year OotP:30", g(HP, "daphne-greengrass", "OotP:30", "enhanced", "year"), None)
check("4 daphne year OotP:31", g(HP, "daphne-greengrass", "OotP:31", "book-purist", "year"), "Harry's year")
check("5 cedric no ledger", g(HP, "cedric-diggory", "GoF:37", "enhanced", "status"), "dead")
check("5 cedric ledger ch1", g(HP, "cedric-diggory", "GoF:37", "enhanced", "status", position="chapter-01", project="two-witnesses"), "alive")
check("5 cedric GoF:20", (g(HP, "cedric-diggory", "GoF:20", "enhanced", "status"), g(HP, "cedric-diggory", "GoF:20", "enhanced", "role")), ("alive", "Hogwarts Triwizard champion"))
check("6 bond PS:8", g(HP, "harry-potter+hermione-granger", "PS:8", "book-purist", "bond"), "acquaintances")
check("6 bond PS:10", g(HP, "harry-potter+hermione-granger", "PS:10", "book-purist", "bond"), "friends")
check("7 knowledge GoF:34", g(HP, "harry-potter", "GoF:34", "book-purist", "moody-identity"), "unaware")
check("7 knowledge GoF:35", g(HP, "harry-potter", "GoF:35", "book-purist", "moody-identity"), "knows")
roster = {r["Slug"]: r for r in table(HP.dir/"characters/_roster.md", "## Characters")}
check("7 reveal alias", (roster["moody-impostor"]["Reveal of"], roster["moody-impostor"]["Revealed at"]), ("barty-crouch-jr", "GoF:35"))

# --- Star Trek ------------------------------------------------------------------
for c, want in [("TNG:3:25", "captain of the USS Enterprise-D"), ("TNG:3:26", "assimilated as Locutus of Borg"),
                ("TNG:4", "assimilated as Locutus of Borg"), ("TNG:4:1", "captain of the USS Enterprise-D")]:
    check(f"8 picard {c}", g(ST, "jean-luc-picard", c, "canon-only", "status"), want)
check("9 tasha TNG:1", g(ST, "tasha-yar", "TNG:1", "canon-only", "status"), "chief of security, USS Enterprise-D")
check("9 tasha TNG:2", g(ST, "tasha-yar", "TNG:2", "canon-only", "status"), "dead")
check("10 mirror TOS2:3", snapshot(ST, "spock-mirror", "TOS:2:3", "canon-only"), {})
check("10 mirror TOS2:4", g(ST, "spock-mirror", "TOS:2:4", "canon-only", "appearance"), "bearded")
check("10 spock has no mirror rows", "appearance" in snapshot(ST, "spock", "TNG:4:26", "canon-only"), False)
check("species borg TNG2:15", g(ST, "borg", "TNG:2:15", "canon-only", "known-to-federation"), None)

# --- Crossover ------------------------------------------------------------------
pj = yaml.safe_load((EX/"projects/hogwarts-at-warp/project.yaml").read_text())["setting"]
check("12 harry broom", g(HP, "harry-potter", pj["canon_points"]["harry-potter"], pj["active_profiles"]["harry-potter"], "broom"), "Firebolt")
check("12 picard", g(ST, "jean-luc-picard", pj["canon_points"]["star-trek"], pj["active_profiles"]["star-trek"], "status"), "captain of the USS Enterprise-D")

# --- canon points (§4.2) ---------------------------------------------------------
def isvalid(pt):
    try: ST.parse(pt); return True
    except ValueError: return False
for pt, want in [("TOS:3:2:14", True), ("TOS:3:2:14+00:12:31", True), ("TMP+01:10:05", True), ("TOS:3:25", False),
                 ("TNG:1:5", False), ("TOS:3+00:01:00", False), ("TOS:3:2:14:1", False), ("TOS:3:2+00:61:00", False), ("DS9:1", False),
                 ("TOS", True), ("TNG", True), ("TMP:4", True)]:
    check(f"P valid {pt}", isvalid(pt), want)
chain = "TOS TOS:1 TOS:3:2 TOS:3:2:14 TOS:3:2:14+00:12:31 TOS:3:2:15 TMP TMP+01:10:05 TNG TNG:1 TNG:2 TNG:2:16".split()
check("P ordering chain", all(ST.cmp(a, b) < 0 for a, b in zip(chain, chain[1:])), True)
check("P ordering transitive sample", all(ST.cmp(chain[i], chain[j]) < 0 for i in range(len(chain)) for j in range(i+1, len(chain))), True)
check("P timecodes win over scenes", ST.cmp("TOS:3:2:14+00:20:00", "TOS:3:2:15+00:10:00"), 1)
try: ST.cmp("TOS:3:2+00:12:31", "TOS:3:2:14"); check("P incomparable reported", False, True)
except Incomparable: check("P incomparable reported", True, True)
check("P different episodes comparable", ST.cmp("TOS:3:2+00:12:31", "TOS:3:3:1"), -1)
check("P HP chapter scene", HP.cmp("PS:6", "PS:6:2") < 0 and HP.cmp("PS:6:2", "PS:7") < 0, True)
try: HP.parse("PS:6+00:00:01"); check("P untimed work rejects timecode", False, True)
except ValueError: check("P untimed work rejects timecode", True, True)

# --- canon track and rearranged canon (§6.6–6.7) ----------------------------------------
R = "second-year-tournament"
def snap_r(e, a, ch, ledger=True):
    if ledger: return snapshot(HP, e, None, "book-purist", position=ch, project=R).get(a)
    return snapshot(HP.reordered(R), e, track_cutoff(R, ch, "PS:17"), "book-purist").get(a)
check("T track cutoff ch05", track_cutoff(R, "chapter-05", "PS:17"), "GoF:1")
check("T track cutoff ch15", track_cutoff(R, "chapter-15", "PS:17"), "GoF:37")
check("T track before first row", track_cutoff(R, "chapter-00", "PS:17"), "PS:17")
check("T order: GoF before PoA", HP.reordered(R).cmp("GoF:20", "PoA:17"), -1)
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

def inversions(world, project):
    w = world.reordered(project); out = set(); groups = {}
    for f in (world.dir/"characters").glob("[!_]*.md"):
        for r in table(f, "## State history"): groups.setdefault((f.stem, r["Attribute"]), []).append(r)
    for r in table(world.dir/"relationships.md", "## State history"): groups.setdefault((r["Pair"], r["Attribute"]), []).append(r)
    for (e, a), rows in groups.items():
        for x in rows:
            for y in rows:
                if x["Value"] != y["Value"] and x["As of"] and y["As of"] and world.cmp(x["As of"], y["As of"]) < 0 and w.cmp(x["As of"], y["As of"]) > 0:
                    out.add(f"{e}.{a}")
    return out
inv = inversions(HP, R)
check("T inversions found", inv, {"harry-potter+sirius-black.bond", "cedric-diggory.status", "cedric-diggory.role"})
covered = set()
for d in table(EX/f"projects/{R}/bible/divergences.md", "## Divergences"):
    if d["Overrides"] != "—": covered |= {a.split("=")[0] for a in d["Overrides"].split("; ")}
check("T every inversion covered by a divergence", inv - covered, set())
check("T no inversions in two-witnesses (canon order)", inversions(HP, "two-witnesses"), set())
check("T Q2 addition D2 (scar)", snapshot(HP, "cedric-diggory", "GoF:37", "enhanced", position="chapter-02", project="two-witnesses").get("scars"), "curse scar across his chest")
for d in table(EX/f"projects/{R}/bible/divergences.md", "## Divergences"):
    if d.get("Until"): check(f"V Until after First occurs {d['ID']}", int(d["Until"].split("-")[1]) > int(d["First occurs"].split("-")[1]), True)

# --- branch and retelling (§6.6) -------------------------------------------------------
B, T = "no-horcruxes", "blind-harry"
check("B voldemort dead from chapter-01", snapshot(HP, "lord-voldemort", None, "book-purist", position="chapter-01", project=B).get("status"), "dead")
check("B broom at chapter-50 stays Nimbus (no later canon)", snapshot(HP, "harry-potter", None, "book-purist", position="chapter-50", project=B).get("broom"), "Nimbus Two Thousand")
check("B sirius never met", snapshot(HP, "harry-potter+sirius-black", None, "book-purist", position="chapter-50", project=B).get("bond"), "strangers")
check("B no branch errors from fixture track", BRANCH_ERRORS, [])
check("B cutoff past divergence point is clamped and reported", (BRANCH_ERRORS, snapshot(HP, "harry-potter", "PoA:11", "book-purist", position="chapter-50", project=B).get("broom")), ([(B, "PoA:11")], "Nimbus Two Thousand"))
BRANCH_ERRORS.clear()
sr = lambda a, ch: snapshot(HP, "harry-potter", None, "book-purist", position=ch, project=T).get(a)
check("R sight blind from chapter-01", sr("sight", "chapter-01"), "blind")
check("R glasses removed (C1 remove)", sr("glasses", "chapter-05"), None)
check("R role at chapter-08 absent (PS:9 not reached)", sr("role", "chapter-08"), None)
check("R role adapted at chapter-09 (C2 adapt)", sr("role", "chapter-09"), "Gryffindor Seeker, flying by sound and feel")
check("R broom kept at chapter-10 (C3 keep)", sr("broom", "chapter-10"), "Nimbus Two Thousand")
check("R canon still happens: house at chapter-09", sr("house", "chapter-09"), "Gryffindor")
br = yaml.safe_load((EX/f"projects/{B}/project.yaml").read_text()); del br["setting"]["divergence_point"]
check("schema branch without divergence point rejected", schema("project").is_valid(br), False)
og = yaml.safe_load((EX/f"projects/{T}/project.yaml").read_text()); og["setting"]["type"] = "original"; og["setting"].pop("fidelity")
check("schema canon_mode on original rejected", schema("project").is_valid(og), False)
for pj in (B, T): check(f"schema project {pj}", schema("project").is_valid(yaml.safe_load((EX/f"projects/{pj}/project.yaml").read_text())), True)

# --- True from and hidden canon (§4.4, §6.12, §7.2) ----------------------------------------
def hidden(world, entity, cutoff, profile, project=None):
    if project: world = world.reordered(project)
    order = ["project", "bridge"] + world.cfg["canon_profiles"][profile]["order"]
    return {r["Attribute"] for r in world.rows(entity) if r["Source"] in order and r.get("True from")
            and world.cmp(r["True from"], cutoff) <= 0 < world.cmp(r["As of"], cutoff)}
check("H snape loyalty not resolved at PS:17", snapshot(HP, "severus-snape", "PS:17", "book-purist").get("loyalty"), None)
check("H snape loyalty is a hidden truth at PS:17", hidden(HP, "severus-snape", "PS:17", "book-purist"), {"loyalty"})
check("H hidden truth even at PS:1", hidden(HP, "severus-snape", "PS:1", "book-purist"), {"loyalty"})
check("H not hidden once revealed (DH:33)", (hidden(HP, "severus-snape", "DH:33", "book-purist"), snapshot(HP, "severus-snape", "DH:33", "book-purist").get("loyalty")), (set(), "loves Lily Potter, and protects Harry for her sake"))
check("H branch: hidden at chapter-05", snapshot(HP, "severus-snape", None, "book-purist", position="chapter-05", project="no-horcruxes").get("loyalty"), None)
check("H branch: revealed early at chapter-20 (D2)", snapshot(HP, "severus-snape", None, "book-purist", position="chapter-20", project="no-horcruxes").get("loyalty"), "loves Lily Potter, and protects Harry for her sake")
for f in (HP.dir/"characters").glob("[!_]*.md"):
    for r in table(f, "## State history"):
        if r.get("True from"): assert HP.cmp(r["True from"], r["As of"]) <= 0, (f, r)
check("V True from never later than As of", True, True)
for r in table(EX/"projects/no-horcruxes/bible/divergences.md", "## Hidden canon"):
    ok = (r["Decision"] != "reveal-early" or r["Divergence"] not in ("", "—")) and (r["Decision"] != "other" or r["Note"])
    check(f"V hidden canon decision {r['Entity']}.{r['Attribute']}", ok, True)

# --- validations ----------------------------------------------------------------
try: ST.key("TNG:1:5"); check("V TNG:1:5 rejected", False, True)
except ValueError: check("V TNG:1:5 rejected", True, True)
for w in (HP, ST):
    ex = set(w.cfg["canon_basis"]["excluded"])
    check(f"V no excluded in profiles {w.cfg['id']}", any(ex & set(p["order"]) for p in w.cfg["canon_profiles"].values()), False)
    reg = {r["ID"] for r in table(w.dir/"sources.md", "## Sources")} | {"project", "bridge"}
    for p in w.cfg["canon_profiles"].values(): assert set(p["order"]) <= reg, p
    for f in (w.dir/"characters").glob("[!_]*.md"):
        for r in table(f, "## State history"):
            assert r["Source"] in reg, (f, r); w.key(r["As of"])
    check(f"V sources and points valid {w.cfg['id']}", True, True)
for proj, w in [("two-witnesses", HP), ("the-long-way-back", ST)]:
    wr = {r["Slug"] for r in table(w.dir/"characters/_roster.md", "## Characters")}
    pr = {r["Slug"] for r in table(EX/f"projects/{proj}/bible/characters/_roster.md", "## Characters")}
    check(f"V no union collision {proj}", wr & pr, set())
    pin = yaml.safe_load((EX/f"projects/{proj}/project.yaml").read_text())["world"]["version"]
    check(f"V version pin {proj}", pin, w.cfg["version"])
    divs = {d["ID"] for d in table(EX/f"projects/{proj}/bible/divergences.md", "## Divergences")}
    cons = {c["Divergence"] for c in table(EX/f"projects/{proj}/bible/divergences.md", "## Consequences")}
    check(f"V consequences {proj}", divs <= cons, True)
u = yaml.safe_load((EX/"universes/wizards-and-warp/universe.yaml").read_text())
check("V universe pins", {x["id"]: x["version"] for x in u["worlds"]}, {"harry-potter": HP.cfg["version"], "star-trek": ST.cfg["version"]})
for t in table(EX/"projects/the-long-way-back/bible/timelines.md", "## Legs"):
    for pt in (t["Departs"], t["Arrives"]): ST.key(pt.split("@")[0])
    ST.key(t["Personal cutoff"])
check("V frames points valid", True, True)
print("\nFAILURES:", fails)
sys.exit(1 if fails else 0)
