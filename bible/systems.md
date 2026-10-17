DRAFT - not canon until Rylee approves (gate 4)

# Systems bible: the kit layer of The Mending Shift

Status: draft for milestone M1. Written against `pitches/pitch-a.md`, `bible/world.md` and
`research/A2-feasibility.md`. Nothing here is a design of record. Every rule below is a proposal for Rylee
to approve, amend or delete at gate 4. No visual anchors are chosen here and none are implied, and no
playtest has been run against any of it.

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
from you. Nothing else in an item record is load-bearing.

### The bone fid

Ottmar's fid, whittled flat at the shoulder by thirty years of the same grip.

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

Sable's coat, waxed inside out by somebody who wades for a living and never got it back.

```json
{
  "id": "tar-coat",
  "name": "Sable's waxed tar-coat",
  "grants": [{"verb": "Wade", "label": "wade, and keep your hands"}],
  "writes": "Wade"
}
```

It rewrites `Wade` so your hands stay above the water and stay usable. What changes: you can work a
thing - a line, a knot, a latch, a person - in the water instead of committing both hands to not
drowning. What you can no longer do afterwards is go under. The coat is waxed and thick and it is not
made for submersion, so the dive that used to be available at the yard's foot during Low Water is
gone for the rest of the shift. It is also the coat that is on somebody else's back all morning, and
carrying it is the yard knowing where it went.

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

Twelve fathoms of tarred line off the rack, with the lay of it gone soft where it has been wet and dried
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
Nothing is rewritten. What you cannot do afterwards is haul anything at all with your hands alone, and
a line that is not anchored is a line that will put you in the channel, so hauling is a thing you do
twice.

### The bend hook

A hook off the rack bent by a hull that wanted to be elsewhere, ground back to an edge by somebody who
did not have a new one.

```json
{
  "id": "bend-hook",
  "name": "the rack's bend hook",
  "grants": [{"verb": "Hook", "label": "hook, and hold on from where you are standing"}]
}
```

It grants `Hook`: catch and hold a line, a gunwale or a stanchion from a distance you do not have to
cross. Nothing is rewritten. What you lose by taking it is the hands: a hook is a thing you use one
handed, and the hand it takes is the same hand the whistle wants when you are calling for somebody.

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
rewritten. What it costs is the whole arm: you cannot steady and hold anything else at the same time,
and the crossing it makes possible is the crossing on which you are the last thing in the water.

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

### Reachability in the slice

Eight items are specified because eight items with fuse pairs is the scope `pitches/pitch-a.md` set.
Three of them are reachable in the 30-60 minute slice, per the pitch: the bone fid, the waxed tar-coat
and the tin whistle. The other five - the line, the hook, the lamp, the knife and the bar - are the
backlog the recipe table below is written against, and none of them is in the slice until gate 4 says
so. The slice's three usable objects against four worn slots is the pitch's arithmetic and this file
does not improve on it.

## Mending recipes

The rack fuses two mended pieces into one heirloom. The heirloom keeps the verbs of both pieces and
loses, forever, everything else about them. The recipe list is the whole vocabulary of fusing in the
slice; a pair not in this table cannot be fused, and there is no second table.

The rule for what survives, stated once and applied to every pair below:

1. The heirloom's verb list is the union of the two inputs' verb lists.
2. Where the union holds two forms of one verb, exactly one survives - the one the recipe names - and
   the other is spent with the piece that carried it.
3. The heirloom also carries one further verb, the one thing the two pieces were mended with together.
   This is the pitch's answer to "builds capped rather than deepened", and it is the only thing that
   comes out of the spent mending.
4. Everything else those two pieces could do is gone. There is no second version of them anywhere.

```json
{
  "recipes": [
    {
      "id": "fuse-fid-coat",
      "inputs": ["bone-fid", "tar-coat"],
      "output": "quiet-coat",
      "say": "Two patches now, one coat, and the wall and the water on the same body."
    },
    {
      "id": "fuse-whistle-line",
      "inputs": ["tin-whistle", "tarred-line"],
      "output": "thrown-whistle",
      "say": "Twelve fathoms with a whistle on the end, for calling somebody you cannot reach."
    },
    {
      "id": "fuse-hook-line",
      "inputs": ["bend-hook", "tarred-line"],
      "output": "grapnel-line",
      "say": "Line out and the hook on it, and it holds on the second pull."
    },
    {
      "id": "fuse-lamp-knife",
      "inputs": ["shuttered-lamp", "bench-knife"],
      "output": "the-dark-mend",
      "say": "Half a lamp and a blunt point, for finding the seam somebody unpicked first."
    },
    {
      "id": "fuse-bar-hook",
      "inputs": ["winch-bar", "bend-hook"],
      "output": "short-haul",
      "say": "The bar and the hook together, and the pull comes to you instead of going."
    },
    {
      "id": "fuse-knife-line",
      "inputs": ["bench-knife", "tarred-line"],
      "output": "spliced-line",
      "say": "Line spliced with a blunt point, and laid out straight for once."
    }
  ]
}
```

What each one keeps and what it destroys:

- **quiet-coat** keeps the quiet `Climb` and the hands-kept `Wade`, and carries `Shelter` - getting
  somebody under you and keeping the weather off both of you. Spent forever: the slow `Climb` and the
  `Wade` that put your hands under the water. After this heirloom exists there is no way to climb the
  wall slowly or to dive at the yard's foot, and the two pieces that knew how are not anywhere.
- **thrown-whistle** keeps `Call` and `Haul` and carries `Reach` - putting something out to arm's
  length across a gap that you cannot cross. Spent forever: the line's own anchoring habit and the
  whistle's plainness. It is now a thing you throw rather than a thing you blow, and if you drop it in
  the channel it is on the bottom and not in the yard's rack.
- **grapnel-line** keeps `Haul` and `Hook` and carries `Anchor` - set something and hold it against the
  pull. Spent forever: the free hauling without a hook, which is the shape that got you across the
  channel in a hurry and now belongs to neither spent piece.
- **the-dark-mend** keeps `Steady` and `Unpick` and carries `Trace` - feeling, by hand, where a mend
  was unpicked before you were. Spent forever: the knife's plain work on a whole object and the lamp's
  plain light on a board. Nothing in the world can now be opened in the ordinary way and nothing can
  be properly seen.
- **short-haul** keeps the bar's planted `Haul` and `Hook` and carries `Draw` - bringing a thing up to
  where you are standing without letting go of it. Spent forever: the line's hauling and the hook's
  reach. This is the deliberate bad fusion in the table, kept in the bible on purpose: it is one verb
  fewer than its inputs looked like, and it is the answer if a player does it knowingly.
- **spliced-line** keeps `Haul` and `Unpick` and carries `Lay` - laying a length out flat and true with
  no knot in it. Spent forever: the knife as a knife and the line as a loose coil.

### The preview

Before the player commits, the rack shows the preview and the preview is the only look they get. It
shows, in this order: the heirloom's name as the bench will say it (`quiet-coat` read aloud as "the
quiet coat"), the heirloom's full verb list including the two kept forms and the one inherited verb, and
underneath, in plain text and not as a warning icon, exactly what is lost forever - named piece by
named piece, so that `bone-fid` and `tar-coat` are not merely gone but are *readable as gone*.

The preview is load-bearing and the reasons are stated here so no later draft quietly drops it. Fusing
is irreversible: there is no undo verb, no bench action that unpicks a fused piece, and no way to
recover either input. And it cannot be previewed after the fact - once the heirloom exists the two
spent pieces are not in the save, not on the rack and not in the yard, so there is no later state in
which the player can go back and see what they gave up. The preview is therefore not a confirmation
dialog. It is the only description of the loss that will ever exist, and if it is wrong the game has
lost something the player cannot get back.

## Time

One shift is four phases, named as `bible/world.md` names them: **The Turning**, **Low Water**, **The
Run**, **Slack Water**. The pack's phase keys are those four names; each is a tone sentence, and one
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
stop being four places. This is the reading of `bible/world.md`'s line that there is no way to skip an
hour and that moving between phases is the yard being different rather than the player paying: the
rail is the tide, and the tide only goes one way.

**`persist: true` - the hour survives a reload.** A kit-runner who has waited out three phases and
reloads is still standing in the fourth, with the same satchel, the same mend history and the same
hour. Without that, the four phases are a conversation with a page refresh in the middle of it.

**A rule cannot condition on the standing phase.** `research/A2-feasibility.md` records this as two
separate gaps. The rule vocabulary's closed set of conditions has no phase key, so no rule can say
"while it is The Turning"; and the `on:` field, which is the nearest thing to a phase gate, is refused
by the validator because phases are not things. The one phase-aware lever a pack can actually ship is
the transition payload, and it is what this pack uses: a rule keyed on entering a phase, whose action
puts a line in a resident's mouth.

```json
{
  "id": "the-watch-comes-round",
  "when": {"phase-changes": {"to": "the-turning"}},
  "once": false,
  "then": [{"say": "Ottmar", "line": "There you are. Bench is warm enough."}]
}
```

Three limits of that lever belong in this bible because a pack author will hit all three. It fires on
the *transition*, not on the standing state: enter Slack Water by any route and the line speaks once,
stand in Slack Water for an hour and it does not speak again. `once` defaults to true in the rules
engine, so a rule meant to fire on every visit needs `"once": false` written on it, as above. And it
only works in the woven player: the standalone rails move time and run no rules at all.

### Known limits, stated rather than smoothed over

Four things the pack is asking for are not built today, and every one of them is recorded in
`research/A2-feasibility.md` rather than guessed at here.

1. **The phase does not survive a reload.** Phase is in-memory state in the player; a reload returns
   the kit-runner to the pack's first phase. So `persist: true` above is a request, not a description:
   until it lands, a reload silently rewinds the shift, and the pack must not be balanced around a
   persistence it does not have.
2. **The phase jump is free, and it stays free until a rest verb exists.** The rail writes the clicked
   phase straight into state with no cost, no delay and no check, and there is no wait, rest or sleep
   verb in the bindable action list to charge. What that means for this slice is blunt: **the rail
   lock in this section is not enforced today.** A player in the current engine can click any of the
   four phases at any time, which is precisely the thing `rail: locked` is written to forbid. The pack
   ships in the meantime by making the four phases descriptive rather than metrical - the rack fills on
   the yard's own schedule, the asks are met at their phase, and skipping an hour loses you the
   resident whose hour it was, without pretending that a button cost you anything.
3. **The standalone rails fire no rules.** A phase-changed rule only speaks in the woven player. If the
   slice is ever demonstrated on a served shell rather than woven, the resident who only speaks at one
   hour does not speak at all.
4. **The rest verb does not exist.** Until it does, `rest: true` has no verb to hang on, and the only
   way to change phase is the rail, which is free.

One tension to put in front of Rylee at gate 4 rather than resolve here. `bible/world.md` lists among
its absolutes that moving between phases is never a cost the player pays for being elsewhere, and this
section writes a rest that spends an hour and a place at the bench. The draft position is that the cost
is the yard's and not the economy's - there is no bar and no currency, and the cost is being somewhere
else - but the two drafts do not say the same thing about a phase move, and only the owner can settle
which one the game ends up with.

## The shingle ending

The ending beat is at Slack Water, at the bench end of the causeway, with the town's evening work lit
on the far bank. The shingle is the slate. The kit-runner wants a name on it because a name on it is
the night roster, and the whole shift has been spent earning a signature rather than a level.

**What is read aloud.** The warden stands at the bench and reads the satchel. Not the build, not the
stats, not the verbs - the objects, in the order they were mended, each one named by what it was for
and what it did for the person who owned it before it was somebody else's, and each one named for what
the yard lost when it changed hands. The reading is done in the yard's own words because that is the
only register anyone at the bench speaks in: an object is named by its use, and a build is legible
because the things in the satchel are named, not because the game explains what they do. Where a piece
is an heirloom it is read as one object with two patches on it and both names still showing, because
the yard knows what was spent and does not hide it. Where an ask was never brought to the bench its
absence is audible: the name simply is not read, and the warden does not fill the gap with a
compliment.

**What the shingle signs or defers.** Three outcomes, decided by the state of the satchel rather than
by anything the player said:

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