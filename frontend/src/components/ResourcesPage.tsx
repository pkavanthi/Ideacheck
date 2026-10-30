import { FormEvent, useCallback, useEffect, useState } from "react";
import { api } from "../api";
import { RESOURCE_STATUSES, Resource, ResourceInput, ResourceStatus } from "../types";
import Modal from "./Modal";

const PAGE_SIZE = 20;

const emptyForm: ResourceInput = {
  name: "",
  resource_type: "",
  quantity: 1,
  status: "available",
  location: null,
  incident_id: null,
};

const strOrNull = (v: FormDataEntryValue | null) => (v === null || String(v).trim() === "" ? null : String(v).trim());

function ResourceForm({
  initial,
  onSave,
  onCancel,
}: {
  initial: ResourceInput;
  onSave: (v: ResourceInput) => Promise<void>;
  onCancel: () => void;
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const incident = strOrNull(f.get("incident_id"));
    const value: ResourceInput = {
      name: String(f.get("name")).trim(),
      resource_type: String(f.get("resource_type")).trim(),
      quantity: Number(f.get("quantity") || 0),
      status: f.get("status") as ResourceStatus,
      location: strOrNull(f.get("location")),
      incident_id: incident === null ? null : Number(incident),
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
      <label>Name<input name="name" required maxLength={200} defaultValue={initial.name} /></label>
      <label>Resource type<input name="resource_type" required maxLength={50} defaultValue={initial.resource_type} /></label>
      <div className="row">
        <label>Quantity<input name="quantity" type="number" min={0} step={1} defaultValue={initial.quantity} /></label>
        <label>Status
          <select name="status" defaultValue={initial.status}>
            {RESOURCE_STATUSES.map((s) => <option key={s}>{s}</option>)}
          </select>
        </label>
      </div>
      <label>Location<input name="location" maxLength={200} defaultValue={initial.location ?? ""} /></label>
      <label>Assigned incident ID<input name="incident_id" type="number" min={1} step={1} defaultValue={initial.incident_id ?? ""} /></label>
      {error && <div className="error" role="alert">{error}</div>}
      <div className="actions">
        <button type="button" className="btn" onClick={onCancel}>Cancel</button>
        <button className="btn primary" disabled={busy}>{busy ? "Saving…" : "Save"}</button>
      </div>
    </form>
  );
}

export default function ResourcesPage() {
  const [items, setItems] = useState<Resource[]>([]);
  const [resourceType, setResourceType] = useState("");
  const [status, setStatus] = useState("");
  const [incidentId, setIncidentId] = useState("");
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState<Resource | "new" | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setItems(
        await api.listResources({
          resource_type: resourceType.trim(),
          status,
          incident_id: incidentId.trim() === "" ? undefined : Number(incidentId),
          skip: page * PAGE_SIZE,
          limit: PAGE_SIZE,
        }),
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load resources");
    } finally {
      setLoading(false);
    }
  }, [resourceType, status, incidentId, page]);

  useEffect(() => {
    void load();
  }, [load]);

  const save = async (value: ResourceInput) => {
    if (editing === "new") await api.createResource(value);
    else if (editing) await api.updateResource(editing.id, value);
    setEditing(null);
    await load();
  };

  const remove = async (r: Resource) => {
    if (!window.confirm(`Delete resource "${r.name}"?`)) return;
    try {
      await api.deleteResource(r.id);
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
        <input placeholder="Filter by type (exact)" value={resourceType} onChange={(e) => resetPage(setResourceType)(e.target.value)} />
        <select value={status} onChange={(e) => resetPage(setStatus)(e.target.value)}>
          <option value="">All statuses</option>
          {RESOURCE_STATUSES.map((s) => <option key={s}>{s}</option>)}
        </select>
        <input
          type="number"
          min={1}
          placeholder="Incident ID"
          value={incidentId}
          onChange={(e) => resetPage(setIncidentId)(e.target.value)}
        />
        <span className="spacer" />
        <button className="btn primary" onClick={() => setEditing("new")}>+ New resource</button>
      </div>

      {error && <div className="error" role="alert">{error}</div>}

      <div className="card table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th><th>Name</th><th>Type</th><th className="num">Qty</th><th>Status</th>
              <th>Location</th><th>Incident</th><th>Updated</th><th />
            </tr>
          </thead>
          <tbody>
            {items.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.name}</td>
                <td>{r.resource_type}</td>
                <td className="num">{r.quantity.toLocaleString()}</td>
                <td><span className={`badge res-${r.status}`}>{r.status}</span></td>
                <td>{r.location ?? "—"}</td>
                <td>{r.incident_id ?? "—"}</td>
                <td>{new Date(r.updated_at).toLocaleString()}</td>
                <td className="row-actions">
                  <button className="btn small" onClick={() => setEditing(r)}>Edit</button>
                  <button className="btn small danger" onClick={() => void remove(r)}>Delete</button>
                </td>
              </tr>
            ))}
            {!loading && items.length === 0 && (
              <tr><td colSpan={9} className="muted center">No resources found.</td></tr>
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
        <Modal title={editing === "new" ? "New resource" : `Edit resource #${editing.id}`} onClose={() => setEditing(null)}>
          <ResourceForm
            initial={editing === "new" ? emptyForm : editing}
            onSave={save}
            onCancel={() => setEditing(null)}
          />
        </Modal>
      )}
    </section>
  );
}
