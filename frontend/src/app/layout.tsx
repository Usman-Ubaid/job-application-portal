import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  preload: false,
});

export const metadata: Metadata = {
  title: {
    template: "%s — JobPortal",
    default: "JobPortal",
  },
  description: "Find your next opportunity or hire great talent.",
  icons: {
    icon: "data:,",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${geistSans.variable} h-full antialiased`}>
      <body className="h-full bg-background">{children}</body>
    </html>
  );
}
