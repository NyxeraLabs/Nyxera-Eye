"use client";

import { useEffect, useState } from "react";

import { fetchSettings, updateSettings } from "../lib/api";
import type { FrontendSettings } from "../lib/types";

const defaultSettings: FrontendSettings = {
  runtimeMode: "passive",
  scanDefaultBatchSize: 96,
  scanDefaultIntervalSeconds: 10,
  autoStartScanLoop: false,
  authorizedScopeReference: "",
};

export default function SettingsPage() {
  const [settings, setSettings] = useState<FrontendSettings>(defaultSettings);
  const [status, setStatus] = useState("");

  useEffect(() => {
    fetchSettings().then((remote) => {
      if (remote) {
        setSettings(remote);
      }
    });
  }, []);

  const save = async () => {
    setStatus("Saving settings...");
    const ok = await updateSettings(settings);
    setStatus(ok ? "Settings updated successfully." : "Failed to update settings. Admin role required.");
  };

  return (
    <div className="flex flex-col gap-4 pb-20">
      <section className="rounded-2xl border border-emerald-300/20 bg-black/35 p-6">
        <p className="font-mono text-xs uppercase tracking-[0.24em] text-emerald-300">Configuration</p>
        <h1 className="mt-2 text-3xl font-bold text-emerald-100">Platform Settings</h1>
        <p className="mt-2 text-sm text-slate-300">Configure runtime mode, scan defaults, and authorization scope metadata.</p>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <article className="rounded-2xl border border-white/10 bg-black/30 p-5">
          <h2 className="text-lg font-semibold text-slate-100">Runtime</h2>
          <div className="mt-4 space-y-3">
            <label className="block text-xs uppercase tracking-[0.14em] text-slate-300">Runtime Mode</label>
            <select
              className="w-full rounded-md border border-white/20 bg-slate-950/80 px-3 py-2 text-sm"
              value={settings.runtimeMode}
              onChange={(e) => setSettings({ ...settings, runtimeMode: e.target.value })}
            >
              <option value="passive">passive</option>
              <option value="authorized_scope">authorized_scope</option>
            </select>

            <label className="block text-xs uppercase tracking-[0.14em] text-slate-300">Authorized Scope Reference</label>
            <input
              className="w-full rounded-md border border-white/20 bg-slate-950/80 px-3 py-2 text-sm"
              value={settings.authorizedScopeReference}
              onChange={(e) => setSettings({ ...settings, authorizedScopeReference: e.target.value })}
            />
          </div>
        </article>

        <article className="rounded-2xl border border-white/10 bg-black/30 p-5">
          <h2 className="text-lg font-semibold text-slate-100">Scan Controls</h2>
          <div className="mt-4 space-y-3">
            <label className="block text-xs uppercase tracking-[0.14em] text-slate-300">Default Batch Size</label>
            <input
              type="number"
              min={1}
              max={1024}
              className="w-full rounded-md border border-white/20 bg-slate-950/80 px-3 py-2 text-sm"
              value={settings.scanDefaultBatchSize}
              onChange={(e) => setSettings({ ...settings, scanDefaultBatchSize: Number(e.target.value || 1) })}
            />

            <label className="block text-xs uppercase tracking-[0.14em] text-slate-300">Default Interval Seconds</label>
            <input
              type="number"
              min={1}
              max={300}
              className="w-full rounded-md border border-white/20 bg-slate-950/80 px-3 py-2 text-sm"
              value={settings.scanDefaultIntervalSeconds}
              onChange={(e) => setSettings({ ...settings, scanDefaultIntervalSeconds: Number(e.target.value || 1) })}
            />

            <label className="flex items-center gap-2 text-xs uppercase tracking-[0.14em] text-slate-300">
              <input
                type="checkbox"
                checked={settings.autoStartScanLoop}
                onChange={(e) => setSettings({ ...settings, autoStartScanLoop: e.target.checked })}
              />
              Auto start scan loop on runtime boot
            </label>
          </div>
        </article>
      </section>

      <button
        onClick={save}
        className="w-fit rounded-md border border-emerald-300/60 bg-emerald-300/15 px-4 py-2 text-sm text-emerald-100"
      >
        Save Settings
      </button>
      {status ? <p className="text-xs text-cyan-300">{status}</p> : null}
    </div>
  );
}
