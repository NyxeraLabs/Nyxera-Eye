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
    <header className="sticky top-0 z-40 border-b border-emerald-400/20 bg-black/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.28em] text-emerald-300">Nyxera Eye · Ops</p>
          <p className="text-sm text-slate-300">Offensive Security Command Surface</p>
        </div>
        <nav className="flex items-center gap-2">
          {links.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={[
                  "rounded-md border px-3 py-2 text-sm transition",
                  active
                    ? "border-emerald-300/60 bg-emerald-300/15 text-emerald-100"
                    : "border-transparent text-slate-300 hover:border-emerald-300/25 hover:bg-emerald-300/5 hover:text-emerald-100",
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
