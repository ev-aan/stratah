# Proposal: the Ledger, a shared register of organizations and money transfers (rules LG1 to LG9)

Status: PROPOSAL under `docs/SCHEMA_PROPOSALS.md`, on branch `process/ledger`. Not in force until an
independent reviewer has checked the seven points and the owner has decided. Agents do not merge it.
Requested by the owner on 2026-10-07 ("Yes to ledger"), after the `israel-palestine-money` pilot.

All commands below were run on 2026-10-07 in a checkout of `dig/ip-money` (commit 0060974) on top of
`origin/main` (867ce14). Nothing on `main` was changed to produce this proposal.

## 1. The failure case

A record of who paid whom, how much, when, and on what document, has no place in the schema and no
check in the validator.

The real case is `build/subjects/israel-palestine-money` on `dig/ip-money`. Its money is recorded in
`data/ledger.yaml`: 85 entities and 117 transfers, each with a source id from the dig's manifest
(for example, Havas Media Germany to Clock Tower X LLC, USD 15,000,000, Oct 2025 to Mar 2026, source
`src-fara-7649-clocktowerx`). Three things go wrong today:

1. **Nothing checks it.** `data/` is not read by `conformance.py`. A transfer with an unknown payer, no
   real source, a non-date and a non-number passes exactly like a correct one (section 2).
2. **Organizations are copied, not shared.** The same organizations will recur in other digs: the
   `oct7-warnings` dig and the planned Netanyahu profile both touch Qatar's payments into Gaza
   (claim `ipm-qatar-gaza-payments`), and `congress-promise-vote` lists "FEC, House financial
   disclosures, lobbying filings" as the next step for every actor (`actors.yaml`, `inducement.next`).
   Each dig would write its own copy of "US Treasury", "Havas Media Germany" or a campaign committee,
   and the copies would drift.
3. **Money is squeezed into claims and timeline dots.** In the pilot, payment chains live in claim prose
   (`ipm-israel-us-media-fara`, field `payments_onward`, an unvalidated extra key) and as timeline events
   whose `detail` text repeats amounts. A reader cannot ask "every payment into Central Fund of Israel"
   or "everything Havas paid, by year" without reading every claim.

## 2. Evidence

Validator run with a deliberately broken transfer appended to `data/ledger.yaml`
(`from: nobody`, `amount: lots`, `date: someday`, `source: src-does-not-exist`), then as filed:

```
A. with a broken flow (unknown entity, no source, bad date, non-number amount):
21 subjects and 115 shared nodes checked: 0 errors, 123 warnings
B. as filed:
21 subjects and 115 shared nodes checked: 0 errors, 123 warnings
```

A and B are identical: the validator cannot tell a sourced transfer from an invented one.

Search of `main` for any money structure: `build/SCHEMA.md` mentions money only in the politics rules
(`filing` as a timeline event kind, line 143; P5 "Money is context", line 156; P9 inducement tiers). There
is no entity or transfer record. `grep` over all subjects finds money only as prose, actor `inducement`
placeholders (`congress-promise-vote/actors.yaml`) and timeline dots.

## 3. The proposed change, exactly

### 3.1 Files
```
build/ledger/entities/<entity-id>.yaml     one file per organization, agency, committee or fund
build/ledger/flows/<subject>/<flow-id>.yaml one file per transfer, grouped by the subject that filed it
```
Shared like `build/nodes/`: any dig may cite an entity or flow; the file is kept once.

### 3.2 Entity fields
`id` (permanent, equals file name), `rev`, `name`, `type` (government | government_agency |
government_fund | quasi_government | company | bank | charity | foundation | donor_advised_fund |
political_committee | un_agency | armed_group | designated_network | organization | aggregate),
`country` (ISO code or `multiple`), `ids` (registry identifiers: `ein`, `cra_bn`, `uk_charity`,
`fara_registration`, `company_number`, `budget_code`, `fec_id`), optional `aliases`, `note`, `history`.

### 3.3 Flow fields
`id`, `rev`, `from` (entity id), `to` (entity id), `amount` (number or `null` when the source gives
none), `currency` (as the source states it), `date` (ISO date, month or year), optional `end`,
`kind` (payment_received, payment_made, grant_abroad, foundation_grant, appropriation, pledge,
budget_support, clearance_revenue_transfer, contracted, loan_guarantee, political_donation,
court_finding, civil_judgment, estimate, reported_payment, ...), `status`, `source` (a manifest id
of the filing subject, or a node id), `subject` (the dig that filed it), optional `note`, `history`.

`status` is one of: `filed` (a document filed by a party records it), `paid` (a payment record shows
it), `contracted`, `pledged`, `guarantee`, `estimate` (a party's estimate, no published method),
`convicted`, `judgment`, `verdict_vacated`, `reported_disputed`, `sources_differ`, `inferred`.

### 3.4 Rules (text for `build/SCHEMA.md`, new section "Ledger")
- **LG1 Every flow has a source.** `source` resolves to a manifest id in its `subject` or to a node.
  A flow with no source is an error.
- **LG2 Both ends exist.** `from` and `to` resolve to entity files.
- **LG3 Status is stated** and is one of the list above. `pledged`, `contracted`, `guarantee` and
  `estimate` are never summed with `paid` or `filed` in any total the site shows.
- **LG4 Amounts stay as the source gives them**: number, currency and year. Any conversion or
  inflation adjustment is a separate, labelled calculation of class `synthetic`, never written into
  `amount`.
- **LG5 Entities merge only on a shared registry identifier** (`ids`), or by an owner-approved
  `history` entry; never on name alone. Two entities with the same name and different identifiers stay
  separate.
- **LG6 Private individuals are not entities** unless a public filing names them in that role (for
  example a signatory on a FARA filing, a foundation, a public official, a party to a court case).
  A donor-advised fund is recorded as the payer; its underlying donors are not inferred.
- **LG7 A flow is a record, not a finding.** It confers no evidential weight on any claim unless the
  claim cites it in `anchor.nodes`-style references (`anchor.flows: [{flow, verb}]`). Same firewall as
  threads (TH2) and transmission chains (X3).
- **LG8 Timing is context** (extends P5 to every subject): a flow shown beside a vote, decision or
  event shows timing only; the page says so unless a source documents the link.
- **LG9 Append-only.** A correction is a new `rev` with a `history` line; nothing is deleted.

### 3.5 Validator (`build/conformance.py`, new function `check_ledger`)
Errors for: LG1 (unresolved `source`), LG2 (unresolved `from`/`to`), LG3 (unknown `status`), malformed
`date`, non-numeric non-null `amount`, missing `currency` when `amount` is set, duplicate ids, an entity
whose `ids` value equals another entity's (LG5), `rev`/`history` out of step (LG9, as N7 does for nodes).
Warning for: a claim citing a flow id outside `anchor.flows` (LG7, mirrors TH2).

### 3.6 View (optional, separate decision)
A Ledger page beside the Atlas: entities as points, flows as lines, a time slider, filters by status
and country, and every line linking to its source. The Atlas shows a flow as a dated event; the Ledger
shows a node as evidence. The view can be decided separately from the rules.

## 4. What it does not change
- No existing claim, finding, weight or state changes. The pilot's claims keep their anchors; adding
  `anchor.flows` to them is optional and would be logged.
- The politics rules P5 and P9 keep their meaning; LG8 only applies P5's wording to every subject.
- Nodes, Atlas, timelines and manifests are unchanged. No existing file is moved except the pilot's
  `data/ledger.yaml`, which is migrated (section 5).

## 5. Impact
| Subject | Before | After | Migration |
|---|---|---|---|
| israel-palestine-money (`dig/ip-money`) | 0 errors; ledger unchecked | Expected 0 errors after migration; a dry run is part of the implementation step | Script splits `data/ledger.yaml` into 85 entity files and 117 flow files; the data file is kept as a generated export |
| congress-promise-vote | 0 errors | 0 errors | None now; its FEC and lobbying next steps would file flows later |
| All other 19 subjects | 0 errors | 0 errors | None: they have no transfers |

The warning count on `main` does not change, because no subject on `main` has ledger data.

## 6. Alternatives considered
1. **Do nothing.** Rejected: section 2 shows invented transfers pass, and organizations would be
   duplicated across digs.
2. **Keep a data file per dig and validate it there.** Fixes LG1 to LG4 but not duplication: the same
   payer would exist once per dig. Rejected for the shared-register reason, though it is the fallback if
   the owner prefers a smaller change.
3. **Make transfers a node type in the Atlas.** Nodes are dated artifacts with a place; a transfer is a
   relation between two parties with an amount and a status. Forcing it into a node would need
   `from`, `to`, `amount` and `status` on every node type, or a special case in N1 to N24. Rejected as
   a worse fit; the proposal links the two instead (a flow's source may be a node).
4. **Store totals only (per payer per year).** Loses the record-level source link that lets a reader
   check each line. Rejected.

## 7. Neutrality check
The rules name no topic, side or outcome. Tested against two sets that point different ways:
- **israel-palestine-money:** its 117 transfers include Israeli government payments to US media firms,
  US aid to Israel, Qatari and Iranian money to Gaza and armed groups, a conviction for money to Hamas,
  US charities and foundations funding settlement institutions, and donor aid to the PA. Every rule
  applies identically to each; LG3 keeps the Iranian "up to $100 million" (`estimate`) and Qatar's 2012
  figures (`sources_differ`) out of totals in the same way it keeps the US-Israel MOU (`pledged`) out.
- **congress-promise-vote:** two members of opposite parties (Barragan, Alford). Under LG8, any
  FEC or lobbying flow filed for either would carry the same timing-only label, and under LG6 their
  individual donors would not be entities unless a filing names them.
No rule depends on a flow's direction, payer, recipient or country.
