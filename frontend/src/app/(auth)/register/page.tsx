import RegisterForm from "../../../components/auth/RegisterForm";
import Link from "next/link";

export const metaData = {
  title: "Create an account - Job Portal",
};

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md space-y-6 rounded-xl bg-white p-8 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Create an account
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Already have an account?{" "}
            <Link
              href="/login"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Sign in
            </Link>
          </p>
        </div>

        <RegisterForm />
      </div>
    </main>
  );
}
