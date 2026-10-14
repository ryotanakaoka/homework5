"""Read-only MCP tools for the three open Campus Customs tickets."""

from pathlib import Path
import sqlite3
import asyncio
from typing import Any

from mcp.server.mcpserver import MCPServer


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "campus_customs_new.db"

mcp = MCPServer(
    name="Campus Customs Ticket Resolution",
    description="Read-only ticket-resolution tools backed by campus_customs_new.db",
)


def query_one(sql: str, parameters: tuple[Any, ...]) -> dict[str, Any] | None:
    """Run a read-only query against the copied database."""
    connection = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        row = connection.execute(sql, parameters).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


@mcp.tool()
def get_customer_order_stock_and_invoice() -> dict[str, Any]:
    """Look up the stock, price, and linked invoice needed to resolve ticket 101."""
    ticket = query_one(
        """
        SELECT t.id, t.requester, t.subject, t.sku, t.size, t.qty, t.notes,
               i.name AS product_name, i.qty AS available_qty, i.location,
               p.list_price, t.invoice_id, inv.amount AS invoice_amount,
               inv.due_date AS invoice_due_date, inv.status AS invoice_status,
               v.name AS vendor_name, v.lead_days
        FROM tickets t
        LEFT JOIN inventory i ON i.sku = t.sku AND i.size = t.size
        LEFT JOIN pricing p ON p.sku = t.sku
        LEFT JOIN invoices inv ON inv.id = t.invoice_id
        LEFT JOIN vendors v ON v.id = inv.vendor_id
        WHERE t.id = ? AND t.status = 'open'
        """,
        (101,),
    )
    return ticket or {"ticket_id": 101, "error": "Open ticket not found"}


@mcp.tool()
def get_rent_lease_and_due_date() -> dict[str, Any]:
    """Look up the lease and due-date details needed to resolve ticket 102."""
    ticket = query_one(
        """
        SELECT t.id, t.requester, t.subject, t.notes, t.lease_id,
               l.space_name, l.landlord, l.monthly_rent, l.next_due, l.notes AS lease_notes
        FROM tickets t
        LEFT JOIN leases l ON l.id = t.lease_id
        WHERE t.id = ? AND t.status = 'open'
        """,
        (102,),
    )
    return ticket or {"ticket_id": 102, "error": "Open ticket not found"}


@mcp.tool()
def get_bulk_hoodie_stock_and_price() -> dict[str, Any]:
    """Look up requested quantity, stock, and list price needed to resolve ticket 103."""
    ticket = query_one(
        """
        SELECT t.id, t.requester, t.subject, t.sku, t.size, t.qty AS requested_qty,
               t.notes, i.name AS product_name, i.qty AS available_qty, i.location,
               p.list_price
        FROM tickets t
        LEFT JOIN inventory i ON i.sku = t.sku AND i.size = t.size
        LEFT JOIN pricing p ON p.sku = t.sku
        WHERE t.id = ? AND t.status = 'open'
        """,
        (103,),
    )
    return ticket or {"ticket_id": 103, "error": "Open ticket not found"}


if __name__ == "__main__":
    asyncio.run(mcp.run_stdio_async())
