"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { useAuth } from "./auth-context";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/map", label: "World Map" },
  { href: "/events", label: "Events" },
  { href: "/findings", label: "Findings" },
  { href: "/settings", label: "Settings" },
  { href: "/audit", label: "Audit" },
];

export function TopNav() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  return (
    <header className="sticky top-0 z-40 border-b border-emerald-400/20 bg-black/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.28em] text-emerald-300">Nyxera Eye · Ops</p>
          <p className="text-sm text-slate-300">Offensive Security Command Surface</p>
        </div>
        <div className="flex items-center gap-3">
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
          {user ? (
            <div className="flex items-center gap-2">
              <p className="font-mono text-xs uppercase tracking-[0.14em] text-cyan-200">
                {user.username} · {user.role}
              </p>
              <button
                onClick={() => logout()}
                className="rounded-md border border-rose-300/45 px-3 py-2 text-xs text-rose-200 hover:bg-rose-300/10"
              >
                Logout
              </button>
            </div>
          ) : null}
        </div>
      </div>
    </header>
  );
}
