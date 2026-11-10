"use client";

import { isValidEmail } from "@/src/lib/validators";
import React, { useState } from "react";
import FieldError from "../FieldError";
import { api } from "@/src/lib/api";

interface FormData {
  email: string;
  password: string;
}

type TouchedFields = Record<keyof FormData, boolean>;
type FormErrors = Partial<Record<keyof FormData, string>>;

export default function LoginForm() {
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: "",
  });
  const [touched, setTouched] = useState<TouchedFields>({
    email: false,
    password: false,
  });
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

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

  const inputClass = (field: keyof typeof formData) => {
    const base =
      "w-full rounded-lg border bg-input-bg px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition";

    if (isInvalid(field)) return `${base} border-error focus:ring-error`;
    if (touched[field]) return `${base} border-primary focus:ring-primary`;

    return `${base} border-border focus:ring-primary`;
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof typeof formData, string>> = {};

    if (!isValidEmail(formData.email)) {
      newErrors.email = "Please enter a valid email address.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitted(true);
    if (!validate) return;
    try {
      await api.post("/v1/auth/login/", {
        email: formData.email,
        password: formData.password,
      });
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-5"
        autoComplete="off"
        noValidate
      >
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
            autoComplete="new-email"
            required
            className={inputClass("email")}
            onChange={handleChange}
            onBlur={handleBlur}
          />
          <FieldError id="email-error" message={errors.email} />
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
            autoComplete="new-password"
            required
            className={inputClass("password")}
            onChange={handleChange}
            onBlur={handleBlur}
          />
        </div>

        <button
          type="submit"
          className="mt-1 w-full bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-semibold text-sm rounded-lg py-2.5 transition cursor-pointer"
        >
          Sign in
        </button>
      </form>
      <p className="mt-6 text-center text-sm text-slate-500">
        Don&apos;t have an account?{" "}
        <a
          href="/register"
          className="font-medium text-indigo-600 hover:text-indigo-700 transition"
        >
          Register here
        </a>
      </p>
    </>
  );
}
