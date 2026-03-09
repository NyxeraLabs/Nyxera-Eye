"use client";

import { useState } from "react";

import { useFinding } from "../components/finding-context";
import type { Finding } from "../lib/types";
import { useOpsFeed } from "../lib/use-ops-feed";

const severityClass: Record<string, string> = {
  critical: "text-rose-300",
  high: "text-orange-300",
  medium: "text-amber-300",
  low: "text-emerald-300",
};

export default function FindingsPage() {
  const { selected, setSelected } = useFinding();
  const { feed, isLoading } = useOpsFeed();
  const [opened, setOpened] = useState<Finding | null>(null);

  return (
    <div className="grid gap-4 pb-20 lg:grid-cols-[1.3fr_0.9fr]">
      <section className="rounded-2xl border border-white/10 bg-black/35 p-5">
        <h1 className="text-2xl font-bold text-emerald-100">Findings Registry</h1>
        <p className="text-sm text-slate-300">Full list of findings with open-and-interact workflow.</p>

        {isLoading || !feed ? (
          <p className="mt-4 text-sm text-slate-300">Loading findings...</p>
        ) : (
          <ul className="mt-4 space-y-3">
            {feed.findings.map((finding) => {
              const active = selected?.id === finding.id;
              const isOpened = opened?.id === finding.id;
              return (
                <li key={finding.id} className="rounded-xl border border-white/10 bg-slate-950/55 p-4">
                  <p className="font-semibold text-slate-100">{finding.title}</p>
                  <p className="mt-1 text-sm text-slate-300">{finding.description}</p>
                  <p className={["mt-2 text-xs font-semibold", severityClass[finding.severity] || "text-slate-300"].join(" ")}>
                    {finding.severity.toUpperCase()} · {finding.deviceId}
                  </p>
                  <div className="mt-3 flex gap-2">
                    <button
                      onClick={() => setOpened(finding)}
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
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      <aside className="rounded-2xl border border-emerald-300/20 bg-black/35 p-5">
        <h2 className="text-lg font-semibold text-emerald-100">Finding Interaction Panel</h2>
        {opened ? (
          <>
            <p className="mt-3 font-semibold text-slate-100">{opened.title}</p>
            <p className="mt-1 text-sm text-slate-300">{opened.description}</p>
            <p className={["mt-2 text-xs font-semibold", severityClass[opened.severity] || "text-slate-300"].join(" ")}>
              {opened.severity.toUpperCase()} · {opened.deviceId}
            </p>
            <div className="mt-4 grid gap-2">
              <button className="rounded-md border border-emerald-300/50 bg-emerald-300/10 px-3 py-2 text-xs text-emerald-200">
                Open Device Investigation
              </button>
              <button className="rounded-md border border-cyan-300/50 bg-cyan-300/10 px-3 py-2 text-xs text-cyan-200">
                Link to Event Timeline
              </button>
              <button className="rounded-md border border-amber-300/50 bg-amber-300/10 px-3 py-2 text-xs text-amber-200">
                Mark for Escalation
              </button>
            </div>
          </>
        ) : (
          <p className="mt-3 text-sm text-slate-400">Open a finding from the list to interact with it.</p>
        )}
      </aside>
    </div>
  );
}
