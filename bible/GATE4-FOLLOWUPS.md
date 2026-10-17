# Gate 4 follow-ups for Rylee (2026-10-17)

You approved the four bibles as canon at 04:55 (Project Home decision 228). That text is tagged
`canon-approved-2026-10-17` (commit 4a1100a).

**What changed after your approval.** The last continuity round (M1e, 04:57-05:01) was still running
when you approved, and Claude pushed it at 05:01. It edits 30 lines across the four files and fixes
the 11 small findings J01-J11 (record: `bible/CONTINUITY-4.md`). To see every line:
`git diff canon-approved-2026-10-17 5a7e7a7 -- bible/*.md`. Three of the fixes are judgement calls,
not just wording:

- **J02.** The coat's record no longer counts trips ("a passenger, held against you, at a walk"). But
  world.md:147 and slice.md:198 still give the coat-alone build two crossings.
- **J05.** The hands-under form lost at the hard is now named as **Roald's** ("how Roald goes under at
  the yard's foot").
- **J11.** The coat repair now says **both faults mended** (both elbows and the shoulder seam), so
  Roald's want can be checked against the coat.

Keep M1e (the default) or revert any of the three: say which.

**Still open after a final two-model check (05:03-05:09).** Codex found nothing, but it was shallow (no
tool calls). MiniMax found three, each with its own caveat. None are edited, since they would change
canon:

1. **C01: does Roald bring his sister at Slack Water?** All four bibles say he "comes back with his
   sister", but the slice says only the kit-runner can make the crossing. Either "comes back with"
   means "arrives at the hour she is brought over", or he carries her. This is your call. Each answer is
   a one-line fix.
2. **C02 (a clear slip).** world.md:115 puts "the resident whose coat is on the rack" at Low Water, but
   the coat has been in the kit-runner's satchel since the end of the Turning. Suggested fix: "the
   resident whose coat is in the satchel".
3. **C03 (a rules gap).** systems.md says quiet-coat spends the kit-runner's slow `Climb` and open-hand
   `Wade`, but rule 2 spends nothing for that pair, and rule 4 as written doesn't produce those losses.
   No other recipe spends starting verbs. Suggested fix: say the losses come from `writes` supersession
   at pickup (systems.md:26-28), not from rule 4.

Softer notes, not contradictions: world.md gives two shingle outcomes where systems/slice give three
(including Refused); Tam's want ("counted once") has no beat; the `tarred-line` item may conflate
Sable's line with the twelve-fathom record.
