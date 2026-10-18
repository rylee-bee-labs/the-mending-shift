#!/usr/bin/env python3
"""M2b acceptance: the Mending Shift pack, its rules, and the three outcomes.

Checks the pack against the four canon bibles in `bible/` (world, cast, systems,
slice), all of which Rylee approved on 2026-10-17 and which this script never
edits. It is stdlib-only and holds two lines at once.

M2a's line: the four phases and their slugs, the time block, every speaker
seeded in every phase with a voice file on disk, full written names only, the
eight item records, and the six recipes with the fid-and-coat fusion keeping
Climb and Wade and carrying Shelter.

M2b's line: the five beats of `bible/slice.md` as rules. Every beat has its
rules, every phase is read by at least one rule, every `say.who` is a speaker
id, every resident's line for every phase is in the rules, each of the three
outcomes has a rule whose condition can actually be met, and no rule names an
item outside the eight canon items and the six heirlooms. The three outcomes
are also proved to partition the satchel: exactly one of their rules reads any
one state out.

With VEFR_DIR set it also runs `vefr check` against the pack and requires exit
0. Without it, it says so and skips. Exit status is 0 only when every check
holds.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent

PHASE_SLUGS = ["the-turning", "low-water", "the-run", "slack-water"]

TIME_BLOCK = {"rest": True, "rail": "locked", "persist": True}

# bible/cast.md writes these names; bible/systems.md's name rule asks for the
# full written name in a `say`, never a short form. The short forms below are
# every given name and every surname in those seven written names.
FULL_NAMES = {
    "warden-ottmar-vell": "Warden Ottmar Vell",
    "roald-fisk": "Roald Fisk",
    "sable-kearn": "Sable Kearn",
    "margit-brack": "Margit Brack",
    "tam-verrow": "Tam Verrow",
    "maud-bray": "Maud Bray",
    "grissel-toft": "Grissel Toft",
}

SHORT_FORMS = {
    "Ottmar", "Roald", "Sable", "Margit", "Tam", "Maud", "Grissel",
    "Vell", "Fisk", "Kearn", "Brack", "Verrow", "Bray", "Toft",
}

# bible/systems.md's eight item records: id -> granted verb, button words, and
# the verb it rewrites where systems.md gives one (`writes`).
ITEMS = {
    "bone-fid": ("Climb", "climb, and do it quiet", "Climb"),
    "tar-coat": ("Wade", "wade, and keep your hands", "Wade"),
    "tin-whistle": ("Call", "call a name across the water, and be heard back", None),
    "bench-knife": ("Unpick", "unpick a mend, and go the whole way down", None),
    "tarred-line": ("Haul", "haul, with the weight on the line and not on you", None),
    "bend-hook": ("Hook", "hook, and hold on from where you are standing", None),
    "shuttered-lamp": ("Steady", "stand steady on the thing that is moving", None),
    "winch-bar": ("Haul", "haul from the rack, both feet on the stone", "Haul"),
}

REACHABLE = ["bone-fid", "tar-coat", "tin-whistle", "bench-knife"]
BACKLOG = ["tarred-line", "bend-hook", "shuttered-lamp", "winch-bar"]

# M2b. The five beats of bible/slice.md, each with the rules that carry it, and
# the three outcomes of the shingle, keyed on what the satchel holds at the end.
# A rule may be named by more than one beat where the bible puts it in two.
BEATS = {
    "1 The Turning": [
        "the-turning-opens",
        "the-slow-climb-fails-at-the-wall",
        "the-hands-under-wade-fails-at-the-causeway-foot",
        "tam-verrow-offers-the-bent-hook",
        "grissel-toft-hands-over-the-heat-glove",
        "roald-fisk-hands-over-the-coat",
    ],
    "2 Low Water": [
        "low-water-comes-in",
        "the-warden-hands-over-the-fid",
        "the-knife-comes-off-the-rack",
        "the-repairs-are-laid-at-the-bench",
        "the-quiet-coat-is-laid-at-the-bench",
        "the-rack-offers-the-preview",
        "the-rack-fuses-the-fid-and-the-coat",
    ],
    "3 The Run": [
        "the-run-floods",
        "margit-brack-hands-over-the-whistle",
        "the-crossing-is-refused-at-the-causeway-head",
    ],
    "4 Slack Water, the crossing": [
        "slack-water-sets",
        "the-note-carries-across-the-water",
        "she-comes-across-under-the-quiet-coat",
        "she-comes-across-one-crossing-at-a-time",
    ],
    "5 The shingle": [
        "the-shingle-is-signed",
        "the-shingle-is-deferred",
        "the-shingle-is-refused-empty",
        "the-shingle-is-refused-over-a-refused-object",
    ],
}

OUTCOMES = {
    "signed": ["the-shingle-is-signed"],
    "deferred": ["the-shingle-is-deferred"],
    "refused": ["the-shingle-is-refused-empty",
                "the-shingle-is-refused-over-a-refused-object"],
}

# A pack may name at most this many rules (docs/adr/0004-scoped-rules.md).
RULE_LIMIT = 40

RECIPES = {
    "fuse-fid-coat": (["bone-fid", "tar-coat"], "Shelter", "quiet-coat",
                      "the quiet coat",
                      "Two patches now, one coat, and the wall and the water on the same body."),
    "fuse-whistle-line": (["tin-whistle", "tarred-line"], "Reach", "thrown-whistle",
                          "the thrown whistle",
                          "Twelve fathoms with a whistle on the end, for calling somebody you cannot reach."),
    "fuse-hook-line": (["bend-hook", "tarred-line"], "Anchor", "grapnel-line",
                       "the grapnel line",
                       "Line out and the hook on it, and it holds on the second pull."),
    "fuse-lamp-knife": (["shuttered-lamp", "bench-knife"], "Trace", "dark-mend",
                        "the dark mend",
                        "Half a lamp and a blunt point, for finding the seam somebody unpicked first."),
    "fuse-bar-hook": (["winch-bar", "bend-hook"], "Draw", "short-haul",
                      "the short haul",
                      "The bar and the hook together, and the pull comes to you instead of going."),
    "fuse-knife-line": (["bench-knife", "tarred-line"], "Lay", "spliced-line",
                        "the spliced line",
                        "Line spliced with a blunt point, and laid out straight for once."),
}

FAILURES = []


def check(condition, message):
    """Record one failed check, or nothing."""
    if not condition:
        FAILURES.append(message)


def verbs_of(item):
    """The verbs one item record grants, as a set."""
    return {g["verb"] for g in item.get("grants") or []}


def said_names(rules):
    """Every name a rule puts in a resident's mouth."""
    names = []
    for rule in rules:
        for action in rule.get("then") or []:
            if isinstance(action, dict) and isinstance(action.get("say"), dict):
                names.append(action["say"].get("who"))
    return [n for n in names if n]


def handed_over(rules):
    """Every item id some rule puts in the bag."""
    given = []
    for rule in rules:
        for action in rule.get("then") or []:
            if isinstance(action, dict) and "give" in action:
                given.append(action["give"])
    return given


def check_world(world):
    check(world.get("name") == "mending-shift",
          "world.json name must be 'mending-shift'")
    check(world.get("title") == "The Mending Shift",
          "world.json title must be 'The Mending Shift'")

    phases = world.get("phases") or {}
    check(list(phases) == PHASE_SLUGS,
          "phases must be exactly the four slugs in order: %r" % (list(phases),))
    for slug in PHASE_SLUGS:
        sentence = phases.get(slug)
        check(isinstance(sentence, str) and sentence.strip().endswith("."),
              "phase '%s' needs a tone sentence from world.md/systems.md" % slug)

    check(world.get("time") == TIME_BLOCK,
          "time block must be %r, got %r" % (TIME_BLOCK, world.get("time")))


def check_speakers(world):
    speakers = world.get("speakers") or {}
    check(set(speakers) == set(FULL_NAMES),
          "speakers must be exactly the seven residents cast.md writes: %r"
          % sorted(speakers))

    for key, full in FULL_NAMES.items():
        speaker = speakers.get(key)
        if speaker is None:
            continue
        name = speaker.get("name")
        check(name == full,
              "speaker '%s' must carry the full written name %r, got %r"
              % (key, full, name))
        check(name not in SHORT_FORMS,
              "speaker '%s' uses the short form %r" % (key, name))
        check(isinstance(speaker.get("at"), list) and len(speaker["at"]) == 2,
              "speaker '%s' needs a position [x, y]" % key)

        voice_file = speaker.get("voice_file")
        check(isinstance(voice_file, str) and voice_file,
              "speaker '%s' needs a voice_file" % key)
        if voice_file:
            path = PACK / voice_file
            check(path.is_file(), "voice file missing: %s" % voice_file)
            frag = PACK / (voice_file[: -len(".md")] + ".fragments.md")
            check(frag.is_file(), "fragments file missing: %s"
                  % frag.relative_to(PACK))

        seeds = speaker.get("seeds") or {}
        for slug in PHASE_SLUGS:
            check(slug in seeds and isinstance(seeds[slug], str) and seeds[slug].strip(),
                  "speaker '%s' needs a seed for phase '%s'" % (key, slug))

    # The engine's `say.who` is the speaker id; the full written name is that speaker's `name`.
    for who in said_names(world.get("rules") or []):
        speaker = (world.get("speakers") or {}).get(who) or {}
        check(speaker.get("name") in FULL_NAMES.values(),
              "a rule says a line as %r, which is not a speaker with a full written name" % who)


def check_items(world):
    catalog = world.get("items") or {}
    for item_id in ITEMS:
        check(item_id in catalog, "item record missing: %s" % item_id)
    for _, (_, _, output, _, _) in RECIPES.items():
        check(output in catalog,
              "recipe output is not an item the pack declares: %s" % output)

    for item_id, (verb, label, writes) in ITEMS.items():
        item = catalog.get(item_id) or {}
        check(isinstance(item.get("name"), str) and item["name"].strip(),
              "item '%s' needs a name" % item_id)
        check(item.get("grants") == [{"verb": verb, "label": label}],
              "item '%s' must grant exactly %r, got %r"
              % (item_id, [{"verb": verb, "label": label}], item.get("grants")))
        check(item.get("writes") == writes,
              "item '%s' writes %r, got %r" % (item_id, writes, item.get("writes")))
        if writes is not None:
            # The rewrite rides the button words and `writes`; the engine's
            # `changes` has only `atk` today, and this yard grants no number,
            # so the change is carried at zero.
            check(item.get("changes") == {writes: {"atk": 0}},
                  "item '%s' must change %r, got %r"
                  % (item_id, writes, item.get("changes")))
            check(writes in verbs_of(item),
                  "item '%s' writes %r but does not grant it" % (item_id, writes))

    # The fid-and-coat fusion, read straight out of the data.
    coat = catalog.get("quiet-coat") or {}
    kept = verbs_of(catalog.get("bone-fid") or {}) | verbs_of(catalog.get("tar-coat") or {})
    check(kept == {"Climb", "Wade"},
          "the fid and the coat between them bring %r, expected Climb and Wade"
          % sorted(kept))
    check(verbs_of(coat) == kept | {"Shelter"},
          "the quiet coat must keep Climb and Wade and carry Shelter, got %r"
          % sorted(verbs_of(coat)))


def check_recipes(world):
    # keeps / carries / read_aloud are systems.md's design keys; the engine's recipe holds only id, inputs,
    # output and say, so they live in design/recipes.json and the output item's grants carry the behaviour.
    design = json.loads((PACK / "design" / "recipes.json").read_text(encoding="utf-8"))["recipes"]
    items = world.get("items") or {}
    recipes = world.get("recipes") or []
    by_id = {r.get("id"): r for r in recipes if isinstance(r, dict)}
    check(set(by_id) == set(RECIPES),
          "recipes must be exactly the six of systems.md: %r" % sorted(by_id))

    for recipe_id, (inputs, carries, output, read_aloud, say) in RECIPES.items():
        recipe = by_id.get(recipe_id)
        if recipe is None:
            continue
        check(recipe.get("inputs") == inputs,
              "recipe '%s' inputs must be %r, got %r"
              % (recipe_id, inputs, recipe.get("inputs")))
        extra = sorted(set(recipe) - {"id", "inputs", "output", "say"})
        check(not extra, "recipe '%s' holds keys the engine refuses: %r" % (recipe_id, extra))
        recipe = dict(recipe, **(design.get(recipe_id) or {}))
        check(carries in verbs_of(items.get(output) or {}),
              "recipe '%s': its output %r must grant the carried verb %r" % (recipe_id, output, carries))
        check(recipe.get("keeps") == inputs,
              "recipe '%s' keeps must name both inputs, got %r"
              % (recipe_id, recipe.get("keeps")))
        check(recipe.get("carries") == carries,
              "recipe '%s' must carry %r, got %r"
              % (recipe_id, carries, recipe.get("carries")))
        check(recipe.get("output") == output,
              "recipe '%s' output must be %r, got %r"
              % (recipe_id, output, recipe.get("output")))
        check(recipe.get("read_aloud") == read_aloud,
              "recipe '%s' read_aloud must be %r, got %r"
              % (recipe_id, read_aloud, recipe.get("read_aloud")))
        check(recipe.get("say") == say,
              "recipe '%s' say must be systems.md's line, got %r"
              % (recipe_id, recipe.get("say")))


def check_reachability(world):
    rules = world.get("rules") or []
    given = handed_over(rules)
    check(sorted(set(given)) == sorted(REACHABLE),
          "only the four reachable items may be handed over, got %r" % sorted(set(given)))
    for item_id in REACHABLE:
        check(item_id in given, "reachable item never reaches the bag: %s" % item_id)
    for item_id in BACKLOG:
        check(item_id not in given,
              "backlog item is placed in this slice and must stay unreachable: %s" % item_id)
    for rule in rules:
        check("id" in rule, "a rule has no id: %r" % rule)


def check_town(world):
    town = world.get("town") or {}
    rows = town.get("map") or []
    check(all(len(r) == 12 for r in rows) and len(rows) == 10,
          "the town map must be 12 wide by 10 tall")
    legend = town.get("legend") or {}
    walkable = {c for c, entry in legend.items() if not entry.get("solid")}
    if rows:
        # The engine's shape is {"x,y": "label"}; a label may sit on its solid prop (the shed, the wall) as
        # long as a walkable tile is near it, which `vefr check` measures.
        for key, name in (town.get("pois") or {}).items():
            try:
                x, y = (int(v) for v in key.split(","))
            except ValueError:
                check(False, "poi key %r must be 'x,y' (the label %r is the value)" % (key, name))
                continue
            check(0 <= x < len(rows[0]) and 0 <= y < len(rows),
                  "poi '%s' is off the map" % name)
        for key, speaker in (world.get("speakers") or {}).items():
            at = speaker.get("at")
            if not (isinstance(at, list) and len(at) == 2):
                continue
            x, y = at
            if not (0 <= x < len(rows[0]) and 0 <= y < len(rows)):
                check(False, "speaker '%s' stands off the map" % key)
                continue
            check(rows[y][x] in walkable,
                  "speaker '%s' stands on the solid tile %r" % (key, rows[y][x]))


def conditions_of(rule):
    """Every condition in a rule's `if`, flattened out of `not`/`all-of`."""
    found = []

    def walk(node):
        if not isinstance(node, dict):
            return
        for key, value in node.items():
            if key == "all-of":
                for child in value:
                    walk(child)
            elif key == "not":
                walk(value)
            else:
                found.append((key, value))

    walk({"all-of": rule.get("if") or []})
    return found


def reads_phase(rule, slug):
    """Whether a rule reads a phase: a `phase` condition, or a change into it."""
    if (rule.get("when") or {}).get("phase-changes", {}).get("to") == slug:
        return True
    return any(key == "phase" and value == slug
               for key, value in conditions_of(rule))


def evaluate(condition, items, flags, phase):
    """One condition against one possible state of the satchel and the shift."""
    if "has" in condition:
        return condition["has"] in items
    if "flag" in condition:
        return (condition["flag"] in flags) == bool(condition.get("is"))
    if "phase" in condition:
        return condition["phase"] == phase
    if "not" in condition:
        return not evaluate(condition["not"], items, flags, phase)
    if "all-of" in condition:
        return all(evaluate(child, items, flags, phase)
                   for child in condition["all-of"])
    raise ValueError("acceptance cannot evaluate the condition %r" % (condition,))


def condition_is_reachable(rule):
    """Whether some satchel, flag set and hour makes a rule's `if` true.

    Only the items, flags and phase the rule itself names can matter, so the
    search is small: every subset of the named items, every set of the named
    flags, and each of the four hours.
    """
    items, flags = set(), set()
    for key, value in conditions_of(rule):
        if key == "has":
            items.add(value)
        elif key == "flag":
            flags.add(value)
        elif key == "not":
            for inner_key, inner_value in conditions_of({"if": [value]}):
                if inner_key == "has":
                    items.add(inner_value)
                elif inner_key == "flag":
                    flags.add(inner_value)

    for mask in range(1 << len(items)):
        carried = {item for i, item in enumerate(sorted(items)) if mask >> i & 1}
        for flag_mask in range(1 << len(flags)):
            standing = {flag for i, flag in enumerate(sorted(flags))
                        if flag_mask >> i & 1}
            for slug in PHASE_SLUGS:
                try:
                    met = all(evaluate(condition, carried, standing, slug)
                              for condition in rule.get("if") or [])
                except ValueError as failure:
                    FAILURES.append("rule '%s': %s" % (rule.get("id"), failure))
                    return False
                if met:
                    return True
    return False


def check_outcome_partition(by_id):
    """Exactly one of the shingle's rules reads the slate out of any satchel.

    Only the items, flags and hours the outcome rules themselves name can
    matter, so every state of those is walked at the hour the shingle is read
    at: no satchel may read twice, and none may read nothing at all.
    """
    rules = [(r, by_id[r]) for ids in OUTCOMES.values() for r in ids if r in by_id]
    # The partition below reads only `if`; every outcome must also be reachable the same way, by
    # walking up to the warden, or a state could "match" a rule the player can never trigger.
    for rule_id, rule in rules:
        near = (rule.get("when") or {}).get("comes-near") or {}
        check(near.get("who") == "warden-ottmar-vell",
              "outcome rule '%s' is not triggered by coming near the warden (when: %r)"
              % (rule_id, rule.get("when")))
    items, flags, hours = set(), set(), set()
    for _, rule in rules:
        for key, value in conditions_of(rule):
            if key == "has":
                items.add(value)
            elif key == "flag":
                flags.add(value)
            elif key == "phase":
                hours.add(value)
            elif key == "not":
                for inner_key, inner_value in conditions_of({"if": [value]}):
                    if inner_key == "has":
                        items.add(inner_value)
                    elif inner_key == "flag":
                        flags.add(inner_value)
    check(len(hours) == 1,
          "the shingle is read at one hour, but its rules name %r" % sorted(hours))

    for mask in range(1 << len(items)):
        carried = {item for i, item in enumerate(sorted(items)) if mask >> i & 1}
        for flag_mask in range(1 << len(flags)):
            standing = {flag for i, flag in enumerate(sorted(flags))
                        if flag_mask >> i & 1}
            for slug in sorted(hours):
                met = [rule.get("id") for _, rule in rules
                       if all(evaluate(condition, carried, standing, slug)
                              for condition in rule.get("if") or [])]
                if len(met) != 1:
                    check(False,
                          "a satchel of %r with flags %r at '%s' is read out by "
                          "%r; exactly one outcome must read it"
                          % (sorted(carried), sorted(standing), slug, met))
                    return


SPEECH_BOX = 280   # the engine's speech box: `vefr check` refuses a longer say line


def check_say_lengths(world):
    for rule in world.get("rules") or []:
        for action in rule.get("then") or []:
            if not isinstance(action, dict) or "say" not in action:
                continue
            say = action["say"]
            line = say.get("line") if isinstance(say, dict) else say
            check(isinstance(line, str) and line.strip() != "",
                  "rule '%s' has a say action with no plain line in it (%r)" % (rule.get("id"), say))
            if isinstance(line, str):
                check(len(line) <= SPEECH_BOX,
                      "rule '%s' says a %d-character line; the speech box holds %d (split it into two say actions)"
                      % (rule.get("id"), len(line), SPEECH_BOX))


def check_rules(world):
    """The M2b line: the beats, the phases, the speakers, the outcomes."""
    rules = world.get("rules") or []
    by_id = {}
    for rule in rules:
        rule_id = rule.get("id")
        check(rule_id and rule_id not in by_id,
              "a rule has no id, or repeats one: %r" % (rule_id,))
        if rule_id and rule_id not in by_id:
            by_id[rule_id] = rule
        # `once` defaults to true, so a rule that means the opposite must say so.
        check("once" in rule,
              "rule '%s' leaves `once` to the default; systems.md asks for it "
              "to be written deliberately" % rule_id)
    check(len(rules) <= RULE_LIMIT,
          "a pack may name at most %d rules, this one names %d"
          % (RULE_LIMIT, len(rules)))

    for beat, needed in BEATS.items():
        for rule_id in needed:
            check(rule_id in by_id, "beat '%s' has no rule: %s" % (beat, rule_id))

    for slug in PHASE_SLUGS:
        check(any(reads_phase(rule, slug) for rule in rules),
              "no rule reads the phase '%s'" % slug)

    # Every `say.who` is a speaker id, and every resident's line for every phase
    # is in the rules, not only in the seeds the weave reads.
    speakers = world.get("speakers") or {}
    said = []
    for rule in rules:
        for action in rule.get("then") or []:
            if isinstance(action, dict) and isinstance(action.get("say"), dict):
                who = action["say"].get("who")
                said.append((who, action["say"].get("line")))
                check(who in speakers,
                      "rule '%s' says a line as %r, which is not a speaker id"
                      % (rule.get("id"), who))
    for key, speaker in speakers.items():
        for slug in PHASE_SLUGS:
            line = (speaker.get("seeds") or {}).get(slug)
            check((key, line) in said,
                  "no rule says %s's line for phase '%s'" % (speaker.get("name"), slug))

    # The three outcomes are keyed on the satchel, each one is reachable, and
    # they partition it: exactly one reads the slate out of any satchel.
    for outcome, rule_ids in OUTCOMES.items():
        reachable = [r for r in rule_ids
                     if r in by_id and condition_is_reachable(by_id[r])]
        check(reachable,
              "outcome '%s' has no rule whose condition can be met" % outcome)
    check_outcome_partition(by_id)

    # Every flag a rule sets is declared where the engine reads it.
    declared = set(world.get("flags") or {})
    for rule in rules:
        for action in rule.get("then") or []:
            if isinstance(action, dict) and "set" in action:
                check(action["set"] in declared,
                      "rule '%s' sets the undeclared flag '%s'"
                      % (rule.get("id"), action["set"]))
    for flag in declared:
        check(any(isinstance(action, dict) and action.get("set") == flag
                  for rule in rules for action in rule.get("then") or []),
              "flag '%s' is declared and never set" % flag)


def check_named_items(world):
    """No rule names an item outside the eight canon items and six heirlooms."""
    allowed = set(ITEMS) | {output for _, (_, _, output, _, _) in RECIPES.items()}
    for rule in world.get("rules") or []:
        named = []
        for key, value in conditions_of(rule):
            if key == "has":
                named.append(value)
            elif key == "not":
                named.extend(v for k, v in conditions_of({"if": [value]})
                             if k == "has")
        for action in rule.get("then") or []:
            if isinstance(action, dict):
                for key in ("give", "takes"):
                    if key in action:
                        named.append(action[key])
        for item_id in named:
            check(item_id in allowed,
                  "rule '%s' names '%s', which is not one of the eight canon "
                  "items or the six heirlooms" % (rule.get("id"), item_id))


def run_vefr_check():
    """`vefr check` when VEFR_DIR names an engine checkout; skipped without it."""
    engine = os.environ.get("VEFR_DIR")
    if not engine:
        print("vefr check: SKIPPED (no VEFR_DIR)")
        return True
    command = ["uv", "run", "--project", engine, "vefr", "check", "--pack", str(PACK)]
    print("vefr check: %s" % " ".join(command))
    done = subprocess.run(command)
    if done.returncode != 0:
        FAILURES.append("vefr check exited %d" % done.returncode)
        return False
    return True


def main():
    world = json.loads((PACK / "world.json").read_text(encoding="utf-8"))
    check_world(world)
    check_speakers(world)
    check_items(world)
    check_recipes(world)
    check_reachability(world)
    check_rules(world)
    check_say_lengths(world)
    check_named_items(world)
    check_town(world)
    run_vefr_check()

    if FAILURES:
        for failure in FAILURES:
            print("FAIL: %s" % failure)
        print("%d check(s) failed." % len(FAILURES))
        return 1
    print("M2b acceptance: PASS - 4 phases, 7 speakers, 8 items, 6 recipes, "
          "%d rules over 5 beats, 3 outcomes." % len(world.get("rules") or []))
    return 0


if __name__ == "__main__":
    sys.exit(main())
