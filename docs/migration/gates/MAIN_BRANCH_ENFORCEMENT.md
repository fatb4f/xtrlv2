# Main branch gate enforcement policy

## Objective
**Prevent schema divergence** by enforcing schema SSOT checks on `main` via **required GitHub Actions checks**.

Without branch protection, CI is advisory; with required checks, CI becomes preventive.

---

## Minimum policy (required)

### 1) Workflow triggers
The workflow **must** run on:
- `pull_request` (all PRs targeting `main`)
- `push` to `main` (post-merge validation)

### 2) Required commands
The workflow **must** execute:
- `just ssot-pin-check`
- `pytest -q tests/test_ssot_pin_check_m2_t01.py tests/test_ssot_conformance.py`

### 3) Branch protection
A branch protection rule on `main` **must**:
- Require the workflow status checks to pass before merge.

Recommended additional constraints:
- Require PRs (no direct pushes)
- Require approvals (at least 1)
- Include administrators (reduce bypass risk)

---

## Required check naming (stability rule)
Once a check is required by branch protection, **do not rename**:
- the workflow name
- the job name

Renaming can break protection until settings are updated.

Suggested stable identifiers:
- Workflow name: `schema-ssot-gate`
- Job name: `ssot-gate`

---

## Reference GitHub Actions workflow (template)
Use this as the base for `.github/workflows/schema-ssot-gate.yml`.

```yaml
name: schema-ssot-gate

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  ssot-gate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install tooling
        run: |
          python -m pip install --upgrade pip
          # Adjust to repo packaging:
          # - requirements.txt
          # - pyproject.toml
          # - etc.
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          # Ensure `just` is available (pin version if desired)
          if ! command -v just >/dev/null 2>&1; then
            curl -Ls https://just.systems/install.sh | bash -s -- --to /usr/local/bin
          fi

      - name: SSOT pin check
        run: just ssot-pin-check

      - name: Conformance gate
        run: pytest -q tests/test_ssot_pin_check_m2_t01.py tests/test_ssot_conformance.py
```

---

## Branch protection settings (operational)

In GitHub UI:

- `Settings -> Branches -> Add branch protection rule`
- Branch name pattern: `main`

Enable:

- `Require status checks to pass before merging`
- Select required checks:
  - `schema-ssot-gate / ssot-gate` (label depends on GitHub UI)
- (Recommended) `Require branches to be up to date before merging`
- (Recommended) `Include administrators`

---

## Audit requirement before declaring migration "Done"

Before marking DoD complete:

1. Enumerate gates by layer (`precheck`, `schema-pin`, `conformance`, `tests`, `promote`, `branch-protection`).
2. For each gate, verify:
   - trigger path
   - fail condition
   - evidence artifact
   - required/optional status in CI policy
3. Record one row per gate in `docs/migration/gates/GATE_MATRIX.md`.
4. Execute a negative test sweep (one intentional failure per gate).

Only then finalize: DoD is "Done" after branch protection requires the CI gate checks on `main`.
