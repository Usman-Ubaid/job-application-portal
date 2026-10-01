"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import axios from "axios";
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
  company_name: string | null;
  company_address: string | null;
  created_at: string;
}

type PostedWithin = "any" | "day" | "week" | "month";

const employmentLabels: Record<EmploymentType, string> = {
  FT: "Full-time",
  PT: "Part-time",
  C: "Contract",
  I: "Internship",
};

const postedWithinOptions: Array<{ label: string; value: PostedWithin }> = [
  { label: "Any time", value: "any" },
  { label: "Past 24 hours", value: "day" },
  { label: "Past week", value: "week" },
  { label: "Past month", value: "month" },
];

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [currentTime, setCurrentTime] = useState<number | null>(null);
  const [postedWithin, setPostedWithin] = useState<PostedWithin>("any");
  const [employmentType, setEmploymentType] = useState<EmploymentType | "all">(
    "all"
  );

  const filteredJobs = useMemo(() => {
    const durations: Record<Exclude<PostedWithin, "any">, number> = {
      day: 24 * 60 * 60 * 1000,
      week: 7 * 24 * 60 * 60 * 1000,
      month: 30 * 24 * 60 * 60 * 1000,
    };
    const cutoff =
      postedWithin === "any" || currentTime === null
        ? null
        : currentTime - durations[postedWithin];

    return jobs.filter((job) => {
      const matchesType =
        employmentType === "all" || job.employment_type === employmentType;
      const postedAt = new Date(job.created_at).getTime();
      const matchesDate = cutoff === null || postedAt >= cutoff;
      return matchesType && matchesDate;
    });
  }, [currentTime, employmentType, jobs, postedWithin]);

  useEffect(() => {
    const loadJobs = async () => {
      try {
        const response = await axiosInstance.get<unknown>("/jobs/");
        const data = response.data;
        if (
          data === null ||
          data === undefined ||
          (typeof data === "object" &&
            !Array.isArray(data) &&
            Object.keys(data).length === 0)
        ) {
          setJobs([]);
        } else if (Array.isArray(data)) {
          setJobs(data);
        } else {
          setError(
            "The jobs service returned an unexpected response. Please try again later."
          );
        }
      } catch (requestError) {
        if (axios.isAxiosError(requestError) && requestError.response) {
          setError(
            `The jobs service returned an error (${requestError.response.status}). Please try again later.`
          );
        } else if (axios.isAxiosError(requestError)) {
          setError(
            "We couldn’t connect to the jobs service. Check your connection and try again."
          );
        } else {
          setError("An unexpected error occurred while loading jobs.");
        }
      } finally {
        setCurrentTime(Date.now());
        setIsLoading(false);
      }
    };
    void loadJobs();
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar />

      <section className="mx-auto max-w-5xl px-5 py-8 sm:px-8 sm:py-12">
        <h1 className="mb-6 text-2xl font-semibold tracking-tight text-slate-950 sm:text-3xl">
          Open Jobs
        </h1>
        {isLoading && (
          <p className="py-8 text-center text-sm text-slate-600" role="status">
            Loading jobs…
          </p>
        )}
        {!isLoading && error && (
          <div
            className="rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-800"
            role="alert"
          >
            <h2 className="font-semibold">Unable to load jobs</h2>
            <p className="mt-1">{error}</p>
          </div>
        )}
        {!isLoading && !error && jobs.length === 0 && (
          <p className="py-8 text-center text-sm text-slate-600">
            No jobs are available right now.
          </p>
        )}
        {!isLoading && !error && jobs.length > 0 && (
          <div>
            <div className="mb-6 flex flex-col gap-4 rounded-xl border border-slate-200 bg-white p-4 sm:flex-row sm:items-center">
              <label className="flex flex-1 flex-col gap-1.5 text-sm font-medium text-slate-700">
                Posted
                <select
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none focus:border-blue-600 focus:ring-4 focus:ring-blue-600/10"
                  value={postedWithin}
                  onChange={(event) =>
                    setPostedWithin(event.target.value as PostedWithin)
                  }
                >
                  {postedWithinOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
              <label className="flex flex-1 flex-col gap-1.5 text-sm font-medium text-slate-700">
                Employment type
                <select
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none focus:border-blue-600 focus:ring-4 focus:ring-blue-600/10"
                  value={employmentType}
                  onChange={(event) =>
                    setEmploymentType(
                      event.target.value as EmploymentType | "all"
                    )
                  }
                >
                  <option value="all">All types</option>
                  {Object.entries(employmentLabels).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </label>
            </div>
            {filteredJobs.length === 0 ? (
              <p className="rounded-xl border border-slate-200 bg-white py-8 text-center text-sm text-slate-600">
                No jobs match these filters.
              </p>
            ) : (
              <div className="grid gap-4 sm:grid-cols-2">
                {filteredJobs.map((job) => (
                  <article
                    className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-blue-200 hover:shadow-md sm:p-6"
                    key={job.id}
                  >
                    <div className="min-w-0">
                      <h2 className="text-lg font-semibold tracking-tight text-slate-950">
                        <Link
                          className="transition hover:text-blue-700"
                          href={`/jobs/${job.id}`}
                        >
                          {job.title}
                        </Link>
                      </h2>
                      <div className="mt-2 space-y-1 text-sm">
                        <p className="font-medium text-slate-800">
                          {job.company_name || "Company not provided"}
                        </p>
                        <p className="text-slate-600">
                          {job.company_address ||
                            job.location ||
                            "Address not provided"}
                        </p>
                        <p className="text-slate-600">
                          {employmentLabels[job.employment_type]}
                        </p>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
