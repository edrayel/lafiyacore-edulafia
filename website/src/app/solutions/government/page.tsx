"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { Button } from "@/components/ui/Button";
import { motion } from "framer-motion";
import { ShieldAlert, BarChart3, Globe, Database } from "lucide-react";
import Link from "next/link";

export default function GovernmentPage() {
  return (
    <main className="flex flex-col items-center">
      <PageHeader 
        title="State-Scale Education & Health Intelligence"
        description="Deploy EduLafia across hundreds of public schools. Gain real-time visibility into attendance, infrastructure, and student health outcomes for policy decisions."
        badge="For State MOE & SUBEB"
      >
        <Button size="lg" variant="premium" asChild>
          <Link href="/book-demo">Request State Pilot</Link>
        </Button>
      </PageHeader>

      <section className="w-full max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-16 items-center">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Actionable Data at State Level</h2>
          <p className="text-slate-400 mb-8 leading-relaxed text-lg">
            Move beyond annual census surveys. EduLafia provides State Ministries of Education and SUBEB with real-time analytics across all local governments.
          </p>
          <ul className="space-y-4 text-slate-300">
            <li className="flex items-start gap-3">
              <Globe className="w-6 h-6 text-teal-500 shrink-0 mt-0.5" />
              <span><strong>State Dashboard:</strong> Aggregate metrics for 1,000+ schools.</span>
            </li>
            <li className="flex items-start gap-3">
              <BarChart3 className="w-6 h-6 text-teal-500 shrink-0 mt-0.5" />
              <span><strong>Attendance Tracking:</strong> Monitor true out-of-school rates.</span>
            </li>
            <li className="flex items-start gap-3">
              <Database className="w-6 h-6 text-teal-500 shrink-0 mt-0.5" />
              <span><strong>Offline Capable:</strong> Works in low-bandwidth rural environments.</span>
            </li>
          </ul>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="glass-panel p-8 rounded-2xl relative border-teal-500/30"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-teal-500/10 to-blue-500/10 rounded-2xl pointer-events-none" />
          <h3 className="text-2xl font-bold mb-6 text-white relative z-10 flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-teal-400" />
            The Sentinel Engine
          </h3>
          <p className="text-slate-400 leading-relaxed relative z-10 mb-6">
            EduLafia goes beyond administration by tracking daily clinic visits and immunization records. Our proprietary <strong>Sentinel Engine</strong> acts as an early warning system for State Ministries of Health, detecting localized outbreak patterns (e.g., Cholera, Malaria) before they spread.
          </p>
          <Button variant="outline" className="relative z-10 w-full" asChild>
            <Link href="/book-demo">Learn About Health Data Integrations</Link>
          </Button>
        </motion.div>
      </section>

      <section className="w-full bg-slate-900/50 border-y border-slate-800/50 py-24">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-3xl font-bold mb-6">Donor-Funded Deployments</h2>
          <p className="text-slate-400 mb-8 text-lg">
            We partner with NGOs (UNICEF, USAID, Gates Foundation) to deploy EduLafia in underserved public schools through grant coverage. 
          </p>
          <Button size="lg" variant="premium" asChild>
            <Link href="/book-demo">Contact Our Partnerships Team</Link>
          </Button>
        </div>
      </section>
    </main>
  );
}
