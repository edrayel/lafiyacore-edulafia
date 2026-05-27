import Link from "next/link";
import { Activity } from "lucide-react";

export function Footer() {
  return (
    <footer className="w-full border-t border-slate-800 bg-slate-950 z-10 relative mt-auto">
      <div className="max-w-7xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="col-span-1 md:col-span-1">
          <Link href="/" className="flex items-center gap-2 mb-4">
            <Activity className="w-6 h-6 text-teal-500" />
            <span className="text-xl font-bold">EduLafia</span>
          </Link>
          <p className="text-slate-500 text-sm leading-relaxed mb-6">
            Digitizing school administration, health records, and parent engagement.
            <br />Built for Nigeria.
          </p>
          <p className="text-slate-600 text-xs">© 2026 EduLafia. All rights reserved.</p>
        </div>
        
        <div>
          <h4 className="font-semibold mb-4 text-slate-200">Solutions</h4>
          <ul className="space-y-3 text-sm text-slate-400">
            <li><Link href="/solutions/private-schools" className="hover:text-white transition-colors">Private Schools</Link></li>
            <li><Link href="/solutions/government" className="hover:text-white transition-colors">Government & SUBEB</Link></li>
            <li><Link href="/#pricing" className="hover:text-white transition-colors">Pricing</Link></li>
            <li><Link href="/book-demo" className="hover:text-white transition-colors text-teal-400">Book a Demo</Link></li>
          </ul>
        </div>
        
        <div>
          <h4 className="font-semibold mb-4 text-slate-200">Company</h4>
          <ul className="space-y-3 text-sm text-slate-400">
            <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
            <li><Link href="/security" className="hover:text-white transition-colors">Trust & Security</Link></li>
            <li><a href="mailto:hello@edulafia.com" className="hover:text-white transition-colors">Contact Support</a></li>
          </ul>
        </div>
        
        <div>
          <h4 className="font-semibold mb-4 text-slate-200">Legal</h4>
          <ul className="space-y-3 text-sm text-slate-400">
            <li><Link href="/legal/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
            <li><Link href="/legal/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
