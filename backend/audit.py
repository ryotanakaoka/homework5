"""Small append-only audit writer shared by routes and agents."""

import json
from datetime import datetime, timezone
from pathlib import Path


AUDIT_PATH = Path(__file__).resolve().parent.parent / "output" / "audit_trail.json"


def append_event(event: dict[str, object]) -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        history = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    history.append({"timestamp": datetime.now(timezone.utc).isoformat(), **event})
    AUDIT_PATH.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
