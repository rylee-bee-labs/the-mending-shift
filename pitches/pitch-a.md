# Pitch A — M0 candidate

## Title

**The Mending Shift**

## Hook

You spend your first week at a tidal boat-yard carrying other people's broken tools, and every repair is a capability you sew
onto yourself rather than a number you grind higher. By the end of one shift, what crosses the flood channel is the knife, the
tar-coat and the whistle your neighbours handed you.

## Who you are

Pell Underhay, fifteen, newest kit-runner on the long bench at Sallowquay Boat-yard — a low stone yard that smells of brine
and hot pitch, where the tide sets the clock. No monster, no chosen one: one worker among forty, and what you want,
embarrassingly, is Warden Ottmar's signature on your shingle so you can be rostered on nights.

## The signature mechanic

**Kitting: a carried object either grants a verb you did not have or rewrites one you did.** Pell has no class and no stat
sheet — an apron, a satchel, four worn slots. Everything that makes you capable is a specific object someone owned first: a
sailmaker's bone fid, a diver's waxed tar-coat, a rigger's tin whistle. Objects add no damage: the fid turns `Climb` from
slow to silent, the coat rewrites `Wade` so you keep your hands.

What is new here: **mending is authoring, and authoring spends the thing you stitch into it.** Every object carries a mend
history — patches, replaced stitching, someone else's name scratched off. To give an object a new capability you unpick it
into another: two mended pieces fuse into one heirloom keeping both verbs and losing the rest forever. The expressive act is
subtraction, and the yard remembers it.

## The 30-60 minute slice

One shift, 4am tide to slack water, one ending beat: **the shingle**. Pell opens with an apron, an empty satchel and two
verbs that visibly fail at the slipway; the three good objects are in other people's hands.

- **The bench loop (8-35 min).** Three asks — Ottmar's fid, Sable's coat, the night crew's whistle — each a repair in the
  pack's rule vocabulary. Residents hand objects over across the hour, so you meet them at their phase and hear a different
  version of the ask at dusk than at dawn.
- **The choice (35-45 min).** Three usable objects, four slots, a rack that fuses two. What you fuse is the build; what you
  leave stays in the yard as somebody's tool, and the residents who wanted it stop offering.
- **The flood (45-55 min).** You cross the slipway and re-cross it with a passenger, and can only manage the second crossing
  with what the shift produced; a build that kept one cheap verb gets across slowly, visibly, twice.
- **Ending (55-60 min).** Ottmar reads the satchel aloud and names the build you made in the yard's own words. The shingle is
  signed or deferred on the strength of what is in it.

## Why players would love it

Because what is remembered is the shape of what you could do, and here that shape is made of other people's cast-offs. The
claim set is consistent that attachment goes to a capability you can point at: a retrospective calls the relic system's
signature reward that each relic carries a special effect "ranging from staff buffs, to new commands, or game-breaking
augments" (https://goombastomp.com/final-fantasy-6-retrospective/) rather than a stat, and a party-based RPG's review puts it
for assembly — "Character creation is also notably improved."
(https://rpgamer.com/review/baldurs-gate-ii-shadows-of-amn-review/) We want that to be the whole game rather than its reward
track. And the craft is the point, not only the kit: an editor writes "I mine materials for hours, finally smelt some
armour" (https://www.rockpapershotgun.com/have-you-played-terraria).

## What players might criticize

**"Job-and-class scaffolding replaced."** We replace the scaffold with a *bench*, not with nothing. No class, but a trade:
Pell apprenticed at the long bench, and the bench is why unpicking and fusing is possible at all.

**"Builds capped rather than deepened."** Four worn slots is the same cap in different clothes. So we cap count and never
depth: fusing keeps both verbs, so a build's verb count only rises. If fusion flattens the fiction, fusion also grants one
verb from the two it loses.

**"Earned power arriving early."** The first mended piece lands near minute twelve, deliberately crude: the fid climbs, but
it rattles, and anyone in the yard hears it. The build is not weaker later — it is quieter.

## VEFR feasibility

Judged only by `research/A2-feasibility.md`, which studied time-of-day and not inventory — so the kit layer below has no A2
coverage. That gap is the top risk.

**BUILT.** One authored line per resident per hour, validator-enforced for first-region speakers
(`src/vefr/maplab.py:3605`, bounded by the skip at `src/vefr/maplab.py:3598`) and picked by the hour you are standing in
(`web/player/parts/480-town-input-and-turns.js:1407`); the pool bakes per phase per speaker (`src/vefr/pool.py:83`). And items
are the one thing rules act on at all — show/hide/reveal returns for anything that is not an item
(`web/player/parts/510-rules-closure-surfaces.js:72`) — so the kit is an authored object surface.

**PARTIAL.** Phase is in-memory only (`web/player/parts/060-minimal-state.js:3`), so nothing A2 read shows a kit surviving a
reload. `once` defaults to true (`web/player/parts/445-rules-engine.js:368`), so a "mended only at dusk" event fires once per
save unless the author writes `"once": false`.

**MISSING, and we lean on two of them.** There is no verb that waits or rests (`web/player/parts/076-keybinds.js:60`) and the
phase jump is free (`web/player/parts/250-phase-rail.js:10`), so "daylight costs you the shift" is not expressible. A rule
cannot condition on the standing hour (`src/vefr/maplab.py:836`), the `on:` workaround is refused
(`src/vefr/maplab.py:2610`), and flag-conditioned dialogue is still `Proposed` (`docs/adr/0005-dialogue-state.md:7`).

**PACK-ONLY FALLBACK, zero engine change.** The slice ships as a pack: phases as the tide's hours, one seed per resident per
hour, and — load-bearing — a resident who only speaks at night, authored as a rule whose event payload is
`{"phase-changes": {"to": "<phase>"}}` (`src/vefr/maplab.py:1001`) whose `say` names that resident. Three limits: it fires on
the transition, not the standing state; `once` defaults true; and it works only in the woven player, since the standalone
rails fire no rules (`web/town.js:293`, `web/index.html:2512`).

## Scope and risks

Cost: one region, one shed, forty speakers at four hours each (~160 authored lines), eight items with fuse pairs, one bench
minigame, one shingle ending, and a first pass of item-granted verbs in the rule vocabulary — a pack-sized build, not an
engine-sized one, if the kit is items plus rules, not new code.

1. **The verb layer is unverified.** A2 shows items are a rule surface and show/hide/reveal is items-only
   (`web/player/parts/510-rules-closure-surfaces.js:72`), but shows no mechanism by which an item *rewrites a verb*. If VEFR
   cannot grant or change a capability, the signature mechanic does not exist and this pitch needs an unscoped engine change.
2. **Time cannot cost anything.** The slice's second half is MISSING; the fallback is to make daylight descriptive — the rack
   fills on the yard's own schedule — rather than something the player pays.
3. **Fusion is irreversible and unmeasured.** No playtest has been run and none is claimed, and A2 measured none of the kit
   layer. If fusion reads as loss-aversion rather than authorship, preview the heirloom's name and verb list before committing.

## Status

**MOCKUP.** Pitch A of three, for milestone M0 — not canon, not a design of record, and nothing committed until Rylee picks
one. No build, no playtest and no spend have been made against it; the feasibility section reads
`research/A2-feasibility.md` only, with its gaps stated rather than smoothed over.
