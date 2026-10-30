export const SEVERITIES = ["low", "moderate", "high", "critical"] as const;
export const INCIDENT_STATUSES = ["reported", "active", "contained", "resolved"] as const;
export const RESOURCE_STATUSES = ["available", "deployed", "maintenance"] as const;

export type Severity = (typeof SEVERITIES)[number];
export type IncidentStatus = (typeof INCIDENT_STATUSES)[number];
export type ResourceStatus = (typeof RESOURCE_STATUSES)[number];

export interface IncidentInput {
  title: string;
  description: string | null;
  disaster_type: string;
  severity: Severity;
  status: IncidentStatus;
  region: string;
  latitude: number | null;
  longitude: number | null;
  affected_population: number;
}

export interface Incident extends IncidentInput {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface ResourceInput {
  name: string;
  resource_type: string;
  quantity: number;
  status: ResourceStatus;
  location: string | null;
  incident_id: number | null;
}

export interface Resource extends ResourceInput {
  id: number;
  created_at: string;
  updated_at: string;
}
