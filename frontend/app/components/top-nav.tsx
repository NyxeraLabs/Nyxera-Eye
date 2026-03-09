"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/map", label: "World Map" },
  { href: "/events", label: "Events" },
  { href: "/findings", label: "Findings" },
];

export function TopNav() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/85 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.28em] text-cyan-300">Nyxera Eye</p>
          <p className="text-sm text-slate-300">Frontend Command Center</p>
        </div>
        <nav className="flex items-center gap-2">
          {links.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={[
                  "rounded-lg px-3 py-2 text-sm transition",
                  active ? "bg-cyan-400/20 text-cyan-200" : "text-slate-300 hover:bg-white/5 hover:text-white",
                ].join(" ")}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
