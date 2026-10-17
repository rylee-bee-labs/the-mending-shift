# The Mending Shift — world pack (M2a)

A VEFR world pack for one shift at Sallowquay Boat-yard, built from the four
canon bibles in `bible/` (approved by Rylee 2026-10-17). This is M2a: the
skeleton, the residents, the items and the reachable recipe. The bibles are
canon and are never edited from here.

## What is built

- **`world.json`**
  - `name: mending-shift`, `title: The Mending Shift`.
  - `phases`: the four tide hours as slugs — `the-turning`, `low-water`,
    `the-run`, `slack-water` — each with one tone sentence drawn from
    `bible/world.md`'s account of that hour.
  - `time: {"rest": true, "rail": "locked", "persist": true}`, the block
    `bible/systems.md` asks for: the shift is walked one hour at a time, the
    rail cannot be clicked forward, and the standing hour survives a reload.
  - `town`: Sallowquay Boat-yard, 12 wide by 10 tall. `#` is the yard's wall
    (the boundary and the cliff the kit-runner climbs), `.` yard stone, `s` the
    shed, `b` the long bench under the lean-to, `k` the rack of hooks, `p` the
    pitch pot, `w` the slipway, `~` the water at the yard's foot. Plain colours
    only. `pois` names the shed, the rack, the bench, the pitch pot, the
    slipway, the wall and the causeway head; a POI's label is its id, so a rule
    can come near it.
  - `speakers`: the seven residents `bible/cast.md` writes, each under the full
    written name (`Warden Ottmar Vell`, never `Ottmar`), each with a position, a
    `voice_file` and a seed line for **every** phase. A resident who is not in
    the yard at an hour still has words there, because who is awake is carried
    by what they say and not by whether the engine can find them.
  - `items`: the eight records of `bible/systems.md`. The four reachable — the
    bone fid, the waxed tar-coat, the tin whistle, the bench knife — carry
    `grants` and, where systems.md gives a rewrite, `writes`. The four backlog
    items — the tarred line, the bend hook, the shuttered lamp, the winch bar —
    are declared and **unreachable**: no rule, drop or chest places them.
  - `recipes`: all six fusions with `keeps`, the inherited verb (`carries`),
    `output`, `read_aloud` and `say`.
  - `rules`: four handoffs and nothing else — Roald Fisk's coat at the end of
    The Turning, the warden's fid and the bench knife at Low Water, the night
    crew's whistle at the end of The Run, each gated on the standing phase and
    each naming its resident by the full written name.
- **`voices/<id>.md` and `voices/<id>.fragments.md`** for each of the seven
  residents: who they are, what they hand over and what they want, in the
  register `bible/cast.md` gives them.
- **`acceptance.py`**: the M2a gate (below).

The six heirloom outputs (`quiet-coat` and the rest) are declared as item
records because the engine refuses a recipe whose output it cannot describe. Their
`grants` are the union of the kept pieces' verbs plus the one verb the pair was
mended with, so the build is readable out of the data.

Two keys carry the rewrite, and the reason is in `bible/world.md`: an object
never adds a number, so nothing here raises attack. `writes` is systems.md's own
key and says which form of a verb is superseded; `changes` is the engine's key
and names the same verb at `atk: 0`. The button words in `grants` are where the
new form is actually written in the player's hand.

## What is M2b, not this

- **Beats.** The slice's five beats — the failing verbs at the wall and the foot
  of the causeway, Grissel Toft's heat-glove mended straight back onto her own
  hand, the two repairs at Low Water, the crossing refused at The Run, the
  crossing with a passenger at Slack Water, Tam Verrow's refused hook. None of
  them is a rule here. What is here is the four handoffs that put the four
  reachable objects in the satchel.
- **The rack preview.** The one look before a fusion: the heirloom's
  `read_aloud` name, its full verb list, and beneath it in plain text exactly
  what is lost forever, named piece by named piece.
- **The three outcomes.** Signed, deferred, refused — and the warden's reading of
  the satchel aloud at the yard end of the causeway.
- **Art.** Every tile here is a plain colour. The anchors in `art/` are chosen
  but unpainted, and no sprite, voice recording or picture is in this pack.
- Also unbuilt: `saves.rules: persist` (so a `once` handoff may repeat once
  after a reload), the slipway's flooding by phase, and any expression of the
  crossing's difficulty beyond the verb lists on the records.

## How to check it

From the repo root:

```sh
python3 worlds/mending-shift/acceptance.py
```

It exits 0 only when every assertion holds, and without `VEFR_DIR` it prints
`vefr check: SKIPPED (no VEFR_DIR)`. To run the engine's own gate as well:

```sh
VEFR_DIR=/path/to/vefr python3 worlds/mending-shift/acceptance.py
```

which adds `uv run --project $VEFR_DIR vefr check --pack <pack>` and requires
exit 0.

## Engine fit (Claude, 2026-10-17)

Run on the host against VEFR main 08fd8767, `vefr check` passes and `vefr weave` builds a playable file that
boots in Chromium with no errors. To make it pass:
- `town.pois` uses the engine's `{"x,y": "label"}` shape.
- `say.who` is the speaker id; the full written name is that speaker's `name`.
- The engine's recipe holds only `id, inputs, output, say`. systems.md's `keeps`, `carries` and `read_aloud` live in
  `design/recipes.json`, and the behaviour is the output item's `grants`: the kept verbs plus the carried one.
  acceptance.py checks the two agree.
- Two heirloom button labels were shortened to the engine's 60-character limit.
- The resident id is `grissel-toft`, matching the canon spelling.

Not done yet (M2b): the woven title screen still shows the engine's default cover art; the anchor art in
`art/anchor-r3/` is not wired in.

CI: `.github/workflows/pack.yml` runs the bible gates and `VEFR_DIR=.vefr python3 worlds/mending-shift/acceptance.py`
against VEFR main on every PR and push.
