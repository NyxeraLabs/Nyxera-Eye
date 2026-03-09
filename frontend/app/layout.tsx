import type { Metadata } from "next";
import { AppShell } from "./components/app-shell";
import "./globals.css";

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
