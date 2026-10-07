# Selection rule (fixed 2026-10-07 BEFORE any per-country results were inspected)

Only the dataset schema and codebook had been read when this was written.

Source table: Voeten UNGA voting data, `completeVotes` (UNVotes-1.RData, Dataverse file id 10295576, dataset version 33).

A roll call is SELECTED if ALL of:
1. Date of vote (column `date`) is on or after 1993-01-01.
2. Whole-resolution vote: `amend == 0` and `para == 0` (amendment and separate-paragraph votes excluded; they are counted in a side tally only).
3. EITHER `me == 1` (Voeten issue code: "Votes relating to the Palestinian conflict")
   OR `short`/`descr` matches (case-insensitive) the regex
   `PALESTIN|ISRAEL|GAZA|JERUSALEM|UNRWA|OCCUPIED ARAB|OCCUPIED SYRIAN|GOLAN|MIDDLE EAST|NEAR EAST`.
   Rows selected only by text (not by `me`) are flagged `text_only` so the two routes can be compared.

Vote coding (codebook): 1 Yes, 2 Abstain, 3 No, 8 Absent, 9 Not a member. Rows with 9 or missing are excluded from counts.
Year = calendar year of `date` (not UN session).

Countries (COW-style ISO3 in `Country`): USA, CAN, GBR, FRA, DEU, IRL, NOR, ESP, QAT, TUR, IRN, EGY.

"Pattern change" (summary heuristic, mechanical): for each country, compute per-year Yes-share among votes cast
(Yes/(Yes+No+Abstain)); report years where the share moves by >= 0.15 versus the mean of the prior 3 years,
and years where the country's modal vote changes.

Landmark votes listed separately (per-country vote read from UN Digital Library record pages, not from Voeten):
A/RES/67/19, A/RES/ES-10/21, A/RES/ES-10/22, A/RES/ES-10/23, A/RES/ES-10/24, and the Sept 2025 New York Declaration endorsement (symbol to be found).
