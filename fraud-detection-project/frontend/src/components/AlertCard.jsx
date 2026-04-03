import { useState, useEffect } from 'react';

const AlertCard = ({ alert }) => {
  const [showDetails, setShowDetails] = useState(false);
  
  const risk_color = alert.risk_score >= 70 ? 'text-red-400' : alert.risk_score >= 40 ? 'text-orange-400' : 'text-green-400';
  const risk_bg = alert.risk_score >= 70 ? 'bg-red-400/5 border-red-400/10' : alert.risk_score >= 40 ? 'bg-orange-400/5 border-orange-400/10' : 'bg-green-400/5 border-green-400/10';

  return (
    <div className={`p-5 rounded-2xl border ${risk_bg} transition-all hover:scale-[1.01] cursor-pointer group fade-in`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`w-2 h-2 rounded-full ${risk_color.replace('text', 'bg')} animate-pulse shrink-0`}></div>
          <div className="flex flex-col">
            <span className="text-xs font-bold text-white uppercase tracking-widest">{alert.action || 'REVIEW'}</span>
            <span className="text-[10px] text-[#718096] font-mono">{alert.alert_id}</span>
          </div>
        </div>
        <div className="flex flex-col items-end">
           <span className={`text-2xl font-black font-display ${risk_color}`}>{alert.risk_score}</span>
           <span className="text-[10px] text-[#718096] uppercase">Risk Index</span>
        </div>
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center justify-between text-xs">
           <span className="text-slate-500">Flow</span>
           <span className="text-white font-mono">{alert.sender_id} → {alert.receiver_id || 'N/A'}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
           <span className="text-slate-500">Amount</span>
           <span className="text-white font-bold">Rs. {alert.amount?.toLocaleString() || 0}</span>
        </div>
      </div>

      <div className="space-y-1">
         {alert.reasons?.slice(0, 2).map((r, i) => (
           <div key={i} className="text-[10px] text-slate-400 flex items-center space-x-2">
              <span className={risk_color}>›</span>
              <span>{r}</span>
           </div>
         ))}
      </div>

      <div className="mt-4 pt-4 border-t border-white/5 flex items-center justify-between">
         <span className="text-[9px] text-slate-600 font-mono italic">Signature: {alert.pattern || 'Anomaly'}</span>
         <span className="text-[9px] text-[#3182ce] hover:underline font-bold" onClick={() => setShowDetails(!showDetails)}>
            {showDetails ? 'Hide Forensics' : 'View Full Trace'}
         </span>
      </div>
      
      {showDetails && (
        <div className="mt-4 p-3 bg-black/20 rounded-xl space-y-2 border border-white/5 fade-in">
           <div className="text-[9px] text-[#718096] uppercase flex justify-between">
              <span>Risk Classification</span>
              <span>{alert.reason_categories ? Object.keys(alert.reason_categories).filter(k => alert.reason_categories[k].length > 0).join(', ') : 'Hybrid'}</span>
           </div>
           <div className="h-1 w-full bg-white/5 rounded-full">
              <div className="h-full bg-[#3182ce] w-[80%]"></div>
           </div>
        </div>
      )}
    </div>
  );
}

export default AlertCard;