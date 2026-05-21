> ## 🧱 Part of the MEOK A2A Substrate
>
> This MCP is 1 of 12 agent-to-agent primitives. Run the whole pipeline
> (identity → trust → policy → firewall → rate-limit → handoff → audit
> → governance) as one signed endpoint for **£499/mo** including 100K
> calls — or **£0.0002 per call** pay-as-you-go.
>
> 👉 [meok.ai/a2a](https://meok.ai/a2a) — see the Substrate

# Agent Policy Enforcement MCP


> ## Buy Starter — £29/mo
> **Signed attestations + unlimited audits + email support.**
> 👉 **[Subscribe at meok.ai](https://buy.stripe.com/00w28t94o5km38156o8k841)** — instant HMAC signing key + Stripe-managed billing.
>
> Free tier remains MIT-licensed and zero-config. Upgrade only when you need signed compliance artefacts for audit.

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


## Sister MCPs

Part of the MEOK **A2a** pack — designed to work together as a fleet. Install the whole pack with `npx meok-setup --pack a2a`, or pick the ones you need:

- **Prompt Injection Firewall** → `uvx agent-prompt-injection-firewall-mcp` · [PyPI](https://pypi.org/project/agent-prompt-injection-firewall-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-prompt-injection-firewall-mcp)
- **Data Residency** → `uvx agent-data-residency-mcp` · [PyPI](https://pypi.org/project/agent-data-residency-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-data-residency-mcp)
- **Certified Handoff** → `uvx agent-handoff-certified-mcp` · [PyPI](https://pypi.org/project/agent-handoff-certified-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-handoff-certified-mcp)
- **Audit Logger** → `uvx agent-audit-logger-mcp` · [PyPI](https://pypi.org/project/agent-audit-logger-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-audit-logger-mcp)
- **Rate Limiter** → `uvx agent-rate-limiter-mcp` · [PyPI](https://pypi.org/project/agent-rate-limiter-mcp/) · [GitHub](https://github.com/CSOAI-ORG/agent-rate-limiter-mcp)

Full catalogue + Anthropic Registry verify links: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)


## Protocol coverage + Universal PAYG

This MCP is part of MEOK's 47-MCP fleet that bridges every active agent-interop protocol
and 30+ regulatory frameworks. See the full coverage matrix at [meok.ai/protocols](https://meok.ai/protocols).

**Agent interop protocols supported (8 live):**

- ✅ **MCP** (Anthropic) — native
- ✅ **A2A** (Google + Linux Foundation, absorbed IBM ACP Sept 2025)
- ✅ **IBM ACP** — covered via A2A merge
- ◐ **Stripe ACP** (Agentic Commerce Protocol) — Q3 bridge via [agent-commerce-protocol-mcp](https://github.com/CSOAI-ORG/agent-commerce-protocol-mcp)
- ◐ **AP2** (Google Agent Payments) — partial via [agent-commerce-payments-mcp](https://github.com/CSOAI-ORG/agent-commerce-payments-mcp)
- ◐ **x402** (Coinbase HTTP 402) — partial via api.meok.ai gateway
- → **OASF / AGNTCY** (Cisco Outshift + Linux Foundation) — Q3 bridge
- 👁 **ANP** (Cisco Agent Network) — watch-list

**Pricing options:**

| Option | Price | Best for |
|---|---|---|
| Self-host (this MCP) | £0 — MIT | Devs |
| This MCP Starter | £29/mo | One-MCP teams |
| This MCP Pro | £79/mo | Production + 24h SLA |
| [Universal PAYG](https://buy.stripe.com/00w3cxcgAaEGcIBcyQ8k90s) | £29/mo + £0.0002/call | Spiky usage across many MCPs |
| Substrate bundle (this category) | £99-£499/mo | A whole pack |
| [MEOK Universe](https://buy.stripe.com/cNi9AV0xS8wy5g9aqI8k90u) | £1,499/mo | All 47 MCPs, 500K calls |

Each tier above the free self-host adds HMAC-signed attestations verifiable at
`verify.meok.ai`. Linux Foundation governance on the A2A spine means EU regulated
buyers can deploy without vendor-lock-in objections.

<!-- mcp-name: io.github.CSOAI-ORG/agent-policy-enforcement-mcp -->
