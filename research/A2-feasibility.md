# A2 feasibility - "time of day changes who will talk to you and what they say"

Pinned checkout SHA: `635e974d2738897e7a93a7267b2b59d09b3a3358`

Every citation below was opened at the line shown and read in surrounding context
at that SHA. Where a lead from an earlier area study did not hold up, the note
files say so and the corrected line is used.

---

## 1. The mechanic, restated

Residents keep a daily schedule: at some hours a resident is asleep and will not
answer you, at others a resident is the one person awake, and what every resident
says to you changes with the hour; the player moves time by waiting or resting.

Two independent claims are hidden in that sentence — *who is available* and *what
is said* — plus a third, *how time is spent*. They have different verdicts.

---

## 2. Merged findings

### 2a. Time state

- `src/vefr/world.py:790` `missing = [k for k in REQUIRED_FLAT if k not in config]` — BUILT — the *flat-shape* branch refuses any flat world.json without `phases`, so a flat pack gets a named phase axis before anything else runs.
- `src/vefr/world.py:762` `if acts_dir.is_dir():` — MISSING — the acts shape is tested first and never falls through to the flat check, so the shipped sample world and every modern pack skip that friendly refusal entirely.
- `src/vefr/world.py:803` `"phases": config["phases"],` — MISSING — the acts shape reaches a bare dict subscript here, so an acts pack with no `phases` raises `KeyError`, not the named `PackError` a pack author would be told to fix.
- `src/vefr/world.py:578` `def _load_act(act_dir: Path) -> dict:` — MISSING — `_load_act` requires only id, title and regions, so no phase axis is checked anywhere on the path the sample pack actually takes.
- `src/vefr/maplab.py:3605` `if set(s.get('seeds', {})) != set(w['phases']):` — BUILT — for a speaker it reaches, the validator compares seed keys against the pack's phase keys and rejects the pack when they differ.
- `src/vefr/maplab.py:3598` `if first_region and s.get('region', first_region) != first_region:` — PARTIAL — any speaker whose `region` differs from the first region's is skipped outright, so the seed-coverage rule above binds only the first region's speakers.
- `src/vefr/maplab.py:133` `all_speakers = act.get('speakers', {})` — BUILT — act unification carries *every* act's speakers onto the first act's world, and `src/vefr/maplab.py:164` stamps that world with a single `_region`, so the filter at `:3598` is exactly what bounds the seed check to first-region speakers of the first act.
- `src/vefr/maplab.py:3606` `errors.append(f'speaker {s["name"]} seeds do not cover every phase')` — BUILT — this is the sentence `vefr check` prints for that mismatch, so phase coverage of a speaker's seeds is enforced in code rather than merely documented — for the speakers that loop reaches.
- `web/player/parts/090-first-run-setup-vs-play.js:54` `STATE.set({ world: window.VEFR_WORLD, phase: Object.keys(window.VEFR_WORLD.phases)[0] });` — BUILT — entering play sets the current phase to the pack's first phase key.
- `web/player/parts/250-phase-rail.js:10` `STATE.set({ phase: k });` — BUILT — the rail button assigns the clicked phase straight into state, with no cost, delay or check.
- `web/player/parts/250-phase-rail.js:18` `fireRule('phase-changes', { to: k });` — BUILT — the same click fires the pack's rules with the new phase as the payload.
- `web/player/parts/480-town-input-and-turns.js:183` `var water = (town.water_by_phase || {})[ph];` — BUILT — the town draw reads the water level of the current phase once per frame.
- `web/player/parts/480-town-input-and-turns.js:283` `if (water === 'high') {` — BUILT — only the literal string `high` paints the flood overlay, so any other authored value silently means "not flooded".
- `web/town.js:53` `watchR = (W.watch.r_by_phase && W.watch.r_by_phase[phase()])` — BUILT — this is the only reader of `r_by_phase` anywhere in `web/`: in the standalone town shell the fog/watch radius follows the phase, with the tower radius as fallback.
- `web/player/parts/450-fog-of-war.js:148` `return fogOn && !explored[x + ',' + y];` — MISSING — in the woven player fog is the explored-tile toggle: a tile is hidden only until it has been walked, with no phase test in the path.
- `web/player/parts/400-setup-town-open.js:35` `watch: r.watch || {},` — MISSING — the baked region contract carries the `watch` table, and its `r_by_phase` with it, into the town object, but no woven-player code reads that field.
- `web/town.js:65` `if (W.water_by_phase && W.water_by_phase[phase()] === 'high') {` — BUILT — the standalone town shell repeats the same `=== 'high'` test for its own flood set, confirming `high` is the only value with behaviour anywhere.
- `web/player/parts/400-setup-town-open.js:36` `water_by_phase: r.water_by_phase || {},` — BUILT — the region contract's water table is passed into the town object unchanged, so an author's phase keys survive the bake.
- `web/player/parts/220-growth.js:202` `if (phases.indexOf(STATE.get().phase) <= 0) {` — BUILT — the encounter prompt is hidden while the current phase is the first or earlier in the order, and shown after; this is positional, not key-based.
- `web/player/parts/260-whisper.js:26` `var tone = window.VEFR_WORLD.phases[ph] || '';` — BUILT — the Listen verb reads the current phase's tone text for its model prompt.
- `src/vefr/pool.py:72` `f"rumor:{ph}", samples,` — BUILT — the baked pool keeps one rumor bucket per phase key.
- `web/player/parts/480-town-input-and-turns.js:1352` `for (var key in speakers) {` — MISSING — the nearest-speaker search walks every speaker in the region with no phase test, so a resident who should be asleep is still the nearest candidate at 3am.
- `web/player/parts/480-town-input-and-turns.js:1361` `if (!nearest || nearest.dist > 2) {` — BUILT — the only gate on talking is Manhattan distance of 2 tiles; nothing about the phase enters this decision.
- `web/player/parts/480-town-input-and-turns.js:861` `if (!brainConfigured() && !hasOfflineLine(key, s)) return;` — BUILT — a resident leaves the Interact list only when there is no model configured and no line to speak, never because of the time of day.
- `web/player/parts/060-minimal-state.js:3` `var s = { phase: null, world: null };` — PARTIAL — the current phase is a field of an in-memory object with no store write in this module, so a page reload starts the player back at the pack's first phase.
- `web/player/parts/076-keybinds.js:60` `var KEYBIND_ACTIONS = [` — MISSING — the closed list of bindable actions holds movement, use, whisper, bag, explore, fog, pages, journal and menu; no wait, rest or sleep verb exists to bind.
- `web/player/parts/520-the-kitchen.js:215` `document.getElementById('k-sleep').addEventListener('click', function () {` — MISSING — `k-sleep` is a button on the desk's paper-kitchen minigame that clears that minigame's ticket queue; it never touches the world phase.
- `src/vefr/combat.py:21` `engine doesn't have a turn system; the action just lives in` — MISSING — this is docstring prose stating the absence of a turn system; no code at that line advances anything.
- `src/vefr/main.py:508` `sessions.write_meta(` — MISSING — the session-fork handler writes parent/fork metadata; no phase is read or written here, so the server holds no clock.
- `src/vefr/achievements.py:183` `ok = h1 <= hour <= h2` — MISSING — this compares a wall-clock hour of day for sticker achievements and has nothing to do with the pack's phases.

### 2b. Speakers and dialogue

- `worlds/sample-world/acts/act-1/world.json:12` `"dusk": "The stone holds the day's warmth. Sit a while.",` — BUILT — the shipped sample act keys a speaker's seeds by phase name, one string per phase.
- `worlds/sample-world/world.json:8` `"dusk": "The day settles. The tone is quiet and watchful.",` — BUILT — the sample pack declares a phase key whose value is a tone sentence, the text the player puts into the model prompt and shows on the rail button.
- `src/vefr/cli.py:2844` `'seeds': spec.get('seeds', {}),` — BUILT — the weave copies each speaker's seed map verbatim into the baked player, so phase keys survive from `world.json` to the shipped file.
- `web/player/parts/480-town-input-and-turns.js:1407` `var seed = (nearest.spec.seeds || {})[ph] || '';` — BUILT — Talk reads the seed belonging to the phase the player is standing in, not the speaker's first seed.
- `web/player/parts/480-town-input-and-turns.js:1409` `var tone = world.phases[ph] || '';` — BUILT — the same function reads the phase's tone text.
- `web/player/parts/480-town-input-and-turns.js:1410` `var system = voice + '\n\nCURRENT PHASE: ' + tone;` — BUILT — the phase tone is concatenated into the system prompt actually posted to the model, so a configured brain is told the time of day.
- `web/player/parts/480-town-input-and-turns.js:1427` `}).catch(function () {` — PARTIAL — everything after this point is the offline fallback chain (pool, composer, fragments, then seed); it is where the phase-keyed line is spoken when no model answers.
- `web/player/parts/480-town-input-and-turns.js:1386` `if (typeof own === 'string' && own.trim()) return own;` — MISSING — the offline selector accepts only a plain string seed, so ADR 0005's proposed list-of-entries seed shape would be ignored here even if a validator accepted it.
- `src/vefr/pool.py:83` `f"npc:{ph}:{key}", samples,` — BUILT — the baked line pool is keyed per phase per speaker, so an offline player drawing from the pool also gets a phase-appropriate line.
- `src/vefr/npc.py:104` `line=spec["seeds"].get(phase, next(iter(spec["seeds"].values()))),` — BUILT — the server's offline generator picks the seed for the requested phase and falls back to the first seed when the phase is absent.
- `web/board.js:156` `function firstSeed(speaker, world, r) {` — MISSING — the board shell (served by `web/index.html:1866`) quotes the seed of the pack's first phase and falls back to the first truthy seed, so what a resident is shown saying there never follows the hour.
- `web/js/rooms/characters.js:190` `function firstSeed(seeds, phase) {` — MISSING — the Folks room's preview quotes `phases[0]`, and both call sites pass `phases[0]` (`:109`, `:251`), so that surface never follows the hour either; it ships in `web/app.html:130`.
- `src/vefr/main.py:88` `phase: str = "whispers"` — PARTIAL — the NPC request model carries a phase field with that default; it selects which line to speak but never decides whether the speaker is present.
- `src/vefr/main.py:201` `journal.log("npc_line", sid=session, phase=req.phase, speaker=spoken.speaker, line=spoken.line)` — BUILT — every served NPC line is journalled with the phase it was said in, so phase-keyed speech is auditable after the fact.
- `src/vefr/shapes.py:1660` `'phase-changes': (Key('to', 'ref', ref='phase'),),` — BUILT — the shared event table declares a phase-change event whose only payload is the phase being entered, as a ref the validator resolves.
- `src/vefr/maplab.py:1001` `if kind == 'phase':` — BUILT — a ref of kind `phase` in a rule payload is checked against the pack's declared phase keys, so a rule *payload* naming a phase is validated rather than ignored.
- `src/vefr/maplab.py:836` `RULE_CONDITION_KEYS = ('has', 'flag', 'is', 'believes', 'not-believes',` — MISSING — the closed set of conditions a rule may name contains no phase key, so no rule can say "while it is night".
- `web/player/parts/445-rules-engine.js:36` `'phase-changes': { keys: ['to'], target: 'to' },` — BUILT — the player's JS twin marks `to` as the event's target, the field an `on` match would compare against if the validator allowed one.
- `web/player/parts/445-rules-engine.js:347` `if ('on' in rule && target && data[target] !== rule.on) return null;` — BUILT — the JS twin does match a rule's `on` against the phase just entered, but no shipped rule can carry that field, because the validator refuses an `on` that names a phase.
- `src/vefr/maplab.py:2610` `elif on not in known['things']:` — MISSING — the rule validator refuses any rule whose `on` is not a known thing, and against a copy of the sample pack `vefr check` printed `rule 'night-line' 'on' names unknown thing 'dawn'`.
- `src/vefr/maplab.py:952` `'things': items | people | places | pois | book_ids | enemies,` — MISSING — that union is what `known['things']` is, and it excludes `phases`, which is why a phase name is not a legal `on` value.
- `web/player/parts/445-rules-engine.js:368` `once: 'once' in rule ? rule.once : true,` — PARTIAL — `once` defaults to true, so even the event-payload lever fires only on the first entry into that phase per save unless the author writes `"once": false`.
- `web/town.js:293` `b.addEventListener('click', function () { STATE.setPhase(p); });` — MISSING — the standalone shell's rail moves time and calls no rule, because no rules engine is loaded in `web/town.js`.
- `web/index.html:2512` `if (b) STATE.setPhase(b.dataset.phase);` — MISSING — the served shell's rail likewise only assigns the phase, and with `web/board.js` no `fireRule`/`RULES_ENGINE` exists there either, so outside the woven player a phase change notifies nothing.
- `web/player/parts/320-pack-rules.js:66` `if (name) showSpeech(name, v.line || '', '');` — BUILT — a rule's `say` action naming a speaker puts that line in the speech box, so a rule fired at dusk can put words in a resident's mouth unprompted.
- `web/player/parts/320-pack-rules.js:45` `RULES_STATE.where[k] = rg;` — PARTIAL — each speaker's location is baked from its declared region once, and the code above it states people do not move in this player, so a resident is never somewhere else at another hour.
- `web/player/parts/510-rules-closure-surfaces.js:72` `window.VEFR_RULES_SURFACE = function (verb, id) {` — BUILT — this is the one function a rule's show/hide/reveal reaches.
- `web/player/parts/510-rules-closure-surfaces.js:73` `if (!itemCatalog()[id]) return;` — MISSING — the surface returns immediately for anything that is not an item, so a rule naming a sleeping resident is skipped silently and cannot remove them from the town.
- `src/vefr/maplab.py:761` `for key, spec in speakers.items():` — BUILT — this is the speaker loop of `identify_errors()`, whose body reads the optional `identify` field and nothing else; the point of citing it is the absence around it — no closed key set is applied to a speaker anywhere in the validator, so `available_in` is carried without complaint and then ignored by the player, while reach and seed coverage are checked far away in `validate()` at `src/vefr/maplab.py:3599`.
- `docs/adr/0005-dialogue-state.md:7` `Proposed` — MISSING — the flag-conditioned seed design is recorded with this status, i.e. it is not built.
- `tests/test_talk_offline.py:83` `assert CAT_DAWN not in json.dumps(log), "a dawn line was said at dusk"` — PARTIAL — this harness never switches phase, so it pins selection at dusk only; it is *not* the only test touching time-of-day selection.
- `tests/test_npc.py:39` `line = generate_line("dawn")` — BUILT — a separate server-side test asks the offline generator for the dawn seed by name and asserts the dawn text came back with `source == "seed"`.
- `tests/fixtures/events_play_harness.mjs:144` `const dawn = document.querySelector('#phase button[data-phase="dawn"]');` — BUILT — the browser harness (driven by `tests/test_events_play.py`) clicks the rail's dawn button and waits for the pack's `phase-changes` rule to fire, so a phase transition is exercised end to end.
- `tests/fixtures/make_events_pack.py:56` `{"id": "the-watch-turned", "when": {"phase-changes": {"to": "dawn"}},` — BUILT — the fixture pack's own rule is gated on a named phase through the event *payload*, which is the phase-aware lever a pack can actually ship.
- `src/vefr/locks.py:28` `the flag, so they are treated as always open and never reported. No` — PARTIAL — the reachability checker treats every flag-gated lock as permanently open, so a schedule expressed as flags would never be reported by `vefr check` as unreachable.
- `src/vefr/chat.py:468` `phases, water_by_phase, watch.r_by_phase, every speaker's seeds."""` — BUILT — the storyteller's phase-rename migrates the phase table, water table, watch table and every speaker's seed keys together, so the mechanic survives a rename.
- `docs/guides/rulesets.md:1130` `"seeds": {"dusk": "...", "dawn": "..."}}` — BUILT — the line sits inside an unrelated shopkeeper example and states no coverage rule; all it shows is that a shopkeeper's speaker record carries a `seeds` map keyed by phase.
- `docs/adr/0005-dialogue-state.md:12` `string per phase, and the validator requires every phase covered` — BUILT — the one-string-per-phase contract is stated in prose here, and the rule it names is the one enforced at `src/vefr/maplab.py:3605`.
- `src/vefr/grammar.py:6` `"grammars": {` — PARTIAL — grammars are a flat map from a rule name to word lists with no phase in the shape, so they cannot vary what a resident says by time on their own.
- `src/vefr/blueprint.py:73` `FIELD_ORDER = ("id", "name", "sprite", "at", "hp", "atk", "xp", "sight", "drops")` — MISSING — this tuple is the emission key order for a blueprint record, not a gate: an extra field is not refused, it is silently dropped at `src/vefr/blueprint.py:1064`. The real reason blueprints cannot express hours is structural — the module expands only enemy records, things and places and never writes a `speakers` key at all.
- `src/vefr/schema_grammar.py:1` `"""JSON Schema to GBNF grammar converter for llama.cpp-compatible backends.` — MISSING — despite the name, this module converts JSON Schema into GBNF for the local model server; it is not a pack authoring surface for seeds, phases or speakers.
- `docs/features.json:2` `"version": 1,` — MISSING — the feature catalogue's version line; the file contains no occurrence of the word `phase` at all, so no phase or schedule behaviour is catalogued for packs to discover.

---

## 3. Verdict per capability

| # | Capability | Verdict | Note |
|---|---|---|---|
| 1 | A pack declares named phases of day | **BUILT** | `src/vefr/world.py:790` refuses a *flat* world.json without `phases`; an acts-shaped pack is branched off at `src/vefr/world.py:762` and never reaches that refusal (it would raise `KeyError` at `src/vefr/world.py:803`). |
| 2 | Time is moved by the player | **BUILT** | `web/player/parts/250-phase-rail.js:10` — a rail button writes the chosen phase into state instantly and for free. |
| 3 | Time is moved by *waiting or resting*, at a cost | **MISSING** | `web/player/parts/076-keybinds.js:60` — the closed verb list has no wait, rest or sleep action; there is nothing to make waiting mean. |
| 4 | The phase change notifies the pack's rules | **BUILT** | In the woven player `web/player/parts/250-phase-rail.js:18` fires `phase-changes` with the new phase. Outside it nothing fires: the standalone rails (`web/town.js:293`, `web/index.html:2512`) only call `setPhase`, and no rules engine is loaded in those shells. |
| 5 | What a resident *says* changes with the phase | **BUILT** | In the woven player `web/player/parts/480-town-input-and-turns.js:1407` selects `seeds[phase]`; the server route `src/vefr/npc.py:104` does the same and `src/vefr/pool.py:83` keys the baked pool per phase. The board shell (`web/board.js:156`) and the Folks room (`web/js/rooms/characters.js:190`) always quote `phases[0]`. |
| 6 | The phase tone reaches the model | **BUILT** | `web/player/parts/480-town-input-and-turns.js:1410` puts the phase tone in the system prompt actually posted. |
| 7 | A pack author must write a line for every phase | **BUILT** | `src/vefr/maplab.py:3605` rejects any speaker whose seed keys do not equal the pack's phases — but only for first-region speakers of the first act; the rest are skipped at `src/vefr/maplab.py:3598`. |
| 8 | Whether a resident is *available* changes with the phase | **MISSING** | `web/player/parts/480-town-input-and-turns.js:1352` searches all speakers, `web/player/parts/480-town-input-and-turns.js:1361` gates only on distance 2, `web/player/parts/480-town-input-and-turns.js:861` filters the Interact list only by "has any line". |
| 9 | A rule can say "only at night" | **MISSING** | `src/vefr/maplab.py:836` — `RULE_CONDITION_KEYS` has no phase key, and the `on:` match cannot stand in for it: `src/vefr/maplab.py:2610` refuses an `on` that names a phase, because phases are excluded from `known['things']` at `src/vefr/maplab.py:952`. The only phase-aware lever a pack can ship is the payload `"when": {"phase-changes": {"to": "<phase>"}}` (`src/vefr/maplab.py:1001`), and it fires on the transition — once per save by default (`web/player/parts/445-rules-engine.js:368`) — never on the standing state. |
| 10 | A rule can hide a resident who is asleep | **MISSING** | `web/player/parts/510-rules-closure-surfaces.js:73` — show/hide/reveal returns for anything that is not an item. |
| 11 | Line choice can react to a flag | **MISSING** | `docs/adr/0005-dialogue-state.md:7` is `Proposed`; `web/player/parts/480-town-input-and-turns.js:1386` only accepts a plain string seed. |
| 12 | Phase-dependent world look (water, fog) | **BUILT** | Water is per-phase on both surfaces: `web/player/parts/480-town-input-and-turns.js:183` and `web/town.js:65`. Fog per phase exists only in the standalone town shell (`web/town.js:53`); in the woven player fog is the explored-tile toggle (`web/player/parts/450-fog-of-war.js:148`). |
| 13 | Time survives a reload | **MISSING** | `web/player/parts/060-minimal-state.js:3` — phase is a plain in-memory field; a reload returns the player to the first phase. |

---

## 4. What the mechanic can and cannot do today

It can do this, today, with no engine change:

- The player moves between named times of day, freely and instantly, on a rail.
- In the woven player and on the server route, every resident answers whenever you
  stand next to them, at any hour, and says the line written for the current
  phase. Offline, with a baked pool, or through a model, the line and the tone
  both follow the phase. The board shell and the Folks room do not: both quote
  the pack's *first* phase, so what a resident is shown saying there never
  follows the hour.
- In the woven player a pack rule can speak a resident's line unprompted the
  moment the player enters a named phase, so a "night only" character can
  interrupt you at dusk. It is keyed on the event payload
  `{"phase-changes": {"to": ...}}`, it fires once per save unless the author
  writes `"once": false`, and outside the woven player the rails fire no rules at
  all.
- Water changes with the phase on both the woven player and the standalone town
  shell. The fog/watch radius follows the phase only in the standalone town
  shell; in the woven player fog is an explored-tile toggle with no phase in it.

It cannot do this, today, at all:

- It cannot stop a resident talking to you. There is no asleep state, no
  availability list, no per-phase position. Everyone is everywhere at every hour.
- It cannot make a line depend on anything but the phase — not a flag, not an
  item, not a place (ADR 0005 is still `Proposed`).
- It cannot let a rule say "only while it is night" and *check* that on every
  turn. The `on:` event match that would read as a phase gate is refused by the
  validator, so only the transition carries phase, and only in the woven player.
- It cannot let the player *wait* or *rest* to move time, because no such verb
  exists and moving time is free, so "waiting" has no meaning to cost.
- It cannot persist the hour across a reload.

The honest summary: **half the mechanic is built and the more distinctive half
is not.** The say-side is mature — pack contract, validator, bake, player, pool,
server, journal. The availability side has no representation at any layer, in the
pack contract, the validator, the player, or the rules vocabulary.

---

## 5. SMALLEST ENGINE CHANGE LIST

Smallest first. Each item names the citation that shows it is needed.

1. **Phase as a rule condition key.** Required.
   Needed because `src/vefr/maplab.py:836` (`RULE_CONDITION_KEYS`) has no phase
   key, so no rule can express "while it is night". Add a condition key plus its
   validator branch next to `src/vefr/maplab.py:1001`, and its twin in the JS
   engine beside `web/player/parts/445-rules-engine.js:36`.
   This is the smallest change that makes schedules *expressible*.

2. **Speaker availability by phase.** Required.
   Needed because `web/player/parts/480-town-input-and-turns.js:1352` searches
   every speaker and `web/player/parts/480-town-input-and-turns.js:861` lists
   every resident: add an optional per-speaker phase list to the contract, bake
   it beside `src/vefr/cli.py:2844`, and consult it in both places. The validator
   already tolerates unknown speaker keys
   (`src/vefr/maplab.py:761`), so no key-set change is forced; a new
   "resident available in phase X that the pack never declares" error should be
   added beside `src/vefr/maplab.py:3605`, and that loop widened past its
   first-region skip at `src/vefr/maplab.py:3598` so it reaches every speaker.

3. **A wait/rest verb that advances one phase.** Required.
   Needed because `web/player/parts/076-keybinds.js:60` is a closed action list
   with no time verb, and `web/player/parts/250-phase-rail.js:10` makes the jump
   free. Add the action, a handler that steps the rail one phase along, and
   whatever cost the pack wants to charge.

4. **Persist the phase.** Optional for the mechanic, required for "the player
   waited an hour and reloaded".
   Needed because `web/player/parts/060-minimal-state.js:3` keeps phase in memory
   only: the two writers of phase (`web/player/parts/090-first-run-setup-vs-play.js:54`
   and `web/player/parts/250-phase-rail.js:10`) both go through this object and
   neither writes it to the player's store.

5. **Flag-conditioned seeds (ADR 0005).** Optional.
   Needed because `docs/adr/0005-dialogue-state.md:7` is `Proposed` and
   `web/player/parts/480-town-input-and-turns.js:1386` requires a string. Nice for
   "he said the thing before the fire, and the other thing after", not required
   by the time-of-day mechanic itself.

6. **A closed set of legal `water_by_phase` values.** Optional.
   Needed because `src/vefr/maplab.py:3612` checks key coverage only while
   `web/player/parts/480-town-input-and-turns.js:283` acts on the literal string
   `high`, so a typo is silent.

---

## 6. PACK-ONLY FALLBACK

What a pack author can ship today with zero engine change:

- **Phases as times of day.** Declare two or more phases in `world.json`
  (`worlds/sample-world/world.json:8`), write tone sentences for each.
- **Different lines per hour.** Write one seed per phase per resident; the
  validator requires them all for first-region speakers
  (`src/vefr/maplab.py:3605`, bounded by the skip at
  `src/vefr/maplab.py:3598`) and the woven player picks them
  (`web/player/parts/480-town-input-and-turns.js:1407`), offline
  (`src/vefr/npc.py:104`) and online
  (`web/player/parts/480-town-input-and-turns.js:1410`).
- **A resident who only speaks at night.** A rule whose event payload is
  `{"phase-changes": {"to": "<phase>"}}`
  (`src/vefr/maplab.py:1001`) whose `say` action names that resident
  (`web/player/parts/320-pack-rules.js:66`) — they speak in their own voice when
  the player enters that phase, unprompted. Three limits an author must be told
  about: it fires only on the *transition* into the phase, never on the standing
  state; `once` defaults to true (`web/player/parts/445-rules-engine.js:368`), so
  without `"once": false` it happens once per save; and it only works in the
  woven player, because the standalone rails
  (`web/town.js:293`, `web/index.html:2512`) move time without firing any rule.
- **A resident who only speaks at night, gated on a flag.** The same phase
  payload plus a condition reading a declared flag (`src/vefr/maplab.py:836`
  allows `flag`), setting and unsetting the flag from per-phase rules. This works
  and needs no engine change, at the cost of being a workaround.
- **Different rumors and water per hour** (`src/vefr/pool.py:72`,
  `web/player/parts/480-town-input-and-turns.js:183`, `web/town.js:65`), and a
  fog radius per hour **only in the standalone town shell**
  (`web/town.js:53`).

What the pack surface cannot reach, with no engine change at all:

- **Refusing a conversation.** A resident who is "asleep" still answers every
  Talk (`web/player/parts/480-town-input-and-turns.js:1361`).
- **Removing a resident from the Interact list by hour**
  (`web/player/parts/480-town-input-and-turns.js:861`).
- **Hiding a resident through a rule** (`web/player/parts/510-rules-closure-surfaces.js:73`
  — show/hide/reveal is items only).
- **Moving a resident between places by hour** (`web/player/parts/320-pack-rules.js:45`
  — locations are baked once; `is-in` reads the bake).
- **Making the player pay for time.** There is no verb to charge
  (`web/player/parts/076-keybinds.js:60`) and the jump is unconditional
  (`web/player/parts/250-phase-rail.js:10`).
- **Depending on the hour in a rule condition**, only on the *transition*,
  through the event payload (`src/vefr/maplab.py:1001`), never on the standing
  state; the `on:` field a rule would need for the latter is refused outright by
  `src/vefr/maplab.py:2610`, which prints `rule '…' 'on' names unknown thing
  '<phase>'` because phases are not in `known['things']`
  (`src/vefr/maplab.py:952`).
- **Any of the above outside the woven player.** The standalone shells move time
  but run no rules at all.
- **Keeping the hour across a reload** (`web/player/parts/060-minimal-state.js:3`).

Trap to warn pack authors about: because the speaker validator has no closed key
set anywhere (`src/vefr/maplab.py:761` reads only `identify`; reach and seed
coverage are checked separately in `validate()` at
`src/vefr/maplab.py:3599`), an author can write `"available_in": ["night"]`
into a speaker and `vefr check` will pass it. Nothing reads it. And because
`src/vefr/locks.py:28` treats every flag-gated lock as permanently open, a
flag-driven schedule is never reported as reachable or unreachable by the checker.

---

## 7. NOT VERIFIED HERE

Exactly what needs host verification before this becomes a plan:

1. **Resolve every citation in this file and in the three note files at
   `635e974d2738897e7a93a7267b2b59d09b3a3358`.** An adversarial pass *has* now
   run over this file: a second reader checked all 54 citations, confirmed 45
   and 9 forced a correction, and every bullet's anchor was re-resolved with
   `sed -n` after the edits. Still outstanding: the bullets were checked in this
   working tree, not against a clean checkout, and the three note files the
   earlier area studies left behind are not in this checkout at all.
2. **Cross-family semantic check of every BUILT row.** The check performed here
   was: does the cited code, read in context, perform the behaviour for *this*
   mechanic. That is not the same as: does it do so in every player, every
   surface, every bake path. The adversarial pass corrected the two worst cases
   of this (the `on`-names-a-phase lever, and seed/fog selection read across
   surfaces), but a full cross-family pass has not been done. Specifically still
   worth a second reader:
   - `web/player/parts/480-town-input-and-turns.js:1407` — read in the woven
     player only. The board shell and the Folks room were then found to quote
     `phases[0]` instead; whether any *further* served surface was missed is not
     established.
   - `web/player/parts/250-phase-rail.js:18` — the woven rail was read. The two
     standalone rails were then found to fire no rules at all; whether a fourth
     rail exists was not enumerated.
   - `src/vefr/maplab.py:836` — read as the closed condition key set for rules.
     Whether any other rule dialect (album stickers, sections, features) carries
     a phase condition was not searched exhaustively.
   - `web/player/parts/510-rules-closure-surfaces.js:73` — read as the only
     show/hide surface; other surfaces reachable from a rule action were not
     enumerated.
3. **No playtest, benchmark or build was run.** No claim here rests on observed
   play. `tests/test_talk_offline.py:83`, `tests/test_npc.py:39` and
   `tests/fixtures/events_play_harness.mjs:144` are read as evidence of intent and
   of what is asserted, not as passing runs at this SHA. The one thing actually
   executed for this revision was the validator itself, against a `/tmp` copy of
   the sample pack, to confirm the `on`-names-a-phase refusal.
4. **The three corrected lead lines** (`400-setup-town-open.js` 35→36,
   `npc.py` 105→104, `510-rules-closure-surfaces.js` 69→72) should be
   re-checked against whatever the earlier area studies said, since their note
   files did not survive into this checkout.
