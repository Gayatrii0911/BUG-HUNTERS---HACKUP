import { useState } from 'react';
import { fetchGraph, fetchAccount } from '../services/api';
import GraphView from '../components/GraphView';
import TracePanel from '../components/TracePanel';
import FraudChainFlow from '../components/FraudChainFlow';
import { motion, AnimatePresence } from 'framer-motion';

const Investigation = () => {
    const [searchId, setSearchId] = useState('');
    const [graphData, setGraphData] = useState(null);
    const [accountData, setAccountData] = useState(null);
    const [loading, setLoading] = useState(false);

    // Mock Fraud Chain (Seed data for visualization)
    const demoChain = [
        { id: 'CHAIN-01', label: 'E_NODE', role: 'ENTRY', isFraud: true },
        { id: 'HUB-99', label: 'T_NODE', role: 'TRANSIT', isFraud: true },
        { id: 'LAYER-X', label: 'L_NODE', role: 'TRANSIT', isFraud: true },
        { id: 'SINK-Z', label: 'S_NODE', role: 'SINK', isFraud: true },
    ];

    const performSearch = async (id) => {
        if (!id) return;
        setLoading(true);
        try {
            const gd = await fetchGraph(id);
            const ad = await fetchAccount(id);
            setGraphData(gd);
            setAccountData(ad);
        } catch (err) {
            console.error("Forensic search failed", err);
        } finally {
            setLoading(false);
        }
    };

    const handleSearchSubmit = (e) => {
        e.preventDefault();
        performSearch(searchId);
    };

    const handleNodeClick = (nodeId) => {
        setSearchId(nodeId);
        performSearch(nodeId);
    };

    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-12 max-w-[1800px] mx-auto px-6 py-6"
        >
            {/* Header / Forensic Area (Orca Style) */}
            <div className="flex items-center justify-between border-b border-white/5 pb-10">
                <div className="space-y-1">
                    <h2 className="text-3xl font-bold font-display text-white tracking-tight">Attack Paths</h2>
                    <p className="text-xs text-slate-500 font-black uppercase tracking-[0.4em] italic opacity-60">Visualizing Structural Network Intelligence Hub [v4.1]</p>
                </div>

                <form onSubmit={handleSearchSubmit} className="flex space-x-6 group relative h-fit items-center">
                    <div className="relative">
                        <input 
                            type="text" 
                            required
                            value={searchId}
                            onChange={(e) => setSearchId(e.target.value)}
                            placeholder="Identify Node Signature..."
                            className="bg-white/[0.03] border border-white/10 rounded-xl px-6 py-3 text-xs font-mono text-white focus:outline-none focus:border-indigo-500/50 w-[300px] shadow-2xl backdrop-blur-2xl group-hover:border-indigo-500/30 transition-all placeholder:italic placeholder:opacity-30"
                        />
                        <div className="absolute top-1/2 -translate-y-1/2 right-4 w-2 h-2 rounded-full bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.5)] animate-pulse" />
                    </div>
                    <button type="submit" className="bg-indigo-600 text-white rounded-xl px-10 py-3 font-black text-[10px] uppercase tracking-[0.3em] hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-500/20">
                        Trace Node
                    </button>
                    <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                </form>
            </div>

            {/* Central Investigation Matrix */}
            <div className="grid grid-cols-1 xl:grid-cols-12 gap-10 items-stretch h-[800px]">
                {/* Graph Viewport */}
                <div className="xl:col-span-8 orca-card p-0 relative overflow-hidden group border-white/10 shadow-[0_0_100px_rgba(0,0,0,0.6)]">
                    <GraphView graphData={graphData} loading={loading} onNodeClick={handleNodeClick} />
                    
                    <div className="absolute top-8 left-8 p-5 bg-black/40 border border-white/5 backdrop-blur-2xl text-[9px] font-black text-indigo-400 uppercase tracking-[0.5em] z-10 italic rounded-xl">
                       <div className="flex items-center space-x-3">
                           <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 shadow-[0_0_8px_#6366f1] animate-pulse" />
                           <span>Structural Network Fabric</span>
                       </div>
                    </div>
                    <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                </div>

                {/* Side Intelligence Panels */}
                <div className="xl:col-span-4 flex flex-col space-y-10 h-full">
                    <div className="flex-1 overflow-auto orca-card p-10 bg-gradient-to-b from-white/[0.02] to-transparent scrollbar-hide border-white/5 relative">
                        <TracePanel profile={accountData} loading={loading} />
                        <div className="hologram-overlay opacity-5 pointer-events-none" />
                    </div>
                    
                    <div className="orca-card p-10 bg-indigo-500/[0.03] border-indigo-500/10 group flex flex-col justify-between relative">
                         <div className="space-y-6">
                            <div className="flex items-center space-x-4 text-white">
                                <span className="text-2xl grayscale group-hover:grayscale-0 transition-grayscale">☣️</span>
                                <h3 className="text-xs font-black uppercase tracking-[0.4em] italic opacity-80 group-hover:opacity-100 transition-opacity">Forensic Audit</h3>
                            </div>
                            <p className="text-[11px] text-slate-500 font-bold italic leading-[2.2] tracking-wide opacity-60 group-hover:opacity-100 transition-opacity">
                                Active node tracing logged to the <span className="text-indigo-400">Secure Audit Vault</span>. 
                                Click any node in the fabric to perform a <span className="text-white italic">Neural Dril-down Audit</span> for real-time risk re-scoring.
                            </p>
                         </div>
                         <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                    </div>
                </div>
            </div>

            {/* Insights Dashboard Layer (Bottom) */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-10 pt-10">
                <FraudChainFlow chain={demoChain} />
                
                <div className="orca-card p-12 overflow-hidden group/pattern relative bg-gradient-to-r from-indigo-500/[0.03] to-transparent border-white/10">
                    <div className="flex justify-between items-start mb-12">
                        <div className="space-y-4">
                            <h3 className="text-xs font-black uppercase text-indigo-400 tracking-[0.6em] italic mb-1">Exposure Affinity</h3>
                            <div className="text-[10px] font-black text-slate-600 uppercase tracking-widest italic opacity-60">Verified Neural Cluster Probability</div>
                        </div>
                        <div className="px-6 py-2 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-[9px] font-black text-indigo-400 italic tracking-widest uppercase shadow-lg">Pattern Verified</div>
                    </div>
                    <div className="space-y-12">
                        {[
                            { label: 'Synthetic Node Similarity', prob: 92 },
                            { label: 'Network Fragmentation Risk', prob: 74 },
                            { label: 'High-Velocity Dispersal', prob: 31 }
                        ].map((m, i) => (
                            <div key={i} className="space-y-5">
                                <div className="flex justify-between items-end text-[10px] font-black uppercase text-slate-500 tracking-[0.3em] italic group-hover/pattern:text-white transition-colors">
                                    <span>{m.label}</span>
                                    <span className="text-white tabular-nums drop-shadow-[0_0_10px_rgba(255,255,255,0.3)] pr-2">{m.prob}_INDEX</span>
                                </div>
                                <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden border border-white/5 shadow-inner">
                                    <motion.div 
                                        initial={{ width: 0 }}
                                        animate={{ width: `${m.prob}%` }}
                                        transition={{ duration: 2, delay: i * 0.2 }}
                                        className={`h-full bg-indigo-600 shadow-[0_0_25px_rgba(99,102,241,0.4)]`}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="hologram-overlay opacity-5 group-hover/pattern:opacity-10 transition-opacity" />
                </div>
            </div>
        </motion.div>
    );
};

export default Investigation;
