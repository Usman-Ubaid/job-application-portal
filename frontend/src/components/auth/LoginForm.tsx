"use client";

import { useState } from "react";

export default function LoginPage() {
  const [formData, setFormData] = useState({ email: "", password: "" });

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }
  return (
    <>
      <form method="POST" action="/api/login" className="flex flex-col gap-5">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="email" className="text-slate-300 text-sm font-medium">
            Email
          </label>
          <input
            id="email"
            type="email"
            name="email"
            value={formData.email}
            placeholder="you@example.com"
            autoComplete="email"
            required
            className="bg-slate-900 border border-slate-700 text-white placeholder-slate-500 rounded-lg px-3.5 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition"
            onChange={handleChange}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label
            htmlFor="password"
            className="text-slate-300 text-sm font-medium"
          >
            Password
          </label>
          <input
            id="password"
            type="password"
            name="password"
            value={formData.password}
            placeholder="••••••••"
            autoComplete="current-password"
            required
            className="bg-slate-900 border border-slate-700 text-white placeholder-slate-500 rounded-lg px-3.5 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition"
            onChange={handleChange}
          />
        </div>

        <button
          type="submit"
          className="mt-1 w-full bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-semibold text-sm rounded-lg py-2.5 transition cursor-pointer"
        >
          Sign in
        </button>
      </form>
    </>
  );
}
