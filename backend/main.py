"""FastAPI routes for the Campus Customs agent team and ticket desk."""

import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .agent import run_team
from .audit import append_event
from .mcp_client import lookup_ticket_evidence


app = FastAPI(title="Campus Customs Agent Team")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "campus_customs_new.db"
ORIGINAL_DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "campus_customs.db"
AUDIT_PATH = Path(__file__).resolve().parent.parent / "output" / "audit_trail.json"
OPEN_TICKETS = {101, 102, 103}


class AgentRequest(BaseModel):
    prompt: str
    ticket_id: int | None = None


class PaymentProposal(BaseModel):
    ticket_id: int = Field(ge=1)
    amount: float = Field(gt=0)
    purpose: str = Field(min_length=1)
    human_approved: bool = False
    approved_by: str | None = None


def append_audit(event: dict[str, object]) -> None:
    """Append one JSON event without replacing prior audit entries."""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        history = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    history.append({"timestamp": datetime.now(timezone.utc).isoformat(), **event})
    AUDIT_PATH.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "model": "gpt-6-luna", "provider": "Portkey"}


@app.get("/api/tickets")
async def open_tickets() -> dict[str, list[dict[str, object]]]:
    """List open tickets from the copied database without writing to it."""
    connection = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            "SELECT id, type, requester, subject, sku, size, qty, status, notes, created_at "
            "FROM tickets WHERE id IN (101, 102, 103) ORDER BY id"
        ).fetchall()
        return {"tickets": [dict(row) for row in rows]}
    finally:
        connection.close()


@app.get("/api/tickets/{ticket_id}")
async def ticket_detail(ticket_id: int) -> dict[str, object]:
    """Return the approved MCP evidence for one of the three open tickets."""
    if ticket_id not in OPEN_TICKETS:
        raise HTTPException(status_code=404, detail="No approved open ticket with that ID")
    return {"ticket_id": ticket_id, "source": "mcp", "evidence": json.loads(await lookup_ticket_evidence(ticket_id))}


@app.post("/api/tickets/{ticket_id}/evidence")
async def ticket_evidence(ticket_id: int) -> dict[str, object]:
    """Invoke the ticket-specific MCP tool for an agent or UI caller."""
    if ticket_id not in OPEN_TICKETS:
        raise HTTPException(status_code=404, detail="No approved open ticket with that ID")
    return {"ticket_id": ticket_id, "source": "mcp", "evidence": json.loads(await lookup_ticket_evidence(ticket_id))}


@app.post("/agent")
async def agent(request: AgentRequest) -> dict[str, str | int | None]:
    append_event({"event": "Boss started", "agent": "Boss", "ticket_id": request.ticket_id, "result": request.prompt[:240]})
    try:
        response = await run_team(request.prompt, request.ticket_id)
    except Exception as exc:
        # Keep missing provider credentials/configuration from becoming an opaque 500.
        raise HTTPException(
            status_code=503,
            detail="Agent service is unavailable; configure valid Portkey credentials before calling /agent.",
        ) from exc
    append_event({"event": "Boss summary", "agent": "Boss", "ticket_id": request.ticket_id, "result": response[:500]})
    return {"ticket_id": request.ticket_id, "response": response}


@app.post("/api/tickets/{ticket_id}/resolve")
async def resolve_ticket(ticket_id: int) -> dict[str, object]:
    """Mark one supported ticket resolved in the working copy only."""
    if ticket_id not in OPEN_TICKETS:
        raise HTTPException(status_code=404, detail="Unsupported ticket ID")
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        result = connection.execute(
            "UPDATE tickets SET status = 'resolved' WHERE id = ? AND status = 'open'",
            (ticket_id,),
        )
        connection.commit()
        if result.rowcount == 0:
            return {"ticket_id": ticket_id, "status": "already_resolved"}
        append_audit({"event": "ticket_resolved", "ticket_id": ticket_id, "result": "working_copy_only"})
        return {"ticket_id": ticket_id, "status": "resolved"}
    finally:
        connection.close()


@app.post("/api/payments/propose")
async def payment_proposal(request: PaymentProposal) -> dict[str, object]:
    """Create a non-executing proposal; only a human can approve payment."""
    if not request.human_approved:
        raise HTTPException(
            status_code=403,
            detail="Human payment approval is required; no payment was executed.",
        )
    return {
        "status": "approval_recorded",
        "executed": False,
        "ticket_id": request.ticket_id,
        "amount": request.amount,
        "purpose": request.purpose,
        "message": "Human approval was recorded as a proposal only. A separate authorized payment system must execute it.",
    }


@app.get("/api/agent/events")
async def agent_events() -> dict[str, list[dict[str, object]]]:
    """Return the append-only agent/payment/reset event history."""
    if not AUDIT_PATH.exists():
        return {"events": []}
    return {"events": json.loads(AUDIT_PATH.read_text(encoding="utf-8"))}


@app.get("/api/cash/balance")
async def cash_balance() -> dict[str, object]:
    """Read the current copied-database cash balance without changing it."""
    connection = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        row = connection.execute(
            "SELECT name, balance, date FROM cash_accounts WHERE name = 'checking'"
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Checking account not found")
        return dict(row)
    finally:
        connection.close()


@app.post("/api/payments/execute")
async def execute_payment(request: PaymentProposal) -> dict[str, object]:
    """Execute a payment only after named human approval and a sufficient balance."""
    if not request.human_approved or not request.approved_by:
        raise HTTPException(status_code=403, detail="Named human approval is required; no payment was executed.")
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        account = connection.execute(
            "SELECT balance FROM cash_accounts WHERE name = 'checking'"
        ).fetchone()
        if account is None:
            raise HTTPException(status_code=404, detail="Checking account not found")
        if request.amount > account["balance"]:
            raise HTTPException(status_code=409, detail="Payment exceeds the verified checking balance")
        next_id = connection.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM payments").fetchone()[0]
        paid_at = datetime.now(timezone.utc).isoformat()
        connection.execute(
            "INSERT INTO payments (id, kind, ref_id, amount, account, paid_at, approved_by) "
            "VALUES (?, 'ticket_payment', ?, ?, 'checking', ?, ?)",
            (next_id, request.ticket_id, request.amount, paid_at, request.approved_by),
        )
        connection.execute(
            "UPDATE cash_accounts SET balance = balance - ?, date = ? WHERE name = 'checking'",
            (request.amount, paid_at[:10]),
        )
        connection.commit()
        append_audit({
            "event": "payment_executed",
            "ticket_id": request.ticket_id,
            "amount": request.amount,
            "approved_by": request.approved_by,
            "result": "executed_in_copied_database_only",
        })
        return {"status": "executed", "payment_id": next_id, "approved_by": request.approved_by, "executed": True}
    finally:
        connection.close()


@app.post("/api/database/reset")
async def reset_database() -> dict[str, object]:
    """Restore the working copy from the preserved original database."""
    shutil.copy2(ORIGINAL_DATABASE_PATH, DATABASE_PATH)
    append_audit({"event": "database_reset", "source": str(ORIGINAL_DATABASE_PATH), "target": str(DATABASE_PATH)})
    return {"status": "reset", "database": "data/campus_customs_new.db", "original_preserved": True}
