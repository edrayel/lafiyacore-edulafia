"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { useState } from "react";
import { Send, CheckCircle2, Loader2 } from "lucide-react";

export function LeadForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setIsSubmitting(false);
    setIsSuccess(true);
  };

  if (isSuccess) {
    return (
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-panel p-10 rounded-2xl border-teal-500/30 text-center bg-slate-900"
      >
        <div className="w-16 h-16 rounded-full bg-teal-500/20 flex items-center justify-center mx-auto mb-6">
          <CheckCircle2 className="w-8 h-8 text-teal-400" />
        </div>
        <h3 className="text-2xl font-bold mb-4 text-white">Demo Requested!</h3>
        <p className="text-slate-400 mb-8">
          Thank you. Our team will contact you shortly to schedule your personalized EduLafia demo.
        </p>
        <Button variant="outline" onClick={() => setIsSuccess(false)}>Send Another Request</Button>
      </motion.div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="glass-panel p-8 md:p-10 rounded-2xl bg-slate-900 shadow-2xl">
      <div className="space-y-6">
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label htmlFor="name" className="text-sm font-medium text-slate-300 block">Full Name</label>
            <input 
              required
              id="name" 
              name="name" 
              type="text" 
              placeholder="e.g., Jane Doe"
              className="w-full h-12 bg-slate-950 border border-slate-800 rounded-lg px-4 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 transition-all"
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium text-slate-300 block">Work Email</label>
            <input 
              required
              id="email" 
              name="email" 
              type="email" 
              placeholder="jane@school.edu.ng"
              className="w-full h-12 bg-slate-950 border border-slate-800 rounded-lg px-4 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 transition-all"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label htmlFor="school" className="text-sm font-medium text-slate-300 block">School Name</label>
          <input 
            required
            id="school" 
            name="school" 
            type="text" 
            placeholder="e.g., Excellence International Academy"
            className="w-full h-12 bg-slate-950 border border-slate-800 rounded-lg px-4 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 transition-all"
          />
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label htmlFor="role" className="text-sm font-medium text-slate-300 block">Your Role</label>
            <select 
              required
              id="role" 
              name="role" 
              className="w-full h-12 bg-slate-950 border border-slate-800 rounded-lg px-4 text-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 transition-all appearance-none"
            >
              <option value="" disabled selected>Select Role</option>
              <option value="proprietor">Proprietor / Owner</option>
              <option value="headteacher">Headteacher / Principal</option>
              <option value="admin">Administrator</option>
              <option value="government">Government Official</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div className="space-y-2">
            <label htmlFor="size" className="text-sm font-medium text-slate-300 block">Student Count</label>
            <select 
              required
              id="size" 
              name="size" 
              className="w-full h-12 bg-slate-950 border border-slate-800 rounded-lg px-4 text-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 transition-all appearance-none"
            >
              <option value="" disabled selected>Select Size</option>
              <option value="1-200">1 - 200 (Starter Tier)</option>
              <option value="201-500">201 - 500 (Standard Tier)</option>
              <option value="500+">500+ (Premium Tier)</option>
              <option value="state">State / Multi-school Network</option>
            </select>
          </div>
        </div>

        <Button type="submit" variant="premium" size="lg" className="w-full mt-4" disabled={isSubmitting}>
          {isSubmitting ? (
            <Loader2 className="w-5 h-5 animate-spin mx-auto" />
          ) : (
            <>
              Request Demo
              <Send className="ml-2 w-5 h-5" />
            </>
          )}
        </Button>
        <p className="text-xs text-center text-slate-500 mt-4">
          By submitting this form, you agree to our Privacy Policy and Terms of Service.
        </p>
      </div>
    </form>
  );
}
