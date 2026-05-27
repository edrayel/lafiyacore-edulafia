"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { ArrowRight, CheckCircle2, Shield, Activity, Users, Wallet } from "lucide-react";
import Link from "next/link";
import { ROICalculator } from "@/components/ui/ROICalculator";

export default function Home() {
  return (
    <main className="flex flex-col items-center relative overflow-hidden -mt-[88px]">
      {/* Background Gradients */}
      <div className="absolute top-[10%] left-[-10%] w-[50%] h-[50%] bg-teal-500/10 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[60%] bg-blue-600/10 blur-[120px] rounded-full pointer-events-none" />

      {/* Hero Section */}
      <section className="w-full max-w-7xl mx-auto px-6 pt-40 pb-24 flex flex-col items-center text-center z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-teal-500/30 bg-teal-500/10 text-teal-300 text-sm font-medium mb-8"
        >
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-teal-500"></span>
          </span>
          Built for the Future of Nigerian Education
        </motion.div>
        
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-5xl md:text-7xl font-bold tracking-tight mb-8 leading-[1.1] max-w-4xl"
        >
          Transform Your School with <br className="hidden md:block" />
          <span className="text-gradient">Intelligent Administration</span>
        </motion.h1>
        
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-lg md:text-xl text-slate-400 mb-12 max-w-2xl leading-relaxed"
        >
          Digitize administration, track student health outcomes, and increase parent engagement—all from one unified platform built specifically for Nigerian schools.
        </motion.p>
        
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto"
        >
          <Button size="lg" variant="premium" className="w-full sm:w-auto group" asChild>
            <Link href="/book-demo">
              Start Free Trial
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </Button>
          <Button size="lg" variant="outline" className="w-full sm:w-auto" asChild>
            <Link href="#roi-calculator">
              Calculate Your ROI
            </Link>
          </Button>
        </motion.div>

        {/* Dashboard Mockup */}
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="w-full mt-24 relative"
        >
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent z-10 h-full w-full" />
          <div className="glass-panel rounded-2xl p-2 md:p-4 shadow-2xl relative z-0 border-t border-slate-700/50">
            <div className="bg-slate-900 rounded-xl overflow-hidden border border-slate-800 aspect-video relative flex items-center justify-center">
              {/* Placeholder for actual dashboard image */}
              <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center opacity-20" />
              <div className="relative z-10 text-center">
                <Activity className="w-16 h-16 text-teal-500/50 mx-auto mb-4" />
                <p className="text-slate-500 font-medium uppercase tracking-widest text-sm">Dashboard Interface</p>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section id="features" className="w-full max-w-7xl mx-auto px-6 py-24 z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Everything you need to run a modern school.</h2>
          <p className="text-slate-400 text-lg">Replace disjointed spreadsheets and WhatsApp groups with one cohesive system.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              title: "Smart Attendance",
              desc: "Automated daily roll calls with instant SMS/Email notifications to parents if a student is absent.",
              icon: <Users className="w-6 h-6 text-blue-400" />
            },
            {
              title: "Sentinel Health Engine",
              desc: "Track immunization records, allergies, and daily clinic visits. Built-in outbreak detection.",
              icon: <Shield className="w-6 h-6 text-teal-400" />
            },
            {
              title: "Financials & Fees",
              desc: "Automate fee collection, generate digital receipts, and track defaulters effortlessly.",
              icon: <Wallet className="w-6 h-6 text-emerald-400" />
            }
          ].map((feature, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
              className="glass-panel p-8 rounded-2xl hover:bg-slate-800/50 transition-colors"
            >
              <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mb-6 border border-slate-700">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ROI Calculator */}
      <ROICalculator />

      {/* Pricing Strategy */}
      <section id="pricing" className="w-full max-w-7xl mx-auto px-6 py-24 z-10 relative">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Transparent Pricing for Every School Size.</h2>
          <p className="text-slate-400 text-lg">No hidden fees. Designed for the Nigerian market.</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch">
          {/* STARTER */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 flex flex-col text-center">
            <h3 className="text-xl font-bold mb-2 uppercase tracking-wider text-slate-200">Starter</h3>
            <p className="text-slate-400 text-sm mb-6 italic">Up to 150 students</p>
            <div className="mb-6">
              <span className="text-sm text-slate-500 mb-1 block">IT Levy</span>
              <span className="text-2xl font-bold text-teal-400">₦3,500<span className="text-sm font-normal text-slate-400">/student/term</span></span>
            </div>
            <div className="space-y-2 text-sm text-slate-300 mb-8 bg-slate-900/50 p-4 rounded-xl">
              <p className="text-slate-500 text-xs uppercase tracking-wider mb-2">School collects</p>
              <p>₦3,500 × students/term</p>
              <p className="font-semibold text-white pt-2 border-t border-slate-800 mt-2">₦1,575,000 / year</p>
              <p className="text-teal-400 font-medium">≈ ₦131,250 / month</p>
            </div>
            <Button variant="outline" className="w-full mt-auto" asChild>
              <Link href="/book-demo">Get Started</Link>
            </Button>
          </div>

          {/* GROWING */}
          <div className="glass-panel p-6 rounded-2xl border-teal-500/50 flex flex-col text-center relative shadow-[0_0_30px_rgba(20,184,166,0.1)] bg-slate-800/80 transform lg:-translate-y-2">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-teal-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              Most Popular
            </div>
            <h3 className="text-xl font-bold mb-2 uppercase tracking-wider text-slate-200 mt-2">Growing</h3>
            <p className="text-slate-400 text-sm mb-6 italic">151 – 350 students</p>
            <div className="mb-6">
              <span className="text-sm text-slate-500 mb-1 block">IT Levy</span>
              <span className="text-2xl font-bold text-teal-400">₦3,000<span className="text-sm font-normal text-slate-400">/student/term</span></span>
            </div>
            <div className="space-y-2 text-sm text-slate-300 mb-8 bg-slate-900/50 p-4 rounded-xl">
              <p className="text-slate-500 text-xs uppercase tracking-wider mb-2">School collects</p>
              <p>₦3,000 × students/term</p>
              <p className="font-semibold text-white pt-2 border-t border-slate-800 mt-2">₦3,150,000 / year</p>
              <p className="text-teal-400 font-medium">≈ ₦262,500 / month</p>
            </div>
            <Button variant="premium" className="w-full mt-auto" asChild>
              <Link href="/book-demo">Get Started</Link>
            </Button>
          </div>

          {/* ESTABLISHED */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 flex flex-col text-center">
            <h3 className="text-xl font-bold mb-2 uppercase tracking-wider text-slate-200">Established</h3>
            <p className="text-slate-400 text-sm mb-6 italic">351 – 600 students</p>
            <div className="mb-6">
              <span className="text-sm text-slate-500 mb-1 block">IT Levy</span>
              <span className="text-2xl font-bold text-teal-400">₦2,500<span className="text-sm font-normal text-slate-400">/student/term</span></span>
            </div>
            <div className="space-y-2 text-sm text-slate-300 mb-8 bg-slate-900/50 p-4 rounded-xl">
              <p className="text-slate-500 text-xs uppercase tracking-wider mb-2">School collects</p>
              <p>₦2,500 × students/term</p>
              <p className="font-semibold text-white pt-2 border-t border-slate-800 mt-2">₦4,500,000 / year</p>
              <p className="text-teal-400 font-medium">≈ ₦375,000 / month</p>
            </div>
            <Button variant="outline" className="w-full mt-auto" asChild>
              <Link href="/book-demo">Get Started</Link>
            </Button>
          </div>

          {/* LARGE */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 flex flex-col text-center">
            <h3 className="text-xl font-bold mb-2 uppercase tracking-wider text-slate-200">Large</h3>
            <p className="text-slate-400 text-sm mb-6 italic">600+ students</p>
            <div className="mb-6">
              <span className="text-sm text-slate-500 mb-1 block">IT Levy</span>
              <span className="text-2xl font-bold text-teal-400">₦2,000<span className="text-sm font-normal text-slate-400">/student/term</span></span>
            </div>
            <div className="space-y-2 text-sm text-slate-300 mb-8 bg-slate-900/50 p-4 rounded-xl">
              <p className="text-slate-500 text-xs uppercase tracking-wider mb-2">School collects</p>
              <p>₦2,000 × students/term</p>
              <p className="font-semibold text-white pt-2 border-t border-slate-800 mt-2">₦6,000,000+ / year</p>
              <p className="text-teal-400 font-medium">≈ ₦500,000+ / month</p>
            </div>
            <Button variant="outline" className="w-full mt-auto" asChild>
              <Link href="/book-demo">Contact Sales</Link>
            </Button>
          </div>
        </div>
      </section>
    </main>
  );
}
