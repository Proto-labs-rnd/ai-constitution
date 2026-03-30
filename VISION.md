# Personal AI Constitution

## The Question

Every agent reads SOUL.md, USER.md, AGENTS.md — but who decides what's in them? Right now: the user writes them ad-hoc, agents interpret them loosely, and there's no formal contract.

What if you had a **constitution** — a single, versioned, cryptographically-signed document that defines the terms of engagement between you and every agent you run?

## Core Concept

A `.constitution.yaml` (or `.md`) that every agent MUST parse at boot:

```yaml
# personal-ai-constitution v1.0
# Signed: sha256:abc123...
# Holder: human identity fingerprint

metadata:
  version: "1.0.0"
  holder: "did:key:z6Mk..."
  issued: "2026-03-30"
  expires: null  # or a date for rotation

articles:
  - id: privacy-1
    title: "No exfiltration"
    text: "My data never leaves my infrastructure without explicit per-instance consent."
    weight: critical  # critical → agent must halt if violated

  - id: autonomy-1
    title: "Right to be forgotten"
    text: "I can request any agent to delete all memory of a conversation within 60s."
    weight: high

  - id: scope-1
    title: "Capability boundaries"
    text: "No agent may access financial accounts, social media, or external communications without a per-session unlock token."
    weight: critical

  - id: transparency-1
    title: "Decision explainability"
    text: "Any agent action that affects external systems must log a human-readable reason."
    weight: medium

  - id: delegation-1
    title: "Chain of command"
    text: "Agents may not delegate to other agents without holder approval, except for pre-approved subagent patterns."
    weight: high

  - id: memory-1
    title: "Memory sovereignty"
    text: "My memory files belong to me. Agents may read but not modify constitutional terms. Only the holder can amend."
    weight: critical

amendments: []
# Future amendments append here with dates and justification

signatures:
  - role: holder
    key: "did:key:z6Mk..."
    timestamp: "2026-03-30T19:14:00Z"
```

## Why This Matters

1. **Today's problem:** Agent configs are scattered, unversioned, and unenforced. USER.md is a freeform text file that agents interpret as suggestions.
2. **The gap:** There's no formal mechanism for a human to say "these are my non-negotiable boundaries" and have agents enforce them programmatically.
3. **The opportunity:** A constitution layer could become a standard — like robots.txt but for personal AI. Interoperable across OpenClaw, Claude, GPT, any agent framework.

## What's Novel Here

- **Weighted enforcement:** `critical` articles halt execution; `high` triggers warnings; `medium` logs.
- **Amendment process:** Like a real constitution — structured, versioned, auditable.
- **Holder sovereignty:** Only the human can amend. Agents can propose but not modify.
- **Portable:** Could work across agent frameworks if adopted as a standard.

## Open Questions

- How does an agent verify the constitution hasn't been tampered with?
- What happens when two articles conflict (e.g., autonomy vs. transparency)?
- Can agents propose amendments, or is this purely top-down?
- How do you handle multiple humans sharing an agent fleet?
- Is this a file format, a protocol, or both?
