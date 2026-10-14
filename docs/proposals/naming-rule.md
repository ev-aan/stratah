# Proposal: one naming rule for the whole repository (NR1 to NR5)

**Status: DRAFT. Not in force. Needs an independent assessment and the owner's approval (docs/SCHEMA_PROPOSALS.md).**
Drafted at the owner's request in chat, 2026-10-14. It would live at `docs/proposals/naming-rule.md` on a `process/naming-rule` branch. Where this draft makes a choice the owner did not state, it is marked **[drafter's choice]** for the owner to confirm or change.

## Owner decisions this draft rests on (chat, 2026-10-14; not yet in any rule)
1. Names are withheld only for (a) children and youth who are not public figures, and (b) victims where being identified would cause harm.
2. "Child or youth" means **under 18**.
3. Harm is decided by **a named test, applied by the reviewer** (not by free judgment).
4. The current rule about suspects not yet named by authorities is **dropped**.

## 1. The failure case
The repository has no single naming rule. Naming is governed by several narrower texts that do not agree, so each dig invents its own ruling and a strict reading withholds names the owner wants allowed.

Concrete cases, with files (all on `origin/main` unless noted):
- `docs/NEWS_REVIEW.md:10` (guardrail 1) and `docs/AGENT_RULES.md` section 11: "do not name a suspect or a private individual who has not been named by authorities and by multiple independent outlets". Scoped to live news.
- `build/SCHEMA.md:283` (N26): redaction of "personal data (for example a private person's name)", owner's decision. No definition of whose name counts.
- `docs/proposals/topic-admission.md` (draft, not in force): a topic test that mentions not targeting a private individual. Line number not re-checked by me.
- Per-dig rulings written because no general rule existed: `build/subjects/anne-frank-diary/log.yaml:9-11` (L-01: defendants "described by role, not named"), `:94` (L-14, owner ruling 2026-10-08: adults who are parties to a court case may be named; only a minor withheld), `claims.yaml:705` ("The defendants are not named here"); `build/subjects/covid-origins/claims.yaml:1151` ("The officer is not named here") and `:1477` ("public documents name private attorneys; they are not named here").
- The Ledger proposal (PR #24) had to write its own naming rule (LG6), and an independent assessment found that strict reading rejects public figures named from press reports.

This is a failure of consistency and of the rule being written down, shown by the dated texts above. It is not a wrong finding on any page.

## 2. The evidence
- The files and lines above (read 2026-10-14 on `origin/main` 25de0d2, except the topic-admission line).
- The independent assessment of the Ledger proposal (PR #24, first comment) found that the owner's naming rule "is not written anywhere as a general rule".
- Not yet gathered, and for the assessor: a scan of every published dig for names of people under 18 and of victims, to see whether NR1 would change any existing page.

## 3. The proposed change, exactly

**NR1. What is withheld.** A person is not named in any published text, node, log, ledger record or page if they are:
(a) **a child or youth, meaning under 18, who is not a public figure**; or
(b) **a victim, where being identified would cause harm** (NR3).
Anyone else may be named, subject to the ordinary evidence rules: a name is a claim and needs an anchor and a read source like any other claim.

**NR2. Definitions.**
- *Public figure*: a person with a public role or public profile recognised in the sources themselves (an official, candidate, executive or board member acting in that role, performer, athlete, author, party to a public court case), including a young person who is such a figure.
- *Under 18*: the person's age on the date the text is written. **[drafter's choice]** If the age cannot be determined from the sources and the person could plausibly be under 18, withhold until it is determined.
- *Victim*: a person identified in the sources as the injured party of a crime, abuse or disaster. A person is not a victim merely because a claim is made about them.

**NR3. The harm test (named test, applied by the reviewer).** **[drafter's list, owner to edit]** Naming a victim is harmful if any of these holds, shown by a source:
1. the harm is sexual violence, domestic abuse, or trafficking;
2. the person is a protected, anonymous or relocated witness or informant;
3. a source documents a credible threat of retaliation or violence if the person is identified;
4. a court or authority has ordered or requested the person not be identified.
The reviewer records, for each withheld victim, which numbered item applied. A victim who does not meet any item may be named.

**NR4. How it is applied.** A withheld person is referred to by role ("the complainant", "a minor"). A name found in a source that NR1 withholds is not copied into the repository, including source titles and file names where it can be avoided; where the source title itself carries the name, the manifest says so and the name goes no further. **[drafter's choice]** This repeats the N26 redaction practice.

**NR5. What this replaces.** It replaces the naming sentences in `docs/NEWS_REVIEW.md` guardrail 1 and `docs/AGENT_RULES.md` section 11, and widens the scope of N26 to "personal data of a person covered by NR1". Rules against speculating about anyone's religion, ethnicity or beliefs, and the rule that an accusation is not a finding, stay unchanged. Per-dig rulings already made (for example L-14) are consistent with NR1 and stay.

Text changes: add the rule to `docs/AGENT_RULES.md` and `CONTRIBUTING.md`; reword `docs/NEWS_REVIEW.md` guardrail 1; extend `build/SCHEMA.md` N26; add a reviewer check to `docs/REVIEW.md` (new check G: "names"). **Validator:** NR1 cannot be checked mechanically, because it needs a judgment about who a person is. The proposal therefore adds a reviewer check, not a validator check. Where a structured record names a person (for example the Ledger's `naming` block), a validator can check that a basis is stated.

## 4. What it does not change
- No claim, weight, state or assessment of any existing finding.
- Names already withheld in existing digs may stay withheld; NR1 sets the minimum that must be withheld, not a requirement to name anyone.
- The evidence rules for a named person's claims are unchanged: an accusation is not a finding, and a name attached to a claim needs a read source.

## 5. Impact
- Every published dig is affected only by loosening: names currently withheld beyond NR1 could be named in a later change. Nothing has to change on any page.
- Validator before: `main` 25de0d2, 20 subjects, 0 errors, 111 warnings. After: no validator change, so the same. Not yet run on a changed tree because no tree changes.
- Migration: none required. The assessor should scan existing digs for any name NR1 would now require withholding (an under-18 non-public person, or a victim meeting NR3) and report the result.

## 6. Alternatives considered
- **Do nothing.** Narrow per-dig rulings continue; the Ledger and future digs each write their own.
- **Keep the current private-individual rule and add exceptions** (political figures, executives). Rejected by the owner as too restrictive; exceptions would always lag.
- **Victim's wishes decide.** Rejected by the owner in favour of the named test.
- **Keep the suspect rule.** Dropped by the owner's decision.

## 7. Neutrality check (to be done by the assessor)
The rule is about who is a person, not what a page concludes, so it should not favour any topic or answer. The assessor should apply NR1 to at least two digs pointing in different directions and confirm the same treatment. **Not yet done.**

## Risks the assessor should weigh
- Dropping the suspect rule means a person who is accused but uncharged can be named wherever a source names them. The existing rules that an accusation is not a finding and that every claim needs an anchor still apply; the assessor should say whether they are sufficient.
- NR3 depends on a reviewer applying a list to a source; a harm not on the list is not caught.
- The age rule uses the person's age at writing, so an adult who was a child at the time of the events can be named.
