import { FormEvent, useCallback, useEffect, useState } from "react";
import { api } from "../api";
import { INCIDENT_STATUSES, SEVERITIES, Incident, IncidentInput, IncidentStatus, Severity } from "../types";
import Modal from "./Modal";

const PAGE_SIZE = 20;

const emptyForm: IncidentInput = {
  title: "",
  description: null,
  disaster_type: "",
  severity: "low",
  status: "reported",
  region: "",
  latitude: null,
  longitude: null,
  affected_population: 0,
};

const numOrNull = (v: FormDataEntryValue | null) => (v === null || String(v).trim() === "" ? null : Number(v));
const strOrNull = (v: FormDataEntryValue | null) => (v === null || String(v).trim() === "" ? null : String(v).trim());

function IncidentForm({
  initial,
  onSave,
  onCancel,
}: {
  initial: IncidentInput;
  onSave: (v: IncidentInput) => Promise<void>;
  onCancel: () => void;
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const value: IncidentInput = {
      title: String(f.get("title")).trim(),
      description: strOrNull(f.get("description")),
      disaster_type: String(f.get("disaster_type")).trim(),
      severity: f.get("severity") as Severity,
      status: f.get("status") as IncidentStatus,
      region: String(f.get("region")).trim(),
      latitude: numOrNull(f.get("latitude")),
      longitude: numOrNull(f.get("longitude")),
      affected_population: Number(f.get("affected_population") || 0),
    };
    setBusy(true);
    setError("");
    try {
      await onSave(value);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed");
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="form">
      <label>Title<input name="title" required maxLength={200} defaultValue={initial.title} /></label>
      <label>Disaster type<input name="disaster_type" required maxLength={50} defaultValue={initial.disaster_type} /></label>
      <label>Region<input name="region" required maxLength={100} defaultValue={initial.region} /></label>
      <div className="row">
        <label>Severity
          <select name="severity" defaultValue={initial.severity}>
            {SEVERITIES.map((s) => <option key={s}>{s}</option>)}
          </select>
        </label>
        <label>Status
          <select name="status" defaultValue={initial.status}>
            {INCIDENT_STATUSES.map((s) => <option key={s}>{s}</option>)}
          </select>
        </label>
      </div>
      <div className="row">
        <label>Latitude<input name="latitude" type="number" step="any" min={-90} max={90} defaultValue={initial.latitude ?? ""} /></label>
        <label>Longitude<input name="longitude" type="number" step="any" min={-180} max={180} defaultValue={initial.longitude ?? ""} /></label>
      </div>
      <label>Affected population<input name="affected_population" type="number" min={0} step={1} defaultValue={initial.affected_population} /></label>
      <label>Description<textarea name="description" rows={3} maxLength={5000} defaultValue={initial.description ?? ""} /></label>
      {error && <div className="error" role="alert">{error}</div>}
      <div className="actions">
        <button type="button" className="btn" onClick={onCancel}>Cancel</button>
        <button className="btn primary" disabled={busy}>{busy ? "Saving…" : "Save"}</button>
      </div>
    </form>
  );
}

export default function IncidentsPage() {
  const [items, setItems] = useState<Incident[]>([]);
  const [region, setRegion] = useState("");
  const [severity, setSeverity] = useState("");
  const [status, setStatus] = useState("");
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState<Incident | "new" | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setItems(await api.listIncidents({ region: region.trim(), severity, status, skip: page * PAGE_SIZE, limit: PAGE_SIZE }));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load incidents");
    } finally {
      setLoading(false);
    }
  }, [region, severity, status, page]);

  useEffect(() => {
    void load();
  }, [load]);

  const save = async (value: IncidentInput) => {
    if (editing === "new") await api.createIncident(value);
    else if (editing) await api.updateIncident(editing.id, value);
    setEditing(null);
    await load();
  };

  const remove = async (i: Incident) => {
    if (!window.confirm(`Delete incident "${i.title}"? Linked resources will be unassigned.`)) return;
    try {
      await api.deleteIncident(i.id);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Delete failed");
    }
  };

  const resetPage = <T,>(setter: (v: T) => void) => (v: T) => {
    setter(v);
    setPage(0);
  };

  return (
    <section>
      <div className="toolbar">
        <input placeholder="Filter by region (exact)" value={region} onChange={(e) => resetPage(setRegion)(e.target.value)} />
        <select value={severity} onChange={(e) => resetPage(setSeverity)(e.target.value)}>
          <option value="">All severities</option>
          {SEVERITIES.map((s) => <option key={s}>{s}</option>)}
        </select>
        <select value={status} onChange={(e) => resetPage(setStatus)(e.target.value)}>
          <option value="">All statuses</option>
          {INCIDENT_STATUSES.map((s) => <option key={s}>{s}</option>)}
        </select>
        <span className="spacer" />
        <button className="btn primary" onClick={() => setEditing("new")}>+ New incident</button>
      </div>

      {error && <div className="error" role="alert">{error}</div>}

      <div className="card table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th><th>Title</th><th>Type</th><th>Region</th><th>Severity</th><th>Status</th>
              <th className="num">Affected</th><th>Updated</th><th />
            </tr>
          </thead>
          <tbody>
            {items.map((i) => (
              <tr key={i.id}>
                <td>{i.id}</td>
                <td>{i.title}</td>
                <td>{i.disaster_type}</td>
                <td>{i.region}</td>
                <td><span className={`badge sev-${i.severity}`}>{i.severity}</span></td>
                <td><span className="badge">{i.status}</span></td>
                <td className="num">{i.affected_population.toLocaleString()}</td>
                <td>{new Date(i.updated_at).toLocaleString()}</td>
                <td className="row-actions">
                  <button className="btn small" onClick={() => setEditing(i)}>Edit</button>
                  <button className="btn small danger" onClick={() => void remove(i)}>Delete</button>
                </td>
              </tr>
            ))}
            {!loading && items.length === 0 && (
              <tr><td colSpan={9} className="muted center">No incidents found.</td></tr>
            )}
            {loading && <tr><td colSpan={9} className="muted center">Loading…</td></tr>}
          </tbody>
        </table>
      </div>

      <div className="pager">
        <button className="btn small" disabled={page === 0} onClick={() => setPage(page - 1)}>Previous</button>
        <span>Page {page + 1}</span>
        <button className="btn small" disabled={items.length < PAGE_SIZE} onClick={() => setPage(page + 1)}>Next</button>
      </div>

      {editing && (
        <Modal title={editing === "new" ? "New incident" : `Edit incident #${editing.id}`} onClose={() => setEditing(null)}>
          <IncidentForm
            initial={editing === "new" ? emptyForm : editing}
            onSave={save}
            onCancel={() => setEditing(null)}
          />
        </Modal>
      )}
    </section>
  );
}
