# Visual anchor, round 3 (OpenDesign, A2 refined)

Status: **scene + tiles APPROVED as the working anchor** (MiniMax judge 21/25, APPROVE; Claude approves, 2026-10-17).
**Bryn (round 4): APPROVED.** The round-3 sheet failed: its back view repeated the front torso and its side view was not a profile. Round 4 fixed both (MiniMax: all three fixes DONE, consistency 5/5, APPROVE). Files: `bryn-*.png` and `bryn-sheet.png` (top row front, back, side idle; bottom row the walk contact poses). `generate_pixel_art_v4.py` reproduces it.

This is a working anchor for building the slice, not canon. Canon and final art direction stay Rylee's (gate 4).

- `option-anchor-scene.png`: a 12x10-tile scene at 1x (32 px tiles)
- `option-anchor-tiles.png`, `tile-00..17.png`: the 18-tile set
- `generate_pixel_art_v2.py` and `generate_pixel_art_v3.py`: original integer raster code, no external art. Run `python3 generate_pixel_art_v3.py`; it reproduces the scene byte-for-byte (checked 2026-10-17).
- Judgements: `research/anchors-round-3-minimax-judgement.md`, `research/anchors-round-4-bryn-minimax-judgement.md`
