# Continuity re-check after M1b (host, 2026-10-16; Codex and MiniMax, fresh passes)

Fix every finding, or say why it is not a contradiction. Findings the reviewer marked LOW CONFIDENCE may be answered NOT A CONTRADICTION with a short reason.

## G01 [codex] timeline
- files: bible/cast.md:45-48, bible/systems.md:72-73, bible/slice.md:53-55
- A: Roald's coat at the end of The Turning
- B: It is also the coat of the yard's diver, handed over at Low Water
- why: The cast and slice place the coat handoff at the end of The Turning; systems places it at Low Water.

## G02 [codex] world rule
- files: bible/world.md:30-33, bible/slice.md:141-142
- A: At The Run the channel is running faster than a person walks: the crossing is still there and still passable
- B: there is no crossing at this hour and nobody on the far side will take a kit-runner off the water in a run
- why: The slice says no crossing exists during The Run; the world bible says the crossing remains passable. The world bible distinguishes passability from whether anyone will take the kit-runner across, but the slice denies the crossing itself.

## G03 [codex] item and recipe data
- files: bible/world.md:69-72, bible/systems.md:214-217, bible/slice.md:103-107
- A: Take two mended pieces to the rack and fuse them and you get one heirloom that keeps both of their verbs and loses the rest forever.
- B: The heirloom also carries one further verb, the one thing the two pieces were mended with together.
- why: The world bible describes the heirloom as retaining the inputs' verbs and losing the rest; systems adds a further inherited verb, which the slice also expects in the preview.

## G04 [minimax] timeline / item handoff
- files: bible/systems.md:72, bible/cast.md:46, bible/slice.md:54
- A: It is also the coat of the yard's diver, handed over at Low Water with the wax gone hard at both elbows
- B: Roald's coat at the end of The Turning, the warden's fid at Low Water, the night crew's whistle at the end of The Run
- why: Three of four files put the tar-coat in the player's hands at the end of The Turning (slice.md:54 'handed to him at the end of the beat', inside Beat 1). systems.md puts the same handoff at Low Water. Verified: cast.md:46 and slice.md:54 agree with each other; systems.md:72 is the outlier. This shifts the whole slot ledger by one phase (see F11).

## G05 [minimax] verb / recipe data
- files: bible/world.md:70, bible/systems.md:279, bible/slice.md:173
- A: The fid's climb and the coat's wading can coexist; the fid's silence cannot also come along, because it was in the piece you spent.
- B: **quiet-coat** ("the quiet coat") keeps the quiet `Climb` and the hands-kept `Wade`, and carries `Shelter`
- why: world.md states as the worked example of fusion that the fid's silence does NOT survive. systems.md keeps the quiet Climb. Additionally world.md:70-71 is confused against systems.md:44-49, where the fid's 'silence' and the fid's 'climb' are the same rewritten verb, so 'the fid's climb... can coexist' and 'the fid's silence cannot' cannot both hold. slice.md:143 and :173 both assume the quiet Climb survives the fusion, so systems.md + slice agree and world.md is the outlier.

## G06 [minimax] world rule broken by a beat
- files: bible/world.md:31, bible/slice.md:141
- A: At The Run the channel is running faster than a person walks: the crossing is still there and still passable, and nobody will take a kit-runner off the water in it
- B: The kit-runner goes out along the causeway toward the far bank and is refused - there is no crossing at this hour and nobody on the far side will take a kit-runner off the water in a run
- why: world.md draws the distinction explicitly and at length ('a different thing from the water being impassable'); world.md:116 repeats it ('the town is there, the crossing is there, the answer is no'). Beat 3 collapses both halves into 'there is no crossing at this hour'.

## G07 [minimax] world rule broken by a beat / internal to slice.md
- files: bible/world.md:117, bible/slice.md:142, bible/slice.md:143
- A: The return is empty-handed and slow.
- B: the return is the one that the shift's own work decides. With the fid and the coat together the crossing is quiet and short and both hands are available.
- why: world.md makes the refused return unconditionally empty-handed; slice.md:143 makes it quality-dependent, in the same paragraph that says there is no crossing at this hour. Beats 3 and 4 also duplicate each other: the Slack Water crossing outcomes (quiet-coat vs one cheap verb) are narrated inside The Run beat and then again at slice.md:171-175.

## G08 [minimax] timeline / tide
- files: bible/world.md:90, bible/world.md:13, bible/world.md:110, bible/slice.md:14
- A: The tide has just turned at the top of its night water and is beginning to fall, so the yard opens at full water with the flood already on its way out.
- B: The yard sits a few feet above high water, so at the top of a tide the sea comes over the wall ... by the middle of the phase the flood has topped the wall: for the length of the run's high water the sea is over the coping.
- why: 'The top of its night water' plus slice.md:14 'at full water' place The Turning at high water, but world.md:13-14 says the sea is over the wall at the top of a tide, and world.md:110 puts the over-the-wall high water in the middle of The Run. Two high waters in one shift, and The Turning's own text ('The wall is a cliff') contradicts the high-water reading. This matters because Grissel's deadline is defined as 'before the water is over the wall' (cast.md:191-194, slice.md:39-41).

## G09 [minimax] motivation vs item behaviour
- files: bible/cast.md:82, bible/systems.md:63, bible/systems.md:68, bible/slice.md:173
- A: The want is checkable: it is the coat's job, and the coat as it stands will not do it.
- B: "grants": [{"verb": "Wade", "label": "wade, and keep your hands"}] ... It rewrites `Wade` so your hands stay above the water and stay usable.
- why: cast.md:9-10 states every want must be checkable against the object named under it. Roald's want is a passenger's feet out of the water; the coat's record keeps the wader's own hands usable and nothing about a passenger. Only the fused heirloom's `Shelter` (systems.md:279) covers 'somebody under you'. On the unfused path slice.md:173 still uses the coat's hands-kept `Wade` to get the sister across dry-footed.

## G10 [minimax] scope / item reachability
- files: bible/slice.md:224, bible/slice.md:31, bible/cast.md:109
- A: are not reachable in this slice: none of `Haul`, `Hook` or `Steady` is in the yard at any hour
- B: a coat hook he has already taken off the rack, and already bent (slice.md:31); A length of tarred line with a block at the standing end stays where it is, on the end of her own bench (cast.md:109)
- why: The yard demonstrably holds a bent coat hook at The Turning (slice's own Beat 1) and a length of tarred line on Sable's bench at Low Water (cast.md:108-112, which even reasons about it as 'not one of the four things this shift can hand to a kit-runner'). The stronger claim systems.md:196 needs is 'not reachable', which is true; 'not in the yard at any hour' is not.

## G11 [minimax] naming / item ownership
- files: bible/systems.md:114, bible/cast.md:149, bible/cast.md:150
- A: The rack's bend hook - a coat hook with the shank drawn and a bend set in it hard enough that it will not open back without a vice.
- B: A coat hook he has already taken off the rack, and already bent. The shank is drawn about a third of the way along and the bend is set hard enough that it will not open back without a vice.
- why: The defect text is word-for-word identical, so it is one item, but systems.md makes it the rack's property while cast.md makes it Tam's, already removed from the rack. Also drives F07: if it is Tam's it is in the yard at The Turning.

## G12 [minimax] internal to cast.md
- files: bible/cast.md:45, bible/cast.md:48, bible/cast.md:149
- A: Four of the seven put an object into a kit-runner's hands in this shift, and none of them does it at every phase:
- B: Grissel Toft's heat-glove is handed over at The Turning ... (cast.md:48); A coat hook he has already taken off the rack (cast.md:149)
- why: The roll-up counts four handers and omits Grissel and Tam, both of whom are described elsewhere in the same file as handing an object over. Cast.md:50 also says Maud 'hands over nothing', which is right, but the file's own header claim does not hold.

## G13 [minimax] who knows what / beat roster
- files: bible/slice.md:134, bible/slice.md:28, bible/slice.md:79
- A: *Sable Kearn*, who is present, and brief, and offers nothing further. She asked for the hoist at The Turning and she has not been given it
- B: Beat 1 -- Who speaks -- Tam Verrow ... Warden Ottmar Vell ... Roald Fisk ... Grissel Toft (slice.md:28-45); Beat 2 -- *Sable Kearn*, who is at the bench through every phase (slice.md:79)
- why: Beat 3 says she already asked at The Turning, but Sable is not in Beat 1's speaker list; the slice places her ask at Low Water. Also brushes systems.md:355 ('a resident whose hour it was does not raise it again') and world.md:114 ('too late in the shift for an ask to be a story any more').

## G14 [minimax] timeline / slot ledger
- files: bible/slice.md:100, bible/cast.md:46
- A: Counting the knife, that is four reachable objects against four worn slots and the cap binds: a kit-runner at the rack holding the fid, the coat, the whistle and the knife is carrying everything there is
- B: the night crew's whistle at the end of The Run
- why: The bind is asserted inside Beat 2 (Low Water), but the whistle is not handed over until the end of The Run (cast.md:46, slice.md:129-130). At the fusion moment the satchel holds coat + fid + knife = 3 of 4. On the fused path only three objects are ever carried; on the unfused path the cap binds at The Run, after the fusion decision. systems.md:192-195 makes the same 'binds rather than sits idle' claim without a beat to hang it on.

## G15 [minimax] world rule vs systems/slice
- files: bible/world.md:190, bible/world.md:164, bible/systems.md:307
- A: It is never true that a fusion is reversible, previewed for free, or undoable.
- B: the one place the game does name a verb and does name a loss is the rack's own preview before a fusion (world.md:164); Before the player commits, the rack shows the preview and the preview is the only look they get (systems.md:307)
- why: systems.md:315-320 reconciles the preview against the 'refuses to explain the mechanic out loud' absolute and calls itself 'prose's exception'. The absolute it does not address is world.md:190, which is about fusing itself and says a fusion is never 'previewed for free' - which is a description of the preview. Either the absolute is amended or the reconciliation at systems.md:315-320 is incomplete.

## G16 [minimax] timeline / crossing direction
- files: bible/world.md:127, bible/slice.md:171, bible/slice.md:175
- A: Slack Water is also where the crossing back with a passenger is possible: somebody from the town bank comes over
- B: The crossing out with a passenger is possible in the way it is only possible at this hour ... and she is put down at the far end of it.
- why: world.md has the passenger coming from the town bank over to the yard; slice.md:171 calls the trip 'out'. Beat 4's own Place (slice.md:154-155) has the player go to the town bank and then 'back to the yard end', and Roald is stranded on the far bank (slice.md:160-163), so the loaded leg is yardward. 'Put down at the far end of it' then names the wrong end under either reading.

## G17 [minimax] naming
- files: bible/systems.md:378, bible/systems.md:398, bible/cast.md:53
- A: "then": [{"say": "Roald Fisk", "line": "Two fathoms on the causeway and rising."}]
- B: "then": [{"say": "Ottmar", "line": "There you are. Bench is warm enough."}]
- why: The two worked rule payloads key the same field two different ways. cast.md:53 gives the name as 'Warden Ottmar Vell', systems.md:73 gives the item as 'Roald Fisk's waxed tar-coat', so the bibles use full-display-name for people in items and short-name in one rule. If `say` is a lookup key rather than a display string these are two different residents.

## G18 [minimax] world rule vs beats
- files: bible/world.md:193, bible/world.md:96, bible/slice.md:131, bible/slice.md:248
- A: It is never true that a resident's schedule is a rule the game can enforce by hiding them. Who is awake is carried by what they say, not by whether they can be found.
- B: She is not in this yard at the start of the phase and she is not in the yard before the end of it (slice.md:131); somebody is asleep in the shed (world.md:96); A rule also cannot hide a resident, so nobody is ever asleep or absent (slice.md:248)
- why: Margit's beat entry schedules her out of the yard for two phases by absence, and world.md:96 gives the sanctioned version ('has nothing to say to you at this hour') as 'the night's people are not up; somebody is asleep'. slice.md:248 then claims flatly that 'nobody is ever asleep or absent' while slice.md:90, :131 and :137 and cast.md:123 write three characters in as absent. LOW CONFIDENCE on the world.md:96 leg (prose in-world fact, not a rule); the slice.md:131 vs :248 pair is the clear one.

## G19 [minimax] who knows what / rules
- files: bible/slice.md:171, bible/slice.md:247, bible/systems.md:424, bible/systems.md:479
- A: nothing anybody says here is a condition on the satchel
- B: it is possible in the way the build allows (slice.md:171); the Signed / Deferred / Refused outcomes at slice.md:207-213; a beat that reads the player's satchel to decide how a resident talks is a beat that can never fire (systems.md:424)
- why: Beat 4's difficulty and the ending beat's three outcomes are both functions of satchel state, and systems.md:479-486 endorses build-driven reading, so the blanket claim in slice.md:247 is the odd one out. Reportable because systems.md:384-385 names this exact construction as unwritable.

## G20 [minimax] item / place data
- files: bible/slice.md:68, bible/cast.md:59, bible/world.md:101
- A: the foot of the slipway, where the packet boat is on the hard and can be worked on at no other hour
- B: To get the packet boat off the blocks (cast.md:59); the underside of the hull on the hard, the boat on the blocks that cannot be worked at any other hour (world.md:101)
- why: LOW CONFIDENCE. world.md:101 distinguishes the hull on the hard from the boat on the blocks; cast.md:59 says the packet boat is the one on the blocks; slice.md:68 puts the packet boat on the hard. Either two boats and slice names the wrong one, or three files disagree on which is workable only at Low Water.

## G21 [minimax] verb terminology
- files: bible/slice.md:176, bible/systems.md:122, bible/systems.md:283
- A: the line's `Haul`, the hook's reach or the lamp's `Steady`
- B: "grants": [{"verb": "Hook", "label": "hook, and hold on from where you are standing"}] ... thrown-whistle ... carries `Reach`
- why: LOW CONFIDENCE. The hook's verb is `Hook`; `Reach` is a defined inherited verb belonging to the thrown whistle (systems.md:283). slice.md:176 uses 'reach' as the hook's capability name, which collides with a different verb in the same bible.
