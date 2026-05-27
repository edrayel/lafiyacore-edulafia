"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { ShieldCheck, Lock, Server, FileCheck } from "lucide-react";

export default function SecurityPage() {
  return (
    <main className="flex flex-col items-center">
      <PageHeader 
        title="Enterprise-Grade Security"
        description="Because you entrust us with your students' financial and health records, security is our foundational pillar. We adhere to strict local and international standards."
        badge="Trust Center"
      />

      <section className="w-full max-w-5xl mx-auto px-6 pb-24 grid md:grid-cols-2 gap-8">
        <div className="glass-panel p-8 rounded-2xl border-l-4 border-teal-500">
          <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mb-6">
            <Lock className="w-6 h-6 text-teal-400" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-white">End-to-End Encryption</h3>
          <p className="text-slate-400 leading-relaxed">
            All data in transit is encrypted using TLS 1.3, and data at rest is encrypted via AES-256. We ensure sensitive health and financial records remain impenetrable.
          </p>
        </div>

        <div className="glass-panel p-8 rounded-2xl border-l-4 border-blue-500">
          <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mb-6">
            <FileCheck className="w-6 h-6 text-blue-400" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-white">NDPR Compliance</h3>
          <p className="text-slate-400 leading-relaxed">
            EduLafia is fully compliant with the Nigeria Data Protection Regulation (NDPR). You maintain full ownership of your data at all times.
          </p>
        </div>

        <div className="glass-panel p-8 rounded-2xl border-l-4 border-indigo-500">
          <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mb-6">
            <Server className="w-6 h-6 text-indigo-400" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-white">Reliable Infrastructure</h3>
          <p className="text-slate-400 leading-relaxed">
            Hosted on secure cloud infrastructure with multi-zone redundancy, ensuring 99.9% uptime even during peak fee-collection periods.
          </p>
        </div>

        <div className="glass-panel p-8 rounded-2xl border-l-4 border-emerald-500">
          <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center mb-6">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-white">Role-Based Access</h3>
          <p className="text-slate-400 leading-relaxed">
            Granular access controls ensure teachers only see what they need, while sensitive financial and health data is restricted to authorized administrators.
          </p>
        </div>
      </section>
    </main>
  );
}
