"use client";

import { isValidEmail, isValidRole } from "@/src/lib/validators";
import React, { useState } from "react";
import FieldError from "../FieldError";

interface FormData {
  email: string;
  firstName: string;
  lastName: string;
  role: "seeker" | "employer";
  password: string;
  confirmPassword: string;
}

type TouchedFields = Record<keyof FormData, boolean>;
type FormErrors = Partial<Record<keyof FormData, string>>;

export default function RegisterForm() {
  const [formData, setFormData] = useState<FormData>({
    email: "",
    firstName: "",
    lastName: "",
    role: "seeker",
    password: "",
    confirmPassword: "",
  });

  const [touched, setTouched] = useState<TouchedFields>({
    email: false,
    firstName: false,
    lastName: false,
    role: false,
    password: false,
    confirmPassword: false,
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleBlur = (
    e: React.FocusEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name } = e.target;

    setTouched((prev) => ({ ...prev, [name]: true }));
  };

  const isInvalid = (field: keyof typeof formData) => {
    const isEmpty = formData[field] === "";
    return (touched[field] && isEmpty) || (submitted && isEmpty);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof typeof formData, string>> = {};

    if (!isValidEmail(formData.email)) {
      newErrors.email = "Please enter a valid email address.";
    }

    if (!isValidRole(formData.role)) {
      newErrors.role = "Invalid role selected.";
    }

    if (formData.confirmPassword !== formData.password) {
      newErrors.confirmPassword = "Passwords do not match.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const inputClass = (field: keyof typeof formData) => {
    const base =
      "w-full rounded-lg border bg-input-bg px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition";

    if (isInvalid(field)) return `${base} border-error focus:ring-error`;
    if (touched[field]) return `${base} border-primary focus:ring-primary`;

    return `${base} border-border focus:ring-primary`;
  };

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitted(true);
    if (!validate()) return;
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="space-y-5" noValidate>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="firstName"
              className="text-sm font-medium text-gray-700"
            >
              First name
            </label>
            <input
              id="firstName"
              name="firstName"
              autoComplete="given-name"
              value={formData.firstName}
              type="text"
              placeholder="Jane"
              className={inputClass("firstName")}
              onChange={handleChange}
              onBlur={handleBlur}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="lastName"
              className="text-sm font-medium text-gray-700"
            >
              Last name
            </label>
            <input
              id="lastName"
              name="lastName"
              autoComplete="family-name"
              value={formData.lastName}
              type="text"
              placeholder="Doe"
              className={inputClass("lastName")}
              onChange={handleChange}
              onBlur={handleBlur}
            />
          </div>
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="email" className="text-sm font-medium text-gray-700">
            Email address
          </label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            autoComplete="email"
            placeholder="jane@example.com"
            className={inputClass("email")}
            onChange={handleChange}
            onBlur={handleBlur}
          />
          <FieldError id="email-error" message={errors.email} />
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="role" className="text-sm font-medium text-gray-700">
            I am a
          </label>
          <div className="relative">
            <select
              id="role"
              name="role"
              value={formData.role}
              className={`${inputClass("role")} appearance-none`}
              onChange={handleChange}
              onBlur={handleBlur}
            >
              <option value="" disabled>
                Select a role
              </option>
              <option value="seeker">Job Seeker</option>
              <option value="employer">Employer</option>
            </select>

            <span className="pointer-events-none absolute inset-y-0 right-3 flex items-center text-slate-400">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                className="w-4 h-4"
              >
                <path
                  fillRule="evenodd"
                  d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z"
                  clipRule="evenodd"
                />
              </svg>
            </span>
          </div>
          <FieldError id="role-error" message={errors.role} />
        </div>

        <div className="flex flex-col gap-1.5">
          <label
            htmlFor="password"
            className="text-sm font-medium text-gray-700"
          >
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            autoComplete="new-password"
            placeholder="At least 8 characters"
            className={inputClass("password")}
            onChange={handleChange}
            onBlur={handleBlur}
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label
            htmlFor="confirmPassword"
            className="text-sm font-medium text-gray-700"
          >
            Confirm password
          </label>
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            placeholder="Repeat your password"
            className={inputClass("confirmPassword")}
            onChange={handleChange}
            onBlur={handleBlur}
          />
          <FieldError
            id="confirmPassword-error"
            message={errors.confirmPassword}
          />
        </div>

        <button
          type="submit"
          className="w-full mt-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 active:bg-indigo-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition"
        >
          Create account
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-500">
        Already have an account?{" "}
        <a
          href="/login"
          className="font-medium text-indigo-600 hover:text-indigo-700 transition"
        >
          Sign in
        </a>
      </p>
    </>
  );
}
