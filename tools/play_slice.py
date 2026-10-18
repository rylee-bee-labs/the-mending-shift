#!/usr/bin/env python3
"""M2d: play the Mending Shift slice, all four phases, with a real browser.

`vefr probe` fires events but cannot advance the watch, so nothing after the
first hour has ever been seen playing. This driver opens a woven pack HTML in
headless Chromium at a 390x844 phone viewport and plays it the way a person
would: walk to every place and every resident that the rules for the standing
phase name in `comes-near`, talk where there is something to talk to, and press
Rest to turn the hour. It writes a screenshot per phase and every line the game
showed into `out/play/`, and it finishes with a report naming the phases
reached, the rule ids whose lines appeared, and the expected rules that never
fired.

Exit status is 0 only when every phase in `world.json`'s `phases` order was
reached and every beat of The Turning fired.

Read-only toward the game: it plays and it reports, and it never writes to
`world.json` or to anything else in the pack. Everything it writes goes under
`--out` (default `out/play/`).

Nothing about the DOM is assumed. The woven player is a build artefact, so the
driver probes for the log region, the phase rail, the Rest control and the
hero's position, and the report says which probe answered. `--plan` prints the
walk without a browser, and `--self-test` runs the whole driver against a fake
page, so the logic is tested on a machine that has no Playwright at all.

Usage:

    uv run vefr weave --pool 2 --pack mending-shift        # -> dist/mending-shift-<date>.html
    python3 tools/play_slice.py dist/mending-shift-2026-10-17.html
    python3 tools/play_slice.py --plan dist/mending-shift-2026-10-17.html
    python3 tools/play_slice.py --self-test                # no browser needed
"""

import argparse
import json
import re
import sys
import tempfile
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

# ---- what the driver assumes, and probes for when it cannot confirm it ----

VIEWPORT = {"width": 390, "height": 844}  # the phone the slice is built for
POLL_MS = 40  # how often a bounded wait re-reads the page; not a random sleep
STEP_TIMEOUT = 4.0  # seconds a single step may take before it is called done
SETTLE_TIMEOUT = 0.6  # seconds a move with no expected text change may settle
ENTER_TIMEOUT = 25.0  # seconds to get from the woven title screen into play
TALK_TIMEOUT = 2.5  # a resident's own line is best effort, never a gate

# The dialogue/log region. The first selector that exists in the page wins; if
# none do, the driver falls back to the page text diff after each step, which
# is what the brief asks for.
LOG_SELECTORS = [
    "#log",
    "[data-log]",
    "#say",
    "#say-line",
    "#message",
    "#messages",
    "#dialogue",
    "#narration",
    "#transcript",
    ".log",
    "[data-region='log']",
    "[data-region='dialogue']",
]

# Out of the title screen and into play. Tried in order; first click wins.
ENTER_SELECTORS = [
    "button:has-text('Enter the yard')",
    "button:has-text('Play offline')",
    "button:has-text('Play')",
    "button:has-text('Begin')",
    "button:has-text('Start')",
    "button:has-text('Continue')",
    "button:has-text('Enter')",
    "[data-action='play']",
    "[data-enter='play']",
    "#play",
    "#start",
]

# Rest. The pack declares `time.rest: true`, so the woven player puts a Rest
# verb in the action row with `data-rest` on it, and the R key does the same.
REST_SELECTORS = ["[data-rest]", "button[data-rest]", "#rest"]

# Talking. The nearest resident gets an entry in the action row; the speaker's
# own name is the fallback handle.
TALK_SELECTORS = [
    "#talk",
    "button:has-text('Talk')",
    "button:has-text('Speak')",
    "button:has-text('Interact')",
    "button:has-text('Say')",
    "[data-talk]",
    "[data-interact]",
]

# Movement. The first candidate per direction is the player's own arrow key;
# the rest are tried only when the driver can watch the hero and see it move.
DIRECTIONS = [
    ((0, -1), "up", ["ArrowUp", "w", "Up"]),
    ((0, 1), "down", ["ArrowDown", "s", "Down"]),
    ((-1, 0), "left", ["ArrowLeft", "a", "Left"]),
    ((1, 0), "right", ["ArrowRight", "d", "Right"]),
]

REST_KEYS = ["r", "R"]
TALK_KEYS = ["f", "F"]  # the player's own Talk keybind

# Mend. The pack's recipes are pressed from a Mend control; the player names none in this repo,
# so each is tried and the report lists what the page offered when none answers.
MEND_SELECTORS = [
    "[data-mend]",
    "#mend",
    "button:has-text('Mend')",
    "button:has-text('Fuse')",
]
MEND_PICK_SELECTORS = ["[data-recipe='%(id)s']", "[data-mend='%(id)s']"]

# Talk refuses beyond this many tiles ("No one is close enough to talk to.").
TALK_REACH = 2

# The hero's tile, published by the player after every accepted step and once at setup.
HERO_EXPR = "window.VEFR_HERO_AT ? JSON.stringify(window.VEFR_HERO_AT) : null"

# State probes. The first reads a top-level `STATE` with a `get()` method, which
# is what the woven player is assumed to expose: a classic <script> puts a
# top-level binding in scope for every other script in the page, so `evaluate`
# can read it by name. This repo holds no player source to check that against,
# so each probe is only believed when it returns a usable state (the run says
# when none did). The later probes are for a build that hangs the state off
# window.
STATE_EXPRS = [
    "JSON.stringify((typeof STATE !== 'undefined' && STATE && STATE.get) ? STATE.get() : null)",
    "JSON.stringify(typeof VEFR_STATE !== 'undefined' ? VEFR_STATE : null)",
    "JSON.stringify(window.VEFR_STATE || null)",
    "JSON.stringify(window.VEFR_PLAYER_STATE || null)",
]

# Keys that hold a tile pair. A hero position is only believed when one of
# these names is found, never when a bare number turns up.
POSITION_KEYS = ["hero", "player", "avatar", "position", "pos", "at", "tile", "xy"]

ACTIVE_CLASSES = {
    "active", "is-active", "current", "is-current", "selected", "is-selected",
    "on", "now", "standing", "phase-active",
}


# ---------------------------------------------------------------- pure logic


def norm(text):
    """Fold a line to a comparable form: case, quotes, dashes, whitespace."""
    if text is None:
        return ""
    text = unicodedata.normalize("NFKC", str(text))
    text = (
        text.replace("‘", "'")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("—", "-")
        .replace("–", "-")
    )
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def load_world(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def phase_order(world):
    """The pack's phases, in the order `world.json` writes them."""
    return [(slug, tone) for slug, tone in world.get("phases", {}).items()]


def walkable(world):
    """The tiles a person can stand on, from the town's legend and map.

    Phase-dependent water is not modelled: `town.water_by_phase` gives the
    standing water level per hour, and `~` is solid water, so a yard that
    actually flooded would need its own pass per phase. The Mending Shift
    writes "low" for all four of its hours, which is why one static pass is
    enough here - and why the driver says so rather than pretending.
    """
    town = world.get("town", {})
    legend = town.get("legend", {})
    tiles = set()
    for y, row in enumerate(town.get("map", [])):
        for x, ch in enumerate(row):
            if ch == "#" or legend.get(ch, {}).get("solid"):
                continue
            tiles.add((x, y))
    return tiles


def hero_start(world):
    start = world.get("town", {}).get("hero_start")
    return (int(start[0]), int(start[1])) if start else None


def poi_coords(world):
    """`town.pois` is {"x,y": "label"}, and a POI's label is its id."""
    out = {}
    for key, label in world.get("town", {}).get("pois", {}).items():
        try:
            x, y = (int(part) for part in str(key).split(","))
        except (TypeError, ValueError):
            continue
        out[label] = (x, y)
    return out


def speaker_coords(world):
    out = {}
    for sid, spec in world.get("speakers", {}).items():
        at = spec.get("at")
        if at and len(at) == 2:
            out[sid] = (int(at[0]), int(at[1]))
    return out


def resolve_who(world, who):
    """A `comes-near` `who` is a speaker id or a POI label. Anything else is
    unresolvable, and the report names it rather than guessing."""
    speakers = speaker_coords(world)
    if who in speakers:
        return speakers[who], "speaker"
    pois = poi_coords(world)
    if who in pois:
        return pois[who], "poi"
    return None, "unresolved"


def phases_in(cond, acc=None):
    """Every phase slug named anywhere in a rule's `if`, through `all-of`."""
    acc = set() if acc is None else acc
    if isinstance(cond, dict):
        if isinstance(cond.get("phase"), str):
            acc.add(cond["phase"])
        for value in cond.values():
            phases_in(value, acc)
    elif isinstance(cond, list):
        for value in cond:
            phases_in(value, acc)
    return acc


def when_kind(rule):
    when = rule.get("when", {})
    if not isinstance(when, dict) or len(when) != 1:
        return "mixed"
    return next(iter(when))


def rule_phases(rule):
    """The hours a rule is about: the phases it tests, plus the phase it fires
    on if it is keyed on the transition."""
    found = set()
    for cond in rule.get("if", []) or []:
        phases_in(cond, found)
    when = rule.get("when", {})
    if isinstance(when, dict) and isinstance(when.get("phase-changes"), dict):
        to = when["phase-changes"].get("to")
        if isinstance(to, str):
            found.add(to)
    return found


def rule_lines(rule):
    """Every line a rule speaks, in order, as (who or None, line)."""
    lines = []
    for action in rule.get("then", []) or []:
        say = action.get("say") if isinstance(action, dict) else None
        if isinstance(say, str) and say.strip():
            lines.append((None, say))
        elif isinstance(say, dict):
            line = say.get("line") or say.get("text") or ""
            if line.strip():
                lines.append((say.get("who"), line))
    return lines


# The events a driver that walks, talks and rests can actually produce. The
# rest of the pack (`mends`, and `uses-verb` unless asked for) is reported as
# not attempted rather than counted against the run.
DRIVEN_EVENTS = {"comes-near", "phase-changes"}


def rule_status_kind(rule, try_verbs=False):
    kind = when_kind(rule)
    if kind in DRIVEN_EVENTS:
        return "required"
    if kind == "uses-verb" and try_verbs:
        return "optional"
    return "not-attempted"


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bfs(tiles, start, goal, blocked=frozenset()):
    """The shortest tile path start -> goal, stepping only on walkable tiles.

    `blocked` holds tiles found to be unwalkable in play (a wall the legend
    does not mark, a door that will not open) so a plan can be re-cut.
    """
    if start == goal:
        return [start]
    if goal not in tiles and goal not in blocked:
        return None
    seen = {start}
    frontier = [start]
    came = {}
    while frontier:
        nxt = []
        for node in frontier:
            x, y = node
            for (dx, dy), _name, _keys in DIRECTIONS:
                step = (x + dx, y + dy)
                if step in seen or step in blocked:
                    continue
                if step != goal and step not in tiles:
                    continue
                seen.add(step)
                came[step] = node
                if step == goal:
                    path = [goal]
                    while path[-1] != start:
                        path.append(came[path[-1]])
                    path.reverse()
                    return path
                nxt.append(step)
        frontier = nxt
    return None


def nearest_reachable(tiles, goal, start, blocked=frozenset()):
    """The goal itself, or the closest tile to it a person can stand on.

    A `comes-near` rule with a distance still fires from next door, so a tile
    nobody can stand on (a cliff, a rack) is satisfied from beside it.
    """
    if goal in tiles:
        path = bfs(tiles, start, goal, blocked)
        if path:
            return goal, path
    best = None
    for tile in sorted(tiles):
        distance = manhattan(tile, goal)
        if distance > 2:
            continue
        path = bfs(tiles, start, tile, blocked)
        if not path:
            continue
        score = (distance, len(path))
        if best is None or score < best[0]:
            best = (score, tile, path)
    return (best[1], best[2]) if best else (None, None)


@dataclass
class Target:
    who: str
    tile: object
    kind: str  # "speaker", "poi" or "unresolved"
    distance: int
    rules: list = field(default_factory=list)
    needs: set = field(default_factory=set)  # items its rules want held
    gives: set = field(default_factory=set)  # items its rules hand over

    def label(self, world):
        spec = world.get("speakers", {}).get(self.who)
        return spec.get("name", self.who) if spec else self.who


def cond_items(cond, want=True, acc=None):
    """Items a condition tests: held when `want`, not held otherwise, through
    `all-of` and `not`."""
    acc = set() if acc is None else acc
    if isinstance(cond, dict):
        if isinstance(cond.get("has"), str) and want:
            acc.add(cond["has"])
        if isinstance(cond.get("not"), dict):
            cond_items(cond["not"], not want, acc)
        for sub in cond.get("all-of") or []:
            cond_items(sub, want, acc)
    return acc


def rule_needs(rule):
    """Items a rule wants held."""
    out = set()
    for cond in rule.get("if", []) or []:
        cond_items(cond, True, out)
    return out


def rule_gives(rule):
    return {a["give"] for a in rule.get("then", []) or [] if isinstance(a, dict) and isinstance(a.get("give"), str)}


def mend_recipes(world):
    """{recipe id: recipe} for every recipe a `mends` rule is keyed on."""
    wanted = {r["when"]["mends"].get("recipe") for r in world.get("rules", [])
              if isinstance(r.get("when"), dict) and isinstance(r["when"].get("mends"), dict)}
    return {rc["id"]: rc for rc in world.get("recipes", []) if rc.get("id") in wanted}


def mend_outputs(world):
    return {rc.get("output") for rc in mend_recipes(world).values()}


def earlier_gives(world, phase):
    """Items rules of hours before `phase` hand over."""
    order = [slug for slug, _ in phase_order(world)]
    before = set(order[:order.index(phase)]) if phase in order else set()
    held = set()
    for rule in world.get("rules", []):
        phases = rule_phases(rule)
        if phases and phases <= before:
            held |= rule_gives(rule)
    return held


def comes_near_targets(world, phase, held=None, only=None):
    """Every place and resident the rules for `phase` name in `comes-near`,
    in dependency order: a target whose rules need an item waits for the
    target that hands it over. Nearest-first among those that can go, ties
    broken by name so two runs walk the same yard. `only` narrows to a set of
    rule ids."""
    found = {}
    for rule in world.get("rules", []):
        when = rule.get("when", {})
        if not isinstance(when, dict):
            continue
        near = when.get("comes-near")
        if not isinstance(near, dict) or phase not in rule_phases(rule):
            continue
        if only is not None and rule.get("id") not in only:
            continue
        who = near.get("who")
        if not isinstance(who, str):
            continue
        tile, kind = resolve_who(world, who)
        try:
            distance = int(near.get("distance", 1))
        except (TypeError, ValueError):
            distance = 1
        entry = found.setdefault(who, {
            "tile": tile, "kind": kind, "distance": distance, "rules": [],
            "needs": set(), "gives": set(),
        })
        entry["distance"] = max(entry["distance"], distance)
        entry["rules"].append(rule.get("id", "?"))
        # what a mend makes is not another target's gift, so it is no wait
        entry["needs"] |= rule_needs(rule) - mend_outputs(world)
        entry["gives"] |= rule_gives(rule)
    targets = [Target(who=who, tile=v["tile"], kind=v["kind"], distance=v["distance"], rules=v["rules"],
                      needs=v["needs"], gives=v["gives"])
               for who, v in found.items()]
    targets.sort(key=lambda t: (t.tile is None, manhattan(hero_start(world) or (0, 0), t.tile)
                                if t.tile else 999, t.who))
    held = set(earlier_gives(world, phase) if held is None else held)
    ordered = []
    while targets:
        ready = next((t for t in targets if t.needs <= held), targets[0])
        targets.remove(ready)
        ordered.append(ready)
        held |= ready.gives
    return ordered


def stand_tile(world, target, start, tiles, blocked=frozenset()):
    """Where to stand for `target`. A place is stood on or beside; a speaker
    is stood beside, with that speaker strictly the nearest (Talk takes the
    nearest), inside the rule's distance and Talk's reach of two."""
    if target.kind != "speaker" or target.tile is None:
        return nearest_reachable(tiles, target.tile, start, blocked)
    others = [at for sid, at in speaker_coords(world).items() if at != target.tile]
    reach = max(1, min(target.distance, TALK_REACH))
    best = None
    for tile in sorted(tiles):
        d = manhattan(tile, target.tile)
        if d > reach:
            continue
        path = bfs(tiles, start, tile, blocked)
        if not path:
            continue
        crowded = any(manhattan(tile, o) <= d for o in others)
        score = (crowded, d == 0, d, len(path))
        if best is None or score < best[0]:
            best = (score, tile, path)
    return (best[1], best[2]) if best else (None, None)


def plan_phase(world, phase, start, tiles, blocked=frozenset(), only=None):
    """The walk for one hour: every comes-near target, in dependency order,
    each with the tile path to it. A target with no coordinates or no route
    comes back flagged, so the report can name it instead of quietly dropping it."""
    plan = []
    at = start
    for target in comes_near_targets(world, phase, only=only):
        if target.tile is None:
            plan.append((target, None))
            continue
        tile, path = stand_tile(world, target, at, tiles, blocked)
        if path:
            at = path[-1]
        plan.append((target, path))
    return plan


def phase_script(world, phase):
    """What the driver does in one hour, in order, as (op, argument):

    verb   a uses-verb beat; the ones that need an item not held yet wait
           until after the walk, and the ones that need it NOT held go first
    target walk to a place or resident (and Talk, for a resident)
    mend   press a recipe, once
    again  the targets whose rules need what the mend made, walked a second time
    """
    verb_rules = [r for r in world.get("rules", [])
                  if when_kind(r) == "uses-verb" and phase in rule_phases(r)]
    before = [r["when"]["uses-verb"]["verb"] for r in verb_rules if not rule_needs(r)]
    after = [r["when"]["uses-verb"]["verb"] for r in verb_rules if rule_needs(r)]
    script = [("verb", v) for v in before]
    script += [("target", t) for t in comes_near_targets(world, phase)]
    script += [("verb", v) for v in after]
    outputs = mend_outputs(world)
    later = [r for r in world.get("rules", []) if phase in rule_phases(r) and rule_needs(r) & outputs
             and when_kind(r) == "comes-near"]
    last = [slug for slug, _ in phase_order(world)
            if any(slug in rule_phases(r) and rule_needs(r) & outputs for r in world.get("rules", []))][-1:]
    if later and phase in last:
        ids = {r["id"] for r in later}
        script += [("mend", rc) for _rid, rc in sorted(mend_recipes(world).items())
                   if rc.get("output") in outputs]
        script += [("again", t) for t in comes_near_targets(world, phase, only=ids)]
    return script


def why_unfireable(world, rule):
    """Plain words for a rule the script cannot fire."""
    givers = set().union(*(rule_gives(r) for r in world.get("rules", [])), set())
    made = mend_outputs(world)
    gone = sorted(i for i in rule_needs(rule) if i not in givers | made)
    if gone:
        return "needs %s, which no rule hands over" % ", ".join(gone)
    flags = []

    def collect(cond):
        if isinstance(cond, dict):
            if "flag" in cond and cond.get("is") is False:
                flags.append(cond["flag"])
            for sub in cond.get("all-of") or []:
                collect(sub)

    for cond in rule.get("if", []) or []:
        collect(cond)
    if flags:
        return ("needs %s unset, but the walk has already set it by the time this hour's "
                "walk reaches it (the bench, an hour earlier, sets it)" % ", ".join(flags))
    if rule_needs(rule) & made:
        return "its branch excludes the other: the walk takes the one that leaves this unmet"
    return "no point in the walk meets its event and its `if` together"


def holds(cond, phase, items, flags):
    """Whether one `if` condition holds in a state."""
    if isinstance(cond, dict):
        if "phase" in cond:
            return cond["phase"] == phase
        if "has" in cond:
            return cond["has"] in items
        if "flag" in cond:
            return bool(flags.get(cond["flag"], False)) == bool(cond.get("is", True))
        if "not" in cond:
            return not holds(cond["not"], phase, items, flags)
        if "all-of" in cond:
            return all(holds(c, phase, items, flags) for c in cond["all-of"])
        if "any-of" in cond:
            return any(holds(c, phase, items, flags) for c in cond["any-of"])
    return False


def simulate(world, try_verbs=True):
    """The rules this walk should fire, by playing the script against the
    pack's own rules: no browser, so only what stepping, Talk, verbs, Rest and
    one Mend are known to do. A rule fires wherever its event and its `if`
    meet; walking past a place on the way to another is not counted."""
    items, flags, fired = set(), {}, []

    def fire(match, phase):
        for rule in world.get("rules", []):
            if not match(rule.get("when", {})):
                continue
            if not all(holds(c, phase, items, flags) for c in rule.get("if", []) or []):
                continue
            if rule["id"] not in fired:
                fired.append(rule["id"])
            for action in rule.get("then", []) or []:
                if isinstance(action, dict) and "give" in action:
                    items.add(action["give"])
                if isinstance(action, dict) and "set" in action:
                    flags[action["set"]] = True

    phases = [slug for slug, _ in phase_order(world)]
    for index, phase in enumerate(phases):
        fire(lambda w, p=phase: isinstance(w, dict) and w.get("phase-changes", {}).get("to") == p, phase)
        for op, arg in phase_script(world, phase):
            if op == "verb" and try_verbs:
                fire(lambda w, v=arg: isinstance(w, dict) and w.get("uses-verb", {}).get("verb") == v, phase)
            elif op in ("target", "again"):
                def near(w, a=arg):
                    n = w.get("comes-near") if isinstance(w, dict) else None
                    return isinstance(n, dict) and n.get("who") == a.who
                fire(near, phase)
            elif op == "mend":
                if set(arg.get("inputs", [])) <= items:
                    items.difference_update(arg.get("inputs", []))
                    items.add(arg.get("output"))
                    fire(lambda w, r=arg["id"]: isinstance(w, dict) and w.get("mends", {}).get("recipe") == r, phase)
    return fired


def match_rule(rule, haystack, world=None):
    """(matched, missing, total) lines of a rule, against everything said.

    A line matches when it is a whole line of what the game showed, or a whole
    line with its speaker in front ("id: line" or "Display Name: line"). It can still
    false-positive when the page shows the same sentence somewhere other than
    the rule firing (a help text, a speaker's seed, a repeat from an earlier
    phase), and a say spanning several lines is matched line by line.
    """
    shown = set(haystack.splitlines())
    speakers = (world or {}).get("speakers", {}) or {}

    def prefixes(who):
        if not who:
            return []
        name = (speakers.get(who) or {}).get("name") if isinstance(speakers.get(who), dict) else None
        return [norm(who)] + ([norm(name)] if name else [])
    matched, missing = [], []
    for who, line in rule_lines(rule):
        parts = [norm(p) for p in line.splitlines() if norm(p)]
        found = all(p in shown or any("%s: %s" % (pre, p) in shown for pre in prefixes(who))
                    for p in parts)
        (matched if found else missing).append((who, line))
    return matched, missing, len(matched) + len(missing)


def find_position(state, world):
    """The hero's tile in a state blob, if this build names one."""
    grid = world.get("town", {}).get("map", [])
    width = max((len(row) for row in grid), default=0)

    def valid(pair):
        return (isinstance(pair, (list, tuple)) and len(pair) == 2
                and all(isinstance(v, int) for v in pair)
                and 0 <= pair[1] < len(grid) and 0 <= pair[0] < width)

    def walk(node):
        if isinstance(node, dict):
            for key in POSITION_KEYS:
                if valid(node.get(key)):
                    return tuple(node[key])
            if valid((node.get("x"), node.get("y"))):
                return (node["x"], node["y"])
            for key in POSITION_KEYS:
                found = walk(node.get(key))
                if found:
                    return found
            return None
        return tuple(node) if valid(node) else None

    return walk(state)


def is_active(el):
    """Whether a phase rail button is the standing one."""
    def attr(name):
        try:
            return (el.get_attribute(name) or "").strip()
        except Exception:
            return ""

    if {word.lower() for word in attr("class").split()} & ACTIVE_CLASSES:
        return True
    if attr("aria-current") or attr("data-active"):
        return True
    if attr("aria-pressed").lower() == "true":
        return True
    return attr("data-state").lower() == "active"


# ---------------------------------------------------------------- the driver


class Report:
    """What one run leaves behind, in memory and on disk."""

    def __init__(self, html, world_path, outdir):
        self.html = html
        self.world = str(world_path)
        self.outdir = str(outdir)
        self.phases = []
        self.rules = []
        self.notes = []
        self.recorded = []
        self.shots = []
        self.missing = []
        self.not_attempted = []
        self.exit = 1

    def note(self, text):
        self.notes.append(text)

    def to_json(self):
        return {
            "html": self.html,
            "world": self.world,
            "out": self.outdir,
            "phases": self.phases,
            "rules": self.rules,
            "recorded": [{"phase": p, "source": s, "line": l} for p, s, l in self.recorded],
            "screenshots": self.shots,
            "missing": self.missing,
            "not_attempted": self.not_attempted,
            "notes": self.notes,
            "exit": self.exit,
        }


class Game:
    """Everything the driver does to one page."""

    def __init__(self, page, world, outdir, html_path=None, world_path=None,
                 step_timeout=STEP_TIMEOUT, settle=SETTLE_TIMEOUT,
                 try_verbs=False, talk=True, quiet=False):
        self.page = page
        self.world = world
        self.html_path = html_path or ""
        self.world_path = world_path or ""
        self.outdir = Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=True)
        self.step_timeout = step_timeout
        self.settle = settle
        self.try_verbs = try_verbs
        self.talk = talk
        self.quiet = quiet
        self.report = Report(self.html_path, self.world_path, self.outdir)
        self.tiles = walkable(world)
        self.blocked = set()
        self.keys = {}  # direction name -> the key that actually moved the hero
        self.rest_control = None
        self.state_expr = None
        self.hero_probe = "unverified"
        self.hero_region = None
        self.log_selector = None
        self.pos = hero_start(world)
        self.tag = "start"  # what the driver is doing, for the lines file
        self.log_lines = []  # (phase, source, line), in the order shown
        self.seen_norm = ""
        self.phase = None

    # ---- reading the page ------------------------------------------------

    def say(self, text):
        if not self.quiet:
            print("  . " + text)
        self.report.note(text)

    def _query(self, selector):
        try:
            return self.page.query_selector(selector)
        except Exception:
            return None

    def log_region(self):
        """The log region, remembered once found. "" means the page-text
        fallback, which is the brief's second choice."""
        if self.log_selector is None:
            for selector in LOG_SELECTORS:
                if self._query(selector) is not None:
                    self.log_selector = selector
                    self.say("log region: %s" % selector)
                    break
            else:
                self.log_selector = ""
                self.say("no log selector matched (tried %s); falling back to the page text diff"
                         % ", ".join(LOG_SELECTORS[:5]))
        return self.log_selector

    def text(self):
        """Everything the game is showing right now, as one string."""
        selector = self.log_region()
        try:
            if selector:
                el = self.page.query_selector(selector)
                if el is not None:
                    return el.inner_text() or ""
            return self.page.inner_text("body") or ""
        except Exception:
            try:
                return self.page.inner_text("body") or ""
            except Exception:
                return ""

    def state(self):
        """The player's own state, if this build exposes one."""
        exprs = [self.state_expr] if self.state_expr else STATE_EXPRS
        for expr in exprs:
            if not expr:
                continue
            try:
                raw = self.page.evaluate(expr)
            except Exception:
                continue
            if not raw:
                continue
            try:
                value = json.loads(raw)
            except (TypeError, ValueError):
                continue
            if isinstance(value, dict) and value:
                if self.state_expr is None:
                    self.state_expr = expr
                    self.say("player state readable: %s" % expr[:58])
                return value
        return None

    def hero_pos(self):
        """(x, y) from `window.VEFR_HERO_AT`, which the player sets after every
        accepted step; else from the player state if that names it; else None."""
        try:
            raw = self.page.evaluate(HERO_EXPR)
            at = json.loads(raw) if raw else None
        except Exception:
            at = None
        if isinstance(at, dict) and all(isinstance(at.get(k), int) for k in ("x", "y")):
            self.hero_probe = "VEFR_HERO_AT"
            self.hero_region = at.get("region")
            return (at["x"], at["y"])
        state = self.state()
        if state is None:
            return None
        found = find_position(state, self.world)
        if found is not None:
            self.hero_probe = "state"
        return found

    def current_phase(self):
        """The standing phase, and how it was read."""
        phases = [slug for slug, _tone in phase_order(self.world)]
        state = self.state()
        if isinstance(state, dict) and state.get("phase") in phases:
            return state["phase"], "state"
        for slug in phases:
            el = self._query('#phase button[data-phase="%s"]' % slug)
            if el is None:
                el = self._query('[data-phase="%s"]' % slug)
            if el is not None and is_active(el):
                return slug, "rail"
        blob = norm(self.text())
        for slug, tone in phase_order(self.world):
            if norm(tone) and norm(tone) in blob:
                return slug, "tone"
        return None, "unknown"

    def wait_for(self, check, timeout):
        """Poll `check` until it is truthy or the bounded timeout runs out."""
        deadline = time.monotonic() + timeout
        while True:
            value = check()
            if value:
                return value
            if time.monotonic() >= deadline:
                return None
            self.page.wait_for_timeout(POLL_MS)

    def absorb(self):
        """Move any new lines out of the page text and into the record.

        A line is recorded once, the first time it is seen: a rule that fires on
        two consecutive steps puts the same line in the scrollback twice, and
        the record is a list of what was said, not of how many times the log
        was redrawn.
        """
        text = self.text()
        added = []
        for line in text.splitlines():
            key = norm(line)
            if len(key) < 3 or key in self.seen_norm:
                continue
            self.seen_norm += "\n" + key
            added.append(line.strip())
        if added:
            phase, _how = self.current_phase()
            for line in added:
                self.log_lines.append((phase or self.phase or "?", self.tag, line))
        return added

    def wait_for_change(self, before, timeout):
        """Wait, bounded, until the page says something new."""
        changed = self.wait_for(lambda: self.text() != before, timeout)
        self.absorb()
        return changed is not None

    # ---- playing ---------------------------------------------------------

    def _visible(self, selector):
        try:
            el = self.page.query_selector(selector)
            return bool(el and el.is_visible())
        except Exception:
            return False

    def enter_play(self):
        """Out of the woven title screen and into the yard."""

        def in_play():
            phase, _how = self.current_phase()
            return phase is not None or self._query("#phase") is not None

        # The woven player keeps its state (and so a phase) behind the title screen, so "a phase
        # is readable" does not mean "in play": a visible start button is clicked first, always.
        title_up = any(self._visible(sel) for sel in ENTER_SELECTORS)
        if title_up or not in_play():
            for selector in ENTER_SELECTORS:
                if not self._visible(selector):
                    continue
                el = self._query(selector)
                if el is None:
                    continue
                try:
                    el.click(timeout=2000)
                except Exception:
                    continue
                self.say("clicked %r to enter play" % selector)
                if self.wait_for(in_play, ENTER_TIMEOUT / 4):
                    break
            else:
                self.say("no play button answered (%s tried); playing whatever loaded"
                         % ", ".join(ENTER_SELECTORS[:4]))
        start = self.hero_pos()
        here = hero_start(self.world)
        if start and here and start != here:
            self.say("player state puts the hero at %s but world.json says %s; trusting the state"
                     % (list(start), list(here)))
        elif start and here:
            self.say("hero at %s, read from player state" % list(here))
        # A setup input left focused would swallow every keypress below.
        try:
            self.page.evaluate(
                "document.activeElement && document.activeElement.blur "
                "? (document.activeElement.blur(), null) : null"
            )
        except Exception:
            pass
        self.absorb()

    def press_dir(self, dx, dy):
        """One step. True when the hero is believed to have moved."""
        name = next(n for d, n, _ in DIRECTIONS if d == (dx, dy))
        candidates = [self.keys[name]] if name in self.keys else \
            next(c for d, n, c in DIRECTIONS if n == name)
        before = self.hero_pos()
        for key in candidates:
            self.page.keyboard.press(key)
            if before is None:
                self.keys[name] = key
                return True
            if self.wait_for(lambda: self.hero_pos() != before, self.settle):
                self.keys[name] = key
                return True
        return False

    def walk_to(self, goal):
        """Walk the hero to a tile. Returns (tile ended on, steps pressed)."""
        at = self.hero_pos() or self.pos
        steps = 0
        for _attempt in range(3):
            path = bfs(self.tiles - self.blocked, at, goal, frozenset())
            if path is None:
                stop, path = nearest_reachable(self.tiles - self.blocked, goal, at, frozenset())
                if path is None:
                    break
                goal = stop
            stalled = False
            for nxt in path[1:]:
                before = self.hero_pos()
                moved = self.press_dir(nxt[0] - at[0], nxt[1] - at[1])
                seen = self.hero_pos()
                steps += 1
                if seen is None:
                    at = nxt  # no state to read: the keypress is taken at its word
                    continue
                if seen == before and not moved:
                    self.blocked.add(nxt)  # the legend disagrees with the game
                    self.say("the game refused %s; re-cutting the walk around it" % (nxt,))
                    stalled = True
                    break
                at = seen
            if stalled:
                at = self.hero_pos() or at
                continue
            self.pos = at
            return at, steps
        self.pos = at
        return at, steps

    def shown(self):
        """Every line on screen, the log region and the page body both, folded."""
        lines = set()
        for chunk in (self.text(), self._body()):
            lines |= {norm(l) for l in chunk.splitlines() if len(norm(l)) >= 3}
        return lines

    def _body(self):
        try:
            return self.page.inner_text("body") or ""
        except Exception:
            return ""

    def press_control(self, selectors, keys=()):
        """Click the first control that answers, else press a key. Returns what
        was pressed, or None."""
        for selector in selectors:
            el = self._query(selector)
            if el is None:
                continue
            try:
                el.click(timeout=1000)
                return selector
            except Exception:
                continue
        for key in keys:
            try:
                self.page.keyboard.press(key)
                return "key %s" % key
            except Exception:
                continue
        return None

    def new_lines(self, before, timeout=TALK_TIMEOUT, wanted=None):
        """Lines that appeared since `before` (a `shown()` snapshot); waits,
        bounded, for one that `wanted` accepts (any, when None)."""
        def fresh():
            lines = [l for l in self.shown() - before if wanted is None or wanted(l)]
            return lines
        got = self.wait_for(fresh, timeout) or []
        self.absorb()
        return got

    def offered(self):
        """The controls the page is offering, for a failure note."""
        try:
            els = self.page.query_selector_all("button") or []
            names = []
            for el in els:
                label = (el.inner_text() or el.get_attribute("title") or "").strip().replace("\n", " ")
                if label and label not in names:
                    names.append(label)
            return names[:16]
        except Exception:
            return []

    def talk_to(self, name, who=None):
        """Talk to a resident and VERIFY it: True only when a new line naming
        them turns up. A click is never taken at its word."""
        if not self.talk:
            return False
        who = who or name
        speaker = speaker_coords(self.world).get(who)
        here = self.hero_pos() or self.pos
        distance = manhattan(here, speaker) if speaker and here else None
        names = {norm(name), norm(who)}
        self.tag = "talk %s" % name
        before = self.shown()
        pressed = self.press_control(TALK_SELECTORS, TALK_KEYS)
        got = self.new_lines(before, wanted=lambda l: any(n in l for n in names)) if pressed else []
        if got:
            return True
        self.say("talk to %s at distance %s produced nothing%s"
                 % (name, "?" if distance is None else distance,
                    "" if pressed else " (no Talk control or F key answered)"))
        return False

    def try_verb(self, verb):
        """Press a verb's control and VERIFY it: True only when a new line shows."""
        self.tag = "verb %s" % verb
        selectors = ["[data-verb='%s']" % verb, "button:has-text('%s')" % verb,
                     "button:has-text(\"%s\")" % verb]
        before = self.shown()
        pressed = self.press_control(selectors)
        if pressed and self.new_lines(before):
            return True
        self.say("verb %s %s; controls offered: %s"
                 % (verb, "produced nothing" if pressed else "has no control",
                    ", ".join(self.offered()) or "none readable"))
        return False

    def try_mend(self, recipe):
        """Press the Mend for a recipe once and verify its own line (or the
        rule's) appears. If the page offers no control, say so."""
        self.tag = "mend %s" % recipe["id"]
        before = self.shown()
        pressed = self.press_control(MEND_SELECTORS)
        if pressed:
            self.press_control([sel % {"id": recipe["id"]} for sel in MEND_PICK_SELECTORS])
        said = norm(recipe.get("say"))
        out = norm((self.world.get("items", {}).get(recipe.get("output")) or {}).get("name"))
        if pressed and self.new_lines(before, wanted=lambda l: (said and said in l) or (out and out in l)):
            return True
        self.say("mend %s: %s; controls offered: %s"
                 % (recipe["id"], "pressed %s but the quiet coat did not appear" % pressed if pressed
                    else "no Mend control is offered", ", ".join(self.offered()) or "none readable"))
        return False

    def rest(self):
        """Press Rest: the button with `data-rest` on it, else the R key."""
        for selector in REST_SELECTORS:
            el = self._query(selector)
            if el is None:
                continue
            try:
                el.click(timeout=2000)
                self.rest_control = "button (%s)" % selector
                return True
            except Exception:
                continue
        for key in REST_KEYS:
            try:
                self.page.keyboard.press(key)
                self.rest_control = "key (%s)" % key
                return True
            except Exception:
                continue
        return False

    def screenshot(self, name):
        path = self.outdir / name
        try:
            self.page.screenshot(path=str(path))
            self.report.shots.append(str(path))
            return path
        except Exception as exc:
            self.say("screenshot %s failed: %s" % (name, exc))
            return None

    def visit(self, target, again=False):
        """Walk to a target and, for a resident, Talk and verify it."""
        line = {"who": target.who, "kind": target.kind, "tile": target.tile,
                "rules": target.rules, "walked": False, "steps": 0, "again": again}
        if target.tile is None:
            line["note"] = "world.json names no coordinates for %r" % target.who
            self.say("%s has no coordinates" % target.who)
            return line
        here = self.hero_pos() or self.pos
        tiles = self.tiles - self.blocked
        stand, path = stand_tile(self.world, target, here, tiles)
        if path is None:
            line["note"] = "no walkable route to %s" % (target.tile,)
            self.say("no route to %r at %s" % (target.who, target.tile))
            return line
        if again and manhattan(here, target.tile) <= target.distance:
            # step away first: a place fires when stepped onto, not when stood on
            far = hero_start(self.world)
            if far and manhattan(far, target.tile) > target.distance:
                self.walk_to(far)
        self.tag = "walk to %s" % target.who
        before = self.text()
        at, steps = self.walk_to(stand)
        line["walked"] = at == stand
        line["tile_reached"] = list(at) if at else None
        line["steps"] = steps
        # a comes-near rule fires on arrival, so give the line its moment
        self.wait_for_change(before, min(self.step_timeout, 1.5))
        if target.kind == "speaker":
            line["talked"] = self.talk_to(target.label(self.world), target.who)
        return line

    # ---- the run ---------------------------------------------------------

    def run(self):
        world = self.world
        phases = phase_order(world)
        self.enter_play()

        for index, (slug, tone) in enumerate(phases, start=1):
            phase, how = self.current_phase()
            entry = {
                "index": index,
                "phase": slug,
                "reached": phase == slug,
                "read_by": how,
                "targets": [],
                "screenshot": None,
            }
            self.phase = phase or slug
            self.tag = "arrive %s" % slug
            self.absorb()
            for op, arg in phase_script(world, slug):
                if op == "verb":
                    if self.try_verbs:
                        entry.setdefault("verbs", []).append({"verb": arg, "pressed": self.try_verb(arg)})
                elif op == "mend":
                    entry["mend"] = {"recipe": arg["id"], "made": self.try_mend(arg)}
                else:
                    entry["targets"].append(self.visit(arg, again=(op == "again")))

            shot = "phase-%02d-%s.png" % (index, slug)
            self.screenshot(shot)
            entry["screenshot"] = shot
            self.report.phases.append(entry)

            if index < len(phases):
                nxt = phases[index][0]
                self.tag = "rest into %s" % nxt
                before = self.text()
                if not self.rest():
                    self.say("no Rest control and no Rest key answered")
                    break
                arrived = self.wait_for(lambda: self.current_phase()[0] == nxt, self.step_timeout)
                self.wait_for_change(before, min(self.step_timeout, 1.5))
                self.absorb()
                if not arrived:
                    self.say("Rest did not turn the watch to %s (control: %s)"
                             % (nxt, self.rest_control))
                    break
                self.say("rested into %s (%s)" % (nxt, self.rest_control))

        self.report.recorded = list(self.log_lines)
        self.score()
        return self.report

    def score(self):
        """Match every rule's own lines against everything the game showed."""
        report = self.report
        haystack = self.seen_norm
        # The player's own record of what ran: the rules engine marks every rule id that fired
        # in window.VEFR_RULES_STATE.fired. It is the authority; matching said lines against the
        # page text is the fallback (a line can be drawn somewhere this script does not read).
        try:
            engine_fired = set(self.page.evaluate(
                "Object.keys(((window.VEFR_RULES_STATE || {}).fired) || {})") or [])
        except Exception:
            engine_fired = set()
        if engine_fired:
            self.say("rules the player marked fired: %d" % len(engine_fired))
        for rule in self.world.get("rules", []):
            matched, missing, total = match_rule(rule, haystack, self.world)
            kind = rule_status_kind(rule, self.try_verbs)
            entry = {
                "id": rule.get("id", "?"),
                "when": when_kind(rule),
                "phases": sorted(rule_phases(rule)),
                "kind": kind,
                "lines": "%d/%d" % (len(matched), total),
                "status": "fired" if (rule.get("id") in engine_fired or matched or total == 0) else "missing",
                "missing_lines": [line for _who, line in missing][:3],
            }
            report.rules.append(entry)
            if kind == "required" and entry["status"] != "fired":
                report.missing.append(entry["id"])
            if kind == "not-attempted":
                report.not_attempted.append(entry["id"])

        reached = [p for p in report.phases if p["reached"]]
        expected_phases = len(phase_order(self.world))
        self.say("phases reached: %d/%d" % (len(reached), expected_phases))
        self.say("hero position: %s" % (
            "read from %s" % self.hero_probe if self.hero_probe != "unverified"
            else "NOT VERIFIED (no VEFR_HERO_AT and none in the player state), so the walk "
                 "takes every keypress at its word"))
        expected = simulate(self.world, self.try_verbs)
        for rule in self.world.get("rules", []):
            if rule.get("id") not in expected:
                self.say("unfireable by this walk: %s: %s" % (rule.get("id"), why_unfireable(self.world, rule)))
        self.say("Rest control: %s" % (self.rest_control or "none found"))
        self.say("uses-verb beats: %s" % ("attempted" if self.try_verbs
                                          else "not attempted (--try-verbs presses them)"))
        report.exit = 0 if (len(reached) == expected_phases and not report.missing) else 1

    def write_lines(self):
        path = self.outdir / "lines.txt"
        with open(path, "w", encoding="utf-8") as fh:
            for phase, source, line in self.log_lines:
                fh.write("[%s] %s: %s\n" % (phase, source, line))
        return path


# --------------------------------------------------------------- the report


def write_report(report, outdir):
    """The report.md and report.json one run leaves behind."""
    outdir = Path(outdir)
    out = []
    add = out.append
    add("# Play slice report")
    add("")
    add("- html: `%s`" % report.html)
    add("- world: `%s`" % report.world)
    add("- viewport: %dx%d" % (VIEWPORT["width"], VIEWPORT["height"]))
    add("- lines recorded: %d" % len(report.recorded))
    add("- screenshots: %d" % len(report.shots))
    add("- exit: %d" % report.exit)
    add("")
    add("## Phases")
    add("")
    add("| # | phase | reached | read by | walked to | screenshot |")
    add("|---|---|---|---|---|---|")
    for phase in report.phases:
        walked = ", ".join(
            "%s%s" % (t["who"], "" if t.get("walked") else " (NOT REACHED)")
            for t in phase["targets"]) or "-"
        add("| %d | `%s` | %s | %s | %s | %s |" % (
            phase["index"], phase["phase"], "yes" if phase["reached"] else "**no**",
            phase["read_by"], walked, phase["screenshot"] or "-"))
    add("")
    add("## Rules")
    add("")
    add("| rule | when | phases | lines | kind | status |")
    add("|---|---|---|---|---|---|")
    for rule in report.rules:
        add("| `%s` | %s | %s | %s | %s | %s |" % (
            rule["id"], rule["when"], ", ".join(rule["phases"]) or "-",
            rule["lines"], rule["kind"], rule["status"]))
    add("")
    add("## Expected rules that never fired")
    add("")
    add("\n".join("- `%s`" % rid for rid in report.missing) if report.missing
        else "None: every rule the walk and Rest can fire fired.")
    add("")
    if report.not_attempted:
        add("Not attempted (no walking, resting or talking produces them): "
            + ", ".join("`%s`" % rid for rid in report.not_attempted))
        add("")
    add("## Notes")
    add("")
    for note in report.notes:
        add("- %s" % note)
    add("")
    (outdir / "report.md").write_text("\n".join(out), encoding="utf-8")
    (outdir / "report.json").write_text(json.dumps(report.to_json(), indent=2, default=str), encoding="utf-8")
    return outdir / "report.md"


# ------------------------------------------------------------------- the CLI


def derive_world(html_path, pack=None):
    """Find world.json for a woven file. `vefr weave` names its output
    `<pack>-<date>.html`, so the pack slug is the stem with the date off it."""
    html_path = Path(html_path)
    if pack:
        return Path(pack) / "world.json"
    stem = html_path.stem
    slug = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", stem)
    for candidate in (Path("worlds") / slug / "world.json",
                      Path("worlds") / stem / "world.json",
                      html_path.parent / "worlds" / slug / "world.json",
                      html_path.parent.parent / "worlds" / slug / "world.json",
                      html_path.parent / "world.json"):
        if candidate.is_file():
            return candidate
    return None


def open_page(html_path, headed=False):
    """The browser: headless Chromium at the phone viewport, on a clean profile.

    The context is new every run, so the pack's `time.persist` standing phase
    (`vefr-time-<world>` in localStorage) cannot start this run an hour in.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "playwright is not installed here.\n"
            "  python3 -m pip install playwright && python3 -m playwright install chromium\n"
            "or: uv run --with playwright python tools/play_slice.py ...\n"
            "(--plan and --self-test need no browser.)\n"
            "original error: %s" % exc
        )
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=not headed)
    context = browser.new_context(
        viewport=VIEWPORT,
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True,
    )
    page = context.new_page()
    page.set_default_timeout(5000)
    return playwright, browser, context, page


def play(args):
    html_path = Path(args.html).resolve()
    if not html_path.is_file():
        raise SystemExit("no such woven file: %s" % html_path)
    world_path = Path(args.world) if args.world else derive_world(html_path, args.pack)
    if world_path is None or not Path(world_path).is_file():
        raise SystemExit("no world.json for %s; pass --world worlds/mending-shift/world.json"
                         % html_path)
    world = load_world(world_path)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    playwright, browser, context, page = open_page(html_path, args.headed)
    try:
        page.goto(html_path.as_uri())
        game = Game(page, world, outdir, html_path=html_path, world_path=world_path,
                    step_timeout=args.step_timeout, try_verbs=args.try_verbs,
                    talk=not args.no_talk)
        report = game.run()
        game.write_lines()
        path = write_report(report, outdir)
    finally:
        context.close()
        browser.close()
        playwright.stop()

    print_report(report, path)
    return report.exit


def plan(world, try_verbs=False):
    """The walk this run would take, printed, with no browser at all."""
    tiles = walkable(world)
    start = hero_start(world)
    phases = phase_order(world)
    print("phases: %s" % ", ".join(slug for slug, _ in phases))
    print("hero start: %s, walkable tiles: %d" % (list(start) if start else None, len(tiles)))
    problems = 0
    for slug, _tone in phases:
        print("\n%s" % slug)
        at = start
        for op, arg in phase_script(world, slug):
            if op == "verb":
                print("  %-30s %s" % (arg, "press the verb, expect a new line" if try_verbs
                                      else "skipped (--try-verbs presses it)"))
                continue
            if op == "mend":
                print("  %-30s press Mend once, expect %s" % (arg["id"], arg.get("output")))
                continue
            label = arg.who + (" (again, after the mend)" if op == "again" else "")
            if arg.tile is None:
                print("  %-30s %-11s NO COORDINATES (%s)" % (label, arg.kind, ", ".join(arg.rules)))
                problems += 1
                continue
            _tile, path = stand_tile(world, arg, at, tiles)
            if path is None:
                print("  %-30s %-11s at %-8s UNREACHABLE (%s)"
                      % (label, arg.kind, arg.tile, ", ".join(arg.rules)))
                problems += 1
                continue
            at = path[-1]
            print("  %-30s %-11s at %-8s %2d steps, ends %s (%s)"
                  % (label, arg.kind, arg.tile, len(path) - 1, path[-1], ", ".join(arg.rules)))
    turning = phases[0][0] if phases else None
    required = [r.get("id") for r in world.get("rules", [])
                if rule_status_kind(r) == "required" and turning in rule_phases(r)]
    print("\nrequired beats of %s: %d" % (turning, len(required)))
    for rid in required:
        print("  %s" % rid)
    expected = simulate(world, try_verbs)
    print("\nrules the plan expects to fire: %d/%d" % (len(expected), len(world.get("rules", []))))
    for rule in world.get("rules", []):
        if rule.get("id") not in expected:
            print("  not expected: %s: %s" % (rule.get("id"), why_unfireable(world, rule)))
    return 0 if problems == 0 else 1


def print_report(report, path):
    print("")
    print("phases reached: %d/%d" % (sum(1 for p in report.phases if p["reached"]),
                                     len(report.phases)))
    for phase in report.phases:
        print("  %d %-14s %-6s %s" % (phase["index"], phase["phase"],
                                       "ok" if phase["reached"] else "MISSED", phase["read_by"]))
    fired = [r for r in report.rules if r["status"] == "fired"]
    print("rules whose lines appeared: %d/%d" % (len(fired), len(report.rules)))
    if report.missing:
        print("expected rules that never fired:")
        for rid in report.missing:
            print("  %s" % rid)
    else:
        print("every expected rule fired")
    print("lines:  %s/lines.txt" % report.outdir)
    for shot in report.shots:
        print("shot:   %s" % shot)
    print("report: %s" % path)
    print("exit %d" % report.exit)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Play a woven VEFR pack slice through all its phases and report on it.")
    parser.add_argument("html", nargs="?", help="the woven pack HTML to open")
    parser.add_argument("--world", help="the pack's world.json (default: derived from the file name)")
    parser.add_argument("--pack", help="pack directory holding world.json")
    parser.add_argument("--out", default="out/play", help="where lines, shots and the report go")
    parser.add_argument("--step-timeout", type=float, default=STEP_TIMEOUT,
                        help="seconds one step may take (default: %(default)s)")
    parser.add_argument("--headed", action="store_true", help="watch it play")
    parser.add_argument("--try-verbs", action="store_true",
                        help="also press the verb buttons, for the uses-verb beats")
    parser.add_argument("--no-talk", action="store_true", help="do not press Interact on residents")
    parser.add_argument("--plan", action="store_true",
                        help="print the walk this run would take and exit, no browser")
    parser.add_argument("--self-test", action="store_true",
                        help="run the driver against a fake page and exit, no browser")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.plan and not args.html and not args.world:
        args.world = str(Path(__file__).resolve().parent.parent / "worlds" / "mending-shift" / "world.json")
    if not args.html and not args.world:
        parser.error("a woven pack HTML path is required (or --world with --plan)")
    world_path = Path(args.world) if args.world else derive_world(args.html, args.pack)
    if world_path is None or not Path(world_path).is_file():
        raise SystemExit("could not find world.json; pass --world worlds/mending-shift/world.json")
    if args.plan:
        return plan(load_world(world_path), args.try_verbs)
    return play(args)


# ------------------------------------------------------- the browserless test


class FakeElement:
    """The slice of Playwright's ElementHandle the driver uses."""

    def __init__(self, page, label, attrs=None):
        self.page = page
        self.label = label
        self.attrs = attrs or {}

    def click(self, timeout=None):
        self.page.activate(self.label)

    def inner_text(self):
        return "\n".join(line for _p, _s, line in self.page.lines)

    def get_attribute(self, name):
        if name == "class":
            return self.attrs.get("class", "")
        return self.attrs.get(name) or None


class FakePage:
    """A stand-in for a woven page: a yard, a log, a phase rail and a Rest.

    It answers the same calls the driver makes, moves the hero with the arrow
    keys, refuses to walk into a wall, fires `comes-near` rules on arrival and
    `phase-changes` rules on Rest, exactly as the woven player does. That makes
    the whole run - walking, waiting, matching, scoring, reporting - testable
    without a browser. It is a test double, not a game.
    """

    def __init__(self, world, outdir, silent=False, refuses=(), mute=(), deaf=False, mend=False):
        self.world = world
        self.deaf = deaf  # Talk answers with nothing at all, even in reach
        self.mend = mend  # the page offers a Mend control
        self.verbs = {}
        self.mute = {line for _w, line in mute}  # lines this page never shows
        self.refuses = set(refuses)  # legend-walkable tiles the game will not enter
        self.outdir = Path(outdir)
        self.lines = []
        self.silent = silent  # a page that never says anything
        self.tiles = walkable(world)
        self.phases = [slug for slug, _ in phase_order(world)]
        self.phase = self.phases[0]
        self.pos = hero_start(world) or (0, 0)
        self.log = FakeElement(self, "log")
        self.rest_el = FakeElement(self, "rest")
        self.talk_el = FakeElement(self, "talk")
        self.play_el = FakeElement(self, "play")
        self.mend_el = FakeElement(self, "mend")
        self.rail = {slug: FakeElement(self, "rail:%s" % slug, {"class": "phase-btn"})
                     for slug in self.phases}
        self.keyboard = self
        self.sync_rail()

    def sync_rail(self):
        """The rail marks the standing phase, the way the woven player does."""
        for slug, el in self.rail.items():
            el.attrs["class"] = "phase-btn active" if slug == self.phase else "phase-btn"

    # -- the Playwright calls the driver makes --
    def query_selector(self, selector):
        if selector == "#log":
            return self.log
        if selector == "[data-rest]":
            return self.rest_el
        if selector in TALK_SELECTORS:
            return self.talk_el
        if selector in MEND_SELECTORS:
            return self.mend_el if self.mend else None
        for verb in self.world.get("verbs", []) + ["Call"]:
            if selector in ("[data-verb='%s']" % verb, "button:has-text('%s')" % verb):
                return self.verbs.setdefault(verb, FakeElement(self, "verb:%s" % verb))
        if selector in ENTER_SELECTORS:
            return self.play_el
        for slug, el in self.rail.items():
            if selector == '#phase button[data-phase="%s"]' % slug or selector == '[data-phase="%s"]' % slug:
                return el
        return None

    def inner_text(self, selector):
        return "\n".join(line for _p, _s, line in self.lines)

    def query_selector_all(self, selector):
        return [self.talk_el, self.rest_el] + list(self.verbs.values())

    def evaluate(self, expr):
        if "VEFR_HERO_AT" in expr:
            return json.dumps({"x": self.pos[0], "y": self.pos[1], "region": "town"})
        if "STATE" in expr and "get" in expr:
            return json.dumps({"phase": self.phase, "hero": {"x": self.pos[0], "y": self.pos[1]}})
        return None

    def wait_for_timeout(self, ms):
        pass

    def screenshot(self, path=None, **kwargs):
        (self.outdir / Path(path).name).write_bytes(b"\x89PNG\r\n\x1a\n fake")

    def press(self, key):
        if key in ("r", "R"):
            return self.activate("rest")
        if key in ("f", "F"):
            return self.activate("talk")
        deltas = {"ArrowUp": (0, -1), "ArrowDown": (0, 1), "ArrowLeft": (-1, 0), "ArrowRight": (1, 0)}
        delta = deltas.get(key)
        if not delta:
            return None
        nxt = (self.pos[0] + delta[0], self.pos[1] + delta[1])
        if nxt in self.tiles and nxt not in self.refuses:
            self.pos = nxt
            self.arrive()
        return None

    # -- what the double does when a control is pressed --
    def emit(self, who, line):
        if not self.silent and line and line not in self.mute:
            self.lines.append((self.phase, "say", line if not who else "%s: %s" % (who, line)))

    def arrive(self):
        for rule in self.world.get("rules", []):
            when = rule.get("when", {})
            near = when.get("comes-near") if isinstance(when, dict) else None
            if not isinstance(near, dict) or self.phase not in rule_phases(rule):
                continue
            tile, kind = resolve_who(self.world, near.get("who", ""))
            # a resident's comes-near only fires from Talk, as in the player
            if kind == "poi" and manhattan(tile, self.pos) <= int(near.get("distance", 1)):
                for who, line in rule_lines(rule):
                    self.emit(who, line)

    def activate(self, label):
        if self.silent:
            return None
        if label == "play":
            return None
        if label == "rest":
            index = self.phases.index(self.phase)
            if index + 1 < len(self.phases):
                self.phase = self.phases[index + 1]
            self.sync_rail()
            for rule in self.world.get("rules", []):
                when = rule.get("when", {})
                if not isinstance(when, dict) or "phase-changes" not in when:
                    continue
                if when["phase-changes"].get("to") != self.phase:
                    continue
                for who, line in rule_lines(rule):
                    self.emit(who, line)
            self.arrive()
            return None
        if label == "mend":
            for recipe in mend_recipes(self.world).values():
                self.emit(None, recipe.get("say"))
            return None
        if label.startswith("verb:"):
            verb = label.split(":", 1)[1]
            for rule in self.world.get("rules", []):
                when = rule.get("when", {})
                if isinstance(when, dict) and when.get("uses-verb", {}).get("verb") == verb \
                        and self.phase in rule_phases(rule):
                    for who, line in rule_lines(rule):
                        self.emit(who, line)
            return None
        if label == "talk":
            if self.deaf:
                return None
            near = sorted((manhattan(self.pos, at), sid)
                          for sid, at in speaker_coords(self.world).items())
            if not near:
                return None
            d, sid = near[0]
            if d > TALK_REACH:
                self.emit(None, "No one is close enough to talk to.")
                return None
            speaker = self.world["speakers"][sid]
            for rule in self.world.get("rules", []):
                when = rule.get("when", {})
                n = when.get("comes-near") if isinstance(when, dict) else None
                if isinstance(n, dict) and n.get("who") == sid and d <= int(n.get("distance", 1)) \
                        and self.phase in rule_phases(rule):
                    for who, line in rule_lines(rule):
                        self.emit(who, line)
            seed = speaker.get("seeds", {}).get(self.phase)
            if isinstance(seed, str):
                self.emit(speaker.get("name", sid), seed)
            return None
        return None


def self_test():
    """Run the driver twice against the fake page: a page that speaks and a
    page that does not. Exit 0 only if the first run passes and the second
    fails, which is what proves the scoring is doing something."""
    world_path = Path(__file__).resolve().parent.parent / "worlds" / "mending-shift" / "world.json"
    if not world_path.is_file():
        print("no world.json at %s" % world_path, file=sys.stderr)
        return 2
    world = load_world(world_path)
    failures = []

    # 1. the plan, from the real pack
    tiles = walkable(world)
    start = hero_start(world)
    check(world.get("phases") and len(world["phases"]) == 4, "four phases", failures)
    for slug, _tone in phase_order(world):
        for target, path in plan_phase(world, slug, start, tiles):
            check(target.tile is not None, "%s: %r resolves to a tile" % (slug, target.who), failures)
            check(path is not None, "%s: %r is walkable from %s" % (slug, target.who, start), failures)
            if path:
                for a, b in zip(path, path[1:]):
                    check(manhattan(a, b) == 1, "%s: %r path step %s->%s is one tile"
                          % (slug, target.who, a, b), failures)
    turning = phase_order(world)[0][0]
    required = [r.get("id") for r in world["rules"]
                if rule_status_kind(r) == "required" and turning in rule_phases(r)]
    check("the-turning-opens" in required, "the-turning-opens is a required beat", failures)
    check(len(required) == 4, "four required beats at The Turning (got %d)" % len(required), failures)

    # 2. a full run against a page that speaks
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        page = FakePage(world, tmp)
        game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
        report = game.run()
        path = write_report(report, tmp)
        game.write_lines()
        check(report.exit == 0, "a speaking page exits 0", failures)
        check(len(report.phases) == 4, "four phases visited", failures)
        check(all(p["reached"] for p in report.phases), "every phase reached", failures)
        check(report.missing == [], "no expected rule missing", failures)
        check(len(report.shots) == 4, "one screenshot per phase", failures)
        check(game.rest_control and game.rest_control.startswith("button"),
              "Rest used the [data-rest] button", failures)
        check(game.hero_probe == "VEFR_HERO_AT", "hero position read from VEFR_HERO_AT", failures)
        walked = [t for p in report.phases for t in p["targets"]]
        check(all(t["walked"] for t in walked), "every target walked to", failures)
        check(any(t.get("talked") for t in walked if t["kind"] == "speaker"),
              "a resident was talked to", failures)
        check(path.is_file() and (tmp / "report.json").is_file() and (tmp / "lines.txt").is_file(),
              "report.md, report.json and lines.txt written", failures)
        said = [norm(line) for _p, _s, line in game.log_lines]
        check(len(said) == len(set(said)), "no line recorded twice", failures)
        check(len(said) > 20, "the run recorded the game's lines (%d)" % len(said), failures)

    # 3. a page that says nothing must fail the run
    with tempfile.TemporaryDirectory() as tmp:
        page = FakePage(world, tmp, silent=True)
        game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
        report = game.run()
        write_report(report, tmp)
        check(report.exit == 1, "a silent page exits 1", failures)
        check("the-turning-opens" in report.missing,
              "the-turning-opens is named as never fired", failures)

    # 3b. a tile the legend calls walkable but the game refuses: the walk must
    # bar that tile (not the hero's own), route around it, and still finish
    first = next((path for slug, _t in phase_order(world)[:1]
                  for target, path in plan_phase(world, slug, start, tiles)
                  if path and len(path) > 2), None)
    refused = None
    if first:
        refused = next((t for t in first[1:-1]
                        if bfs(tiles - {t}, start, first[-1], frozenset()) is not None), None)
    check(refused is not None, "a refusable tile with a way round exists", failures)
    if refused:
        with tempfile.TemporaryDirectory() as tmp:
            page = FakePage(world, tmp, refuses=[refused])
            game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
            report = game.run()
            write_report(report, tmp)
            check(refused in game.blocked, "legend-walkable but refused: the refused tile is barred", failures)
            check(start not in game.blocked and len(game.blocked) == 1,
                  "legend-walkable but refused: no other tile is barred", failures)
            check(report.exit == 0 and report.missing == [],
                  "legend-walkable but refused: the walk routes round it and the run passes", failures)

    # 3c. a required rule outside The Turning that never fires is named, and
    # the exit code and report.missing agree
    with tempfile.TemporaryDirectory() as tmp:
        later = next((r for r in world["rules"] if rule_status_kind(r) == "required"
                      and turning not in rule_phases(r)
                      and when_kind(r) == "comes-near"), None)
        if later is None:
            check(False, "a required comes-near rule outside The Turning exists", failures)
        else:
            page = FakePage(world, tmp, mute=rule_lines(later))
            game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
            report = game.run()
            check(report.missing == [later["id"]] and report.exit == 1,
                  "a muted %s rule is the one rule named, and the run exits 1" % later["id"], failures)

    # 4. a page with no hero state in it must still finish, and say so
    with tempfile.TemporaryDirectory() as tmp:
        page = FakePage(world, tmp)
        page.evaluate = lambda expr: None
        game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
        report = game.run()
        check(game.hero_probe == "unverified", "no state means unverified movement", failures)
        check(any("NOT VERIFIED" in note for note in report.notes),
              "the report says the walk was unverified", failures)
        check(len(report.phases) == 4, "a stateless page still visits four phases", failures)
        check(all(p["read_by"] == "rail" for p in report.phases),
              "with no player state the rail is what reads the phase", failures)
        check(all(p["reached"] for p in report.phases),
              "a stateless page reaches every phase", failures)

    # 5. a refused step is seen, not taken at its word
    with tempfile.TemporaryDirectory() as tmp:
        page = FakePage(world, tmp, refuses=[(6, 4)])
        game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
        before = game.hero_pos()
        check(game.press_dir(0, -1) is False and game.hero_pos() == before,
              "a refused step reports False and leaves the hero's tile alone", failures)

    # 6. a talk that says nothing, and a talk beyond two tiles, are named and not counted
    with tempfile.TemporaryDirectory() as tmp:
        page = FakePage(world, tmp, deaf=True)
        game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
        game.enter_play()
        page.pos = (5, 5)
        check(game.talk_to("Roald Fisk", "roald-fisk") is False, "a silent talk in reach returns False", failures)
        check(any("talk to Roald Fisk at distance 1 produced nothing" in n for n in game.report.notes),
              "a silent talk is noted with its distance", failures)
    with tempfile.TemporaryDirectory() as tmp:
        page = FakePage(world, tmp)
        game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True)
        game.enter_play()
        page.pos = (1, 1)
        check(game.talk_to("Roald Fisk", "roald-fisk") is False, "a talk beyond two tiles returns False", failures)
        check(any("talk to Roald Fisk at distance" in n and "produced nothing" in n for n in game.report.notes),
              "a refused talk is noted", failures)
        page.pos = (5, 5)
        check(game.talk_to("Roald Fisk", "roald-fisk") is True, "a talk in reach is verified by a line naming them", failures)

    # 7. verbs and the Mend are verified by their effect
    for offered in (True, False):
        with tempfile.TemporaryDirectory() as tmp:
            page = FakePage(world, tmp, mend=offered)
            game = Game(page, world, tmp, html_path="fake.html", world_path=world_path, quiet=True,
                        try_verbs=True)
            report = game.run()
            verbs = [v for p in report.phases for v in p.get("verbs", [])]
            check(verbs and all(v["pressed"] for v in verbs), "every verb pressed produced a line", failures)
            mends = [p["mend"] for p in report.phases if "mend" in p]
            check(len(mends) == 1 and mends[0]["made"] is offered,
                  "the Mend is pressed once and %s" % ("verified" if offered else "reported as not offered"), failures)
            check(offered or any("no Mend control is offered" in n for n in report.notes),
                  "an absent Mend control is said so", failures)

    if failures:
        print("self-test: %d FAILED" % len(failures))
        for line in failures:
            print("  FAIL %s" % line)
        return 1
    print("self-test: all checks passed (plan, a speaking page, a silent page, a legend-walkable-but-refused tile, a stateless page, a refused step, a silent and a far talk, verbs, the Mend)")
    return 0


def check(condition, description, failures):
    if not condition:
        failures.append(description)


if __name__ == "__main__":
    sys.exit(main())