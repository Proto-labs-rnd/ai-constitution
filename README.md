# Personal AI Constitution

A governance layer that lets humans define how AI agents treat their data, boundaries, and intent. Think of it as a "Terms of Service" between you and your agents.

## Concept

Instead of hardcoded rules, your AI agents read a **constitution file** that defines:
- **Boundaries** — What agents can and cannot do
- **Data policies** — How your data is handled, stored, and shared
- **Consent rules** — What requires explicit permission vs. autonomous action
- **Amendment process** — How rules evolve over time

## Files

| File | Description |
|------|-------------|
| `constitution-validator.py` | Validator engine — parses and enforces constitution rules |
| `sample-constitution.yaml` | Example constitution with boundaries, data policies, consent |
| `test-action-*.json` | Test cases (allow, deny, financial, amend) |
| `VISION.md` | Concept vision and motivation |

## Sample Constitution

```yaml
boundaries:
  - action: "delete files"
    allow: false
    reason: "Data loss risk"
  - action: "send email"
    allow: true
    conditions:
      - "not after 22:00"
      - "not to unknown recipients"

data_policy:
  personal_data:
    store_locally: true
    share_with_third_parties: false
  retention: "30 days"

consent:
  financial_actions: "explicit"
  public_posts: "explicit"
  file_operations: "implicit"
```

## Validator

```bash
python3 constitution-validator.py --constitution sample-constitution.yaml --action test-action-allow.json
# → ALLOWED

python3 constitution-validator.py --constitution sample-constitution.yaml --action test-action-deny.json
# → DENIED: delete files violates boundary
```

## Key Insight

Rule-based enforcement works for binary decisions (allow/deny). The **hard problem** is semantic intent detection — understanding *why* a user wants something, not just *what* they asked. This requires an LLM layer on top of the rule engine.

## Future Directions

- [ ] Semantic intent layer (LLM-powered governance)
- [ ] Agent-specific rules (different boundaries per agent)
- [ ] Temporal rules (time-based consent)
- [ ] Audit trail for all constitutional decisions
- [ ] Integration with OpenClaw agent system

## License

MIT
