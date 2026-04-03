import { useState, useEffect } from 'react';
import { fetchAlerts } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadAlerts();
    const interval = setInterval(loadAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  async function loadAlerts() {
    try {
      const data = await fetchAlerts();
      const list = Array.isArray(data) ? data : (data.alerts || []);
      setAlerts(list);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  const filtered = alerts.filter(a => {
    if (filter === 'all') return true;
    if (filter === 'high') return a.risk_score >= 70;
    if (filter === 'block') return a.action === 'BLOCK';
    if (filter === 'mfa') return a.action === 'MFA';
    return true;
  });

  return (
    <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-12 max-w-[1800px] mx-auto px-6 py-6"
    >
      {/* Header (Orca Style) */}
      <div className="flex items-center justify-between border-b border-white/5 pb-10">
        <div className="space-y-1">
            <h1 className="text-3xl font-display font-bold text-white tracking-tight">Security Events</h1>
            <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">{alerts.length} neural signatures detected</p>
        </div>
        <div className="flex space-x-4">
             {['all', 'high', 'block', 'mfa'].map(f => (
                <button 
                  key={f} 
                  onClick={() => setFilter(f)}
                  className={`text-[10px] px-6 py-2.5 rounded-xl font-black uppercase tracking-widest border transition-all duration-200
                              ${filter === f 
                                ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30' 
                                : 'text-slate-500 border-white/5 hover:border-white/10 hover:text-white'}`}
                >
                  {f === 'all' ? 'FULL_LOG' : f === 'high' ? 'CRITICAL' : f.toUpperCase()}
                </button>
             ))}
        </div>
      </div>

      {loading ? (
        <div className="p-40 text-center text-[10px] font-black uppercase tracking-[0.4em] text-slate-600 italic animate-pulse">Syncing Event Logs...</div>
      ) : (
        <div className="orca-card p-0 overflow-hidden group border-white/5 shadow-[0_0_80px_rgba(0,0,0,0.5)]">
            <div className="overflow-x-auto">
                <table className="w-full text-left">
                    <thead>
                        <tr className="text-[10px] text-slate-500 uppercase tracking-widest font-black italic border-b border-white/5">
                            <th className="px-10 py-6"><input type="checkbox" className="w-4 h-4 rounded border-white/10 bg-transparent" /></th>
                            <th className="px-10 py-6">Date and Time</th>
                            <th className="px-10 py-6">Event Type</th>
                            <th className="px-10 py-6">Source Node</th>
                            <th className="px-10 py-6">Risk Level</th>
                            <th className="px-10 py-6">Status Trace</th>
                            <th className="px-10 py-6 text-right">Export</th>
                        </tr>
                    </thead>
                    <tbody className="text-[11px] font-bold">
                        <AnimatePresence mode="popLayout">
                            {filtered.slice().reverse().map((a, i) => (
                                <motion.tr 
                                    layout
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ scale: 0.9, opacity: 0 }}
                                    key={a.alert_id} 
                                    className="orca-table-row group/row"
                                >
                                    <td className="px-10 py-7"><input type="checkbox" className="w-4 h-4 rounded border-white/10 bg-transparent" /></td>
                                    <td className="px-10 py-7 text-slate-400 font-mono italic">{new Date(a.timestamp * 1000).toLocaleString()}</td>
                                    <td className="px-10 py-7">
                                        <span className={`px-4 py-1.5 rounded-lg border ${a.action === 'BLOCK' ? 'bg-red-500/10 text-red-400 border-red-500/20' : a.action === 'MFA' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'} uppercase tracking-widest leading-none`}>
                                            {a.event_type || 'TRANSACTION'}
                                        </span>
                                    </td>
                                    <td className="px-10 py-7 text-slate-500 font-mono tracking-tighter truncate max-w-[150px]">{a.sender_id}</td>
                                    <td className="px-10 py-7">
                                        <div className="flex items-center space-x-3">
                                            <div className={`w-10 h-1 rounded-full ${a.risk_score >= 70 ? 'bg-red-500' : a.risk_score >= 40 ? 'bg-amber-500' : 'bg-blue-500'} opacity-30 group-hover/row:opacity-100 transition-opacity`} />
                                            <span className={`text-[10px] uppercase font-black tracking-widest ${a.risk_score >= 70 ? 'text-red-500' : 'text-slate-300'}`}>{a.risk_level}</span>
                                        </div>
                                    </td>
                                    <td className="px-10 py-7 text-slate-600 italic font-medium">Neural confirmation {a.risk_score.toFixed(1)}%</td>
                                    <td className="px-10 py-7 text-right text-slate-600 group-hover/row:text-white transition-colors cursor-pointer text-sm">📤</td>
                                </motion.tr>
                            ))}
                        </AnimatePresence>
                    </tbody>
                </table>
            </div>
        </div>
      )}
    </motion.div>
  );
}