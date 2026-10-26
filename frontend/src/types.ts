export const HAZARD_TYPES = ["flood", "landslide"] as const;
export const SEVERITIES = ["low", "moderate", "high", "critical"] as const;
export const INCIDENT_STATUSES = ["reported", "active", "contained", "resolved"] as const;
export const ASSET_TYPES = ["rescue_team", "drone", "floodgate", "pump", "grid_node"] as const;
export const ASSET_STATUSES = ["available", "deployed", "maintenance", "offline"] as const;

export type HazardType = (typeof HAZARD_TYPES)[number];
export type Severity = (typeof SEVERITIES)[number];
export type IncidentStatus = (typeof INCIDENT_STATUSES)[number];
export type AssetType = (typeof ASSET_TYPES)[number];
export type AssetStatus = (typeof ASSET_STATUSES)[number];

export interface IncidentInput {
  title: string;
  description: string | null;
  hazard_type: HazardType;
  severity: Severity;
  status: IncidentStatus;
  district: string;
  latitude: number | null;
  longitude: number | null;
}

export interface Incident extends IncidentInput {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface AssetInput {
  name: string;
  asset_type: AssetType;
  status: AssetStatus;
  district: string;
  latitude: number | null;
  longitude: number | null;
  incident_id: number | null;
}

export interface Asset extends AssetInput {
  id: number;
  created_at: string;
  updated_at: string;
}
