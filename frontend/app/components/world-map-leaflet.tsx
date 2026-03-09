"use client";

import { CircleMarker, MapContainer, Popup, TileLayer } from "react-leaflet";
import type { DeviceLocation, EventLocation } from "../lib/types";

const severityColor: Record<string, string> = {
  critical: "#ef4444",
  high: "#f97316",
  medium: "#eab308",
  low: "#22c55e",
};

type Props = {
  devices: DeviceLocation[];
  events: EventLocation[];
  showDevices?: boolean;
  showEvents?: boolean;
};

export default function WorldMapLeaflet({ devices, events, showDevices = true, showEvents = true }: Props) {
  return (
    <div className="overflow-hidden rounded-2xl border border-emerald-300/15 shadow-[0_0_0_1px_rgba(16,185,129,0.2),0_24px_70px_rgba(2,6,23,0.7)]">
      <MapContainer center={[18, 5]} zoom={2} minZoom={2} style={{ height: "460px", width: "100%" }} scrollWheelZoom>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />

        {showDevices &&
          devices.map((device) => (
            <CircleMarker
              key={device.id}
              center={[device.lat, device.lon]}
              radius={7}
              pathOptions={{
                color: severityColor[device.severity] || "#14b8a6",
                fillColor: severityColor[device.severity] || "#14b8a6",
                fillOpacity: 0.9,
                weight: 2,
              }}
            >
              <Popup>
                <div className="space-y-1 text-sm">
                  <p><strong>Asset:</strong> {device.name}</p>
                  <p><strong>IP:</strong> {device.ip}</p>
                  <p><strong>Country:</strong> {device.country}</p>
                  <p><strong>Severity:</strong> {device.severity.toUpperCase()}</p>
                </div>
              </Popup>
            </CircleMarker>
          ))}

        {showEvents &&
          events.map((event) => (
            <CircleMarker
              key={event.id}
              center={[event.lat, event.lon]}
              radius={5}
              pathOptions={{
                color: "#22d3ee",
                fillColor: "#22d3ee",
                fillOpacity: 0.9,
                weight: 2,
                dashArray: "2 2",
              }}
            >
              <Popup>
                <div className="space-y-1 text-sm">
                  <p><strong>Event:</strong> {event.title}</p>
                  <p><strong>Type:</strong> {event.type}</p>
                  <p><strong>Device:</strong> {event.deviceId}</p>
                  <p><strong>Severity:</strong> {event.severity.toUpperCase()}</p>
                  <p><strong>Time:</strong> {event.timestamp}</p>
                </div>
              </Popup>
            </CircleMarker>
          ))}
      </MapContainer>
    </div>
  );
}
