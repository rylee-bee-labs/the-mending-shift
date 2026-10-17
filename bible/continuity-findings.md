# Continuity findings on the M1 draft bibles (host, 2026-10-16; two independent passes, Codex and MiniMax, unioned)

Fix every finding below in the bibles, or, if a finding is wrong, say why in bible/CONTINUITY.md. Duplicates across the two passes are listed once each per pass.

## F01 [codex] item ownership
- files: bible/systems.md:54-60, bible/cast.md:75-80, bible/slice.md:210-214
- A: Sable's coat, waxed inside out by somebody who wades for a living and never got it back.
- B: His waxed tar-coat.
- why: Systems assigns the coat to Sable, while cast assigns it to Roald. The slice identifies this owner disagreement as unresolved.

## F02 [codex] item reachability
- files: bible/systems.md:156-157, bible/systems.md:182-186, bible/slice.md:80-83, bible/slice.md:215-218
- A: It grants `Unpick`, and it is the only source of `Unpick` in the slice: without the knife in a worn slot there is no fusing at all
- B: The other five - the line, the hook, the lamp, the knife and the bar - are the backlog ... and none of them is in the slice until gate 4 says so.
- why: Systems both requires the bench knife for any fusion and places it outside slice reachability. The slice nevertheless presents a reachable fid-and-coat fusion, and flags the knife's scope as unresolved.

## F03 [codex] location
- files: bible/world.md:24-28, bible/world.md:106-108, bible/slice.md:151-152, bible/slice.md:219-221
- A: The town on the far bank is where the shingle is signed
- B: The ending beat is at Slack Water, at the bench end of the causeway, with the town's evening work lit on the far bank.
- why: World places the shingle signing in the town on the far bank; the slice places the reading/signing beat at the bench end of the causeway, on the yard side. The slice calls this unresolved.

## F04 [codex] time rules
- files: bible/world.md:112-115, bible/world.md:152-154, bible/systems.md:304-321, bible/systems.md:372-377, bible/slice.md:192-194
- A: moving between phases is free
- B: rest advances the shift by exactly one phase along the tide.
- why: World says phase movement is free and is not a cost paid by the player; systems proposes rest that spends the hour and place at the bench. Systems itself names this tension as unresolved. The slice describes a free phase rail and says its lock is not enforced.

## F05 [codex] timeline
- files: bible/world.md:102-105, bible/cast.md:107-111, bible/slice.md:104-106
- A: Who is speaking: the night crew and the people who came to collect.
- B: Comes across the causeway at the end of The Run, and is there for Slack Water and not before
- why: World places the night crew among the Slack Water speakers, while cast says Margit (the night crew representative) is present only from the end of The Run. The slice follows that transition, so the stated Slack Water timing conflicts.

## F06 [codex] character presence
- files: bible/slice.md:129-135, bible/slice.md:157-162
- A: Nobody else. The yard is quieter at this hour than at any other, and the people who come across now have come to collect.
- B: Margit Brack and the night crew, and the residents who came to collect what they lent. ... Maud Bray, who is at the bench at every phase including this one
- why: The beat 4 speaker list says nobody else speaks besides Roald and Margit, while the ending beat in the same Slack Water phase includes the night crew, collecting residents and Maud. Both are presented as events in that phase without a stated transition or distinction in speaker scope.

## F07 [codex] item and want consistency
- files: bible/cast.md:172-177, bible/slice.md:39-40
- A: To have the pot down and covered before the water is over the wall, with the collar bone whole
- B: wants the pot down and covered with the collar bone whole
- why: Cast says Grissel hands over a heat-glove to mend, but her stated want and the slice's beat concern a collar bone, which neither file identifies as an item she hands over or connects to that want. This is an internal cast/slice mismatch in the actionable object.

## F08 [codex] item state / motivation
- files: bible/cast.md:55-60, bible/slice.md:74-78, bible/slice.md:97-100
- A: To get the packet boat off the blocks and across the channel on the evening tide, which needs his bone fid back with its stem sound, not merely whole.
- B: The fid's split stem ... mended so it is sound rather than whole
- why: The slice says the repaired fid is sound rather than whole, yet later says Ottmar wants the fid back and treats its being fused or retained as the alternative. Cast's condition is specifically that the stem be sound; slice's phrase 'rather than whole' makes the repaired state ambiguous and potentially fails that condition.

## F09 [minimax] item ownership / provenance
- files: bible/systems.md:54, bible/systems.md:59, bible/cast.md:76, bible/cast.md:79, bible/slice.md:210, pitches/pitch-a.md:36
- A: systems.md:54 "Sable's coat, waxed inside out by somebody who wades for a living and never got it back." / :59 "name": "Sable's waxed tar-coat"
- B: cast.md:79 (under ### Roald Fisk, cast.md:69) "**What they hand you to mend** -- His waxed tar-coat."
- why: Two different owners for the same item id `tar-coat`, and Roald's want is explicitly made checkable only against that object (cast.md:75-77: "it is the coat's job, and the coat as it stands will not do it"). The slice follows cast (slice.md:210-215), matching the pitch's "Sable's coat" (pitch-a.md:36). Acknowledged as unresolved at slice.md:214 ("The owner is unresolved."), but the item data still disagrees across systems.md/cast.md.

## F10 [minimax] reachability / systems-internal contradiction
- files: bible/systems.md:156, bible/systems.md:183, bible/systems.md:184, bible/systems.md:185, bible/slice.md:80, bible/slice.md:215
- A: systems.md:156-157 "It grants `Unpick`, and it is the only source of `Unpick` in the slice: without the knife in a worn slot there is no fusing at all, so the knife is not a tool, it is the price of every heirloom the player will build."
- B: systems.md:184-185 "The other five - the line, the hook, the lamp, the knife and the bar - are the backlog the recipe table below is written against, and none of them is in the slice until gate 4 says so."
- why: Within systems.md the knife is simultaneously required for fusing in the slice and excluded from the slice. Every recipe in systems.md:206-245 requires `Unpick`, and the slice makes fusion the centrepiece (slice.md:80-84), so with the reachability rule as written no heirloom can exist. Acknowledged at slice.md:215-218, which assumes the knife is in scope.

## F11 [minimax] capacity / item data
- files: bible/slice.md:78, bible/slice.md:79, bible/systems.md:156, bible/world.md:51
- A: slice.md:78-79 "That is three usable objects against four worn slots, and the fourth slot is never filled: the cap is visible, not binding."
- B: systems.md:156-157 "without the knife in a worn slot there is no fusing at all"
- why: slice.md counts three carried objects and declares the fourth slot permanently empty, while F02 requires a fourth carried item (the knife) in a worn slot to perform the slice's central fusion. The two statements about how full the satchel gets cannot both hold.

## F12 [minimax] beat breaks an engine/world rule
- files: bible/slice.md:99, bible/slice.md:100, bible/slice.md:107, bible/slice.md:159, bible/slice.md:199, bible/world.md:98
- A: slice.md:99-100 "If the fid is in the satchel he is terse about it; if it went onto the rack as somebody's tool he does not ask for it twice, and his politeness about that is the punishment." / slice.md:107-108 "*Sable Kearn*, only if the thing she wanted is what the rack took." / slice.md:159-160 "A resident whose object was fused is in the yard and hears their own name not read."
- B: slice.md:199-200 "A line cannot react to a flag, an item or a place, so a resident's version of an ask changes with the hour and with nothing else."
- why: Three beats are written as conditional on satchel/rack state that the slice's own known-limits say is not expressible; the only phase-aware lever is the transition payload (systems.md:327-347). The same unexpressible conditional is also in world.md:98-99 ("A resident who wanted an object you fused cannot offer you anything now"). These lines can only ever be their untoggled default.

## F13 [minimax] timeline / tide phase
- files: bible/world.md:25, bible/world.md:99, bible/world.md:100, bible/slice.md:127, bible/slice.md:137
- A: world.md:99-100 (The Run) "This is the phase in which the player crosses out and is refused, and then crosses back with a passenger - and a build that kept one cheap verb manages the return slowly, out loud, twice, in front of the yard."
- B: slice.md:127 "**Phase** -- Slack Water." (Beat 4, slice.md:122-141) and slice.md:137-138 "The crossing out with a passenger is possible in the way it is only possible at this hour"
- why: world.md places the crossing back with a passenger in The Run; slice.md places the passenger crossing in Slack Water (Beat 4) and has The Run's return carry no passenger (slice.md:112-116). world.md:25-26 also says the channel "is crossable at exactly one part of the shift", i.e. Slack Water, which contradicts world.md:99 inside world.md itself.

## F14 [minimax] world rule vs beat
- files: bible/slice.md:124, bible/slice.md:130, bible/slice.md:131, bible/world.md:103
- A: slice.md:130-131 "*Roald Fisk*, who is on the far side with his sister and cannot come across to help her, because the crossing goes one way this hour and he is on the wrong side of it."
- B: slice.md:124-125 "-- The causeway from the yard end to the town bank: the plank, the stepping, and the rest of it. Then back to the yard end of the same causeway, which is where the shift is read out."
- why: Beat 4's own Place has the kit-runner crossing to the town bank and back again at Slack Water, i.e. the crossing is two-way that hour, which contradicts the 'goes one way' justification invented to strand Roald. world.md:102-103 supports two-way ('the crossing is possible in the way it is only possible at this hour') and states no one-way rule; no file defines one.

## F15 [minimax] timeline / tide hours
- files: bible/slice.md:101, bible/world.md:95, bible/world.md:78, bible/world.md:102
- A: slice.md:101 "The ask at dusk, in the hour that is his: the crossing is at slack, the water is on the rise, and it is the coat's job and not anybody else's."
- B: world.md:95 "**The Run (the flood, late morning into the afternoon).**"
- why: The Run is dusk in the slice but late morning/afternoon in world.md. The whole shift runs 4am (world.md:78) to Slack Water, which world.md:102 calls 'the end of the shift' with high water - yet slice.md:151 and world.md:103-104 both stage Slack Water with 'evening work lit'. Inherited from pitch-a.md:36 ('a different version of the ask at dusk than at dawn'); the world bible's tide-hour table is the one that disagrees with its own slice.

## F16 [minimax] timeline vs world water state
- files: bible/cast.md:172, bible/slice.md:39, bible/world.md:13, bible/world.md:78, bible/world.md:102
- A: cast.md:172 "**Want** -- To have the pot down and covered before the water is over the wall, with the collar bone whole" (slice.md:39-40 repeats it)
- B: world.md:13-14 "The yard sits a few feet above high water, so at the top of a tide the sea is visible over the wall" / world.md:78-79 "**The Turning (roughly four in the morning).** The tide has just turned and the yard is at full water." / world.md:102 "Slack Water ... Water is high"
- why: The only water states world.md defines are full/high water at the opening beat and high water at Slack Water, with no later beat in which the water rises over the wall. Grissel's want therefore has no deadline that can fall inside the shift, and at The Turning (where she is placed, cast.md:168-169) the water is already at the top of the tide. Inference: the two files use 'over the wall' differently, but they cannot both be satisfiable.

## F17 [minimax] recipe data / systems-internal
- files: bible/systems.md:233, bible/systems.md:234, bible/systems.md:265, bible/systems.md:266
- A: systems.md:233-234 "\"id\": \"fuse-bar-hook\", \"inputs\": [\"winch-bar\", \"bend-hook\"],"
- B: systems.md:265-266 "**short-haul** keeps the bar's planted `Haul` and `Hook` and carries `Draw` ... Spent forever: the line's hauling and the hook's reach."
- why: The tarred line is not an input to this recipe, so 'the line's hauling' cannot be spent by it. Either the recipe inputs or the keep/spent list is wrong. (Related, same bullet: 'it is one verb fewer than its inputs looked like' - inputs give Haul+Hook, output has Haul+Hook+Draw, so the arithmetic of that claim is also unexplained; see UNRESOLVED.)

## F18 [minimax] systems rule vs item prose
- files: bible/systems.md:22, bible/systems.md:30, bible/systems.md:105, bible/systems.md:123, bible/systems.md:140, bible/world.md:44
- A: systems.md:30 "Two keys, then: `grants` is what the item gives, and `writes` is what it takes the old version of away from you. Nothing else in an item record is load-bearing." / systems.md:22 "An item does one of two things and there is no third kind." / world.md:44 "A carried object either grants a verb you did not have or rewrites one you did. There is no third kind."
- B: systems.md:105 "Nothing is rewritten. What you cannot do afterwards is haul anything at all with your hands alone" / systems.md:123 "Nothing is rewritten. What you lose by taking it is the hands: a hook is a thing you use one handed" / systems.md:140 "What it costs is the whole arm: you cannot steady and hold anything else at the same time"
- why: Three items that ship `grants` with no `writes` are described as removing existing capabilities or adding a handling restriction. That is a third kind of effect under systems.md:22 / world.md:44, and it is carried only in prose with no key. The lamp's 'whole arm' cost is not a verb change at all, so 'nothing else in an item record is load-bearing' does not hold.

## F19 [minimax] location / world rule
- files: bible/world.md:26, bible/world.md:27, bible/systems.md:381, bible/slice.md:151
- A: world.md:26-27 "The town on the far bank is where the shingle is signed, where the evening work is, and where the kit-runner cannot get to at flood without a good reason."
- B: systems.md:381 "The ending beat is at Slack Water, at the bench end of the causeway, with the town's evening work lit" / slice.md:151-152 "**Place** -- The bench end of the causeway, with the town's evening work lit across the water and the slate in the warden's arm."
- why: world.md puts the signature on the town bank; systems.md and slice.md read the slate at the yard end of the causeway. Acknowledged as an open point at slice.md:219-221, which takes the yard-side reading. Note the open point as written attributes the far-bank claim only to world.md, but world.md:26-27 also says the kit-runner 'cannot get to at flood' - the two readings are not reconciled.

## F20 [minimax] cast/slice contradiction; who knows what
- files: bible/cast.md:45, bible/cast.md:156, bible/cast.md:9, bible/slice.md:71, bible/slice.md:74, bible/slice.md:161
- A: cast.md:156 "**What they hand you to mend** -- Her own tarred line, brought in by her own hand." / cast.md:45 "Five of the seven hand over something at every phase in a different version of the same request." / cast.md:9-10 "Where a want below is checkable, it is checkable against the object named in the same entry."
- B: slice.md:74-75 "**What the player mends or earns** -- The two repairs, and then the decision. The fid's split stem ..." and slice.md:161-162 "*Maud Bray* ... who wants to know whether her scratch is on anything anybody is holding."
- why: Beat 2 has Maud speak but hands the player only the fid and the coat; her line never enters the satchel, so her want is not checkable in the slice and her line at the ending beat asks whether her scratch is on anything the player holds - which presupposes the player received and possibly fused her object. This is both a beat/cast gap and a knowledge contradiction.

## F21 [minimax] reachability / dead conditional
- files: bible/slice.md:68, bible/slice.md:70, bible/slice.md:107, bible/slice.md:80, bible/slice.md:183, bible/systems.md:184
- A: slice.md:68-70 "*Sable Kearn* ... She says the gear wants doing, and hands over the piece that does not want doing at all." (her object is a tarred line with a block, cast.md:98-99)
- B: slice.md:183-185 "The five items `bible/systems.md` holds as backlog - the tarred line, the bend hook, the shuttered lamp, the bench knife and the winch bar - are not reachable in this slice except where the open points below say otherwise" / slice.md:80 "In this slice there is exactly one reachable pair - the fid and the coat"
- why: Beat 2 hands the player an object systems.md lists as out of slice, and neither of slice.md's open points (slice.md:210-221) covers it. Consequently slice.md:107-108 ('Sable Kearn, only if the thing she wanted is what the rack took') can never fire: the only reachable fusion pair is fid+coat, so the rack can never take her line. A beat's dialogue is unreachable by construction.

## F22 [minimax] verb data the slice uses but systems does not supply
- files: bible/slice.md:137, bible/slice.md:139, bible/systems.md:103, bible/systems.md:92, bible/systems.md:250
- A: slice.md:137-139 "**What the player mends or earns** -- Nothing new; the beat spends everything the shift made. The crossing out with a passenger is possible ... The quiet coat is what puts somebody under you and keeps the weather off both of you"
- B: systems.md:103-104 "It grants `Haul`: you can take a load - including a passenger's weight - onto the line and let the line carry it" (tarred-line, systems.md:92-100 - backlog per systems.md:184-185); systems.md:250-251 Shelter exists only on the fused heirloom: "**quiet-coat** keeps the quiet `Climb` and the hands-kept `Wade`, and carries `Shelter`"
- why: Beat 4 requires carrying a passenger. The only verb systems.md defines that carries a passenger's weight is `Haul` from the tarred line, which systems.md excludes from the slice; `Shelter` exists only on the heirloom, which requires the excluded bench knife (F02). An un-fused satchel of fid + coat + whistle therefore has no verb the crossing is built on, yet cast.md:75-77 and slice.md:130-131 make the crossing the checkable want.

## F23 [minimax] recipe data / systems-internal
- files: bible/systems.md:198, bible/systems.md:206, bible/systems.md:244
- A: systems.md:198 "2. Where the union holds two forms of one verb, exactly one survives - the one the recipe names - and the other is spent with the piece that carried it."
- B: systems.md:206-244 recipe records carry only "id", "inputs", "output", "say" - e.g. :210-212 "\"id\": \"fuse-fid-coat\", \"inputs\": [\"bone-fid\", \"tar-coat\"], \"output\": \"quiet-coat\""
- why: The stated rule requires each recipe to name which form of a contested verb survives, but no recipe has any such key, and no listed pair actually produces two forms of one verb. Rule 2 is unimplementable as the data stands. (Related: fuse-bar-hook :233-237 is the only pair involving a `writes` item, and it is the one whose spent-list is wrong - F09.)

## F24 [minimax] cast-internal contradiction
- files: bible/cast.md:168, bible/cast.md:175, bible/slice.md:39
- A: cast.md:168-169 "**Role** -- Keeps the pitch pot: lights it, banks it, and puts it down and covers it. She is in the yard at The Turning when the pot is lit and gone before The Run"
- B: cast.md:175 "She is checking the glove all shift and asking about it without asking about it."
- why: She leaves before The Run but checks her glove 'all shift'; slice.md:39-40 places her only in Beat 1 (The Turning), with no later beat carrying the glove check that is the engine of her want.

## F25 [minimax] naming / data shape
- files: bible/world.md:73, bible/systems.md:291, bible/systems.md:337
- A: world.md:73-74 "the yard's residents do not carry clocks and the pack's phase keys are the tide's names" / systems.md:290-291 "The pack's phase keys are those four names; each is a tone sentence"
- B: systems.md:337 "\"when\": {\"phase-changes\": {\"to\": \"the-turning\"}}"
- why: The bibles say the phase keys are the names as written (The Turning), while the only concrete rule payload uses a slug 'the-turning'. Minor, and A2 (research/A2-feasibility.md:59-60) shows real pack keys are lowercase tokens like 'dusk', so the slug is probably right and the prose sentence is the sloppy part. Reported because the brief asks for naming mismatches; low severity.

## F26 [minimax] item data / provenance
- files: bible/systems.md:110, bible/cast.md:135, bible/cast.md:136
- A: systems.md:110-112 "A hook off the rack bent by a hull that wanted to be elsewhere, ground back to an edge by somebody who did not have a new one."
- B: cast.md:135-136 "**What they hand you to mend** -- A coat hook he has already taken off the rack, and already bent. The shank is drawn about a third of the way along and the bend is set hard enough that it will not open back without a vice."
- why: Same hook item id, different damage history (hull impact + ground back to an edge vs a drawn shank with a set bend) and different mending state (partly worked vs untouched). slice.md:46-47 also has the kit-runner refuse the hook outright ('it is not his mend to make'), while cast.md:133-134 has Tam offering to do a mend nobody gave him.

## F27 [minimax] naming / recipe data
- files: bible/systems.md:229, bible/systems.md:275, bible/slice.md:82
- A: systems.md:229 "\"output\": \"the-dark-mend\"" among otherwise slug-shaped ids (quiet-coat, thrown-whistle, grapnel-line, short-haul, spliced-line)
- B: systems.md:275 "the heirloom's name as the bench will say it (`quiet-coat` read aloud as \"the quiet coat\")" / slice.md:82 "the heirloom's name as the bench would say it"
- why: One of six heirloom ids breaks the id convention, and only one of six has the read-aloud form the preview is required to show. The bench-readable name for the-dark-mend is undefined in every file.

## F28 [minimax] world absolute vs systems
- files: bible/world.md:112, bible/world.md:152, bible/systems.md:304, bible/systems.md:316, bible/systems.md:318
- A: world.md:152-154 "It is never true that there is fast travel, a map screen, or a way to skip an hour ... moving between phases is a description of the yard, never a cost the player pays for being elsewhere." / world.md:112-113 "And there is no verb that waits or rests, and moving between phases is free"
- B: systems.md:304-305 "**`rest: true` - the player waits or rests, and it spends the hour.**" / systems.md:317-318 "There is no control that carries the kit-runner to Low Water from Slack Water ... and no back."
- why: world.md lists a wait/rest verb as inexpressible and phase moves as free and costless in both directions; systems.md writes a rest that spends the hour and the bench place and a rail with no backwards travel. systems.md:372-377 raises this with the owner and does not resolve it; slice.md:192-194 restates only the enforcement half.

## F29 [minimax] world rule vs systems (tone/mechanic disclosure)
- files: bible/world.md:131, bible/systems.md:275, bible/systems.md:276, bible/slice.md:82
- A: world.md:131 "It refuses to explain the mechanic out loud. The game never says \"this item grants a verb\"; residents say what the thing is for and what it did for them"
- B: systems.md:275-276 "the heirloom's full verb list including the two kept forms and the one inherited verb" / slice.md:82-83 "its full verb list including the inherited one, and underneath, in plain text and named piece by named piece, exactly what is lost forever"
- why: Inference, not a hard breach: world.md's prohibition is written about prose and residents' lines, and the preview is rack UI, but the required preview is the one place the game states verbs and loss explicitly, and both files present it as load-bearing. Worth an explicit ruling since world.md:129-138 lists mechanic-explanation refusals among the absolutes.
