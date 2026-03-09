"use client";

import { useFinding } from "./finding-context";

const severityClass: Record<string, string> = {
  critical: "text-rose-300",
  high: "text-orange-300",
  medium: "text-amber-300",
  low: "text-emerald-300",
};

export function FooterFindingBar() {
  const { selected } = useFinding();
  return (
    <footer className="sticky bottom-0 z-40 border-t border-white/10 bg-slate-950/95">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 sm:px-6 lg:px-8 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.22em] text-slate-400">Selected Finding</p>
          {selected ? (
            <>
              <p className="text-sm font-semibold text-white">{selected.title}</p>
              <p className="text-xs text-slate-300">{selected.description}</p>
              <p className={["text-xs font-semibold", severityClass[selected.severity] || "text-slate-300"].join(" ")}>
                Severity: {selected.severity.toUpperCase()} · Device: {selected.deviceId}
              </p>
            </>
          ) : (
            <p className="text-sm text-slate-400">No finding selected. Select one from Events or Findings pages.</p>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button className="rounded-md border border-cyan-300/40 px-3 py-2 text-xs text-cyan-200 hover:bg-cyan-300/10">
            Investigate
          </button>
          <button className="rounded-md border border-white/20 px-3 py-2 text-xs text-slate-200 hover:bg-white/10">Open Device</button>
          <button className="rounded-md border border-emerald-300/40 px-3 py-2 text-xs text-emerald-200 hover:bg-emerald-300/10">
            Export JSON
          </button>
        </div>
      </div>
    </footer>
  );
}
