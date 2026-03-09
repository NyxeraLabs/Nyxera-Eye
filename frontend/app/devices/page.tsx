/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { fetchDevices } from "../lib/api";
import type { DeviceLocation } from "../lib/types";

export default function DevicesPage() {
  const [items, setItems] = useState<DeviceLocation[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [query, setQuery] = useState<string>("");
  const [severity, setSeverity] = useState<string>("");
  const [country, setCountry] = useState<string>("");
  const [vendor, setVendor] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    fetchDevices({ q: query, severity, country, vendor, limit: 250 }).then((result) => {
      if (!active) {
        return;
      }
      setItems(result.items);
      setTotal(result.total);
      setLoading(false);
    });
    return () => {
      active = false;
    };
  }, [country, query, severity, vendor]);

  return (
    <div className="flex flex-col gap-4 pb-20">
      <section className="rounded-2xl border border-white/10 bg-black/35 p-5">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold text-emerald-100">Device Registry</h1>
            <p className="text-sm text-slate-300">Search and filter the full accumulated asset inventory.</p>
            <p className="mt-1 text-xs text-slate-400">{total} devices matched current filters.</p>
          </div>
          <Link href="/map" className="rounded-md border border-cyan-300/40 px-3 py-2 text-xs text-cyan-200">
            Open Map
          </Link>
        </div>
        <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search device, IP, model, vendor"
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
          <input
            value={country}
            onChange={(e) => setCountry(e.target.value.toUpperCase())}
            placeholder="Country code"
            className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none"
          />
          <input
            value={vendor}
            onChange={(e) => setVendor(e.target.value)}
            placeholder="Vendor"
            className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none"
          />
        </div>
      </section>

      <section className="rounded-2xl border border-white/10 bg-black/35 p-5">
        {loading ? (
          <p className="text-sm text-slate-300">Loading devices...</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="text-xs uppercase tracking-[0.12em] text-slate-400">
                <tr>
                  <th className="pb-3">Device</th>
                  <th className="pb-3">Vendor / Model</th>
                  <th className="pb-3">Location</th>
                  <th className="pb-3">Severity</th>
                  <th className="pb-3">Scans</th>
                  <th className="pb-3">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {items.map((device) => (
                  <tr key={device.id}>
                    <td className="py-3">
                      <p className="font-semibold text-emerald-100">{device.name}</p>
                      <p className="text-xs text-slate-400">{device.ip}</p>
                    </td>
                    <td className="py-3 text-slate-300">
                      {device.iotMetadata?.vendor || "-"}
                      <p className="text-xs text-slate-500">{device.iotMetadata?.model || "-"}</p>
                    </td>
                    <td className="py-3 text-slate-300">{device.country}</td>
                    <td className="py-3 text-slate-300">{device.severity}</td>
                    <td className="py-3 text-slate-300">{device.scanCount || 0}</td>
                    <td className="py-3">
                      <Link href={`/devices/${device.id}`} className="rounded-md border border-emerald-300/40 px-3 py-2 text-xs text-emerald-200">
                        Investigate
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
