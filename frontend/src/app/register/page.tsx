"use client";

import axiosInstance from "@/lib/axios";
import Link from "next/link";
import React, { useState } from "react";

const RegisterPage = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [role, setRole] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isRegistered, setIsRegistered] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    if (password !== password2) {
      setError("Your passwords do not match. Please try again.");
      return;
    }

    setIsSubmitting(true);
    try {
      await axiosInstance.post("/auth/register/", {
        username,
        email,
        password,
        password2,
        role,
      });
      setIsRegistered(true);
    } catch {
      setError(
        "We couldn't create your account. Check your details and try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="grid min-h-screen lg:grid-cols-2">
        <section className="relative isolate flex min-h-64 flex-col justify-between overflow-hidden bg-linear-to-br from-slate-950 via-blue-950 to-indigo-950 px-7 py-8 text-white sm:px-12 sm:py-10 lg:min-h-screen lg:px-16 lg:py-14">
          <div
            aria-hidden="true"
            className="absolute -right-32 -top-36 -z-10 size-96 rounded-full border border-white/10"
          />
          <div
            aria-hidden="true"
            className="absolute -right-16 -top-20 -z-10 size-64 rounded-full border border-white/10"
          />
          <div
            aria-hidden="true"
            className="absolute -bottom-48 -left-32 -z-10 size-96 rounded-full bg-blue-500/20 blur-3xl"
          />

          <Link
            href="/"
            className="inline-flex w-fit items-center"
            aria-label="JobBridge home"
          >
            <span className="text-lg font-semibold tracking-tight">
              JobBridge
            </span>
          </Link>

          <div className="relative max-w-xl py-10 lg:py-0">
            <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-blue-300/20 bg-blue-300/10 px-3.5 py-1.5 text-xs font-medium tracking-wide text-blue-100">
              <span className="size-1.5 rounded-full bg-emerald-400" />
              YOUR NEXT CHAPTER STARTS HERE
            </p>
            <h1 className="max-w-lg text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
              Make your next move with JobBridge.
            </h1>
            <p className="mt-5 max-w-md text-base leading-7 text-blue-100/75 sm:text-lg">
              Create an account to discover opportunities or find the right
              people for your team.
            </p>
          </div>

          <p className="hidden text-xs text-blue-100/50 lg:block">
            © {new Date().getFullYear()} JobBridge. Built for what&apos;s next.
          </p>
        </section>

        <section className="flex items-center justify-center px-6 py-12 sm:px-10 lg:px-16">
          <div className="w-full max-w-md">
            <div className="mb-8 lg:hidden">
              <Link
                href="/"
                className="inline-flex items-center"
                aria-label="JobBridge home"
              >
                <span className="text-lg font-semibold tracking-tight text-slate-950">
                  JobBridge
                </span>
              </Link>
            </div>

            <div className="mb-8">
              <p className="mb-3 text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">
                Join JobBridge
              </p>
            </div>
            {isRegistered ? (
              <div
                role="status"
                className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-4 text-sm leading-6 text-emerald-900"
              >
                <p className="font-semibold">Your account has been created.</p>
                <p className="mt-1">
                  You can now{" "}
                  <Link
                    href="/login"
                    className="font-semibold underline underline-offset-2"
                  >
                    sign in
                  </Link>
                  .
                </p>
              </div>
            ) : (
              <>
                <h2 className="text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
                  Create your account
                </h2>
                <form onSubmit={handleSubmit} className="space-y-5">
                  {error && (
                    <div
                      role="alert"
                      className="flex gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm leading-6 text-red-800"
                    >
                      <svg
                        aria-hidden="true"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        className="mt-0.5 size-5 shrink-0"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm0-11a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 10 7Zm0 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z"
                          clipRule="evenodd"
                        />
                      </svg>
                      <p>{error}</p>
                    </div>
                  )}

                  <div>
                    <label
                      htmlFor="username"
                      className="mb-2 block text-sm font-medium text-slate-800"
                    >
                      Username <span aria-hidden="true">*</span>
                    </label>
                    <input
                      id="username"
                      autoComplete="username"
                      placeholder="Choose a username"
                      required
                      name="username"
                      type="text"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      className="block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 hover:border-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-600/10"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="email"
                      className="mb-2 block text-sm font-medium text-slate-800"
                    >
                      Email address <span aria-hidden="true">*</span>
                    </label>
                    <input
                      id="email"
                      autoComplete="email"
                      placeholder="you@example.com"
                      required
                      name="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 hover:border-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-600/10"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="password"
                      className="mb-2 block text-sm font-medium text-slate-800"
                    >
                      Password <span aria-hidden="true">*</span>
                    </label>
                    <input
                      id="password"
                      autoComplete="new-password"
                      placeholder="Create a password"
                      required
                      name="password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 hover:border-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-600/10"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="password2"
                      className="mb-2 block text-sm font-medium text-slate-800"
                    >
                      Repeat password <span aria-hidden="true">*</span>
                    </label>
                    <input
                      id="password2"
                      autoComplete="new-password"
                      placeholder="Enter your password again"
                      required
                      name="password2"
                      type="password"
                      value={password2}
                      onChange={(e) => setPassword2(e.target.value)}
                      className="block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 hover:border-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-600/10"
                    />
                  </div>

                  <div>
                    <label
                      htmlFor="role"
                      className="mb-2 block text-sm font-medium text-slate-800"
                    >
                      I am a <span aria-hidden="true">*</span>
                    </label>
                    <select
                      id="role"
                      required
                      name="role"
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                      className="block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-base text-slate-900 shadow-sm outline-none transition hover:border-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-600/10"
                    >
                      <option value="" disabled>
                        Select your role
                      </option>
                      <option value="SK">Seeker</option>
                      <option value="EP">Employer</option>
                    </select>
                  </div>

                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-blue-700 px-5 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-900/15 transition hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
                  >
                    {isSubmitting && (
                      <svg
                        aria-hidden="true"
                        viewBox="0 0 24 24"
                        fill="none"
                        className="size-4 animate-spin"
                      >
                        <circle
                          cx="12"
                          cy="12"
                          r="9"
                          stroke="currentColor"
                          strokeOpacity=".25"
                          strokeWidth="3"
                        />
                        <path
                          d="M21 12a9 9 0 0 0-9-9"
                          stroke="currentColor"
                          strokeLinecap="round"
                          strokeWidth="3"
                        />
                      </svg>
                    )}
                    {isSubmitting ? "Creating account..." : "Create account"}
                  </button>
                </form>
              </>
            )}

            {!isRegistered && (
              <p className="mt-8 text-center text-sm text-slate-500">
                Already have an account?{" "}
                <Link
                  href="/login"
                  className="font-semibold text-blue-700 underline-offset-4 hover:underline"
                >
                  Sign in
                </Link>
              </p>
            )}
          </div>
        </section>
      </div>
    </main>
  );
};

export default RegisterPage;
