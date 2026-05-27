"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { ArrowRight, Shield, Users, Wallet } from "lucide-react";
import Link from "next/link";
import { ROICalculator } from "@/components/ui/ROICalculator";

export default function Home() {
  return (
    <main className="flex flex-col items-center relative overflow-hidden -mt-[88px]">
      <div className="absolute top-[10%] left-[-10%] w-[50%] h-[50%] bg-teal-500/10 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[60%] bg-blue-600/10 blur-[120px] rounded-full pointer-events-none" />

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

        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="w-full mt-24 relative"
        >
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent z-10 h-full w-full pointer-events-none" />
          <div className="glass-panel rounded-2xl p-2 md:p-4 shadow-2xl relative z-0 border-t border-slate-700/50">
            <div className="bg-slate-900 rounded-xl overflow-hidden border border-slate-800 aspect-video relative flex items-center justify-center">
              <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800/80 to-slate-900" />
              <div className="absolute top-0 left-0 right-0 h-12 bg-slate-800/60 flex items-center px-4 gap-2 z-10">
                <div className="w-3 h-3 rounded-full bg-red-500/60" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
                <div className="w-3 h-3 rounded-full bg-green-500/60" />
                <div className="ml-4 h-2 w-32 rounded-full bg-slate-700/50" />
              </div>
              <div className="absolute inset-0 flex items-center justify-center z-10 pt-6">
                <div className="grid grid-cols-3 gap-4 p-8 w-full max-w-2xl">
                  {[
                    { label: "Students", value: "1,247", color: "bg-blue-500/20 border-blue-500/30" },
                    { label: "Attendance", value: "96%", color: "bg-teal-500/20 border-teal-500/30" },
                    { label: "Alerts", value: "3", color: "bg-amber-500/20 border-amber-500/30" },
                  ].map((stat, i) => (
                    <div key={i} className={`rounded-xl p-4 border ${stat.color} backdrop-blur-sm`}>
                      <div className="text-slate-500 text-xs mb-1 font-medium">{stat.label}</div>
                      <div className="text-2xl font-bold text-white">{stat.value}</div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-teal-500/30 to-transparent" />
            </div>
          </div>
        </motion.div>
      </section>

      <section id="features" className="w-full max-w-7xl mx-auto px-6 py-24 z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Everything you need to run a modern school.</h2>
          <p className="text-slate-400 text-lg">Replace disjointed spreadsheets and WhatsApp groups with one cohesive system.</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { title: "Smart Attendance", desc: "Automated daily roll calls with instant SMS/Email notifications to parents if a student is absent.", icon: <Users className="w-6 h-6 text-blue-400" /> },
            { title: "Sentinel Health Engine", desc: "Track immunization records, allergies, and daily clinic visits. Built-in outbreak detection.", icon: <Shield className="w-6 h-6 text-teal-400" /> },
            { title: "Financials & Fees", desc: "Automate fee collection, generate digital receipts, and track defaulters effortlessly.", icon: <Wallet className="w-6 h-6 text-emerald-400" /> },
          ].map((feature, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
              className="glass-panel p-8 rounded-2xl hover:bg-slate-800/50 transition-colors"
            >
              <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mb-6 border border-slate-700">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <ROICalculator />

      <section id="pricing" className="w-full max-w-7xl mx-auto px-6 py-24 z-10 relative">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">Transparent Pricing for Every School Size.</h2>
          <p className="text-slate-400 text-lg">No hidden fees. Designed for the Nigerian market.</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 items-stretch">
          {[
            { name: "Starter", students: "Up to 150 students", levy: 3500, yearly: 1575000, monthly: 131250, btn: "Get Started", popular: false },
            { name: "Growing", students: "151 – 350 students", levy: 3000, yearly: 3150000, monthly: 262500, btn: "Get Started", popular: true },
            { name: "Established", students: "351 – 600 students", levy: 2500, yearly: 4500000, monthly: 375000, btn: "Get Started", popular: false },
            { name: "Large", students: "600+ students", levy: 2000, yearly: 6000000, monthly: 500000, btn: "Contact Sales", popular: false },
          ].map((plan) => (
            <div 
              key={plan.name}
              className={`glass-panel p-6 rounded-2xl flex flex-col text-center ${plan.popular ? "border-teal-500/50 shadow-[0_0_30px_rgba(20,184,166,0.1)] bg-slate-800/80 transform lg:-translate-y-2 relative" : "border-slate-800"}`}
            >
              {plan.popular && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-teal-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Most Popular</div>
              )}
              <h3 className="text-xl font-bold mb-2 uppercase tracking-wider text-slate-200">{plan.popular ? <span className="mt-2 inline-block">{plan.name}</span> : plan.name}</h3>
              <p className="text-slate-400 text-sm mb-6 italic">{plan.students}</p>
              <div className="mb-6">
                <span className="text-sm text-slate-500 mb-1 block">IT Levy</span>
                <span className="text-2xl font-bold text-teal-400">₦{plan.levy.toLocaleString()}<span className="text-sm font-normal text-slate-400">/student/term</span></span>
              </div>
              <div className="space-y-2 text-sm text-slate-300 mb-8 bg-slate-900/50 p-4 rounded-xl">
                <p className="text-slate-500 text-xs uppercase tracking-wider mb-2">School collects</p>
                <p>₦{plan.levy.toLocaleString()} × students/term</p>
                <p className="font-semibold text-white pt-2 border-t border-slate-800 mt-2">₦{plan.yearly.toLocaleString()} / year</p>
                <p className="text-teal-400 font-medium">≈ ₦{plan.monthly.toLocaleString()} / month</p>
              </div>
              <Button variant={plan.popular ? "premium" : "outline"} className="w-full mt-auto" asChild>
                <Link href="/book-demo">{plan.btn}</Link>
              </Button>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
