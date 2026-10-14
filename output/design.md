# Campus Customs Operations Dashboard

## Direction

The dashboard is designed as a calm, high-trust operations desk: a Yale-adjacent navy foundation, warm gold action accent, generous white panels, and restrained green status signals. The interface keeps the operational questions visible—what ticket is selected, what the agents found, and what a human is approving—without turning the screen into a dense admin table.

## Layout and interaction

- The top bar establishes system identity and shows the live `localhost:8000` connection.
- The hero area states the job of the desk and makes the human-in-the-loop payment guardrail prominent.
- Three summary cards expose open-ticket count, checking balance, and recent activity at a glance.
- The left queue lists all three tickets; the selected ticket gets a gold inset edge and a detailed workspace on the right.
- The detail workspace separates agent execution, resolution, and payment approval into explicit actions.
- The activity panel polls the append-only audit endpoint every five seconds, filters events to the selected ticket, and shows the individual agent name, action, and returned summary for each delegation/MCP step.
- The guardrail panel makes the system boundaries visible: MCP evidence, human approval, and working-copy writes.

## Visual system

- Navy `#102f4e` anchors navigation and primary actions.
- Soft blue surfaces communicate verified evidence and active selection.
- Gold `#c8903e` is reserved for payment approval and the selected-ticket marker.
- Green indicates a healthy connection or resolved state; amber indicates open work.
- DM Sans provides readable UI text; DM Mono is used for IDs, labels, and technical connection details.
- Cards use 8–12px corners, thin cool-gray borders, and minimal shadows so hierarchy comes from spacing and typography.

## API behavior

The Vite app calls `http://localhost:8000` directly. The backend permits both `http://localhost:5173` and the equivalent loopback origin `http://127.0.0.1:5173` through CORS. It uses `GET /api/tickets`, the ticket-specific MCP evidence routes, `POST /agent`, `GET /api/agent/events`, `GET /api/cash/balance`, `POST /api/tickets/{id}/resolve`, and the human-approved payment endpoint. The dashboard never talks to SQLite directly.

## Verification

The production build passes with `npm run build`. The dashboard was served with Vite on port 5173 and checked against the FastAPI backend on port 8000; CORS and the live ticket/agent/balance flows were exercised over HTTP.
