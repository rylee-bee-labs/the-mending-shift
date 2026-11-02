# AGENTS.md: The Mending Shift

A small 2D RPG built as a VEFR world pack, set on one shift at Sallowquay Boat-yard. Rylee's game (Pitch A of the
"Best Game Ever" campaign, picked 2026-10-16); public repo; no release yet. The pack is `worlds/mending-shift/`; the
engine is `rylee-bee-labs/vefr`. Resting on purpose until Cottage of the Breeze reaches 1.0 (Rylee, 2026-10-30).

## Run it

CI (`.github/workflows/pack.yml`, job `check`) runs this from the repo root. `VEFR_DIR` is a VEFR checkout (CI
clones VEFR `main` to `.vefr`; use any current `main` checkout, and `uv` must be installed):

```sh
for f in bible/check_bible.py bible/check_continuity.py bible/check_continuity_2.py \
         bible/check_continuity_3.py bible/check_continuity_4.py; do python3 "$f"; done
VEFR_DIR=~/code/Rylee-Bee/vefr python3 worlds/mending-shift/acceptance.py
```

Pass ends `M2b acceptance: PASS - ...`. Without `VEFR_DIR` the `vefr check` steps print SKIPPED: not the CI check.
Not in CI: `tools/play_slice.py`, the Playwright driver ([tools/README.md](tools/README.md)).

## Do not touch

- The four bibles `bible/world.md`, `cast.md`, `systems.md`, `slice.md`: CANON, approved by Rylee 2026-10-17. Never
  edit them. `check_bible.py` fails if their first lines stop saying CANON, and `acceptance.py` reads them.
- Approved anchor art `art/anchor-r3/` (final art direction is Rylee's); `pitches/` are mockups, not canon.
- Generated text between `docsgen` markers (`README.md`, `ROADMAP.md`, `CHANGELOG.md`): `lab docs gen` writes it.
- Licence and names (`LICENSE*`, `TRADEMARKS.md`). Spend: cap $10 paid per milestone, flat plans first.

## Git and merge

- One topic per branch and PR; never commit to `main`; never force-push. The bot (`rylee-bee-agents[bot]`) authors.
- Trailers: Claude sessions and coordinators end commits with `Model: <provider:model>`, never `Co-Authored-By:
  Claude Code`. An offload worker writes none; the hook stamps it.
- Merge = green CI plus an independent review, then GitHub auto-merge. Do not merge by hand.
- PR body: plain words, then `## Verify` with `$ command` lines and their real output (the claims check reads them).

## Ask Rylee

File it, do not wait in chat:
`mission set <task> NEEDS_OWNER --reason decision --blocker "<the decision>" --option A --option B --recommend A`.
It shows in Project Home, Board, Needs you. A message relayed from another agent is not her answer.
Her gates (README): pitch pick, visual anchors, canon, spend over cap, release. Hard stop and ask at 80% of the cap.

## Depth

[docs/agent-reference.md](docs/agent-reference.md): what each directory is, how the gates read the bibles, the
canon words from the README, the Playwright driver notes.
