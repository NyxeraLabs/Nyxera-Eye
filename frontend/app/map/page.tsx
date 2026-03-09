"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import { deviceLocations, eventLocations } from "../lib/data";

const WorldMapLeaflet = dynamic(() => import("../components/world-map-leaflet"), { ssr: false });

export default function MapPage() {
  const [showDevices, setShowDevices] = useState(true);
  const [showEvents, setShowEvents] = useState(true);

  return (
    <div className="flex flex-col gap-6 pb-16">
      <section className="rounded-2xl border border-white/10 bg-slate-950/55 p-5">
        <h1 className="text-2xl font-bold">World Map</h1>
        <p className="mt-1 text-sm text-slate-300">Interactive Leaflet map with separate device and event overlays.</p>
      </section>

      <section className="flex flex-wrap gap-2">
        <button
          onClick={() => setShowDevices((v) => !v)}
          className={[
            "rounded-md border px-3 py-2 text-xs",
            showDevices ? "border-cyan-300/60 bg-cyan-300/15 text-cyan-200" : "border-white/20 bg-white/5 text-slate-200",
          ].join(" ")}
        >
          {showDevices ? "Hide" : "Show"} Devices
        </button>
        <button
          onClick={() => setShowEvents((v) => !v)}
          className={[
            "rounded-md border px-3 py-2 text-xs",
            showEvents ? "border-fuchsia-300/60 bg-fuchsia-300/15 text-fuchsia-200" : "border-white/20 bg-white/5 text-slate-200",
          ].join(" ")}
        >
          {showEvents ? "Hide" : "Show"} Events
        </button>
      </section>

      <WorldMapLeaflet devices={deviceLocations} events={eventLocations} showDevices={showDevices} showEvents={showEvents} />

      <section className="grid gap-4 md:grid-cols-2">
        <article className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
          <h2 className="font-semibold">Device Overlay</h2>
          <p className="mt-2 text-sm text-slate-300">Severity-colored circles with device detail popups.</p>
        </article>
        <article className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
          <h2 className="font-semibold">Event Overlay</h2>
          <p className="mt-2 text-sm text-slate-300">Event markers include type, severity, linked device, and timestamp.</p>
        </article>
      </section>
    </div>
  );
}
