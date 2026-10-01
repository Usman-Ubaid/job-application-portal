"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import axiosInstance from "@/lib/axios";
import Navbar from "@/components/Navbar";

type EmploymentType = "FT" | "PT" | "C" | "I";

interface Job {
  id: number;
  title: string;
  description: string;
  location: string | null;
  salary_range: string | null;
  employment_type: EmploymentType;
}

const employmentLabels: Record<EmploymentType, string> = {
  FT: "Full-time",
  PT: "Part-time",
  C: "Contract",
  I: "Internship",
};

export default function JobDetailPage() {
  const params = useParams<{ id: string }>();
  const [job, setJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadJob = async () => {
      try {
        const response = await axiosInstance.get<Job>(`/jobs/${params.id}/`);
        setJob(response.data);
      } catch {
        setError("We couldn’t find this job. It may have been removed.");
      } finally {
        setIsLoading(false);
      }
    };
    void loadJob();
  }, [params.id]);

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar />

      <section className="mx-auto max-w-5xl px-5 py-8 sm:px-8 sm:py-12">
        <Link
          className="text-sm font-medium text-blue-700 hover:text-blue-800"
          href="/"
        >
          ← All jobs
        </Link>
        {isLoading && (
          <p className="py-16 text-center text-sm text-slate-600" role="status">
            Loading job details…
          </p>
        )}
        {!isLoading && error && (
          <div className="mx-auto max-w-xl py-16 text-center" role="alert">
            <h1 className="text-2xl font-semibold tracking-tight text-slate-950">
              Job unavailable
            </h1>
            <p className="mt-3 text-sm leading-6 text-slate-600">{error}</p>
            <Link
              className="mt-6 inline-flex rounded-xl bg-blue-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-800"
              href="/"
            >
              Browse jobs
            </Link>
          </div>
        )}
        {!isLoading && job && (
          <article className="mt-8 overflow-hidden rounded-xl border border-slate-200 bg-white">
            <header className="border-b border-slate-200 px-5 py-6 sm:px-8 sm:py-8">
              <h1 className="text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
                {job.title}
              </h1>
              <p className="mt-4 text-sm text-slate-600">
                {employmentLabels[job.employment_type]}
                <span className="mx-2 text-slate-300" aria-hidden="true">
                  ·
                </span>
                {job.location || "Location flexible"}
                {job.salary_range && (
                  <>
                    <span className="mx-2 text-slate-300" aria-hidden="true">
                      ·
                    </span>
                    {job.salary_range}
                  </>
                )}
              </p>
            </header>
            <div className="px-5 py-6 sm:px-8 sm:py-8">
              <h2 className="text-lg font-semibold text-slate-950">
                About this role
              </h2>
              <p className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-600">
                {job.description}
              </p>
              <Link
                className="mt-8 inline-flex rounded-xl bg-blue-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-800"
                href="/register"
              >
                Create an account to apply
              </Link>
            </div>
          </article>
        )}
      </section>
    </main>
  );
}
