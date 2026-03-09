import type { DeviceLocation, EventLocation, Finding, OpsFeed } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_NYXERA_API_BASE || "/api/nyxera";
const API_TOKEN = process.env.NEXT_PUBLIC_NYXERA_API_TOKEN || "";

function buildHeaders(): HeadersInit {
  return API_TOKEN ? { "X-API-Token": API_TOKEN } : {};
}

function normalizeSeverity(value: unknown): "critical" | "high" | "medium" | "low" {
  const v = String(value || "low").toLowerCase();
  if (v === "critical" || v === "high" || v === "medium" || v === "low") {
    return v;
  }
  return "low";
}

function normalizeDevices(input: unknown): DeviceLocation[] {
  if (!Array.isArray(input)) {
    return [];
  }
  return input.map((item, index) => {
    const record = item as Record<string, unknown>;
    return {
      id: String(record.device_id || record.id || `dev-${index}`),
      name: String(record.name || record.device_id || "Unknown device"),
      ip: String(record.ip || "0.0.0.0"),
      lat: Number(record.latitude ?? record.lat ?? 0),
      lon: Number(record.longitude ?? record.lon ?? 0),
      severity: normalizeSeverity(record.severity),
      country: String(record.country || "N/A"),
    };
  });
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

function normalizeFindings(input: unknown): Finding[] {
  if (!Array.isArray(input)) {
    return [];
  }
  return input.map((item, index) => {
    const record = item as Record<string, unknown>;
    return {
      id: String(record.id || `f-${index}`),
      title: String(record.title || "Finding"),
      description: String(record.description || "No description"),
      severity: normalizeSeverity(record.severity),
      deviceId: String(record.device_id || record.deviceId || "unknown"),
      status: String(record.status || "open"),
      actions: Array.isArray(record.actions) ? (record.actions as Array<Record<string, unknown>>) : [],
      updatedAt: String(record.updated_at || new Date().toISOString()),
    };
  });
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
        devicesByCountry: (metrics.devices_by_country as Record<string, number>) || {},
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
    const response = await fetch(
      `${API_BASE}/frontend/scan/start?batch_size=${batchSize}&interval_seconds=${intervalSeconds}`,
      {
        method: "POST",
        headers: buildHeaders(),
        cache: "no-store",
      }
    );
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
