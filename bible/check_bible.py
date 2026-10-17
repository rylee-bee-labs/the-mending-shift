#!/usr/bin/env python3
"""M1 acceptance: the four draft bibles exist with their sections, all are marked DRAFT (not canon), no name leaked
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
    assert "DRAFT" in t.split("\n", 3)[0] + t.split("\n", 3)[1] + t.split("\n", 3)[2], f"{name}: the first lines must say DRAFT"
    leaks = [n for n in LEAKED if re.search(r"\b" + re.escape(n.strip()) + r"\b", t)]
    assert not leaks, f"{name} uses names from the synthetic audition bible: {leaks}"
s = (B / "systems.md").read_text(encoding="utf-8")
for shape in ('"grants"', '"recipes"', '"inputs"', '"output"', '"time"', '"rest"'):
    assert shape in s, f"systems.md does not use the planned engine shape {shape}"
cast = (B / "cast.md").read_text(encoding="utf-8")
assert len(re.findall(r"^### ", cast, re.M)) >= 6, "cast.md needs at least 6 characters (### headings)"
print("ok: four DRAFT bibles, no leaked names, systems in the engine's shapes")
