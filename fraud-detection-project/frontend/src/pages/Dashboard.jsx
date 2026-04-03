import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchAlerts, fetchHealth } from '../services/api';
import MetricCard from '../components/MetricCard';
import NeuralRiskMeter from '../components/NeuralRiskMeter';
import RiskBreakdown from '../components/RiskBreakdown';
import ThreatMap from '../components/ThreatMap';

const Dashboard = () => {
    const [alerts, setAlerts] = useState([]);
    const [health, setHealth] = useState(null);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({ total: 0, suspicious: 0, blocked: 0, mfa: 0, avg_risk: 0 });

    useEffect(() => {
        const load = async () => {
            try {
                const data = await fetchAlerts();
                const h = await fetchHealth();
                setAlerts(data);
                setHealth(h);

                const count = data.length || 0;
                const suspicious = data.filter(a => a.risk_score >= 40).length;
                const blocked = data.filter(a => a.action === 'BLOCK').length;
                const mfa = data.filter(a => a.action === 'MFA').length;
                const avg = count > 0 ? (data.reduce((sum, a) => sum + (a.risk_score || 0), 0) / count) : 0;
                
                setStats({ 
                    total: count, 
                    suspicious, 
                    blocked, 
                    mfa, 
                    avg_risk: parseFloat(avg.toFixed(1)) 
                });
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };

        load();
        const interval = setInterval(load, 5000);
        return () => clearInterval(interval);
    }, []);

    const latestAlert = alerts[0] || { risk_score: 0, risk_level: 'STABLE' };

    return (
        <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-12 max-w-[1800px] mx-auto px-6 py-6"
        >
            {/* Header / Engine Monitor Strip */}
            <div className="flex flex-col xl:flex-row xl:items-center justify-between gap-8 border-b border-white/5 pb-10">
                <div className="space-y-1">
                    <h1 className="text-3xl font-display font-bold text-white tracking-tight">Forensic Cyber Command</h1>
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-widest italic tracking-tighter shadow-sm opacity-60">Unified Neural Ingress & Real-Time Intelligence Orchestration</p>
                </div>
                
                {/* Neural Progress Module (Demonstrates AI Lifecycle) */}
                <div className="flex items-center space-x-10 px-10 py-5 bg-white/[0.02] border border-white/10 rounded-2xl shadow-[0_0_40px_rgba(0,0,0,0.4)] backdrop-blur-3xl group">
                   <div className="flex flex-col">
                      <span className="text-[10px] text-slate-600 font-black uppercase tracking-[0.4em] mb-2 italic">Neural Training Fabric</span>
                      <div className="flex items-center space-x-4">
                         <div className="w-40 h-1.5 bg-white/5 rounded-full overflow-hidden border border-white/5">
                            <motion.div 
                               initial={{ width: 0 }}
                               animate={{ width: `${health?.adaptive_learning?.progress_percent || 0}%` }}
                               transition={{ duration: 1.5 }}
                               className="h-full bg-indigo-500 shadow-[0_0_20px_#6366f1]" 
                            />
                         </div>
                         <span className="text-[11px] text-indigo-400 font-mono font-black italic tabular-nums">{health?.adaptive_learning?.progress_percent || 0}%</span>
                      </div>
                   </div>
                   <div className="w-[1px] h-10 bg-white/10 mx-2" />
                   <div className="flex flex-col text-right">
                      <span className="text-[10px] text-slate-600 font-black uppercase tracking-[0.4em] mb-2 italic">Fabric Precision</span>
                      <span className="text-md font-black text-white italic tracking-tighter shadow-sm group-hover:text-indigo-400 transition-colors">99.82% CONFIDENCE</span>
                   </div>
                </div>
            </div>

            {/* Neural Metric Strip (Top Stats) */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <MetricCard label="Suspicious Count" value={stats.suspicious} variant="red" icon="☣️" />
                <MetricCard label="Neural Ingress" value={stats.total} variant="blue" icon="🪐" />
                <MetricCard label="Blocked Assets" value={stats.blocked} variant="amber" icon="🔐" />
                <MetricCard label="Average Risk" value={`${stats.avg_risk}%`} variant="blue" icon="⚡" />
            </div>

            {/* Central Tactical Matrix (Centerpiece) */}
            <div className="grid grid-cols-1 xl:grid-cols-12 gap-10 items-stretch">
                {/* Neural Risk Hub (Gauge + Breakdown) */}
                <div className="xl:col-span-4 h-[750px] flex flex-col space-y-10 group">
                    <div className="flex-1 orca-card p-12 bg-gradient-to-b from-white/[0.03] to-transparent relative group overflow-hidden border-white/10">
                        <NeuralRiskMeter score={latestAlert.risk_score} status={latestAlert.risk_level} />
                        <div className="hologram-overlay opacity-5 pointer-events-none" />
                    </div>
                    <div className="flex-1 orca-card p-12 bg-gradient-to-t from-white/[0.02] to-transparent border-white/5 group">
                        <RiskBreakdown components={latestAlert.score_breakdown} />
                        <div className="hologram-overlay opacity-5 pointer-events-none" />
                    </div>
                </div>

                {/* Tactical Visuals (Heatmap + Map) */}
                <div className="xl:col-span-8 flex flex-col space-y-10">
                    <div className="flex-[4] orca-card p-12 relative overflow-hidden group border-white/10">
                        <h3 className="text-xs font-black uppercase text-indigo-500 tracking-[0.6em] italic mb-10 flex items-center space-x-4 leading-none">
                           <span className="w-2 h-2 rounded-full bg-indigo-500 shadow-[0_0_10px_#6366f1] animate-pulse" />
                           <span>Target Ingress Affinity Matrix</span>
                        </h3>
                        <div className="space-y-6 pt-4">
                            {[...Array(8)].map((_, r) => (
                                <div key={r} className="flex items-center space-x-8 group/row">
                                    <span className="text-[9px] text-slate-700 font-black font-mono w-28 truncate italic uppercase tracking-[0.4em] group-hover/row:text-slate-400 transition-colors">{['ALPHA-7', 'BETA-X', 'DELTA-S', 'GAMMA-O', 'IOTA-N', 'ZETA-9', 'SIGMA-2', 'OMEGA-F'][r]}.node</span>
                                    <div className="flex-1 flex space-x-3">
                                        {[...Array(14)].map((_, c) => {
                                            const intensity = Math.random();
                                            return (
                                                <div 
                                                    key={c} 
                                                    className={`flex-1 h-10 rounded-lg border border-white/5 shadow-inner transition-all duration-1000 group-hover:scale-110 cursor-pointer
                                                        ${intensity > 0.8 ? 'bg-indigo-500/80 shadow-[0_0_20px_rgba(99,102,241,0.5)] border-indigo-400/30' : 
                                                        intensity > 0.5 ? 'bg-indigo-500/30' : 
                                                        intensity > 0.3 ? 'bg-indigo-500/10' : 'bg-transparent'}`}
                                                />
                                            )
                                        })}
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                    </div>

                    <div className="flex-[3] orca-card p-0 relative group overflow-hidden bg-gradient-to-r from-indigo-500/[0.03] to-transparent border-white/10 group">
                        <div className="p-10 absolute top-0 left-0 z-10 w-full flex justify-between items-start">
                            <h3 className="text-xs font-black uppercase text-slate-500 tracking-[0.4em] italic mb-10 leading-none group-hover:text-indigo-400 transition-colors">Global Geo-Ingress Vector</h3>
                            <div className="flex items-center space-x-4">
                                <div className="text-[10px] font-black text-white italic tracking-tighter opacity-40 group-hover:opacity-100 transition-opacity">V_TRACE_MAP [v4.1]</div>
                            </div>
                        </div>
                        <div className="scale-[1.8] translate-y-32 translate-x-12 opacity-60 group-hover:opacity-100 transition-all duration-1000 grayscale group-hover:grayscale-0 contrast-125">
                            <ThreatMap />
                        </div>
                        <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                    </div>
                </div>
            </div>

            {/* Intelligence Stream Layer (Bottom) */}
            <div className="orca-card p-0 overflow-hidden group border-white/5 shadow-[0_0_100px_rgba(0,0,0,0.6)] backdrop-blur-md pb-16">
                <div className="p-12 flex justify-between items-end border-b border-white/10 bg-white/[0.01]">
                    <div className="space-y-2">
                        <h3 className="text-[10px] font-black uppercase text-indigo-500 tracking-[1em] italic mb-4">Neural Intelligence Feed</h3>
                        <div className="text-3xl font-black text-white italic tracking-tighter shadow-sm">Real-Time Threat Fabric Replay</div>
                    </div>
                    <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest italic animate-pulse shadow-sm">Syncing Neural Signatures...</div>
                </div>
                
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="text-[10px] text-slate-600 uppercase tracking-[0.4em] font-black italic border-b border-white/5">
                                <th className="px-12 py-8">Identity_Signature</th>
                                <th className="px-12 py-8">Nodal_Context</th>
                                <th className="px-12 py-8">Neural_Integrity</th>
                                <th className="px-12 py-8 text-right">Audit_Trace</th>
                            </tr>
                        </thead>
                        <tbody className="text-[11px] font-bold text-slate-400 font-mono">
                            {alerts.slice(0, 5).map((a, i) => (
                                <tr key={i} className="orca-table-row group/row">
                                    <td className="px-12 py-9 flex items-center space-x-6">
                                        <div className={`w-12 h-12 rounded-2xl bg-black/50 border flex items-center justify-center shadow-2xl transition-all duration-700
                                            ${a.risk_score >= 70 ? 'border-red-500/40 text-red-500 shadow-[0_0_20px_rgba(239,68,68,0.2)]' : 'border-indigo-500/20 text-indigo-500 shadow-[0_0_20px_rgba(99,102,241,0.1)]'}`}>
                                            ⚛️
                                        </div>
                                        <div className="flex flex-col">
                                            <span className="text-white mb-2 uppercase italic font-black text-sm tracking-tighter drop-shadow-sm">{a.transaction_id.slice(0, 14)}</span>
                                            <span className="text-[9px] text-slate-600 font-black uppercase tracking-[0.2em] italic leading-none group-hover/row:text-slate-400">{a.pattern}</span>
                                        </div>
                                    </td>
                                    <td className="px-12 py-9">
                                       <div className="flex items-center space-x-4 text-slate-500 italic group-hover/row:text-slate-300 transition-colors">
                                          <span className="w-4 h-4 rounded-full bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-[8px] text-indigo-400 shadow-[0_0_8px_rgba(99,102,241,0.2)]">◎</span>
                                          <span className="tracking-tighter uppercase">{a.sender_id.slice(0, 16)}</span>
                                       </div>
                                    </td>
                                    <td className="px-12 py-9">
                                        <div className="flex flex-col space-y-4 max-w-[200px]">
                                            <div className="flex justify-between items-end pr-2">
                                               <span className={`text-[12px] font-black tabular-nums italic ${a.risk_score >= 70 ? 'text-red-500' : 'text-indigo-400'} drop-shadow-md`}>
                                                  {(a.risk_score / 100).toFixed(2)}_NR
                                               </span>
                                            </div>
                                            <div className="w-full h-[4px] bg-black/40 rounded-full overflow-hidden border border-white/5 relative shadow-inner">
                                               <motion.div 
                                                  initial={{ x: '-100%' }}
                                                  animate={{ x: '100%' }}
                                                  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                                                  className="absolute inset-y-0 w-1/3 bg-white/20 blur-[1px]" 
                                               />
                                               <div 
                                                  className={`h-full ${a.risk_score >= 70 ? 'bg-red-500 shadow-[0_0_10px_#ef4444]' : 'bg-indigo-500 shadow-[0_0_10px_#6366f1]'} transition-all duration-1000`} 
                                                  style={{ width: `${a.risk_score}%` }} 
                                               />
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-12 py-9 text-right">
                                       <motion.div 
                                          whileHover={{ scale: 1.1, rotate: 90 }}
                                          className="w-10 h-10 rounded-xl bg-white/[0.03] border border-white/10 flex items-center justify-center text-indigo-500 hover:text-white hover:bg-indigo-600 transition-all cursor-pointer shadow-2xl mx-auto italic font-black text-lg"
                                       >
                                          ⋮
                                       </motion.div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div className="hologram-overlay opacity-5 pointer-events-none" />
            </div>
        </motion.div>
    );
};

export default Dashboard;