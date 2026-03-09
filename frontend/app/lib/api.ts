import { deviceLocations, eventLocations, findings } from "./data";
import type { DeviceLocation, EventLocation, Finding, OpsFeed } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_NYXERA_API_BASE || "http://127.0.0.1:8000";
const API_TOKEN = process.env.NEXT_PUBLIC_NYXERA_API_TOKEN || "";

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
    };
  });
}

function fallbackFeed(): OpsFeed {
  return {
    generatedAt: new Date().toISOString(),
    devices: deviceLocations,
    events: eventLocations,
    findings,
    metrics: {
      queueDepth: 12,
      miningThroughput: 245.5,
      probeSuccessRate: 97.2,
      storageGrowthGb: 1.24,
    },
    source: "fallback",
  };
}

export async function fetchOpsFeed(): Promise<OpsFeed> {
  try {
    const response = await fetch(`${API_BASE}/frontend/ops-feed`, {
      headers: API_TOKEN ? { "X-API-Token": API_TOKEN } : {},
      cache: "no-store",
    });

    if (!response.ok) {
      return fallbackFeed();
    }

    const payload = (await response.json()) as Record<string, unknown>;

    return {
      generatedAt: String(payload.generated_at || new Date().toISOString()),
      devices: normalizeDevices(payload.devices),
      events: normalizeEvents(payload.events),
      findings: normalizeFindings(payload.findings),
      metrics: {
        queueDepth: Number((payload.metrics as Record<string, unknown> | undefined)?.queue_depth ?? 0),
        miningThroughput: Number((payload.metrics as Record<string, unknown> | undefined)?.mining_throughput ?? 0),
        probeSuccessRate: Number((payload.metrics as Record<string, unknown> | undefined)?.probe_success_rate ?? 0),
        storageGrowthGb: Number((payload.metrics as Record<string, unknown> | undefined)?.storage_growth_gb ?? 0),
      },
      source: "api",
    };
  } catch {
    return fallbackFeed();
  }
}
