"use client";

import { PageHeader } from "@/components/ui/PageHeader";
import { Activity, Target, Flag } from "lucide-react";

export default function AboutPage() {
  return (
    <main className="flex flex-col items-center">
      <PageHeader 
        title="Built for Nigeria"
        description="We're on a mission to modernize educational infrastructure across Nigeria, ensuring every child's academic and health data is secure, accessible, and actionable."
      />

      <section className="w-full max-w-4xl mx-auto px-6 pb-24">
        <div className="prose prose-invert max-w-none">
          <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-3">
            <Target className="w-6 h-6 text-teal-500" />
            Our Story
          </h2>
          <p className="text-slate-300 text-lg leading-relaxed mb-8">
            EduLafia was born out of a stark realization: Nigerian schools were struggling under the weight of manual administration, and critical health data was being lost in paper files. We built a platform that not only handles the day-to-day operations—like fee collection and attendance—but also acts as a sentinel for student health.
          </p>

          <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-3">
            <Flag className="w-6 h-6 text-blue-500" />
            Our Mission
          </h2>
          <p className="text-slate-300 text-lg leading-relaxed mb-12">
            To bridge the gap between education and health in Nigeria by providing a unified, intelligent platform that empowers educators, engages parents, and informs state-level policy.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="glass-panel p-6 rounded-xl border-t-2 border-teal-500">
            <div className="text-4xl font-bold text-white mb-2">9+</div>
            <div className="text-slate-400 font-medium">Core Modules</div>
          </div>
          <div className="glass-panel p-6 rounded-xl border-t-2 border-blue-500">
            <div className="text-4xl font-bold text-white mb-2">1</div>
            <div className="text-slate-400 font-medium">Unified Platform</div>
          </div>
          <div className="glass-panel p-6 rounded-xl border-t-2 border-indigo-500">
            <div className="text-4xl font-bold text-white mb-2">100%</div>
            <div className="text-slate-400 font-medium">NDPR Compliant</div>
          </div>
        </div>
      </section>
    </main>
  );
}
