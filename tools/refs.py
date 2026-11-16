"""Check that every § reference in the spec and the repository's documents resolves to a
numbered heading in spec/.

Usage:
    python tools/refs.py [repo-root]     # repo-root defaults to this file's parent's parent

Prints each unresolved reference as <file>:<line>: §<n>, or a confirmation; exits 1 if
any reference does not resolve. Ranges (§6.7–6.8, §10.1–2) check both ends.
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

print("\n".join(bad) or "all § references resolve")
sys.exit(1 if bad else 0)
