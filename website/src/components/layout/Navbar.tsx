"use client";

import Link from "next/link";
import { Activity, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { useState, useEffect, useCallback } from "react";

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const closeMobile = useCallback(() => setMobileOpen(false), []);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [mobileOpen]);

  return (
    <nav 
      className={`fixed top-0 left-0 right-0 w-full z-50 transition-all duration-300 ${
        scrolled ? "bg-slate-950/80 backdrop-blur-lg border-b border-slate-800/50 py-4" : "bg-transparent py-6"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white">EduLafia</span>
        </Link>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
          <Link href="/#features" className="hover:text-teal-400 transition-colors">Features</Link>
          <Link href="/#pricing" className="hover:text-teal-400 transition-colors">Pricing</Link>
          <div className="relative group">
            <span className="hover:text-teal-400 transition-colors cursor-pointer py-2">Solutions</span>
            <div className="absolute top-full left-0 mt-2 w-48 bg-slate-900 border border-slate-800 rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all flex flex-col overflow-hidden">
              <Link href="/solutions/private-schools" className="px-4 py-3 hover:bg-slate-800 transition-colors">Private Schools</Link>
              <Link href="/solutions/government" className="px-4 py-3 hover:bg-slate-800 transition-colors">Government & Scale</Link>
            </div>
          </div>
          <Link href="/about" className="hover:text-teal-400 transition-colors">About</Link>
        </div>
        
        <div className="flex items-center gap-4">
          <Button variant="ghost" className="hidden md:inline-flex" asChild>
            <a href="https://app.edulafia.com">Sign In</a>
          </Button>
          <Button variant="premium" className="hidden md:inline-flex" asChild>
            <Link href="/book-demo">Book a Demo</Link>
          </Button>
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-slate-300 hover:text-white transition-colors"
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div
          className="fixed inset-0 top-0 left-0 w-full h-screen bg-slate-950/95 backdrop-blur-md z-40 md:hidden"
          onClick={closeMobile}
        >
          <div className="flex flex-col items-center justify-center h-full gap-8 text-lg" onClick={(e) => e.stopPropagation()}>
            <Link href="/#features" onClick={closeMobile} className="text-slate-300 hover:text-teal-400 transition-colors text-xl font-medium">Features</Link>
            <Link href="/#pricing" onClick={closeMobile} className="text-slate-300 hover:text-teal-400 transition-colors text-xl font-medium">Pricing</Link>
            <Link href="/solutions/private-schools" onClick={closeMobile} className="text-slate-300 hover:text-teal-400 transition-colors text-xl font-medium">Private Schools</Link>
            <Link href="/solutions/government" onClick={closeMobile} className="text-slate-300 hover:text-teal-400 transition-colors text-xl font-medium">Government</Link>
            <Link href="/about" onClick={closeMobile} className="text-slate-300 hover:text-teal-400 transition-colors text-xl font-medium">About</Link>
            <Link href="/security" onClick={closeMobile} className="text-slate-300 hover:text-teal-400 transition-colors text-xl font-medium">Trust & Security</Link>
            <hr className="w-16 border-slate-700" />
            <Button variant="outline" asChild>
              <a href="https://app.edulafia.com">Sign In</a>
            </Button>
            <Button variant="premium" asChild>
              <Link href="/book-demo" onClick={closeMobile}>Book a Demo</Link>
            </Button>
          </div>
        </div>
      )}
    </nav>
  );
}
