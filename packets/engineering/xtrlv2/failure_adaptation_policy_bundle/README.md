# Failure + Adaptive Strategy Policy (Bundle)

Generated: 2026-02-07

## Files
- `failure_adaptation_policy.schema.json` — JSON Schema (Draft 2020-12)
- `failure_adaptation_policy.example.json` — Minimal example instance

## Typical usage
1. Validate a policy document against the schema.
2. Use `failure_signals[*].detector` to map evidence -> `reason_code`.
3. Execute `strategies[*].steps` as the deterministic response policy.
