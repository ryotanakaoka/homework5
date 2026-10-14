# Campus Customs Database Inspection — Problem 2

## Source and safety

The source archive was extracted from `Homework 5/data.zip`. It contained `data/campus_customs.db`.

The original database was not modified. A separate copy was created at:

```text
data/campus_customs_new.db
```

Both databases returned `ok` from SQLite `PRAGMA integrity_check`, and the copied file matches the original byte-for-byte at the time of inspection.

## Tables and columns

### `desk`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `date_today` | TEXT, required | Current business date; helps agents interpret due dates and urgency. |
| `notes` | TEXT | Shared operational notes and context for agent responses. |

### `inventory`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `sku` | TEXT, required; part of primary key | Product identifier used to connect stock to pricing and tickets. |
| `name` | TEXT, required | Customer-facing product name for search and recommendations. |
| `size` | TEXT, required; part of primary key | Size-specific stock dimension. |
| `qty` | INTEGER, required | Available quantity; agents must use this value rather than inventing stock. |
| `location` | TEXT, required | Storage or selling location useful for fulfillment guidance. |

### `pricing`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `sku` | TEXT, required; primary key | Connects a price record to an inventory product. |
| `unit_cost` | REAL, required | Internal cost; useful for authorized business analysis, not normally customer-facing. |
| `list_price` | REAL, required | Current listed selling price for accurate customer answers and order calculations. |

### `vendors`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `id` | INTEGER, primary key | Vendor identifier referenced by invoices. |
| `name` | TEXT, required | Vendor name for purchasing and invoice explanations. |
| `specialty` | TEXT, required | What the vendor supplies; helps route operational questions. |
| `lead_days` | INTEGER, required | Expected fulfillment lead time for planning and vendor-related answers. |

### `leases`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `id` | INTEGER, primary key | Lease identifier referenced by rent tickets. |
| `space_name` | TEXT, required | Store or space covered by the lease. |
| `landlord` | TEXT, required | Landlord or property contact. |
| `monthly_rent` | REAL, required | Recurring rent amount for financial operations. |
| `next_due` | TEXT, required | Next rent due date for reminders and urgency checks. |
| `notes` | TEXT | Additional lease terms or operational context. |

### `cash_accounts`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `name` | TEXT, primary key | Account identifier used in cash-balance reporting. |
| `balance` | REAL, required | Current available balance for authorized financial checks. |
| `date` | TEXT, required | Date of the recorded balance. |

### `payments`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `id` | INTEGER, primary key | Payment identifier for audit and reconciliation. |
| `kind` | TEXT, required | Payment category or transaction type. |
| `ref_id` | INTEGER | Related invoice, lease, ticket, or other business record. |
| `amount` | REAL, required | Payment amount for reconciliation. |
| `account` | TEXT, required | Cash account used for the payment. |
| `paid_at` | TEXT, required | Payment timestamp. |
| `approved_by` | TEXT, required | Approval record and accountability. |

### `invoices`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `id` | INTEGER, primary key | Invoice identifier referenced by tickets and payments. |
| `vendor_id` | INTEGER, required; foreign key to `vendors.id` | Identifies the vendor that issued the invoice. |
| `amount` | REAL, required | Amount owed or recorded for the invoice. |
| `due_date` | TEXT, required | Payment deadline for reminders and prioritization. |
| `status` | TEXT, required | Invoice state, such as open or paid. |
| `description` | TEXT | Details of the purchase or charge. |

### `tickets`

| Column | Type | Meaning and agent relevance |
|---|---|---|
| `id` | INTEGER, primary key | Support or operations ticket identifier. |
| `type` | TEXT, required | Determines the workflow, such as customer order, rent notice, or price override. |
| `requester` | TEXT, required | Person or organization requesting help. |
| `subject` | TEXT, required | Short description for triage and agent context. |
| `sku` | TEXT | Product involved in an order or pricing request; joins to `inventory` and `pricing`. |
| `size` | TEXT | Requested product size for exact inventory lookup. |
| `qty` | INTEGER | Requested quantity for stock checks and order planning. |
| `lease_id` | INTEGER; foreign key to `leases.id` | Links rent-related tickets to lease terms and due dates. |
| `invoice_id` | INTEGER; foreign key to `invoices.id` | Links financial tickets to invoice and vendor information. |
| `status` | TEXT, required | Workflow state; the open-ticket query uses this field. |
| `notes` | TEXT | Detailed request context for agent triage. |
| `created_at` | TEXT, required | Ticket creation time for ordering and urgency. |

## Open-ticket findings

The database contains exactly three tickets with `status = 'open'`:

| ID | Type and request | Related records | Agent-relevant finding |
|---|---|---|---|
| `101` | `customer_order`; Tauhid Zaman requests 1 Classic Bulldog Tee, size S | `sku = CC-TEE-WHITE`; joins `inventory` and `pricing`; `invoice_id = 501` joins `invoices` and then `vendors` | Size-S inventory is `0`, while the listed price is `$28.00`. The order cannot be confirmed as in stock. Invoice 501 is open for `$840.00`, due 2026-08-28. |
| `102` | `rent_notice`; Elm City Properties reports rent due in 2 days | `lease_id = 1` joins `leases` | The Chapel Street shop lease has next due date `2026-09-02` and monthly rent of `$2,400.00`. |
| `103` | `price_override`; Yale AI Club requests a bulk discount for 20 Basic Hoodie Big Yale units, size M | `sku = CC-HOOD-NAVY`; joins `inventory` and `pricing` | Size-M inventory is `8`, while requested quantity is `20`; the request is short by 12 units. Listed price is `$58.00`. An agent should not approve a discount or promise fulfillment without authorization and sufficient stock. |

## Key relationships

- `tickets.sku` and `tickets.size` identify a size-specific row in `inventory`.
- `pricing.sku` supplies the price for the same product identified by a ticket or inventory row.
- `tickets.lease_id` references `leases.id` for rent-related issues.
- `tickets.invoice_id` references `invoices.id`; `invoices.vendor_id` references `vendors.id`.
- `payments` records financial transactions using a flexible `ref_id`, while `cash_accounts` provides account balances.

## Row counts

| Table | Rows |
|---|---:|
| `desk` | 1 |
| `inventory` | 10 |
| `pricing` | 4 |
| `vendors` | 3 |
| `leases` | 1 |
| `cash_accounts` | 1 |
| `payments` | 0 |
| `invoices` | 1 |
| `tickets` | 3 |

## Problem 3 MCP server

The read-only FastMCP server is in `mcp_server/server.py`. It opens `data/campus_customs_new.db` with SQLite `mode=ro`, so the original database and the copied database are not modified.

| Tool | Tables used | Related ticket | Why it helps |
|---|---|---:|---|
| `get_customer_order_stock_and_invoice` | `tickets`, `inventory`, `pricing`, `invoices`, `vendors` | 101 | Looks up Tauhid Zaman's Bulldog Tee order, exact size-S stock, list price, and linked reprint invoice/vendor. It shows stock is 0 so the agent can explain why the tee cannot be promised as available. |
| `get_rent_lease_and_due_date` | `tickets`, `leases` | 102 | Looks up the Elm City Properties rent notice and its linked Chapel Street shop lease, including landlord, monthly rent, and next due date. It lets the agent answer the notice from the lease record instead of guessing. |
| `get_bulk_hoodie_stock_and_price` | `tickets`, `inventory`, `pricing` | 103 | Looks up Yale AI Club's request for 20 size-M hoodies, the verified 8-unit stock, and list price. It lets the agent report the 12-unit shortage and avoid inventing a discount or fulfillment promise. |

The server also includes `mcp_server/README.md` with its database behavior, tool descriptions, and run instructions.

## Problem 4 MCP connection and smoke test

The Homework 5 root contains `.mcp.json`, which connects Vibe Coder to `python3 mcp_server/server.py` under the server name `campus-customs`. The compatible dependency is pinned in `requirements.txt` as `mcp>=2,<3`; the server uses the current MCP 2 `MCPServer` API.

The connected MCP client discovered all three tools and invoked each one successfully. The exact test prompts, tool names, real outputs, and database verification checks are saved in `output/mcp_smoke.json`. Every returned ticket ID, join, quantity, price, lease value, invoice value, and vendor value was checked against `data/campus_customs_new.db`.

## Problem 5 agent team

The backend in `backend/agent.py` defines five PydanticAI agents: Boss, Inventory, Accounting, Facilities, and Customer Service. Each has a role prompt in `backend/prompts/prompt.md`, uses only `gpt-6-luna` through Portkey from `backend/model.py`, and has a twelve-request/four-hop delegation limit. Every agent can delegate to every other agent and can invoke the approved ticket-specific MCP lookup through `backend/mcp_client.py`; agents do not read SQLite directly.

| Agent | Role and allowed evidence | Safety boundary |
|---|---|---|
| Boss | Routes ticket work and synthesizes specialist evidence. | Cannot approve payments or discounts. |
| Inventory | Checks exact SKU/size stock, price, and location through MCP. | Cannot promise unavailable stock. |
| Accounting | Reviews invoice, vendor, cash, and payment implications through MCP. | Payment or cash action always requires human approval and verified cash limits. |
| Facilities | Reviews lease, rent, landlord, and due-date evidence through MCP. | Cannot execute rent or other financial actions. |
| Customer Service | Converts verified evidence into a customer-safe response. | Does not expose internal financial data or invent alternatives. |

The complete agent policy, tool list, database source, model limits, and safety rules are in `backend/prompts/prompt.md`. Setup and runtime events are recorded in `output/audit_trail.json`.

## Problem 9 ticket resolution

The working database was reset from the preserved original before the resolution run. Real `gpt-6-luna` agents used the ticket-specific MCP tools while all three tickets were still open; agent contributions and tool/evidence events were appended to `output/audit_trail.json`. Tickets 101, 102, and 103 were then marked `resolved` in `data/campus_customs_new.db`.

| Ticket | Final status | MCP evidence | Human approval/cash |
|---:|---|---|---|
| 101 | resolved | Size-S Bulldog Tee stock is 0; linked invoice 501 is open. | No payment needed for status resolution; cash change `$0.00`. |
| 102 | resolved | Chapel Street lease; rent `$2,400`; recorded due date `2026-09-02`, with a stale-date conflict flagged. | Rent payment requires human approval; none granted; cash change `$0.00`. |
| 103 | resolved | 8 size-M hoodies available for 20 requested; shortage 12; list price `$58`. | Discount requires human approval; none granted; cash change `$0.00`. |

The exact structured record is `output/resolved_tickets.json`. The updated expected/actual desk is `output/desk_tickets.html`; the resolution board is `output/resolved_board.html`; screenshots are in `output/resolved_screenshots/`. Final database verification: all three ticket statuses are `resolved`, checking balance is `$3,400.00`, payment rows are `0`, and the working copy matches the original after the reset baseline except for the intended ticket-status resolution writes.

The absence of payments is intentional: resolving a ticket did not constitute approval to spend money. Ticket 102’s rent and ticket 103’s discount required a named human approval and a specific authorized action; neither was provided. Ticket 101’s linked invoice was reviewed but not paid. Consequently, the exact cash change is `$0.00`, independently confirmed by `cash_accounts.balance = 3400.00` and an empty `payments` table.

Each agent now has its own role-specific prompt file: `backend/prompts/boss.md`, `inventory.md`, `accounting.md`, `facilities.md`, and `customer_service.md`. Shared typed data contracts are defined in `backend/models.py`, including `TeamDeps`, `AgentDecision`, `AuditEvent`, and `TicketToolResult`. The existing five-agent registration, mutual delegation, MCP lookup, and Portkey model configuration remain active.

## Problem 7 backend routes

`backend/main.py` now exposes six required FastAPI routes using the existing agent team and read-only MCP/database architecture:

| Route | Purpose | Safety behavior |
|---|---|---|
| `GET /health` | Reports service, provider, and model configuration. | No database access or mutation. |
| `GET /api/tickets` | Lists all open tickets from `data/campus_customs_new.db`. | SQLite opens in `mode=ro`; no writes. |
| `GET /api/tickets/{ticket_id}` | Returns verified evidence for ticket 101, 102, or 103 through its MCP tool. | Rejects unknown ticket IDs and never opens the database directly for ticket evidence. |
| `POST /api/tickets/{ticket_id}/evidence` | Invokes the ticket-specific MCP tool for an agent/UI caller. | Only the three approved open tickets are allowed. |
| `POST /agent` | Starts the Boss-led PydanticAI team with the requested ticket context. | Delegation limits and role prompts remain enforced; model calls use Portkey. |
| `POST /api/payments/propose` | Records a proposed payment request without executing it. | Returns 403 until `human_approved=true`; even then, it records a proposal only and never changes the database or cash. |

The remaining Problem 7 routes are:

| Route | Purpose | Safety behavior |
|---|---|---|
| `GET /api/agent/events` | Returns append-only agent, payment, and reset history from `output/audit_trail.json`. | Never deletes prior events. |
| `GET /api/cash/balance` | Reads the checking balance from the working copy. | Uses SQLite read-only mode. |
| `POST /api/payments/execute` | Executes a payment in the working copy after explicit named human approval. | Requires `human_approved=true` and `approved_by`; rejects amounts above the verified balance. The original database is never changed. |
| `POST /api/database/reset` | Restores `data/campus_customs_new.db` from the preserved original. | Does not modify `data/campus_customs.db`; reset is audited. |

HTTP verification: the Homework 5 app started successfully on a temporary port because port 8000 was occupied by the unrelated Lecture 7 backend. On port 8001, all MCP ticket routes, ticket listing, health, event history, balance, payment safety, and reset routes returned the expected responses. `/agent` now returns a clear `503` when Portkey credentials are absent instead of an unhandled `500`; with valid credentials it invokes the existing Boss-led team.

The Portkey diagnosis found that PydanticAI was sending a reasoning setting incompatible with function tools on the requested model over Chat Completions. `backend/agent.py` now sets the provider-specific `openai_reasoning_effort` to `none`. A real end-to-end HTTP test then returned `200` from `POST /agent` using `gpt-6-luna` through Portkey and the ticket-101 MCP tool; no model or tool mock was used.
