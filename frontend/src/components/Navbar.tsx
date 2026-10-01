import Link from "next/link";

export default function Navbar() {
  return (
    <header className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-6 sm:px-10 lg:px-16">
      <Link
        href="/"
        className="text-lg font-semibold tracking-tight text-slate-950"
        aria-label="JobBridge home"
      >
        JobBridge
      </Link>
      <nav className="flex items-center gap-5 sm:gap-8" aria-label="Account">
        <Link
          href="/login"
          className="text-sm font-medium text-slate-600 transition hover:text-slate-950"
        >
          Log in
        </Link>
        <Link
          href="/register"
          className="rounded-xl bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-800 sm:px-5"
        >
          Get Started
        </Link>
      </nav>
    </header>
  );
}
