import { useCallback, useEffect, useMemo, useState, type FormEvent } from "react";
import { createRoot } from "react-dom/client";
import { Activity, ArrowUpRight, CheckCircle2, CircleDollarSign, Clock3, Database, Loader2, Play, RefreshCw, ShieldCheck, Sparkles, Ticket, Wallet } from "lucide-react";
import "./styles.css";

const API = "http://localhost:8000";
type Ticket = { id: number; type: string; requester: string; subject: string; sku?: string; size?: string; qty?: number; status: string; notes: string; created_at: string };
type Event = { timestamp: string; event: string; agent?: string; ticket_id?: number; result?: string; summary?: string; prompt?: string; request?: string };

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, { headers: { "Content-Type": "application/json" }, ...options });
  if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.detail || `Request failed (${response.status})`); }
  return response.json();
}

function App() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selected, setSelected] = useState(101);
  const [events, setEvents] = useState<Event[]>([]);
  const [balance, setBalance] = useState(0);
  const [agentResult, setAgentResult] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("Connected to the local agent desk.");
  const [payment, setPayment] = useState({ amount: "", purpose: "", approver: "" });

  const refresh = useCallback(async () => {
    try {
      const [ticketData, eventData, balanceData] = await Promise.all([api<{ tickets: Ticket[] }>("/api/tickets"), api<{ events: Event[] }>("/api/agent/events"), api<{ balance: number }>("/api/cash/balance")]);
      setTickets(ticketData.tickets); setEvents(eventData.events.slice(-30).reverse()); setBalance(balanceData.balance); setMessage("Live data refreshed");
    } catch (error) { setMessage(error instanceof Error ? error.message : "Unable to reach backend"); }
  }, []);

  useEffect(() => { refresh(); const timer = window.setInterval(refresh, 5000); return () => window.clearInterval(timer); }, [refresh]);
  const ticket = useMemo(() => tickets.find((item) => item.id === selected), [tickets, selected]);
  const ticketEvents = events.filter((event) => event.ticket_id === selected);

  async function runAgent() {
    if (!ticket) return; setBusy(true); setAgentResult(""); setMessage(`Boss is coordinating ticket ${ticket.id}…`);
    try { const result = await api<{ response: string }>("/agent", { method: "POST", body: JSON.stringify({ ticket_id: ticket.id, prompt: `Review ticket ${ticket.id}. Use the approved MCP evidence, delegate to the right specialists, and give a concise safe recommendation.` }) }); setAgentResult(result.response); setMessage("Agent run completed"); await refresh(); }
    catch (error) { setMessage(error instanceof Error ? error.message : "Agent run failed"); } finally { setBusy(false); }
  }

  async function resolve() { if (!ticket) return; setBusy(true); try { await api(`/api/tickets/${ticket.id}/resolve`, { method: "POST" }); setMessage(`Ticket ${ticket.id} marked resolved in the working database`); await refresh(); } catch (error) { setMessage(error instanceof Error ? error.message : "Resolve failed"); } finally { setBusy(false); } }
  async function approvePayment(event: FormEvent) { event.preventDefault(); setBusy(true); try { await api("/api/payments/execute", { method: "POST", body: JSON.stringify({ ticket_id: selected, amount: Number(payment.amount), purpose: payment.purpose, human_approved: true, approved_by: payment.approver }) }); setMessage("Payment executed in the working database and logged"); setPayment({ amount: "", purpose: "", approver: "" }); await refresh(); } catch (error) { setMessage(error instanceof Error ? error.message : "Payment failed"); } finally { setBusy(false); } }

  return <div className="app-shell">
    <header className="topbar"><div className="brand"><div className="brand-mark">CC</div><div><div className="eyebrow">CAMPUS CUSTOMS</div><h1>Operations desk</h1></div></div><div className="connection"><span className="pulse" /> Backend online <code>localhost:8000</code><button className="icon-button" onClick={refresh} title="Refresh"><RefreshCw size={16} /></button></div></header>
    <main className="main"><section className="hero"><div><p className="eyebrow gold">TICKET COMMAND CENTER</p><h2>Make the next right move.</h2><p className="hero-copy">Coordinate agents, protect approvals, and keep every decision tied to verified Campus Customs records.</p></div><div className="hero-badge"><ShieldCheck size={20} /><span>Human-in-the-loop<br /><strong>payments protected</strong></span></div></section>
      <div className="stats"><div className="stat"><Ticket size={19} /><div><span>Open tickets</span><strong>{tickets.filter((item) => item.status === "open").length} <small>/ {tickets.length}</small></strong></div></div><div className="stat"><Wallet size={19} /><div><span>Checking balance</span><strong>${balance.toLocaleString()}</strong></div></div><div className="stat"><Activity size={19} /><div><span>Recent activity</span><strong>{events.length} <small>events</small></strong></div></div></div>
      <div className="workspace"><section className="tickets-panel panel"><div className="panel-heading"><div><p className="eyebrow">QUEUE</p><h3>Three open tickets</h3></div><span className="live-tag"><span className="pulse" /> LIVE</span></div><div className="ticket-list">{tickets.map((item) => <button key={item.id} className={`ticket-card ${item.id === selected ? "selected" : ""}`} onClick={() => { setSelected(item.id); setAgentResult(""); }}><div className="ticket-top"><span className="ticket-id">#{item.id}</span><span className={`status ${item.status}`}>{item.status}</span></div><strong>{item.subject}</strong><span className="requester">{item.requester}</span><span className="ticket-note">{item.notes}</span><ArrowUpRight size={17} className="arrow" /></button>)}</div></section>
        <section className="detail panel">{ticket ? <><div className="detail-head"><div><p className="eyebrow">SELECTED TICKET · #{ticket.id}</p><h3>{ticket.subject}</h3><p className="muted">{ticket.requester} · {ticket.type.replace("_", " ")}</p></div><span className={`status large ${ticket.status}`}>{ticket.status}</span></div><div className="facts-grid"><div><span>SKU</span><strong>{ticket.sku || "—"}</strong></div><div><span>Size</span><strong>{ticket.size || "—"}</strong></div><div><span>Quantity</span><strong>{ticket.qty ?? "—"}</strong></div></div><div className="action-row"><button className="primary" disabled={busy || ticket.status !== "open"} onClick={runAgent}>{busy ? <Loader2 className="spin" size={17} /> : <Play size={17} />} Run agent team</button><button className="secondary" disabled={busy || ticket.status !== "open"} onClick={resolve}><CheckCircle2 size={17} /> Mark resolved</button></div>{agentResult && <div className="agent-result"><div className="result-label"><Sparkles size={16} /> Agent summary</div><p>{agentResult}</p></div>}<div className="payment-box"><div className="section-title"><CircleDollarSign size={18} /><div><h4>Human-approved payment</h4><p>Only execute against the working database after a named human approves.</p></div></div><form onSubmit={approvePayment}><input required type="number" min="0.01" step="0.01" placeholder="Amount" value={payment.amount} onChange={(e) => setPayment({ ...payment, amount: e.target.value })} /><input required placeholder="Purpose" value={payment.purpose} onChange={(e) => setPayment({ ...payment, purpose: e.target.value })} /><input required placeholder="Approver name" value={payment.approver} onChange={(e) => setPayment({ ...payment, approver: e.target.value })} /><button className="approve" disabled={busy}><ShieldCheck size={16} /> Approve & execute</button></form></div></> : <div className="empty">No ticket selected.</div>}</section>
      </div><div className="lower-grid"><section className="activity panel"><div className="panel-heading"><div><p className="eyebrow">AUDIT TRAIL</p><h3>Live agent activity</h3></div><Clock3 size={18} className="muted" /></div><div className="activity-list">{ticketEvents.length ? ticketEvents.map((event, index) => <div className="activity-item" key={`${event.timestamp}-${index}`}><span className="activity-dot" /><div><strong>{event.event.replaceAll("_", " ")}</strong><p>{event.result || event.prompt || `Ticket ${event.ticket_id ?? "system"}`}</p><time>{new Date(event.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</time></div></div>) : <p className="empty">Run the selected ticket to see its activity here.</p>}</div></section><section className="guardrail panel"><div className="panel-heading"><div><p className="eyebrow">GUARDRAILS</p><h3>Operational confidence</h3></div><Database size={18} className="muted" /></div><div className="guard"><ShieldCheck size={18} /><div><strong>Read-only evidence</strong><span>Agents use the approved MCP ticket tools.</span></div></div><div className="guard"><CircleDollarSign size={18} /><div><strong>Payment approval</strong><span>Every payment requires a named human and balance check.</span></div></div><div className="guard"><Database size={18} /><div><strong>Working copy</strong><span>Operational writes never touch the original database.</span></div></div></section></div>
    </main><footer><span>Campus Customs · Agent operations</span><span>{message}</span></footer>
  </div>;
}

export default App;

createRoot(document.getElementById("root")!).render(<App />);
