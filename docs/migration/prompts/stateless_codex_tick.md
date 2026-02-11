# Stateless Codex Tick Prompt

Use this prompt with the `codex` tool for one phase per call.

Template:

```
Load `migration/runtime/loop_state.json`.
Execute exactly one phase: <PHASE>.
Run:
python tools/migration/loop_tick.py \\
  --run-id <RUN_ID> \\
  --phase <PHASE> \\
  --status OK \\
  --artifact <OPTIONAL_ARTIFACT_PATH>
Return only the JSON printed by the command.
```

Rules:
- Execute exactly one phase per call.
- Do not run multiple phases in one call.
- Keep output strictly to the command JSON.
