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

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("analyst");
  const [status, setStatus] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus("Creating account...");
    const ok = await register(username, password, role);
    if (!ok) {
      setStatus("Registration failed. Username may exist or password is too short.");
      return;
    }
    setStatus("Account created. Redirecting...");
    router.replace("/");
  };

  return (
    <section className="mx-auto mt-10 w-full max-w-2xl rounded-3xl border border-cyan-300/25 bg-black/45 p-6 shadow-2xl sm:mt-16 sm:p-10">
      <div className="flex flex-col items-center text-center">
        <Image
          src="/nyxera-eye-logo.png"
          alt="Nyxera Eye"
          width={720}
          height={280}
          priority
          className="h-auto w-full max-w-xl"
        />
        <p className="mt-2 font-mono text-xs uppercase tracking-[0.26em] text-cyan-300">Nyxera Identity Provisioning</p>
        <h1 className="mt-2 text-3xl font-bold text-cyan-100 sm:text-4xl">Register Operator</h1>
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
          placeholder="Password (min 10 chars)"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <select
          className="w-full rounded-md border border-white/20 bg-slate-950/80 px-3 py-2 text-sm"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="analyst">analyst</option>
          <option value="operator">operator</option>
          <option value="admin">admin</option>
        </select>
        <button className="w-full rounded-md border border-cyan-300/60 bg-cyan-300/15 px-3 py-2 text-sm text-cyan-100">
          Create Account
        </button>
      </form>
      {status ? <p className="mt-3 text-center text-xs text-cyan-300">{status}</p> : null}
      <p className="mt-4 text-center text-xs text-slate-300">
        Already registered?{" "}
        <Link href="/login" className="text-cyan-300 underline">
          Login
        </Link>
      </p>
    </section>
  );
}
