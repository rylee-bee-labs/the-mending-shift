# The Mending Shift — world pack (M2e)

A VEFR world pack for one shift at Sallowquay Boat-yard, built from the four
canon bibles in `bible/` (approved by Rylee 2026-10-17). M2a built the skeleton,
the residents, the items and the recipes; **M2b builds the five beats of
`bible/slice.md` as rules**, the fusion at the rack, and the three outcomes of
the shingle; **M2c wires the approved anchor art** so the game opens on this
yard and not on the engine's default cover; **M2e makes Bryn the hero in play**
and fixes the shape the sprite map is written in. The bibles are canon and are
never edited from here.

## What is built

- **`world.json`**
  - `name: mending-shift`, `title: The Mending Shift`.
  - `player`: `title_art` (the cover a shared file opens on) and `sprites`, the
    map the hero and every `sprite` in the pack are drawn from — Bryn's six
    approved frames under both the three-view names and the four facings, and
    nothing else (see **Art**).
  - `phases`: the four tide hours as slugs — `the-turning`, `low-water`,
    `the-run`, `slack-water` — each with one tone sentence drawn from
    `bible/world.md`'s account of that hour.
  - `time: {"rest": true, "rail": "locked", "persist": true}`, the block
    `bible/systems.md` asks for: the shift is walked one hour at a time, the
    rail cannot be clicked forward, and the standing hour survives a reload.
    Every rule below is written against that block — nothing moves the hour
    except Rest, and every rule that means anything at an hour reads the
    standing phase with `if: [{"phase": "<slug>"}]`.
  - `flags`: the two names a rule sets. `work-mended` (the two repairs were
    laid at the bench at Low Water) and `quiet-coat-made` (the rack fused the
    fid and the coat).
  - `town`: Sallowquay Boat-yard, 12 wide by 10 tall. `#` is the yard's wall
    (the boundary and the cliff the kit-runner climbs), `.` yard stone, `s` the
    shed, `b` the long bench under the lean-to, `k` the rack of hooks, `p` the
    pitch pot, `w` the slipway, `~` the water at the yard's foot. Each glyph's
    `base` colour is kept as the fallback, and seven of the eight also name an
    approved `tile` (see **Art**). `pois` names the shed, the rack, the bench,
    the pitch pot, the slipway, the wall and the causeway head; a POI's label is
    its id, so a rule can come near it.
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
  - `rules`: **23 rules** over the five beats (the engine's own ceiling is 40).
- **`voices/<id>.md` and `voices/<id>.fragments.md`** for each of the seven
  residents: who they are, what they hand over and what they want, in the
  register `bible/cast.md` gives them.
- **`design/recipes.json`**: systems.md's design keys the engine's recipe shape
  does not hold (`keeps`, `carries`, `read_aloud`).
- **`acceptance.py`**: the gate (below).

The six heirloom outputs (`quiet-coat` and the rest) are declared as item
records because the engine refuses a recipe whose output it cannot describe. Their
`grants` are the union of the kept pieces' verbs plus the one verb the pair was
mended with, so the build is readable out of the data.

Two keys carry the rewrite, and the reason is in `bible/world.md`: an object
never adds a number, so nothing here raises attack. `writes` is systems.md's own
key and says which form of a verb is superseded; `changes` is the engine's key
and names the same verb at `atk: 0`. The button words in `grants` are where the
new form is actually written in the player's hand.

## The rules, by beat

Rules run in the order written, and every rule writes `once` on itself, because
`bible/systems.md` says the default (`true`) is the one to override on purpose.

| Beat | Rules |
|---|---|
| 1 The Turning | `the-turning-opens` (all seven residents' lines for the hour), `the-slow-climb-fails-at-the-wall`, `the-hands-under-wade-fails-at-the-causeway-foot`, `tam-verrow-offers-the-bent-hook`, `grissel-toft-hands-over-the-heat-glove`, `roald-fisk-hands-over-the-coat` |
| 2 Low Water | `low-water-comes-in`, `the-warden-hands-over-the-fid`, `the-knife-comes-off-the-rack`, `the-repairs-are-laid-at-the-bench`, `the-rack-offers-the-preview`, `the-rack-fuses-the-fid-and-the-coat` |
| 3 The Run | `the-run-floods`, `margit-brack-hands-over-the-whistle`, `the-crossing-is-refused-at-the-causeway-head` |
| 4 Slack Water | `slack-water-sets`, `the-note-carries-across-the-water`, `she-comes-across-under-the-quiet-coat`, `she-comes-across-one-crossing-at-a-time` |
| 5 The shingle | `the-shingle-is-signed`, `the-shingle-is-deferred`, `the-shingle-is-refused-empty`, `the-shingle-is-refused-over-a-refused-object` |

How the five beats are written:

- **Every resident's line for every phase** is in the rules, not only in the
  `seeds`. One rule per hour (`phase-changes` **and** a standing-phase `if`)
  carries all seven lines at the moment the hour turns; `acceptance.py` checks
  every seed line is spoken by a rule under that resident's own id.
- **The hour lines are `once: false`.** They fire on the transition into the
  hour, which is what Rest produces, and `bible/systems.md` is explicit that a
  rule meant to fire on every visit needs `once: false` written on it.
- **The beat moments are `once: true`** and keyed on `comes-near` a place or a
  resident with a standing-phase `if`, so they happen while you are standing in
  that hour and not on the transition.
- **The two failing starting verbs** fire on `uses-verb` at The Turning, each
  carrying `{"not": {"has": ...}}` so the line is the *starting* form's failure
  and never the mended one's.

## The fusion at the rack

`fuse-fid-coat` is the one reachable pair, and it is the only one whose inputs
a player can hold. The moment is two rules:

- `the-rack-offers-the-preview`, gated on Low Water, on carrying **both**
  inputs, and on `quiet-coat-made` still false. It is the one look, said once:
  the heirloom's name as the bench will say it (`the quiet coat`), its full verb
  list — the two kept forms and the inherited one — and, underneath in plain
  text, what is lost forever, named piece by named piece. It fires **before** the
  mend and never after it, which is the absolute in `bible/world.md`: a fusion is
  never previewed twice and there is no later look at the same loss.
- `the-rack-fuses-the-fid-and-the-coat` fires on `{"mends": {"recipe":
  "fuse-fid-coat"}}`. The recipe's own `say` carries systems.md's line; the
  rule adds Maud Bray saying what the mend spent (her scratch, gone with the
  seam thread — she said so at the bench first), the yard reading both spent
  names on the heirloom, and the `quiet-coat-made` flag the shingle reads. Mend
  consumes both inputs itself, so no `takes` is written.

What the engine has no word for: that the preview is rack **UI**. The engine
speaks the preview as a `say`, so the words on it are a narrator's line rather
than a panel — the content is systems.md's, the surface is the closest one the
rules layer has.

## The three outcomes

All four rules are keyed on `comes-near` the warden at the yard end of the
causeway at Slack Water, and each is keyed on the satchel:

| Outcome | Rule | Condition that can be met |
|---|---|---|
| **Signed** | `the-shingle-is-signed` | the shift's work is mended and the satchel holds `quiet-coat` — a build means a decision |
| **Deferred** | `the-shingle-is-deferred` | `work-mended` is true, with no heirloom and no refused object in the satchel — mended work, nothing decided |
| **Refused** | `the-shingle-is-refused-empty` | `work-mended` is false — the satchel is empty |
| **Refused** | `the-shingle-is-refused-over-a-refused-object` | `work-mended` is true, no heirloom, and `bend-hook` is in the satchel — an object whose owner was told no |

`acceptance.py` proves each outcome is reachable by searching the rules' own
conditions for a state that satisfies them (every subset of the items the rule
names, every set of the flags it names, each of the four hours), and it proves
they **partition** the space: it walks every such state at the hour the shingle
is read and requires that exactly one of the four rules fires, so no satchel is
read out twice and none is read out at all. Where two conditions could have
overlapped, the heirloom wins: a satchel that holds one is signed, whatever else
is in it.

**The fourth row cannot fire in this slice, and that is deliberate.** The bent
hook is refused at The Turning and never enters the satchel — systems.md's
reachability decision — so the second refused cause in systems.md and slice.md
("holds an object whose owner came to the bench for it and was told no") has no
way to happen here. The rule is written anyway because it is canon, and its
condition is satisfiable as data; a later slice that puts the hook in a
player's bag switches it on without touching the shingle.

## Art

M2c wires the approved anchor art into the pack. **Provenance:
[`art/anchor-r3/README.md`](../../art/anchor-r3/README.md)** — round 3 (scene +
the 18-tile set) and round 4 (Bryn), approved by Claude 2026-10-17. Nothing was
regenerated or repainted for this step; every file below is a byte-for-byte copy
out of that folder, checked with `cmp`, and `generate_pixel_art_v3.py` /
`generate_pixel_art_v4.py` reproduce all 25 of them. The pack holds no path out
to `art/`: a player runs the pack alone.

| Where | What | From |
|---|---|---|
| `assets/title.png` | the 12x10-tile anchor scene, wired as `player.title_art` — the file the shared game opens on, in place of the engine's default cover | `option-anchor-scene.png` |
| `sprites/hero.png` | Bryn Aukett's still, wired as `player.sprites.hero` | `bryn-front.png` (via `make_sheet.py`) |
| `sprites/hero-sheet.png` + `hero.sheet.json` | Bryn's walk sheet: down, up and right (left mirrors right), idle plus a two-step walk | `bryn-{front,back,side}.png` + `-walk.png` |
| `sprites/bryn-*.png` | the approved round-4 frames the sheet was built from | `bryn-*.png` |
| `tiles/*.png` | the 18-tile set, named for the kinds `generate_pixel_art_v3.py`'s `TILES` list gives them | `tile-00..17.png` |

Seven of the eight town glyphs name a tile; the `tile` value is the stem of a
file in the pack's `tiles/`, which the engine looks for before its own art:

| Glyph | Tile | What it paints |
|---|---|---|
| `#` | `wall` | the yard's wall, the cliff the kit-runner climbs |
| `.` | `paving` | worn flags, the walkable yard |
| `s` | `door` | shed planks |
| `b` | `boards` | bench grain under the lean-to |
| `k` | `rack` | hooks and rope |
| `w` | `rock` | black basalt, the slipway |
| `~` | `water` | the open channel |

**`p`, the pitch pot, has no approved tile**, so it keeps the engine default and
its own `base` colour, as it did in M2b. The other eleven tiles — the tide foam,
the four copings and their corners, the cliff return and the five slip edges —
are copied in and carry names the legend can use when a later slice draws the
shoreline out of whole cells.

**How vefr finds the hero (M2e, read from the engine, not guessed).** `vefr`'s
`cli.resolve_sprites` reads `player.sprites` as *key -> pack-relative path*, and
the hero's key is `hero`. A walk sheet rides beside it as `sprites/hero.sheet.json`
naming `hero-sheet.png` (`cli._player_sprite_sheets`). M2c wrote paths under view
names (`front`/`back`/`side`) and M2e's first attempt wrote stems under both view
and facing names; vefr reads neither, which is why the hero stayed a white circle.
The sheet was built with vefr's own `tools/art/make_sheet.py` from the approved
round-4 frames; each walk cycle pairs the standing pose with the walk pose, since
the engine takes two or more walk frames. The seven residents have no approved
sprite yet and keep the engine's default figure (see **Not built**).

## Acceptance coverage (selected)

  under the engine's 40-rule ceiling.
- **M2c**: `player.title_art` is set and the file is inside the pack, and every
  sprite and every `tile` the legend names resolves to a file inside the pack —
  a path that climbs out of the pack, or names a file that is not there, fails.
- **M2e**: `player.sprites.hero` is a pack-relative path to a file inside the
  pack, `sprites/hero.sheet.json` names an image that exists and gives down, up
  and right an idle frame and at least two walk frames; and with `VEFR_DIR` set,
  vefr's own `_player_sprite_sheets` must bake a `hero` sheet from this pack (so a
  sheet the engine would not pick up fails).

To run the engine's own gate as well:

```sh
VEFR_DIR=/path/to/vefr python3 worlds/mending-shift/acceptance.py
```

which adds `uv run --project $VEFR_DIR vefr check --pack <pack>` and requires
exit 0.

## Engine fit

M2a (Claude, 2026-10-17) was run on the host against VEFR main 08fd8767 and
`vefr check` passed. To make it pass:
- `town.pois` uses the engine's `{"x,y": "label"}` shape.
- `say.who` is the speaker id; the full written name is that speaker's `name`.
- The engine's recipe holds only `id, inputs, output, say`. systems.md's `keeps`,
  `carries` and `read_aloud` live in `design/recipes.json`, and the behaviour is
  the output item's `grants`: the kept verbs plus the carried one.
  acceptance.py checks the two agree.
- Two heirloom button labels were shortened to the engine's 60-character limit.
- The resident id is `grissel-toft`, matching the canon spelling.

M2b's rules use only shapes `docs/guides/rules.md` documents: the fourteen
events (`starts`, `enters`, `comes-near`, `opens`, `picks-up`, `uses-with`,
`defeats`, `buys`, `sells`, `reads`, `phase-changes`, `falls`, `wakes`,
`uses-verb`, `mends`), the conditions `has`, `flag`/`is`, `phase`, `not` and
`all-of`, and the actions `say`, `give` and `set`. Every named speaker id, POI
label, phase, item, flag and recipe is one the pack declares.
**`vefr check` was not run on M2b's rules** — the sandbox has no `uv` or `vefr`
— so CI (`.github/workflows/pack.yml`, which runs the bible gates and this
acceptance with `VEFR_DIR`) is the first place these rules are seen by the
engine.

M2c's art keys are in the same position, and one is worth a decision on the
host run. `title_art` and the legend's `tile` come out of
`docs/guides/world-creation.md` as this brief quoted them. `player.sprites` is
named by the same brief but its own shape is **not** in the excerpt.

**M2e** read the hero's shape out of vefr's source (`resolve_sprites`,
`_player_sprite_sheets`) after a host play-through showed the white circle, and a
second host run shows Bryn drawn in play. `world.json` still carries M2a's
`"surface": "plain"`, which only hides HUD rows (HP, level, the verb row) and
does not affect sprites; it stays as M2a set it.

## Not built

- **`saves.rules: persist`.** Without it a `once` rule's fired marker is
  forgotten on reload, so a handoff may repeat once after a reload and the
  standing hour is the `time` block's own persistence rather than the rules'.
- **The rack preview is a `say`, not rack UI** (see above).
- **Art.** The cover, the hero and seven of the eight glyphs are wired (see
  **Art** above); what is left is the pitch pot `p`, which has no approved tile
  and still draws as its `base` colour, and the eleven shoreline and slip tiles,
  which are copied in but not yet named by any glyph. No voice recording is in
  this pack.
- **The seven residents have no approved sprite**, and the decisions in force
  for this step allow no new art, so each keeps the engine's own figure. To
  commission, one line each: `warden-ottmar-vell` (Warden Ottmar Vell),
  `roald-fisk` (Roald Fisk), `sable-kearn` (Sable Kearn), `margit-brack`
  (Margit Brack), `tam-verrow` (Tam Verrow), `maud-bray` (Maud Bray),
  `grissel-toft` (Grissel Toft). The wiring is a picture at `sprites/<speaker-key>.png`
  (vefr resolves a speaker key by name) or a `player.sprites` entry with a
  pack-relative path;
  `acceptance.py` will hold both to a file inside this pack.
- **The four worn slots and the bag cap** are in the bibles and in the prose;
  the engine has no cap on carried items, so the bind at the rack is said
  rather than enforced.
- **The crossing's difficulty** is in the two Slack Water rules (one for the
  fused coat, one for everything else) and not in any number.
- **`point-to` hints** ("Where next?") are left out: the guide documents the
  action but not its payload, and a rule here may only use keys the guide
  spells out.