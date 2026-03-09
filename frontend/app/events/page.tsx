"use client";

import { useFinding } from "../components/finding-context";
import { eventLocations, findings } from "../lib/data";

export default function EventsPage() {
  const { selected, setSelected } = useFinding();

  return (
    <div className="flex flex-col gap-4 pb-16">
      <section className="rounded-2xl border border-white/10 bg-slate-950/55 p-5">
        <h1 className="text-2xl font-bold">Events Timeline</h1>
        <p className="text-sm text-slate-300">Select an event to bind the related finding to the global footer actions.</p>
      </section>

      <ul className="space-y-3">
        {eventLocations.map((event, index) => {
          const linked = findings[index % findings.length];
          const isActive = selected?.id === linked.id;
          return (
            <li key={event.id} className="rounded-xl border border-white/10 bg-slate-950/50 p-4">
              <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="font-semibold">{event.title}</p>
                  <p className="text-xs text-slate-400">
                    {event.type} · {event.timestamp} · [{event.lat.toFixed(2)}, {event.lon.toFixed(2)}]
                  </p>
                </div>
                <button
                  onClick={() => setSelected(linked)}
                  className={[
                    "rounded-md px-3 py-2 text-xs",
                    isActive
                      ? "border border-cyan-300/50 bg-cyan-300/15 text-cyan-200"
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
    </div>
  );
}
