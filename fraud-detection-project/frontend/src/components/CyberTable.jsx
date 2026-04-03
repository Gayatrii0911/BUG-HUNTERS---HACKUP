import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, ShieldCheck, ShieldAlert, Cpu, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const CyberTable = ({ alerts }) => {
  const navigate = useNavigate();

  return (
    <div className="w-full overflow-x-auto glass rounded-2xl border border-white/5 shadow-2xl">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-cyber-border bg-white/5">
            <th className="px-6 py-4 text-[10px] uppercase font-bold text-slate-500 tracking-widest">ID / Timestamp</th>
            <th className="px-6 py-4 text-[10px] uppercase font-bold text-slate-500 tracking-widest">User Intelligence</th>
            <th className="px-6 py-4 text-[10px] uppercase font-bold text-slate-500 tracking-widest">Risk Index</th>
            <th className="px-6 py-4 text-[10px] uppercase font-bold text-slate-500 tracking-widest">Action Status</th>
            <th className="px-6 py-4 text-[10px] uppercase font-bold text-slate-500 tracking-widest">ML Category</th>
            <th className="px-6 py-4 text-[10px] uppercase font-bold text-slate-500 tracking-widest">Forensics</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-cyber-border/50">
          {alerts.map((alert, i) => (
            <motion.tr 
              key={alert.alert_id || i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="hover:bg-white/5 transition-colors group cursor-crosshair"
            >
              <td className="px-6 py-3">
                <div className="flex flex-col">
                  <span className="text-[10px] font-mono text-cyan-400 font-bold tracking-tighter">
                    {alert.transaction_id?.slice(0, 13)}...
                  </span>
                  <span className="text-[9px] text-slate-600 mt-1 uppercase font-bold">
                    {new Date().toLocaleTimeString()}
                  </span>
                </div>
              </td>
              <td className="px-6 py-3">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-cyber-bg border border-cyber-border flex items-center justify-center text-cyber-accent">
                    <Cpu className="w-4 h-4" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-slate-300">{alert.sender_id || alert.user_id}</span>
                    <span className="text-[9px] text-slate-600 font-bold uppercase tracking-widest">Account ID Verified</span>
                  </div>
                </div>
              </td>
              <td className="px-6 py-3">
                <div className="flex items-center space-x-2">
                  <div className={`h-1.5 w-12 rounded-full bg-cyber-border overflow-hidden`}>
                    <motion.div 
                      className={`h-full ${alert.risk_score >= 70 ? 'bg-cyber-danger' : alert.risk_score >= 40 ? 'bg-cyber-warning' : 'bg-cyber-success'}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${alert.risk_score}%` }}
                    />
                  </div>
                  <span className={`text-xs font-black font-display ${alert.risk_score >= 70 ? 'text-cyber-danger' : alert.risk_score >= 40 ? 'text-cyber-warning' : 'text-cyber-success'}`}>
                    {alert.risk_score?.toFixed(1)}
                  </span>
                </div>
              </td>
              <td className="px-6 py-3">
                <div className={`inline-flex items-center px-3 py-1 rounded-md text-[10px] font-black uppercase tracking-widest space-x-2
                                ${alert.decision === 'BLOCK' ? 'bg-cyber-danger/10 text-cyber-danger border border-cyber-danger/20' : 
                                  alert.decision === 'MFA' ? 'bg-cyber-warning/10 text-cyber-warning border border-cyber-warning/20' : 
                                  'bg-cyber-success/10 text-cyber-success border border-cyber-success/20'}`}>
                  {alert.decision === 'BLOCK' ? <ShieldAlert className="w-3 h-3" /> : alert.decision === 'MFA' ? <AlertTriangle className="w-3 h-3" /> : <ShieldCheck className="w-3 h-3" />}
                  <span>{alert.decision}</span>
                </div>
              </td>
              <td className="px-6 py-3">
                <span className="text-[10px] font-mono text-slate-500 uppercase font-black tracking-widest">
                  {alert.fraud_type || 'unclassified'}
                </span>
              </td>
              <td className="px-6 py-3">
                <button 
                  onClick={() => navigate(`/investigator?id=${alert.transaction_id || alert.sender_id || alert.user_id}`)}
                  className="p-2 bg-cyber-accent/10 border border-cyber-accent/30 rounded-lg text-cyber-accent hover:bg-cyber-accent hover:text-cyber-bg transition-all group/btn"
                  title="Deep Forensic Trace"
                >
                  <Search className="w-3 h-3 group-hover/btn:scale-125 transition-transform" />
                </button>
              </td>
            </motion.tr>
          ))}
        </tbody>
      </table>
      {alerts.length === 0 && (
         <div className="p-20 text-center flex flex-col items-center justify-center space-y-4">
            <Cpu className="w-12 h-12 text-cyber-border animate-pulse" />
            <span className="text-xs font-black text-slate-600 uppercase tracking-widest">No active threats detected in sync buffer</span>
         </div>
      )}
    </div>
  );
};

export default CyberTable;
