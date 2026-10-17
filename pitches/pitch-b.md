# Pitch B — The Best Game Ever (working title)

## Title

**Slackwater Shift**

## Hook

You are a relief shift-warden walking a freight route, and every interruption on it — a derail, an inspector, a
washout on the causeway — is a job you *file*, on a ledger, against a schedule you cannot make late. The game is
deciding how often to stop, and how fast to clear it.

## Who you are

**Vell Ostrand**, hired for one night rotation because the last warden walked off at Hask Siding. Vell does not fight
anything; Vell *runs the shift*. The want is procedural: walk the manifest from Hask Siding to Coldmouth Gate before the
freight window closes at the last bell. No crew, no combat training — a ledger, a wrist clock and the radio, against
four yards and ninety minutes of night. Not a mystery and not a home: a working route, staffed by four people who
each want something off the schedule.

## The signature mechanic

**The Shift Ledger.** Encounter rhythm is the whole system, and the player drives it from the outside. Three levers,
always on the ledger:

- **Filing.** File a *contact* at a junction and take the next interruption deliberately. This chooses *when* you are
  interrupted, and costs the only thing that matters: minutes off the window.
- **Cadence.** Between filings the ledger shows the *next* interruption the route will produce on its own, with a
  countdown. **Answer it on the radio** in a short window and it clears without being entered. This chooses *how often*
  you actually fight.
- **Line.** Inside a contact, commands resolve on a beat; chaining the **same line** — the running road, the standing
  yard, the book — resolves faster than hopping between. This chooses *how fast* one resolves.

What is new: the clock is the schedule, not a battle timer. It never runs while you pick a command, so the pressure is
administrative rather than twitchy, and every decision is a budgeting question about a future you can read in advance.

## 30-60 minute slice

One night, four yards, one manifest. Vell accepts the ledger at Hask Siding and the window prints; two harmless
contacts teach the three levers. Then the route starts producing contacts on its own and Vell begins spending —
answering some, filing others, chaining inside them. The climax is the washout on the causeway: a contact that
clears in a minute if Vell chains well and eats most of the window if Vell does not, beside the choice to abandon the
manifest and run. First ending beat: the gate, the last bell, a scored handover.

## Why players would love it

Rank 2's evidence is about pacing, and it cuts both ways. Breath of Fire's pacing is praised on exactly the terms this
pitch is built on — fast, skippable, infrequent:
http://www.honestgamers.com/606/snes/breath-of-fire/review.html

And praise for a *new rhythm* rather than merely a faster one is the target here:
https://goombastomp.com/final-fantasy-4-retrospective/

## What players might criticize

- **Clock pressure on command choice.** The ledger clock is paused for the whole contact, so commands are never timed,
  and each cost is printed on the sheet *before* you file it. The choice is "is this worth eleven minutes", not "pick
  now".
- **One command that covers most enemies.** Every archetype has a declared pair of counters and a blind spot: the brake
  ends a derail in four seconds and does nothing to an inspector; the book comparison clears an inspector and cannot
  touch a washout.
- **Frequency and friction.** Every contact has a hard, printed cost, and the slice ships a **hands-off dispatch**
  toggle — Vell clears contacts on the standing line without choosing, and the route plays itself at a slower, duller
  pace. The escape valve, turned by the player.
- **Random encounters interrupting the memorable parts.** There are none: nothing fires that is not on the ledger, and
  the ledger is on screen.

## VEFR feasibility

Judged only against `research/A2-feasibility.md`.

**BUILT.** The four yards are phases, moved freely and for free on the rail
(`web/player/parts/250-phase-rail.js:10`), and a phase change fires the pack's rules with the new phase as payload
(`web/player/parts/250-phase-rail.js:18`) — the "yardmaster who only radioes in on the Windshift" trick. Each crew
member has one written line per phase, required by the validator (`src/vefr/maplab.py:3605`) and read at the phase you
stand in (`web/player/parts/480-town-input-and-turns.js:1407`), with the phase tone pushed into the model prompt
(`web/player/parts/480-town-input-and-turns.js:1410`). Per-phase water is authorable and drawn
(`web/player/parts/480-town-input-and-turns.js:183`).

**PACK-ONLY FALLBACK (zero engine change).** Per-phase water levels and lines, per-phase rumors baked into the pool
(`src/vefr/pool.py:72`), and a resident who only speaks at night via the `phase-changes` payload rule
(`src/vefr/maplab.py:1001`) whose `say` action puts words in their mouth unprompted
(`web/player/parts/320-pack-rules.js:66`).

**PARTIAL.** Rule `once` defaults to true (`web/player/parts/445-rules-engine.js:368`), so a contact that must re-fire
each cycle needs `"once": false` written explicitly. Phase-seed coverage binds only first-region speakers
(`src/vefr/maplab.py:3598`), so the slice keeps its cast in one region on purpose. Phase lives in memory only
(`web/player/parts/060-minimal-state.js:3`), so a reload returns Vell to dusk.

**MISSING, and the pitch leans on two of them.** No turn system (`src/vefr/combat.py:21`), so contact resolution is
hand-authored rather than simulated — Line-chaining is content, not a rule engine. And no wait or rest verb
(`web/player/parts/076-keybinds.js:60`), with the phase jump unconditional and free
(`web/player/parts/250-phase-rail.js:10`), so **the schedule cannot charge Vell anything**; minutes come off an
author-tracked counter. Availability is MISSING too: a yardmaster who "isn't there" still answers every talk
(`web/player/parts/480-town-input-and-turns.js:1361`) and rules cannot hide anyone
(`web/player/parts/510-rules-closure-surfaces.js:73`), so Vell cannot refuse a conversation.

## Scope and risks

What the `## The 30-60 minute slice` above costs: one world, four phases, one region, six speaking residents at four
seeds each, five authored contact archetypes, four yard maps and a ledger panel — pack data plus the existing player
shell. **No engine change is required as scoped.**

Three risks. The pressure is voluntary: time is free and unconditional (`web/player/parts/250-phase-rail.js:10`), so a
player can spam the rail and skip the game — the window must be a pack-side counter with the ending beat gated on it
by flag. The missing turn system means Line chaining cannot generalise past five hand-built contacts: the slice proves
the idea, not a system. And the slice is single-sitting by accident (`web/player/parts/060-minimal-state.js:3`), which
suits 30-60 minutes but needs work before this has saves.

## Status

**MOCKUP.** This is a pitch, not canon. Nothing here — the title, the yard names, Vell Ostrand, the Shift Ledger — is
approved design until Rylee picks one of the three M0 pitches. No playtest has been run and none is claimed.