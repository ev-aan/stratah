# Proposal: the Ledger, a validated per-dig transfer file (rules LG1 to LG4, LG7, LG9 to LG11)

Status: PROPOSAL under `docs/SCHEMA_PROPOSALS.md`, on branch `process/ledger` (draft PR #24). Not in force until an
independent reviewer has checked the seven points and the owner has decided. Agents do not merge it.
Requested by the owner on 2026-10-07 ("Yes to ledger"), after the `israel-palestine-money` pilot.
Narrowed on 2026-10-14 after the second independent assessment (it rejected the earlier shared-register version because
point 7 could not be met with one dig) to the route that assessment named: a per-dig validated file.

What this proposal is, in three lines:
- Each dig keeps its transfers in its own file, `build/subjects/<subject>/data/ledger.yaml`. `conformance.py` checks it.
  The file sits inside the dig, so the dig's `review.yaml` and the publish gate cover it by location.
- It makes no claim that needs a run across two digs. What it defers, and what each deferred piece needs, is in section 8.
- It depends on a separate naming proposal (section 3.3, "Dependency"). Until that is adopted, only organization-type
  entities are accepted; a person-type entity is an error.

What was run, and on what. `origin/main` is 2d69ee2 (21 subjects, 116 shared nodes). The pilot data is
`build/subjects/israel-palestine-money/data/ledger.yaml` at the tip of `origin/dig/ip-money` (fcd7cbe), a test input
only, not modified. All runs were made in scratch worktrees outside the repository; nothing was written to a checkout of
the repository. The validator code in section 3.6 is not in `build/conformance.py`: the runs insert the block printed in
that section, extracted from this file, into a scratch copy of `conformance.py` exactly as section 3.6 says to, and run
that copy. Section 2 shows the output.

### What changed since the shared-register draft
| Earlier finding | Where it is handled |
|---|---|
| Point 7: neutrality not run on two digs | scope cut to a per-dig file (this page); section 7; deferred items in section 8 |
| B2 loader, `main()` wiring, `_file`, base read, `r.err` path, SCHEMA text scope | section 3.6 (wiring code), sections 3.1 and 3.2 (exact SCHEMA text and the list of files), section 3.6 (wiring) |
| B3 F6 skipped node sources; first-word `read` match; manifests with other wording | LG1, section 3.4, F6, section 2.3 |
| B4 F7 did not compare originators | F7 and `ledger_origins` (section 3.6), origin rule in 3.4 |
| B5 stale numbers | whole of section 2 and section 5, re-run on main 2d69ee2 |
| B6 naming | removed from this proposal; dependency stated (3.3) |
| Non-blocking: real dates, real ISO codes, non-dict anchor, LG10 back doors, legal statuses, `approved_by`, silent without `--base` | F9, E3, C1, F13 and F10, LG3 and F5, G2 dropped, G0 |

## 1. The failure case

A record of who paid whom, how much, when, and on what document, has no place in the schema and no check in the
validator.

The real case is `build/subjects/israel-palestine-money` on `dig/ip-money`. Its money is in `data/ledger.yaml`:
136 entities and 189 flows, each flow with a `source` that is a manifest id (for example `src-fara-7649-clocktowerx`).
Three things go wrong today:

1. **Nothing checks it.** `conformance.py` does not read `data/`. A flow with an unknown payer, a source that is not in the
   manifest, a non-date and a non-number passes exactly like a correct one (section 2.1).
2. **Nothing separates a filed figure from a pledge, an estimate or a court finding.** The file uses 15 distinct `status`
   values and 21 distinct entity `type` values in free text. Nothing says which may be added together or shown beside a
   payment, and four of the 189 "flows" are legal records (a conviction, a vacated verdict, a judgment, a designation),
   not transfers.
3. **Nothing says what "read" means for a flow's source.** `filed` flows rest on manifest entries whose `read` field is
   free text; nine flows rest on a source read only through a summarizing tool (section 2.3).

A further case is a forecast, not an observation, and is not part of this proposal: that other digs would each write their
own copy of the same organization. Only one dig has ledger data (section 8).

## 2. Evidence

All numbers below are from `origin/main` 2d69ee2 and `origin/dig/ip-money` fcd7cbe, run on 2026-10-14.

### 2.1 The current validator does not see the ledger
`python3 build/conformance.py --base origin/main`, in a scratch tree of `origin/main` with the pilot's subject folder
added (22 subjects), as filed, then with one deliberately broken flow appended to `data/ledger.yaml` (`from: nobody`,
`amount: lots`, `date: someday`, `source: src-does-not-exist`):

```
main 2d69ee2 alone (21 subjects)                  0 errors, 113 warnings
+ pilot subject folder, as filed (22 subjects)    0 errors, 126 warnings
+ pilot, broken flow appended                     0 errors, 126 warnings
```
The last two lines are identical: the validator cannot tell a sourced flow from an invented one.

### 2.2 What the pilot file contains (counted from the file)
- 136 entities, 189 flows, 63 distinct flow sources; 174 manifest ids; all 189 flow sources resolve; none is Wikipedia.
- No flow has `id`, `rev` or `history`; no entity has `rev` or `history`. No flow has `amount: 0`. 4 flows have `amount: null`;
  every non-null amount has a currency (`USD` 182, `CAD` 3, `ILS` 3, `EUR` 1).
- 15 distinct `status` values: `filed` 159, `pledged` 8, `notified` 7, `contracted` 2, `estimate` 2, `sources_differ` 2, and one
  each of `reported_disputed`, `convicted`, `inferred`, `guarantee`, `verdict_vacated`, `judgment`, `designation`, `reported`,
  `partial`. `paid` is used by 0 flows.
- 21 distinct entity `type` values: `charity` 34, `company` 21, `foundation` 17, `organization` 15, `government` 10,
  `government_agency` 10, `aggregate` 8, `political_committee` 3, `political_target` 3, `armed_group` 2, `donor_advised_fund` 2,
  `individual_public` 2, and one each of `quasi_government`, `designated_network`, `un_agency`, `government_holding`,
  `government_fund`, `bank`, `government_committee`, `hospital`, `activity`.
- `date` forms: `YYYY` 123, `YYYY-MM-DD` 47, `YYYY-YYYY` 12, `FY2024`-style 3, `YYYY-MM` 2, `through FY2020` 1, `all years` 1
  (17 are not ISO dates). All are quoted strings.
- `country`: 12 values are assigned ISO 3166-1 alpha-2 codes or `multiple`; `IL/WB` (8 entities) and `EU` (1) are not.
- `ids` keys: `ein` 40, `fara_registration` 8, `cra_bn` 4, `budget_code` 2, `uk_charity` 1, and `status` 6 (free text, such as a
  revocation date, not a registry identifier).
- 3 flows touch the 2 `individual_public` entities; 3 flows go to the 3 `political_target` entities.
- 41 distinct `kind` labels; none is used by any rule below.

### 2.3 What the manifests say about "read" (16 manifests, 729 entries)
`SCHEMA.md` does not define the manifest `read` field. Each dig writes its own wording. The pilot's manifest header
describes `full`, `tool`, `snippet`, `blocked`, `quoted`; other digs use other forms. Section 3.4 defines the vocabulary
and the exact parse. Result of that parse over every manifest entry on `main` plus the pilot's (`ledger_read_class`):

| class | entries | | class | entries |
|---|---|---|---|---|
| `full` | 396 | | `metadata only` | 5 |
| not in the vocabulary (None) | 148 | | `not read` | 8 |
| `tool` | 51 | | `no` | 14 |
| `abstract` | 40 | | `blocked` | 2 |
| entry has no `read` field | 39 | | `partial` | 12 |
| `page` | 13 | | `snippet` | 1 |

The 148 entries in no class are not read as `full`. They fall in these groups, none mapped automatically (section 3.4):

| group of wording (first words) | entries |
|---|---|
| `yes, directly ...` or `yes, ...` | 77 |
| begins `abstract`, `full abstract`, `summary`, `title and`, `excerpts`, `introduction`, `page introduction` | 29 |
| begins `full text`, `full for`, `open full` | 17 |
| begins `opened <date>` | 8 |
| begins `search result`, `search summaries` | 3 |
| a negative or a flag: `NO -`, `not_read:`, `UNVERIFIED`, `recorded as read` | 5 |
| other (`Europe PMC ...`, `downloaded ...`, `saved ...`, `section ...`, `the claim lines ...`) | 9 |

Per subject (entries by class): `incandescent-lamp` 44 (None 43, `no` 1); `fluoride-iq` 80 (`full` 60, `abstract` 11, `metadata only` 3,
None 3, `tool` 2, `partial` 1); `anne-frank-diary` 28 (`full` 23, `not read` 5); `covid-origins` 102 (`full` 77, `partial` 11, None 10,
`abstract` 3, `not read` 1); the pilot 174 (`full` 133, `tool` 36, `blocked` 2, None 2, `snippet` 1). Five other subjects
have no `read` field on any manifest entry (39 entries); six of the 22 subjects have no manifest. Applied to the pilot's flows: 157 `paid`/`filed`
flows rest on a `full` source, 1 on `tool`, 1 on a source in no class.

### 2.4 The proposed check run on the pilot file
The code of section 3.6 was inserted into a scratch copy of `build/conformance.py` as section 3.6 says, and that copy was run
as `python3 build/conformance_patched.py --base origin/main` in the scratch tree of main plus the pilot folder. Two runs of the
pilot file: **raw** (exactly as filed) and **migrated** (the mechanical migration of section 5 applied in a scratch copy of the
file; nothing was written to the repository). The listing is one line per check code, with the first message.

```
raw:
22 subjects and 116 shared nodes checked: 561 errors, 140 warnings
  error   E2   x9    e.g. pa-off-budget: type 'government_holding' is not in the allowed list
  error   E3   x9    e.g. elad: country 'IL/WB' is not an assigned ISO 3166-1 alpha-2 code or `multiple`
  error   E4   x6    e.g. hlf: ids key 'status' is not a registry identifier
  error   E5   x136  e.g. gov-il: rev (integer) and history (non-empty list) are required
  error   F1   x189  e.g. None: flow id missing, not a string, or duplicated
  error   F12  x189  e.g. None: rev (integer) and history (non-empty list) are required
  error   F5   x4    e.g. None: status 'convicted' is a legal record, not a transfer: record it in the claims or timeline
  error   F6   x2    e.g. None: status filed needs a source read in full; 'src-fara-7662-davis' has read class 'tool'
  error   F9   x17   e.g. None: date '2012-2025' is not a real YYYY, YYYY-MM or YYYY-MM-DD date
  warning F13  x1    e.g. None: note reads like an absence statement; absence belongs in a claim with absence_anchor: true (LG10)
  warning F9   x13   e.g. None: a flow with an end date needs a note saying what the amount covers

migrated (the ids of the two person-type entities are replaced by <person-entity-1> and <person-entity-2> in this listing):
22 subjects and 116 shared nodes checked: 8 errors, 140 warnings
  error   E2   x2    e.g. <person-entity-1>: type 'individual_public' is person-type: entities that are people wait for the naming proposal
  error   F5   x4    e.g. ipm-027: status 'convicted' is a legal record, not a transfer: record it in the claims or timeline
  error   F6   x2    e.g. ipm-018: status filed needs a source read in full; 'src-fara-7662-davis' has read class 'tool'
  warning F13  x1    e.g. ipm-141: note reads like an absence statement; absence belongs in a claim with absence_anchor: true (LG10)
  warning F9   x13   e.g. ipm-002: a flow with an end date needs a note saying what the amount covers
```
In the raw run, E5, F1 and F12 fire on every record only because the file has none of the new fields; E2, E3, E4, F5, F6 and F9
are the real mismatches (9 entities with off-list types, 9 with a non-ISO country, 6 with `ids.status`, 4 legal-record
statuses, 2 `filed` flows whose source is not read in full, 17 non-ISO dates). In the migrated run nothing is left of the
mechanical mismatches. The 8 errors are not mechanical, and each needs a decision by the dig's author:
```
[E2] <person-entity-1>: type 'individual_public' is person-type: entities that are people wait for the naming proposal
[E2] <person-entity-2>: type 'individual_public' is person-type: entities that are people wait for the naming proposal
[F13] ipm-141: note reads like an absence statement; absence belongs in a claim with absence_anchor: true (LG10)
[F5] ipm-027: status 'convicted' is a legal record, not a transfer: record it in the claims or timeline
[F5] ipm-116: status 'verdict_vacated' is a legal record, not a transfer: record it in the claims or timeline
[F5] ipm-117: status 'judgment' is a legal record, not a transfer: record it in the claims or timeline
[F5] ipm-165: status 'designation' is a legal record, not a transfer: record it in the claims or timeline
[F6] ipm-018: status filed needs a source read in full; 'src-fara-7662-davis' has read class 'tool'
[F6] ipm-144: status filed needs a source read in full; 'src-990-dell-foundation' has read class None
```
`E2` x2: the two person-type entities wait for the naming proposal (3.3). `F5` x4: legal records are not transfers; they
belong in the claims or the timeline. `F6` x2: re-read the source in full (and re-label the manifest entry), or change the
flow's status to one not in totals. The warning `F13` is a flow note that says a payment was not found; the sentence moves
to a claim (LG10). The 13 `F9` warnings are flows with an end date and no note on what the amount covers.

Checks that read the append-only base and the claims were run too, on the migrated file in the scratch tree:

```
broken flows appended (one with an unknown payer, source, a non-date, amount "lots", kind no_payment_found;
one with amount 0 and a note "no payment found in the filing"):
  F3  ipm-bad: from 'nobody' does not resolve to an entity in this file
  F4  ipm-bad: source 'src-does-not-exist' is in neither this subject's manifest nor the shared nodes
  F9  ipm-bad: date '2025-13-45' is not a real YYYY, YYYY-MM or YYYY-MM-DD date
  F10 ipm-bad: amount 'lots' must be a number greater than zero, or null
  F13 ipm-bad: kind 'no_payment_found' states an absence; a flow records a transfer a source shows (LG10)
  F10 ipm-zero: amount 0 must be a number greater than zero, or null
  F13 (warning) ipm-zero: note reads like an absence statement ...
  -> 14 errors in total (8 + 6)
the same date written unquoted in YAML (2025-13-45):  1 error, "YAML does not parse: month must be in 1..12"
--base set to a commit holding the migrated file, then one flow removed, one flow and one entity edited with no rev bump:
  G1  gov-il: changed without a higher rev
  G1  ipm-006: flow was removed (LG9: append, never erase)
  G1  ipm-008: changed without a higher rev
run without --base:  [G0] file: run without --base: the append-only checks (G1, LG9) were skipped   (a warning)
```

### 2.5 The check run on other subjects
Of the 21 subjects on `main`, none has a `data/ledger.yaml`; the check returns nothing for them and the totals do not move:
`main` alone, unpatched and patched, both `0 errors, 113 warnings`. To exercise the checks on subjects other than the pilot,
two scratch fixtures were written into two other subjects' `data/` folders (`incandescent-lamp`, `fluoride-iq`): two invented
organizations and a handful of invented flows (amount 100, labelled `SYNTHETIC FIXTURE`) that cite those subjects' real manifest
ids and one real node each. They test the mechanics of the checks (read wording, originators, node sources), not the
neutrality of any rule, and were removed with the scratch tree.

```
ERROR    fluoride-iq/data/ledger.yaml: [F7] fx-2: status paid needs a corroboration source, read in full, with an origin different from `source`
ERROR    fluoride-iq/data/ledger.yaml: [F7] fx-4: status paid needs a corroboration source, read in full, with an origin different from `source`
ERROR    fluoride-iq/data/ledger.yaml: [F10] fx-5: amount 0 must be a number greater than zero, or null
ERROR    fluoride-iq/data/ledger.yaml: [F13] fx-6: kind 'no_payment_found' states an absence; a flow records a transfer a source shows (LG10)
ERROR    incandescent-lamp/data/ledger.yaml: [F6] fx-1: status filed needs a source read in full; 'src-us223898' has read class None
ERROR    incandescent-lamp/data/ledger.yaml: [F6] fx-4: status filed needs a source read in full; 'period-old-kingdom-egypt' has read class 'node without access: read'
```
What this shows: in `incandescent-lamp` a `filed` flow whose source's `read` is `yes, directly (OCR of ...)` fails F6, and a `filed`
flow citing a node with only `access: cited_only` sources fails F6, while a `filed` flow citing a node with `access: read` passes.
In `fluoride-iq` a `paid` flow corroborated by a source from the same host as its `source` fails F7, a `paid` flow with no
corroboration fails F7, and a `paid` flow corroborated by a source from a different host passes. `amount: 0` and a
`no_payment_found` kind are errors. (The 22-subject run with all fixtures: 14 errors, 8 from the pilot and 6 from the fixtures.)

## 3. The proposed change, exactly

### 3.1 What an adoption changes (all owner-only paths; this proposal changes none of them)
| File | Change |
|---|---|
| `build/SCHEMA.md` | One new section, "Ledger (per-dig transfer file)", appended after the last section. Its text is the block in 3.2, verbatim. No existing section is edited: N25 (anchor format) and P5 are unchanged. |
| `build/conformance.py` | Four imports added at the top; the block of 3.6 inserted before `def main():`; one line added in `main()`. Nothing else. |
| `docs/PUBLISH_GATE.md` | One sentence in "How a review is done", step 2: for a subject with `data/ledger.yaml` the reviewer also opens the sources behind a sample of the flows, every `paid` flow included. The exact wording is the owner's. |
| `build/subjects/<subject>/data/ledger.yaml` | Created or migrated by that dig, on its own branch, in its own PR, with a new entry in that dig's `log.yaml`. |

### 3.2 Text for `build/SCHEMA.md`

~~~markdown
## Ledger (per-dig transfer file)

A dig that records money moving between parties keeps it in `build/subjects/<subject>/data/ledger.yaml`. The file is part
of the dig: it is reviewed with the dig and published only with it (LG11). Conformance checks it (`check_ledger`). A flow is
a record of what a source shows, not a finding (LG7).

### File
```yaml
note: free text
entities:
  - id: gov-x                       # string, unique in the file
    name: "..."
    type: government                # list below
    country: US                     # assigned ISO 3166-1 alpha-2 code, or `multiple`
    country_note: "..."             # optional: the source's own wording for the place
    ids: {ein: "..."}               # optional: registry identifiers only (keys below)
    note: "..."                     # optional
    rev: 1
    history: [{rev: 1, date: "2026-10-14", change: "..."}]
flows:
  - id: f-001                       # string, unique in the file, never reused
    from: gov-x                     # entity id
    to: org-y                       # entity id, different from `from`
    amount: 1500000                 # number greater than zero, or null when the source gives none
    currency: USD                   # three capitals; required when amount is set
    date: "2025-03"                 # YYYY, YYYY-MM or YYYY-MM-DD, as precise as the source; quote it
    end: "2025-09"                  # optional, same forms, not before `date`
    period_label: "FY2025"          # optional: the source's own label for the period
    date_note: "..."                # required when date is null: the source's wording
    kind: grant                     # snake_case display label; used by no rule
    status: filed                   # transfer status, list below
    source: src-abc                 # manifest id of this subject, or a shared node id
    corroboration: [src-def]        # required for `paid`
    note: "..."                     # required for `inferred`, for amount null, and with `end`
    rev: 1
    history: [{rev: 1, date: "2026-10-14", change: "..."}]
```

### Closed lists (a new value needs a change to this section under docs/SCHEMA_PROPOSALS.md)
Transfer statuses. "Totals" says whether a flow may be added into a total.

| status | meaning | totals |
|---|---|---|
| `paid` | the transfer is shown by one record and corroborated by a second record from a different originator, both read in full | yes, as `paid` only |
| `filed` | a document filed by a party records the transfer: that party's own report, not a verified payment | yes, as `filed` only |
| `partial` | a filed record whose amount is incomplete | no |
| `pledged` | announced or promised, not shown as paid | no |
| `contracted` | a contract or agreement to pay exists | no |
| `guarantee` | a loan or payment guarantee, not a transfer | no |
| `estimate` | an estimate or a ceiling | no |
| `notified` | a notice of a proposed transfer with a maximum value | no |
| `reported` | a third party reports the transfer; not read in a filing | no |
| `reported_disputed` | reported, and a source disputes the figure or the fact | no |
| `sources_differ` | sources give different figures; each is recorded | no |
| `inferred` | inferred by the entry's author, not read in a document | no |

A conviction, a judgment, a vacated verdict and a designation are legal records, not transfers. They are not flows;
they belong in the dig's claims or timeline.

Entity types: `government`, `government_agency`, `government_fund`, `quasi_government`, `company`, `bank`, `charity`,
`foundation`, `donor_advised_fund`, `political_committee`, `un_agency`, `armed_group`, `designated_network`, `organization`,
`aggregate` (a group, or a category, that a source gives only as a total). Every entity is an organization or an aggregate.
A natural person is not an entity in this section. `ids` keys: `ein`, `cra_bn`, `uk_charity`,
`fara_registration`, `company_number`, `budget_code`, `fec_id`, and nothing else.

### Manifest `read` vocabulary (used by LG1)
The `read` field of a manifest entry starts with one keyword: `full`, `partial`, `abstract`, `page`, `tool`, `snippet`,
`blocked`, `quoted`, `not read`, `metadata only` or `no`. The keyword is the whole value or is followed by ` (`, or by one of
`;` `:` `.` `,` and a space; what follows is a qualifier for the reader and is not parsed. The longest keyword that matches is
the class. A value that matches no keyword (for example `yes, directly`, `full text ...`, `full for ...`, `abstract only`) has no
class and is never read as `full`. Meanings: `full` the whole document was opened and read; `partial` part was read; `abstract`
an abstract or summary; `page` a web page, not a document; `tool` read through a summarizing tool; `snippet` a search result
only; `blocked` could not be opened; `quoted` known only as quoted elsewhere; `not read`, `metadata only`, `no` not read. A bare
YAML `no` counts as `no`. A shared node counts as read in full if one of its sources has `access: read` (N12).
Origin of a source: a manifest entry's `origin` if it has one, else the registrable host of its `url` (the last two labels, the
last three before `co`, `com`, `org`, `gov` or `ac` under a two-letter country), together with the origins of any entry named in its
`copy_of` or `derived_from`; for a node, each source's `origin` and `derives_from`. Two sources have different originators when
their origin sets do not intersect. Host is a proxy: two institutions on different hosts pass, a mirror on another host
passes unless `copy_of` is stated. The reviewer checks what the proxy cannot.

### Rules
- **LG1 Every flow has a source that was read.** `source` is a manifest id of this subject or a shared node id. Wikipedia is
  never a source. A flow with status `paid` or `filed` needs a source read in full (above). A source in any other class, or in
  none, supports only a status that is not in totals.
- **LG2 Both ends exist and are organizations.** `from` and `to` are entities of this file and differ. Entity types and `ids`
  keys are the lists above. Two entities of one file with the same registry identifier are one entity and are an error.
- **LG3 Status is stated, from the transfer list.** Only `paid` and `filed` enter a total, and each only with its own status:
  a total is shown for one status and one currency, labelled with both. A `filed` flow is a party's own report; no page or
  claim calls it paid. A `paid` flow lists in `corroboration` at least one source, read in full, with an originator different
  from `source`. Legal records are not flows (above).
- **LG4 Amounts and dates stay as the source gives them.** An amount is a number greater than zero, or `null`; zero is not an
  amount. A date is a real calendar date at the source's precision. A range is `date` plus `end` (`end` as a year runs to the
  end of that year; `end` is not before `date`); a fiscal year is written with the year or dates the source states and
  `period_label`; a source with no start date gives `date: null` and `date_note`. Conversion, inflation adjustment and fiscal
  calendars are separate, labelled calculations of class `synthetic`, never written into `amount` or `date`.
- **LG7 A flow is a record, not a finding.** It carries no evidential weight. A claim that depends on a transfer cites the
  flow's own `source` in its `anchor.sources` and says in `anchor.description` what was read there; its weight follows that
  source and what was read, as for any claim. A claim may not cite a flow id in its anchor, and `anchor.flows` is not a key.
  Same firewall as threads (TH2) and transmission chains (X3).
- **LG9 Append-only.** A correction is a new `rev` with a new `history` entry. A flow or entity is never removed and earlier
  `history` entries are never edited. Conformance compares with the base ref when run with `--base`; without it, it warns that
  this check was skipped.
- **LG10 Absence is not a flow and is not evidence.** The absence of a flow in the file is never evidence that no payment
  occurred; the file holds only what a source shows and says nothing about what was not searched. There is no status, kind,
  key or amount for "no payment found". A claim that rests on "no flow found" lives in `claims.yaml` with
  `anchor.type: search-record` listing what was searched and where, with `absence_anchor: true`, capped at provisional (the
  absence-anchor rule in `conformance.py`). Text in a flow's `note`, `date_note` or `period_label`, or in an entity's `note`, that states a payment was
  not found is a warning: the sentence moves to a claim.
- **LG11 The ledger is part of the dig.** `data/ledger.yaml` is reviewed with the dig (docs/PUBLISH_GATE.md) and is shown
  on the site only if its subject is listed under `publish` with a `review.yaml` of status `passed` or
  `passed_with_open_items`. Nothing in this section renders flows; any page or export that does follows the subject's publication.
~~~

### 3.3 Dependency: the naming rule is a separate proposal
The owner's intent of 2026-10-14, stated in chat, is that the private-individual name rule does not apply to political
figures, public profiles, or publicly known executives and board members of organizations acting in that role. That is not in
any rule file, and a chat statement alone does not change a rule (`CLAUDE.md`, `docs/SCHEMA_PROPOSALS.md`). The naming rule is
going into its own proposal. This is a dependency, not a decision:
- Until a naming rule is adopted, this proposal accepts only organization-type entities (`aggregate` included). Any
  person-type entity is an error to be sent to the naming proposal: `check_ledger` reports type `person_public`,
  `individual_public`, `political_target` and any type containing `person`, `individual` or `target` as E2 with that message.
- This proposal contains no naming standard, no `naming` field and no category of person. When the naming proposal is
  adopted it adds its own entity type, fields and checks; it does not need anything in this proposal to change except the E2 list.
- What this proposal cannot check: a private person's name written into an entity `name` or `note`, an alias, a flow `note`, or
  an `aggregate` label. That is the reviewer's check (`docs/REVIEW.md`), and the validator does not catch it.
- Effect on the pilot (section 5): 2 `individual_public` entities and the 3 flows that touch them cannot pass until the naming
  proposal is adopted or the dig's author removes them; the 3 `political_target` entities are re-pointed to one `aggregate` of
  recipients, and the name of the opposed candidate is not carried into the ledger (it stays in the filing the flow cites).
  That loses a fact from the ledger; it does not remove it from the source.

### 3.4 The manifest `read` vocabulary and the existing manifests
The vocabulary is defined in the SCHEMA text (3.2) and used only by F6 for sources a flow cites. It does not require any
dig that has no ledger to change its manifest, and this proposal changes no manifest. Section 2.3 lists what the parse does to
the 729 existing entries: 396 are `full`; 148 match no keyword. For a dig that adopts a ledger, a cited source whose wording has
no class must be re-labelled by the dig's author when they next edit the manifest (a logged change after re-checking what was
read), with these suggested targets and never an automatic mapping:

| existing wording | entries | suggested label |
|---|---|---|
| `yes, directly ...` | 77 | `full` only if the whole document was read, else `partial`; the qualifier already states the extent |
| begins `abstract`, `full abstract`, `summary`, `title and`, `excerpts`, `introduction`, `page introduction` | 29 | `abstract` or `partial` |
| begins `full text`, `full for`, `open full` | 17 | `full` or `partial` as the qualifier says |
| begins `opened <date>` | 8 | `partial` unless the qualifier says the whole document |
| begins `search result`, `search summaries` | 3 | `snippet` |
| `NO -`, `not_read:`, `UNVERIFIED`, `recorded as read` | 5 | `no` or `not read` |
| other | 9 | by reading the entry |
| `full ...` with a qualifier that limits the reading (for example `full (executive summary only; ...)`) | in the 396 | the parse accepts it as `full`; the qualifier is not parsed, so the reviewer reads it |

The last row is a stated limit: F6 is necessary, not sufficient.

### 3.5 Checks
Each check fires on the condition shown. "Level" is what conformance does: an error stops the deploy, a warning is printed.

| Check | Fails when | Level | Rule |
|---|---|---|---|
| L0 | the file is not a mapping, or an entity or flow is not a mapping | error | file format |
| E1 | entity `id` missing, not a string, or duplicated | error | LG2 |
| E2 | `type` not in the entity list; a person-type name (3.3) gets its own message | error | LG2 |
| E3 | `country` is not an assigned ISO 3166-1 alpha-2 code (249 codes, in the code) or `multiple` | error | LG2 |
| E4 | an `ids` key is not a registry key | error | LG2 |
| E5 | `rev` not an integer, `history` empty, or the last `history` entry's `rev` differs | error | LG9 |
| E7 | two entities share a registry key and value | error | LG2 |
| F1 | flow `id` missing, not a string, or duplicated | error | LG9 |
| F3 | `from` or `to` is not an entity of the file, or they are equal | error | LG2 |
| F4 | `source` is in neither the manifest nor the nodes; or a manifest URL, or any URL of a node's sources, is on wikipedia.org | error | LG1 |
| F5 | `status` is a legal record (`convicted`, `judgment`, `verdict_vacated`, `designation`), or not in the transfer list | error | LG3 |
| F6 | status `paid` or `filed` and the source is not read in full: a manifest `read` class other than `full`, or a node with no source marked `access: read` (applies to manifest and node sources) | error | LG1 |
| F7 | status `paid` and no `corroboration` id, other than `source`, that resolves, is read in full, and has an origin set disjoint from the origin set of `source` | error | LG3 |
| F8 | status `inferred` without a `note` | error | LG3 |
| F9 | `date` neither a real calendar date in the three forms nor `null` with a `date_note`; `end` not a real date, or its last day before `date`'s first day | error | LG4 |
| F9 | `end` present and no `note` | warning | LG4 |
| F10 | `amount` not a number greater than zero or null (zero, negative, text, boolean, infinity are errors); or set without a 3-capital `currency` | error | LG4 |
| F10 | `amount` null and no `note` | warning | LG4 |
| F11 | `kind` is not `snake_case` | error | LG4 |
| F12 | flow `rev` not an integer, `history` empty, or last entry's `rev` differs | error | LG9 |
| F13 | `kind` contains the word `no`, `not`, `none`, `absent`, `absence` or `missing`; or a flow has the key `absent`, `no_payment` or `none_found` | error | LG10 |
| F13 | a flow `note`, `date_note` or `period_label`, or an entity `note` or `country_note`, matches an absence phrase (`not found`, `no record`, `none found`, `no payment`, `no flow`, `absent`, `not located`, `no trace`, `nothing found`) | warning | LG10 |
| G0 | conformance was run without `--base` and the file has entities or flows | warning | LG9 |
| G1 | with `--base`: a flow or entity of the base is missing; or changed without a higher `rev`; or earlier `history` entries were edited | error | LG9 |
| C1 | a claim of the same subject has an `anchor.flows` key, or contains a flow id (whole-id match) in its description, sources or nodes; a claim whose `anchor` is not a mapping is skipped here (N25 reports it) | error | LG7 |

Not enforced by the validator, and said so: that a source says what the flow says (reviewer, `docs/REVIEW.md` A); that a `filed`
flow is not in fact a verified payment; that a `full` qualifier does not limit the reading; that two hosts are two originators; that
LG3's totals rule holds in any page or claim text; that a person's name is not hidden in a label or note (3.3); that the absence phrase
list catches every wording; that the dig's review is newer than its last ledger edit (the publish gate checks that a passing
`review.yaml` exists, not its date, for every file in a subject). The `approved_by` field of the earlier draft is dropped: it
was a field the author writes and gave no safeguard.

### 3.6 Code and wiring
Add these four imports at the top of `build/conformance.py`: `import calendar`, `import math`,
`from datetime import date as _date`, `from urllib.parse import urlparse`. Insert the block below before `def main():`. In
`main()`, add the line `check_ledgers(r, subjects, args.base)` immediately after `nodes = check_nodes(r)`.
The block uses only names the file already defines (`ROOT`, `load`, `load_sources`, `git_show`, `yaml`, `glob`, `os`, `re`).

How it works. **Loader:** `check_ledgers` visits every subject folder in `subjects`, looks for `data/ledger.yaml`, and
parses it with the file's own `load`. There is no `_file` key; the subject is the folder. **Base read:** with `--base REF`,
`git_show(REF, "build/subjects/<subject>/data/ledger.yaml")` returns the file at the base ref, as `check_history` does for
logs; a file not present at the base is a new file (`{}`, nothing to compare); without `--base` the base is `None` and the
check warns (G0). **Reporting:** `check_ledger` is pure and returns `(errors, warnings)` as `(code, where, message)`; the
wiring turns each into `r.err(rel, "[code] where: message")` or `r.warn(...)`, where `rel` is the file's path from the repo
root. **Parse errors:** a YAML syntax error, or an unquoted impossible date such as `2025-13-45` (the loader raises
`ValueError`), is reported as one error for the file and no other ledger check runs on it. **Sources and nodes:** the
subject's manifest comes from the existing `load_sources`; nodes are read once from `build/nodes/*.yaml`. **Claims:** the
subject's own `claims.yaml`.

```python
# --- Ledger (docs/proposals/ledger.md): per-dig transfer file build/subjects/<subject>/data/ledger.yaml ---
# New imports at the top of conformance.py: `import calendar`, `import math`, `from datetime import date as _date`, `from urllib.parse import urlparse`.

LEDGER_ISO_COUNTRIES = set((
    "AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI "
    "BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN "
    "CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK "
    "FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM "
    "HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN "
    "KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK "
    "ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP "
    "NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW "
    "SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF "
    "TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI "
    "VN VU WF WS YE YT ZA ZM ZW"
).split())
LEDGER_ENTITY_TYPES = {"government", "government_agency", "government_fund", "quasi_government",
                       "company", "bank", "charity", "foundation", "donor_advised_fund",
                       "political_committee", "un_agency", "armed_group", "designated_network",
                       "organization", "aggregate"}
LEDGER_REGISTRY_KEYS = {"ein", "cra_bn", "uk_charity", "fara_registration", "company_number",
                        "budget_code", "fec_id"}
LEDGER_STATUSES = {"paid", "filed", "partial", "pledged", "contracted", "guarantee", "estimate",
                   "notified", "reported", "reported_disputed", "sources_differ", "inferred"}
LEDGER_LEGAL_STATUSES = {"convicted", "judgment", "verdict_vacated", "designation"}  # not transfers
LEDGER_IN_TOTALS = {"paid", "filed"}            # each summed only with its own status and currency
LEDGER_READ_KEYWORDS = ("full", "partial", "abstract", "page", "tool", "snippet", "blocked",
                        "quoted", "not read", "metadata only", "no")
LEDGER_ABSENCE = re.compile(r"not found|no record|none found|no payment|no flow|absent|not located|"
                            r"no trace|nothing found", re.I)
LEDGER_ABSENT_KIND = re.compile(r"(^|_)(no|not|none|absent|absence|missing)(_|$)")
LEDGER_PERSON_TYPE = re.compile(r"person|individual|target")


def ledger_read_class(value):
    """Class of a manifest `read` value: the longest vocabulary keyword that is the whole value or is
    followed by ` (`, or by one of `;:.,` and a space. Anything else (including `yes, directly`,
    `full text ...`, `full for ...`) is None, which never counts as read in full. A bare YAML `no` is False."""
    if value is False:
        return "no"
    v = str(value).strip()
    for k in sorted(LEDGER_READ_KEYWORDS, key=len, reverse=True):
        if v == k or re.match(re.escape(k) + r"( \(|[;:.,] )", v):
            return k
    return None


def ledger_read_in_full(ref, manifest, nodes):
    """True if a flow source was read in full: a manifest entry whose `read` class is `full`, or a
    shared node with at least one source marked `access: read` (N12)."""
    if ref in manifest:
        return ledger_read_class(manifest[ref].get("read")) == "full"
    if ref in nodes:
        return any(isinstance(s, dict) and s.get("access") == "read" for s in nodes[ref].get("sources") or [])
    return False


def ledger_origins(ref, manifest, nodes, seen=None):
    """Set of origin labels behind a source. Manifest entry: its `origin` if it has one, else the
    registrable host of its `url` (last two labels, three before co/com/org/gov/ac), plus the origins of
    entries named in `copy_of` or `derived_from`. Node: each source's `origin` and `derives_from`.
    Two sources have different originators when their sets do not intersect."""
    seen = seen or set()
    if ref in seen:
        return set()
    seen.add(ref)
    out = set()
    if ref in manifest:
        e = manifest[ref]
        parts = urlparse(str(e.get("url") or "")).netloc.lower().split(":")[0].split(".")
        k = 3 if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in ("co", "com", "org", "gov", "ac") else 2
        out.add(str(e.get("origin") or ".".join(parts[-k:]) or ref))
        for key in ("copy_of", "derived_from"):
            if isinstance(e.get(key), str):
                out |= ledger_origins(e[key], manifest, nodes, seen)
    elif ref in nodes:
        for s in nodes[ref].get("sources") or []:
            if isinstance(s, dict):
                out.add(str(s.get("origin") or ref))
                d = s.get("derives_from")
                out |= {str(x) for x in (d if isinstance(d, list) else [d] if d else [])}
    return out or {str(ref)}


def ledger_span(d, end=False):
    """(earliest, latest) calendar day of YYYY, YYYY-MM or YYYY-MM-DD; None if not a real date."""
    m = re.fullmatch(r"(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?", str(d))
    if not m:
        return None
    y, mo, dd = int(m[1]), m[2] and int(m[2]), m[3] and int(m[3])
    try:
        first = _date(y, mo or 1, dd or 1)
        last = _date(y, mo or 12, dd or calendar.monthrange(y, mo or 12)[1])
    except ValueError:
        return None
    return first, last


def check_ledger(data, manifest, nodes, claims, base):
    """data: parsed data/ledger.yaml of one subject. manifest: {source id: entry} (load_sources).
    nodes: {node id: node}. claims: that subject's claims. base: None when conformance was run without
    --base; {} when the file is new at the base ref; otherwise the parsed file at the base ref.
    Returns (errors, warnings), each a list of (code, where, message)."""
    err, warn = [], []
    E = lambda c, w, m: err.append((c, w, m))
    W = lambda c, w, m: warn.append((c, w, m))
    if not isinstance(data, dict):
        return [("L0", "file", "ledger.yaml must be a mapping with `entities` and `flows`")], []
    ents = [e for e in data.get("entities") or [] if isinstance(e, dict)]
    flows = [f for f in data.get("flows") or [] if isinstance(f, dict)]
    if len(ents) != len(data.get("entities") or []) or len(flows) != len(data.get("flows") or []):
        E("L0", "file", "every entity and every flow must be a mapping")
    ids, regs = set(), {}
    for e in ents:
        i = e.get("id")
        if not isinstance(i, str) or i in ids:
            E("E1", i, "entity id missing, not a string, or duplicated")
        ids.add(i)
        t = e.get("type")
        if t not in LEDGER_ENTITY_TYPES:
            if LEDGER_PERSON_TYPE.search(str(t)):
                E("E2", i, f"type {t!r} is person-type: entities that are people wait for the naming proposal")
            else:
                E("E2", i, f"type {t!r} is not in the allowed list")
        if e.get("country") not in LEDGER_ISO_COUNTRIES and e.get("country") != "multiple":
            E("E3", i, f"country {e.get('country')!r} is not an assigned ISO 3166-1 alpha-2 code or `multiple`")
        for k, v in (e.get("ids") or {}).items() if isinstance(e.get("ids"), dict) else []:
            if k not in LEDGER_REGISTRY_KEYS:
                E("E4", i, f"ids key {k!r} is not a registry identifier")
            else:
                regs.setdefault((k, str(v)), []).append(i)
        if not isinstance(e.get("rev"), int) or not e.get("history"):
            E("E5", i, "rev (integer) and history (non-empty list) are required")
        elif not isinstance(e["history"][-1], dict) or e["history"][-1].get("rev") != e["rev"]:
            E("E5", i, "the last history entry must carry the current rev")
        for field in ("note", "country_note"):
            if LEDGER_ABSENCE.search(str(e.get(field) or "")):
                W("F13", i, f"entity {field} reads like an absence statement (LG10)")
    for (k, v), who in regs.items():
        if len(who) > 1:
            E("E7", ",".join(map(str, who)), f"{k} {v} is on more than one entity in this file")

    fids = set()
    for f in flows:
        i = f.get("id")
        if not isinstance(i, str) or i in fids:
            E("F1", i, "flow id missing, not a string, or duplicated")
        fids.add(i)
        for end in ("from", "to"):
            if f.get(end) not in ids:
                E("F3", i, f"{end} {f.get(end)!r} does not resolve to an entity in this file")
        if f.get("from") == f.get("to"):
            E("F3", i, "from and to are the same entity")
        s, st = f.get("source"), f.get("status")
        if s in manifest:
            urls = [str(manifest[s].get("url") or "")]
        elif s in nodes:
            urls = [str(x.get("url") or "") for x in nodes[s].get("sources") or [] if isinstance(x, dict)]
        else:
            urls = None
            E("F4", i, f"source {s!r} is in neither this subject's manifest nor the shared nodes")
        if urls and any("wikipedia.org" in urlparse(u).netloc for u in urls):
            E("F4", i, "Wikipedia is never a source")
        if st in LEDGER_LEGAL_STATUSES:
            E("F5", i, f"status {st!r} is a legal record, not a transfer: record it in the claims or timeline")
        elif st not in LEDGER_STATUSES:
            E("F5", i, f"status {st!r} is not in the allowed list")
        if st in LEDGER_IN_TOTALS and urls is not None and not ledger_read_in_full(s, manifest, nodes):
            E("F6", i, f"status {st} needs a source read in full; {s!r} has read class "
                       f"{ledger_read_class(manifest[s].get('read')) if s in manifest else 'node without access: read'!r}")
        if st == "paid":
            mine = ledger_origins(s, manifest, nodes)
            ok = [c for c in f.get("corroboration") or []
                  if c != s and (c in manifest or c in nodes) and ledger_read_in_full(c, manifest, nodes)
                  and not (ledger_origins(c, manifest, nodes) & mine)]
            if not ok:
                E("F7", i, "status paid needs a corroboration source, read in full, with an origin different from `source`")
        if st == "inferred" and not f.get("note"):
            E("F8", i, "status inferred needs a note stating the inference")
        d, en = f.get("date"), f.get("end")
        if d is None:
            if not f.get("date_note"):
                E("F9", i, "date is null and date_note is missing")
        elif ledger_span(d) is None:
            E("F9", i, f"date {d!r} is not a real YYYY, YYYY-MM or YYYY-MM-DD date")
        if en is not None:
            if ledger_span(en) is None:
                E("F9", i, f"end {en!r} is not a real YYYY, YYYY-MM or YYYY-MM-DD date")
            elif d is not None and ledger_span(d) and ledger_span(en)[1] < ledger_span(d)[0]:
                E("F9", i, "end is before date")
            if not f.get("note"):
                W("F9", i, "a flow with an end date needs a note saying what the amount covers")
        a = f.get("amount")
        if a is not None:
            if isinstance(a, bool) or not isinstance(a, (int, float)) or not (0 < a < math.inf):
                E("F10", i, f"amount {a!r} must be a number greater than zero, or null")
            elif not re.fullmatch(r"[A-Z]{3}", str(f.get("currency", ""))):
                E("F10", i, "amount is set but currency is not a 3-letter code")
        elif not f.get("note"):
            W("F10", i, "amount is null: a note should say what the source gives instead")
        k = str(f.get("kind", ""))
        if not re.fullmatch(r"[a-z][a-z0-9_]*", k):
            E("F11", i, "kind must be a snake_case label")
        elif LEDGER_ABSENT_KIND.search(k):
            E("F13", i, f"kind {k!r} states an absence; a flow records a transfer a source shows (LG10)")
        if not isinstance(f.get("rev"), int) or not f.get("history"):
            E("F12", i, "rev (integer) and history (non-empty list) are required")
        elif not isinstance(f["history"][-1], dict) or f["history"][-1].get("rev") != f["rev"]:
            E("F12", i, "the last history entry must carry the current rev")
        for key in ("absent", "no_payment", "none_found"):
            if key in f:
                E("F13", i, f"key {key!r}: absence is not a flow (LG10)")
        for field in ("note", "date_note", "period_label"):
            if LEDGER_ABSENCE.search(str(f.get(field) or "")):
                W("F13", i, f"{field} reads like an absence statement; absence belongs in a claim with absence_anchor: true (LG10)")

    if base is None:
        if ents or flows:
            W("G0", "file", "run without --base: the append-only checks (G1, LG9) were skipped")
    else:
        for kind, cur_list in (("entities", ents), ("flows", flows)):
            cur = {x.get("id"): x for x in cur_list}
            for x in (base.get(kind) or []) if isinstance(base, dict) else []:
                if not isinstance(x, dict):
                    continue
                n = cur.get(x.get("id"))
                if n is None:
                    E("G1", x.get("id"), f"{kind[:-1]} was removed (LG9: append, never erase)")
                elif n != x:
                    if not isinstance(n.get("rev"), int) or n["rev"] <= (x.get("rev") or 0):
                        E("G1", x.get("id"), "changed without a higher rev")
                    old_h = x.get("history") or []
                    if (n.get("history") or [])[:len(old_h)] != old_h:
                        E("G1", x.get("id"), "earlier history entries were edited")

    for c in claims:
        a = c.get("anchor") if isinstance(c, dict) else None
        if not isinstance(a, dict):
            continue                              # a non-mapping anchor is reported by N25 (check_anchor_format)
        where = f"claim {c.get('id')}"
        if "flows" in a:
            E("C1", where, "anchor.flows is not a key; cite the flow's own source (LG7)")
        texts = [str(a.get("description", ""))]
        for key in ("sources", "nodes"):
            for x in a.get(key) if isinstance(a.get(key), list) else []:
                texts.append(str(x.get("node") if isinstance(x, dict) else x))
        blob = " ".join(texts)
        for fid in fids:
            if isinstance(fid, str) and re.search(r"(?<![\w-])" + re.escape(fid) + r"(?![\w-])", blob):
                E("C1", where, f"cites flow id {fid} in its anchor (LG7)")
    return err, warn


def check_ledgers(r, subjects, base):
    """Wiring: run check_ledger for every subject that has data/ledger.yaml; report through r."""
    nodes = {}
    for p in glob.glob(os.path.join(ROOT, "build", "nodes", "*.yaml")):
        n = load(p)
        if isinstance(n, dict) and isinstance(n.get("id"), str):
            nodes[n["id"]] = n
    for sdir in subjects:
        rel = os.path.relpath(os.path.join(sdir, "data", "ledger.yaml"), ROOT)
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        try:
            data = load(os.path.join(ROOT, rel))
            old = None
            if base:
                txt = git_show(base, rel)
                old = (yaml.safe_load(txt) or {}) if txt is not None else {}
            cp = os.path.join(sdir, "claims.yaml")
            cd = load(cp) if os.path.exists(cp) else None
            claims = (cd.get("claims") if isinstance(cd, dict) else None) or []
        except (yaml.YAMLError, ValueError) as e:     # ValueError: an unquoted impossible date such as 2025-13-45
            r.err(rel, f"YAML does not parse: {e}")
            continue
        errs, warns = check_ledger(data, load_sources(sdir), nodes, claims, old)
        for code, where, msg in errs:
            r.err(rel, f"[{code}] {where}: {msg}")
        for code, where, msg in warns:
            r.warn(rel, f"[{code}] {where}: {msg}")


# In main(), after `nodes = check_nodes(r)` and before the `if args.base:` line, add:
#     check_ledgers(r, subjects, args.base)
```

## 4. What it does not change
- No existing claim, finding, weight or state changes. No claim in any subject cites a flow (LG7). N25 (anchor format) and P5
  are unchanged; the publish gate is unchanged.
- No manifest is changed by this proposal (3.4). No page, export or total is rendered from a ledger by this proposal.
- The shared register, the shared Ledger view, the timing rule for every subject (LG8) and the view's drawing limits (LG12) are not
  in this proposal (section 8).
- The pilot's source statements are not re-judged. Migrating the pilot changes labels in its data file and removes legal records
  from the flow list; it changes no claim, and is logged in the pilot's `log.yaml` as a new entry.

## 5. Impact
Counts: `origin/main` 2d69ee2 has 21 subjects; the pilot is a 22nd on `dig/ip-money`. Ledger data exists for 1 of the 22.

| Subject | Before | After |
|---|---|---|
| israel-palestine-money (`dig/ip-money`; not on `main`, not listed under `publish`, no `review.yaml`) | `conformance.py`: 0 errors, 126 warnings in the scratch tree of main plus the pilot folder (22 subjects; main alone has 113); the broken flow of 2.1 changes nothing | raw file: 561 errors, 140 warnings (2.4; 514 of the errors come from the file having no `id`, `rev` or `history` yet). After the mechanical migration below: 8 errors and 14 warnings, listed in 2.4; each needs the author's decision, so the final result is not known until they are made and the check re-run |
| the other 21 subjects on `main` | 0 errors, 113 warnings | 0 errors, 113 warnings: run, patched and unpatched (2.5); none has a ledger file. On two of them (`incandescent-lamp`, `fluoride-iq`) the check was also run on synthetic fixtures to exercise it (2.5) |

**Migration of the pilot** (by the dig's author, on its own branch, in its own PR; the owner decides the rules first):
1. Add to each entity `rev: 1` and a `history` entry; to each flow an `id` (`ipm-001` to `ipm-189` in file order), `rev: 1` and
   a `history` entry. Both `history` entries say the file was migrated.
2. Types: `government_holding` to `quasi_government`; `government_committee` to `government_agency`; `hospital` to
   `organization`; `activity` (a disclosure category, not a party) to `aggregate`. `individual_public` (2): waits for the naming
   proposal (3.3). `political_target` (3): not an entity type; the three flows are re-pointed to one `aggregate` of recipients named
   "Recipients of independent expenditures (per filing)"; the name of the opposed candidate stays in the cited filing.
3. Country: `IL/WB` (8) and `EU` (1) are not assigned ISO codes; they become `multiple` and the original text goes in
   `country_note`. This loses information in the `country` field: `multiple` says only that the party is not one assigned
   country; it does not say which, and for `IL/WB`, which spans two assigned codes, it takes no position between them or on any
   territory's status. `country_note` keeps the source's wording so nothing is lost from the file.
4. `ids.status` strings (6) move to the entity `note`; `ids` keeps registry keys only.
5. Dates: `2012-2025` becomes `date: "2012"`, `end: "2025"`; `FY2024` becomes `date: "2024"` with `period_label: FY2024`;
   `all years` becomes `date: null` with `date_note`; `through FY2020` becomes `date: null`, `end: "2020"`, `period_label`, `date_note`.
6. Author decisions: the 4 flows with legal-record statuses move to claims or the timeline; the 2 `filed` flows with a source not
   read in full are re-read (and the manifest entry re-labelled) or relabelled to a status not in totals; the 2 person-type
   entities and their 3 flows wait or are removed; notes are added to the 13 flows with `end` and no note; the flow note that says a
   payment was not found moves to a claim.
Steps 1 to 5 were run in memory for the dry run in 2.4; step 6 is why it shows 8 errors.

## 6. Alternatives considered
1. **Do nothing.** Rejected: 2.1 shows an invented flow passes, and the pilot's 15 statuses and 21 types are unconstrained.
2. **A per-dig validated file (chosen).** Keeps the dig's data inside the dig, so its review and the publish gate cover it by
   location. Costs: an organization appears once per dig, and a total across digs is impossible. Both are the deferred items of
   section 8.
3. **A shared register under `build/ledger/` (the earlier draft).** Rejected for now: its main benefit (one entity across digs) is
   a forecast, only one dig has data, and it needs the cross-dig neutrality run that point 7 requires.
4. **Make flows a node type in the Atlas.** A node is a dated artifact with a place; a flow is a relation between two parties with
   an amount and a status. A worse fit; a flow's `source` may be a node.
5. **Totals only (per payer per year).** Loses the record-level source link. Rejected.
6. **A closed list for `kind`.** Rejected: 41 labels are in use and no rule reads `kind` except to refuse an absence wording.
7. **Define "read" by adding a new field to the manifest.** Rejected for now: it would change every manifest. The keyword
   parse needs no manifest change; dropping it for a field is possible later.

## 7. Neutrality check
**The narrowed proposal makes no claim that needs a run across two digs.** It does not claim to treat two digs alike; it has
not been run on two digs, because only one dig has ledger data (every branch of `origin` was searched for ledger or flow data
files). Point 7 of `docs/SCHEMA_PROPOSALS.md` asks for that run. This proposal does not meet it; it cuts its scope to the rules
for which the owner or the assessor may accept inspection instead, and defers the rest (section 8). Whether that satisfies point 7 is
the owner's decision.

Properties that can be checked by reading section 3 and no run (inspection-only):
- No check reads a payer's or payee's name, country, direction of payment or amount to decide an outcome. The checks read
  format, resolvability, `status`, entity `type`, the manifest `read` class and origin, dates, and an absence wording.
- `country` is checked only for being an assigned code; the proposal makes no statement about any territory.
- Rules that apply to every entity and flow the same way: LG1, LG2, LG4, LG7, LG9, LG10.
- Rules whose effect depends on how the data is labelled and so could fall unevenly across digs: LG3 (what is `filed`), LG1
  and F6 (the `read` wording each dig used: 77 entries use `yes, directly` and are in no class), F7 (host as proxy for
  originator) and F13 (the absence phrase list). These are the rules a two-dig run would examine first (section 8).
The fixture runs in 2.5 test mechanics on two other subjects. They are not a neutrality test: the fixtures are invented.

## 8. Deferred until a second dig has ledger data
Nothing below is proposed here. Each item says what it needs before it can be proposed.

| Deferred item | What it needs first |
|---|---|
| **LG5, shared entity ids and merges** (a register under `build/ledger/`, merging on a shared registry identifier, who approves a merge, who owns the folder) | A second dig with ledger data in which the same organization appears; the two-dig run below; a decision on whether `build/ledger/` is owner-only (it is not on the list in `docs/REVIEW.md`); an enforcement path for owner approval that is not a field the author writes; and how `review_dig.py` and the publish gate cover a folder outside `build/subjects/`. |
| **The shared Ledger view** (points, lines, time slider, filters) | The item above; a site-build filter that shows only flows of published subjects, with a build test (a fixture flow of an unpublished subject is absent from every output); a build test that a fixture with one `filed` and one `pledged` flow totals only the `filed` one. Neither test exists. |
| **LG12, what the view may not draw** (no line, arrow, shading, ordering or caption implying influence or cause between a payer and a later or earlier event; no pairing by date proximity; no total across statuses or currencies; the only line is a flow's own `from` to `to`, labelled with its status and linked to its source) | The view. The rule has no object until a view exists. |
| **LG8, timing is context in every subject** (extends P5 from politics digs to every subject, a scope change) | A page that shows flows beside dated events. This proposal shows none. |
| **LG6, naming** | Its own proposal (3.3). |

**The two-dig neutrality run (point 7), for the shared register and the view.** What will be run: the checks of 3.5 on two digs'
ledger files, unchanged between the two runs, then a table per dig of errors and warnings per check code per 100 flows; the share of
flows in totals (`paid`, `filed`); flows refused by F6 and F7 and the `read` wording behind them; entities refused by E2. For any
check whose rate differs materially, the cases are opened and the cause is recorded as the rule's wording or the dig's sources;
a cause in the wording sends the rule back as a revised proposal. On which two digs: the pilot (`israel-palestine-money`) and a
second dig with ledger data whose question points the other way; the owner names the second dig, before its ledger data is read.
The commit of the rules and of `check_ledger` is recorded in the proposal's PR before the second dig's data is read, and neither
is changed to fit it. The result is recorded on the PR that proposes the deferred item. It tests whether the checks fall unevenly
on two digs; it does not test whether either dig's selection of flows met a common standard, which is the dig's review
(`docs/REVIEW.md` D) and has not been done for the pilot's ledger.
