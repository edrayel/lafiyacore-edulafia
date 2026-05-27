"use client";

import { PageHeader } from "@/components/ui/PageHeader";

export default function TermsPage() {
  return (
    <main className="flex flex-col items-center">
      <PageHeader 
        title="Terms of Service"
        description="Effective Date: April 10, 2026"
      />

      <section className="w-full max-w-4xl mx-auto px-6 pb-32">
        <div className="prose prose-invert prose-teal max-w-none text-slate-300 leading-loose">
          <p>
            Welcome to EduLafia. These Terms of Service constitute a legally binding agreement made between you, 
            whether personally or on behalf of an entity &quot;you&quot; and EduLafia ("we," "us," or "our").
          </p>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">1. Agreement to Terms</h2>
          <p>
            By accessing the Site, you agree that you have read, understood, and agree to be bound by all of these 
            Terms of Service. If you do not agree with all of these terms, you are expressly prohibited from using the Site 
            and must discontinue use immediately.
          </p>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">2. Intellectual Property Rights</h2>
          <p>
            Unless otherwise indicated, the Site is our proprietary property and all source code, databases, functionality, 
            software, website designs, audio, video, text, photographs, and graphics on the Site (collectively, the "Content") 
            are owned or controlled by us.
          </p>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">3. User Representations</h2>
          <p>
            By using the Site, you represent and warrant that:
          </p>
          <ul className="list-disc pl-6 space-y-2 mt-4 text-slate-400">
            <li>All registration information you submit will be true, accurate, current, and complete.</li>
            <li>You have the legal capacity and you agree to comply with these Terms of Service.</li>
            <li>You will not access the Site through automated or non-human means.</li>
            <li>You will not use the Site for any illegal or unauthorized purpose.</li>
          </ul>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">4. Subscriptions and Billing</h2>
          <p>
            Some aspects of our services are billed on a subscription basis. You will be billed in advance on a recurring 
            and periodic basis depending on the type of subscription plan you select. At the end of each period, your 
            Subscription will automatically renew under the exact same conditions unless you cancel it or EduLafia cancels it.
          </p>

          <h2 className="text-white text-2xl font-bold mt-12 mb-6 border-b border-slate-800 pb-2">5. Limitation of Liability</h2>
          <p>
            In no event will we or our directors, employees, or agents be liable to you or any third party for any direct, 
            indirect, consequential, exemplary, incidental, special, or punitive damages arising from your use of the Site.
          </p>
        </div>
      </section>
    </main>
  );
}
