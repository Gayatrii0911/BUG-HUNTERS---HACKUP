import { useState, useEffect } from 'react';
import { fetchAccountSummary } from '../services/api';
import BehaviorCard from '../components/BehaviorCard';
import DeviceIntelligenceCard from '../components/DeviceIntelligenceCard';
import MetricCard from '../components/MetricCard';
import { motion } from 'framer-motion';

const Behavior = () => {
    const [accountId, setAccountId] = useState('User_01');
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState(null);

    useEffect(() => {
        handleSearch();
    }, []);

    const handleSearch = async () => {
        if (!accountId) return;
        setLoading(true);
        try {
            const res = await fetchAccountSummary(accountId);
            setData(res);
        } catch (err) {
            console.error("Behavioral audit failed", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-12 max-w-[1800px] mx-auto px-6 py-6"
        >
            {/* Header / Search Area (Orca Style) */}
            <div className="flex items-center justify-between border-b border-white/5 pb-10">
                <div className="space-y-1">
                    <h2 className="text-3xl font-bold font-display text-white tracking-tight">Inventory Context</h2>
                    <p className="text-xs text-slate-500 font-bold uppercase tracking-widest italic">Auditing Real-Time Usage Signatures and Location Drift</p>
                </div>
                <div className="flex space-x-4">
                    <input
                        type="text"
                        value={accountId}
                        onChange={(e) => setAccountId(e.target.value)}
                        className="bg-white/[0.03] border border-white/10 rounded-xl px-6 py-3 text-xs focus:outline-none focus:border-indigo-500/50 transition-all text-white placeholder:italic placeholder:opacity-30 w-64"
                        placeholder="Search Account ID..."
                    />
                    <button
                        onClick={handleSearch}
                        className="px-8 py-3 bg-indigo-600 text-white rounded-xl font-black text-[10px] uppercase tracking-[0.2em] hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-500/20"
                    >
                        Audit Profile
                    </button>
                </div>
            </div>

            {loading && (
                <div className="p-40 flex flex-col items-center justify-center space-y-6">
                    <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin shadow-[0_0_20px_rgba(99,102,241,0.2)]" />
                    <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest italic animate-pulse">Scanning behavioral baseline...</span>
                </div>
            )}

            {!loading && data && (
                <div className="space-y-12">
                     {/* Key Metrics Strip */}
                     <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <MetricCard 
                            label="Total Ingress" 
                            value={data.transaction_count} 
                            icon="📂" 
                            variant="blue"
                        />
                        <MetricCard 
                            label="Volume Value" 
                            value={`Rs. ${data.total_volume.toLocaleString()}`} 
                            icon="💰" 
                            variant="blue"
                        />
                        <MetricCard 
                            label="Nodal Reach" 
                            value={data.graph_connections} 
                            icon="🌐" 
                            variant="blue"
                        />
                        <MetricCard 
                            label="Risk Momentum" 
                            value={(data.risk_history?.slice(-1)[0] || 0).toFixed(1)} 
                            icon="⚡" 
                            variant={data.is_fraudulent ? "red" : "blue"}
                        />
                     </div>

                     <div className="grid grid-cols-12 gap-10 items-start">
                         {/* Behavioral Snapshot */}
                         <div className="col-span-12 lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-8">
                             <BehaviorCard label="Geographical Points" data={data.behavior_snapshot?.top_locations} />
                             <BehaviorCard label="Identity Hardware" data={data.behavior_snapshot?.top_devices} />
                             
                             <div className="col-span-1 md:col-span-2 orca-card p-10 h-[400px] relative overflow-hidden group">
                                <div className="text-[10px] uppercase font-black text-slate-500 tracking-[0.4em] italic mb-10 flex items-center space-x-3 leading-none">
                                    <span className="w-2 h-2 rounded-full bg-indigo-500" />
                                    <span>24h Temporal Distribution</span>
                                </div>
                                <div className="h-2/3 w-full flex items-end justify-between px-4">
                                    {(Object.entries(data.behavior_snapshot?.transaction_hours_counts || {}).map(([hour, count]) => (
                                        <div key={hour} className="group relative flex-1 flex flex-col items-center mx-1">
                                            <div className="absolute -top-8 text-[9px] text-white font-mono opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap bg-indigo-600 px-2 py-0.5 rounded shadow-lg">{count} NODES</div>
                                            <div 
                                                className={`w-full bg-indigo-500 transition-all rounded-t-lg shadow-sm
                                                    ${count > 0 ? 'opacity-40 hover:opacity-100 hover:shadow-[0_0_15px_rgba(99,102,241,0.5)]' : 'opacity-5'}`} 
                                                style={{ height: `${(count / Math.max(...Object.values(data.behavior_snapshot?.transaction_hours_counts || {x:1}))) * 100}%` }} 
                                            />
                                            <div className="text-[8px] text-slate-600 mt-4 font-mono font-black italic">{hour}H</div>
                                        </div>
                                    )))}
                                </div>
                                <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                             </div>
                         </div>

                         {/* Side Forensic Intelligence */}
                         <div className="col-span-12 lg:col-span-4 space-y-10">
                             <DeviceIntelligenceCard signals={data.synthetic_identity_signals} />
                             <div className="orca-card p-10 bg-gradient-to-br from-indigo-500/[0.05] via-transparent to-transparent group overflow-hidden">
                                <div className="flex items-center space-x-3 mb-6">
                                    <span className="text-lg">🧬</span>
                                    <h3 className="text-xs uppercase font-black text-white italic tracking-[0.3em]">Neural Insight</h3>
                                </div>
                                <p className="text-[11px] text-slate-500 font-bold italic leading-[2] tracking-wide opacity-60 group-hover:opacity-100 transition-opacity">
                                    This node exhibits <span className="text-indigo-400">{data.behavior_snapshot?.top_locations?.length} unique locations</span> across its transaction lifespan. 
                                    Significant deviation from baseline behavior is noted in its <span className="text-white font-black italic">Temporal Sync Window</span>.
                                </p>
                                <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                             </div>
                         </div>
                     </div>
                </div>
            )}

            {!loading && !data && (
                <div className="p-40 text-center orca-card border-dashed bg-transparent group relative overflow-hidden">
                    <span className="text-[10px] font-black uppercase font-mono tracking-[0.4em] italic text-slate-600">Awaiting Target Identity Parameter...</span>
                    <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
                </div>
            )}
        </motion.div>
    );
};

export default Behavior;
