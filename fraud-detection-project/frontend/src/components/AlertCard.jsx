import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const AlertCard = ({ alert }) => {
  const [showDetails, setShowDetails] = useState(false);
  
  const getActionColor = (action) => {
    switch (action) {
      case 'BLOCK': return 'text-red-500 bg-red-500/10 border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.1)]';
      case 'MFA': return 'text-amber-500 bg-amber-500/10 border-amber-500/20 shadow-[0_0_15px_rgba(245,158,11,0.1)]';
      default: return 'text-green-500 bg-green-500/10 border-green-500/20 shadow-[0_0_15px_rgba(34,197,94,0.1)]';
    }
  };

  const riskColor = alert.risk_score >= 70 ? 'text-red-500' : alert.risk_score >= 40 ? 'text-amber-500' : 'text-green-500';

  return (
    <div className={`card group relative overflow-hidden transition-all hover:bg-[#1a1c2e] ${alert.risk_score >= 70 ? 'border-red-500/30' : ''}`}>
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-white/5 to-transparent rounded-bl-full pointer-events-none" />
      
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center relative z-10">
        {/* Risk Score Sphere */}
        <div className="md:col-span-2 flex flex-col items-center justify-center p-2 border-r border-[#2d3748]">
            <div className={`w-14 h-14 rounded-full border-2 flex items-center justify-center transition-all duration-700
                ${alert.risk_score >= 70 ? 'border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.4)]' : 'border-[#3182ce] shadow-[0_0_15px_rgba(49,130,206,0.2)]'}
            `}>
                <span className="text-sm font-black text-white">{alert.risk_score.toFixed(0)}</span>
            </div>
            <span className="text-[8px] font-black uppercase text-slate-500 mt-2 tracking-widest">{alert.risk_level}</span>
        </div>

        {/* Intelligence Data */}
        <div className="md:col-span-6 space-y-3">
          <div className="flex items-center space-x-3">
            <span className="text-white font-black text-xs tracking-tighter uppercase tabular-nums">{alert.transaction_id.slice(0, 16)}...</span>
            <span className={`px-3 py-0.5 rounded-full text-[9px] font-black border uppercase tracking-widest ${getActionColor(alert.action)}`}>
               {alert.action}
            </span>
          </div>
          
          <div className="flex flex-wrap gap-2">
            {(alert.reasons || []).slice(0, 3).map((r, i) => (
              <span key={i} className="text-[9px] px-2 py-0.5 bg-[#05060F] text-[#718096] rounded-md border border-[#2d3748] flex items-center space-x-1.5 group-hover:border-[#3182ce]/30 transition-colors">
                <span className={`w-1 h-1 rounded-full ${riskColor.replace('text', 'bg')}`}></span>
                <span className="truncate max-w-[150px]">{typeof r === 'object' ? r.message : r}</span>
              </span>
            ))}
          </div>
        </div>

        {/* Forensic Metadata */}
        <div className="md:col-span-3 grid grid-cols-2 gap-4 border-l border-[#2d3748] pl-6 py-2">
             <div className="space-y-1">
                <span className="text-[7px] text-slate-600 font-bold uppercase block">Amount</span>
                <span className="text-xs font-black text-white italic">Rs. {alert.amount.toLocaleString()}</span>
             </div>
             <div className="space-y-1">
                <span className="text-[7px] text-slate-600 font-bold uppercase block">Pulse</span>
                <span className="text-xs font-black text-white">{new Date(alert.timestamp * 1000).toLocaleTimeString()}</span>
             </div>
        </div>

        {/* Investigative CTA */}
        <div className="md:col-span-1 flex justify-end">
          <Link 
            to={`/investigator?account=${alert.sender_id}`} 
            className="w-10 h-10 rounded-xl bg-[#2d3748]/50 border border-[#2d3748] flex items-center justify-center text-slate-400 hover:text-[#3182ce] hover:border-[#3182ce] hover:bg-[#3182ce]/10 transition-all shadow-lg"
          >
            <span className="text-xl">→</span>
          </Link>
        </div>
      </div>
      
      {/* Retraining Feedback if applicable */}
      {alert.is_pre_transaction_check && (
         <div className="mt-4 pt-4 border-t border-white/5 flex items-center justify-between text-[10px] text-indigo-400 font-black uppercase tracking-widest italic animate-pulse">
            Neural Simulation Feed Active
         </div>
      )}
    </div>
  );
};

export default AlertCard;