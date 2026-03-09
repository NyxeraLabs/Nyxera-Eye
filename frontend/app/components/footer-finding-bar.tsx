"use client";

import { useState } from "react";

import { exportFinding } from "../lib/api";
import { useOpsFeed } from "../lib/use-ops-feed";
import { useFinding } from "./finding-context";

const severityClass: Record<string, string> = {
  critical: "text-rose-300",
  high: "text-orange-300",
  medium: "text-amber-300",
  low: "text-emerald-300",
};

export function FooterFindingBar() {
  const { selected } = useFinding();
  const { findingAction } = useOpsFeed(30000);
  const [status, setStatus] = useState<string>("");

  const handleAction = async (action: string) => {
    if (!selected) {
      setStatus("Select a finding first.");
      return;
    }
    const ok = await findingAction(selected.id, action);
    setStatus(ok ? `Action '${action}' applied.` : `Action '${action}' failed.`);
  };

  const handleExport = async () => {
    if (!selected) {
      setStatus("Select a finding first.");
      return;
    }
    const payload = await exportFinding(selected.id);
    if (!payload) {
      setStatus("Export failed.");
      return;
    }
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${selected.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
    setStatus("Finding exported.");
  };

  return (
    <footer className="sticky bottom-0 z-40 border-t border-emerald-300/20 bg-black/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 sm:px-6 lg:px-8 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.22em] text-emerald-300">Selected Finding Context</p>
          {selected ? (
            <>
              <p className="text-sm font-semibold text-emerald-50">{selected.title}</p>
              <p className="text-xs text-slate-300">{selected.description}</p>
              <p className={["text-xs font-semibold", severityClass[selected.severity] || "text-slate-300"].join(" ")}>
                Severity: {selected.severity.toUpperCase()} · Device: {selected.deviceId} · Status: {selected.status}
              </p>
            </>
          ) : (
            <p className="text-sm text-slate-400">No finding selected. Select one from Events or Findings pages.</p>
          )}
          {status ? <p className="mt-1 text-xs text-cyan-300">{status}</p> : null}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => handleAction("investigate")}
            className="rounded-md border border-emerald-300/50 px-3 py-2 text-xs text-emerald-200 hover:bg-emerald-300/10"
          >
            Investigate
          </button>
          <button
            onClick={() => handleAction("open_device")}
            className="rounded-md border border-cyan-300/40 px-3 py-2 text-xs text-cyan-200 hover:bg-cyan-300/10"
          >
            Open Device
          </button>
          <button
            onClick={() => handleAction("escalate")}
            className="rounded-md border border-rose-300/45 px-3 py-2 text-xs text-rose-200 hover:bg-rose-300/10"
          >
            Escalate
          </button>
          <button
            onClick={handleExport}
            className="rounded-md border border-amber-300/40 px-3 py-2 text-xs text-amber-200 hover:bg-amber-300/10"
          >
            Export JSON
          </button>
        </div>
      </div>
    </footer>
  );
}
