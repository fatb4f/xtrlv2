# PR #3 Dependency Matrix

Scope: dependencies for Python-actuator gate cutover and enforcement hardening.

## Task dependencies

| Task | Depends on | Rationale |
|---|---|---|
| PR3-T01 `schema-ssot-gate` trigger cutover | none | Required first so gate runs on PR/push. |
| PR3-T02 Python actuator commands in schema gate | PR3-T01 | Command path only matters once workflow triggers are active. |
| PR3-T03 Add `python-quality-gate` | none | Can be added in parallel with schema gate cutover. |
| PR3-T08 Add ast-grep policy gate | PR3-T01, PR3-T02 | Policy gate validates actuator rules once schema gate contract is updated. |
| PR3-T04 Bind required checks in branch protection | PR3-T01, PR3-T03 | Required checks must exist before protection can require them. |
| PR3-T05 Standalone docs alignment (`xtrlv2` not `xtrl` actuator) | PR3-T02 | Docs must reflect actual executed gate contract. |
| PR3-T06 Evidence links for Issue #2 | PR3-T04 | Need active enforcement and real CI runs to collect proof. |
| PR3-T07 Ruff baseline cleanup | PR3-T03 | Quality gate exists; cleanup makes it reliably green. |
| PR3 closeout | PR3-T06, PR3-T07 | Audit evidence and green required checks are both required. |

## Critical path

1. PR3-T01
2. PR3-T02 and PR3-T03 (parallel)
3. PR3-T08
4. PR3-T04
5. PR3-T07
6. PR3-T06
7. PR3 closeout

## Active blockers

- `ruff` baseline debt prevents `python-quality-gate` from passing.
- Issue #2 evidence links not yet populated with failing/passing run URLs.
