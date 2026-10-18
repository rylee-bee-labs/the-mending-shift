#!/usr/bin/env python3
"""Offline negative tests for acceptance.py's M3b resident-sprite contract.

`acceptance.py` is the check that guards the seven residents' sprites, so the
check itself needs a test: a scratch copy of the pack, one mutation at a time,
and the run's verdict asserted. Every case here is a way the M3b contract was
let through or crashed the checker before the second review.

    python3 worlds/mending-shift/test_acceptance_sprites.py

Runs offline and needs no VEFR_DIR; the mutations are made on a temp copy, never
on the committed sprites. Exits 0 when every case behaves, 1 otherwise.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACK = Path(__file__).resolve().parent
CHECKER = PACK / "acceptance.py"

# Every resident the pack ships art for, minus Bryn, who has her own checks.
RESIDENTS = sorted(path.name[: -len(".sheet.json")]
                   for path in (PACK / "sprites").glob("*.sheet.json")
                   if path.name != "hero.sheet.json")

# What each broken sidecar looks like: (label, mutation, what must be said).
# `mutate` takes the parsed sidecar and breaks it in place; the third item is the
# line that must be said, either a fixed string or one built from the mutation.
CASES = [
    ("missing up and right",
     lambda meta, key: [meta["directions"].pop(facing) for facing in ("up", "right")],
     "has no 'up' direction"),
    ("idle is a number, not a list",
     lambda meta, key: meta["directions"]["down"].__setitem__("idle", 3),
     "idle must be a list of frame numbers"),
    ("walk is a string, not a list",
     lambda meta, key: meta["directions"]["down"].__setitem__("walk", "ab"),
     "walk must be a list of frame numbers"),
    ("a frame entry is an object",
     lambda meta, key: meta["directions"]["down"].__setitem__("walk", [2, {}]),
     "is not a whole frame number"),
    ("a frame entry is a bool",
     lambda meta, key: meta["directions"]["down"].__setitem__("walk", [2, True]),
     "is not a whole frame number"),
    ("directions is not a map",
     lambda meta, key: meta.__setitem__("directions", ["down"]),
     "has no 'directions' map"),
    # A frame of no size in one axis: the grid modulo and division below used to
    # read it anyway and raise ZeroDivisionError out of the checker.
    ("frame width is zero",
     lambda meta, key: meta.__setitem__("frame", [0, meta["frame"][1]]),
     lambda meta: "frame [w, h] of positive whole numbers, got [0, %d]" % meta["frame"][1]),
    ("frame height is zero",
     lambda meta, key: meta.__setitem__("frame", [meta["frame"][0], 0]),
     lambda meta: "frame [w, h] of positive whole numbers, got [%d, 0]" % meta["frame"][0]),
]


def run_checker(root):
    """(exit status, everything the checker said) for a scratch copy of the pack."""
    done = subprocess.run([sys.executable, str(root / "acceptance.py")],
                          capture_output=True, text=True, cwd=str(root))
    return done.returncode, done.stdout + done.stderr


def scratch(root, key, mutate):
    """A temp copy of the pack whose <key>.sheet.json is mutated; committed files untouched.

    Also hands back the mutated sidecar, so a case can say what it expects to be
    told from a value it does not want to hard-code.
    """
    tmp = tempfile.mkdtemp(prefix="m3b-negative-")
    pack = Path(tmp) / "mending-shift"
    shutil.copytree(PACK, pack)
    sidecar = pack / "sprites" / ("%s.sheet.json" % key)
    meta = json.loads(sidecar.read_text(encoding="utf-8"))
    mutate(meta, key)
    sidecar.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return tmp, pack, meta


# One resident is enough to prove the frame-size contract; the main() sweep below
# then runs every case against every resident.
FRAME_SIZE_KEY = RESIDENTS[0]


def bad_frame_says(frame):
    """(exit status, what the checker said) for <FRAME_SIZE_KEY> with `frame` as its size."""
    tmp, pack, _ = scratch(PACK, FRAME_SIZE_KEY,
                           lambda meta, key: meta.__setitem__("frame", frame))
    try:
        return run_checker(pack)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def assert_fails_cleanly(label, frame, expected):
    status, said = bad_frame_says(frame)
    assert status != 0, "%s: frame %r passed, should have failed:\n%s" % (label, frame, said)
    assert "Traceback" not in said, "%s: frame %r crashed the checker:\n%s" % (label, frame, said)
    assert expected in said, "%s: frame %r gave no %r:\n%s" % (label, frame, expected, said)
    assert FRAME_SIZE_KEY in said, "%s: frame %r never named the resident:\n%s" % (label, frame, said)


def test_frame_width_zero_fails_cleanly():
    assert_fails_cleanly("frame width is zero", [0, 33],
                          "frame [w, h] of positive whole numbers, got [0, 33]")


def test_frame_height_zero_fails_cleanly():
    assert_fails_cleanly("frame height is zero", [26, 0],
                          "frame [w, h] of positive whole numbers, got [26, 0]")


def main():
    failures = []

    status, said = run_checker(PACK)
    if status != 0:
        failures.append("the unmutated pack should pass, got exit %d:\n%s" % (status, said))
    else:
        print("ok: the pack as committed passes (exit 0)")

    for key in RESIDENTS:
        for label, mutate, expected in CASES:
            tmp, pack, meta = scratch(PACK, key, mutate)
            want = expected(meta) if callable(expected) else expected
            try:
                status, said = run_checker(pack)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)

            if status == 0:
                failures.append("%s / %s: passed, should have failed" % (key, label))
                continue
            if "Traceback" in said:
                failures.append("%s / %s: crashed the checker\n%s" % (key, label, said))
                continue
            if want not in said:
                failures.append("%s / %s: exit %d but no %r in:\n%s"
                                % (key, label, status, want, said))
                continue
            if key not in said:
                failures.append("%s / %s: exit %d but never named the resident:\n%s"
                                % (key, label, status, said))
                continue
            print("ok: %s / %s fails cleanly and names the cause (exit %d)"
                  % (key, label, status))

    for failure in failures:
        print("FAIL: %s" % failure)
    print("%d of %d case(s) failed." % (len(failures), 1 + len(RESIDENTS) * len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())