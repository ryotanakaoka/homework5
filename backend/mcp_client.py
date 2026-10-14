"""Async MCP client used by agents for all database evidence."""

import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOL_BY_TICKET = {
    101: "get_customer_order_stock_and_invoice",
    102: "get_rent_lease_and_due_date",
    103: "get_bulk_hoodie_stock_and_price",
}


async def lookup_ticket_evidence(ticket_id: int) -> str:
    """Invoke the ticket-specific MCP tool and return only its verified output."""
    tool_name = TOOL_BY_TICKET.get(ticket_id)
    if not tool_name:
        return f"No approved MCP tool exists for ticket {ticket_id}."
    parameters = StdioServerParameters(
        command="python3", args=["mcp_server/server.py"], cwd=str(PROJECT_ROOT)
    )
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, {})
            text = "\n".join(
                item.text for item in result.content if getattr(item, "type", None) == "text"
            )
            return text or json.dumps(result.model_dump(), default=str)
