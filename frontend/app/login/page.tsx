/*
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
*/

"use client";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useAuth } from "../components/auth-context";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin-change-me");
  const [status, setStatus] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus("Authenticating...");
    const ok = await login(username, password);
    if (!ok) {
      setStatus("Login failed. Check credentials.");
      return;
    }
    setStatus("Authenticated. Redirecting...");
    router.replace("/");
  };

  return (
    <section className="mx-auto mt-10 w-full max-w-2xl rounded-3xl border border-emerald-300/25 bg-black/45 p-6 shadow-2xl sm:mt-16 sm:p-10">
      <div className="flex flex-col items-center text-center">
        <Image
          src="/nyxera-eye-logo.png"
          alt="Nyxera Eye"
          width={720}
          height={280}
          priority
          className="h-auto w-full max-w-xl"
        />
        <p className="mt-2 font-mono text-xs uppercase tracking-[0.26em] text-emerald-300">Nyxera Authentication</p>
        <h1 className="mt-2 text-3xl font-bold text-emerald-100 sm:text-4xl">Operator Login</h1>
      </div>
      <form onSubmit={handleSubmit} className="mx-auto mt-8 max-w-md space-y-4">
        <input
          className="w-full rounded-md border border-white/20 bg-slate-950/80 px-3 py-2 text-sm"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="w-full rounded-md border border-white/20 bg-slate-950/80 px-3 py-2 text-sm"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="w-full rounded-md border border-emerald-300/60 bg-emerald-300/15 px-3 py-2 text-sm text-emerald-100">
          Sign In
        </button>
      </form>
      {status ? <p className="mt-3 text-center text-xs text-cyan-300">{status}</p> : null}
      <p className="mt-4 text-center text-xs text-slate-300">
        No account?{" "}
        <Link href="/register" className="text-emerald-300 underline">
          Register here
        </Link>
      </p>
    </section>
  );
}
