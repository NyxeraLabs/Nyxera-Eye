"use client";

import { usePathname, useRouter } from "next/navigation";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { fetchCurrentUser, loginUser, logoutUser, registerUser } from "../lib/api";
import type { AuthUser } from "../lib/types";

type AuthContextValue = {
  user: AuthUser | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  register: (username: string, password: string, role?: string) => Promise<boolean>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const PUBLIC_PATHS = new Set<string>(["/login", "/register"]);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    fetchCurrentUser()
      .then((nextUser) => {
        if (!mounted) {
          return;
        }
        setUser(nextUser);
      })
      .finally(() => {
        if (mounted) {
          setLoading(false);
        }
      });
    return () => {
      mounted = false;
    };
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      loading,
      login: async (username: string, password: string) => {
        const next = await loginUser(username, password);
        setUser(next);
        return Boolean(next);
      },
      register: async (username: string, password: string, role: string = "analyst") => {
        const next = await registerUser(username, password, role);
        setUser(next);
        return Boolean(next);
      },
      logout: async () => {
        await logoutUser();
        setUser(null);
      },
    }),
    [loading, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function AuthGate({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    if (loading) {
      return;
    }
    if (PUBLIC_PATHS.has(pathname)) {
      return;
    }
    if (!user) {
      router.replace("/login");
    }
  }, [loading, pathname, router, user]);

  if (loading && !PUBLIC_PATHS.has(pathname)) {
    return (
      <main className="mx-auto w-full max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <section className="rounded-2xl border border-white/10 bg-black/30 p-6 text-sm text-slate-300">
          Loading authenticated operator context...
        </section>
      </main>
    );
  }

  if (!user && !PUBLIC_PATHS.has(pathname)) {
    return null;
  }

  return <>{children}</>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
