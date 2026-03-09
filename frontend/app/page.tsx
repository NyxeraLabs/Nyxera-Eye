"use client";

import { useMemo } from "react";

import { useOpsFeed } from "./lib/use-ops-feed";

function severityBars(severities: string[]) {
  const counts = severities.reduce<Record<string, number>>((acc, severity) => {
    acc[severity] = (acc[severity] || 0) + 1;
    return acc;
  }, {});

  const entries = ["critical", "high", "medium", "low"].map((level) => ({
    level,
    count: counts[level] || 0,
  }));

  const max = Math.max(1, ...entries.map((item) => item.count));
  return entries.map((item) => ({ ...item, width: (item.count / max) * 100 }));
}

export default function DashboardPage() {
  const { feed, isLoading } = useOpsFeed();

  const bars = useMemo(() => {
    if (!feed) {
      return [];
    }
    return severityBars(feed.findings.map((finding) => finding.severity));
  }, [feed]);

  const metricCards = feed
    ? [
        { label: "Queue Depth", value: String(feed.metrics.queueDepth), note: "tasks pending" },
        { label: "Mining Throughput", value: `${feed.metrics.miningThroughput.toFixed(1)}/s`, note: "collector pace" },
        { label: "Probe Success", value: `${feed.metrics.probeSuccessRate.toFixed(1)}%`, note: "protocol health" },
        { label: "Storage Growth", value: `${feed.metrics.storageGrowthGb.toFixed(2)} GB`, note: "daily growth" },
      ]
    : [];

  return (
    <div className="flex flex-col gap-6 pb-20">
      <section className="rounded-2xl border border-emerald-400/20 bg-black/35 p-6 shadow-[0_0_0_1px_rgba(16,185,129,0.18),0_30px_80px_rgba(2,6,23,0.7)] backdrop-blur">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-emerald-300">Nyxera Ops Dashboard</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-emerald-100 sm:text-4xl">Operations and Telemetry Overview</h1>
        <p className="mt-2 text-sm text-slate-300">
          Dashboard is separated from map view. World map is available in the dedicated "World Map" page.
        </p>
        <p className="mt-2 text-xs text-slate-400">
          Feed source: {feed?.source ?? "loading"} · Updated: {feed?.generatedAt ?? "-"}
        </p>
      </section>

      {isLoading ? (
        <section className="rounded-2xl border border-white/10 bg-black/30 p-6 text-sm text-slate-300">Loading operations feed...</section>
      ) : (
        <>
          <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {metricCards.map((metric) => (
              <article
                key={metric.label}
                className="rounded-2xl border border-emerald-300/15 bg-slate-950/70 p-4 shadow-[0_12px_36px_rgba(2,6,23,0.75)]"
              >
                <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-emerald-300">{metric.label}</p>
                <p className="mt-2 text-3xl font-bold text-emerald-100">{metric.value}</p>
                <p className="mt-1 text-xs text-slate-400">{metric.note}</p>
              </article>
            ))}
          </section>

          <section className="grid gap-4 lg:grid-cols-[1.15fr_1fr]">
            <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
              <h2 className="text-lg font-semibold text-slate-100">Findings Severity Distribution</h2>
              <div className="mt-4 space-y-3">
                {bars.map((bar) => (
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
              <h2 className="text-lg font-semibold text-slate-100">Operational Tempo</h2>
              <ul className="mt-4 space-y-2 text-sm text-slate-300">
                <li>Tracked assets: {feed?.devices.length ?? 0}</li>
                <li>Active events: {feed?.events.length ?? 0}</li>
                <li>Open findings: {feed?.findings.length ?? 0}</li>
                <li>High-risk findings: {feed?.findings.filter((f) => ["critical", "high"].includes(f.severity)).length ?? 0}</li>
              </ul>
              <p className="mt-4 rounded-md border border-emerald-300/20 bg-emerald-300/5 p-3 text-xs text-emerald-200">
                Tactical recommendation: pivot to findings page and escalate critical items first.
              </p>
            </article>
          </section>
        </>
      )}
    </div>
  );
}
