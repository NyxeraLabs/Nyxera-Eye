"use client";

import { useFinding } from "../components/finding-context";
import { useOpsFeed } from "../lib/use-ops-feed";

export default function EventsPage() {
  const { selected, setSelected } = useFinding();
  const { feed, isLoading } = useOpsFeed();

  return (
    <div className="flex flex-col gap-4 pb-20">
      <section className="rounded-2xl border border-emerald-300/20 bg-black/35 p-5">
        <h1 className="text-2xl font-bold text-emerald-100">Events Timeline</h1>
        <p className="text-sm text-slate-300">Select an event to link its associated finding to the global footer actions.</p>
      </section>

      {isLoading || !feed ? (
        <section className="rounded-xl border border-white/10 bg-black/35 p-4 text-sm text-slate-300">Loading events...</section>
      ) : (
        <ul className="space-y-3">
          {feed.events.map((event) => {
            const linked = feed.findings.find((finding) => finding.deviceId === event.deviceId) ?? feed.findings[0] ?? null;
            const isActive = selected?.id === linked?.id;
            return (
              <li key={event.id} className="rounded-xl border border-white/10 bg-black/35 p-4">
                <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                  <div>
                    <p className="font-semibold text-slate-100">{event.title}</p>
                    <p className="text-xs text-slate-400">
                      {event.type} · {event.timestamp} · [{event.lat.toFixed(2)}, {event.lon.toFixed(2)}]
                    </p>
                  </div>
                  <button
                    disabled={!linked}
                    onClick={() => linked && setSelected(linked)}
                    className={[
                      "rounded-md px-3 py-2 text-xs",
                      isActive
                        ? "border border-emerald-300/50 bg-emerald-300/15 text-emerald-200"
                        : "border border-white/20 bg-white/5 text-slate-200 hover:bg-white/10",
                    ].join(" ")}
                  >
                    {isActive ? "Selected" : "Select Finding"}
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
