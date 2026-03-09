/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

import type {
  AuthUser,
  DeviceLocation,
  EventLocation,
  Finding,
  FrontendSettings,
  OpsFeed,
  PagedResult,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_NYXERA_API_BASE || "/api/nyxera";
const ENV_API_TOKEN = process.env.NEXT_PUBLIC_NYXERA_API_TOKEN || "";

function getStoredToken(): string {
  if (typeof window === "undefined") {
    return ENV_API_TOKEN;
  }
  return window.localStorage.getItem("nyxera_api_token") || ENV_API_TOKEN;
}

export function setStoredToken(token: string): void {
  if (typeof window === "undefined") {
    return;
  }
  if (token) {
    window.localStorage.setItem("nyxera_api_token", token);
    return;
  }
  window.localStorage.removeItem("nyxera_api_token");
}

function buildHeaders(jsonBody: boolean = false): HeadersInit {
  const token = getStoredToken();
  const headers: HeadersInit = {};
  if (token) {
    headers["X-API-Token"] = token;
  }
  if (jsonBody) {
    headers["Content-Type"] = "application/json";
  }
  return headers;
}

function normalizeSeverity(value: unknown): "critical" | "high" | "medium" | "low" {
  const v = String(value || "low").toLowerCase();
  if (v === "critical" || v === "high" || v === "medium" || v === "low") {
    return v;
  }
  return "low";
}

function normalizeEvents(input: unknown): EventLocation[] {
  if (!Array.isArray(input)) {
    return [];
  }
  return input.map((item, index) => {
    const record = item as Record<string, unknown>;
    const rawType = String(record.type || "state_change");
    const type = ["state_change", "deception", "vision", "vulnerability"].includes(rawType)
      ? (rawType as EventLocation["type"])
      : "state_change";
    return {
      id: String(record.id || `evt-${index}`),
      title: String(record.title || "Event"),
      deviceId: String(record.device_id || record.deviceId || "unknown"),
      lat: Number(record.lat ?? record.latitude ?? 0),
      lon: Number(record.lon ?? record.longitude ?? 0),
      severity: normalizeSeverity(record.severity),
      type,
      timestamp: String(record.timestamp || new Date().toISOString()),
    };
  });
}

function normalizeDevices(input: unknown): DeviceLocation[] {
  if (!Array.isArray(input)) {
    return [];
  }
  return input.map((item, index) => normalizeDevice(item, `dev-${index}`));
}

function normalizeDevice(input: unknown, fallbackId: string = "device"): DeviceLocation {
  const record = (input as Record<string, unknown>) || {};
  const findingRecord = record.finding as Record<string, unknown> | undefined;
  return {
    id: String(record.device_id || record.id || fallbackId),
    name: String(record.name || record.device_id || "Unknown device"),
    ip: String(record.ip || "0.0.0.0"),
    lat: Number(record.latitude ?? record.lat ?? 0),
    lon: Number(record.longitude ?? record.lon ?? 0),
    severity: normalizeSeverity(record.severity),
    country: String(record.country || "N/A"),
    services: Array.isArray(record.services)
      ? (record.services as Array<Record<string, unknown>>).map((service) => ({
          port: Number(service.port ?? 0),
          protocol: String(service.protocol || "tcp"),
          service: String(service.service || "unknown"),
          banner: String(service.banner || ""),
        }))
      : [],
    fingerprints:
      record.fingerprints && typeof record.fingerprints === "object"
        ? {
            faviconHash: String((record.fingerprints as Record<string, unknown>).favicon_hash || ""),
            httpServer: String((record.fingerprints as Record<string, unknown>).http_server || ""),
            htmlTitle: String((record.fingerprints as Record<string, unknown>).html_title || ""),
            htmlMetadata:
              ((record.fingerprints as Record<string, unknown>).html_metadata as Record<string, string> | undefined) || {},
          }
        : null,
    iotMetadata:
      record.iot_metadata && typeof record.iot_metadata === "object"
        ? {
            vendor: String((record.iot_metadata as Record<string, unknown>).vendor || ""),
            model: String((record.iot_metadata as Record<string, unknown>).model || ""),
            firmware: String((record.iot_metadata as Record<string, unknown>).firmware || ""),
          }
        : null,
    firstSeen: String(record.first_seen || ""),
    lastSeen: String(record.last_seen || ""),
    lastUpdated: String(record.last_updated || ""),
    scanCount: Number(record.scan_count ?? 0),
    finding: findingRecord ? normalizeFinding(findingRecord) : null,
    events: normalizeEvents(record.events),
  };
}

function normalizeFindings(input: unknown): Finding[] {
  if (!Array.isArray(input)) {
    return [];
  }
  return input.map((item, index) => normalizeFinding(item, `f-${index}`));
}

function normalizeFinding(input: unknown, fallbackId: string = "finding"): Finding {
  const record = (input as Record<string, unknown>) || {};
  const deviceRecord = record.device as Record<string, unknown> | undefined;
  return {
    id: String(record.id || fallbackId),
    title: String(record.title || "Finding"),
    description: String(record.description || "No description"),
    severity: normalizeSeverity(record.severity),
    deviceId: String(record.device_id || record.deviceId || "unknown"),
    status: String(record.status || "open"),
    actions: Array.isArray(record.actions)
      ? (record.actions as Array<Record<string, unknown>>).map((actionItem) => ({
          action: String(actionItem.action || "unknown"),
          at: String(actionItem.at || new Date().toISOString()),
        }))
      : [],
    updatedAt: String(record.updated_at || new Date().toISOString()),
    device: deviceRecord ? normalizeDevice(deviceRecord) : null,
  };
}

function buildQuery(params: Record<string, string | number | undefined>): string {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === "" || Number.isNaN(value)) {
      continue;
    }
    query.set(key, String(value));
  }
  const encoded = query.toString();
  return encoded ? `?${encoded}` : "";
}

export async function registerUser(username: string, password: string, role: string = "analyst"): Promise<AuthUser | null> {
  try {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: buildHeaders(true),
      body: JSON.stringify({ username, password, role }),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    const payload = (await response.json()) as Record<string, unknown>;
    const token = String(payload.token || "");
    if (!token) {
      return null;
    }
    setStoredToken(token);
    return { username: String(payload.username || username), role: String(payload.role || role), token };
  } catch {
    return null;
  }
}

export async function loginUser(username: string, password: string): Promise<AuthUser | null> {
  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: buildHeaders(true),
      body: JSON.stringify({ username, password }),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    const payload = (await response.json()) as Record<string, unknown>;
    const token = String(payload.token || "");
    if (!token) {
      return null;
    }
    setStoredToken(token);
    return { username: String(payload.username || username), role: String(payload.role || "analyst"), token };
  } catch {
    return null;
  }
}

export async function fetchCurrentUser(): Promise<AuthUser | null> {
  const token = getStoredToken();
  if (!token) {
    return null;
  }
  try {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    const payload = (await response.json()) as Record<string, unknown>;
    return { username: String(payload.username || "unknown"), role: String(payload.role || "analyst"), token };
  } catch {
    return null;
  }
}

export async function logoutUser(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/auth/logout`, {
      method: "POST",
      headers: buildHeaders(),
      cache: "no-store",
    });
    setStoredToken("");
    return response.ok;
  } catch {
    setStoredToken("");
    return false;
  }
}

export async function fetchOpsFeed(): Promise<OpsFeed | null> {
  try {
    const response = await fetch(`${API_BASE}/frontend/ops-feed`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }

    const payload = (await response.json()) as Record<string, unknown>;
    const metrics = (payload.metrics as Record<string, unknown> | undefined) || {};
    return {
      generatedAt: String(payload.generated_at || new Date().toISOString()),
      devices: normalizeDevices(payload.devices),
      events: normalizeEvents(payload.events),
      findings: normalizeFindings(payload.findings),
      metrics: {
        queueDepth: Number(metrics.queue_depth ?? 0),
        miningThroughput: Number(metrics.mining_throughput ?? 0),
        probeSuccessRate: Number(metrics.probe_success_rate ?? 0),
        storageGrowthGb: Number(metrics.storage_growth_gb ?? 0),
        scanRuns: Number(metrics.scan_runs ?? 0),
        findingsBySeverity: (metrics.findings_by_severity as Record<string, number>) || {},
        findingsByStatus: (metrics.findings_by_status as Record<string, number>) || {},
        devicesByCountry: (metrics.devices_by_country as Record<string, number>) || {},
        devicesByVendor: (metrics.devices_by_vendor as Record<string, number>) || {},
        servicesByPort: (metrics.services_by_port as Record<string, number>) || {},
        scanHistory: Array.isArray(metrics.scan_history)
          ? (metrics.scan_history as Array<{ run: number; timestamp: string; devices: number; findings: number; events: number }>)
          : [],
        scanLoopRunning: Boolean(metrics.scan_loop_running ?? false),
        scanLoopBatchSize: Number(metrics.scan_loop_batch_size ?? 0),
        scanLoopIntervalSeconds: Number(metrics.scan_loop_interval_seconds ?? 0),
      },
      source: String(payload.source || "api-runtime"),
    };
  } catch {
    return null;
  }
}

export async function fetchDevices(params: {
  q?: string;
  severity?: string;
  country?: string;
  vendor?: string;
  limit?: number;
  offset?: number;
} = {}): Promise<PagedResult<DeviceLocation>> {
  try {
    const response = await fetch(`${API_BASE}/frontend/devices${buildQuery(params)}`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return { items: [], total: 0, offset: 0, limit: params.limit || 100 };
    }
    const payload = (await response.json()) as Record<string, unknown>;
    return {
      items: normalizeDevices(payload.items),
      total: Number(payload.total ?? 0),
      offset: Number(payload.offset ?? 0),
      limit: Number(payload.limit ?? params.limit ?? 100),
    };
  } catch {
    return { items: [], total: 0, offset: 0, limit: params.limit || 100 };
  }
}

export async function fetchDevice(deviceId: string): Promise<DeviceLocation | null> {
  try {
    const response = await fetch(`${API_BASE}/frontend/devices/${encodeURIComponent(deviceId)}`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    const payload = (await response.json()) as Record<string, unknown>;
    return normalizeDevice(payload.device, deviceId);
  } catch {
    return null;
  }
}

export async function fetchFindings(params: {
  q?: string;
  severity?: string;
  status?: string;
  deviceId?: string;
  limit?: number;
  offset?: number;
} = {}): Promise<PagedResult<Finding>> {
  const apiParams = {
    q: params.q,
    severity: params.severity,
    status: params.status,
    device_id: params.deviceId,
    limit: params.limit,
    offset: params.offset,
  };
  try {
    const response = await fetch(`${API_BASE}/frontend/findings${buildQuery(apiParams)}`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return { items: [], total: 0, offset: 0, limit: params.limit || 100 };
    }
    const payload = (await response.json()) as Record<string, unknown>;
    return {
      items: normalizeFindings(payload.items),
      total: Number(payload.total ?? 0),
      offset: Number(payload.offset ?? 0),
      limit: Number(payload.limit ?? params.limit ?? 100),
    };
  } catch {
    return { items: [], total: 0, offset: 0, limit: params.limit || 100 };
  }
}

export async function fetchFinding(findingId: string): Promise<Finding | null> {
  try {
    const response = await fetch(`${API_BASE}/frontend/findings/${encodeURIComponent(findingId)}`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    const payload = (await response.json()) as Record<string, unknown>;
    return normalizeFinding(payload.finding, findingId);
  } catch {
    return null;
  }
}

export async function fetchSettings(): Promise<FrontendSettings | null> {
  try {
    const response = await fetch(`${API_BASE}/frontend/settings`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    const payload = (await response.json()) as Record<string, unknown>;
    const settings = (payload.settings as Record<string, unknown>) || {};
    return {
      runtimeMode: String(settings.runtime_mode || "passive"),
      scanDefaultBatchSize: Number(settings.scan_default_batch_size || 96),
      scanDefaultIntervalSeconds: Number(settings.scan_default_interval_seconds || 10),
      autoStartScanLoop: Boolean(settings.auto_start_scan_loop || false),
      authorizedScopeReference: String(settings.authorized_scope_reference || ""),
    };
  } catch {
    return null;
  }
}

export async function updateSettings(settings: FrontendSettings): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/frontend/settings`, {
      method: "PUT",
      headers: buildHeaders(true),
      body: JSON.stringify({
        runtime_mode: settings.runtimeMode,
        scan_default_batch_size: settings.scanDefaultBatchSize,
        scan_default_interval_seconds: settings.scanDefaultIntervalSeconds,
        auto_start_scan_loop: settings.autoStartScanLoop,
        authorized_scope_reference: settings.authorizedScopeReference,
      }),
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  }
}

export async function fetchAuditEvents(limit: number = 200): Promise<AuditEvent[]> {
  try {
    const response = await fetch(`${API_BASE}/audit/events?limit=${Math.max(1, Math.min(limit, 2000))}`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return [];
    }
    const payload = (await response.json()) as Record<string, unknown>;
    const events = (payload.events as Array<Record<string, unknown>>) || [];
    return events.map((event) => ({
      id: String(event.id || ""),
      timestamp: String(event.timestamp || ""),
      actor: String(event.actor || "unknown"),
      action: String(event.action || "unknown"),
      status: String(event.status || "unknown"),
      method: String(event.method || ""),
      path: String(event.path || ""),
      ip: String(event.ip || ""),
      details: (event.details as Record<string, unknown>) || {},
    }));
  } catch {
    return [];
  }
}

export async function triggerScan(batchSize: number = 96): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/frontend/scan?batch_size=${batchSize}`, {
      method: "POST",
      headers: buildHeaders(),
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  }
}

export async function startScanLoop(batchSize: number = 96, intervalSeconds: number = 10): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/frontend/scan/start?batch_size=${batchSize}&interval_seconds=${intervalSeconds}`, {
      method: "POST",
      headers: buildHeaders(),
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  }
}

export async function stopScanLoop(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/frontend/scan/stop`, {
      method: "POST",
      headers: buildHeaders(),
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  }
}

export async function performFindingAction(findingId: string, action: string): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/frontend/findings/${findingId}/action?action=${encodeURIComponent(action)}`, {
      method: "POST",
      headers: buildHeaders(),
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  }
}

export async function exportFinding(findingId: string): Promise<Record<string, unknown> | null> {
  try {
    const response = await fetch(`${API_BASE}/frontend/findings/${findingId}/export`, {
      headers: buildHeaders(),
      cache: "no-store",
    });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as Record<string, unknown>;
  } catch {
    return null;
  }
}

export type AuditEvent = {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  status: string;
  method: string;
  path: string;
  ip: string;
  details: Record<string, unknown>;
};
