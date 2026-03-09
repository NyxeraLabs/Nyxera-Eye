/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { fetchSettings } from "./lib/api";
import { useOpsFeed } from "./lib/use-ops-feed";

type BarItem = {
  label: string;
  count: number;
  width: number;
  tone: string;
};

function buildBars(source: Record<string, number>, colors: string[]): BarItem[] {
  const items = Object.entries(source).map(([label, count], index) => ({
    label,
    count: Number(count),
    tone: colors[index % colors.length],
  }));
  const max = Math.max(1, ...items.map((item) => item.count));
  return items
    .sort((a, b) => b.count - a.count)
    .map((item) => ({ ...item, width: (item.count / max) * 100 }));
}

export default function DashboardPage() {
  const { feed, isLoading, error, runScan, scanLoopStart, scanLoopStop } = useOpsFeed();
  const [scanStatus, setScanStatus] = useState<string>("");
  const [loopInterval, setLoopInterval] = useState<number>(10);
  const [loopBatch, setLoopBatch] = useState<number>(96);
  const [deviceQuery, setDeviceQuery] = useState<string>("");

  useEffect(() => {
    fetchSettings().then((settings) => {
      if (!settings) {
        return;
      }
      setLoopBatch(settings.scanDefaultBatchSize);
      setLoopInterval(settings.scanDefaultIntervalSeconds);
    });
  }, []);

  const severityBars = useMemo(
    () => buildBars(feed?.metrics.findingsBySeverity || {}, ["bg-rose-500", "bg-orange-500", "bg-amber-400", "bg-emerald-500"]),
    [feed],
  );
  const statusBars = useMemo(
    () => buildBars(feed?.metrics.findingsByStatus || {}, ["bg-cyan-400", "bg-violet-400", "bg-emerald-500", "bg-rose-500", "bg-slate-400"]),
    [feed],
  );
  const vendorBars = useMemo(() => buildBars(feed?.metrics.devicesByVendor || {}, ["bg-cyan-400", "bg-sky-500", "bg-indigo-500"]), [feed]);
  const portBars = useMemo(() => buildBars(feed?.metrics.servicesByPort || {}, ["bg-emerald-500", "bg-lime-500", "bg-teal-500"]), [feed]);
  const countryBars = useMemo(() => buildBars(feed?.metrics.devicesByCountry || {}, ["bg-cyan-400", "bg-sky-400", "bg-blue-500"]), [feed]);

  const historyPoints = useMemo(() => {
    if (!feed || feed.metrics.scanHistory.length === 0) {
      return "";
    }
    const list = feed.metrics.scanHistory;
    const maxY = Math.max(1, ...list.map((x) => x.devices));
    const width = 420;
    const height = 120;
    return list
      .map((item, index) => {
        const x = (index / Math.max(1, list.length - 1)) * width;
        const y = height - (item.devices / maxY) * height;
        return `${x},${y}`;
      })
      .join(" ");
  }, [feed]);

  const filteredDevices = useMemo(() => {
    if (!feed) {
      return [];
    }
    const query = deviceQuery.trim().toLowerCase();
    const items = [...feed.devices].sort((a, b) => (b.scanCount || 0) - (a.scanCount || 0));
    if (!query) {
      return items.slice(0, 10);
    }
    return items
      .filter((device) =>
        [device.name, device.ip, device.country, device.iotMetadata?.vendor || "", device.iotMetadata?.model || ""]
          .join(" ")
          .toLowerCase()
          .includes(query),
      )
      .slice(0, 12);
  }, [deviceQuery, feed]);

  const handleScan = async () => {
    setScanStatus("Running single scan...");
    const ok = await runScan(128);
    setScanStatus(ok ? "Single scan completed." : "Single scan failed.");
  };

  const handleLoopToggle = async () => {
    if (feed?.metrics.scanLoopRunning) {
      setScanStatus("Stopping scan loop...");
      const ok = await scanLoopStop();
      setScanStatus(ok ? "Scan loop stopped." : "Failed to stop scan loop.");
      return;
    }

    setScanStatus("Starting scan loop...");
    const ok = await scanLoopStart(loopBatch, loopInterval);
    setScanStatus(ok ? "Scan loop started." : "Failed to start scan loop.");
  };

  if (isLoading || !feed) {
    return <section className="rounded-2xl border border-white/10 bg-black/30 p-6 text-sm text-slate-300">Loading operations feed...</section>;
  }

  return (
    <div className="flex flex-col gap-6 pb-20">
      <section className="rounded-2xl border border-emerald-400/20 bg-black/35 p-6 shadow-[0_0_0_1px_rgba(16,185,129,0.18),0_30px_80px_rgba(2,6,23,0.7)] backdrop-blur">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-emerald-300">Nyxera Ops Dashboard</p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight text-emerald-100 sm:text-4xl">Accumulated Asset Intelligence</h1>
            <p className="mt-2 text-sm text-slate-300">Single scans and scan loops now build a persistent live inventory instead of resetting the view each run.</p>
            <p className="mt-2 text-xs text-slate-400">Source: {feed.source} · Updated: {feed.generatedAt}</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <input
              type="number"
              min={1}
              value={loopBatch}
              onChange={(e) => setLoopBatch(Number(e.target.value || 1))}
              className="w-24 rounded-md border border-white/20 bg-slate-900/80 px-2 py-1 text-xs text-slate-100"
              aria-label="Loop batch size"
            />
            <input
              type="number"
              min={1}
              value={loopInterval}
              onChange={(e) => setLoopInterval(Number(e.target.value || 1))}
              className="w-24 rounded-md border border-white/20 bg-slate-900/80 px-2 py-1 text-xs text-slate-100"
              aria-label="Loop interval"
            />
            <button
              onClick={handleScan}
              className="rounded-md border border-cyan-300/60 bg-cyan-300/15 px-3 py-2 text-xs uppercase tracking-[0.12em] text-cyan-200"
            >
              Single Scan
            </button>
            <button
              onClick={handleLoopToggle}
              className={[
                "rounded-md border px-3 py-2 text-xs uppercase tracking-[0.12em]",
                feed.metrics.scanLoopRunning
                  ? "border-rose-300/60 bg-rose-300/15 text-rose-200"
                  : "border-emerald-300/60 bg-emerald-300/15 text-emerald-200",
              ].join(" ")}
            >
              {feed.metrics.scanLoopRunning ? "Stop Scan Loop" : "Start Scan Loop"}
            </button>
          </div>
        </div>
        {scanStatus ? <p className="mt-2 text-xs text-cyan-300">{scanStatus}</p> : null}
        <p className="mt-1 text-xs text-slate-400">
          Loop status: {feed.metrics.scanLoopRunning ? "RUNNING" : "STOPPED"} · Batch: {feed.metrics.scanLoopBatchSize} · Interval:{" "}
          {feed.metrics.scanLoopIntervalSeconds}s
        </p>
        {error ? <p className="mt-2 text-xs text-rose-300">{error}</p> : null}
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-6">
        {[
          { label: "Assets", value: feed.devices.length },
          { label: "Findings", value: feed.findings.length },
          { label: "Events", value: feed.events.length },
          { label: "Queue", value: feed.metrics.queueDepth },
          { label: "Throughput", value: feed.metrics.miningThroughput.toFixed(1) },
          { label: "Scan Runs", value: feed.metrics.scanRuns },
        ].map((card) => (
          <article key={card.label} className="rounded-xl border border-emerald-300/15 bg-slate-950/70 p-4">
            <p className="text-xs uppercase tracking-[0.15em] text-emerald-300">{card.label}</p>
            <p className="mt-2 text-3xl font-bold text-emerald-100">{card.value}</p>
          </article>
        ))}
      </section>

      <section className="grid gap-4 xl:grid-cols-2">
        <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
          <h2 className="text-lg font-semibold text-slate-100">Asset Growth Trend</h2>
          <div className="mt-4 rounded-lg border border-white/10 bg-slate-950/60 p-3">
            <svg viewBox="0 0 420 120" className="h-32 w-full">
              <polyline fill="none" stroke="#22d3ee" strokeWidth="3" points={historyPoints} />
            </svg>
          </div>
          <p className="mt-2 text-xs text-slate-400">Device inventory after each scan run. Repeated loops should trend upward until the pool is fully covered.</p>
        </article>

        <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold text-slate-100">Device Query</h2>
              <p className="mt-1 text-sm text-slate-400">Search devices by IP, vendor, model, or country.</p>
            </div>
            <Link href="/devices" className="rounded-md border border-cyan-300/40 px-3 py-2 text-xs text-cyan-200">
              Full Device Registry
            </Link>
          </div>
          <input
            value={deviceQuery}
            onChange={(e) => setDeviceQuery(e.target.value)}
            placeholder="Search devices..."
            className="mt-4 w-full rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none"
          />
          <div className="mt-4 space-y-3">
            {filteredDevices.map((device) => (
              <div key={device.id} className="rounded-xl border border-white/10 bg-slate-950/65 p-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-semibold text-slate-100">{device.name}</p>
                    <p className="text-xs text-slate-400">
                      {device.ip} · {device.country} · {device.iotMetadata?.vendor || "Unknown vendor"}
                    </p>
                  </div>
                  <Link href={`/devices/${device.id}`} className="rounded-md border border-emerald-300/40 px-3 py-2 text-xs text-emerald-200">
                    Investigate
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="grid gap-4 lg:grid-cols-2 xl:grid-cols-4">
        {[
          { title: "Findings by Severity", items: severityBars },
          { title: "Findings by Status", items: statusBars },
          { title: "Devices by Vendor", items: vendorBars },
          { title: "Services by Port", items: portBars },
        ].map((group) => (
          <article key={group.title} className="rounded-2xl border border-white/10 bg-black/35 p-5">
            <h2 className="text-lg font-semibold text-slate-100">{group.title}</h2>
            <div className="mt-4 space-y-3">
              {group.items.map((bar) => (
                <div key={bar.label}>
                  <div className="mb-1 flex items-center justify-between text-xs uppercase tracking-[0.12em] text-slate-300">
                    <span>{bar.label}</span>
                    <span>{bar.count}</span>
                  </div>
                  <div className="h-2 rounded-full bg-slate-800">
                    <div className={`${bar.tone} h-2 rounded-full`} style={{ width: `${bar.width}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </article>
        ))}
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold text-slate-100">Hot Assets</h2>
              <p className="mt-1 text-sm text-slate-400">Most recently updated devices with direct investigation links.</p>
            </div>
            <Link href="/findings" className="rounded-md border border-amber-300/40 px-3 py-2 text-xs text-amber-200">
              Full Findings Registry
            </Link>
          </div>
          <div className="mt-4 overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="text-xs uppercase tracking-[0.12em] text-slate-400">
                <tr>
                  <th className="pb-3">Device</th>
                  <th className="pb-3">Vendor</th>
                  <th className="pb-3">Severity</th>
                  <th className="pb-3">Scans</th>
                  <th className="pb-3">Updated</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {[...feed.devices]
                  .sort((a, b) => (b.scanCount || 0) - (a.scanCount || 0))
                  .slice(0, 10)
                  .map((device) => (
                    <tr key={device.id}>
                      <td className="py-3">
                        <Link href={`/devices/${device.id}`} className="font-semibold text-emerald-100 hover:text-cyan-200">
                          {device.name}
                        </Link>
                        <p className="text-xs text-slate-400">{device.ip}</p>
                      </td>
                      <td className="py-3 text-slate-300">{device.iotMetadata?.vendor || "-"}</td>
                      <td className="py-3 text-slate-300">{device.severity}</td>
                      <td className="py-3 text-slate-300">{device.scanCount || 0}</td>
                      <td className="py-3 text-slate-300">{device.lastUpdated || "-"}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
          <h2 className="text-lg font-semibold text-slate-100">Country Coverage</h2>
          <div className="mt-4 space-y-3">
            {countryBars.map((bar) => (
              <div key={bar.label}>
                <div className="mb-1 flex items-center justify-between text-xs uppercase tracking-[0.12em] text-slate-300">
                  <span>{bar.label}</span>
                  <span>{bar.count}</span>
                </div>
                <div className="h-2 rounded-full bg-slate-800">
                  <div className={`${bar.tone} h-2 rounded-full`} style={{ width: `${bar.width}%` }} />
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 rounded-xl border border-white/10 bg-slate-950/70 p-4">
            <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Probe Success</p>
            <p className="mt-2 text-3xl font-bold text-cyan-100">{feed.metrics.probeSuccessRate.toFixed(1)}%</p>
            <p className="mt-1 text-sm text-slate-400">Storage growth: {feed.metrics.storageGrowthGb.toFixed(3)} GB</p>
          </div>
        </article>
      </section>
    </div>
  );
}
