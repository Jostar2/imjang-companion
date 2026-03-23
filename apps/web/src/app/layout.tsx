import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Imjang Companion MVP",
  description: "Mobile-first field visit workflow for real-estate comparison."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
