# tools

One tool: `play_slice.py`, the M2d driver. It plays a woven pack slice through
every phase of its watch and reports on what played.

## `play_slice.py`

`vefr probe` fires events but cannot advance the watch, so the beats after the
first hour have never been seen playing. This driver opens a woven pack HTML in
headless Chromium at a 390x844 phone viewport and plays it the way a person
would: walk to every place and every resident that the rules for the standing
phase name in `comes-near`, talk where there is something to talk to, and press
Rest to turn the hour.

```sh
uv run vefr weave --pool 2 --pack mending-shift        # -> dist/mending-shift-<date>.html
python3 tools/play_slice.py dist/mending-shift-2026-10-17.html
python3 tools/play_slice.py --plan dist/mending-shift-2026-10-17.html   # no browser
python3 tools/play_slice.py --self-test                                 # no browser
```

It reads `world.json` for the coordinates (`speakers[*].at` and `town.pois`,
whose label is the id a rule's `comes-near` names) and for the phase order. It
**never writes to the pack** - `world.json` is opened for reading and nothing
else in the repo is touched. Everything it writes goes under `--out`
(default `out/play/`):

- `phase-NN-<slug>.png`, one screenshot per phase;
- `lines.txt`, every line the game showed, with the phase and what the driver
  was doing when it appeared;
- `report.md` and `report.json`, the run's report.

**Exit status is 0 only when every phase in `phases` order was reached and every
beat of The Turning fired.** Anything else exits 1 and prints the expected rules
that never fired, by rule id.

### Flags

| flag | what it does |
|---|---|
| `--world PATH` | the pack's `world.json`; by default derived from the woven file's name |
| `--pack DIR` | pack directory holding `world.json` |
| `--out DIR` | where lines, shots and the report go (default `out/play`) |
| `--step-timeout S` | seconds one step may take before it is called done (default 4.0) |
| `--headed` | watch it play |
| `--try-verbs` | also press the verb buttons, for the `uses-verb` beats |
| `--no-talk` | do not press Interact on residents |
| `--plan` | print the walk and exit, no browser |
| `--self-test` | run the whole driver against a fake page, no browser |

### How it plays

For each phase in `world.json`'s `phases` order it collects every `comes-near`
`who` the rules for that phase name, resolves each to a tile (a speaker's `at`,
or a POI from `town.pois`), BFSs a tile path from wherever the hero is standing,
and walks it one tile per arrow key. On arrival it waits for the line the
`comes-near` rule speaks, talks to the resident where there is a control for
it, screenshots the phase, and presses Rest (`[data-rest]`, else the `R` key)
to turn the watch, waiting for the next phase to stand.

It is deterministic: no random waits anywhere. Every wait is a poll for a
DOM change with a bounded timeout, and every path is the shortest one over the
same map, so two runs walk the same yard in the same order.

### What it does not know

The woven player is a build artefact, so nothing about its DOM is assumed. The
driver probes, in order, and the report says which probe answered:

- **the log region** - `#log`, `[data-log]`, `#say`, `#message`, `.log`, and a
  list of others; failing all of them it falls back to the page text diff after
  each step;
- **the phase** - the player's own `STATE` (`web/player/parts/090-first-run-
  setup-vs-play.js:54`), then the rail's `[data-phase="<slug>"]` button's
  active class, then the phase's tone sentence appearing in the log;
- **the hero's position** - a tile pair named in the player state. Without one
  the walk takes every keypress at its word and the report says
  `NOT VERIFIED`, so an unverified run is never mistaken for a verified one;
- **Rest** - `[data-rest]`, else the `R` key;
- **talking** - a Talk/Speak/Interact control; residents whose line is already
  carried by a rule are a bonus, never a gate.

Phase-dependent water is not modelled: the map's `~` is solid water, and the
Mending Shift writes `"low"` for all four of its hours, so one static walkable
pass is right for this pack and would not be for a yard that floods.

### The check on the host

The driver has not been run against a real browser. `--self-test` runs it
against a fake page instead - a yard, a log, a phase rail, a Rest button, rules
that fire on arrival and on the transition - so the walking, the waiting, the
line matching, the scoring and the report are all exercised without Playwright:

```sh
python3 tools/play_slice.py --self-test    # exit 0
python3 tools/play_slice.py --plan --world worlds/mending-shift/world.json
```

Playwright is imported lazily, so both of those run on a machine that has never
had `python3 -m playwright install chromium` run against it. The first real run
needs it:

```sh
python3 -m pip install playwright && python3 -m playwright install chromium
```