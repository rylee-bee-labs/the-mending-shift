CANON - approved by Rylee 2026-10-17 (gate 4, Project Home decision 228)

# Systems bible: the kit layer of The Mending Shift

Status: canon, approved by Rylee 2026-10-17 (gate 4). Later canon calls were decided by Claude and MiniMax on her
handover the same day; see `bible/GATE4-FOLLOWUPS.md`. Written for milestone M1 against `pitches/pitch-a.md`,
`bible/world.md` and `research/A2-feasibility.md`. Every rule below is canon as approved at gate 4. No visual
anchors are chosen here and none are implied.

The kit layer is the layer A2 did not study. `pitches/pitch-a.md` says so in its own words: the kit has
no A2 coverage and that gap is the top risk. So the shapes written here are the engine's *planned* shapes
for the kit layer, not shapes A2 verified. Where A2 has something to say about a shape this file leans
on, it is quoted through A2 rather than from the engine source.

## Items and the verbs they grant

The kit-runner starts with an apron, an empty satchel, four worn slots, and exactly two verbs that
visibly fail at the slipway: `Climb` in its slow form, which announces you to anyone above the wall, and
`Wade` in its form that puts both hands under the water. Nothing that carries is capable of anything
else at the start, and no object ever adds a number.

An item does one of two things and there is no third kind. It either **grants** a verb the kit-runner
did not have, or it **rewrites** a verb the kit-runner already has. In the planned shape a grant is a
list under `grants`, and a rewrite carries the same entry plus a `writes` key naming the verb it
replaces. A rewrite applies to the form you have; if you do not have that verb at all, the item grants
it outright instead. Two forms of one verb never both stand: the later one supersedes the earlier and
the superseded form sits inert in the satchel until something is fused, which is the whole point of
having a rack.

Two keys, then: `grants` is what the item gives, and `writes` is what it takes the old version of away
from you. Nothing else in an item record is load-bearing, and this needs saying plainly because several entries
below describe a cost in prose: where an item is written up as costing a hand, a habit or an arm, that is the yard
describing what it watches a kit-runner do with the thing. It is not a third kind, it is not read by any rule, and
it does not remove a capability. Only `grants` and `writes` change what the kit-runner is able to do. So where an
item's prose below talks about taking a dive away, it is talking about the superseded `Wade` form - the one that
puts both hands under the water - and not about a third kind of effect.

### The bone fid

Ottmar's fid, whittled flat by thirty years of the same grip.

```json
{
  "id": "bone-fid",
  "name": "Ottmar's bone fid",
  "grants": [{"verb": "Climb", "label": "climb, and do it quiet"}],
  "writes": "Climb"
}
```

It rewrites `Climb` from slow and audible to quiet. What changes: the wall stops being a place the yard
can hear you at. What you can no longer do afterwards is climb *deliberately* - take the wall slowly,
stopping where you want, in the full view of whoever is above you. That was never a convenience, it was
the only warning the causeway gave a resident that somebody was on it, and the fid takes the warning
with it. The climb is not faster. It is quieter and you can no longer choose the other.

### The waxed tar-coat

Roald Fisk's coat, waxed inside out by a diver and never got back.

```json
{
  "id": "tar-coat",
  "name": "Roald Fisk's waxed tar-coat",
  "grants": [{"verb": "Wade", "label": "wade, and keep your hands"}],
  "writes": "Wade"
}
```

It rewrites `Wade` so your hands stay above the water and stay usable. What changes: you can work a
thing - a line, a knot, a latch, a person - in the water instead of committing both hands to not
drowning. What you can no longer do afterwards is go under. The dive at the yard's foot on the hard during Low
Water is the `Wade` form that puts both hands under the water, and the coat supersedes that form, so what is gone
for the rest of the shift is the old hands-under form and not a third capability the coat takes away some other
way. The coat is waxed and thick and it is not made for submersion, which is why the hands stay out of it.
The record is about the hands of whoever is wearing it, and hands that stay above the water are hands that can
hold somebody else: that is what his owner's want is made of - one
passenger, held against you, at a walk, in front of anybody on the bank - and the coat as it stands,
with the wax gone hard and the seam open, will not do it. The single trip with the weather off both of
you is the inherited verb on the quiet coat.
The coat is also the coat of the yard's diver, handed over at the end of The Turning with the wax
gone hard at both elbows, and carrying it is the yard knowing where it went.

### The tin whistle

The night crew's whistle, on a loop of tarred twine, with three names ground into its rim.

```json
{
  "id": "tin-whistle",
  "name": "the night crew's tin whistle",
  "grants": [{"verb": "Call", "label": "call a name across the water, and be heard back"}]
}
```

It grants `Call`, which has no other source in the yard: put a name out over the channel and get an
answer, without being anywhere near the edge. Nothing is taken away, because nothing existed to take.
What it does take is privacy - every call you make is a resident hearing you need something, at the
hour you needed it. The pitch's rule that the yard's opinion is not "you are strong" but "you are
carrying somebody's coat and you did not give it back" is enforced most cheaply here.

### The tarred line

Twelve fathoms of tarred line, with the lay of it gone soft where it has been wet and dried
too many times.

```json
{
  "id": "tarred-line",
  "name": "twelve fathoms of tarred line",
  "grants": [{"verb": "Haul", "label": "haul, with the weight on the line and not on you"}]
}
```

It grants `Haul`: you can take a load - including a passenger's weight - onto the line and let the line
carry it, instead of putting it on your shoulder and announcing the crossing by your own two feet.
Nothing is rewritten and nothing is taken away, because the kit-runner had no `Haul` at all to lose. What
the entry describes is the habit of the thing: hauling comes with the line rather than with the arms, an
unanchored line will put you in the channel, and a yard that has watched somebody learn that puts the habit
in front of you twice. None of that is in the record; it is what the yard sees you do with a line.

### The bend hook

Tam Verrow's bent coat hook - he has already taken it off the rack, with the shank drawn about a third
of the way along and the bend set hard enough that it will not open back without a vice.

```json
{
  "id": "bend-hook",
  "name": "the bent coat hook",
  "grants": [{"verb": "Hook", "label": "hook, and hold on from where you are standing"}]
}
```

It grants `Hook`: catch and hold a line, a gunwale or a stanchion from a distance you do not have to
cross. Nothing is rewritten and nothing is taken away, because the kit-runner had no `Hook` to lose. What
the entry describes is the handling: a hook is a thing you use one handed, and the free hand is the one the
whistle wants when you are calling for somebody. The record does not take a hand; the arranging is yours.
The hook's reach is the hook doing `Hook`, and it is not a second verb: `Reach`, capitalised, is the
inherited verb on the thrown whistle and belongs to that heirloom alone.

### The shuttered lamp

The shed's lamp with a shutter on it that only opens halfway, so it lights a board and not a room.

```json
{
  "id": "shuttered-lamp",
  "name": "the shed's shuttered lamp",
  "grants": [{"verb": "Steady", "label": "stand steady on the thing that is moving"}]
}
```

It grants `Steady`: hold a position against the run of the water - the causeway when the channel is
moving fast, a plank with one end loose - long enough for somebody else to cross behind you. Nothing is
rewritten and nothing is taken away, because the kit-runner had no `Steady` to lose. What the entry
describes is what steadying takes: it is an arm's worth of holding for as long as the other person is on
the plank, which is why the yard watches somebody steady rather than help, and why the crossing it makes
possible is the crossing on which you are the last thing in the water. None of that is in the record.

### The bench knife

The bench's own knife, blunted at the point on purpose, because it is a mending knife and not a
cutting one.

```json
{
  "id": "bench-knife",
  "name": "the bench's blunt mending knife",
  "grants": [{"verb": "Unpick", "label": "unpick a mend, and go the whole way down"}]
}
```

It grants `Unpick`, and it is the only source of `Unpick` in the slice: without the knife in a worn
slot there is no fusing at all, so the knife is not a tool, it is the price of every heirloom the player
will build. Nothing is rewritten. What you lose is the peace of an intact mend - an object you have not
unpicked is somebody else's work, still their object, and the knife is what turns it into parts.

### The winch bar

The rack's winch bar, worn smooth in three places where hands have gone for thirty years.

```json
{
  "id": "winch-bar",
  "name": "the rack's winch bar",
  "grants": [{"verb": "Haul", "label": "haul from the rack, both feet on the stone"}],
  "writes": "Haul"
}
```

It rewrites `Haul` from the line's free-and-distant form to the bar's planted one: you take the pull
from the rack with your feet on stone and your hands in reach of the winch, and nothing about the pull
can run away from you. What you can no longer do afterwards is haul away from the rack at all - on the
channel, on the causeway, out in the dark - because the bar's version is anchored to the bench end of
the yard. If the kit-runner has no `Haul` at all when the bar is mended in, the bar grants it outright.

**The heat-glove is the one mendable object in the slice that is deliberately not an item record.** Grissel Toft's
heat-glove comes to the bench with the left cuff burnt out at the wrist and the cloth inside it gone to powder,
and the bone comes out of the fire on it: with that cuff as it is, nobody can get a whole hand under the collar
bone, so the pot's own work goes on unwound until the glove is mended. It has no id, no `grants` and no `writes`,
it is in no satchel and in no worn slot, and it appears in no recipe: it is handed over at the pot at The Turning
and goes straight back onto her own hand, mended, before that hour passes. It takes no worn slot because it never
occupies one, grants no verb and rewrites no verb because a mend to the yard's own tool is not a mend to the
kit-runner's build, and it is written here rather than in a record above because an object with nothing in it for a
rule to read is exactly what it is meant to be.

### Reachability in the slice

Eight item records are specified because eight items with fuse pairs is the scope `pitches/pitch-a.md` set, and
the heat-glove above is the one mendable object in the slice that is deliberately not one of the eight.
Four of them are reachable in the 30-60 minute slice: the bone fid, the waxed tar-coat, the tin whistle
and the bench knife. The knife is in the slice because fusing is the centrepiece of the pitch and
`Unpick` has exactly one source, so without the knife in a worn slot there is no fusing at all. That makes
four carried objects against four worn slots, so the cap binds rather than sits idle - on the path where
nothing is fused. The whistle is handed over at the end of The Run, so the bind is a thing that happens at
the rack by the end of that phase rather than at Low Water: a kit-runner at the rack holding the fid, the
coat, the whistle and the knife is full, and the fifth thing somebody offers is a thing that has to stay on
the rack. A kit-runner who has fused ends the shift carrying one thing lighter, because the fusion spends two
slots and gives one back, and the slot it gives back has two spent names on it. The other four - the tarred
line, the bend hook, the shuttered lamp and the winch bar - are the backlog the recipe table below is written
against, and they are not reachable in this slice until gate 4 says so, which is a different claim from where
they are kept: the hook is off the rack and in a child's hands at The Turning, and the line is on the end of
somebody's own bench. Nothing in the slice is mended outside those four except the heat-glove, and it is not a
fifth reachable item: it never takes a worn slot and it is on Grissel Toft's own hand again before The Turning
ends, so the count of what the player can be carrying stays four.

## Mending recipes

The rack fuses two mended pieces into one heirloom. The heirloom keeps the verbs of both pieces, picks up
the one verb the two were mended with together, and loses, forever, everything else about them. The recipe
list is the whole vocabulary of fusing in the slice; a pair not in this table cannot be fused, and there is no
second table.

The rule for what survives, stated once and applied to every pair below:

1. The heirloom's verb list is the union of the two inputs' verb lists.
2. Every recipe carries a `keeps` key, and it is load-bearing: it names, by input item id, the forms that
   survive into the heirloom. Where the union holds two forms of one verb, `keeps` names exactly one of the
   two - the one that survives - and the other form is spent with the piece that carried it. Where the two
   inputs bring one form of a verb between them, as every pair in the table below does, `keeps` names both
   inputs and rule 2 spends nothing on its own; the losses listed under the table are the forms the two pieces' `writes` keys supersede at pickup, not anything rule 4 spends. The key
   is on every record so that the heirloom's verb list is readable out of the data and not out of the prose.
3. The heirloom also carries one further verb, the one thing the two pieces were mended with together.
   This is the pitch's answer to "builds capped rather than deepened", and it is the only thing that
   comes out of the spent mending.
4. Everything else those two pieces could do is gone. There is no second version of them anywhere.

Every recipe also carries `read_aloud`, the heirloom's name as the bench will say it, because the preview is
required to show it and there is nowhere else in the record for it to live.

```json
{
  "recipes": [
    {
      "id": "fuse-fid-coat",
      "inputs": ["bone-fid", "tar-coat"],
      "keeps": ["bone-fid", "tar-coat"],
      "output": "quiet-coat",
      "read_aloud": "the quiet coat",
      "say": "Two patches now, one coat, and the wall and the water on the same body."
    },
    {
      "id": "fuse-whistle-line",
      "inputs": ["tin-whistle", "tarred-line"],
      "keeps": ["tin-whistle", "tarred-line"],
      "output": "thrown-whistle",
      "read_aloud": "the thrown whistle",
      "say": "Twelve fathoms with a whistle on the end, for calling somebody you cannot reach."
    },
    {
      "id": "fuse-hook-line",
      "inputs": ["bend-hook", "tarred-line"],
      "keeps": ["bend-hook", "tarred-line"],
      "output": "grapnel-line",
      "read_aloud": "the grapnel line",
      "say": "Line out and the hook on it, and it holds on the second pull."
    },
    {
      "id": "fuse-lamp-knife",
      "inputs": ["shuttered-lamp", "bench-knife"],
      "keeps": ["shuttered-lamp", "bench-knife"],
      "output": "dark-mend",
      "read_aloud": "the dark mend",
      "say": "Half a lamp and a blunt point, for finding the seam somebody unpicked first."
    },
    {
      "id": "fuse-bar-hook",
      "inputs": ["winch-bar", "bend-hook"],
      "keeps": ["winch-bar", "bend-hook"],
      "output": "short-haul",
      "read_aloud": "the short haul",
      "say": "The bar and the hook together, and the pull comes to you instead of going."
    },
    {
      "id": "fuse-knife-line",
      "inputs": ["bench-knife", "tarred-line"],
      "keeps": ["bench-knife", "tarred-line"],
      "output": "spliced-line",
      "read_aloud": "the spliced line",
      "say": "Line spliced with a blunt point, and laid out straight for once."
    }
  ]
}
```

What each one keeps and what it destroys, read off the `keeps` key and the `writes` supersession at pickup:

- **quiet-coat** ("the quiet coat") keeps the quiet `Climb` and the hands-kept `Wade`, and carries `Shelter` - getting
  somebody under you and keeping the weather off both of you. Spent forever: the slow `Climb` and the
  `Wade` that put your hands under the water. After this heirloom exists there is no way to climb the
  wall slowly or to go under at the yard's foot on the hard, which is what that hands-under `Wade` was and is
  the only form of going under the slice has, and the two pieces that knew how are not anywhere.
- **thrown-whistle** ("the thrown whistle") keeps `Call` and `Haul` and carries `Reach` - putting something out to arm's
  length across a gap that you cannot cross. Spent forever: the line's own anchoring habit and the
  whistle's plainness. It is now a thing you throw rather than a thing you blow, so what `Call` is on it now is the
  name going out and the answer coming back, and if you drop it in
  the channel it is on the bottom and not in the yard's rack.
- **grapnel-line** ("the grapnel line") keeps `Haul` and `Hook` and carries `Anchor` - set something and hold it against the
  pull. Spent forever: the free hauling without a hook, which is the shape that got you across the
  channel in a hurry and now belongs to neither spent piece.
- **dark-mend** ("the dark mend") keeps `Steady` and `Unpick` and carries `Trace` - feeling, by hand, where a mend
  was unpicked before you were. Spent forever: the knife's plain work on a whole object and the lamp's
  plain light on a board. Nothing in the world can now be opened in the ordinary way and nothing can
  be properly seen.
- **short-haul** takes the winch bar and the bend hook and nothing else - the tarred line is not an input
  to this recipe and nothing of the line's hauling is spent by it. It keeps the bar's planted `Haul` and the
  hook's `Hook` and carries `Draw` - bringing a thing up to where you are standing without letting go of it.
  Spent forever: no *form* of either verb, because these two inputs never brought a second form of either
  between them, which is the point. What the fusion does spend is both tools as separate objects - neither
  the bar nor the hook is anywhere for the rest of the shift - and what it leaves is a heirloom built on the
  bar's `Haul`, which is anchored to the rack's end of the yard and does not travel. This is the deliberate
  thin fusion in the table, kept in the bible on purpose: two working tools go in and the pull comes to you
  instead of going, and a kit-runner who does it knowingly gets a build they cannot take off the rack.
- **spliced-line** ("the spliced line") keeps `Haul` and `Unpick` and carries `Lay` - laying a length out flat and true with
  no knot in it. Spent forever: the knife as a knife and the line as a loose coil.

### The preview

Before the player commits, the rack shows the preview and the preview is the only look they get. It
shows, in this order: the heirloom's name as the bench will say it, taken from the recipe's `read_aloud`
- `the quiet coat`, `the thrown whistle`, `the grapnel line`, `the dark mend`, `the short haul`,
`the spliced line`, one for each of the six heirlooms - then the heirloom's full verb list including the two
kept forms and the one inherited verb, and
underneath, in plain text and not as a warning icon, exactly what is lost forever - named piece by
named piece, so that `bone-fid` and `tar-coat` are not merely gone but are *readable as gone*.

One scoping sentence so this is not read as a breach of the world bible's absolutes. The preview is rack
UI: it is not narration and it is not a resident's line, and it is the one place in the game where the game
itself names a verb and names what a mechanic spends. `bible/world.md`'s refusal to explain the mechanic out loud is a rule
about prose, and this is prose's exception rather than a contradiction of it; the words on the preview are
still the bench's words and not a rulebook's. The second absolute it has to answer is the one about fusing
itself - that a fusion is never reversible, previewed twice, or undoable - and it answers it by count: one
look, once, before the piece is spent, and no second look afterwards. A preview the player may open again
afterwards would be the breach; this is not that.

The preview is load-bearing and the reasons are stated here so no later draft quietly drops it. Fusing
is irreversible: there is no undo verb, no bench action that unpicks a fused piece, and no way to
recover either input. And it cannot be previewed after the fact - once the heirloom exists the two
spent pieces are not in the save, not on the rack and not in the yard, so there is no later state in
which the player can go back and see what they gave up. The preview is therefore not a confirmation
dialog. It is the only description of the loss that will ever exist, and if it is wrong the game has
lost something the player cannot get back.

## Time

One shift is four phases, named as `bible/world.md` names them: **The Turning**, **Low Water**, **The
Run**, **Slack Water**. The pack's phase keys are lowercase slugs of those names - `the-turning`,
`low-water`, `the-run`, `slack-water` - and the names as written are what the residents say and what the
player reads; the slug is what a rule payload carries. Each phase is a tone sentence, and one
line per resident per phase is written against them.

```json
{
  "time": {
    "rest": true,
    "rail": "locked",
    "persist": true
  }
}
```

**`rest: true` - the player waits or rests, and it spends the hour.** The kit-runner can rest at the
bench or wait anywhere in the yard, and rest advances the shift by exactly one phase along the tide. It
spends nothing the game can put a number on: no coin, no hunger, no stamina, nothing that could be
drawn as a bar. What it spends is two things, both of them already true of this yard in
`bible/world.md`. It spends the hour: the phase you were standing in is the phase you were standing in,
and it does not come back. And it spends your place at the bench: whoever is at the bench in the new
hour is the one mending in it, so resting is how a kit-runner who is not finished at the bench ends up
finished anyway. Any ask still standing when the hour passes closes unanswered, and a resident whose
hour it was does not raise it again at the next one. That is the whole cost, and it is the cost the yard
would charge on its own.

**`rail: locked` - the player cannot skip ahead to the phases they want.** Time along the tide moves
forward one phase at a time, in order, from the phase the player is standing in. There is no control
that carries the kit-runner to Low Water from Slack Water, no button for the hour the player wants, and
no back. A rail that a player can click freely is fast travel with a tide attached, and the four phases
stop being four places. This is `bible/world.md`'s no-fast-travel absolute read against the cost of a phase
move: the rail is the tide, the tide only goes one way, and the hour it carries you past does not come back.

**`persist: true` - the hour survives a reload.** A kit-runner who has waited out three phases and
reloads is still standing in the fourth, with the same satchel, the same mend history and the same
hour. Without that, the four phases are a conversation with a page refresh in the middle of it.

**A rule conditions on the standing phase.** This is engine work landing for this milestone, and the shape
it takes is a phase key in the rule's conditions:

```json
{
  "id": "the-bench-end-goes-under-while-she-is-counting",
  "when": {"phase": "the-run"},
  "once": false,
  "then": [{"say": "Sable Kearn", "line": "Water's over the coping. Bench end's going under."}]
}
```

The speaker cannot be Roald Fisk at this phase, and the record says so here so it cannot drift back: he went
under the hull at Low Water, and after that hour he crossed
to the town bank before the flood, The Run closes the water between him and the yard, and he is on the far side
for the whole of it, speaking from the far end of the causeway and coming back with his sister at Slack Water.
The resident who is at the bench through every phase and short of time at this one is Sable Kearn, and she says
what she says by where things sit rather than by what they are called.

What that condition does *not* buy is a condition on the kit-runner's own pockets. Nothing in this pack
conditions on what the player happens to be carrying or on what the rack took, beyond what items, recipes and
rules already express, so a beat written "if the thing she wanted is what the rack took" can only ever be its
untoggled default and must not be written.

`research/A2-feasibility.md` records the gap this closes as two separate ones: the rule vocabulary's closed
set of conditions had no phase key, and the `on:` field, the nearest thing to a phase gate, is refused by
the validator because phases are not things. Until the phase condition lands, the one phase-aware lever a
pack can actually ship today is the transition payload: a rule keyed on entering a phase, whose action puts
a line in a resident's mouth.

```json
{
  "id": "the-watch-comes-round",
  "when": {"phase-changes": {"to": "the-turning"}},
  "once": false,
  "then": [{"say": "Warden Ottmar Vell", "line": "There you are. Bench is warm enough."}]
}
```

`say` is the resident's name as `bible/cast.md` writes it, and it is the whole of the lookup: `Roald Fisk`,
`Warden Ottmar Vell`, and every other resident under their written name, never a short form. A pack that writes
`"say": "Ottmar"` is asking the engine for a resident the cast bible has not met.

Three limits of that lever belong in this bible because a pack author will hit all three. It fires on
the *transition*, not on the standing state: enter Slack Water by any route and the line speaks once,
stand in Slack Water for an hour and it does not speak again. `once` defaults to true in the rules
engine, so a rule meant to fire on every visit needs `"once": false` written on it, as above. And it
only works in the woven player: the standalone rails move time and run no rules at all.

### Known limits, stated rather than smoothed over

Three things the pack is asking for are not built today, and every one of them is recorded in
`research/A2-feasibility.md` rather than guessed at here. A fourth - the rest verb and the rail lock - is
engine work landing for this milestone, and is written up differently because it is not a limit the slice
has to be balanced around.

1. **The phase does not survive a reload.** Phase is in-memory state in the player; a reload returns
   the kit-runner to the pack's first phase. So `persist: true` above is a request, not a description:
   until it lands, a reload silently rewinds the shift, and the pack must not be balanced around a
   persistence it does not have.
2. **The standalone rails fire no rules.** A phase-changed rule only speaks in the woven player, and the
   same goes for a phase condition. If the slice is ever demonstrated on a served shell rather than woven,
   the resident who only speaks at one hour does not speak at all.
3. **No rule conditions on what the player carries or what is on the rack.** The phase condition above is
   the whole of what the rule layer gains for this milestone. Satchel and rack state beyond what items,
   recipes and rules already express stays out of the slice, and a beat that reads the player's satchel to
   decide how a resident talks is a beat that can never fire. What the limit does *not* touch is what the
   items and recipes already say: how hard the Slack Water crossing is, and whether the satchel holds an
   heirloom when the warden reads it, are read out of the heirloom's verb list and not out of a rule's
   conditions, so a build can decide those without the rule layer ever knowing what is in the satchel. The
   residents' lines in `bible/slice.md` that lean on it are written as their default version instead.

**The rest verb and the rail lock are landing for this milestone.** `research/A2-feasibility.md` records
the action list as closed with no wait, rest or sleep verb in it, and the rail as writing the clicked phase
straight into state with no cost, no delay and no check. That is the state the rest of this section was
written against and it is what the Rest action, the locked rail and the standing-phase condition above are
the engine work for. Until they land, the honest position is that `rest: true` has no verb to hang on and
the rail lock is not enforced: a player in today's engine can still click any of the four phases at any
time, which is precisely what `rail: locked` forbids. The pack ships in the meantime by paying the hour in
prose and in the residents' lines rather than in a button - the rack fills on the yard's own schedule, the
asks are met at their phase, and an hour passed is an hour the kit-runner was not at the bench - and not by
pretending a free click cost anything.

The tension this section used to carry is closed by decision rather than by draft: `bible/world.md`'s
no-fast-travel absolute now stands with the cost of a phase move written into it, and the cost is the
yard's and not the economy's - no bar, no currency, and the price of a phase move is the hour you leave and
the place at the bench. What is left for Rylee at gate 4 is the persistence gap above and the four
reachable items, not the shape of a phase move.

## The shingle ending

The ending beat is at Slack Water, at the bench end of the causeway on the yard side, with the warden, the
bench and the slate, and with the town's evening work lit across the water on the far bank. The shingle is
read and signed there, in the yard and not in the town; the far bank is where the work it is signing for
happens, and nothing on this beat crosses to do it. The kit-runner wants a name on it because a name on it
is the night roster, and the whole shift has been spent earning a signature rather than a level.

**What is read aloud.** The warden stands at the bench and reads the satchel. Not the build, not the
stats, not the verbs - the objects, in the order they were mended, each one named by what it was for
and what it did for the person who owned it before it was somebody else's, and each one named for what
the yard lost when it changed hands. The reading is done in the yard's own words because that is the
only register anyone at the bench speaks in: an object is named by its use, and a build is legible
because the things in the satchel are named, not because the game explains what they do. Where a piece
is an heirloom it is read as one object with two patches on it, and the two names the warden reads on it are
the two spent pieces' names - for the quiet coat, the bone fid and the waxed tar-coat - because the yard knows
what was spent and does not hide it. A mending mark is not one of those names: Maud Bray's scratch is not a name
on the object but the record of a hand on a seam, and fusion unpicks the seam and spends it with the hand that
laid it, so the heirloom carries what was spent and not who mended it. Where an ask was never brought to the bench
its absence is audible: the name simply is not read, and the warden does not fill the gap with a
compliment.

**What the shingle signs or defers.** Three outcomes, decided by what the satchel holds rather than
by anything the player said, and read out of the item and recipe records rather than out of a rule's
conditions on the satchel:

- **Signed.** The satchel holds a build, and a build means at least one heirloom - at least one piece
  that was made by fusion rather than merely carried. A kit-runner who has mended and carried and never
  decided anything has not been read out for a signature. The name goes on the slate, the slate is
  held up, and the week of nights is the consequence.
- **Deferred.** The satchel holds mended work but no heirloom. The warden reads it, names it
  accurately, and defers, and the deferral is specific: the work was good and the shift decided
  nothing, so come back at The Turning. This is the outcome the design is most comfortable with,
  because it is the one the pitch's "what you fuse is the build" is actually testing.
- **Refused.** The satchel is empty, or holds an object whose owner came to the bench for it and was
  told no. The slate is not read for a signature at all, and the refusal is given in the same plain
  register as the reading.

**What the build does to it.** The objects themselves are specified in the two sections above; this
section is only the beat. The build reaches the beat in exactly three ways. It decides *signed* versus
*deferred*, through whether anything was fused. It decides how long the reading is and what it
contains, because a satchel with four objects in it is a longer reading than a satchel with two, and a
satchel carrying somebody's coat that was never returned is read differently from the same four objects
with the coat left on the rack. And it decides what the yard has become: the fuse pairs that never
fused are somebody's tools still hanging on the rack, and the residents who wanted them have stopped
offering, which is the outcome the world bible asks for and the one the pitch promises.

Nothing here is canon. At gate 4 this beat may be signed, deferred or deleted outright, and if it is
deleted the kit layer still has to work, because the satchel is read aloud by a person who is not a
game mechanic wearing a person.