import { FormEvent, useCallback, useEffect, useState } from "react";
import { api } from "./api";
import { Badge, Field, FilterSelect, fmtDate, Modal, Select, toNum } from "./components";
import { HAZARD_TYPES, INCIDENT_STATUSES, SEVERITIES } from "./types";
import type { Incident, IncidentInput } from "./types";

const EMPTY = {
  title: "",
  description: "",
  hazard_type: "flood",
  severity: "low",
  status: "reported",
  district: "",
  latitude: "",
  longitude: "",
} as const;

type FormState = { [K in keyof typeof EMPTY]: string };

function toForm(i: Incident): FormState {
  return {
    title: i.title,
    description: i.description ?? "",
    hazard_type: i.hazard_type,
    severity: i.severity,
    status: i.status,
    district: i.district,
    latitude: i.latitude?.toString() ?? "",
    longitude: i.longitude?.toString() ?? "",
  };
}

function toInput(f: FormState): IncidentInput {
  return {
    title: f.title.trim(),
    description: f.description.trim() || null,
    hazard_type: f.hazard_type as IncidentInput["hazard_type"],
    severity: f.severity as IncidentInput["severity"],
    status: f.status as IncidentInput["status"],
    district: f.district.trim(),
    latitude: toNum(f.latitude),
    longitude: toNum(f.longitude),
  };
}

function IncidentForm({ initial, onSaved, onCancel }: { initial: Incident | null; onSaved: () => void; onCancel: () => void }) {
  const [f, setF] = useState<FormState>(initial ? toForm(initial) : { ...EMPTY });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const set = (k: keyof FormState) => (v: string) => setF((p) => ({ ...p, [k]: v }));

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      if (initial) await api.updateIncident(initial.id, toInput(f));
      else await api.createIncident(toInput(f));
      onSaved();
    } catch (err) {
      setError((err as Error).message);
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit}>
      <Field name="Title">
        <input value={f.title} onChange={(e) => set("title")(e.target.value)} required minLength={3} maxLength={200} />
      </Field>
      <Field name="Description">
        <textarea value={f.description} onChange={(e) => set("description")(e.target.value)} maxLength={5000} rows={3} />
      </Field>
      <div className="row">
        <Field name="Hazard">
          <Select value={f.hazard_type} options={HAZARD_TYPES} onChange={set("hazard_type")} />
        </Field>
        <Field name="Severity">
          <Select value={f.severity} options={SEVERITIES} onChange={set("severity")} />
        </Field>
        <Field name="Status">
          <Select value={f.status} options={INCIDENT_STATUSES} onChange={set("status")} />
        </Field>
      </div>
      <Field name="District">
        <input value={f.district} onChange={(e) => set("district")(e.target.value)} required maxLength={120} />
      </Field>
      <div className="row">
        <Field name="Latitude">
          <input type="number" step="any" min={-90} max={90} value={f.latitude} onChange={(e) => set("latitude")(e.target.value)} />
        </Field>
        <Field name="Longitude">
          <input type="number" step="any" min={-180} max={180} value={f.longitude} onChange={(e) => set("longitude")(e.target.value)} />
        </Field>
      </div>
      {error && <p className="error">{error}</p>}
      <div className="actions">
        <button type="button" className="secondary" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" disabled={busy}>
          {initial ? "Save changes" : "Create incident"}
        </button>
      </div>
    </form>
  );
}

export default function IncidentsPage() {
  const [items, setItems] = useState<Incident[]>([]);
  const [filters, setFilters] = useState({ hazard_type: "", severity: "", status: "", district: "" });
  const [editing, setEditing] = useState<Incident | "new" | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setItems(await api.listIncidents({ ...filters, district: filters.district.trim() }));
      setError("");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    void load();
  }, [load]);

  async function remove(i: Incident) {
    if (!window.confirm(`Delete incident "${i.title}"? Assigned assets will be unassigned.`)) return;
    try {
      await api.deleteIncident(i.id);
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  const setFilter = (k: keyof typeof filters) => (v: string) => setFilters((p) => ({ ...p, [k]: v }));

  return (
    <section>
      <div className="toolbar">
        <FilterSelect placeholder="All hazards" value={filters.hazard_type} options={HAZARD_TYPES} onChange={setFilter("hazard_type")} />
        <FilterSelect placeholder="All severities" value={filters.severity} options={SEVERITIES} onChange={setFilter("severity")} />
        <FilterSelect placeholder="All statuses" value={filters.status} options={INCIDENT_STATUSES} onChange={setFilter("status")} />
        <input placeholder="District (exact)" value={filters.district} onChange={(e) => setFilter("district")(e.target.value)} />
        <button onClick={() => setEditing("new")}>+ New incident</button>
      </div>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Hazard</th>
            <th>Severity</th>
            <th>Status</th>
            <th>District</th>
            <th>Location</th>
            <th>Created</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {items.map((i) => (
            <tr key={i.id}>
              <td>{i.title}</td>
              <td>{i.hazard_type}</td>
              <td>
                <Badge value={i.severity} />
              </td>
              <td>
                <Badge value={i.status} />
              </td>
              <td>{i.district}</td>
              <td>{i.latitude != null && i.longitude != null ? `${i.latitude}, ${i.longitude}` : "—"}</td>
              <td>{fmtDate(i.created_at)}</td>
              <td className="row-actions">
                <button className="secondary" onClick={() => setEditing(i)}>
                  Edit
                </button>
                <button className="danger" onClick={() => remove(i)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
          {!loading && items.length === 0 && (
            <tr>
              <td colSpan={8} className="empty">
                No incidents found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
      {editing && (
        <Modal title={editing === "new" ? "New incident" : "Edit incident"} onClose={() => setEditing(null)}>
          <IncidentForm
            initial={editing === "new" ? null : editing}
            onCancel={() => setEditing(null)}
            onSaved={() => {
              setEditing(null);
              void load();
            }}
          />
        </Modal>
      )}
    </section>
  );
}
