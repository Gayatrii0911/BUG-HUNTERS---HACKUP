import { useState } from 'react';
import { runScenario, resetSystem } from '../services/api';
import SimulationCard from '../components/SimulationCard';
import { motion } from 'framer-motion';

const SCENARIOS = [
  { id: 'normal_user', name: 'Verified Baseline', desc: 'Legitimate behavioral footprint. Zero neural drift.' },
  { id: 'new_device_anomaly', name: 'Identity Drift', desc: 'Hardware mismatch + volume spike. High anomaly score.' },
  { id: 'cycle_fraud', name: 'Node Laundering', desc: 'Circular nodal flow detected. Neural graph loop.' },
  { id: 'mule_hub', name: 'Mule Aggregator', desc: 'Centralized fan-out distribution. Hub detection.' },
  { id: 'layering_chain', name: 'Path Dispersal', desc: 'Deep multi-hop fund lineage tracking. Forensic chain.' },
  { id: 'account_takeover', name: 'Rapid Takeover', desc: 'Abnormal velocity + credential abuse. Fraud chain.' },
  { id: 'coordinated_synergy', name: 'Elite Cluster', desc: 'Hybrid Graph + ML fusion. Critical risk trigger.' },
  { id: 'repeated_suspicious', name: 'Adaptive Spike', desc: 'Escalation based on nodal history matching.' }
];

const Simulation = () => {
    const [running, setRunning] = useState(null);
    const [msg, setMsg] = useState('');

    const handleRun = async (id) => {
        setRunning(id);
        setMsg(`TRANSMITTING INSTRUCTION: ${id.toUpperCase()}...`);
        try {
            const res = await runScenario(id);
            const lastTxResult = res.results[res.results.length - 1];
            setMsg(`EXECUTION_COMPLETE: ${res.results.length} NODES PROCESSED. DECISION: ${lastTxResult.decision} | SCORE: ${lastTxResult.risk_score.toFixed(1)}`);
        } catch (err) {
            setMsg('ERROR_FAULT: NEURAL LINK INTERRUPTED. CHECK CONSOLE.');
        } finally {
            setRunning(null);
        }
    };

    const handleReset = async () => {
        if (!window.confirm("Perform System-Wide Wipe?")) return;
        try {
            await resetSystem();
            setMsg('CORE_RESET: ALL FORENSIC PROFILES AND GRAPH STATES PURGED.');
        } catch (err) {
            setMsg('ERROR_FAULT: RESET SEQUENCE FAILED.');
        }
    };

    return (
        <motion.div 
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="space-y-20 max-w-[1700px] mx-auto px-6 pb-20"
        >
            {/* Header / Global Controller */}
            <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-12 border-b border-white/5 pb-16">
                <div className="space-y-4">
                    <div className="text-[10px] uppercase font-black tracking-[0.6em] text-blue-500 mb-2 italic">Neural Environment Controller</div>
                    <h2 className="text-[5rem] font-display font-black text-white italic tracking-tighter leading-none drop-shadow-[0_20px_50px_rgba(0,0,0,0.5)] pr-8">
                       Simulation <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-400">Lab</span>
                    </h2>
                    <p className="text-[10px] text-slate-500 uppercase font-black mt-3 tracking-[0.4em] italic opacity-60">Injecting Synthetic Risk Patterns into Adaptive Engine Runtime</p>
                </div>

                <button 
                  onClick={handleReset} 
                  className="px-12 py-5 border border-red-500/20 text-red-500 rounded-[2rem] font-black text-[10px] uppercase tracking-[0.4em] hover:bg-red-500/10 transition-all hover:shadow-[0_0_40px_rgba(239,68,68,0.2)] is-3d italic"
                >
                    System Wide Wipe
                </button>
            </div>

            {/* Tactical Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
                {SCENARIOS.map((s, i) => (
                    <motion.div
                        key={s.id}
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: i * 0.05 }}
                    >
                        <SimulationCard 
                          scenario={s} 
                          onRun={handleRun} 
                          running={running} 
                        />
                    </motion.div>
                ))}
            </div>

            {/* Neural Replay Interface */}
            <div className="space-y-8">
                 <div className="flex items-center space-x-3 text-[10px] uppercase font-black text-slate-500 tracking-[0.4em] italic">
                    <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse shadow-[0_0_10px_#3b82f6]" />
                    <span>Real-Time Replay Analytics Stream</span>
                 </div>
                 
                 <div className="cyber-card p-12 bg-gradient-to-tr from-[hsl(var(--bg-card))] to-blue-500/[0.05] overflow-hidden group">
                   <div className="relative z-10 space-y-12">
                      <div className="w-full text-center py-8 border-b border-white/5 relative">
                          <div className={`font-mono text-xs tracking-widest ${msg.includes('COMPLETE') ? 'text-green-500' : msg.includes('TRANSMITTING') ? 'text-blue-400' : 'text-slate-500'} italic`}>
                             {msg || 'AWAITING COMMAND INGRESS FROM CONTROLLER...'}
                          </div>
                          {msg && <div className="absolute inset-x-0 h-[1px] bg-blue-500/20 bottom-0 scanline" />}
                      </div>
                      
                      <div className="grid grid-cols-3 gap-16 px-20">
                         <div className="text-center group-hover:scale-110 transition-transform">
                            <div className="text-4xl font-black text-white italic tracking-tighter shadow-sm">42ms</div>
                            <div className="text-[9px] text-slate-600 font-black uppercase tracking-widest mt-2">Neural Latency</div>
                         </div>
                         <div className="text-center group-hover:scale-110 transition-transform">
                            <div className="text-4xl font-black text-white italic tracking-tighter">Full-Sync</div>
                            <div className="text-[9px] text-slate-600 font-black uppercase tracking-widest mt-2">Fabric Mode</div>
                         </div>
                         <div className="text-center group-hover:scale-110 transition-transform">
                            <div className="text-4xl font-black text-white italic tracking-tighter">99.2%</div>
                            <div className="text-[9px] text-slate-600 font-black uppercase tracking-widest mt-2">Inference Hub</div>
                         </div>
                      </div>
                   </div>
                   <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                 </div>
            </div>

            <div className="p-12 glass-panel border-white/5 flex items-center justify-center text-center opacity-40 hover:opacity-100 transition-opacity">
               <div className="max-w-2xl space-y-4">
                  <h3 className="text-xs font-black text-white uppercase tracking-[0.4em] italic mb-4 leading-none">Simulation Environment Notice</h3>
                  <p className="text-[11px] text-slate-500 font-bold italic leading-loose lowercase tracking-widest">
                     "the simulation executes against the actual production-ready endpoints. any decisions made here update the internal neural fabric and graph relationship indices in real-time. forensic snapshots are permanent."
                  </p>
               </div>
            </div>
        </motion.div>
    );
};

export default Simulation;