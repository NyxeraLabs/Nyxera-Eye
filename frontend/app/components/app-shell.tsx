"use client";

import { FooterFindingBar } from "./footer-finding-bar";
import { FindingProvider } from "./finding-context";
import { TopNav } from "./top-nav";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <FindingProvider>
      <div className="min-h-screen bg-nyx-gradient text-slate-100">
        <TopNav />
        <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
        <FooterFindingBar />
      </div>
    </FindingProvider>
  );
}
