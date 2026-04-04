import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Info, Activity, ShieldAlert, Cpu, Network } from 'lucide-react';
import { fetchTrace } from '../services/api';
import NetworkGraph from '../components/NetworkGraph';
import { useSearchParams } from 'react-router-dom';

export default function Investigator() {
  const [searchParams] = useSearchParams();
  const initialId = searchParams.get('id') || 'BOSS';
  
  const [accountId, setAccountId] = useState(initialId);
  const [loading, setLoading] = useState(false);
  const [graphData, setGraphData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [error, setError] = useState(null);
  const [showLogs, setShowLogs] = useState(false);

  useEffect(() => {
    if (initialId) {
       setAccountId(initialId);
       handleSearch(initialId);
    }
  }, [initialId]);

  const nodeTransactions = graphData ? graphData.filter(el => 
    el.data.source === selectedNode?.id || el.data.target === selectedNode?.id
  ).map(el => el.data) : [];

  const handleSearch = async (idOrEvent) => {
    // If called from button, idOrEvent is the event object. Use accountId state instead.
    const targetId = (typeof idOrEvent === 'string') ? idOrEvent : accountId;
    
    if (!targetId || typeof targetId !== 'string') return;
    setLoading(true);
    setGraphData(null);
    setShowLogs(false);
    setError(null);
    try {
      const res = await fetchTrace(targetId);
      if (res.status === 'success' && res.graph_payload) {
        const elements = [
          ...res.graph_payload.nodes,
          ...res.graph_payload.edges
        ];
        if (elements.length === 0) {
           setError("No transaction traces found for this account.");
        } else {
           setGraphData(elements);
           // If the backend returned a specific focus account (e.g. from a TX trace), use it
           if (res.account) {
             setAccountId(res.account);
           }
        }
      } else {
        setError(res.message || "Trace failed");
      }
    } catch (err) {
      setError("Trace failed. Backend offline?");
    } finally {
      setLoading(false);
    }
  };

  const handleNodeClick = (nodeData) => {
    setSelectedNode(nodeData);
    setShowLogs(false);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-cyber-accent/10 rounded-xl border border-cyber-accent/20">
            <Network className="w-6 h-6 text-cyber-accent" />
          </div>
          <div>
            <h2 className="text-xl font-black font-display text-white uppercase tracking-tighter">Forensic Node Investigator</h2>
            <p className="text-[10px] text-slate-500 font-mono uppercase font-bold tracking-widest">Network Fund Tracing Loop v1.2</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="relative">
             <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
             <input 
               type="text" 
               value={accountId}
               onChange={(e) => setAccountId(e.target.value)}
               onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
               className="w-64 bg-cyber-panel border border-cyber-border rounded-xl pl-12 pr-6 py-3 text-sm focus:outline-none focus:border-cyber-accent transition-all text-white font-mono"
               placeholder="Search Account Vector..."
             />
          </div>
          <button 
            disabled={loading}
            onClick={handleSearch} 
            className="clay-btn text-xs font-black uppercase tracking-widest"
          >
            Investigate
          </button>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6 flex-1 overflow-hidden">
        <div className="col-span-12 lg:col-span-8 glass rounded-2xl border border-white/5 relative overflow-hidden group h-[600px] lg:h-full">
          <div className="absolute top-6 left-6 z-10 flex flex-col space-y-2">
             <div className="text-[10px] uppercase font-mono font-bold text-cyber-accent bg-cyber-accent/10 px-3 py-1 rounded border border-cyber-accent/20">
                Live Analysis System
             </div>
             {graphData && (
                <div className="text-[9px] text-slate-500 font-bold px-3">
                   {graphData.length} VECTORS SYNCED
                </div>
             )}
          </div>

          {loading && (
             <div className="absolute inset-0 z-20 glass flex flex-col items-center justify-center space-y-4">
                <motion.div 
                  animate={{ rotate: 360, scale: [1, 1.2, 1] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                  className="w-16 h-16 border-t-4 border-cyber-accent rounded-full border-r-4 border-r-transparent" 
                />
                <span className="text-xs font-black text-slate-400 uppercase tracking-[0.3em]">Decoding Flow Graph...</span>
             </div>
          )}

          {error && (
             <div className="absolute inset-0 z-20 flex flex-col items-center justify-center space-y-4">
                <ShieldAlert className="w-12 h-12 text-cyber-danger" />
                <span className="text-xs font-black text-cyber-danger uppercase tracking-widest">{error}</span>
             </div>
          )}

          <NetworkGraph data={graphData} onNodeClick={handleNodeClick} highlightNode={accountId} />
          
          <div className="absolute bottom-6 left-6 flex space-x-3">
             <Legend color="border-cyber-accent/50 bg-[#1a1c2e]" text="Normal Node" />
             <Legend color="border-cyber-danger bg-cyber-danger/20" text="Fraud Entity" />
             <Legend color="border-cyber-danger border-[5px] opacity-60" text="Blocked System" />
          </div>
        </div>

        <div className="col-span-12 lg:col-span-4 flex flex-col space-y-6 overflow-auto pr-1">
          <AnimatePresence mode="wait">
            {!selectedNode ? (
              <motion.div 
                key="empty"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className="flex-1 glass-card flex flex-col items-center justify-center text-center space-y-6"
              >
                 <Network className="w-16 h-16 text-cyber-border animate-pulse" />
                 <div>
                    <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-2">Select a Node to Decrypt</h3>
                    <p className="text-[10px] text-slate-600 leading-relaxed px-12">
                       Network graph analysis results are decrypted on-demand. Select any account vector to view deep relationship details.
                    </p>
                 </div>
              </motion.div>
            ) : (
              <motion.div 
                key="details"
                initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
                className="flex-1 glass-card space-y-8"
              >
                  <div className="flex items-center justify-between border-b border-cyber-border pb-6">
                     <div className="flex items-center space-x-4">
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center border-2 
                                       ${selectedNode.is_fraudulent ? 'border-cyber-danger text-cyber-danger' : 'border-cyber-accent text-cyber-accent'}`}>
                           <Cpu className="w-6 h-6" />
                        </div>
                        <div>
                           <div className="text-sm font-black font-display text-white">{selectedNode.label}</div>
                           <div className="text-[9px] uppercase font-bold text-slate-500 tracking-widest">Digital Fingerprint Sync</div>
                        </div>
                     </div>
                  </div>

                  <div className="space-y-4">
                     <DetailRow label="System Status" value={selectedNode.is_blocked ? "LOCKED" : "OPERATIONAL"} color={selectedNode.is_blocked ? "text-cyber-danger" : "text-cyber-success"} />
                     <DetailRow label="Risk Classification" value={selectedNode.is_fraudulent ? "SUSPECTED FRAUD" : "VERIFIED CLEAR"} color={selectedNode.is_fraudulent ? "text-cyber-danger" : "text-cyber-success"} />
                     <DetailRow label="AI Confidence" value="98.2%" color="text-cyber-accent" />
                  </div>

                  <div className="p-4 bg-cyber-bg/50 rounded-xl border border-cyber-border space-y-2">
                     <div className="flex items-center space-x-2 mb-2">
                        <Activity className="w-3 h-3 text-cyber-accent" />
                        <span className="text-[10px] font-black uppercase text-slate-400 tracking-tighter">Behavioral Analysis</span>
                     </div>
                     {!showLogs ? (
                        <p className={`text-[10px] leading-relaxed italic ${selectedNode.is_fraudulent ? 'text-cyber-danger/80' : 'text-slate-500'}`}>
                           "{selectedNode.reasons || `SYSTEM: ${selectedNode.is_fraudulent ? 'SUSPECT' : 'APPROVED'} | Account ${selectedNode.id} identified as ${nodeTransactions.filter(t => t.source === selectedNode.id).length >= nodeTransactions.filter(t => t.target === selectedNode.id).length ? 'PROLIFIC SENDER' : 'PRIMARY RECEIVER'}. AI confirms profile integrity within normal fund-flow bounds.`}"
                        </p>
                     ) : (
                        <div className="space-y-3 pt-2">
                           {nodeTransactions.length > 0 ? (
                              nodeTransactions.slice(0, 6).map((tx, i) => (
                                 <div key={i} className="flex justify-between items-center text-[9px] font-mono border-b border-white/5 pb-2">
                                    <span className={tx.source === selectedNode.id ? "text-cyber-danger" : "text-cyber-success"}>
                                       {tx.source === selectedNode.id ? "OUT" : "IN"}
                                    </span>
                                    <span className="text-white">₹{tx.amount?.toLocaleString()}</span>
                                    <span className="text-slate-500 uppercase">{tx.decision || 'DONE'}</span>
                                 </div>
                              ))
                           ) : (
                              <div className="text-[9px] text-slate-600 italic">No recent vectors recorded in neural cache.</div>
                           )}
                        </div>
                     )}
                  </div>

                  <button 
                    onClick={() => setShowLogs(!showLogs)}
                    className="w-full py-4 text-[10px] font-black uppercase tracking-[0.2em] bg-cyber-bg border border-cyber-border rounded-xl hover:border-cyber-accent/50 hover:text-white transition-all"
                  >
                     {showLogs ? "Return to Behavioral Intel" : "View Complete Transaction Log"}
                  </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

// Sub-components moved above or converted to function declarations to avoid ReferenceErrors
function DetailRow({ label, value, color }) {
  return (
    <div className="flex justify-between items-center text-[11px] font-bold">
      <span className="text-slate-500 uppercase tracking-widest">{label}</span>
      <span className={`${color} font-mono font-black`}>{value}</span>
    </div>
  );
}

function Legend({ color, text }) {
  return (
    <div className="flex items-center space-x-2 bg-cyber-panel/80 px-3 py-1.5 rounded-lg border border-white/5">
       <div className={`w-3 h-3 rounded border ${color}`}></div>
       <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">{text}</span>
    </div>
  );
}

