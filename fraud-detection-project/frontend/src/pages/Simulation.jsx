import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Send, RefreshCw, ShieldAlert, CheckCircle, Info, Zap } from 'lucide-react';
import { processTransaction, runScenario } from '../services/api';
import RiskGauge from '../components/RiskGauge';
import DecisionBadge from '../components/DecisionBadge';

export default function Simulation() {
  const [tx, setTx] = useState({
    sender_id: 'user_123',
    receiver_id: 'merchant_456',
    amount: 100.0,
    device_id: 'DEVICE_X',
    location: 'Mumbai'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [simStatus, setSimStatus] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setShowSuccess(false);
    try {
      const resp = await processTransaction(tx);
      setResult(resp);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (err) {
      console.error("Manual injection failed", err);
    } finally {
      setLoading(false);
    }
  };

  const handleScenario = async (name) => {
    setLoading(true);
    setResult(null); // Clear manual result to show sync progress
    setSimStatus(`UPLINKING VECTOR SCENARIO: ${name.toUpperCase()}...`);
    try {
      const res = await runScenario(name);
      setSimStatus(`MATRIX SYNCHRONIZED: ${res.steps || 0} VECTORS ANALYZED`);
      setTimeout(() => setSimStatus(null), 5000);
    } catch (err) {
      setSimStatus(`UPLINK FAILURE: SCENARIO ${name.toUpperCase()} INTERRUPTED`);
    } finally {
      setLoading(false);
    }
  };

  const scenarios = [
    { name: 'normal', label: 'Baseline Activity', color: 'bg-cyber-success', icon: <CheckCircle className="w-4 h-4" /> },
    { name: 'mule_hub', label: 'Network Smurfing', color: 'bg-cyber-warning', icon: <RefreshCw className="w-4 h-4" /> },
    { name: 'account_takeover', label: 'Identity Hijack', color: 'bg-cyber-danger', icon: <ShieldAlert className="w-4 h-4" /> },
    { name: 'money_laundering', label: 'Circular Ring', color: 'bg-cyber-purple', icon: <Zap className="w-4 h-4" /> }
  ];

  return (
    <div className="grid grid-cols-12 gap-8 h-[calc(100vh-140px)]">
      <div className="col-span-12 lg:col-span-4 flex flex-col space-y-6">
        <div className="glass-card flex-1 flex flex-col">
           <div className="flex items-center space-x-3 mb-8">
              <Zap className="w-5 h-5 text-cyber-accent animate-pulse" />
              <h2 className="text-sm font-black font-display text-white uppercase tracking-[0.2em]">Matrix Injection Console</h2>
           </div>

           <form onSubmit={handleSubmit} className="space-y-6 flex-1">
              <SimInput label="Vector Target (Sender ID)" value={tx.sender_id} onChange={(v) => setTx({...tx, sender_id: v})} />
              <SimInput label="Receiver Node" value={tx.receiver_id} onChange={(v) => setTx({...tx, receiver_id: v})} />
              <SimInput label="Quantum Unit (Amount)" type="number" value={tx.amount} onChange={(v) => setTx({...tx, amount: parseFloat(v)})} />
              <div className="grid grid-cols-2 gap-4">
                 <SimInput label="Device Identity" value={tx.device_id} onChange={(v) => setTx({...tx, device_id: v})} />
                 <SimInput label="Geo Latency" value={tx.location} onChange={(v) => setTx({...tx, location: v})} />
              </div>

              <button 
                type="submit" 
                disabled={loading}
                className="w-full clay-btn py-4 flex items-center justify-center space-x-3 group relative overflow-hidden"
              >
                {showSuccess ? (
                  <motion.div initial={{ y: 20 }} animate={{ y: 0 }} className="flex items-center space-x-2 text-cyber-success">
                    <CheckCircle className="w-4 h-4" />
                    <span className="text-[10px] font-black uppercase tracking-widest">Injection Successful</span>
                  </motion.div>
                ) : (
                  <>
                    <Send className="w-4 h-4 group-hover:-translate-y-1 group-hover:translate-x-1 transition-transform" />
                    <span className="text-[10px] font-black uppercase tracking-widest">Inject Transaction</span>
                  </>
                )}
              </button>
           </form>

           <div className="mt-4 p-4 bg-cyber-bg/50 border border-white/5 rounded-xl">
              <div className="flex items-center space-x-2 mb-2">
                 <Info className="w-3 h-3 text-cyber-accent" />
                 <span className="text-[9px] font-black uppercase text-slate-500 tracking-widest">Simulation Purpose</span>
              </div>
              <p className="text-[9px] text-slate-600 leading-relaxed font-medium">
                 Use the <b>Matrix Simulator</b> to stress-test your AI defense. Manual injections check individual rules, while <b>Scenarios</b> launch coordinated attacks like Mule Hubs to verify graph-level detection and automated blocking.
              </p>
           </div>
           
               <div className="mt-8 pt-8 border-t border-cyber-border space-y-4">
                  <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Demo Orchestration</h3>
                  <button 
                    onClick={() => handleScenario('mule_hub')}
                    className="w-full py-4 bg-cyber-accent/10 border border-cyber-accent text-cyber-accent rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-cyber-accent hover:text-cyber-bg transition-all shadow-[0_0_20px_rgba(0,245,255,0.15)] group"
                  >
                     <RefreshCw className="w-4 h-4 inline-block mr-2 group-hover:rotate-180 transition-transform" />
                     Initialize Fraud Matrix (Demo Hub)
                  </button>
                  <p className="text-[8px] text-slate-600 font-bold uppercase text-center px-4">
                     Warning: This will inject 50+ nodes and edges into the real-time neural buffer for forensic testing.
                  </p>
               </div>
            </div>
         </div>

      <div className="col-span-12 lg:col-span-8 overflow-hidden">
         <AnimatePresence mode="wait">
            {!result ? (
               <motion.div 
                 key="idle"
                 initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                 className="h-full glass-card flex flex-col items-center justify-center text-center space-y-6"
               >
                  <div className="relative">
                     <RefreshCw className="w-20 h-20 text-cyber-border animate-spin-slow opacity-20" />
                     <div className="absolute inset-0 flex items-center justify-center">
                        <Zap className="w-8 h-8 text-cyber-border animate-pulse" />
                     </div>
                  </div>
                  <div>
                     <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.3em]">Awaiting Uplink...</h3>
                     <p className="text-[10px] text-slate-700 font-mono mt-2 uppercase">Neural Matrix Disconnected | Port 8000 Sync Standby</p>
                  </div>
                  {simStatus && (
                     <div className="px-6 py-2 bg-cyber-accent/10 border border-cyber-accent/20 rounded-full">
                        <span className="text-[10px] font-black text-cyber-accent uppercase tracking-widest animate-pulse">{simStatus}</span>
                     </div>
                  )}
               </motion.div>
            ) : (
               <motion.div 
                 key="result"
                 initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
                 className="h-full flex flex-col space-y-6"
               >
                  <div className="grid grid-cols-2 gap-6 h-[400px]">
                     <RiskGauge score={result.risk_score} />
                     <div className="glass-card flex flex-col justify-between">
                        <div className="flex items-center justify-between mb-8">
                           <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Decision Logic Branch</h3>
                           <div className="flex space-x-2">
                              <span className="text-[8px] font-bold text-cyber-accent bg-cyber-accent/10 px-2 py-0.5 rounded uppercase">Pre-Transaction Sync</span>
                           </div>
                        </div>
                        
                        <div className="flex flex-col items-center space-y-6 flex-1 justify-center">
                           <DecisionBadge decision={result.decision} />
                           {result.critical_fraud && (
                              <motion.div 
                                animate={{ scale: [1, 1.1, 1] }} transition={{ repeat: Infinity }}
                                className="px-4 py-1.5 bg-cyber-danger text-white rounded-lg text-[10px] font-black uppercase tracking-widest shadow-[0_0_15px_rgba(255,0,60,0.5)]"
                              >
                                 Critical Threat Detected
                              </motion.div>
                           )}
                           <div className="text-center">
                              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1 font-mono">Trace Vector ID</div>
                              <div className="text-xs font-black text-white font-mono break-all px-12">{result.transaction_id}</div>
                           </div>
                        </div>
                     </div>
                  </div>

                  <div className="flex-1 glass-card overflow-hidden flex flex-col">
                     <div className="flex items-center space-x-3 mb-6">
                        <Info className="w-4 h-4 text-cyber-accent" />
                        <h3 className="text-[10px] font-black text-white uppercase tracking-[0.2em] italic">Neural Reasoning Log</h3>
                     </div>

                     <div className="grid grid-cols-2 gap-12 flex-1 items-start">
                        <div className="space-y-4">
                           {Object.entries(result.reason_categories).map(([cat, list]) => (
                              list.length > 0 && (
                                 <div key={cat} className="space-y-2">
                                    <h4 className="text-[9px] font-black text-slate-600 uppercase tracking-widest border-b border-cyber-border pb-1">{cat}</h4>
                                    <div className="space-y-1.5">
                                       {list.map((r, i) => (
                                          <div key={i} className="flex items-start space-x-2">
                                             <div className="w-1.5 h-1.5 rounded-full bg-cyber-accent mt-1 shrink-0" />
                                             <span className="text-[10px] text-slate-300 font-bold leading-tight">{r.message}</span>
                                          </div>
                                       ))}
                                    </div>
                                 </div>
                              )
                           ))}
                        </div>

                        <div className="space-y-6">
                           <h4 className="text-[9px] font-black text-slate-600 uppercase tracking-widest border-b border-cyber-border pb-1">Weighted Signal Breakdown</h4>
                           <div className="space-y-4">
                              {Object.entries(result.score_breakdown).map(([key, val]) => (
                                 <div key={key} className="space-y-1.5">
                                    <div className="flex justify-between text-[9px] font-black uppercase text-slate-500">
                                       <span>{key} Analysis</span>
                                       <span>{val}%</span>
                                    </div>
                                    <div className="h-1 bg-cyber-bg rounded-full overflow-hidden">
                                       <motion.div 
                                         className={`h-full ${val > 60 ? 'bg-cyber-danger shadow-[0_0_8px_rgba(255,0,60,0.5)]' : val > 30 ? 'bg-cyber-warning' : 'bg-cyber-accent'}`}
                                         initial={{ width: 0 }} animate={{ width: `${val}%` }} transition={{ duration: 1 }}
                                       />
                                    </div>
                                 </div>
                              ))}
                           </div>
                        </div>
                     </div>
                  </div>
               </motion.div>
            )}
         </AnimatePresence>
      </div>
    </div>
  );
}

function SimInput({ label, value, onChange, type = "text" }) {
  return (
    <div className="space-y-2">
      <label className="text-[9px] uppercase font-black text-slate-600 tracking-widest px-1">{label}</label>
      <input 
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-cyber-bg border border-cyber-border rounded-xl px-4 py-3 text-xs focus:outline-none focus:border-cyber-accent transition-all text-white font-mono"
      />
    </div>
  );
}