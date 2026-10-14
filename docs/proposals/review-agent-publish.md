# Proposal: let the review agent publish work it has approved (narrowly)

**Status: DRAFT. Not in force. Needs independent assessment and owner approval (docs/SCHEMA_PROPOSALS.md).**
Drafted at the owner's request in chat, 2026-10-14. This file lives at `docs/proposals/review-agent-publish.md` once it is on a `process/review-agent-publish` branch.

## 1. The failure case
Approved work sits unpublished until the owner merges it, because `review.yaml`, `build/site.yaml` and `build/taxonomy.yaml` are owner-only.

Concrete case: PR #21 (`fix/anne-frank-r5-1`, `build/subjects/anne-frank-diary/{log,review}.yaml`). It was opened 2026-10-08. A first independent reviewer and, on 2026-10-14, a second independent reviewer both posted APPROVE with no blocking findings. It stayed open until the owner told the agent in chat to merge it (2026-10-14, merge commit 25de0d2).

**Honest limit of this case:** the result was a delay of about six days, not a wrong or misleading page. Under standard 1 of `docs/SCHEMA_PROPOSALS.md` ("a wrong, misleading or unusable result") the reviewer should decide whether a delay meets the bar. A second case of the same kind is `dig/covid-origins-atlas` (PR #22), which did not touch an owner-only path and merged within hours of review. That contrast shows the owner-only list, not the review, is what causes the wait.

## 2. The evidence
- PR #21 and PR #22 timelines on the repository (created, review comments, merge).
- `docs/REVIEW.md`, "What only the owner merges": the stated reason for the list is that "a gate reviewed only by agents could lower its own bar".
- Validator on `main` at 25de0d2: 0 errors. (To be re-run by the assessor before and after.)
- Not yet gathered: how many PRs have waited on the owner and for how long. The assessor should count them from the PR history rather than rely on this draft.

## 3. The proposed change
Keep everything on the owner-only list owner-only **except** a narrowly scoped "publish PR" that the review agent may merge, when all of these hold:
1. The PR changes only: (a) `build/subjects/<subject>/review.yaml`, `log.yaml` and the subject's other content files; (b) **one added line** under `publish:` in `build/site.yaml`; (c) **one added entry** for that subject in `build/taxonomy.yaml`. Nothing else.
2. `review.yaml` status is `passed` or `passed_with_open_items`, written by a reviewer who is not the author (PUBLISH_GATE rule, unchanged).
3. **Two** independent reviewers have posted APPROVE on the PR (one more than today), and neither wrote any part of the change.
4. `conformance` is green, including a new check below.
5. No change to `docs/`, `CLAUDE.md`, `CONTRIBUTING.md`, `build/SCHEMA.md`, `build/conformance.py`, `build/tools/`, `.github/`, `build/news.yaml`, `method/`, `netlify.toml` or licence files. A PR touching any of those is escalated exactly as today.

Text changes:
- `docs/REVIEW.md`, "What only the owner merges": add the exception above, word for word.
- `docs/PUBLISH_GATE.md`: state that the owner delegates the *merge click* for conforming publish PRs, not the criteria.
- `.github/CODEOWNERS`: unchanged. GitHub cannot enforce this exception (REVIEW.md "Known limit"), so it holds by agents following the rule, as the rest of the review gate already does.
- Validator: add `check_publish_scope` in `build/conformance.py` (run with `--base origin/main`): fails if a PR labelled as a publish PR changes `site.yaml` or `taxonomy.yaml` by anything other than added lines for the subject named in its `review.yaml`.

## 4. What it does not change
- No claim, weight, state or assessment of any existing subject.
- The criteria for `passed` are unchanged. The owner can still unpublish, revert, or remove the delegation at any time.
- Rules, schema, validator and process documents stay owner-only. This proposal itself needs the owner to merge it.

## 5. Impact
- No existing dig is affected. The 12 subjects on `main`'s `publish` list and their `review.yaml` statuses are untouched.
- Validator before: 0 errors on 25de0d2. After: to be shown by the assessor once `check_publish_scope` is written. Not yet run, because the check does not exist.
- Migration: none.

## 6. Alternatives considered
- **Do nothing.** The owner merges owner-only PRs. Cost: waiting. Benefit: the gate cannot lower its own bar. Reasonable to keep.
- **Owner says "merge" in chat each time** (what happened for PR #21). No rule change, but it depends on the owner's attention and is not recorded as a policy.
- **Only post-publish logging by the agent.** Rejected: does not remove the wait.
- **Full delegation** (the agent may also merge rule, schema and validator changes). Rejected: that lets the agents lower their own gate.

## 7. Neutrality check (to be done by the assessor)
The change is procedural and does not read content, so it should not favour any topic or answer. The assessor should replay the rule on at least two digs that point in different directions (for example `vaccines-autism` and `covid-vaccine-cancer`, or `gulf-of-tonkin` and `apollo-landings`) and confirm the same outcome for both. **Not yet done.**

## Risks the assessor should weigh
- Agents reviewing agents: two reviewers raise the bar but share a failure mode. The owner's sole remaining control would be unpublishing after the fact.
- A mistaken `taxonomy.yaml` or `site.yaml` addition goes live before the owner sees it.
- The "one added line" check is mechanical; it cannot judge whether the subject should be on the site.
