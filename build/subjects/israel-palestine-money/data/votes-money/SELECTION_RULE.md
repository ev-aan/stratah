# Vote selection rule (written before any results were examined)

Written: 2026-10-08, before downloading or inspecting any roll-call data.

## Universe
All US House and Senate roll-call votes held 2019-01-03 through 2026-12-31
(116th, 117th, 118th, 119th Congresses), as listed in Voteview
`HSall_rollcalls.csv`.

## Keyword match
A roll call is a candidate if any of these Voteview fields — `bill_number`,
`vote_question`, `vote_desc`, `dtl_desc` (bill title / description text) —
contains, case-insensitive, any of:

    Israel  (covers Israeli)
    Palestin  (covers Palestine, Palestinian)
    Gaza
    Hamas
    Hezbollah | Hizballah
    UNRWA
    Iron Dome
    antisemitism | anti-semitism
    BDS
    boycott

`BDS` is matched as a whole word only (to avoid matching inside other tokens).

## Keep only passage / adoption votes
Keep a candidate only if its `vote_question` is a final-disposition question:

- "On Passage", "On Passage of the Bill", "On the Joint Resolution",
  "On the Resolution", "On the Concurrent Resolution",
  "On Motion to Suspend the Rules and Pass", "... and Pass, as Amended",
  "... and Agree", "... and Agree to the Resolution",
  "On Agreeing to the Resolution", "On the Conference Report",
  "On Motion to Concur in the Senate Amendment" / "House Amendment",
  Senate "On Passage of the Bill", "On the Joint Resolution",
  "On the Resolution", "On the Motion (Motion to Concur ...)" when
  it is the final disposition.

Exclude procedural votes: motions to table, cloture, motions to proceed,
motions to recommit, ordering the previous question, rules (H.Res. providing
for consideration), points of order, quorum calls, motions to waive, and
amendment votes.

## Known limits of this rule (declared in advance)
- Keyword matching on titles will include omnibus/appropriations bills only
  if their Voteview description text contains a keyword; large appropriations
  packages containing Israel aid under a generic title will be MISSED.
- Keyword matching may include bills where the term is incidental
  (e.g., a title that merely mentions Israel among many items). Matches are
  kept as matched; any judgement-based exclusion would be listed explicitly.
- Voteview's description text is secondary. Five votes are cross-checked
  against official Clerk/Senate XML.

---

# ADDENDA (written AFTER first results were seen; 2026-10-08). Kept separate on purpose.

**Why:** the first pass showed that Voteview's description fields are empty for ~1,291
roll calls in 2019-2026 (mostly amendment votes, but also a few passage votes), and that
Voteview's text sometimes paraphrases rather than giving the bill title. The original
rule says "bill title or vote question", so the addenda bring the official bill title in.
The keyword list and the passage-only filter are unchanged.

**Addendum A.** A passage-type vote whose Voteview text is empty is matched against the
Voteview text of other roll calls on the same bill in the same Congress.
(Effect: H.R. 6126, House roll 577, 2023-11-02.)

**Addendum B.** For every bill that had a passage-type roll call in 2019-2026 (1,914 bills),
the official titles were fetched from GovInfo BILLSTATUS XML
(https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{type}/BILLSTATUS-{congress}{type}{n}.xml)
and the same keyword rule was applied to the titles in `bill/titles/item`. Titles of type
"...for portions of this bill" do not count; such bills are listed but not selected.
(Effect: adds H.R. 5323, Iron Dome Supplemental Appropriations Act, 2022 — House roll 275,
2021-09-23 — and H.R. 4795, 2026-09-03. Not selected, portion-title only: H.R. 6395 and
S. 4049 (display titles: "...National Defense Authorization Act for Fiscal Year 2021"), and
H.R. 815 (display title: "Making emergency supplemental appropriations for the fiscal year
ending September 30, 2024..."; one portion is titled "Israel Security Supplemental
Appropriations Act, 2024").)

**Explicit judgement exclusion.** 116th Senate vote 179 (S.J.Res. 48, 2019-06-20) matched
only because Voteview joins the titles of about 20 other disapproval resolutions into that
one record. S.J.Res. 48 itself covers UAE/UK/Australia, and none of its official titles
contains a keyword. It is excluded and listed in excluded_matches.csv.

**Known consequence (not corrected):** only 2 Senate roll calls pass the rule (S. 1 in 2019;
S.Res. 417 in 2023). Senate action on these topics in 2019-2026 took the form of cloture
votes, motions to discharge arms-sale disapproval resolutions (2024-11-20, 2025-04-03,
2025-07-30, 2026-04-15), motions to table, amendment votes, and packages whose titles have
no keyword. The rule excludes all of these, so under the ">= 3 selected votes" threshold no
senator appears unless they also cast House votes. This follows from the rule as written.
The excluded Senate votes are listed in excluded_matches.csv.

**Not resolvable from documents:** the 17 en-bloc suspension votes of the 117th House
("Suspend the Rules and Pass Certain Bills") list no bill numbers in Voteview or in the
Clerk XML (legis-num = "MOTION"). Whether any bill in those packages carried a keyword
was not determined.
