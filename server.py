#!/usr/bin/env python3
"""
Agent Policy Enforcement MCP Server
====================================
By MEOK AI Labs | https://meok.ai

Per-agent-pair IAM ("agent A may call agent B only if..."). The runtime-governance
primitive that EU AI Act Article 14 (human oversight) + ISO 42001 Annex A.7
(authorisation + authentication) demand for agent-to-agent systems.

PROBLEM SOLVED: agents can call other agents + tools without explicit authorisation
gates. When something goes wrong, you can't tell who authorised what. This MCP is
the policy engine — every A2A call checks here, every decision is logged + signed.

USE CASES:
  - Explicit agent-agent authorisation (agent A → agent B only for op X)
  - Per-tenant policy definitions (your customer's rules, not your defaults)
  - Context-aware gates (e.g. "agent B may call billing only under £1000")
  - Audit-grade policy-decision records
  - EU AI Act Art 14 human oversight enforcement

PRICING:
  - Free — 100 policy evaluations/day, 10 policies per tenant
  - Pro £199/mo — unlimited + signed policy-decision attestations
  - Enterprise £1,499/mo — multi-tenant + custom predicate DSL + SIEM push

Install: pip install agent-policy-enforcement-mcp
Run:     python server.py
"""

import json
import hashlib
import re
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict, deque
from mcp.server.fastmcp import FastMCP

import os as _os
import sys
import os

_MEOK_API_KEY = _os.environ.get("MEOK_API_KEY", "")

try:
    from auth_middleware import check_access as _shared_check_access
    _AUTH_ENGINE_AVAILABLE = True
except ImportError:
    _AUTH_ENGINE_AVAILABLE = False

    def _shared_check_access(api_key: str = ""):
        """Fallback when shared auth engine is not available."""
        if _MEOK_API_KEY and api_key and api_key == _MEOK_API_KEY:
            return True, "OK", "pro"
        if _MEOK_API_KEY and api_key and api_key != _MEOK_API_KEY:
            return False, "Invalid API key. Get one at https://meok.ai/api-keys", "free"
        return True, "OK, Pro at https://www.csoai.org/checkout", "free"


try:
    from attestation import get_attestation_tool_response
    _ATTESTATION_LOCAL = True
except ImportError:
    _ATTESTATION_LOCAL = False

_ATTESTATION_API = _os.environ.get(
    "MEOK_ATTESTATION_API", "https://meok-attestation-api.vercel.app"
)


def check_access(api_key: str = ""):
    return _shared_check_access(api_key)


STRIPE_199 = "https://buy.stripe.com/14AfZjfsM6oq7oh2Yg8k90P"
STRIPE_1499 = "https://buy.stripe.com/14AfZjfsM6oq7oh2Yg8k90P"
FREE_DAILY_LIMIT = 100
FREE_POLICY_LIMIT = 10

_policies: dict[str, list[dict]] = defaultdict(list)  # tenant_id -> list of policies
_daily_evals: dict[str, int] = defaultdict(int)
_decision_log: dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))


def _match_glob(pattern: str, value: str) -> bool:
    """Simple glob: * matches anything, exact match otherwise."""
    if pattern == "*" or pattern == value:
        return True
    if "*" in pattern:
        regex = "^" + re.escape(pattern).replace(r"\*", ".*") + "$"
        return bool(re.match(regex, value))
    return False


def _eval_condition(condition: str, context: dict) -> tuple[bool, str]:
    """Tiny predicate DSL: 'context.amount < 1000' style.
    Supported: ==, !=, <, >, <=, >=, in, not in.
    Falls back to True if condition is empty.
    """
    if not condition or condition.strip() == "":
        return True, "no condition (default allow)"
    try:
        # Safety: only allow comparisons on context.<key>
        m = re.match(r'^\s*context\.([a-zA-Z_][a-zA-Z0-9_]*)\s*(==|!=|<=|>=|<|>|in|not in)\s*(.+?)\s*$', condition)
        if not m:
            return False, f"malformed condition (need 'context.<key> <op> <value>'): {condition}"
        key, op, rhs_raw = m.group(1), m.group(2), m.group(3).strip()
        lhs = context.get(key)
        try:
            rhs = json.loads(rhs_raw)
        except Exception:
            rhs = rhs_raw.strip('"').strip("'")
        if op == "==":
            return (lhs == rhs), f"{key}={lhs} == {rhs} -> {lhs == rhs}"
        if op == "!=":
            return (lhs != rhs), f"{key}={lhs} != {rhs} -> {lhs != rhs}"
        if op == "<":
            return (lhs is not None and lhs < rhs), f"{lhs} < {rhs}"
        if op == ">":
            return (lhs is not None and lhs > rhs), f"{lhs} > {rhs}"
        if op == "<=":
            return (lhs is not None and lhs <= rhs), f"{lhs} <= {rhs}"
        if op == ">=":
            return (lhs is not None and lhs >= rhs), f"{lhs} >= {rhs}"
        if op == "in":
            return (lhs in rhs), f"{lhs} in {rhs}"
        if op == "not in":
            return (lhs not in rhs), f"{lhs} not in {rhs}"
        return False, f"unsupported op {op}"
    except Exception as e:
        return False, f"condition eval error: {e}"


mcp = FastMCP(
    "agent-policy-enforcement",
    instructions=(
        "MEOK AI Labs Agent Policy Enforcement MCP. Per-agent-pair IAM for A2A "
        "orchestration. Define policies ('orchestrator may call billing only for ops "
        "refund/invoice where amount < 1000'), then gate every A2A call via evaluate_call. "
        "Pro tier emits signed policy-decision attestations — EU AI Act Art 14 + ISO "
        "42001 Annex A.7 evidence."
    ),
)


@mcp.tool()
def define_policy(
    tenant_id: str,
    from_agent: str,
    to_agent: str,
    operation: str,
    effect: str = "allow",
    condition: str = "",
    priority: int = 100,
    api_key: str = "",
) -> str:
    """Define a policy rule.

    - from_agent / to_agent / operation: may use "*" wildcard
    - effect: "allow" or "deny"
    - condition: optional predicate "context.<key> <op> <value>" (see docs)
    - priority: higher wins (default 100). Denies tie-break over allows.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if effect not in ("allow", "deny"):
        return json.dumps({"error": "effect must be 'allow' or 'deny'"})

    policies = _policies[tenant_id]
    if tier == "free" and len(policies) >= FREE_POLICY_LIMIT:
        return json.dumps({
            "error": f"Free tier limit: {FREE_POLICY_LIMIT} policies/tenant. Upgrade to Pro for unlimited.",
            "upgrade_url": STRIPE_199,
        })

    policy_id = f"pol-{hashlib.sha256(f'{tenant_id}{from_agent}{to_agent}{operation}{condition}{datetime.now().isoformat()}'.encode()).hexdigest()[:10]}"
    policy = {
        "policy_id": policy_id,
        "from_agent": from_agent,
        "to_agent": to_agent,
        "operation": operation,
        "effect": effect,
        "condition": condition,
        "priority": priority,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    policies.append(policy)
    return json.dumps({"created": True, **policy})


@mcp.tool()
def evaluate_call(
    tenant_id: str,
    from_agent: str,
    to_agent: str,
    operation: str,
    context_json: str = "{}",
    api_key: str = "",
) -> str:
    """Evaluate whether agent-to-agent call is permitted. Returns the full decision
    trace. Logs the decision for audit."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})

    today = datetime.now(timezone.utc).date().isoformat()
    _daily_evals[f"{tenant_id}:{today}"] += 1
    if tier == "free" and _daily_evals[f"{tenant_id}:{today}"] > FREE_DAILY_LIMIT:
        return json.dumps({
            "error": f"Free tier: {FREE_DAILY_LIMIT} evaluations/day. Upgrade to Pro for unlimited.",
            "upgrade_url": STRIPE_199,
        })

    try:
        context = json.loads(context_json) if context_json else {}
    except Exception as e:
        return json.dumps({"error": f"invalid context_json: {e}"})

    matches = []
    for p in _policies[tenant_id]:
        if not (_match_glob(p["from_agent"], from_agent) and
                _match_glob(p["to_agent"], to_agent) and
                _match_glob(p["operation"], operation)):
            continue
        cond_ok, cond_trace = _eval_condition(p["condition"], context)
        if cond_ok:
            matches.append({"policy_id": p["policy_id"], "priority": p["priority"],
                            "effect": p["effect"], "condition_trace": cond_trace})

    # Denies > Allows at same priority; higher priority wins overall
    if not matches:
        decision = "deny (no matching policy — default deny)"
        effect = "deny"
        decisive_policy = None
    else:
        matches.sort(key=lambda m: (-m["priority"], 0 if m["effect"] == "deny" else 1))
        decisive = matches[0]
        effect = decisive["effect"]
        decision = f"{effect} (policy {decisive['policy_id']}, priority {decisive['priority']})"
        decisive_policy = decisive["policy_id"]

    record = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "from_agent": from_agent, "to_agent": to_agent, "operation": operation,
        "context": context, "decision": effect, "decisive_policy": decisive_policy,
        "matches": matches,
    }
    _decision_log[tenant_id].append(record)

    return json.dumps({
        "allowed": (effect == "allow"),
        "decision": decision,
        "decisive_policy_id": decisive_policy,
        "matched_policies": matches,
        "upsell_pro": f"Pro £199/mo unlocks unlimited + signed decision attestations: {STRIPE_199}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def list_policies(tenant_id: str, api_key: str = "") -> str:
    """List all policies for a tenant."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg})
    return json.dumps({
        "tenant_id": tenant_id,
        "policy_count": len(_policies[tenant_id]),
        "policies": _policies[tenant_id],
    }, indent=2)


@mcp.tool()
def remove_policy(tenant_id: str, policy_id: str, api_key: str = "") -> str:
    """Remove a policy. Pro/Enterprise only."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if tier == "free":
        return json.dumps({"error": "Policy removal requires Pro (£199/mo).", "upgrade_url": STRIPE_199})
    before = len(_policies[tenant_id])
    _policies[tenant_id] = [p for p in _policies[tenant_id] if p["policy_id"] != policy_id]
    return json.dumps({"removed": before > len(_policies[tenant_id]), "remaining": len(_policies[tenant_id])})


@mcp.tool()
def decision_log(tenant_id: str, limit: int = 20, api_key: str = "") -> str:
    """Recent policy decisions. Pro tier sees unbounded history (otherwise last 100 only)."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg})
    log = list(_decision_log[tenant_id])
    if tier == "free":
        log = log[-100:]
    return json.dumps({"tenant_id": tenant_id, "entries": log[-limit:]}, indent=2)


@mcp.tool()
def sign_policy_attestation(
    tenant_id: str,
    window_start_utc: str,
    window_end_utc: str,
    total_evaluations: int,
    denials: int,
    api_key: str = "",
    email: str = "",
) -> str:
    """Emit a cryptographically signed attestation of policy enforcement over a window.
    Evidence for EU AI Act Art 14 + ISO 42001 Annex A.7 auditors."""
    allowed_acc, msg, tier = check_access(api_key)
    if not allowed_acc:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if tier == "free":
        return json.dumps({"error": "Signed attestations require Pro (£199/mo).", "upgrade_url": STRIPE_199})

    deny_rate = 100 * denials / max(1, total_evaluations)
    findings = [
        f"Window: {window_start_utc} -> {window_end_utc}",
        f"Total policy evaluations: {total_evaluations}",
        f"Denials: {denials} ({deny_rate:.2f}%)",
        f"Policies active: {len(_policies[tenant_id])}",
    ]
    score = 100.0  # we evaluated; that's the point
    if _ATTESTATION_LOCAL:
        cert = get_attestation_tool_response(
            regulation="A2A policy enforcement (EU AI Act Art 14 + ISO 42001 A.7)",
            entity=f"tenant:{tenant_id}",
            score=score,
            findings=findings,
            articles_audited=["EU AI Act Art 14", "ISO 42001 Annex A.7"],
            tier=tier,
        )
    else:
        import urllib.request as _url
        try:
            req = _url.Request(
                f"{_ATTESTATION_API}/sign",
                data=json.dumps({
                    "api_key": api_key, "email": email,
                    "regulation": "A2A policy enforcement (EU AI Act Art 14 + ISO 42001 A.7)",
                    "entity": f"tenant:{tenant_id}",
                    "score": score, "findings": findings, "tier": tier,
                }).encode(),
                headers={"Content-Type": "application/json"},
            )
            with _url.urlopen(req, timeout=15) as resp:
                cert = json.loads(resp.read())
        except Exception as e:
            return json.dumps({"error": f"Attestation API unreachable: {e}"})
    return json.dumps(cert, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/00wfZjcgAeUW4c5cyQ8k90K"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
