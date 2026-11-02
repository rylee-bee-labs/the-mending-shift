# The Mending Shift: agent reference

Detail behind `AGENTS.md`. Nothing here overrides it.

## What each path is

| Path | What it is |
|---|---|
| `bible/` | the four CANON bibles (`world.md`, `cast.md`, `systems.md`, `slice.md`), the continuity rounds, and the `check_*.py` gates that read them |
| `worlds/mending-shift/` | the VEFR pack: `world.json`, `acceptance.py`, `voices/`, `sprites/`, `tiles/`, `assets/`, `design/recipes.json`; its own README has the rules, beat by beat |
| `pitches/` | the three M0 mockup pitches (A, B, C); `check_pitches.py` checks their shape and is not run by CI |
| `research/` | A1 mechanics, A2 feasibility, and the MiniMax anchor judgements |
| `art/anchor-r3/` | the approved working anchor (scene, tiles, Bryn) and the scripts that draw it and the seven residents |
| `tools/play_slice.py` | the Playwright driver that plays a woven slice through all four phases ([tools/README.md](../tools/README.md)) |

## How the gates read the bibles

- `bible/check_bible.py`: the four bibles have their required sections, their first lines say `CANON - approved by
  Rylee 2026-10-17`, no name leaked from the synthetic audition bible, and `systems.md` uses the engine's data shapes.
- `bible/check_continuity.py`, `_2`, `_3`, `_4`: each runs `check_bible.py`, then requires its `CONTINUITY*.md` to
  answer every finding in its `continuity-findings*.md` with FIXED (where) or NOT A CONTRADICTION (why).
- `worlds/mending-shift/acceptance.py`: the pack against the bibles (phases, the seven residents under their full
  written names, eight items, six recipes, 40-rule ceiling, five beats, three outcomes, art and sprites resolving
  inside the pack). With `VEFR_DIR` it also asks VEFR to bake Bryn's walk sheet and runs `vefr check`; both are
  skipped, with a SKIPPED line, when it is unset.
- `worlds/mending-shift/test_acceptance_sprites.py`: offline negative tests for acceptance.py's sprite contract
  (`python3 worlds/mending-shift/test_acceptance_sprites.py`; no `VEFR_DIR`). Not run by CI.
- `bible/GATE4-FOLLOWUPS.md` records what changed after Rylee approved the bibles (tag `canon-approved-2026-10-17`).

## Rylee's words in the README, kept here

- "Nothing here is canon until Rylee approves it (owner gates: pitch pick, visual anchors, canon, spend over cap, release)."
- "Resting on purpose until Cottage of the Breeze reaches 1.0 (Rylee, 2026-10-30). The first slice is playable; canon
  calls belong to Claude and MiniMax (Rylee, 2026-10-17)."
- "Campaign launched 2026-10-16 after audition pass 3 passed (rylee-bee-workspace charter review section 11). Cap: $10
  paid per milestone, flat plans first; hard stop and escalation at 80%."
- 2026-10-16, Rylee (gate 2, picker): **Pitch A, The Mending Shift**. The direction is set; the pitch itself is still
  a MOCKUP until the bibles and anchors are approved (gates 3 and 4). The hero's name "Pell" is replaced, because it
  leaked from the synthetic audition bible. (The bibles were approved 2026-10-17; the anchor art is the working anchor.)

The first and second lines read against each other: the bibles are approved canon and stay untouched, while the
2026-10-17 line hands later canon calls to Claude and MiniMax. When it is unclear which applies, ask (see
`AGENTS.md`, "Ask Rylee").

## The Playwright driver

`tools/play_slice.py` is a manual check, not a CI gate. `--plan` prints the walk with no browser and runs in under a
second. Its README says the driver had not been run against a real browser, and the first real run needs
`python3 -m pip install playwright && python3 -m playwright install chromium`. On 2026-11-02 its documented
`--self-test` had not finished after two minutes on the agent host and was stopped; the cause is UNKNOWN.
