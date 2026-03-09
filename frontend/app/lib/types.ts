/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

export type Severity = "critical" | "high" | "medium" | "low";

export type AssetService = {
  port: number;
  protocol: string;
  service: string;
  banner: string;
};

export type AssetFingerprint = {
  faviconHash: string;
  httpServer: string;
  htmlTitle: string;
  htmlMetadata: Record<string, string>;
};

export type AssetIoTMetadata = {
  vendor: string;
  model: string;
  firmware: string;
};

export type FindingAction = {
  action: string;
  at: string;
};

export type Finding = {
  id: string;
  title: string;
  description: string;
  severity: Severity;
  deviceId: string;
  status: string;
  actions: FindingAction[];
  updatedAt: string;
  device?: DeviceLocation | null;
};

export type EventLocation = {
  id: string;
  title: string;
  deviceId: string;
  lat: number;
  lon: number;
  severity: Severity;
  type: "state_change" | "deception" | "vision" | "vulnerability";
  timestamp: string;
};

export type DeviceLocation = {
  id: string;
  name: string;
  ip: string;
  lat: number;
  lon: number;
  severity: Severity;
  country: string;
  city?: string;
  services?: AssetService[];
  fingerprints?: AssetFingerprint | null;
  iotMetadata?: AssetIoTMetadata | null;
  firstSeen?: string;
  lastSeen?: string;
  lastUpdated?: string;
  scanCount?: number;
  finding?: Finding | null;
  events?: EventLocation[];
};

export type OpsMetrics = {
  queueDepth: number;
  miningThroughput: number;
  probeSuccessRate: number;
  storageGrowthGb: number;
  scanRuns: number;
  findingsBySeverity: Record<string, number>;
  findingsByStatus: Record<string, number>;
  devicesByCountry: Record<string, number>;
  devicesByVendor: Record<string, number>;
  servicesByPort: Record<string, number>;
  scanHistory: Array<{ run: number; timestamp: string; devices: number; findings: number; events: number }>;
  scanLoopRunning: boolean;
  scanLoopBatchSize: number;
  scanLoopIntervalSeconds: number;
};

export type OpsFeed = {
  generatedAt: string;
  devices: DeviceLocation[];
  events: EventLocation[];
  findings: Finding[];
  metrics: OpsMetrics;
  source: string;
};

export type AuthUser = {
  username: string;
  role: string;
  token: string;
};

export type FrontendSettings = {
  runtimeMode: string;
  scanDefaultBatchSize: number;
  scanDefaultIntervalSeconds: number;
  autoStartScanLoop: boolean;
  authorizedScopeReference: string;
};

export type PagedResult<T> = {
  items: T[];
  total: number;
  offset: number;
  limit: number;
};
