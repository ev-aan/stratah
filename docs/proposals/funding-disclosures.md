# Proposal: funding and competing interests on sources (rules FD1 to FD8)

Status: PROPOSAL under `docs/SCHEMA_PROPOSALS.md`, on branch `process/funding-disclosures`. Not in force
until an independent reviewer has checked the seven points and the owner has decided. Agents do not merge it.
Requested by the owner on 2026-10-14, while reading the fluoride dig: "Do we know who funded each of these
studies?" The answer today is no, and the schema has nowhere to put it.

Worked example (data collected for this proposal, not yet applied to any dig):
- `funding-disclosures/fluoride-iq-funding.yaml`: 37 studies and reviews cited by `fluoride-iq`.
- `funding-disclosures/fluoride-iq-court-experts.yaml`: the expert witnesses in *Food & Water Watch v. EPA*.
- `funding-disclosures/ledger-entities-pilot.yaml`: the 58 funder names as candidate Ledger entities.

All validator runs below were made on 2026-10-14 against `origin/main`.

## 1. The failure case

`build/subjects/fluoride-iq` weighs about 37 studies and reviews, including the studies at the centre of the
dispute (Green 2019, Till 2020, Bashash 2017, Grandjean 2024) and the ones on the other side (Do 2024,
Warren 2025 and 2026, Broadbent 2015, Kumar 2025, Guichon 2024). A reader asking who paid for each one, and
what its authors declared, gets no answer from the dig. Three things go wrong:

1. **There is no field.** `build/SCHEMA.md` gives a source `authenticity` and `publication` blocks. Neither
   covers funding or declared interests. The word "fund" does not appear in the schema.
2. **Anything typed in passes.** An invented funder, of an invalid kind, citing a source that does not exist,
   is accepted silently (section 2).
3. **The facts are material to readers and sometimes cross between claims.** In this dig, an author of a
   study cited in the claims also appears in the court record cited by other claims: Green 2019's own
   disclosure says Bruce Lanphear would serve, unpaid, as an expert witness in an upcoming EPA fluoridation
   case, and the court's findings cite a witness named Lanphear (`src-fww-v-epa-2024`, lines 3865 and others).
   The court also calls a witness named Savitz "EPA's expert" (line 3129), and the dig cites a 2025 commentary
   by David A. Savitz (`src-savitz-2025`); the court text gives no first name, so the identity is a name
   match only. Today these connections can only live in prose, where nothing checks them and
   nothing guarantees both sides are treated alike.

## 2. Evidence

Validator run with a made-up funding block added to `src-green-2019` in
`build/subjects/fluoride-iq/sources/MANIFEST.yaml`
(`funding: {funders: [{name: 'Made Up Funder', kind: nonsense}], source: src-does-not-exist}`) and an
unsourced `funding_note` added to claim `fl-maternal-urine-signal`:

```
A. as filed:              20 subjects and 115 shared nodes checked: 0 errors, 111 warnings
B. with invented funding: 20 subjects and 115 shared nodes checked: 0 errors, 111 warnings
```

A and B are identical. The validator cannot tell a recorded funding statement from an invented one.

What the worked example found when the records were collected (read 2026-10-14, each from the document's own
funding and disclosure sections, then re-opened by an independent checker who fixed 8 records):

| | Count |
|---|---|
| Sources read in full or from the report's front matter | 31 of 37 |
| Blocked by the publisher, or abstract only (recorded as not read, nothing listed) | 6 |
| Funder mentions across the 31 read | 70 (government 47, university 8, intergovernmental 4, foundation 4, charity 2, professional body 2, other 3) |
| Industry funders named by any study read | 0 |
| Read sources naming no funder at all | 7 |
| Studies whose authors declared competing interests | 9 |

The checker's corrections show why a fixed shape and rules are needed: a reviewer-only conflict statement had
been read as covering the authors (NTP); funders taken from database metadata had been listed for a paper
nobody could open (Simon 2026); and author affiliations had been listed as competing interests for two papers
on one side of the question but not for papers on the other (Kumar 2025, Perrott 2017).

## 3. The proposed change, exactly

### 3.1 On each source (`sources/MANIFEST.yaml`), optional

```yaml
funding:
  checked: 2026-10-14
  read: full_text | front_matter | abstract_only | blocked
  read_from: "<where in the document, e.g. Europe PMC PMC6704756, Funding and Conflict of Interest sections>"
  funders:                        # as the document names them; [] when it states none
    - name: "<as named>"
      entity: <ledger entity id>  # optional; only once the Ledger (docs/proposals/ledger.md) is in force
      kind: government | intergovernmental | university | foundation | charity | industry | advocacy | professional_body | other
      country: <ISO 3166 alpha-2 | multiple>
      grants: ["<numbers as given>"]
      note: "<optional, e.g. 'supported the cohort, not this analysis'>"
  statement: >                    # plain paraphrase of what the document says about funding
  funder_role: "<what the document says about the funder's role, or 'not stated'>"
  competing_interests:
    declared_none: true | false | not_stated
    items: [{who: "<author>", what: "<plain paraphrase of the declaration>"}]
  other_records:                  # interests documented outside the paper, each with its own source
    - {who: "<name>", what: "<plain>", source: <manifest id>, where: "<page or line>", identity: confirmed | name_match_only}
  gaps: "<what could not be checked>"
```

### 3.2 Rules (text for `build/SCHEMA.md`, new section "Funding and competing interests")

- **FD1 Context, never evidence.** Funding and interests never raise or lower `evidential_weight`,
  `confidence`, `state` or `anchor_checked`, and never serve as a refutation (Rule 9 still requires material or
  primary-text evidence against the finding itself). The page labels the block "context, not evidence".
- **FD2 Silence means not looked up.** A source with no `funding` block has not been checked; it does not
  mean "no funding". `read: blocked` or `abstract_only` lists no funders and no interests; a dig page says
  how many sources were checked and which were not.
- **FD3 As the document states it.** Funders, grants, role and declarations come only from the document
  read. Funders found only in database metadata (PubMed, Crossref, Europe PMC grant lists) go in `gaps` as
  unverified, never in `funders`.
- **FD4 Declared interests, not inferred ones.** `competing_interests.items` holds what the authors declared.
  Author affiliations are not interests unless the document declares them as such.
- **FD5 Outside records need their own source.** Each `other_records` entry cites a manifest id and a page or
  line, and says whether the person's identity is `confirmed` or a `name_match_only`.
- **FD6 Same treatment for every side.** A dig that records funding for any study records it for every study
  and review it weighs, or lists the ones not yet done in its log; the reviewer checks that studies on each
  side of the question were treated alike.
- **FD7 No motive language.** Text that links a finding to its funding or to an author's interest is allowed
  only where a source documents the link (for example a journal's own correction or a court finding). Timing
  shown beside a decision is timing only (as LG8 in the Ledger proposal).
- **FD8 Shown on the claim, stored once.** The build shows, on each claim, the funding block of every manifest
  source in that claim's `anchor.sources`. Nothing is copied into `claims.yaml`, so the two cannot drift.

### 3.3 Validator (`build/conformance.py`, new function `check_funding`)

Errors for: unknown `read` value; unknown funder `kind`; `country` not ISO alpha-2 or `multiple`;
`declared_none` not one of its three values; `read: blocked` or `abstract_only` with funders or interest items
listed (FD2); an `other_records` entry whose `source` is not in the manifest, or with no `where` or `identity`
(FD5); `funding` keys inside `claims.yaml` (FD8, so it is never stored twice). Warning for: a dig with any
funding block whose `log.yaml` does not list the studies not yet checked (FD6).

### 3.4 Site (`build/tools/build_site.py`)

A "Funding and interests" panel on each claim (FD8), a coverage line under the Sources heading
("funding recorded for 31 of 37 studies; not opened: ..."), and the same panel on each source in the Sources
list. Wording is fixed: "Who paid for this study, and what its authors declared. Context, not evidence."

### 3.5 Link to the Ledger

When `docs/proposals/ledger.md` is in force, each funder may carry `entity:` pointing at a shared entity file,
so "everything NIEHS funded, across all digs" becomes one query. Funding statements almost never give an
amount or a recipient account, so they are NOT written as Ledger flows: a flow would need numbers the source
does not give (LG4). `ledger-entities-pilot.yaml` lists the 58 distinct funder names; under LG5 none are
merged on name alone (the NIEHS appears under several spellings and stays separate until a registry id joins
them).

## 4. What it does not change

- No claim, state, weight, anchor or finding in any dig changes. FD1 forbids it.
- `authenticity` (A1 to A10) and `publication` (PS1 to PS4) keep their meaning; `funding` sits beside them.
- No existing file is moved. The fluoride records are applied only after the owner decides, as their own
  logged change on `dig/fluoride-iq`, with a review round under `docs/PUBLISH_GATE.md`.

## 5. Impact

| Subject | Before | After | Migration |
|---|---|---|---|
| fluoride-iq | 0 errors | Expected 0 errors with 37 funding blocks added | Copy `fluoride-iq-funding.yaml` records into the manifest; log entry; review round |
| All other 19 subjects | 0 errors | 0 errors | None; the field is optional (FD2 makes its absence visible, not an error) |

Warning count on `main` is unchanged, because no subject on `main` has a funding block.

## 6. Alternatives considered

1. **Do nothing.** Rejected: section 2 shows invented funding passes, and the owner asked for it.
2. **Write funding into claim prose.** Rejected: unchecked, copied per claim, and uneven between sides (the
   checker found exactly this unevenness).
3. **Record funding only as Ledger flows.** Rejected: papers name funders and grant numbers but almost never
   amounts or recipients, so flows would require invented numbers (LG4).
4. **A separate `funding.yaml` per dig.** Workable, but funding is a fact about a source, like `publication`
   status, and belongs on the source entry where the build already reads it.

## 7. Neutrality check

The rules name no topic, side or outcome, and were applied to two sets pointing different ways:
- **fluoride-iq, both directions.** Green 2019 (inverse association; NIEHS, Health Canada, Ontario, CIHR;
  Lanphear's unpaid expert-witness declaration) and Do 2024 (no association; NHMRC; no interests declared)
  get identical fields. Kumar 2025 (critique of the NTP analysis; no funding; ADA advisory-committee and
  British Fluoridation Society memberships declared) and Grandjean 2024 (inverse association; 11 funders;
  three declarations) are treated the same way. FD4 removed affiliations from Kumar 2025 and Perrott 2017
  because affiliations had not been listed for any study on the other side.
- **vaccines-autism** (not collected; rule text tested against its manifest). Wakefield 1998 (retracted;
  claimed link) and Hviid 2019 (no association) would each carry the same block; FD3 and FD5 apply equally to
  the papers' own statements and to the court and GMC records the dig already cites.
No rule depends on which way a study's result points, who paid for it, or which side an expert served.

## Future work the owner has endorsed (each needs its own proposal)

On 2026-10-14 the owner agreed to treat funding as one part of a wider "who and why" layer, with its own view
beside the Atlas and the Ledger, showing how the people, money, places and decisions behind a dig connect.
Proposed next, in two groups that must stay separate:

- **Evidence quality (may affect weight, under existing rules):** pre-registration of the analysis; data
  availability and reanalysis; independent replication; venue (peer-reviewed, preprint, unpublished, court
  or hearing record); a structured study design card (design, size, exposure and outcome measures,
  adjustments, effect and interval).
- **Context only (shown, never weighted, under FD1-style firewalls):** author affiliations and the employer's
  stated position; author networks (extending citation-insularity to authorship); who commissioned a review and
  who later acted on it (the latter is adoption weight); who decided each decision; what followed (policy and
  measured outcomes); timing beside events.
- **Parked by the owner:** a general-audience narrative written for each dig.
