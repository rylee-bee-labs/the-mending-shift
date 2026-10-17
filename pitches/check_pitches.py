#!/usr/bin/env python3
"""M0 acceptance: exactly three pitch files, each with every required section, at least two A1 claims cited
by exact URL from research/A1-verified.md, and at least one VEFR file:line or A2 reference in the feasibility section."""
import pathlib
import re
import sys

REQUIRED = ["## Title", "## Hook", "## Who you are", "## The signature mechanic", "## The 30-60 minute slice",
            "## Why players would love it", "## What players might criticize", "## VEFR feasibility",
            "## Scope and risks", "## Status"]
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "pitches")
verified = set(re.findall(r'Source: <?(https?://[^\s>]+)', open("research/A1-verified.md", encoding="utf-8").read()))
files = sorted(root.glob("pitch-*.md"))
assert len(files) == 3, f"expected exactly 3 pitch-*.md files, found {[f.name for f in files]}"
for f in files:
    text = f.read_text(encoding="utf-8")
    missing = [h for h in REQUIRED if h not in text]
    assert not missing, f"{f.name} lacks {missing}"
    cited = {u for u in re.findall(r'https?://[^\s>)\]"]+', text) if u in verified}
    assert len(cited) >= 2, f"{f.name} cites {len(cited)} host-verified A1 URLs (need 2+)"
    feas = text.split("## VEFR feasibility", 1)[1].split("\n## ", 1)[0]
    assert re.search(r'[\w/.-]+\.(py|js|json|md|html|css):\d+|A2-feasibility', feas), f"{f.name}: feasibility cites no file:line or A2"
    assert "MOCKUP" in text.split("## Status", 1)[1], f"{f.name}: Status must say MOCKUP (not canon until Rylee picks)"
print("ok: 3 pitches, all sections, verified citations, feasibility grounded, marked MOCKUP")
