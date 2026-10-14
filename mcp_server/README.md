# Campus Customs MCP Server

This directory contains a read-only Model Context Protocol server built with the MCP 2 `MCPServer` API. It uses the copied database at `data/campus_customs_new.db`, so the source database and all business records remain unchanged.

## Database

The server resolves the path relative to the project directory and opens the database with SQLite `mode=ro`. The tools query the existing `tickets`, `inventory`, `pricing`, `leases`, `invoices`, and `vendors` tables. They do not insert, update, delete, or alter schema records.

## Tools

### `get_customer_order_stock_and_invoice`

Returns ticket 101's requester, product, requested size and quantity, current size-specific stock, location, list price, and linked invoice/vendor details. It helps an agent explain that the Classic Bulldog Tee in size S has zero available units and identify the linked open reprint invoice.

### `get_rent_lease_and_due_date`

Returns ticket 102's requester, lease, shop space, landlord, monthly rent, and next due date. It helps an agent answer the rent notice using the lease record rather than guessing the amount or date.

### `get_bulk_hoodie_stock_and_price`

Returns ticket 103's requester, product, requested quantity, size-specific stock, location, and list price. It helps an agent identify that the Yale AI Club requests 20 size-M hoodies but only 8 are available, so the request is short by 12 units and should not be promised as fulfilled.

## Run

Install the MCP Python package in the active environment, then run from this directory or from the Homework 5 folder:

```bash
pip install mcp
python mcp_server/server.py
```

The default FastMCP transport is suitable for an MCP client that launches the server as a subprocess. Keep `data/campus_customs_new.db` available at its documented path.

## Agent-team use

The Problem 5 backend launches this server through an MCP stdio client. Ticket 101 uses `get_customer_order_stock_and_invoice`, ticket 102 uses `get_rent_lease_and_due_date`, and ticket 103 uses `get_bulk_hoodie_stock_and_price`. Agents never open SQLite directly.
