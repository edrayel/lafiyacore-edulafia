"use client";

import { PageHeader } from "@/components/ui/PageHeader";

export default function PrivacyPage() {
  return (
    <main className="flex flex-col items-center">
      <PageHeader 
        title="Privacy Policy"
        description="Effective Date: April 10, 2026"
      />

      <section className="w-full max-w-4xl mx-auto px-6 pb-32">
        <div className="prose prose-invert prose-teal max-w-none text-slate-300 leading-loose">
          <p>
            Welcome to EduLafia. We are committed to protecting your personal information and your right to privacy. 
            This Privacy Policy applies to all information collected through our website, application, and related services.
          </p>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">1. Information We Collect</h2>
          <p>
            We collect personal information that you voluntarily provide to us when you register on the Services, 
            express an interest in obtaining information about us or our products, or when you contact us.
          </p>
          <ul className="list-disc pl-6 space-y-2 mt-4 text-slate-400">
            <li><strong>School Administrators:</strong> Name, work email, school name, phone number, and role.</li>
            <li><strong>Students & Parents:</strong> Educational records, attendance data, fee payment history, and health records (immunizations, allergies) as provided by the school.</li>
          </ul>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">2. How We Use Your Information</h2>
          <p>
            We use personal information collected via our Services for a variety of business purposes described below:
          </p>
          <ul className="list-disc pl-6 space-y-2 mt-4 text-slate-400">
            <li>To facilitate account creation and logon process.</li>
            <li>To send administrative information to you (e.g., fee reminders, attendance alerts).</li>
            <li>To fulfill and manage orders and payments.</li>
            <li>To protect our Services (e.g., fraud monitoring).</li>
            <li>To generate anonymized, aggregated health intelligence for state-level outbreak detection.</li>
          </ul>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">3. Data Security and Compliance</h2>
          <p>
            We have implemented appropriate technical and organizational security measures designed to protect the security 
            of any personal information we process. We are fully compliant with the Nigeria Data Protection Regulation (NDPR).
          </p>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">4. Contact Us</h2>
          <p>
            If you have questions or comments about this notice, you may email us at privacy@edulafia.com.
          </p>
        </div>
      </section>
    </main>
  );
}
