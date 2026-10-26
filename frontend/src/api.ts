import type { Asset, AssetInput, Incident, IncidentInput } from "./types";

const BASE_URL: string = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const KEY_STORAGE = "aegisflow_api_key";

let apiKey = sessionStorage.getItem(KEY_STORAGE) ?? "";

export const hasApiKey = () => apiKey !== "";

export function setApiKey(key: string) {
  apiKey = key;
  sessionStorage.setItem(KEY_STORAGE, key);
}

export function clearApiKey() {
  apiKey = "";
  sessionStorage.removeItem(KEY_STORAGE);
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function formatDetail(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) => {
        const field = Array.isArray(d?.loc) ? d.loc.filter((p: unknown) => p !== "body").join(".") : "";
        return field ? `${field}: ${d?.msg}` : String(d?.msg ?? d);
      })
      .join("; ");
  }
  return "Request failed";
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      method,
      headers: {
        "X-API-Key": apiKey,
        ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError(0, `Cannot reach the backend at ${BASE_URL}`);
  }
  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      message = formatDetail((await res.json()).detail);
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(res.status, message);
  }
  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}

function query(params: Record<string, string | number | undefined>): string {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== "") q.set(k, String(v));
  }
  const s = q.toString();
  return s ? `?${s}` : "";
}

export const api = {
  listIncidents: (f: Record<string, string | undefined> = {}) =>
    request<Incident[]>("GET", `/api/incidents${query({ limit: 200, ...f })}`),
  createIncident: (b: IncidentInput) => request<Incident>("POST", "/api/incidents", b),
  updateIncident: (id: number, b: Partial<IncidentInput>) => request<Incident>("PATCH", `/api/incidents/${id}`, b),
  deleteIncident: (id: number) => request<void>("DELETE", `/api/incidents/${id}`),

  listAssets: (f: Record<string, string | undefined> = {}) =>
    request<Asset[]>("GET", `/api/assets${query({ limit: 200, ...f })}`),
  createAsset: (b: AssetInput) => request<Asset>("POST", "/api/assets", b),
  updateAsset: (id: number, b: Partial<AssetInput>) => request<Asset>("PATCH", `/api/assets/${id}`, b),
  deleteAsset: (id: number) => request<void>("DELETE", `/api/assets/${id}`),
};
