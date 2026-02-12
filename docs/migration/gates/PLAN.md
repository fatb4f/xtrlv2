# Gate audit + main-branch enforcement plan

## Goal
Prevent schema divergence by making the schema SSOT checks **required on `main`** (not advisory).

## Scope
This plan covers:
- A **required** GitHub Actions workflow that runs:
  - `just ssot-pin-check`
  - `pytest -q tests/test_ssot_pin_check_m2_t01.py tests/test_ssot_conformance.py`
- **Branch protection** that requires the workflow to pass before merge.
- A focused **gate audit** (enumerate -> verify -> negative test) before declaring migration "Done".

## Operating posture (cutover)
- **xtrlv2 = primary**: active development, planning, schema SSOT.
- **xtrl = transitional**: compatibility/runtime adapter until sunset.
- New milestones/issues land in **xtrlv2 first**.
- xtrl only receives downstream conformance updates driven by xtrlv2 changes.

This reduces split-brain risk and matches the migration objective.

---

## Deliverables
1. `docs/migration/gates/MAIN_BRANCH_ENFORCEMENT.md`
   - Policy + required checks list + branch protection configuration.
2. `docs/migration/gates/GATE_MATRIX.md`
   - One row per gate with trigger/fail/evidence/enforcement.
3. GitHub Actions workflow (to be implemented per policy)
   - Suggested name: `schema-ssot-gate`
   - Triggers: `pull_request`, `push` to `main`
   - Steps: setup (python), install deps, run `just ...`, run `pytest ...`
4. Branch protection rule on `main`
   - Require the workflow status check(s) to pass.
5. CI branch gate requirements (enforced)
   - Required check: `schema-ssot-gate / ssot-gate`
   - Require branches to be up to date before merging
   - Include administrators in protection scope
   - Optional hardening: disallow direct pushes to `main`

---

## Execution steps (timeboxed)

### 1) Implement CI gate workflow
- Add `.github/workflows/schema-ssot-gate.yml` (or similar) per policy.
- Ensure the workflow has **stable check names** (avoid renaming after enforcement).
- Confirm it runs successfully on:
  - a PR
  - a direct push to `main` (post-merge)

### 2) Turn on branch protection
- Add a `main` branch protection rule requiring the workflow checks.
- Include admins (recommended) to prevent bypass.
- Add CI branch gate requirements:
  - required status check `schema-ssot-gate / ssot-gate`
  - require up-to-date branch before merge
  - require PR-based merge flow (no direct pushes) when policy allows

### 2.5) Verify branch-gate enforcement
- Open a test PR that intentionally fails `ssot-gate` and confirm merge is blocked.
- Re-run with passing checks and confirm merge unblocks.
- Capture screenshots/links in migration evidence for auditability.

### 3) Gate audit pass
Enumerate gates by layer:
- precheck
- schema-pin
- conformance
- tests
- promote
- branch-protection

For each gate, verify:
- **Trigger path** (where it runs)
- **Fail condition** (what blocks)
- **Evidence artifact** (what it writes / how it proves it ran)
- **Required vs optional** (in CI policy)

Record one row per gate in `GATE_MATRIX.md`.

### 4) Negative test sweep
Prove each gate blocks correctly with **one intentional failure** per gate:
- Example: change SSOT pin target to an incorrect hash -> `just ssot-pin-check` fails.
- Example: break a conformance fixture -> `tests/test_ssot_conformance.py` fails.

Capture:
- failing command output
- failure reason code / categorization
- expected remediation

### 5) Finalize DoD
Only mark "Done" when:
- CI gate workflow runs on PR + push to `main`
- Branch protection **requires** it to pass prior to merge
- Negative tests have proven the blocking behavior

---

## Acceptance criteria
- A PR cannot merge to `main` when schema SSOT checks fail.
- `main` cannot drift from pinned SSOT / conformance rules without a deliberate, reviewed change.
- `GATE_MATRIX.md` enumerates all gates with verified trigger/fail/evidence/enforcement fields.
