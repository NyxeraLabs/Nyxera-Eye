/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { useFinding } from "../components/finding-context";
import { exportFinding, fetchFinding, fetchFindings } from "../lib/api";
import type { Finding } from "../lib/types";
import { useOpsFeed } from "../lib/use-ops-feed";

const severityClass: Record<string, string> = {
  critical: "text-rose-300",
  high: "text-orange-300",
  medium: "text-amber-300",
  low: "text-emerald-300",
};

export default function FindingsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { selected, setSelected } = useFinding();
  const { findingAction } = useOpsFeed();
  const [items, setItems] = useState<Finding[]>([]);
  const [opened, setOpened] = useState<Finding | null>(null);
  const [status, setStatus] = useState<string>("");
  const [query, setQuery] = useState<string>(searchParams.get("q") || "");
  const [severity, setSeverity] = useState<string>(searchParams.get("severity") || "");
  const [findingStatus, setFindingStatus] = useState<string>(searchParams.get("status") || "");
  const [loading, setLoading] = useState<boolean>(true);
  const [total, setTotal] = useState<number>(0);

  useEffect(() => {
    let active = true;
    setLoading(true);
    fetchFindings({ q: query, severity, status: findingStatus, limit: 250 }).then((result) => {
      if (!active) {
        return;
      }
      setItems(result.items);
      setTotal(result.total);
      setLoading(false);
      const requestedFindingId = searchParams.get("finding");
      if (requestedFindingId) {
        fetchFinding(requestedFindingId).then((finding) => {
          if (!active || !finding) {
            return;
          }
          setOpened(finding);
          setSelected(finding);
        });
      }
    });
    return () => {
      active = false;
    };
  }, [findingStatus, query, searchParams, setSelected, severity]);

  const act = async (finding: Finding, action: string) => {
    const ok = await findingAction(finding.id, action);
    setStatus(ok ? `Action '${action}' applied.` : `Action '${action}' failed.`);
    if (ok) {
      const refreshed = await fetchFinding(finding.id);
      if (refreshed) {
        setOpened(refreshed);
        setSelected(refreshed);
      }
      const result = await fetchFindings({ q: query, severity, status: findingStatus, limit: 250 });
      setItems(result.items);
      setTotal(result.total);
    }
  };

  const doExport = async (finding: Finding) => {
    const payload = await exportFinding(finding.id);
    if (!payload) {
      setStatus("Export failed.");
      return;
    }
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${finding.id}.json`;
    anchor.click();
    URL.revokeObjectURL(url);
    setStatus("Exported finding JSON.");
  };

  const openFinding = async (finding: Finding) => {
    setOpened(finding);
    setSelected(finding);
    const detail = await fetchFinding(finding.id);
    if (detail) {
      setOpened(detail);
      setSelected(detail);
    }
  };

  const investigate = async (finding: Finding) => {
    await act(finding, "investigate");
    router.push(`/devices/${finding.deviceId}`);
  };

  return (
    <div className="grid gap-4 pb-20 lg:grid-cols-[1.2fr_0.8fr]">
      <section className="rounded-2xl border border-white/10 bg-black/35 p-5">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold text-emerald-100">Findings Registry</h1>
            <p className="text-sm text-slate-300">Full searchable list of findings with working investigation links and detail view.</p>
            <p className="mt-1 text-xs text-slate-400">{total} findings matched current filters.</p>
          </div>
          <Link href="/devices" className="rounded-md border border-cyan-300/40 px-3 py-2 text-xs text-cyan-200">
            Browse Devices
          </Link>
        </div>
        {status ? <p className="mt-2 text-xs text-cyan-300">{status}</p> : null}

        <div className="mt-4 grid gap-3 md:grid-cols-[1fr_160px_180px]">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search title, description, device, or finding id"
            className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none"
          />
          <select
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
            className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none"
          >
            <option value="">All severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <select
            value={findingStatus}
            onChange={(e) => setFindingStatus(e.target.value)}
            className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none"
          >
            <option value="">All statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="acknowledged">Acknowledged</option>
            <option value="escalated">Escalated</option>
            <option value="closed">Closed</option>
          </select>
        </div>

        {loading ? (
          <p className="mt-4 text-sm text-slate-300">Loading findings...</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {items.map((finding) => {
              const active = selected?.id === finding.id;
              const isOpened = opened?.id === finding.id;
              return (
                <li key={finding.id} className="rounded-xl border border-white/10 bg-slate-950/55 p-4">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="font-semibold text-slate-100">{finding.title}</p>
                      <p className="mt-1 text-sm text-slate-300">{finding.description}</p>
                      <p className={["mt-2 text-xs font-semibold", severityClass[finding.severity] || "text-slate-300"].join(" ")}>
                        {finding.severity.toUpperCase()} · {finding.deviceId} · status: {finding.status}
                      </p>
                    </div>
                    <Link href={`/devices/${finding.deviceId}`} className="rounded-md border border-emerald-300/40 px-3 py-2 text-xs text-emerald-200">
                      Device Detail
                    </Link>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <button
                      onClick={() => openFinding(finding)}
                      className={[
                        "rounded-md px-3 py-2 text-xs",
                        isOpened
                          ? "border border-cyan-300/50 bg-cyan-300/15 text-cyan-200"
                          : "border border-white/20 bg-white/5 text-slate-200 hover:bg-white/10",
                      ].join(" ")}
                    >
                      {isOpened ? "Opened" : "Open"}
                    </button>
                    <button
                      onClick={() => setSelected(finding)}
                      className={[
                        "rounded-md px-3 py-2 text-xs",
                        active
                          ? "border border-emerald-300/50 bg-emerald-300/15 text-emerald-200"
                          : "border border-white/20 bg-white/5 text-slate-200 hover:bg-white/10",
                      ].join(" ")}
                    >
                      {active ? "Selected" : "Select"}
                    </button>
                    <button
                      onClick={() => investigate(finding)}
                      className="rounded-md border border-emerald-300/50 bg-emerald-300/10 px-3 py-2 text-xs text-emerald-200"
                    >
                      Investigate
                    </button>
                    <button
                      onClick={() => act(finding, "escalate")}
                      className="rounded-md border border-rose-300/40 bg-rose-300/10 px-3 py-2 text-xs text-rose-200"
                    >
                      Escalate
                    </button>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      <aside className="rounded-2xl border border-emerald-300/20 bg-black/35 p-5">
        <h2 className="text-lg font-semibold text-emerald-100">Finding Detail</h2>
        {opened ? (
          <>
            <p className="mt-3 font-semibold text-slate-100">{opened.title}</p>
            <p className="mt-1 text-sm text-slate-300">{opened.description}</p>
            <p className={["mt-2 text-xs font-semibold", severityClass[opened.severity] || "text-slate-300"].join(" ")}>
              {opened.severity.toUpperCase()} · {opened.deviceId} · {opened.status}
            </p>
            <div className="mt-4 rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Linked Device</p>
              <p className="mt-2 text-sm text-slate-100">{opened.device?.name || opened.deviceId}</p>
              <p className="text-xs text-slate-400">
                {opened.device?.ip || "-"} · {opened.device?.iotMetadata?.vendor || "Unknown vendor"} · {opened.device?.iotMetadata?.model || "-"}
              </p>
              <p className="mt-2 text-xs text-slate-400">Updated at {opened.updatedAt}</p>
            </div>
            <div className="mt-4 grid gap-2">
              <button
                onClick={() => investigate(opened)}
                className="rounded-md border border-emerald-300/50 bg-emerald-300/10 px-3 py-2 text-xs text-emerald-200"
              >
                Open Device Investigation
              </button>
              <button
                onClick={() => act(opened, "ack")}
                className="rounded-md border border-cyan-300/50 bg-cyan-300/10 px-3 py-2 text-xs text-cyan-200"
              >
                Acknowledge
              </button>
              <button
                onClick={() => act(opened, "close")}
                className="rounded-md border border-slate-300/40 bg-slate-300/10 px-3 py-2 text-xs text-slate-200"
              >
                Close
              </button>
              <button
                onClick={() => doExport(opened)}
                className="rounded-md border border-amber-300/50 bg-amber-300/10 px-3 py-2 text-xs text-amber-200"
              >
                Export JSON
              </button>
            </div>
            <div className="mt-4 rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Action History</p>
              <div className="mt-3 space-y-2">
                {opened.actions.length === 0 ? (
                  <p className="text-sm text-slate-400">No actions recorded yet.</p>
                ) : (
                  opened.actions.map((action) => (
                    <div key={`${action.action}-${action.at}`} className="flex items-center justify-between gap-3 text-sm text-slate-300">
                      <span>{action.action}</span>
                      <span className="text-xs text-slate-500">{action.at}</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </>
        ) : (
          <p className="mt-3 text-sm text-slate-400">Open a finding from the list to inspect details and take actions.</p>
        )}
      </aside>
    </div>
  );
}
