"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { LeadForm } from "@/components/ui/LeadForm";
import { CheckCircle2, Shield, Clock } from "lucide-react";

export default function BookDemoPage() {
  return (
    <main className="flex flex-col items-center">
      <PageHeader 
        title="See EduLafia in Action"
        description="Book a personalized demo with our team. Discover how we can help digitize your school's administration, health records, and fee collection."
      />

      <section className="w-full max-w-7xl mx-auto px-6 pb-24 grid md:grid-cols-5 gap-12 lg:gap-24">
        {/* Left Column: Form */}
        <div className="md:col-span-3 order-2 md:order-1 relative z-10">
          <LeadForm />
        </div>

        {/* Right Column: Info */}
        <div className="md:col-span-2 order-1 md:order-2 space-y-10">
          <div>
            <h3 className="text-2xl font-bold mb-4">What to expect:</h3>
            <p className="text-slate-400 leading-relaxed mb-6">
              A 30-minute tailored walkthrough of the platform focused on your specific challenges—whether that&apos;s fee recovery, health compliance, or parent engagement.
            </p>
          </div>

          <div className="space-y-6">
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-teal-500/20 flex items-center justify-center shrink-0">
                <CheckCircle2 className="w-5 h-5 text-teal-400" />
              </div>
              <div>
                <h4 className="font-semibold text-slate-200">No Obligation</h4>
                <p className="text-sm text-slate-400 mt-1">Get your questions answered without pressure.</p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center shrink-0">
                <Clock className="w-5 h-5 text-blue-400" />
              </div>
              <div>
                <h4 className="font-semibold text-slate-200">Quick Setup</h4>
                <p className="text-sm text-slate-400 mt-1">We can have your school running on EduLafia within 48 hours of sign-up.</p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center shrink-0">
                <Shield className="w-5 h-5 text-indigo-400" />
              </div>
              <div>
                <h4 className="font-semibold text-slate-200">NDPR Compliant</h4>
                <p className="text-sm text-slate-400 mt-1">Your data is hosted securely and meets all local regulations.</p>
              </div>
            </div>
          </div>
          
          <div className="pt-8 border-t border-slate-800">
            <p className="text-sm text-slate-500 mb-4 uppercase tracking-widest font-semibold">Join The Network</p>
            <div className="flex items-center gap-6 opacity-50 grayscale hover:grayscale-0 transition-all">
              <div className="font-bold text-xl">Private Schools</div>
              <div className="font-bold text-xl font-serif">State SUBEBs</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
