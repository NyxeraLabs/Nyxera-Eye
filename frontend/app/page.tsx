"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchSettings } from "./lib/api";
import { useOpsFeed } from "./lib/use-ops-feed";

export default function DashboardPage() {
  const { feed, isLoading, error, runScan, scanLoopStart, scanLoopStop } = useOpsFeed();
  const [scanStatus, setScanStatus] = useState<string>("");
  const [loopInterval, setLoopInterval] = useState<number>(10);
  const [loopBatch, setLoopBatch] = useState<number>(96);

  useEffect(() => {
    fetchSettings().then((settings) => {
      if (!settings) {
        return;
      }
      setLoopBatch(settings.scanDefaultBatchSize);
      setLoopInterval(settings.scanDefaultIntervalSeconds);
    });
  }, []);

  const severityBars = useMemo(() => {
    if (!feed) {
      return [] as Array<{ level: string; count: number; width: number }>;
    }
    const entries = ["critical", "high", "medium", "low"].map((level) => ({
      level,
      count: Number(feed.metrics.findingsBySeverity[level] || 0),
    }));
    const max = Math.max(1, ...entries.map((item) => item.count));
    return entries.map((item) => ({ ...item, width: (item.count / max) * 100 }));
  }, [feed]);

  const countryBars = useMemo(() => {
    if (!feed) {
      return [] as Array<{ country: string; count: number; width: number }>;
    }
    const items = Object.entries(feed.metrics.devicesByCountry).map(([country, count]) => ({ country, count: Number(count) }));
    const max = Math.max(1, ...items.map((item) => item.count));
    return items.sort((a, b) => b.count - a.count).slice(0, 8).map((item) => ({ ...item, width: (item.count / max) * 100 }));
  }, [feed]);

  const historyPoints = useMemo(() => {
    if (!feed || feed.metrics.scanHistory.length === 0) {
      return "";
    }
    const list = feed.metrics.scanHistory;
    const maxY = Math.max(1, ...list.map((x) => x.findings));
    const width = 420;
    const height = 120;
    return list
      .map((item, index) => {
        const x = (index / Math.max(1, list.length - 1)) * width;
        const y = height - (item.findings / maxY) * height;
        return `${x},${y}`;
      })
      .join(" ");
  }, [feed]);

  const fingerprintAssets = useMemo(() => {
    if (!feed) {
      return [];
    }
    return feed.devices.slice(0, 6);
  }, [feed]);

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

  return (
    <div className="flex flex-col gap-6 pb-20">
      <section className="rounded-2xl border border-emerald-400/20 bg-black/35 p-6 shadow-[0_0_0_1px_rgba(16,185,129,0.18),0_30px_80px_rgba(2,6,23,0.7)] backdrop-blur">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-emerald-300">Nyxera Ops Dashboard</p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight text-emerald-100 sm:text-4xl">Metrics and Threat Charts</h1>
            <p className="mt-2 text-sm text-slate-300">Dashboard is separated from map view and fed by live runtime scan data.</p>
            <p className="mt-2 text-xs text-slate-400">Source: {feed?.source ?? "offline"} · Updated: {feed?.generatedAt ?? "-"}</p>
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
                feed?.metrics.scanLoopRunning
                  ? "border-rose-300/60 bg-rose-300/15 text-rose-200"
                  : "border-emerald-300/60 bg-emerald-300/15 text-emerald-200",
              ].join(" ")}
            >
              {feed?.metrics.scanLoopRunning ? "Stop Scan Loop" : "Start Scan Loop"}
            </button>
          </div>
        </div>
        {scanStatus ? <p className="mt-2 text-xs text-cyan-300">{scanStatus}</p> : null}
        <p className="mt-1 text-xs text-slate-400">Loop status: {feed?.metrics.scanLoopRunning ? "RUNNING" : "STOPPED"} · Batch: {feed?.metrics.scanLoopBatchSize ?? "-"} · Interval: {feed?.metrics.scanLoopIntervalSeconds ?? "-"}s</p>
        {error ? <p className="mt-2 text-xs text-rose-300">{error}</p> : null}
      </section>

      {isLoading || !feed ? (
        <section className="rounded-2xl border border-white/10 bg-black/30 p-6 text-sm text-slate-300">Loading operations feed...</section>
      ) : (
        <>
          <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-6">
            <article className="rounded-xl border border-emerald-300/15 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.15em] text-emerald-300">Assets</p>
              <p className="mt-2 text-3xl font-bold text-emerald-100">{feed.devices.length}</p>
            </article>
            <article className="rounded-xl border border-emerald-300/15 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.15em] text-emerald-300">Findings</p>
              <p className="mt-2 text-3xl font-bold text-emerald-100">{feed.findings.length}</p>
            </article>
            <article className="rounded-xl border border-emerald-300/15 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.15em] text-emerald-300">Events</p>
              <p className="mt-2 text-3xl font-bold text-emerald-100">{feed.events.length}</p>
            </article>
            <article className="rounded-xl border border-emerald-300/15 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.15em] text-emerald-300">Queue</p>
              <p className="mt-2 text-3xl font-bold text-emerald-100">{feed.metrics.queueDepth}</p>
            </article>
            <article className="rounded-xl border border-emerald-300/15 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.15em] text-emerald-300">Throughput</p>
              <p className="mt-2 text-3xl font-bold text-emerald-100">{feed.metrics.miningThroughput.toFixed(1)}</p>
            </article>
            <article className="rounded-xl border border-emerald-300/15 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.15em] text-emerald-300">Scan Runs</p>
              <p className="mt-2 text-3xl font-bold text-emerald-100">{feed.metrics.scanRuns}</p>
            </article>
          </section>

          <section className="grid gap-4 lg:grid-cols-[1fr_1fr_1fr]">
            <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
              <h2 className="text-lg font-semibold text-slate-100">Findings by Severity</h2>
              <div className="mt-4 space-y-3">
                {severityBars.map((bar) => (
                  <div key={bar.level}>
                    <div className="mb-1 flex items-center justify-between text-xs uppercase tracking-[0.12em] text-slate-300">
                      <span>{bar.level}</span>
                      <span>{bar.count}</span>
                    </div>
                    <div className="h-2 rounded-full bg-slate-800">
                      <div
                        className={[
                          "h-2 rounded-full",
                          bar.level === "critical"
                            ? "bg-rose-500"
                            : bar.level === "high"
                              ? "bg-orange-500"
                              : bar.level === "medium"
                                ? "bg-amber-400"
                                : "bg-emerald-500",
                        ].join(" ")}
                        style={{ width: `${bar.width}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </article>

            <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
              <h2 className="text-lg font-semibold text-slate-100">Devices by Country</h2>
              <div className="mt-4 space-y-3">
                {countryBars.map((item) => (
                  <div key={item.country}>
                    <div className="mb-1 flex items-center justify-between text-xs uppercase tracking-[0.12em] text-slate-300">
                      <span>{item.country}</span>
                      <span>{item.count}</span>
                    </div>
                    <div className="h-2 rounded-full bg-slate-800">
                      <div className="h-2 rounded-full bg-cyan-400" style={{ width: `${item.width}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </article>

            <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
              <h2 className="text-lg font-semibold text-slate-100">Findings Trend</h2>
              <div className="mt-4 rounded-lg border border-white/10 bg-slate-950/60 p-3">
                <svg viewBox="0 0 420 120" className="h-32 w-full">
                  <polyline fill="none" stroke="#22d3ee" strokeWidth="3" points={historyPoints} />
                </svg>
              </div>
              <p className="mt-2 text-xs text-slate-400">Trend line shows findings count progression per scan run.</p>
            </article>
          </section>

          <section className="rounded-2xl border border-white/10 bg-black/35 p-5">
            <div className="flex items-end justify-between gap-3">
              <div>
                <h2 className="text-lg font-semibold text-slate-100">Fingerprint Intelligence</h2>
                <p className="mt-1 text-sm text-slate-400">HTTP banners, HTML metadata, favicon hashes, and model or firmware hints from the current asset feed.</p>
              </div>
              <p className="text-xs uppercase tracking-[0.12em] text-cyan-300">{fingerprintAssets.length} assets shown</p>
            </div>
            <div className="mt-4 grid gap-4 xl:grid-cols-2">
              {fingerprintAssets.map((device) => (
                <article key={device.id} className="rounded-xl border border-emerald-300/10 bg-slate-950/70 p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-emerald-100">{device.name}</p>
                      <p className="text-xs text-slate-400">{device.ip} · {device.country}</p>
                    </div>
                    <span className="rounded-full border border-white/10 px-2 py-1 text-[10px] uppercase tracking-[0.16em] text-slate-300">
                      {device.severity}
                    </span>
                  </div>
                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    <div>
                      <p className="text-[11px] uppercase tracking-[0.16em] text-cyan-300">HTTP Server</p>
                      <p className="mt-1 text-sm text-slate-200">{device.fingerprints?.httpServer || "-"}</p>
                    </div>
                    <div>
                      <p className="text-[11px] uppercase tracking-[0.16em] text-cyan-300">HTML Title</p>
                      <p className="mt-1 text-sm text-slate-200">{device.fingerprints?.htmlTitle || "-"}</p>
                    </div>
                    <div>
                      <p className="text-[11px] uppercase tracking-[0.16em] text-cyan-300">Model Hint</p>
                      <p className="mt-1 text-sm text-slate-200">{device.iotMetadata?.model || "-"}</p>
                    </div>
                    <div>
                      <p className="text-[11px] uppercase tracking-[0.16em] text-cyan-300">Firmware Hint</p>
                      <p className="mt-1 text-sm text-slate-200">{device.iotMetadata?.firmware || "-"}</p>
                    </div>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {(device.services || []).map((service) => (
                      <span key={`${device.id}-${service.port}`} className="rounded-full border border-emerald-300/15 bg-emerald-300/5 px-2 py-1 text-[11px] text-emerald-200">
                        {service.service}/{service.port}
                      </span>
                    ))}
                    {device.fingerprints?.faviconHash ? (
                      <span className="rounded-full border border-cyan-300/15 bg-cyan-300/5 px-2 py-1 font-mono text-[11px] text-cyan-200">
                        favicon {device.fingerprints.faviconHash}
                      </span>
                    ) : null}
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {Object.entries(device.fingerprints?.htmlMetadata || {}).slice(0, 2).map(([key, value]) => (
                      <span key={`${device.id}-${key}`} className="rounded-md border border-white/10 px-2 py-1 text-[11px] text-slate-300">
                        {key}: {value}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
