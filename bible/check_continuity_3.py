#!/usr/bin/env python3
"""M1b acceptance: the bible gate still passes, and bible/CONTINUITY-3.md answers every finding H01..Hnn in
bible/continuity-findings-3.md with FIXED (where) or NOT A CONTRADICTION (why)."""
import re
import subprocess
import sys

r = subprocess.run([sys.executable, "bible/check_bible.py"], capture_output=True, text=True)
assert r.returncode == 0, r.stdout + r.stderr
ids = re.findall(r"^## (H\d+)", open("bible/continuity-findings-3.md", encoding="utf-8").read(), re.M)
ans = open("bible/CONTINUITY-3.md", encoding="utf-8").read()
missing = [i for i in ids if not re.search(rf"\b{i}\b.*(FIXED|NOT A CONTRADICTION)", ans)]
assert not missing, f"CONTINUITY.md does not answer: {missing}"
print(f"ok: bible gate passes; all {len(ids)} findings answered")
