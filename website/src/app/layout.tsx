import type { Metadata, Viewport } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

const plusJakarta = Plus_Jakarta_Sans({
  variable: "--font-plus-jakarta",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "EduLafia | Transform Your School",
  description: "Digitize school administration, health records, and parent engagement in Nigeria.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${plusJakarta.variable} font-sans antialiased bg-slate-950 text-slate-50 flex flex-col min-h-screen`}
      >
        <Navbar />
        <div className="flex-grow pt-[88px]">
          {children}
        </div>
        <Footer />
      </body>
    </html>
  );
}
