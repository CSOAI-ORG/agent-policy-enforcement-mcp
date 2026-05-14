# Agent Policy Enforcement MCP

[![PyPI](https://img.shields.io/pypi/v/agent-policy-enforcement-mcp)](https://pypi.org/project/agent-policy-enforcement-mcp/) [![Python](https://img.shields.io/pypi/pyversions/agent-policy-enforcement-mcp)](https://pypi.org/project/agent-policy-enforcement-mcp/)


**Per-agent-pair IAM for A2A orchestration**

The runtime-governance primitive that EU AI Act Article 14 (human oversight) + ISO 42001 Annex A.7 (authorisation) demand for agent-to-agent systems.

By [MEOK AI Labs](https://meok.ai).

## Install

```bash
pip install agent-policy-enforcement-mcp
```

## Tools

- `define_policy`
- `evaluate_call`
- `list_policies`
- `remove_policy`
- `decision_log`
- `sign_policy_attestation`

## Claude Desktop

```json
{
  "mcpServers": {
    "agentpolicyenforcement": { "command": "agent-policy-enforcement-mcp" }
  }
}
```

## Tiers

- **Free** — generous daily limit (100-1,000 depending on operation)
- **Pro £199/mo** — unlimited + signed HMAC attestations with public verify URLs — [subscribe](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836)
- **Enterprise £1,499/mo** — multi-tenant + custom predicate DSL + SIEM webhook push — [subscribe](https://buy.stripe.com/4gM9AV80kaEG0ZT42k8k837)

## Why this exists

The EU AI Act (Aug 2026), DORA (live), ISO 42001, and OWASP LLM01 Top-10 all demand runtime controls for agent systems — not just deployment-time audits. This MCP is that runtime control layer, emitting cryptographically signed evidence your auditor accepts.

## Related MEOK A2A MCPs

- [`agent-policy-enforcement-mcp`](https://pypi.org/project/agent-policy-enforcement-mcp/) — per-pair IAM
- [`agent-handoff-certified-mcp`](https://pypi.org/project/agent-handoff-certified-mcp/) — signed delegation chain
- [`agent-prompt-injection-firewall-mcp`](https://pypi.org/project/agent-prompt-injection-firewall-mcp/) — prompt injection WAF
- [`agent-rate-limiter-mcp`](https://pypi.org/project/agent-rate-limiter-mcp/) — fleet-wide quota
- [`agent-audit-logger-mcp`](https://pypi.org/project/agent-audit-logger-mcp/) — hash-chained signed log
- [`a2a-governance-bridge-mcp`](https://pypi.org/project/a2a-governance-bridge-mcp/) — map A2A to compliance frameworks
- [`meok-attestation-verify`](https://pypi.org/project/meok-attestation-verify/) — independent cert verifier

## License

MIT — MEOK AI Labs, 2026.

<!-- mcp-name: io.github.CSOAI-ORG/agent-policy-enforcement-mcp -->
