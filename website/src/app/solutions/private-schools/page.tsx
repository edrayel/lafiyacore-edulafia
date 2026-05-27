"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { Button } from "@/components/ui/Button";
import { motion } from "framer-motion";
import { CheckCircle2, Users, Receipt, CalendarClock, Smartphone } from "lucide-react";
import Link from "next/link";

export default function PrivateSchoolsPage() {
  return (
    <main className="flex flex-col items-center">
      <PageHeader 
        title="Modernize Your Private School"
        description="Stop losing time to manual record keeping and unpaid fee tracking. EduLafia automates your administration so you can focus on academic excellence."
        badge="For Proprietors & Headteachers"
      >
        <Button size="lg" variant="premium" asChild>
          <Link href="/book-demo">Calculate Your Savings</Link>
        </Button>
      </PageHeader>

      <section className="w-full max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-16 items-center">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-6">The True Cost of Manual Processes</h2>
          <p className="text-slate-400 mb-8 leading-relaxed text-lg">
            Nigerian private schools spend an average of 15 hours per week chasing fee payments, compiling paper attendance, and managing fragmented WhatsApp groups.
          </p>
          <ul className="space-y-4 text-slate-300">
            <li className="flex items-start gap-3">
              <CheckCircle2 className="w-6 h-6 text-rose-500 shrink-0 mt-0.5" />
              <span><strong>Lost Revenue:</strong> Delayed fee tracking means missed payments.</span>
            </li>
            <li className="flex items-start gap-3">
              <CheckCircle2 className="w-6 h-6 text-rose-500 shrink-0 mt-0.5" />
              <span><strong>Wasted Time:</strong> Teachers act as administrators instead of educators.</span>
            </li>
            <li className="flex items-start gap-3">
              <CheckCircle2 className="w-6 h-6 text-rose-500 shrink-0 mt-0.5" />
              <span><strong>Parent Friction:</strong> Lack of real-time visibility causes complaints.</span>
            </li>
          </ul>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="glass-panel p-8 rounded-2xl relative"
        >
          <div className="absolute -inset-1 bg-gradient-to-r from-teal-500 to-blue-500 rounded-2xl blur opacity-20" />
          <div className="relative bg-slate-900 rounded-xl p-6 border border-slate-800">
            <h3 className="text-xl font-bold mb-4 text-teal-400">The EduLafia Advantage</h3>
            <div className="space-y-6">
              <div className="flex gap-4">
                <Receipt className="w-8 h-8 text-teal-500 shrink-0" />
                <div>
                  <h4 className="font-semibold text-slate-200">Automated Fee Collection</h4>
                  <p className="text-sm text-slate-400">Direct Paystack integration with automated SMS reminders for defaulters.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <CalendarClock className="w-8 h-8 text-teal-500 shrink-0" />
                <div>
                  <h4 className="font-semibold text-slate-200">Smart Attendance</h4>
                  <p className="text-sm text-slate-400">Instant digital roll calls with auto-notification to parents for absentees.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <Smartphone className="w-8 h-8 text-teal-500 shrink-0" />
                <div>
                  <h4 className="font-semibold text-slate-200">Parent Portal</h4>
                  <p className="text-sm text-slate-400">Give parents real-time access to health records, fees, and results.</p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      <section className="w-full bg-slate-900/50 border-y border-slate-800/50 py-24">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-3xl font-bold mb-6">Ready to modernize your school's administration?</h2>
          <p className="text-slate-400 mb-8 text-lg">
            Start with our ₦60,000/year Starter plan and see the difference in your first term.
          </p>
          <Button size="lg" variant="premium" asChild>
            <Link href="/book-demo">Book a Live Demo</Link>
          </Button>
        </div>
      </section>
    </main>
  );
}
