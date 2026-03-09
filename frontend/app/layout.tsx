/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

import type { Metadata } from "next";
import { AppShell } from "./components/app-shell";
import "./globals.css";
import "leaflet/dist/leaflet.css";

export const metadata: Metadata = {
  title: "Nyxera Eye Command Center",
  description: "Next.js + Tailwind frontend for Nyxera Eye",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
