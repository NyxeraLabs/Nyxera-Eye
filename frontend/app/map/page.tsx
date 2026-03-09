/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import dynamic from "next/dynamic";
import { useState } from "react";

import { useOpsFeed } from "../lib/use-ops-feed";

const WorldMapLeaflet = dynamic(() => import("../components/world-map-leaflet"), { ssr: false });

export default function MapPage() {
  const [showDevices, setShowDevices] = useState(true);
  const [showEvents, setShowEvents] = useState(true);
  const { feed, isLoading } = useOpsFeed();

  return (
    <div className="flex flex-col gap-6 pb-20">
      <section className="rounded-2xl border border-emerald-300/20 bg-black/35 p-5">
        <h1 className="text-2xl font-bold text-emerald-100">World Map</h1>
        <p className="mt-1 text-sm text-slate-300">Live geolocation overlays for assets and events. Dark tactical rendering enabled.</p>
        <p className="mt-2 text-xs text-slate-400">Source: {feed?.source ?? "loading"} · Updated: {feed?.generatedAt ?? "-"}</p>
      </section>

      <section className="flex flex-wrap gap-2">
        <button
          onClick={() => setShowDevices((v) => !v)}
          className={[
            "rounded-md border px-3 py-2 text-xs uppercase tracking-[0.12em]",
            showDevices ? "border-emerald-300/70 bg-emerald-400/15 text-emerald-200" : "border-white/20 bg-white/5 text-slate-200",
          ].join(" ")}
        >
          {showDevices ? "Hide" : "Show"} Devices
        </button>
        <button
          onClick={() => setShowEvents((v) => !v)}
          className={[
            "rounded-md border px-3 py-2 text-xs uppercase tracking-[0.12em]",
            showEvents ? "border-cyan-300/70 bg-cyan-400/15 text-cyan-200" : "border-white/20 bg-white/5 text-slate-200",
          ].join(" ")}
        >
          {showEvents ? "Hide" : "Show"} Events
        </button>
      </section>

      {isLoading || !feed ? (
        <section className="rounded-2xl border border-white/10 bg-black/35 p-6 text-sm text-slate-300">Loading map intelligence...</section>
      ) : (
        <>
          <WorldMapLeaflet devices={feed.devices} events={feed.events} showDevices={showDevices} showEvents={showEvents} />

          <section className="grid gap-4 md:grid-cols-2">
            <article className="rounded-2xl border border-white/10 bg-black/35 p-4">
              <h2 className="font-semibold text-slate-100">Device Overlay</h2>
              <p className="mt-2 text-sm text-slate-300">{feed.devices.length} assets with severity-coded markers.</p>
            </article>
            <article className="rounded-2xl border border-white/10 bg-black/35 p-4">
              <h2 className="font-semibold text-slate-100">Event Overlay</h2>
              <p className="mt-2 text-sm text-slate-300">{feed.events.length} events with type and timestamp popups.</p>
            </article>
          </section>
        </>
      )}
    </div>
  );
}
