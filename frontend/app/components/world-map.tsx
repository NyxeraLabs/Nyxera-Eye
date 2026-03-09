import type { DeviceLocation, EventLocation } from "../lib/types";

function toPercent(lat: number, lon: number) {
  const x = ((lon + 180) / 360) * 100;
  const y = ((90 - lat) / 180) * 100;
  return { x, y };
}

const severityRing: Record<string, string> = {
  critical: "ring-2 ring-rose-300",
  high: "ring-2 ring-orange-300",
  medium: "ring-2 ring-amber-300",
  low: "ring-2 ring-emerald-300",
};

export function WorldMap({ devices, events }: { devices: DeviceLocation[]; events: EventLocation[] }) {
  return (
    <div className="relative h-[420px] w-full overflow-hidden rounded-2xl border border-white/10 bg-[radial-gradient(circle_at_20%_20%,rgba(6,182,212,0.18),transparent_35%),radial-gradient(circle_at_70%_50%,rgba(250,204,21,0.13),transparent_35%),linear-gradient(180deg,rgba(15,23,42,0.92),rgba(2,6,23,0.96))]">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(148,163,184,0.07)_1px,transparent_1px),linear-gradient(to_bottom,rgba(148,163,184,0.07)_1px,transparent_1px)] bg-[size:40px_40px]" />

      {devices.map((device) => {
        const pos = toPercent(device.lat, device.lon);
        return (
          <div key={device.id} className="absolute" style={{ left: `${pos.x}%`, top: `${pos.y}%` }}>
            <div
              className={[
                "-translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-300/90 px-1.5 py-0.5 text-[10px] font-mono text-slate-900",
                severityRing[device.severity] || "",
              ].join(" ")}
            >
              D
            </div>
          </div>
        );
      })}

      {events.map((event) => {
        const pos = toPercent(event.lat, event.lon);
        return (
          <div key={event.id} className="absolute" style={{ left: `${pos.x}%`, top: `${pos.y}%` }}>
            <div className="-translate-x-1/2 -translate-y-1/2 rounded-full border border-fuchsia-200/80 bg-fuchsia-300/85 px-1.5 py-0.5 text-[10px] font-mono text-slate-900">
              E
            </div>
          </div>
        );
      })}

      <div className="absolute bottom-3 left-3 rounded-md border border-white/10 bg-slate-900/85 px-2 py-1 text-xs text-slate-300">
        D = Device · E = Event
      </div>
    </div>
  );
}
