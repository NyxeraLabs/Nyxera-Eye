"use client";

import { useFinding } from "../components/finding-context";
import { findings } from "../lib/data";

const severityClass: Record<string, string> = {
  critical: "text-rose-300",
  high: "text-orange-300",
  medium: "text-amber-300",
  low: "text-emerald-300",
};

export default function FindingsPage() {
  const { selected, setSelected } = useFinding();

  return (
    <div className="flex flex-col gap-4 pb-16">
      <section className="rounded-2xl border border-white/10 bg-slate-950/55 p-5">
        <h1 className="text-2xl font-bold">Findings</h1>
        <p className="text-sm text-slate-300">Choose a finding to activate footer action buttons and context summary.</p>
      </section>

      <div className="grid gap-3 md:grid-cols-2">
        {findings.map((finding) => {
          const active = selected?.id === finding.id;
          return (
            <article key={finding.id} className="rounded-xl border border-white/10 bg-slate-950/50 p-4">
              <p className="font-semibold">{finding.title}</p>
              <p className="mt-1 text-sm text-slate-300">{finding.description}</p>
              <p className={["mt-2 text-xs font-semibold", severityClass[finding.severity] || "text-slate-300"].join(" ")}>
                {finding.severity.toUpperCase()} · {finding.deviceId}
              </p>
              <button
                onClick={() => setSelected(finding)}
                className={[
                  "mt-3 rounded-md px-3 py-2 text-xs",
                  active
                    ? "border border-cyan-300/50 bg-cyan-300/15 text-cyan-200"
                    : "border border-white/20 bg-white/5 text-slate-200 hover:bg-white/10",
                ].join(" ")}
              >
                {active ? "Selected" : "Select"}
              </button>
            </article>
          );
        })}
      </div>
    </div>
  );
}
