export default function RegisterForm() {
  return (
    <main className="min-h-screen bg-slate-50 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border border-slate-100 px-8 py-10">
        <div className="mb-8">
          <div className="border-l-4 border-indigo-600 pl-3 mb-1">
            <h1 className="text-2xl font-semibold tracking-tight text-gray-900">
              Create your account
            </h1>
          </div>
          <p className="text-sm text-slate-500 mt-2">
            Join thousands of professionals on the platform.
          </p>
        </div>

        <form className="space-y-5" noValidate>
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
                type="text"
                placeholder="Jane"
                className="w-full rounded-lg border bg-slate-50 px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition border-slate-200 focus:ring-indigo-500"
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
                type="text"
                placeholder="Doe"
                className="w-full rounded-lg border bg-slate-50 px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition border-slate-200 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="email"
              className="text-sm font-medium text-gray-700"
            >
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="jane@example.com"
              className="w-full rounded-lg border bg-slate-50 px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition border-slate-200 focus:ring-indigo-500"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label htmlFor="role" className="text-sm font-medium text-gray-700">
              I am a
            </label>
            <div className="relative">
              <select
                id="role"
                name="role"
                className="w-full rounded-lg border bg-slate-50 px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition border-slate-200 focus:ring-indigo-500 appearance-none"
                defaultValue=""
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
              placeholder="At least 8 characters"
              className="w-full rounded-lg border bg-slate-50 px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition border-slate-200 focus:ring-indigo-500"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label
              htmlFor="password2"
              className="text-sm font-medium text-gray-700"
            >
              Confirm password
            </label>
            <input
              id="password2"
              name="password2"
              type="password"
              placeholder="Repeat your password"
              className="w-full rounded-lg border bg-slate-50 px-3 py-2.5 text-sm text-gray-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:border-transparent transition border-slate-200 focus:ring-indigo-500"
            />
          </div>

          <button
            type="button"
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
      </div>
    </main>
  );
}
