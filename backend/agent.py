"""Five mutually delegating PydanticAI agents for Campus Customs."""

from __future__ import annotations

from pathlib import Path

from pydantic_ai import Agent, RunContext, UsageLimits

from .mcp_client import lookup_ticket_evidence
from .audit import append_event
from .models import TeamDeps
from .model import AGENT_MODEL, MODEL_SETTINGS


MAX_DELEGATION_DEPTH = 4
MAX_REQUESTS = 12


PROMPT_DIR = Path(__file__).parent / "prompts"
PROMPT_FILES = {
    "Boss": "boss.md",
    "Inventory": "inventory.md",
    "Accounting": "accounting.md",
    "Facilities": "facilities.md",
    "Customer Service": "customer_service.md",
}


def _agent(name: str) -> Agent[TeamDeps, str]:
    return Agent(
        AGENT_MODEL,
        name=f"Campus Customs {name}",
        deps_type=TeamDeps,
        system_prompt=(
            (PROMPT_DIR / PROMPT_FILES[name]).read_text(encoding="utf-8")
            + "\n\n" + (PROMPT_DIR / "prompt.md").read_text(encoding="utf-8")
            + "\n\nReturn evidence, risks, and next step."
        ),
        model_settings=MODEL_SETTINGS,
        retries=1,
    )


boss_agent = _agent("Boss")
inventory_agent = _agent("Inventory")
accounting_agent = _agent("Accounting")
facilities_agent = _agent("Facilities")
customer_service_agent = _agent("Customer Service")

AGENTS = {
    "Boss": boss_agent,
    "Inventory": inventory_agent,
    "Accounting": accounting_agent,
    "Facilities": facilities_agent,
    "Customer Service": customer_service_agent,
}


def _delegation_tool(target_name: str):
    async def delegate(ctx: RunContext[TeamDeps], request: str) -> str:
        if ctx.deps.depth >= MAX_DELEGATION_DEPTH:
            return "Delegation stopped: maximum delegation depth reached."
        append_event({"event": f"{target_name} delegation started", "agent": target_name, "ticket_id": ctx.deps.ticket_id, "result": request[:240]})
        target = AGENTS[target_name]
        result = await target.run(
            request,
            deps=TeamDeps(depth=ctx.deps.depth + 1, ticket_id=ctx.deps.ticket_id),
            usage_limits=UsageLimits(request_limit=MAX_REQUESTS),
        )
        append_event({"event": f"{target_name} summary", "agent": target_name, "ticket_id": ctx.deps.ticket_id, "result": str(result.output)[:500]})
        return str(result.output)

    delegate.__name__ = f"delegate_to_{target_name.lower().replace(' ', '_')}"
    delegate.__doc__ = f"Delegate a bounded evidence request to the {target_name} agent."
    return delegate


# Full mutual delegation: every agent can request a bounded review from every other agent.
for source_name, source_agent in AGENTS.items():
    for target_name in AGENTS:
        if source_name != target_name:
            source_agent.tool(_delegation_tool(target_name))

    async def lookup_mcp_for_agent(ctx: RunContext[TeamDeps], ticket_id: int, agent_name: str = source_name) -> str:
        """Read the requested ticket through its approved MCP tool."""
        if ctx.deps.ticket_id is not None and ticket_id != ctx.deps.ticket_id:
            return "Lookup blocked: requested ticket differs from the active ticket."
        append_event({"event": f"{agent_name} MCP lookup", "agent": agent_name, "ticket_id": ticket_id, "result": "Requested ticket-specific MCP evidence"})
        evidence = await lookup_ticket_evidence(ticket_id)
        append_event({"event": f"{agent_name} evidence received", "agent": agent_name, "ticket_id": ticket_id, "result": evidence[:500]})
        return evidence

    lookup_mcp_for_agent.__name__ = "lookup_ticket_evidence_through_mcp"
    source_agent.tool(lookup_mcp_for_agent)


async def run_team(request: str, ticket_id: int | None = None) -> str:
    """Start every workflow at Boss with bounded delegation and model usage."""
    result = await boss_agent.run(
        request,
        deps=TeamDeps(ticket_id=ticket_id),
        usage_limits=UsageLimits(request_limit=MAX_REQUESTS),
    )
    return str(result.output)
