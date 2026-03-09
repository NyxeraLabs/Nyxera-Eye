export type Severity = "critical" | "high" | "medium" | "low";

export type DeviceLocation = {
  id: string;
  name: string;
  ip: string;
  lat: number;
  lon: number;
  severity: Severity;
  country: string;
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

export type Finding = {
  id: string;
  title: string;
  description: string;
  severity: Severity;
  deviceId: string;
};
