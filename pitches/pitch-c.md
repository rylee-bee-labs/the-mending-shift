# Pitch C — M0 candidate

## Title

**Plain Speaking** (working title; set in the invented salt town of Saltmere)

## Hook

Everyone in Saltmere tells you out loud, in plain words, exactly *why* they are lying to you — so the only thing left
to solve is what is actually true. You walk four hours of a small town's day with a grey ledger under your arm, and a
notary who interrupts to announce the rule the game just used.

## Who you are

Wren Alday, tide-clerk of Saltmere. The harbourmaster vanished; every resident signed a statement about the night of
the storm, and the charter makes you keeper of the record. Before the season ends you want a ledger the clerk before
you would have signed — which means naming who is lying, or writing "nobody", and living with which the town survives.

## The signature mechanic

**The game states its own deepest rule every time it fires, in the fiction, out loud.**

The deep interaction is *someone tells you their motive*. Whenever a resident withholds or contradicts you, the game
announces the motive in-fiction before you answer: Ferrow lies about the ferry because he fears Odile, not because he
distrusts you. Over that sits **Pell Rundle, the notary**, who says the *rule* that produced what just happened, flatly:
*"Ferrow gave you the noon line. The rule is that nobody here changes a story — they only stop telling it."*

What is new: legibility is not a tutorial but the delivery mechanism for the mystery. The game is **motive-honest and
fact-secret** — it always tells you *why* someone acted, never *what happened* — so deduction of hidden motives is
never the puzzle; collection of hidden facts is, and legibility is what makes collecting facts the correct play.

## The 30-60 minute slice

One region, Quay Street; six residents; four hours — dawn, noon, dusk, small hours.

- **Dawn (0–10).** Every resident states their motive when pressed. Pell gives the first rule: *a thing said twice at
  the same hour is a rule.*
- **Noon (10–22).** The statements. Ask about the others, get motive-stated deflection, not lies. The Grey Book accepts
  only what was said at an hour you can name. First conflict: two ferry accounts that cannot both be true at one hour.
- **Dusk (22–38).** Ferrow and Halla change their line; Pell announces the second rule — *nobody changes a story, they
  only stop telling one* — and the ledger records who stopped. Odile's dusk line is the hinge: she names the hour.
- **Small hours (38–50).** One confrontation at the ferry office. Name a liar or write "nobody"; three ~150-word
  endings the next morning, told by whoever you spent the day with.
- **50–60.** Replay the day from the ledger screen; every rule-line you heard is readable in one place.

## Why players would love it

The praise in this family is for systems that state what they do: a reverse-design breakdown of Chrono Trigger argues
its enemies split into two functional classes rather than one difficulty curve — a rule the design owns out loud.
http://thegamedesignforum.com/features/reverse_design_CT_9.html

Undertale's developer holds that every monster should feel like an individual; Plain Speaking takes that ambition one
layer down, making every *motive* authored and specific rather than procedural.
https://www.escapistmagazine.com/undertale-dev-every-monster-should-feel-like-an-individual/

And Sabotage Studio's combat breakdown says all combat actions build energy that eventually turn into combo points —
an input-to-output relation stated in one sentence. Plain Speaking's is one sentence too, said aloud every time.
https://blog.playstation.com/2022/07/07/a-closer-look-at-the-turn-based-combat-in-sea-of-stars/

## What players might criticize

- **An interaction that is never explained.** **Decision:** every interaction carries a mandatory authored rule-line, and
  the validator refuses a resident lacking a line for a declared hour (`src/vefr/maplab.py:3605`) — a resident who
  could withhold the rule cannot ship.
- **Damage doubled across the board.** **Decision:** no such route exists here. The one difficulty lever is withheld
  speech: exactly one resident changes between noon and dusk, the ledger names them first, and the change is announced
  rather than silently applied.
- **Mechanics that never develop.** **Decision:** the four hours develop the *same* rule rather than adding abilities —
  its subject moves from *motive* to *contradiction* to *reticence* to *cost*, one new question per hour.
- **Rules the game hides.** **Decision:** no hidden odds and no percentage checks exist. The only check is whether the
  statement you hold was made at an hour you can name, and the ledger always shows that hour and its speaker.

## VEFR feasibility

Grounded only in `research/A2-feasibility.md`.

**BUILT.** Hours are named phases and the rail moves time instantly and free (`web/player/parts/250-phase-rail.js:10`).
What a resident says follows the hour: the woven player reads `seeds[phase]`
(`web/player/parts/480-town-input-and-turns.js:1407`), the offline generator picks the same seed (`src/vefr/npc.py:104`),
the pool is keyed per phase per speaker (`src/vefr/pool.py:83`), the tone reaches the model prompt
(`web/player/parts/480-town-input-and-turns.js:1410`), and the validator refuses a resident missing an hour's line
(`src/vefr/maplab.py:3605`). A rule keyed on the phase-transition payload (`src/vefr/maplab.py:1001`) can put a
resident's authored line in their mouth unprompted (`web/player/parts/320-pack-rules.js:66`) — exactly Pell's
rule-line.

**PACK-ONLY FALLBACK (zero engine change, ships today).** Two levers from A2 section 6: a line per phase per resident,
and a rule that speaks a resident's line on a phase transition. Together they deliver this pitch's whole mechanic.
Three limits must be designed around: it fires only on the *transition* into the hour, never on the standing state;
`once` defaults to true (`web/player/parts/445-rules-engine.js:368`), so every rule-line ships `"once": false`; and it
works only in the woven player, since standalone rails fire nothing (`web/town.js:293`).

**PARTIAL.** The hour is an in-memory field, so a reload returns to the first hour
(`web/player/parts/060-minimal-state.js:3`) — the slice is one sitting. Seed coverage binds only first-region speakers
(`src/vefr/maplab.py:3598`), fine for one region, a trap later. The offline chain falls back
pool→composer→fragment→seed (`web/player/parts/480-town-input-and-turns.js:1427`), so an offline Pell can paraphrase
a rule; rule-lines are authored strings, never pool draws.

**MISSING, and this pitch leans on three.** No asleep state: the nearest-speaker search walks every resident
(`web/player/parts/480-town-input-and-turns.js:1352`) and gates only on distance
(`web/player/parts/480-town-input-and-turns.js:1361`). No phase condition exists in the rules vocabulary
(`src/vefr/maplab.py:836`), and an `on` naming a phase is refused outright (`src/vefr/maplab.py:2610`). No wait or rest
verb (`web/player/parts/076-keybinds.js:60`), so time cannot cost anything. A rule also cannot hide a resident
(`web/player/parts/510-rules-closure-surfaces.js:73`).

## Scope and risks

**Cost:** one region, six residents, four hours, ~120 authored lines, 12 pack rules, one item, three short endings. No
new engine code for the slice as scoped.

**Risks, biggest first.**

1. The pitch's promise is what the engine cannot enforce: with phase-as-condition MISSING, legibility is authoring
   discipline, and only the seed-coverage rule at `src/vefr/maplab.py:3605` catches a forgotten rule-line.
2. Leaning on MISSING availability — "nobody talks at night" cannot be built. Residents instead *say* they aren't
   talking and then talk anyway; if Rylee wants a real asleep state, that is A2 change #2 and it leaves the zero-engine
   path.
3. Leaning on MISSING paid time — if waiting must cost, that is A2 change #3 and the flat rail is a placeholder.
4. Reload loses the hour; the slice is one sitting.
5. Tone risk: a game that explains itself can read as smug. The defence is that Pell is a character with a reason.

## Status

**MOCKUP.** This is pitch C of three, written to be compared against the other two and discarded if Rylee picks
those. Nothing in it is canon. No playtest was run and no score exists; every feasibility claim above is read out of
`research/A2-feasibility.md` and nothing else. Rylee picks one pitch and the other two stop existing.
