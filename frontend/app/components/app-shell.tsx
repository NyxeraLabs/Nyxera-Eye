/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import { usePathname } from "next/navigation";

import { AuthGate, AuthProvider } from "./auth-context";
import { FooterFindingBar } from "./footer-finding-bar";
import { FindingProvider } from "./finding-context";
import { TopNav } from "./top-nav";

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const hideOpsShell = pathname === "/login" || pathname === "/register";

  return (
    <AuthProvider>
      <AuthGate>
        <FindingProvider>
          <div className="min-h-screen bg-nyx-gradient text-slate-100">
            {!hideOpsShell ? <TopNav /> : null}
            <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
            {!hideOpsShell ? <FooterFindingBar /> : null}
          </div>
        </FindingProvider>
      </AuthGate>
    </AuthProvider>
  );
}
