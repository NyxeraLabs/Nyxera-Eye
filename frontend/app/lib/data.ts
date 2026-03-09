import type { DeviceLocation, EventLocation, Finding } from "./types";

export const deviceLocations: DeviceLocation[] = [
  { id: "dev-1", name: "Acme Cam-7", ip: "198.51.100.10", lat: -31.4, lon: -64.2, severity: "high", country: "AR" },
  { id: "dev-2", name: "Edge RTSP Node", ip: "203.0.113.44", lat: 37.77, lon: -122.41, severity: "critical", country: "US" },
  { id: "dev-3", name: "Factory PLC", ip: "192.0.2.77", lat: 52.52, lon: 13.41, severity: "medium", country: "DE" },
  { id: "dev-4", name: "Power Gateway", ip: "203.0.113.50", lat: 35.68, lon: 139.69, severity: "low", country: "JP" },
];

export const eventLocations: EventLocation[] = [
  {
    id: "evt-1",
    title: "Secure -> Vulnerable",
    deviceId: "dev-2",
    lat: 37.77,
    lon: -122.41,
    severity: "critical",
    type: "state_change",
    timestamp: "2026-03-09T13:02:00Z",
  },
  {
    id: "evt-2",
    title: "Firmware Changed",
    deviceId: "dev-1",
    lat: -31.4,
    lon: -64.2,
    severity: "high",
    type: "vulnerability",
    timestamp: "2026-03-09T13:05:00Z",
  },
  {
    id: "evt-3",
    title: "Deception Signal",
    deviceId: "dev-3",
    lat: 52.52,
    lon: 13.41,
    severity: "medium",
    type: "deception",
    timestamp: "2026-03-09T13:08:00Z",
  },
  {
    id: "evt-4",
    title: "Vision Tag: Industrial Panel",
    deviceId: "dev-4",
    lat: 35.68,
    lon: 139.69,
    severity: "low",
    type: "vision",
    timestamp: "2026-03-09T13:10:00Z",
  },
];

export const findings: Finding[] = [
  {
    id: "f-1",
    title: "CVE-2026-1000 exploit exposure",
    description: "Device exposes vulnerable firmware with confirmed exploit availability.",
    severity: "critical",
    deviceId: "dev-2",
  },
  {
    id: "f-2",
    title: "Unsafe protocol surface",
    description: "Modbus service reachable with high exposure profile.",
    severity: "high",
    deviceId: "dev-3",
  },
  {
    id: "f-3",
    title: "State change reappearance",
    description: "Previously disappeared device has reappeared in monitored segment.",
    severity: "medium",
    deviceId: "dev-1",
  },
  {
    id: "f-4",
    title: "Vision intelligence update",
    description: "New industrial panel tag collected from latest snapshot processing.",
    severity: "low",
    deviceId: "dev-4",
  },
];
