"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Calculator, ArrowRight } from "lucide-react";
import { Button } from "./Button";
import Link from "next/link";

export function ROICalculator() {
  const [students, setStudents] = useState<number>(250);
  const [avgFee, setAvgFee] = useState<number>(50000);

  // Business Logic for ROI
  const TERMS_PER_YEAR = 3;
  const PAPER_SMS_COST_PER_STUDENT = 500; // ₦500 per student per term for printing/SMS
  const DELAYED_FEE_RECOVERY_RATE = 0.03; // Assume 3% of total revenue is recovered that would otherwise be lost

  const totalRevenue = students * avgFee * TERMS_PER_YEAR;
  const recoveredRevenue = totalRevenue * DELAYED_FEE_RECOVERY_RATE;
  const paperSavings = students * PAPER_SMS_COST_PER_STUDENT * TERMS_PER_YEAR;
  const totalSavings = recoveredRevenue + paperSavings;

  const getLevy = (count: number) => {
    if (count <= 150) return 3500;
    if (count <= 350) return 3000;
    if (count <= 600) return 2500;
    return 2000;
  };

  const levyPerTerm = getLevy(students);
  const edulafiaCost = students * levyPerTerm * TERMS_PER_YEAR;
  
  // Since the IT Levy is passed to parents, the actual cost to the school is 0. 
  // The net ROI is simply the total savings/recovered fees.
  const netROI = totalSavings;

  const formatCurrency = (num: number) => {
    return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN', maximumFractionDigits: 0 }).format(num);
  };

  return (
    <section id="roi-calculator" className="w-full max-w-7xl mx-auto px-6 py-24 z-10 relative">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-5xl font-bold mb-4 flex items-center justify-center gap-4">
          <Calculator className="w-10 h-10 text-teal-500" />
          Calculate Your ROI
        </h2>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          See how much your school can save by automating fee collection, digitizing records, and eliminating paper waste.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-12 items-start">
        {/* Left: Inputs */}
        <div className="glass-panel p-8 rounded-2xl bg-slate-900 border-slate-800">
          <div className="space-y-8">
            <div>
              <div className="flex justify-between mb-4">
                <label className="text-slate-300 font-medium">Number of Students</label>
                <span className="text-teal-400 font-bold text-xl">{students}</span>
              </div>
              <input 
                type="range" 
                min="50" 
                max="1000" 
                step="10" 
                value={students}
                onChange={(e) => setStudents(Number(e.target.value))}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-500"
              />
              <div className="flex justify-between mt-2 text-xs text-slate-500">
                <span>50</span>
                <span>1000+</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-4">
                <label className="text-slate-300 font-medium">Average Fee Per Term</label>
                <span className="text-teal-400 font-bold text-xl">{formatCurrency(avgFee)}</span>
              </div>
              <input 
                type="range" 
                min="10000" 
                max="500000" 
                step="5000" 
                value={avgFee}
                onChange={(e) => setAvgFee(Number(e.target.value))}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-500"
              />
              <div className="flex justify-between mt-2 text-xs text-slate-500">
                <span>₦10,000</span>
                <span>₦500,000+</span>
              </div>
            </div>
            
            <div className="pt-6 border-t border-slate-800">
              <p className="text-sm text-slate-400 leading-relaxed">
                * Our model assumes EduLafia&apos;s automated reminders recover just <strong>3%</strong> of delayed or lost fees, and eliminates <strong>₦500</strong> per student per term in paper/SMS costs.
              </p>
            </div>
          </div>
        </div>

        {/* Right: Results */}
        <motion.div 
          key={`${students}-${avgFee}`}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="glass-panel p-8 rounded-2xl relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-teal-500/10 blur-[80px] rounded-full pointer-events-none" />
          
          <h3 className="text-xl font-bold mb-8 text-white">Estimated Annual Impact</h3>
          
          <div className="space-y-6 relative z-10">
            <div className="flex justify-between items-center pb-4 border-b border-slate-800">
              <span className="text-slate-400">Recovered Fees & Savings</span>
              <span className="text-2xl font-bold text-emerald-400">+{formatCurrency(totalSavings)}</span>
            </div>
            
            <div className="flex justify-between items-center pb-4 border-b border-slate-800">
              <span className="text-slate-400">Annual IT Levy (Passed to Parents)</span>
              <span className="text-xl font-semibold text-slate-300">{formatCurrency(edulafiaCost)}</span>
            </div>

            <div className="pt-4">
              <span className="text-slate-400 block mb-2">Net ROI (Value Created for School)</span>
              <div className="flex items-end gap-4">
                <span className="text-5xl font-bold text-white tracking-tight">{formatCurrency(netROI)}</span>
              </div>
              <p className="text-teal-400 font-medium mt-3">
                Since the IT Levy is covered by parents, 100% of these operational savings go directly to your bottom line.
              </p>
            </div>
            
            <Button variant="premium" size="lg" className="w-full mt-8 group" asChild>
              <Link href="/book-demo">
                Unlock These Savings
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}