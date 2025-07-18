import type { Metadata, Viewport } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "PDF Query Assistant",
  description: "Upload PDFs and ask questions about their content using AI",
  keywords: ["PDF", "AI", "Chat", "Document Analysis", "Query"],
  authors: [{ name: "PDF Query Assistant" }],
};

// ✅ Move viewport into its own export
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased">{children}</body>
    </html>
  );
}
