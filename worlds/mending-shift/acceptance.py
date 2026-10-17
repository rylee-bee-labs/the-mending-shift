#!/usr/bin/env python3
"""M2a acceptance: the Mending Shift skeleton, residents, items and recipes.

Checks the pack against the four canon bibles in `bible/` (world, cast, systems,
slice), all of which Rylee approved on 2026-10-17 and which this script never
edits. It is stdlib-only and holds the line the brief drew: the four phases and
their slugs, the time block, every speaker seeded in every phase with a voice
file on disk, full written names only, the eight item records, and the six
recipes with the fid-and-coat fusion keeping Climb and Wade and carrying
Shelter.

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
    "grisel-toft": "Grissel Toft",
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

    for name in said_names(world.get("rules") or []):
        check(name in FULL_NAMES.values(),
              "a rule says a line with %r, which is not a full written name" % name)


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
        for name, (x, y) in (town.get("pois") or {}).items():
            check(0 <= x < len(rows[0]) and 0 <= y < len(rows),
                  "poi '%s' is off the map" % name)
            check(rows[y][x] in walkable,
                  "poi '%s' stands on the solid tile %r" % (name, rows[y][x]))
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
    check_town(world)
    run_vefr_check()

    if FAILURES:
        for failure in FAILURES:
            print("FAIL: %s" % failure)
        print("%d check(s) failed." % len(FAILURES))
        return 1
    print("M2a acceptance: PASS - 4 phases, 7 speakers, 8 items, 6 recipes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
