# Proposal: the Ledger, a shared register of organizations and money transfers (rules LG1 to LG12)

Status: PROPOSAL under `docs/SCHEMA_PROPOSALS.md`, on branch `process/ledger` (draft PR #24). Not in force until
an independent reviewer has checked the seven points and the owner has decided. Agents do not merge it.
Requested by the owner on 2026-10-07 ("Yes to ledger"), after the `israel-palestine-money` pilot.
Revised on 2026-10-14 after the independent assessment on PR #24 (blocking findings B1 to B6, non-blocking N2 to N8).

What was run, and on what: the pilot data is `build/subjects/israel-palestine-money/data/ledger.yaml` at the tip of
`origin/dig/ip-money` (commit fcd7cbe), used as a test input only and not modified. `origin/main` is 25de0d2 (20 subjects).
The validator check in section 3.6 is not in `build/conformance.py`; the dry runs in section 2 and section 5 execute the
code block of section 3.6 exactly as printed here (extracted from this file), outside the repository.

Two things this document does not do. It does not satisfy point 7 of `docs/SCHEMA_PROPOSALS.md` (section 7 says why and
what is deferred). It contains one clause, LG6 (naming), that is a rule change needing the owner's approval; section 3.5
says so, and LG6 is not written into any rule file.

### What changed since the first draft
| Finding | Where it is handled |
|---|---|
| B1 stale counts, no dry run | section 2 (real counts, real output), section 5 |
| B2 validator not exact; statuses, types, dates | sections 3.2 to 3.4, 3.6 (table and code) |
| B3 absence | LG10, check F13 |
| B4 naming | LG6 and the notice in section 3.5 |
| B5 publish-gate bypass | LG11, section 6 (alternative 5) |
| B6 neutrality | section 7 (not run; deferred, with the test stated) |
| N2 LG7 and `anchor.flows` | LG7, check C1 (the key is dropped; N25 is unchanged) |
| N3 `ids` | E4, section 3.4 |
| N4 ownership of `build/ledger/` | section 3.7 |
| N5 LG8 scope | LG8 |
| N6 what the view may draw | LG12 |
| N7 `filed` versus `paid` | section 3.4, LG3, F7 |
| N8 subject count | section 5 |

The file layout also changed: flows are one file per filing subject (a list), not one file per transfer, so a dig's
189 flows are one reviewable file. Entities stay one file each.

## 1. The failure case

A record of who paid whom, how much, when, and on what document, has no place in the schema and no check in the
validator.

The real case is `build/subjects/israel-palestine-money` on `dig/ip-money`. Its money is recorded in
`data/ledger.yaml`: 136 entities and 189 flows, each flow with a `source` that is a manifest id (for example
`src-fara-7649-clocktowerx`). Three things go wrong today:

1. **Nothing checks it.** `data/` is not read by `conformance.py`. A flow with an unknown payer, a source that is not in
   the manifest, a non-date and a non-number passes exactly like a correct one (section 2).
2. **Nothing separates a filed figure from a pledge, an estimate or a vacated verdict.** The pilot uses 15 distinct
   `status` values and 21 distinct entity `type` values in a free-text field; nothing says which may be added together
   or shown beside a payment (section 3.4).
3. **Money is squeezed into claims.** In the pilot, payment chains also live in claim prose
   (`ipm-israel-us-media-fara`, field `payments_onward` at `claims.yaml:814`, an unvalidated extra key). A reader cannot ask
   "every flow into entity X" without reading every claim.

A forecast, not an observation: other digs would each write their own copy of the same organization, and the copies
would drift. Only one dig has ledger data today (section 7), so this part of the case is not demonstrated.

## 2. Evidence

### 2.1 The current validator does not see the ledger
`python3 build/conformance.py --base origin/main`, run in a checkout of `origin/dig/ip-money`, as filed, then with one
deliberately broken flow appended to `data/ledger.yaml` (`from: nobody`, `amount: lots`, `date: someday`,
`source: src-does-not-exist`), then the file restored:

```
as filed:               21 subjects and 115 shared nodes checked: 1 errors, 125 warnings
broken flow appended:   21 subjects and 115 shared nodes checked: 1 errors, 125 warnings
```
The one error in both runs is `anne-frank-diary/log.yaml: log entry L-14 was removed (rule 6)`: the `dig/ip-money`
branch was cut before `main` received that entry. It is not caused by the ledger. The two outputs are identical, so the
validator cannot tell a sourced flow from an invented one. On this branch (`process/ledger`, `main` merged in) the same
command gives `20 subjects and 115 shared nodes checked: 0 errors, 111 warnings`.

### 2.2 What the pilot data contains (counted from the file)
- 136 entities, 189 flows; 174 manifest ids, all 189 flow sources resolve; 0 flow sources are Wikipedia.
- Flow fields present: `from`, `to`, `amount`, `currency`, `date`, `kind`, `status`, `source` on all 189; `note` on 130; `end` on 22.
  No flow has `id`, `rev`, `subject` or `history`; no entity has `rev` or `history`.
- 15 distinct `status` values: `filed` 159, `pledged` 8, `notified` 7, `contracted` 2, `estimate` 2, `sources_differ` 2,
  and one each of `reported_disputed`, `convicted`, `inferred`, `guarantee`, `verdict_vacated`, `judgment`, `designation`,
  `reported`, `partial`. `paid` is used by 0 flows.
- 21 distinct entity `type` values: `charity` 34, `company` 21, `foundation` 17, `organization` 15, `government` 10,
  `government_agency` 10, `aggregate` 8, `political_committee` 3, `political_target` 3, `armed_group` 2,
  `donor_advised_fund` 2, `individual_public` 2, and one each of `quasi_government`, `designated_network`, `un_agency`,
  `government_holding`, `government_fund`, `bank`, `government_committee`, `hospital`, `activity`.
- `date` forms: `YYYY` 123, `YYYY-MM-DD` 47, `YYYY-YYYY` 12, `FY2024`-style 3, `YYYY-MM` 2, `through FY2020` 1, `all years` 1.
  17 flows are not ISO dates.
- 4 flows have `amount: null`; every non-null amount has a currency (`USD` 182, `CAD` 3, `ILS` 3, `EUR` 1).
- `country`: 12 values are ISO codes or `multiple`; `IL/WB` (8 entities) and `EU` (1) are not.
- `ids` keys: `ein` 40, `fara_registration` 8, `cra_bn` 4, `budget_code` 2, `uk_charity` 1, and `status` 6 (free text such as
  a revocation date, which is not a registry identifier; two entities share the same `status` string).
- Flow sources by `read` value in the manifest: 9 of 189 flows rest on a source marked `tool` (read through a summarizing
  fetch tool); the other 180 are marked `full`. Of the 9, one has `status: filed`.
- The manifest is the pilot's own; no flow was compared with its source document for this proposal.

### 2.3 The proposed check run on the current pilot data
`check_ledger` is the code in section 3.6, extracted from this file and run by a script outside the repository. Two runs:
**raw** is the file exactly as it is; **migrated** applies, in memory, the mechanical mapping of section 5 (flow ids,
`rev`, `history`, `subject`, type and country mapping, date split) and nothing else. The migrated run is a dry run of the
migration, not a pass of the final data: nothing was written to the repository.

```
mode=raw: 136 entities, 189 flows -> 932 errors, 14 warnings
  error E2: 9   e.g. ('pa-off-budget', "entity type 'government_holding' not in the allowed list")
  error E3: 8   e.g. ('elad', "country 'IL/WB' is not an ISO alpha-2 code or 'multiple'")
  error E4: 6   e.g. ('hlf', "ids key 'status' is not a registry identifier")
  error E5: 136   e.g. ('gov-il', 'rev (integer) and history (non-empty) are required')
  error F1: 189   e.g. (None, 'flow id missing or duplicated')
  error F12: 189   e.g. (None, 'rev (integer) and history (non-empty) are required')
  error F2: 189   e.g. (None, 'subject None is not a subject with a sources manifest')
  error F4: 189   e.g. (None, "source 'src-fara-7649-clocktowerx' is not in the manifest of None or a shared node")
  error F9: 17   e.g. (None, "date '2012-2025' is not YYYY, YYYY-MM or YYYY-MM-DD")
  warning F13: 1   e.g. (None, 'note reads like an absence statement; absence belongs in a claim with absence_anchor: true')
  warning F9w: 13   e.g. (None, 'a flow with an end date needs a note saying what the amount covers')
```
```
mode=migrated: 134 entities, 189 flows -> 5 errors, 14 warnings
  error E6: 4   e.g. ('dell-michael-susan', 'person_public needs naming.category and naming.standard from the lists')
  error F6: 1   e.g. ('israel-palestine-money-018', "status filed needs a source read in full; manifest says read: 'tool'")
  warning F13: 1   e.g. ('israel-palestine-money-141', 'note reads like an absence statement; absence belongs in a claim with absence_anchor: true')
  warning F9w: 13   e.g. ('israel-palestine-money-002', 'a flow with an end date needs a note saying what the amount covers')
```
In the raw run, E5, F1, F12, F2 and F4 fire on every record only because the file has none of the new fields (`id`,
`rev`, `history`, `subject`); E2, E3, E4 and F9 are the real mismatches (9 entities with off-list types, 8 with `IL/WB`
country, 6 with `ids.status`, 17 non-ISO dates). No raw record fails F5 (statuses), F3 (ends) or F10 (amounts).
The driver script is not committed; it only loads the YAML, applies the mapping and calls `check_ledger`.

The five residual errors in the migrated run are not mechanical: four are the two `person_public` entities lacking a
`naming` block and a `role.title` (LG6), one is a `filed` flow whose source is marked `tool` (F6). They need a decision by
the dig's author: supply the naming sources, re-read the source in full, or change the label to `reported`. The 14
warnings are 13 flows with an `end` date and no note about what the amount covers, and 1 flow whose note contains an
absence phrase (F13).

## 3. The proposed change, exactly

### 3.1 Files
```
build/ledger/entities/<entity-id>.yaml    one file per organization, agency, committee, fund or named person
build/ledger/flows/<subject>.yaml         one file per filing subject: `flows:` is a list of flows
```
Entities are shared like `build/nodes/`: any dig may cite one; the file exists once. A flow file belongs to the subject
named by its file name, and every flow in it has `subject:` equal to that name.

### 3.2 Entity fields
Required: `id` (permanent, equals the file name), `rev` (integer, starts at 1), `name`, `type` (section 3.4), `country`
(ISO 3166-1 alpha-2 code, or `multiple`), `history` (list; each entry has `rev`, `date`, `by`, `change`).
Optional: `ids` (registry identifiers only, keys listed in 3.4), `aliases`, `note`.
Required when `type: person_public`: `naming` (LG6) and `role` (`title`, and `organization` for an officer).

### 3.3 Flow fields
Required: `id` (unique in the repository), `rev`, `subject`, `from` and `to` (entity ids), `amount` (a non-negative number, or
`null` when the source gives none), `currency` (3-letter code, required when `amount` is set), `kind`, `status`, `source`,
`history`, and a date as follows.

- **Dates.** `date` is `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, exactly as precise as the source. A range is `date` (start) plus
  `end` (inclusive, same three forms, not before `date`). A fiscal year is written as the year or dates the source states
  for it, with the source's own label kept in `period_label` (for example `FY2024`); the ledger does not compute fiscal
  calendars. When the source gives no start (for example "all years", "through FY2020"), `date` is `null` and `date_note`
  quotes the source's wording. Any flow with `end` needs a `note` saying what the amount covers (a total over the period,
  a per-year figure, the top of a range).
- **`kind`** is a display label in `snake_case`, not an enumerated list and never used in totals or any other logic. The
  pilot uses 41 labels. Totals depend on `status` only.
- **`source`** is a manifest id of the flow's `subject`, or a shared node id (LG1). For `paid`, `corroboration` lists at
  least one further manifest id.
- Optional: `note`, `period_label`, `date_note`, `corroboration`.

### 3.4 Closed lists (a new value needs a SCHEMA change under `docs/SCHEMA_PROPOSALS.md`)

**Statuses.** Every status the pilot uses is named. "Totals" says whether the site may add the flow into a total; a total is
shown for one status and one currency at a time, with the status and currency printed beside it (LG3).

| `status` | Meaning | Pilot flows | Totals |
|---|---|---|---|
| `paid` | A payment record shows the money moved: a record from the payer or payee plus a second record from a different originator (`corroboration`), or both parties' filings agreeing | 0 | yes, as `paid` only |
| `filed` | A document filed by a party records the transfer. It is that party's own report to an official body, not a verified payment | 159 | yes, as `filed` only |
| `partial` | A filed record whose amount is incomplete (for example only legible fields) | 1 | no |
| `pledged` | Announced or promised, not shown as paid | 8 | no |
| `contracted` | A contract or agreement to pay exists | 2 | no |
| `guarantee` | A loan or payment guarantee, not a transfer | 1 | no |
| `estimate` | A party's or an analyst's estimate or ceiling | 2 | no |
| `notified` | A government notification of a proposed transfer, with a maximum case value | 7 | no |
| `designation` | An official designation or blocking action; amount is usually `null` | 1 | no |
| `reported` | A report of the transfer by a third party, not read in a filing | 1 | no |
| `reported_disputed` | A report whose figure or fact is disputed by a source | 1 | no |
| `sources_differ` | Sources give different figures; each is recorded | 2 | no |
| `inferred` | Inferred by the entry's author, not read in a document; `note` must state the inference | 1 | no |
| `convicted` | A criminal finding of a court or jury | 1 | no |
| `judgment` | A civil judgment | 1 | no |
| `verdict_vacated` | A finding that was set aside | 1 | no |

The pilot's `partial`, `notified`, `designation` and `reported` are kept and added to the list (the first draft omitted
them); no pilot status is renamed. The decision to exclude every status except `paid` and `filed` from totals is the
owner's to confirm.

`filed` versus `paid`: `filed` says what a party reported. It is never labelled "paid" anywhere on the site; the page
shows "reported by <filer> in <document>". A flow may be `paid` only with `corroboration` (check F7). The pilot has no
`paid` flow.

**Entity types.** Allowed: `government`, `government_agency`, `government_fund`, `quasi_government`, `company`, `bank`,
`charity`, `foundation`, `donor_advised_fund`, `political_committee`, `un_agency`, `armed_group`, `designated_network`,
`organization`, `aggregate` (a group, or a category the source gives only as a total), `person_public` (LG6 only).
The 21 pilot types are decided as follows.

| Pilot type (entities) | Decision |
|---|---|
| the 15 pilot types that are already on the allowed list (all except the six below) | allowed, unchanged |
| `government_holding` (1) | mapped to `quasi_government` |
| `government_committee` (1) | mapped to `government_agency` |
| `hospital` (1) | mapped to `organization` |
| `activity` (1: a disclosure category, not a party) | mapped to `aggregate` |
| `individual_public` (2) | renamed `person_public`; needs `naming` and `role` under LG6 |
| `political_target` (3: "independent expenditures against <named candidate>") | excluded as an entity type. The payee of a filed expenditure is its recipient, not the person it opposes; a "target" entity records an intended effect, which LG7 and LG12 do not allow. The three flows are re-pointed to one `aggregate` of recipients, and the candidate named in the filing is kept in the flow's `note` with its source |

**Registry identifier keys** (`ids`): `ein`, `cra_bn`, `uk_charity`, `fara_registration`, `company_number`, `budget_code`,
`fec_id`. Nothing else goes in `ids`; the pilot's six `ids.status` strings (for example a revocation date) move to `note`.

**Countries.** ISO 3166-1 alpha-2, or `multiple`. The pilot's `IL/WB` (8) and `EU` (1) are mapped to `multiple`.

### 3.5 Rules (text for `build/SCHEMA.md`, new section "Ledger")

- **LG1 Every flow has a source that was read.** `source` resolves to a manifest id of the flow's `subject`, or to a shared
  node. Wikipedia is never a source (CLAUDE.md), here as everywhere. A flow with status `paid` or `filed` needs a source
  whose manifest `read` is `full`; a source read only through a summarizing tool (`tool`), seen as a snippet, blocked or
  known only as quoted supports at most a status that is not in totals (for example `reported`).
- **LG2 Both ends exist.** `from` and `to` resolve to entity files; they differ.
- **LG3 Status is stated, from the closed list in 3.4.** Only `paid` and `filed` enter a total, each on its own: a total
  is shown for one status and one currency, labelled with both, and the site also shows how many flows were left out for
  lack of an amount. A `filed` flow is a party's own report and is never described as paid. No other status is added to
  any total or shown as a payment.
- **LG4 Amounts and dates stay as the source gives them**: number, currency, and date at the source's precision (3.3).
  Any conversion, inflation adjustment or fiscal-year calendar is a separate, labelled calculation of class `synthetic`,
  never written into `amount` or `date`.
- **LG5 Entities.** Two entities merge only on a shared registry identifier in `ids`, or by a `history` entry with
  `approved_by: owner`; never on name alone. Two entities with the same name and different identifiers stay separate.
  `ids` holds registry identifiers only (3.4). A change to an existing entity's `name`, `type` or `ids` also needs a
  `history` entry with `approved_by: owner` (3.7).
- **LG6 Who may be named.** See the notice below. Drafted for the owner's decision; not in force.
- **LG7 A flow is a record, not a finding.** A flow carries no evidential weight. A claim that depends on a transfer cites
  the flow's own `source` in its `anchor.sources` and says in `anchor.description` what was read there; the claim's weight
  follows that source and what was read, as for any other claim. A claim may not cite a flow id in its anchor, and
  `anchor.flows` is not a key (N25 is unchanged and already allows no other keys to carry weight). Same firewall as
  threads (TH2) and transmission chains (X3).
- **LG8 Timing is context, in every subject.** P5 (`SCHEMA.md:156`) says a dated filing beside a vote shows timing only;
  it sits among the politics-only rules. LG8 extends that wording from politics digs to every subject: wherever a flow is
  shown beside any dated event (a vote, decision, designation, statement, publication), the page says it shows timing
  only, and that timing does not show cause, unless a source documents the link. This is a scope change to P5's wording and
  is part of what the owner would approve.
- **LG9 Append-only.** A correction is a new `rev` with a new `history` entry; nothing is deleted, and earlier `history`
  entries are never edited. Ids are never reused.
- **LG10 Absence is not a flow and is not evidence.** The absence of a flow in the ledger is never evidence that no payment
  occurred; the ledger holds only what a source shows and says nothing about what was not searched. A flow records a transfer
  that a source shows. There is no status, kind or key for "no payment found". A claim that rests on "no flow found"
  lives in the subject's `claims.yaml`, with `anchor.type: search-record` listing what was searched and where, with
  `absence_anchor: true`, and is capped at provisional (the existing rule, `conformance.py:453`). A flow whose note says a
  payment was not found is a warning (F13): the sentence moves to a claim. Pages that list flows state which sources were
  searched, so a reader sees coverage, not completeness.
- **LG11 Publication.** A flow appears on any public page, export or total only if its `subject` is listed under `publish`
  in `build/site.yaml` and has a `review.yaml` with status `passed` or `passed_with_open_items` (`docs/PUBLISH_GATE.md`).
  An entity appears only through such flows. The ledger has no review of its own (section 6, alternative 5, gives the
  reason). Taking a subject off the list removes its flows from every public page.
- **LG12 What the Ledger view may not draw.** No line, arrow, highlight, shading, ordering or caption that implies influence
  or cause between a payer and a later (or earlier) event; no automatic pairing of a flow with a vote, decision or
  statement by date proximity; no ranking labelled as influence or weight; no total across statuses or currencies; no
  entity typed by an intended effect. The only line drawn from a flow connects its own `from` and `to`, labelled with its
  status and linked to its source. A time slider changes which dated flows are shown and does nothing else.

#### Notice on LG6: a rule change that needs the owner's approval
The owner stated on 2026-10-14, in chat, that the private-individual name rule does not apply to political figures, public
profiles, or publicly known executives and board members of organizations acting in that role. That statement is not in any
rule file, and under `CLAUDE.md` and `docs/SCHEMA_PROPOSALS.md` a chat statement alone does not change a rule, even
the owner's; the change needs a proposal that meets the standards, an independent assessment, and then the owner's decision.
LG6 below is the drafted wording of that intent for the Ledger only. It is not written into `build/SCHEMA.md`,
`CONTRIBUTING.md` or any other rule file by this proposal. Existing related text, for the reviewer's comparison:
`docs/NEWS_REVIEW.md:10` (names only where authorities and several independent outlets name them), `docs/AGENT_RULES.md:90`,
`build/SCHEMA.md` N26 (redaction of a private person's name), `docs/proposals/topic-admission.md` TA4 (draft), and the
subject-level ruling `anne-frank-diary/log.yaml` L-14. A general naming rule for all subjects would be a separate proposal.

**LG6 (draft).** A natural person is an entity (`type: person_public`) only in one of three categories, stated in
`naming.category`:
1. `political_figure`: a holder of, or candidate for, public office or a party or government post;
2. `public_profile`: a person with a public profile, named in the cited sources in connection with the flow;
3. `organization_officer`: a publicly known executive or board member of an organization, named in that role
   (`role.organization` resolves to an entity). The flow must be one the source attributes to the person in that role.

Entity types the pilot already uses are covered: `individual_public` becomes `person_public` (category 2 or 3 as the
sources show); `political_target` is not an entity type (3.4), though a political figure named in a filing may appear in
a flow's note; `political_committee`, `donor_advised_fund`, `company` and the other organization types are not persons.
Any other natural person is a private individual: not an entity, not in `aliases`, not in `note`. The flow is then recorded
against the organization, fund or `aggregate` the source gives, or not recorded. A donor-advised fund is the payer; its
underlying donors are not inferred. A minor is never named.

**Source standard for naming.** `naming.standard` is one of: `filing` (a public filing in which the person is named in
that capacity), `official_record` (a court record, register, legislative or government record), or `independent_outlets`
(at least three outlets with different publishers, none citing another as its origin). `naming.sources` lists manifest ids,
at least 1 for `filing` and `official_record`, at least 3 distinct for `independent_outlets`, each read in full. The
validator checks the count and the categories; whether the outlets are independent and whether the person fits the
category is the reviewer's judgment. The threshold of three, and `read: full` for each, are choices for the owner.

### 3.6 Validator: `check_ledger` in `build/conformance.py`
Runs only on `build/ledger/`; with no such directory it returns nothing. Called once per run with every entity, every
flow, each subject's manifest, the shared node ids, every claim, and (when `--base` is given) the entities and flows read
from that git ref. Each row is one check: the condition that fails it, its level, and the rule it enforces.

| Check | Fails when | Level | Rule |
|---|---|---|---|
| E1 | entity `id` missing, duplicated, or different from the file name | error | LG5 |
| E2 | entity `type` not in the allowed list (3.4) | error | LG5, 3.4 |
| E3 | `country` is not an ISO alpha-2 code or `multiple` | error | 3.2 |
| E4 | an `ids` key is not a registry key (3.4) | error | LG5 |
| E5 | `rev` is not an integer, `history` is empty, or the last `history` entry's `rev` differs from `rev` | error | LG9 |
| E6 | `person_public` without a valid `naming` (category, standard, enough distinct sources, each a `subject:id` manifest entry read in full and not Wikipedia), without `role.title`, or an `organization_officer` whose `role.organization` does not resolve | error | LG6 |
| E7 | two entities share the same registry key and value | error | LG5 |
| F1 | flow `id` missing or duplicated | error | LG9 |
| F2 | `subject` is not a subject with a sources manifest, or differs from the flow file name | error | LG1 |
| F3 | `from` or `to` does not resolve to an entity, or they are equal | error | LG2 |
| F4 | `source` is in neither the subject's manifest nor the node ids, or its URL is on wikipedia.org | error | LG1 |
| F5 | `status` not in the closed list (3.4) | error | LG3 |
| F6 | status `paid` or `filed` and the source's manifest `read` does not begin `full` | error | LG1 |
| F7 | status `paid` without a `corroboration` id, other than `source`, that is in the manifest | error | LG3 |
| F8 | status `inferred` without a `note` | error | 3.4 |
| F9 | `date` is neither ISO (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`) nor `null` with a `date_note`; `end` not ISO or before `date` | error | LG4 |
| F9w | `end` present and no `note` | warning | LG4 |
| F10 | `amount` not a non-negative number or `null`; or set with no 3-letter `currency` | error | LG4 |
| F10w | `amount` is `null` and no `note` | warning | LG4 |
| F11 | `kind` is not `snake_case` | error | 3.3 |
| F12 | `rev` not an integer, `history` empty, or last entry's `rev` differs | error | LG9 |
| F13 | a key `absent`, `no_payment` or `none_found` on a flow (error); a `note` containing an absence phrase (warning) | error / warning | LG10 |
| G1 | against `--base`: an entity or flow was removed; changed without a higher `rev`; or earlier `history` entries were edited | error | LG9 |
| G2 | against `--base`: an entity's `name`, `type` or `ids` changed and the last `history` entry lacks `approved_by: owner` | error | LG5 |
| C1 | a claim's `anchor` has a `flows` key, or contains a flow id (whole-id match) in its description, sources or nodes | error | LG7 |

Not enforced by this validator, and said so: that a source says what the flow says (reviewer, `docs/REVIEW.md` A); that
`filed` was not in fact a verified payment; whether naming outlets are independent; that `approved_by: owner` is true
(the field is checked, the approval is not; see 3.7); LG8 and LG12 (page text and drawing), LG11 and the totals rule of LG3
(site build, 3.8). The absence phrase list in F13 is a heuristic and will miss some wordings.

```python
import re
from urllib.parse import urlparse

ENTITY_TYPES = {"government", "government_agency", "government_fund", "quasi_government",
                "company", "bank", "charity", "foundation", "donor_advised_fund", "political_committee",
                "un_agency", "armed_group", "designated_network", "organization", "aggregate",
                "person_public"}
REGISTRY_KEYS = {"ein", "cra_bn", "uk_charity", "fara_registration", "company_number",
                 "budget_code", "fec_id"}
STATUSES = {"paid", "filed", "partial", "pledged", "contracted", "guarantee", "estimate", "notified",
            "designation", "reported", "reported_disputed", "sources_differ", "inferred",
            "convicted", "judgment", "verdict_vacated"}
IN_TOTALS = {"paid", "filed"}                 # each summed only with its own status (LG3)
NEEDS_FULL_READ = {"paid", "filed"}           # source must have been read in full (LG1)
NAMING_STANDARDS = {"filing": 1, "official_record": 1, "independent_outlets": 3}
NAMING_CATEGORIES = {"political_figure", "public_profile", "organization_officer"}
DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
COUNTRY = re.compile(r"^([A-Z]{2}|multiple)$")
ABSENCE_WORDS = re.compile(r"not found|no record|none found|no payment|no flow|absent|not located", re.I)


def read_full(entry):
    return str((entry or {}).get("read", "")).split(" ")[0].strip("(;,") == "full"


def check_ledger(entities, flows, manifests, node_ids, claims, base=None):
    """entities, flows: lists of dicts. manifests: {subject: {source id: manifest entry}}.
    node_ids: set of shared node ids. claims: [(subject, claim dict)].
    base: None, or {"entities": {id: dict}, "flows": {id: dict}} read from the --base ref.
    Returns (errors, warnings), each a list of (code, where, message)."""
    err, warn = [], []
    E = lambda c, w, m: err.append((c, w, m))
    W = lambda c, w, m: warn.append((c, w, m))
    all_ids = {x.get("id") for x in entities}
    ents, seen_regs = {}, {}
    for e in entities:
        i = e.get("id")
        if not i or i in ents:
            E("E1", i, "entity id missing or duplicated")
        ents[i] = e
        if e.get("_file") not in (None, i):
            E("E1", i, "id differs from the file name")
        if e.get("type") not in ENTITY_TYPES:
            E("E2", i, f"entity type {e.get('type')!r} not in the allowed list")
        if not COUNTRY.match(str(e.get("country", ""))):
            E("E3", i, f"country {e.get('country')!r} is not an ISO alpha-2 code or 'multiple'")
        for k, v in (e.get("ids") or {}).items():
            if k not in REGISTRY_KEYS:
                E("E4", i, f"ids key {k!r} is not a registry identifier")
            else:
                seen_regs.setdefault((k, str(v)), []).append(i)
        if not isinstance(e.get("rev"), int) or not e.get("history"):
            E("E5", i, "rev (integer) and history (non-empty) are required")
        elif e["history"][-1].get("rev") != e["rev"]:
            E("E5", i, "last history entry does not carry the current rev")
        if e.get("type") == "person_public":
            n = e.get("naming") or {}
            std = n.get("standard")
            srcs = n.get("sources") or []
            if n.get("category") not in NAMING_CATEGORIES or std not in NAMING_STANDARDS:
                E("E6", i, "person_public needs naming.category and naming.standard from the lists")
            elif len(set(srcs)) < NAMING_STANDARDS[std]:
                E("E6", i, f"naming.standard {std} needs at least {NAMING_STANDARDS[std]} distinct sources")
            for ref in srcs:                      # written subject:source-id
                m = (manifests.get(str(ref).split(":")[0]) or {}).get(str(ref).split(":")[-1])
                if m is None or not read_full(m) or "wikipedia.org" in urlparse(str(m.get("url", ""))).netloc:
                    E("E6", i, f"naming source {ref!r} must be a manifest entry read in full, and not Wikipedia")
            if n.get("category") == "organization_officer" and (e.get("role") or {}).get("organization") not in all_ids:
                E("E6", i, "organization_officer needs role.organization that resolves to an entity")
            if not (e.get("role") or {}).get("title"):
                E("E6", i, "person_public needs role.title (the office, profile or position named)")
    for (k, v), who in seen_regs.items():
        if len(who) > 1:
            E("E7", ",".join(who), f"{k} {v} is shared by more than one entity (merge needs an owner-approved history entry)")

    fids = set()
    for f in flows:
        i = f.get("id")
        if not i or i in fids:
            E("F1", i, "flow id missing or duplicated")
        fids.add(i)
        sub = f.get("subject")
        if sub not in manifests:
            E("F2", i, f"subject {sub!r} is not a subject with a sources manifest")
        if f.get("_file") not in (None, sub):
            E("F2", i, "subject differs from the name of the flow file")
        for end in ("from", "to"):
            if f.get(end) not in ents:
                E("F3", i, f"{end} {f.get(end)!r} does not resolve to an entity")
        if f.get("from") == f.get("to"):
            E("F3", i, "from and to are the same entity")
        s = f.get("source")
        entry = (manifests.get(sub) or {}).get(s)
        if entry is None and s not in node_ids:
            E("F4", i, f"source {s!r} is not in the manifest of {sub!r} or a shared node")
        if entry is not None and "wikipedia.org" in urlparse(str(entry.get("url", ""))).netloc:
            E("F4", i, "Wikipedia is never a source")
        st = f.get("status")
        if st not in STATUSES:
            E("F5", i, f"status {st!r} not in the allowed list")
        if st in NEEDS_FULL_READ and entry is not None and not read_full(entry):
            E("F6", i, f"status {st} needs a source read in full; manifest says read: {entry.get('read')!r}")
        if st == "paid" and not [c for c in (f.get("corroboration") or []) if c != s and c in (manifests.get(sub) or {})]:
            E("F7", i, "status paid needs corroboration: a second manifest source, not the one in source")
        if st == "inferred" and not f.get("note"):
            E("F8", i, "status inferred needs a note stating the inference")
        d, en = f.get("date"), f.get("end")
        if d is None:
            if not f.get("date_note"):
                E("F9", i, "date is null and date_note is missing")
        elif not DATE.match(str(d)):
            E("F9", i, f"date {d!r} is not YYYY, YYYY-MM or YYYY-MM-DD")
        if en is not None:
            if not DATE.match(str(en)):
                E("F9", i, f"end {en!r} is not YYYY, YYYY-MM or YYYY-MM-DD")
            elif d is not None and DATE.match(str(d)) and str(en) < str(d):
                E("F9", i, "end is before date")
            if not f.get("note"):
                W("F9w", i, "a flow with an end date needs a note saying what the amount covers")
        a = f.get("amount")
        if a is not None and (isinstance(a, bool) or not isinstance(a, (int, float)) or a < 0):
            E("F10", i, f"amount {a!r} is not a non-negative number or null")
        elif a is not None and not re.match(r"^[A-Z]{3}$", str(f.get("currency", ""))):
            E("F10", i, "amount is set but currency is not a 3-letter code")
        if a is None and not f.get("note"):
            W("F10w", i, "amount is null: a note should say what the source gives instead")
        if not re.match(r"^[a-z][a-z0-9_]*$", str(f.get("kind", ""))):
            E("F11", i, "kind must be a snake_case label")
        if not isinstance(f.get("rev"), int) or not f.get("history"):
            E("F12", i, "rev (integer) and history (non-empty) are required")
        elif f["history"][-1].get("rev") != f["rev"]:
            E("F12", i, "last history entry does not carry the current rev")
        if f.get("note") and ABSENCE_WORDS.search(str(f["note"])):
            W("F13", i, "note reads like an absence statement; absence belongs in a claim with absence_anchor: true")
        for k in ("absent", "no_payment", "none_found"):
            if k in f:
                E("F13", i, f"key {k!r}: a flow records a transfer that a source shows; absence is not a flow")

    if base is not None:
        for kind, new in (("entities", {e.get("id"): e for e in entities}), ("flows", {f.get("id"): f for f in flows})):
            for i, old in base[kind].items():
                cur = new.get(i)
                if cur is None:
                    E("G1", i, f"{kind[:-1]} was removed (LG9: append, never erase)")
                elif cur != old:
                    if (cur.get("rev") or 0) <= (old.get("rev") or 0):
                        E("G1", i, "changed without a higher rev")
                    if (cur.get("history") or [])[:len(old.get("history") or [])] != (old.get("history") or []):
                        E("G1", i, "earlier history entries were edited")
                    if kind == "entities" and any(cur.get(k) != old.get(k) for k in ("name", "type", "ids")) and \
                       not (cur.get("history") or [{}])[-1].get("approved_by") == "owner":
                        E("G2", i, "identity fields (name, type, ids) changed without a history entry approved_by: owner")

    for sub, c in claims:
        a = c.get("anchor") or {}
        blob = " ".join([str(a.get("description", "")), *map(str, a.get("sources") or []),
                         *[str(n.get("node")) for n in a.get("nodes") or [] if isinstance(n, dict)]])
        if "flows" in a:
            E("C1", f"{sub}:{c.get('id')}", "anchor.flows is not allowed (LG7); cite the flow's own source")
        for fid in fids:
            if fid and re.search(r"(?<![\w-])" + re.escape(fid) + r"(?![\w-])", blob):
                E("C1", f"{sub}:{c.get('id')}", f"claim cites flow id {fid} in its anchor (LG7)")
    return err, warn
```

### 3.7 Ownership of `build/ledger/`
`build/ledger/` is not on the owner-only list (`docs/REVIEW.md`, "What only the owner merges"; `.github/CODEOWNERS`). This
proposal keeps it that way, with one exception, and the owner can choose otherwise:
- **Flows** (`build/ledger/flows/<subject>.yaml`) are content of the subject that filed them: written on that dig's branch,
  reviewed with it by the independent review agent, merged on APPROVE as any content PR.
- **New entities** are content, reviewed the same way.
- **Changes to an existing entity's `name`, `type` or `ids`, and every merge or split of entities (LG5)** are escalated to
  the owner: the review agent posts its verdict and does not merge. The enforcement path is check G2 (the change cannot carry
  a passing `history` entry without `approved_by: owner`) plus the review agent's duty to escalate; the validator cannot tell
  whether the owner really approved, so this relies on the review step like every other judgment rule. Making this
  automatic would need `build/ledger/entities/` added to `.github/CODEOWNERS` and to the owner-only list, which would send
  every new entity to the owner as well.
- Adopting this needs a one-line addition to `docs/REVIEW.md` stating the escalation. That file is owner-only and is not
  changed by this proposal.

### 3.8 View (separate decision)
A Ledger page beside the Atlas: entities as points, flows as lines, a time slider, filters by status and country, every
line linking to its source. It is bound by LG11 and LG12. The publication filter (LG11), the totals rule (LG3) and the
drawing limits (LG12) are enforced in the site build (`build/tools/build_site.py`, an owner-only path), which is not
written or tested here. The view must not ship before a build test exists that shows (a) a fixture flow of an unpublished
subject is absent from every output, (b) a fixture with one `filed` and one `pledged` flow totals only the `filed`
one, labelled. Neither test has been run.

### 3.9 Files an adoption would change (all owner-only)
`build/SCHEMA.md` (the section in 3.5, with LG6 only if the owner approves it), `build/conformance.py` (3.6),
`build/tools/build_site.py` (3.8), `docs/REVIEW.md` (3.7), and the pilot's migration (section 5).

## 4. What it does not change
- No existing claim, finding, weight or state changes. The pilot's claims keep their anchors; no claim cites a flow (LG7).
  N25 (anchor format) is unchanged: this revision drops the `anchor.flows` key the first draft proposed.
- P5 and P9 keep their meaning inside politics digs; LG8 extends P5's wording to every subject (a scope change, stated in LG8).
- The publish gate is unchanged; LG11 uses it. Nodes, Atlas, timelines and manifests are unchanged.
- The pilot's source statements are not re-judged here. The migration changes labels in the pilot's data file (types,
  country codes, date forms, one `ids` field moved to `note`) and nothing a claim says; it is logged in the pilot's
  `log.yaml` as a new entry (append-only), and no flow's amount, source or status is changed by the mechanical steps.

## 5. Impact
Counts are from `origin/main` (25de0d2): 20 subjects; and from the pilot branch.

| Subject | Before | After | Migration |
|---|---|---|---|
| israel-palestine-money (`dig/ip-money`, not on `main`, not listed under `publish`, no `review.yaml`) | `conformance.py`: 1 error (stale base, unrelated), 125 warnings; ledger unchecked. `check_ledger`, raw: see 2.3 | Dry run of the mechanical migration: 5 errors, 14 warnings (2.3). Not zero. Those 5 need the author's decision; the final result is not known until they are resolved and the check re-run | Below |
| All 20 subjects on `main` | `conformance.py`: 0 errors, 111 warnings | Not run: `check_ledger` is not in `conformance.py`, and this proposal does not edit it. By construction the function reads only `build/ledger/`, which does not exist on `main`, so it would return nothing; that is a statement about the code, not a run | None: they have no ledger data (ledger data exists for 1 of 21 subjects) |

**Migration of the pilot** (done by the dig's author on its own branch, then reviewed; the owner decides the rules first):
1. Split `data/ledger.yaml` into `build/ledger/entities/<id>.yaml` (136 files, minus the 3 `political_target` entities, plus one
   `aggregate` of recipients: 134) and `build/ledger/flows/israel-palestine-money.yaml` (189 flows).
2. Flow ids `israel-palestine-money-001` to `-189` in file order; `subject`; `rev: 1`; one `history` entry saying "migrated
   from data/ledger.yaml at <commit>". Entities: `rev: 1` and the same history entry.
3. Types and countries as in 3.4; `ids.status` strings to `note`; `partial`, `notified`, `designation`, `reported` kept.
4. Dates: `2012-2025` becomes `date: 2012`, `end: 2025`; `FY2024` becomes `date: 2024`, `period_label: FY2024`;
   `all years` becomes `date: null` with `date_note`; `through FY2020` becomes `date: null`, `end: 2020`, `date_note`.
5. The three flows into `political_target` entities are re-pointed to the recipients `aggregate`; the candidate named in the filing
   goes in the `note`.
6. Author decisions the script cannot make: `naming` and `role` for the two `person_public` entities (or remove them as
   entities under LG6); the one `filed` flow whose source is read through a tool (re-read in full, or relabel `reported`);
   notes for the 13 flows with `end` and no note.
7. `data/ledger.yaml` is replaced by an export generated from `build/ledger/`, so one copy is authoritative.
The dry run in 2.3 executed steps 1 to 5 in memory only; step 6 is why it shows 5 errors.

The warning count on `main` does not change, because no subject on `main` has ledger data.

## 6. Alternatives considered
1. **Do nothing.** Rejected: 2.1 shows an invented flow passes, and the pilot's 15 statuses and 21 types are unconstrained.
2. **Keep a data file per dig and validate it there.** Fixes LG1 to LG4 and LG9 but not duplication of organizations across
   digs; that benefit is a forecast (only one dig has data). It is the fallback if the owner prefers a smaller change, and it
   could adopt LG1 to LG4, LG7, LG10, LG11 unchanged.
3. **Make flows a node type in the Atlas.** A node is a dated artifact with a place; a flow is a relation between two
   parties with an amount and a status. Rejected as a worse fit; a flow's `source` may be a node.
4. **Store totals only (per payer per year).** Loses the record-level source link. Rejected.
5. **Give the ledger its own review instead of tying flows to the publish gate (B5).** Chosen instead: LG11 ties each flow to
   its subject's publication. Reasons: the independent review of a dig already opens the sources behind its flows; a second
   review would be a new process and a new rule set (owner-only files) and would need its own independent reviewer; and a
   shared register with its own gate could show a flow whose dig a reviewer has not passed. The cost: a flow filed by a
   dig that is never published is never shown, however well sourced, and an entity appears only through published flows.
6. **A closed list for `kind`.** Rejected: 41 labels are in use, none is used in logic, and a closed list would need a
   SCHEMA change for each new label. Totals depend on `status`, which is closed.

## 7. Neutrality check
**Not met. Point 7 asks for a test on at least two digs that point in different directions. Only one dig has ledger data
(`dig/ip-money`; every branch of `origin` was searched for ledger or flow data files), so the test has not been run, and no
claim of one is made here.** Nothing in this document shows that the rules treat two digs alike.

What can be said without a second dig, by inspection of section 3: no list, check or rule reads a flow's payer, recipient,
country, direction or amount to decide an outcome. The checks read format, resolvability, `status`, entity `type`, the
manifest `read` value, and `naming`. Country is checked only for format. That is a property of the text, not a test.

Deferred test, to run the first time a second dig has ledger data, before the Ledger view (3.8) is built or any flow is
shown publicly:
1. Record the commit of the rules and the check before reading the second dig's data; do not change either to fit it.
2. Run `check_ledger` on both digs. Tabulate, per dig: errors and warnings per check code per 100 flows; the share of flows
   in totals (`paid`, `filed`); flows excluded by F6; naming rejections (E6); entities mapped or excluded by type.
3. For any check whose rate differs materially between the two digs, open the cases and record whether the cause is the rule's
   wording or the dig's sources. A cause in the rule's wording sends the rule back as a revised proposal.
4. Record the result on the PR that builds the view. The two digs must point in different directions on their questions, as
   `docs/SCHEMA_PROPOSALS.md` requires; the owner picks them.
It tests whether the rules and checks fall unevenly on two different digs. It does not test whether the pilot's selection of
flows met a common standard; that is the dig's review (`docs/REVIEW.md` D) and has not been done for this ledger.
