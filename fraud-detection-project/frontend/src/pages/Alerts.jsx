import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { fetchAlerts } from '../services/api';
import CyberTable from '../components/CyberTable';
import { ShieldAlert, Filter, RefreshCw, Layers } from 'lucide-react';

export default function Alerts() {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');

    const load = async () => {
        setLoading(true);
        try {
            const data = await fetchAlerts();
            setAlerts(data.alerts || []);
        } catch (e) {
            console.error("Alerts sync failed", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        load();
    }, []);

    const filtered = alerts.filter(a => {
        if (filter === 'all') return true;
        if (filter === 'high') return a.risk_score >= 70;
        if (filter === 'block') return a.decision === 'BLOCK';
        if (filter === 'mfa') return a.decision === 'MFA';
        return true;
    });

    const filters = [
        { id: 'all', label: 'Matrix All', icon: <Layers className="w-3 h-3" /> },
        { id: 'high', label: 'High Priority', icon: <ShieldAlert className="w-3 h-3" /> },
        { id: 'block', label: 'Interventions', icon: <ShieldAlert className="w-3 h-3" /> },
        { id: 'mfa', label: 'Challenges', icon: <ShieldAlert className="w-3 h-3" /> }
    ];

    return (
        <div className="space-y-10 animate-fade-in">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    <div className="p-4 bg-cyber-danger/10 rounded-2xl border border-cyber-danger/20">
                        <ShieldAlert className="w-8 h-8 text-cyber-danger" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-black font-display text-white uppercase tracking-tighter">Security Alerts Hub</h2>
                        <div className="flex items-center space-x-3 mt-1">
                           <span className="text-[10px] text-slate-500 font-mono uppercase font-black tracking-widest leading-none">
                               Neural Intelligence Buffering...
                           </span>
                           <div className="h-1 w-24 bg-cyber-border rounded-full overflow-hidden">
                              <motion.div 
                                className="h-full bg-cyber-danger"
                                animate={{ x: [-100, 100] }} transition={{ repeat: Infinity, duration: 2 }}
                              />
                           </div>
                        </div>
                    </div>
                </div>

                <div className="flex items-center space-x-4">
                   <div className="text-right">
                      <div className="text-[10px] font-black text-slate-600 uppercase tracking-widest">Active Alerts</div>
                      <div className="text-xl font-black font-display text-white">{filtered.length}</div>
                   </div>
                   <button 
                     onClick={load}
                     className="p-3 bg-cyber-panel border border-cyber-border rounded-xl text-slate-400 hover:text-white hover:border-cyber-accent transition-all group"
                   >
                      <RefreshCw className={`w-5 h-5 group-active:rotate-180 transition-transform ${loading ? 'animate-spin' : ''}`} />
                   </button>
                </div>
            </div>

            <div className="flex items-center space-x-2 p-1 bg-cyber-bg border border-cyber-border rounded-2xl w-fit">
                {filters.map((f) => (
                    <button
                        key={f.id}
                        onClick={() => setFilter(f.id)}
                        className={`flex items-center space-x-3 px-6 py-2.5 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all
                                   ${filter === f.id ? 'bg-cyber-panel border border-white/10 text-white shadow-xl' : 'text-slate-600 hover:text-slate-400'}`}
                    >
                        {f.icon}
                        <span>{f.label}</span>
                    </button>
                ))}
            </div>

            <div className="glass shadow-2xl rounded-3xl overflow-hidden min-h-[500px]">
                <CyberTable alerts={filtered} />
            </div>

            <div className="grid grid-cols-4 gap-6">
               <MiniStat label="Anomalies" value={alerts.filter(a => a.fraud_type === 'anomaly').length} color="text-cyber-accent" />
               <MiniStat label="Account Takeover" value={alerts.filter(a => a.fraud_type === 'account_takeover').length} color="text-cyber-danger" />
               <MiniStat label="Money Laundering" value={alerts.filter(a => a.fraud_type === 'money_laundering').length} color="text-cyber-purple" />
               <MiniStat label="Synthetic" value={alerts.filter(a => a.fraud_type === 'synthetic_identity').length} color="text-cyber-warning" />
            </div>
        </div>
    );
}

function MiniStat({ label, value, color }) {
  return (
    <div className="glass-card flex flex-col justify-center p-6 border-white/5">
      <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">{label}</div>
      <div className={`text-2xl font-black font-display ${color}`}>{value}</div>
    </div>
  );
}