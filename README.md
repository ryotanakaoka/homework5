# Campus Customs — Homework 5

Campus Customs is a ticket-resolution workspace with a read-only MCP evidence server, a five-agent PydanticAI team, a FastAPI backend, and a React/Vite/TypeScript dashboard. It includes the three supplied Campus Customs tickets, the working database copy, agent/audit reports, resolution artifacts, and screenshots required for the assignment.

## Submission structure

```text
Homework 5/
├── backend/                 # FastAPI routes and five PydanticAI agents
│   └── prompts/             # Shared policy plus one prompt per agent
├── data/
│   ├── campus_customs.db    # Preserved original database
│   └── campus_customs_new.db# Working database used by the app
├── frontend/                # React + Vite + TypeScript dashboard
├── mcp_server/              # Read-only MCP ticket tools
├── output/                  # Harness, audit, resolution, design, and screenshots
├── .mcp.json                # Vibe Coder MCP connection
├── .env.example             # Safe credential template
├── AI_prompts.md            # Actual prompt record for Problems 1–11
└── requirements.txt         # Python dependencies
```

Both database files are included for the assignment. The MCP server opens `campus_customs_new.db` read-only for evidence. Operational writes such as ticket resolution and approved payments affect only the working copy; the reset endpoint restores it from `campus_customs.db`.

## Requirements

- Python 3.11+ (Python 3.14 was used for verification)
- Node.js and npm
- A Portkey API key with access to `gpt-6-luna`

## Setup

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set a real `PORTKEY_API_KEY`. Never commit `.env` or paste its contents into a public repository.

Install the dashboard dependencies:

```bash
cd frontend
npm install
cd ..
```

## Startup

Start the backend from the Homework 5 directory:

```bash
source .venv/bin/activate
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

In a second terminal, start the dashboard:

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open <http://localhost:5173>. The dashboard connects to the backend at <http://localhost:8000>. CORS allows both `localhost:5173` and `127.0.0.1:5173`.

The MCP server can be launched independently with:

```bash
python3 mcp_server/server.py
```

## Database reset

To restore the working database to the preserved original state:

```bash
curl -X POST http://localhost:8000/api/database/reset
```

The endpoint copies `data/campus_customs.db` to `data/campus_customs_new.db`, records the reset in `output/audit_trail.json`, and never changes the original file. Use this before reproducing the ticket-resolution run.

## Verification

```bash
cd frontend
npm run build
cd ..
python3 -m py_compile backend/*.py mcp_server/server.py
sqlite3 data/campus_customs.db 'PRAGMA integrity_check;'
sqlite3 data/campus_customs_new.db 'PRAGMA integrity_check;'
```

The public submission includes `output/harness.md`, `output/audit_trail.json`, `output/mcp_smoke.json`, `output/resolved_tickets.json`, `output/desk_tickets.html`, `output/resolved_board.html`, `output/design.md`, and the screenshots under `output/resolved_screenshots/`.

## Public-repository safety checklist

- `.env` is ignored; only `.env.example` is included.
- Python caches, virtual environments, frontend dependencies, and generated bundles are ignored.
- API keys are not stored in source or output files.
- The two supplied database files are intentionally included as required by the assignment.
- Review `git status` and `git diff --cached` before pushing to a public repository.
