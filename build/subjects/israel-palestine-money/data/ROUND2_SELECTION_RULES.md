# Round 2 (16 October 2026): FEC pull and company document search, rules written before results

## Leads (not sources)
Two websites supplied as leads were used only to learn where primary records live. Neither is cited as a source in any
claim, and no figure from either is used in a claim. One data file records the first lead's stated candidate figures beside this
pull's figures (`fec-pull-vs-lead-site-independent-expenditures.csv`), as asked; that file is a comparison, not an anchor, and is limited to the 55 candidates the lead lists. The
second lead's company names were used as search terms (`company-israel-document-search-2026-10-16.csv` marks each name's origin).

## A. FEC records, 2022, 2024 and 2026 cycles
Raw files downloaded from fec.gov bulk downloads on 16 Oct 2026 (stored outside the repository), sha256:
- cm22 (cm22.zip): fb8962cc4cdc5e588913c7f6a6b4ddeccdff057beb81396d04f5df3b3f349c01
- cm24 (cm24.zip): 55cbb3d18ce750249d72b40b08ab132d6a550f7b760042fbd5f088e1d5287b90
- cm26 (cm26.zip): 25aa6521769b0dde3c1afe2525aaa500de616485e36679fd0296b04b1e114e39
- webk22 (webk22.zip): 12f0fa3ee0e35dc7ae5ccf1a4d7421e89d01945cece3d4791fd2693c31bea148
- webk24 (webk24.zip): 67238201b4649747cf91f8c13e4af746c88a03ae1e5a7d91ddb56330c040081c
- webk26 (webk26.zip): 74e6b604dcc69eb2a6aba05cf524573d13066351abb97df03faf7e61bcf32379
- independent_expenditure_2022 (ie22.csv): 2c45de89834adcb1906860c86bb99649b4880535c51a1318d6391d001bc02d04
- _2024 (ie24.csv): 26e2cf659f45aa6955c45612d1b9e6583d5d95c92f8b4572542b1347a8777bfa
- _2026 (ie26.csv): 76769f7430650593270cc10aa559d519f0d3ff700e0db903957afb6a87d381c6
- pas222 (pas222.zip): cb4de978d0968ebf8c095886df2799365297f02dbcd0d514c24f7a883b96d484
- pas224 (pas224.zip): dce0819d08c98cac52dfba13c6b9d0ffd4f731f8450a1dd3ef7834ce7c243e53
- pas226 (pas226.zip): 025f727c06ed541fb09e52963e3d516c7a70eb804232661fe0a4a1bf819b5316
- oth22 (oth22.zip): ec7d7fb16dddf4e4f08484fffa27ef67e170b2bd8da9bc77eeb6140bcccef59c
- oth24 (oth24.zip): d06f62bc47ea6293951c2c41d743d1d88df51e4561a5614756c95af048a20650
- oth26 (oth26.zip): 5dba05478acc1d555db1e21f9a487573519fa87f20c1d8ebe7e8dd7ed0953cb4

Committee rule (applied identically to every committee in the three committee-master files): a committee is selected when it is not a
candidate committee (types H, S, P excluded) and (a) its FEC id appears in an earlier data file of this dig, or (b) its name or its
connected-organisation name matches, case-insensitively, any of: ISRAEL, ZIONIST, ANTI.ZION, ZIONESS, whole-word AIPAC, JEWISH, PALEST,
whole-word-start ARAB, MUSLIM, ISLAM, TURK, whole-word-start IRAN, PERSIAN, QATAR, SAUDI, EMIRAT, LEBAN, EGYPT, whole-word GAZA, HAMAS, J STREET,
JUSTICE DEMOCRATS, EMGAGE, whole-word CAIR, NORPAC, whole-word RJC, UNITED DEMOCRACY PROJECT, PEACE NOW. The keyword list was fixed after one
trial run that matched unrelated words (JORDAN, GULF, ZIONS, HEBREW and AIPAC inside another word were removed or tightened) and before any
amount was read. Result: 87 committees (`fec-selected-committees-2022-2026.csv`): the file records 71 as selected by name keyword, 1 by connected-organisation keyword and 15 because the id appears in an earlier data file of this dig; a regular-expression re-count on 16 Oct 2026 over the stored names finds 86 of the 87 matching a keyword (the one that matches none is Vote Uncommitted MN, in the list only by earlier use); a reviewer counted 84 keyword matches and the difference of two was not resolved. The rule is mechanical; a committee's purpose was not read,
so the list includes committees chosen only by a name that contains a keyword.

Records pulled for each selected committee, the same for all:
1. Committee summary (webk files): receipts, individual and committee contributions, disbursements, contributions to other committees,
   independent expenditures, coverage end date (`fec-committee-summaries-webk-2022-2026.csv`).
2. Independent expenditures (Schedule E bulk file): one row per transaction, de-duplicated on (spender id, transaction id) keeping the
   highest file number; support/oppose stated.
3. Contributions out (pas2 file, Schedule B): transactions with memo code X dropped; types 24E and 24A (independent-expenditure items) are not
   repeated here because the Schedule E file is the source for them.
4. Committee-to-committee records (oth file): receipts (types other than 24x) and any 24x transfer not already in pas2.
All transaction rows are in `fec-transactions-2022-2026.csv.gz` with payer, payee, other id or candidate id, amount, date, transaction type,
image number (the filing image on docquery.fec.gov/cgi-bin/fecimg/?<image number>), transaction id and file number.

Not pulled, stated as coverage facts: individual-donor itemised receipts (Schedule A, `itcont` files); Form 3, 3X and 5 filings were not opened
(docquery PDFs); OpenFEC API not used; cycles before 2022; state and local committees; organisations not registered with the FEC (for example
501(c)(4) and 527 groups); committees whose names and connected-organisation names contain none of the keywords and whose ids are not in an earlier
data file; candidate committees as payers (they appear as payees). The 2026 cycle is partial: coverage ends 31 Aug to 30 Sep 2026 depending on filer.
Summary totals (webk) and transaction totals (Schedule E) differ slightly for the same committee and cycle; both are recorded.

## B. Company document search
For each name, three kinds of document were searched with the same rule; a name is "found" for a document type only when at least one document
of that type names Israel in the sense stated:
1. US federal contract awards: USAspending.gov API spending_by_award, award types A-D (contracts), 1 Oct 2007 to 16 Oct 2026, keyword "Israel"
   in the award description, recipient name search on the names listed in the data file. Each row records the award id, recipient name as
   returned, award amount as returned, dates, awarding agency and the description verbatim. USAspending recipient search can return related
   recipient names (for example a subsidiary or former name); the recipient name is recorded as returned and no relationship is asserted.
2. Foreign Military Sales notifications to Israel: the 43 Federal Register and DSCA notices already listed in `israel-bonds-and-us-arms-sales.csv`
   (kind "arms sale") were re-downloaded (38 read; 5 returned 403 and are UNREAD: media.defense.gov for 10-41, 13-20, 13-73, 16-40 and the
   dsca.mil page for 24-13). A company is matched when its name appears in a sentence about the principal or prime contractor.
3. SEC annual reports (10-K, 20-F, 40-F): the EDGAR full-text index was searched for the exact company name, a filer was accepted only when its
   name equals the searched name plus ordinary corporate words (inc, corp, ltd, holdings and similar); then the index was searched for the word
   "Israel" in that filer's annual reports and the most recent such filing was opened and sentences naming a government, ministry or military
   customer of Israel were recorded (at most 3, 15 words each).
Company sets: (1) the 58 entries of the first lead's list (57 companies; the entry "Airlines, Shipping, Logistics" is a group and was not searched);
(2) contractors named in the Israel notices that are not on that list; (3) all 182 companies of the UN business-database listing in this dig
(`un-business-database/companies.csv`). The same three searches were run for all three sets.
Result files: `company-israel-document-search-2026-10-16.csv` (one row per company and document type: found, searched/none found, unreachable) and
`company-israel-documents-found-2026-10-16.csv` (one row per document), `company-israel-notice-matches-2026-10-16.csv`.

## C. FARA statements read by eye
`fara-receipts-read-by-eye-2026-10-16.csv`: 19 principal-level records transcribed from the Item 14(a) table (and appendix) of the latest statements
of 19 registrants (the highest-value single-country-label statements and every Türkiye-labelled statement with a figure whose table could be read).
Each record has the statement's hash. Statements of MMGY Global, FTI Consulting, Hogan Lovells, Mercury Public Affairs, Sonoran Policy Group and others
with many principals were opened but their principal-level lines were not transcribed (marked in the claim as not read at principal level).
