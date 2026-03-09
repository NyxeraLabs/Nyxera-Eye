import { WorldMap } from "../components/world-map";
import { deviceLocations, eventLocations } from "../lib/data";

export default function MapPage() {
  return (
    <div className="flex flex-col gap-6 pb-16">
      <section className="rounded-2xl border border-white/10 bg-slate-950/55 p-5">
        <h1 className="text-2xl font-bold">World Map</h1>
        <p className="mt-1 text-sm text-slate-300">Device locations and event locations are rendered together.</p>
      </section>

      <WorldMap devices={deviceLocations} events={eventLocations} />

      <section className="grid gap-4 md:grid-cols-2">
        <article className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
          <h2 className="font-semibold">Device Points</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {deviceLocations.map((d) => (
              <li key={d.id} className="rounded-md border border-white/10 bg-white/5 p-2">
                {d.name} ({d.ip}) - {d.country} [{d.lat.toFixed(2)}, {d.lon.toFixed(2)}]
              </li>
            ))}
          </ul>
        </article>
        <article className="rounded-2xl border border-white/10 bg-slate-950/45 p-4">
          <h2 className="font-semibold">Event Points</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {eventLocations.map((e) => (
              <li key={e.id} className="rounded-md border border-white/10 bg-white/5 p-2">
                {e.title} - {e.timestamp} [{e.lat.toFixed(2)}, {e.lon.toFixed(2)}]
              </li>
            ))}
          </ul>
        </article>
      </section>
    </div>
  );
}
