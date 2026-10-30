import type { Incident, IncidentInput, Resource, ResourceInput } from "./types";

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

let apiKey = "";
let onUnauthorized: () => void = () => {};

export function configureApi(key: string, unauthorizedHandler: () => void) {
  apiKey = key;
  onUnauthorized = unauthorizedHandler;
}

function describeDetail(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) => {
        const field = Array.isArray(d?.loc) ? d.loc.filter((p: unknown) => p !== "body").join(".") : "";
        return field ? `${field}: ${d?.msg}` : String(d?.msg ?? "Invalid input");
      })
      .join("; ");
  }
  return "Request failed";
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: { "X-API-Key": apiKey, "Content-Type": "application/json" },
    });
  } catch {
    throw new ApiError(0, "Cannot reach the server");
  }
  if (res.status === 401) {
    onUnauthorized();
    throw new ApiError(401, "Invalid or missing API key");
  }
  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      message = describeDetail((await res.json()).detail);
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(res.status, message);
  }
  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}

function qs(params: Record<string, string | number | undefined>): string {
  const sp = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== "") sp.set(k, String(v));
  });
  const s = sp.toString();
  return s ? `?${s}` : "";
}

const json = (body: unknown) => JSON.stringify(body);

export const api = {
  listIncidents: (p: { region?: string; severity?: string; status?: string; skip?: number; limit?: number }) =>
    request<Incident[]>(`/api/incidents${qs(p)}`),
  createIncident: (body: IncidentInput) =>
    request<Incident>("/api/incidents", { method: "POST", body: json(body) }),
  updateIncident: (id: number, body: Partial<IncidentInput>) =>
    request<Incident>(`/api/incidents/${id}`, { method: "PATCH", body: json(body) }),
  deleteIncident: (id: number) => request<void>(`/api/incidents/${id}`, { method: "DELETE" }),

  listResources: (p: { resource_type?: string; status?: string; incident_id?: number; skip?: number; limit?: number }) =>
    request<Resource[]>(`/api/resources${qs(p)}`),
  createResource: (body: ResourceInput) =>
    request<Resource>("/api/resources", { method: "POST", body: json(body) }),
  updateResource: (id: number, body: Partial<ResourceInput>) =>
    request<Resource>(`/api/resources/${id}`, { method: "PATCH", body: json(body) }),
  deleteResource: (id: number) => request<void>(`/api/resources/${id}`, { method: "DELETE" }),
};
