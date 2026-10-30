#!/usr/bin/env python3
"""M1 acceptance: the four bibles exist with their sections, all are marked CANON (approved 2026-10-17), no name leaked
from the synthetic audition bible, and the systems spec uses the engine's planned data shapes."""
import pathlib
import re

B = pathlib.Path("bible")
NEED = {
    "world.md": ["## The place", "## How the world works", "## The tide and the hours", "## Tone", "## What is never true here"],
    "cast.md": ["## The kit-runner", "## The yard"],
    "systems.md": ["## Items and the verbs they grant", "## Mending recipes", "## Time", "## The shingle ending"],
    "slice.md": ["## Beat 1", "## Beat 2", "## Beat 3", "## The ending beat"],
}
LEAKED = ["Pell", "Lisle", "Ness", "Oda", "Merrow", "Ys "]   # names from the synthetic A3 audition bible
for name, heads in NEED.items():
    t = (B / name).read_text(encoding="utf-8")
    missing = [h for h in heads if h not in t]
    assert not missing, f"{name} lacks {missing}"
    head = "\n".join(t.split("\n", 3)[:3])
    assert "CANON - approved by Rylee 2026-10-17" in head and "DRAFT" not in head, f"{name}: the first lines must say CANON, approved 2026-10-17"
    leaks = [n for n in LEAKED if re.search(r"\b" + re.escape(n.strip()) + r"\b", t)]
    assert not leaks, f"{name} uses names from the synthetic audition bible: {leaks}"
s = (B / "systems.md").read_text(encoding="utf-8")
for shape in ('"grants"', '"recipes"', '"inputs"', '"output"', '"time"', '"rest"'):
    assert shape in s, f"systems.md does not use the planned engine shape {shape}"
cast = (B / "cast.md").read_text(encoding="utf-8")
assert len(re.findall(r"^### ", cast, re.M)) >= 6, "cast.md needs at least 6 characters (### headings)"
print("ok: four CANON bibles, no leaked names, systems in the engine's shapes")
