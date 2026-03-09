import { WorldMap } from "./components/world-map";
import { deviceLocations, eventLocations } from "./lib/data";

const metrics = [
  { label: "Queue Depth", value: "12", trend: "+4.1%" },
  { label: "Mining Throughput", value: "245.5/s", trend: "+8.3%" },
  { label: "Probe Success", value: "97.2%", trend: "+1.2%" },
  { label: "Storage Growth", value: "1.24GB", trend: "-0.6%" },
];

export default function DashboardPage() {
  return (
    <div className="flex flex-col gap-6 pb-16">
      <section className="rounded-2xl border border-white/15 bg-white/5 p-6 shadow-glow backdrop-blur">
        <p className="font-mono text-xs uppercase tracking-[0.25em] text-cyan-300">Sprint 18/19 Frontend</p>
        <h1 className="mt-2 text-3xl font-bold sm:text-4xl">Global Exposure Dashboard</h1>
        <p className="mt-2 text-sm text-slate-300">Shared top navigation and footer finding bar are active across all pages.</p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric) => (
          <article key={metric.label} className="rounded-2xl border border-cyan-200/20 bg-slate-950/55 p-4 shadow-glow">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-cyan-300">{metric.label}</p>
            <p className="mt-2 text-3xl font-semibold">{metric.value}</p>
            <p className="mt-1 text-sm text-emerald-300">{metric.trend}</p>
          </article>
        ))}
      </section>

      <section className="rounded-2xl border border-white/10 bg-slate-950/55 p-4">
        <h2 className="mb-3 text-xl font-semibold">World Map Snapshot (Devices + Events)</h2>
        <WorldMap devices={deviceLocations} events={eventLocations} />
      </section>
    </div>
  );
}
