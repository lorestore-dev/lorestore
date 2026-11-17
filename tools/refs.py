"""Check that every § reference in the spec and the repository's documents resolves to a
numbered heading in spec/.

Usage:
    python tools/refs.py [repo-root]     # repo-root defaults to this file's parent's parent

Prints each unresolved reference as <file>:<line>: §<n>, or a confirmation; exits 1 if
any reference does not resolve. Ranges (§6.7–6.8, §10.1–2) check both ends.

It also checks relative Markdown links in the same files: each must point to a file that
exists, and an anchor in a Markdown file must be one of its headings or an
<a id="…"></a>. Every example case in examples/README.md (an <a id="case-…"></a>) must
be linked from at least one spec section.
"""
import re, sys, pathlib

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
DOCS = ("README.md", "CONTRIBUTING.md", "DECISIONS.md", "ROADMAP.md", "CLAUDE.md", "examples/README.md")

heads = set()
for p in sorted((ROOT / "spec").glob("*.md")):
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"#+\s+(\d+(?:\.\d+)*)\.?\s", line)
        if m: heads.add(m.group(1))

files = sorted((ROOT / "spec").glob("*.md")) + [ROOT / f for f in DOCS if (ROOT / f).is_file()]
bad = []
for p in files:
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        for m in re.finditer(r"§\s?(\d+(?:\.\d+)*)((?:[–-]\d+(?:\.\d+)*)?)", line):
            refs = [m.group(1)]
            if m.group(2):
                end = m.group(2)[1:]
                if "." not in end and "." in refs[0]:
                    end = refs[0].rsplit(".", 1)[0] + "." + end
                refs.append(end)
            bad += [f"{p.relative_to(ROOT).as_posix()}:{i}: §{r}" for r in refs if r not in heads]

def slug(h):
    """A heading's anchor, as GitHub makes it."""
    return re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")

def anchors(path):
    """A Markdown file's headings' anchors and its <a id> anchors, outside fenced code."""
    out, fence = set(), False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"): fence = not fence; continue
        if fence: continue
        m = re.match(r"#+\s+(.*)", line)
        if m: out.add(slug(m.group(1)))
        out.update(re.findall(r'<a id="([^"]+)"></a>', line))
    return out

EXAMPLES = (ROOT / "examples/README.md").resolve()
cache, linked = {}, set()
for p in files:
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        for m in re.finditer(r"\]\(([^)\s]+)\)", line):
            href = m.group(1)
            if re.match(r"[a-z]+:", href): continue
            target, _, frag = href.partition("#")
            dest = (p.parent / target).resolve() if target else p.resolve()
            where = f"{p.relative_to(ROOT).as_posix()}:{i}: {href}"
            if not dest.exists():
                bad.append(where + " (no such file)"); continue
            if frag and dest.suffix == ".md":
                if dest not in cache: cache[dest] = anchors(dest)
                if frag not in cache[dest]: bad.append(where + " (no such anchor)")
            if p.parent.name == "spec" and dest == EXAMPLES:
                linked.add(frag)

cases = re.findall(r'<a id="(case-[^"]+)"></a>', EXAMPLES.read_text(encoding="utf-8"))
bad += [f"examples/README.md: #{c} is linked from no spec section" for c in cases if c not in linked]

print("\n".join(bad) or "all § references and links resolve")
sys.exit(1 if bad else 0)
