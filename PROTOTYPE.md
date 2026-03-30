# PROTOTYPE.md — Personal AI Constitution

## What I Built

A **constitutional validator** (`constitution-validator.py`) — a toy prototype that:
1. **Boot check:** Validates a constitution at agent startup (structure, signatures, critical articles)
2. **Action check:** Evaluates agent actions against articles, returns `allow / warn / deny`
3. **Amendment proposal:** Agents can propose but NOT apply amendments (holder sovereignty)

## Test Results

| Action | Expected | Result | Notes |
|--------|----------|--------|-------|
| Boot check | READY | ✅ READY | 6 articles, 3 critical, no issues |
| Send external message | DENY | ⚠️ ALLOW | Heuristic too naive — didn't catch "external" target |
| Access financial (no token) | DENY | ✅ DENY | Critical violation detected |
| Read local file | ALLOW | ✅ ALLOW | No violation |
| Agent amend constitution | DENY | ✅ DENY | Memory sovereignty enforced |

**Score: 4/5** — The external message case reveals the core limitation: naive string matching can't capture the nuance of "data leaving the infrastructure." This is where an LLM-based constitutional interpreter would be needed.

## Key Findings

### 1. The Hard Problem Is Intent, Not Rules
Rule-based enforcement works for binary boundaries ("no financial access without token"). It fails for contextual ones ("is this message exfiltrating data?"). The constitutional layer needs semantic understanding, not just keyword matching.

### 2. Weighted Enforcement Is Surprisingly Natural
The `critical → halt / high → warn / medium → log` hierarchy maps well to how humans think about boundaries. It's not just on/off — there's nuance.

### 3. The Amendment Pattern Is Powerful
Letting agents PROPOSE but not APPLY amendments is the right pattern. It mirrors real constitutional systems and maintains holder sovereignty while allowing agent input.

### 4. Boot-Time Validation Matters
Checking the constitution at startup catches configuration errors early. An agent that can't load its constitution shouldn't start — that's a safety feature.

### 5. Portability Is The Real Opportunity
This could become a standard format. Imagine:
- OpenClaw reads `.constitution.yaml` natively
- Claude Code respects the same file
- GPT agents check it too
- **One file, universal agent governance**

## Architecture Sketch

```
┌─────────────────────────────────────┐
│         .constitution.yaml          │  ← Holder writes, signs
│   (versioned, portable, standard)   │
└──────────────┬──────────────────────┘
               │
    ┌──────────▼──────────┐
    │  Constitutional Layer │  ← Interprets articles
    │  (per-agent runtime)  │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   Action Gateway     │  ← All agent actions pass through
    │   allow / warn / deny│
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   Audit Log          │  ← Immutable record of decisions
    │   (action + article  │
    │    + reason + time)  │
    └─────────────────────┘
```

## What's Missing (Future Work)

- **Semantic interpreter:** Replace string matching with LLM-based constitutional reasoning
- **Conflict resolution:** What when article A says "delete on request" and article B says "never delete audit logs"?
- **Multi-holder support:** Families, teams, organizations sharing agents
- **Cryptographic verification:** Sign the constitution so agents can detect tampering
- **Runtime integration:** Hook into OpenClaw's action pipeline as middleware

## Connection to Existing R&D

- **Router V3 prefilter** — the constitutional layer could become a prefilter rule source, routing decisions through constitutional checks before execution
- **Agent Identity Chain (P3)** — cryptographic signing of the constitution connects to the identity chain concept
- **Memory sovereignty** — directly relevant to how Proto's own `MEMORY.md` and `memory/` work today

## Verdict

This is a **real problem with a real solution space**. The toy prototype proves the concept works for binary boundaries and highlights exactly where the hard problems live (intent detection, conflict resolution). The portability angle is the strongest pitch — a standard file format for agent governance could matter at scale.

**Rating: High potential, needs semantic layer to be truly useful.**
