"use client";

import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import type { DeviceLocation, EventLocation } from "../lib/types";

const severityColor: Record<string, string> = {
  critical: "#fb7185",
  high: "#fb923c",
  medium: "#facc15",
  low: "#4ade80",
};

type Props = {
  devices: DeviceLocation[];
  events: EventLocation[];
  showDevices?: boolean;
  showEvents?: boolean;
};

export default function WorldMapLeaflet({
  devices,
  events,
  showDevices = true,
  showEvents = true,
}: Props) {
  return (
    <div className="overflow-hidden rounded-2xl border border-white/10">
      <MapContainer
        center={[18, 5]}
        zoom={2}
        minZoom={2}
        style={{ height: "440px", width: "100%" }}
        scrollWheelZoom
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {showDevices &&
          devices.map((device) => (
            <CircleMarker
              key={device.id}
              center={[device.lat, device.lon]}
              radius={7}
              pathOptions={{
                color: severityColor[device.severity] || "#38bdf8",
                fillColor: severityColor[device.severity] || "#38bdf8",
                fillOpacity: 0.85,
                weight: 2,
              }}
            >
              <Popup>
                <div className="space-y-1 text-sm">
                  <p><strong>Device:</strong> {device.name}</p>
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
                color: "#e879f9",
                fillColor: "#e879f9",
                fillOpacity: 0.85,
                weight: 2,
                dashArray: "3 2",
              }}
            >
              <Popup>
                <div className="space-y-1 text-sm">
                  <p><strong>Event:</strong> {event.title}</p>
                  <p><strong>Type:</strong> {event.type}</p>
                  <p><strong>Device:</strong> {event.deviceId}</p>
                  <p><strong>Severity:</strong> {event.severity.toUpperCase()}</p>
                  <p><strong>Timestamp:</strong> {event.timestamp}</p>
                </div>
              </Popup>
            </CircleMarker>
          ))}
      </MapContainer>
    </div>
  );
}
