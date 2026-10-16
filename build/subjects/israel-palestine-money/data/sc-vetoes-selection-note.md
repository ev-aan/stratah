# Security Council vetoes on Israel-Palestine: selection and hashes (added 2026-10-16)

Source table: UN DPPA veto dataset, https://api.psdata.un.org/public/data/DPPA-SCVETOES/json, downloaded 2026-10-16
(273 rows; sha256 fc3c4c2a1700140dfd79072a278ff75693d0bc9d67baa981aa520a0af8add124; stored outside the repository).

Rule (written before the new row was added): keep rows dated on or after 1993-01-01 whose `agenda` or `short_agenda`
contains "Palestin" or "Occupied", plus the row whose draft symbol is S/2024/312 (agenda "Admission of new Members";
the text of S/2024/312 recommends admission of the State of Palestine). Result: 25 rows.

`sc-vetoes-1993-2025.json` holds these 25 rows plus 20 rows on other Middle East items (Syria, Yemen, Hormuz) kept from
the first pass; the 25 selected are the rows listed in `sc-vetoes-meeting-records.csv`. sha256 of the JSON file after
adding the S/2024/312 row: 224510329f57f3f369d07f6e947de0f92dd5f990cf41a8ce911091177edd50b9.

`sc-vetoes-meeting-records.csv`: one row per selected veto with the meeting-record PDF hash (sha256 of the file served by
documents.un.org on 2026-10-16) and the result and Against passages extracted by script. Meeting 4438: the extracted
result line is partly garbled (the "has not been adopted" words are cut) but the Against list reads "United States of
America" and the next words read "owing the negative vote of a permanent member".
Item type: the 2023-12-22 row (S/PV.9520) is a vote on an oral amendment by the Russian Federation to the draft in S/2023/1029,
adopted afterwards as resolution 2720 (13-0-2); the amendment received 10-1-4.
