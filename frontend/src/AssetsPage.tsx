import { FormEvent, useCallback, useEffect, useState } from "react";
import { api } from "./api";
import { Badge, Field, FilterSelect, label, Modal, Select, toNum } from "./components";
import { ASSET_STATUSES, ASSET_TYPES } from "./types";
import type { Asset, AssetInput, Incident } from "./types";

const EMPTY = {
  name: "",
  asset_type: "rescue_team",
  status: "available",
  district: "",
  latitude: "",
  longitude: "",
  incident_id: "",
} as const;

type FormState = { [K in keyof typeof EMPTY]: string };

function toForm(a: Asset): FormState {
  return {
    name: a.name,
    asset_type: a.asset_type,
    status: a.status,
    district: a.district,
    latitude: a.latitude?.toString() ?? "",
    longitude: a.longitude?.toString() ?? "",
    incident_id: a.incident_id?.toString() ?? "",
  };
}

function toInput(f: FormState): AssetInput {
  return {
    name: f.name.trim(),
    asset_type: f.asset_type as AssetInput["asset_type"],
    status: f.status as AssetInput["status"],
    district: f.district.trim(),
    latitude: toNum(f.latitude),
    longitude: toNum(f.longitude),
    incident_id: toNum(f.incident_id),
  };
}

function AssetForm({
  initial,
  incidents,
  onSaved,
  onCancel,
}: {
  initial: Asset | null;
  incidents: Incident[];
  onSaved: () => void;
  onCancel: () => void;
}) {
  const [f, setF] = useState<FormState>(initial ? toForm(initial) : { ...EMPTY });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const set = (k: keyof FormState) => (v: string) => setF((p) => ({ ...p, [k]: v }));

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      if (initial) await api.updateAsset(initial.id, toInput(f));
      else await api.createAsset(toInput(f));
      onSaved();
    } catch (err) {
      setError((err as Error).message);
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit}>
      <Field name="Name">
        <input value={f.name} onChange={(e) => set("name")(e.target.value)} required minLength={2} maxLength={150} />
      </Field>
      <div className="row">
        <Field name="Type">
          <Select value={f.asset_type} options={ASSET_TYPES} onChange={set("asset_type")} />
        </Field>
        <Field name="Status">
          <Select value={f.status} options={ASSET_STATUSES} onChange={set("status")} />
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
      <Field name="Assigned incident">
        <select value={f.incident_id} onChange={(e) => set("incident_id")(e.target.value)}>
          <option value="">Unassigned</option>
          {incidents.map((i) => (
            <option key={i.id} value={i.id}>
              #{i.id} {i.title}
            </option>
          ))}
        </select>
      </Field>
      {error && <p className="error">{error}</p>}
      <div className="actions">
        <button type="button" className="secondary" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" disabled={busy}>
          {initial ? "Save changes" : "Create asset"}
        </button>
      </div>
    </form>
  );
}

export default function AssetsPage() {
  const [items, setItems] = useState<Asset[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [filters, setFilters] = useState({ asset_type: "", status: "", district: "", incident_id: "" });
  const [editing, setEditing] = useState<Asset | "new" | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [assets, incs] = await Promise.all([
        api.listAssets({ ...filters, district: filters.district.trim() }),
        api.listIncidents(),
      ]);
      setItems(assets);
      setIncidents(incs);
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

  async function remove(a: Asset) {
    if (!window.confirm(`Delete asset "${a.name}"?`)) return;
    try {
      await api.deleteAsset(a.id);
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  const setFilter = (k: keyof typeof filters) => (v: string) => setFilters((p) => ({ ...p, [k]: v }));
  const incidentTitle = (id: number | null) => {
    if (id == null) return "—";
    const i = incidents.find((x) => x.id === id);
    return i ? `#${i.id} ${i.title}` : `#${id}`;
  };

  return (
    <section>
      <div className="toolbar">
        <FilterSelect placeholder="All types" value={filters.asset_type} options={ASSET_TYPES} onChange={setFilter("asset_type")} />
        <FilterSelect placeholder="All statuses" value={filters.status} options={ASSET_STATUSES} onChange={setFilter("status")} />
        <select value={filters.incident_id} onChange={(e) => setFilter("incident_id")(e.target.value)} aria-label="Incident">
          <option value="">All incidents</option>
          {incidents.map((i) => (
            <option key={i.id} value={i.id}>
              #{i.id} {i.title}
            </option>
          ))}
        </select>
        <input placeholder="District (exact)" value={filters.district} onChange={(e) => setFilter("district")(e.target.value)} />
        <button onClick={() => setEditing("new")}>+ New asset</button>
      </div>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Status</th>
            <th>District</th>
            <th>Location</th>
            <th>Incident</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {items.map((a) => (
            <tr key={a.id}>
              <td>{a.name}</td>
              <td>{label(a.asset_type)}</td>
              <td>
                <Badge value={a.status} />
              </td>
              <td>{a.district}</td>
              <td>{a.latitude != null && a.longitude != null ? `${a.latitude}, ${a.longitude}` : "—"}</td>
              <td>{incidentTitle(a.incident_id)}</td>
              <td className="row-actions">
                <button className="secondary" onClick={() => setEditing(a)}>
                  Edit
                </button>
                <button className="danger" onClick={() => remove(a)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
          {!loading && items.length === 0 && (
            <tr>
              <td colSpan={7} className="empty">
                No assets found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
      {editing && (
        <Modal title={editing === "new" ? "New asset" : "Edit asset"} onClose={() => setEditing(null)}>
          <AssetForm
            initial={editing === "new" ? null : editing}
            incidents={incidents}
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
