import { AuthProvider } from "@/context/AuthContext";

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <AuthProvider>
      <html lang="en">
        <body className="min-h-full flex flex-col">{children}</body>
      </html>
    </AuthProvider>
  );
}
