# Documented-flows pass, 16 October 2026: selection rules, methods and hashes

Written to fix what is counted before the amounts are summarised in claims. Raw downloads are stored outside the
repository; hashes below let a reader fetch and check. All rules apply to every country or side named; no side is
given a different rule.

## Record format
`documented-flows-2026-10-16.csv`: flow_id, channel, payer, payee, amount, currency, year_or_period, document,
document_date, source_id, document_url, read_status, note. Rows with read_status UNREAD list documents that were
not read, with the reason (blocked, not located, not searched, language).

## Channels and rules
1. US public laws (govinfo.gov, HTML text): search for Israel, Palestin, West Bank, Gaza, UNRWA, Foreign Military
   in P.L. 118-47, 118-50, 119-4 and Sec. 1002 of P.L. 115-141; every dollar line found for Israel, Jordan, Egypt,
   the Palestinian Authority and the West Bank and Gaza program is recorded.
   sha256: plaw118-47 4a1f78da4e44c5f1c5ea358ad4a68913523df9f3fe305a22f3ee9c6bbb7cd52c; plaw118-50
   a28f94e94257e3cb5b06499a5d98a4bafeea09181d8a62f474a1b4d69322856d; plaw119-4
   fda2d01ea333cbce2209eb2df6042682947a2248843fb3ce81b7338fab4e1cfc; plaw115-141
   12b165f1b76f830aa5e5a0e9fd3cd1d2921314830efa7f7a2af6b0e5ab58d762.
2. World Bank AHLC reports (documents.worldbank.org, found via the WDS API): every sentence with a dollar figure
   for donor financing, budget support, deductions, advances or loans in the reports of Sept 2016, Sept 2018,
   Sept 2019, Nov 2021, Sept 2022, Sept 2023 that the text search returned; the 2017 and 2020 reports were
   downloaded but not searched in full. sha256: 2016-09 48588718d16cd16bb00e7d547d692bef7fb7cca8a7a84e7ec9ac340d0e5c492f;
   2018-09 3b7cf979ed2fb097e6dae69b544a047281f9bc1bc9b04ce1986b332d688097fc; 2019-09
   41352a3e845ba2c8abd859ce0e4b577c9791a1dd4d5bafd61699618663c387da; 2021-11
   4aa69f70ddef2d588aa99c890c511726fb248b39f610ff40455090da5f16d16a; 2022-09
   2f9331cdb0be49522ecd2a7d1e7b4a0c352124ebbf4014d8a2d6e76a959ba573; 2023-09
   c0646cd42b82f1ad824ef3f5bfc7183bfe3c79cf5a80b6f349bcd3b66e8df96f.
3. OCHA FTS payer table (`ocha-fts/fts_payers_2016_2025.csv`): from the hashed flows in `ocha-fts/` (see
   raw_sha256.txt): years 2016 and later, boundary = incoming; paid plus commitment summed per payer and year;
   pledges in their own column; column "of_which_payee_is_UNRWA" sums flows whose destination is UNRWA. All payers
   are kept, not only the ones named in claims. Rerunning the rule on the hashed flows reproduces the file.
4. OECD DAC2A (SDMX API, recipient PSE, from 2016): measure 240 (gross ODA), price base current, unit USD;
   all donors kept. Raw file sha256 68a9dfde6e40a40c15e7e6447a3493a6554a04111c03c607aba909129d7fb5b9.
5. UK FCDO "Data underlying SID 2017-2024" (.ods), Data sheet, column AmountsExtended(GBP thousands) summed by
   recipient label and year for: West Bank & Gaza Strip, Israel, Türkiye, Turkey, Egypt, Jordan, Iran, Qatar, Saudi
   Arabia, Lebanon. Rows exist for West Bank & Gaza Strip (524 project rows over 2017-2024), Egypt (351), Iran (17), Jordan (507),
   Lebanon (480) and the label "Turkey" (535); there are no rows for Israel, the spelling "Türkiye", Qatar or Saudi Arabia (corrected
   16 Oct 2026; the earlier text said only the first label had rows). sha256 91524225f5370e0532028d5f2913a1ce9eab10991c400b729a2c874be6052c03.
6. CORDIS organisation.csv from FP7, Horizon 2020, Horizon Europe zips: ecContribution summed by participant
   country code for IL, PS, TR, QA, EG, IR, SA, AE, JO, LB. zip sha256: FP7 886ee47973584971259db3ab3de76feb4d95c9b13fbe41241b85e5bfc97113a6;
   H2020 7c00e367edbb22163d78b20fe466c9d910d2824d9ec882fc0a1a9f966335b914; Horizon Europe
   b9919057b77e897a884bbbd82005db1e25defd56f7c7be9e97d6ef9495ace6c4.
7. FARA register (FARA_All_ForeignPrincipals, FARA_All_RegistrantDocs): rows with no termination date and
   country label in {Saudi Arabia, Qatar, United Arab Emirates, Israel, Türkiye, Iran, Egypt, Palestine, Kuwait,
   Jordan}. The latest Supplemental Statement of the registrant (by date stamp) is downloaded; Item 14(a) is located
   by pattern; the largest dollar figure in the section is recorded. A figure is called attributable to the country
   only when the registrant has exactly one active principal in the whole register. Known limits: appendices
   not read; scanned statements without text are UNREAD; terminated principals are not listed. Register zip sha256:
   foreign principals 6eca1ecd9bf376d636cc480b8b429713754e84549848302b467e08a298209095; registrant documents
   e43c7518bf2c5ca20889977f44635e807af1b23143ce3aee64a80fb82717d053. Statement hashes are in the data file.
8. UK Charity Commission public extract (charity.zip sha256 6fc7e81fc4f431235cd850ce05edaee701ca1357e7f92a8b3f7ffdb18ba9e75b;
   annual return history 976d02f39ab0f552b2eeef36cc05323b1e74bb47c3deb1a4f7cc51dc81371227): registered, not-linked
   charities whose names match the regular expression `palestin|israel|gaza|aqsa` (case-insensitive), plus charity
   numbers 1040094 (Interpal), 328158 (Islamic Relief Worldwide), 1154288 (Human Appeal), 1176462 (Muslim Aid),
   1045315 (Medical Aid for Palestinians), 1020238 (The Welfare Association). Names matched include unrelated bodies.
   The six named were chosen before the output was seen; Qatar Charity and Jewish National Fund were searched for
   by name and found no registered charity with income above GBP 50,000 for either name.
9. ProPublica Nonprofit Explorer: search API pages (up to 100) for `palestin`, `gaza`, `israel`, `aqsa`; names
   containing a keyword kept (a keyword found only in a city name is dropped); organisation endpoint read for latest
   filing with data (total revenue, expenses, contributions). Returns for those organisations were not opened.
10. Commission pages 14 Apr 2025 sha256 e8d989db3a95823a82ce6f743a9fc6f9f6d4721758bccd7482210d1f3e220570; 23 Jun 2025
    a2b0a9939e68fc64a7e9355e9f5f4955c5ddddf6be1bd03ba14cced312ff35fe.

## Not done (see claim ipm-flows-unread-and-coverage)
UNRWA audited statements; ForeignAssistance.gov; explanatory statements and FY2026 act; IMF and Palestinian MoF
reports; Nordic, Japanese, German, Turkish, Qatari, Saudi, Iranian and Egyptian budget documents; EU Financial
Transparency System; Israeli, Dutch and German registers; IHH reports. Reasons are in the CSV.
