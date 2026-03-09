/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import { useEffect, useState } from "react";

import { fetchAuditEvents } from "../lib/api";
import type { AuditEvent } from "../lib/api";

export default function AuditPage() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [status, setStatus] = useState("");

  const load = async () => {
    setStatus("Loading audit events...");
    const rows = await fetchAuditEvents(300);
    setEvents(rows);
    setStatus(rows.length ? `Loaded ${rows.length} events.` : "No events returned (admin role required).");
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="flex flex-col gap-4 pb-20">
      <section className="rounded-2xl border border-cyan-300/20 bg-black/35 p-6">
        <p className="font-mono text-xs uppercase tracking-[0.24em] text-cyan-300">Audit</p>
        <h1 className="mt-2 text-3xl font-bold text-cyan-100">Traceability Ledger</h1>
        <p className="mt-2 text-sm text-slate-300">All user and API operations are logged with actor, action, status, method, path, and timestamp.</p>
        <button
          onClick={load}
          className="mt-4 rounded-md border border-cyan-300/55 bg-cyan-300/10 px-3 py-2 text-xs uppercase tracking-[0.12em] text-cyan-200"
        >
          Refresh Audit Log
        </button>
        {status ? <p className="mt-2 text-xs text-cyan-300">{status}</p> : null}
      </section>

      <section className="overflow-hidden rounded-2xl border border-white/10 bg-black/30">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-xs">
            <thead className="bg-slate-900/70 text-slate-300">
              <tr>
                <th className="px-3 py-2">Timestamp</th>
                <th className="px-3 py-2">Actor</th>
                <th className="px-3 py-2">Action</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Method</th>
                <th className="px-3 py-2">Path</th>
                <th className="px-3 py-2">IP</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event) => (
                <tr key={event.id} className="border-t border-white/5 text-slate-200">
                  <td className="px-3 py-2">{event.timestamp}</td>
                  <td className="px-3 py-2">{event.actor}</td>
                  <td className="px-3 py-2">{event.action}</td>
                  <td className={["px-3 py-2", event.status === "ok" ? "text-emerald-300" : "text-rose-300"].join(" ")}>
                    {event.status}
                  </td>
                  <td className="px-3 py-2">{event.method}</td>
                  <td className="px-3 py-2">{event.path}</td>
                  <td className="px-3 py-2">{event.ip}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
