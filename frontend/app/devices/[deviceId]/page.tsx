/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { fetchDevice } from "../../lib/api";
import type { DeviceLocation } from "../../lib/types";

export default function DeviceDetailPage() {
  const params = useParams<{ deviceId: string }>();
  const [device, setDevice] = useState<DeviceLocation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    fetchDevice(params.deviceId).then((result) => {
      if (!active) {
        return;
      }
      setDevice(result);
      setLoading(false);
    });
    return () => {
      active = false;
    };
  }, [params.deviceId]);

  if (loading) {
    return <section className="rounded-2xl border border-white/10 bg-black/35 p-6 text-sm text-slate-300">Loading device investigation...</section>;
  }

  if (!device) {
    return <section className="rounded-2xl border border-rose-300/20 bg-black/35 p-6 text-sm text-rose-200">Device not found.</section>;
  }

  return (
    <div className="flex flex-col gap-4 pb-20">
      <section className="rounded-2xl border border-white/10 bg-black/35 p-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.16em] text-cyan-300">Investigation</p>
            <h1 className="mt-2 text-3xl font-bold text-emerald-100">{device.name}</h1>
            <p className="mt-2 text-sm text-slate-300">
              {device.ip} · {device.city || "-"}, {device.country} · {device.iotMetadata?.vendor || "Unknown vendor"} · {device.iotMetadata?.model || "Unknown model"}
            </p>
          </div>
          <div className="flex gap-2">
            <Link href="/devices" className="rounded-md border border-white/20 px-3 py-2 text-xs text-slate-200">
              Back to Devices
            </Link>
            {device.finding ? (
              <Link href={`/findings?finding=${device.finding.id}`} className="rounded-md border border-amber-300/40 px-3 py-2 text-xs text-amber-200">
                Open Finding
              </Link>
            ) : null}
          </div>
        </div>
      </section>

      <section className="grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
        <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
          <h2 className="text-lg font-semibold text-slate-100">Device Profile</h2>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Severity</p>
              <p className="mt-2 text-xl font-semibold text-slate-100">{device.severity}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Scan Count</p>
              <p className="mt-2 text-xl font-semibold text-slate-100">{device.scanCount || 0}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">First Seen</p>
              <p className="mt-2 text-sm text-slate-100">{device.firstSeen || "-"}</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Last Updated</p>
              <p className="mt-2 text-sm text-slate-100">{device.lastUpdated || "-"}</p>
            </div>
          </div>

          <div className="mt-4 rounded-xl border border-white/10 bg-slate-950/70 p-4">
            <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Fingerprint</p>
            <div className="mt-3 space-y-2 text-sm text-slate-300">
              <p>HTTP Server: {device.fingerprints?.httpServer || "-"}</p>
              <p>HTML Title: {device.fingerprints?.htmlTitle || "-"}</p>
              <p>Firmware: {device.iotMetadata?.firmware || "-"}</p>
              <p>Favicon Hash: {device.fingerprints?.faviconHash || "-"}</p>
            </div>
          </div>
        </article>

        <article className="rounded-2xl border border-white/10 bg-black/35 p-5">
          <h2 className="text-lg font-semibold text-slate-100">Services and Activity</h2>
          <div className="mt-4 grid gap-4">
            <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Services</p>
              <div className="mt-3 space-y-3">
                {(device.services || []).map((service) => (
                  <div key={`${service.port}-${service.protocol}`} className="rounded-lg border border-white/10 bg-black/20 p-3 text-sm text-slate-300">
                    <p className="font-semibold text-slate-100">
                      {service.service} · {service.port}/{service.protocol}
                    </p>
                    <p className="text-xs text-slate-400">{service.banner}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Linked Finding</p>
              {device.finding ? (
                <div className="mt-3 rounded-lg border border-white/10 bg-black/20 p-3 text-sm text-slate-300">
                  <p className="font-semibold text-slate-100">{device.finding.title}</p>
                  <p className="mt-1">{device.finding.description}</p>
                  <p className="mt-2 text-xs text-slate-400">
                    {device.finding.severity} · {device.finding.status} · updated {device.finding.updatedAt}
                  </p>
                </div>
              ) : (
                <p className="mt-3 text-sm text-slate-400">No active finding linked to this device.</p>
              )}
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-950/70 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-cyan-300">Recent Events</p>
              <div className="mt-3 space-y-2">
                {(device.events || []).length === 0 ? (
                  <p className="text-sm text-slate-400">No recent events recorded.</p>
                ) : (
                  (device.events || []).map((event) => (
                    <div key={event.id} className="flex items-center justify-between gap-3 rounded-lg border border-white/10 bg-black/20 p-3 text-sm text-slate-300">
                      <div>
                        <p className="font-semibold text-slate-100">{event.title}</p>
                        <p className="text-xs text-slate-400">{event.type}</p>
                      </div>
                      <p className="text-xs text-slate-500">{event.timestamp}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </article>
      </section>
    </div>
  );
}
