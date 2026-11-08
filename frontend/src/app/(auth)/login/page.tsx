import LoginForm from "../../../components/auth/LoginForm";

export const metaData = {
  title: "Create an account - Job Portal",
};

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md space-y-6 rounded-xl bg-white p-8 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Sign in</h1>
          <p className="mt-1 text-sm text-gray-500">
            Enter your credentials to continue
          </p>
        </div>

        <LoginForm />
      </div>
    </main>
  );
}
