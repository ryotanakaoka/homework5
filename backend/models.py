"""Typed data contracts shared by the Campus Customs agent team."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class TeamDeps(BaseModel):
    depth: int = Field(default=0, ge=0, le=4)
    ticket_id: int | None = None


class AgentDecision(BaseModel):
    agent: str
    ticket_id: int | None = None
    evidence: list[str] = Field(default_factory=list)
    recommendation: str
    requires_human_approval: bool = False
    stop_reason: str | None = None


class AuditEvent(BaseModel):
    timestamp: str
    event: str
    agent: str | None = None
    tool_name: str | None = None
    ticket_id: int | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    result_summary: str = ""
    stop_reason: str | None = None
    safety_flags: list[str] = Field(default_factory=list)


class TicketToolResult(BaseModel):
    ticket_id: int
    tool_name: str
    data: dict[str, Any] = Field(default_factory=dict)
    verified: bool = False
    source_database: Literal["data/campus_customs_new.db"] = "data/campus_customs_new.db"
