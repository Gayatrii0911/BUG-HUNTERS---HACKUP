import { motion } from 'framer-motion';

const TracePanel = ({ profile, loading }) => {
  if (!profile && !loading) {
    return (
      <div className="p-12 orca-card border-dashed bg-transparent text-center space-y-10 group relative overflow-hidden">
        <div className="w-24 h-24 bg-white/5 rounded-[2rem] flex items-center justify-center mx-auto shadow-inner border border-white/5 is-3d group-hover:scale-110 transition-transform duration-500">
            <span className="text-5xl opacity-40 group-hover:opacity-100 transition-opacity">🕵️</span>
        </div>
        <div className="space-y-4">
            <h3 className="text-xs font-black text-white uppercase tracking-[0.4em] italic mb-4">Forensic Nodal Ghost</h3>
            <p className="text-[11px] text-slate-500 font-bold italic leading-loose lowercase tracking-widest max-w-[240px] mx-auto opacity-60">
               "identify a node signature to reveal its neural fingerprint and network flow lineage."
            </p>
        </div>
        <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
      </div>
    );
  }

  const riskScore = profile?.risk_score || (profile?.is_fraudulent ? 85 : 12);
  const confidence = 94.2;

  return (
    <div className="space-y-10 relative group h-full">
      {loading && (
        <div className="absolute inset-0 bg-[hsl(var(--bg-deep))/0.8] backdrop-blur-2xl z-30 flex items-center justify-center rounded-[1.5rem]">
            <div className="flex flex-col items-center space-y-4">
                <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin shadow-[0_0_20px_rgba(99,102,241,0.2)]" />
                <span className="text-[10px] font-black text-indigo-400 uppercase tracking-widest italic animate-pulse">Decryption In Progress</span>
            </div>
        </div>
      )}
      
      {/* Forensic Identity Header */}
      <section className="orca-card p-10 bg-gradient-to-tr from-white/[0.02] to-transparent overflow-hidden h-[240px]">
        <div className="flex justify-between items-start mb-10">
            <div className="space-y-2">
                <div className="text-[11px] uppercase font-black text-indigo-500 tracking-[0.4em] italic leading-none mb-4">Forensic ID context</div>
                <div className="text-3xl font-display font-black text-white italic tracking-tighter shadow-sm">NODE_{profile?.account_id?.slice(0, 10).toUpperCase()}</div>
            </div>
            <div className="w-12 h-12 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center shadow-inner group-hover:scale-110 transition-transform duration-700">
                ⚛️
            </div>
        </div>

        <div className="grid grid-cols-2 gap-8">
            <div className="flex flex-col">
                <span className="text-[9px] text-slate-600 font-black uppercase tracking-[0.3em] mb-2 px-1 italic">Confidence</span>
                <span className="text-3xl font-black text-indigo-400 font-mono italic tracking-tight">{confidence}%</span>
            </div>
             <div className="flex flex-col">
                <span className="text-[9px] text-slate-600 font-black uppercase tracking-[0.3em] mb-2 px-1 italic">Neural risk</span>
                <span className={`text-3xl font-black font-mono italic tracking-tight ${riskScore >= 70 ? 'text-red-500' : 'text-green-500'}`}>{riskScore}</span>
            </div>
        </div>
        <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
      </section>

      {/* Intelligence Trace Indicators */}
      <section className="orca-card p-10 space-y-8 h-[320px]">
        <div className="text-[10px] uppercase font-black text-slate-500 tracking-[0.4em] mb-4 italic leading-none border-b border-white/5 pb-4">Trace intelligence weight</div>
        <div className="space-y-8">
          {[
            { label: 'Flow Consistency', value: 82, color: 'from-indigo-600 to-indigo-400' },
            { label: 'Network Centrality', value: profile?.graph_connections * 10 || 48, color: 'from-indigo-600 to-indigo-400' },
            { label: 'Asset Velocity', value: 14, color: 'from-indigo-600 to-indigo-400' },
          ].map((attr, i) => (
            <div key={i} className="space-y-4">
                <div className="flex justify-between text-[10px] font-black uppercase text-slate-500 italic tracking-widest leading-none">
                    <span>{attr.label}</span>
                    <span className="text-white tabular-nums">{attr.value}%</span>
                </div>
                <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden border border-white/5 shadow-inner">
                    <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${attr.value}%` }}
                        transition={{ duration: 1.5, delay: i * 0.1 }}
                        className={`h-full bg-gradient-to-r ${attr.color} shadow-[0_0_10px_rgba(99,102,241,0.3)] opacity-60 hover:opacity-100 transition-opacity`} 
                    />
                </div>
            </div>
          ))}
        </div>
        <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
      </section>

      {/* Status Signature Block */}
      <section className="orca-card p-10 bg-gradient-to-b from-white/[0.03] to-transparent h-[160px]">
        <div className="text-[10px] uppercase font-black text-slate-500 tracking-[0.4em] mb-6 italic leading-none">Integrity Signals</div>
        <div className="grid grid-cols-1 gap-6">
             <div className="flex items-center justify-between group/status">
                <div className="flex items-center space-x-4">
                  <div className={`w-3 h-3 rounded-full ${riskScore >= 70 ? 'bg-red-500 animate-pulse shadow-[0_0_10px_#ef4444]' : 'bg-green-500 shadow-[0_0_10px_#22c55e]'}`} />
                  <span className="text-[11px] font-black text-slate-300 uppercase tracking-widest italic group-hover/status:text-white transition-colors">{riskScore >= 70 ? 'Fraudulent Cluster' : 'Verified Trusted Node'}</span>
                </div>
                <div className="text-[10px] text-slate-600 font-mono italic">Signature_{riskScore >= 70 ? 'X' : 'SAFE'}</div>
             </div>
             <div className="flex items-center justify-between group/traces">
                <div className="flex items-center space-x-4">
                  <div className="w-3 h-3 rounded-full bg-indigo-500 shadow-[0_0_10px_#6366f1]" />
                  <span className="text-[11px] font-black text-slate-300 uppercase tracking-widest italic group-hover/traces:text-white transition-colors">{profile?.transaction_count || 0} Relationship Traces</span>
                </div>
                <div className="text-[10px] text-slate-600 font-mono italic">Link_Count</div>
             </div>
        </div>
        <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
      </section>

      <div className="absolute -bottom-24 -left-24 w-80 h-80 bg-indigo-500/5 rounded-full blur-[100px] pointer-events-none group-hover:bg-indigo-500/10 transition-colors duration-1000" />
    </div>
  );
};

export default TracePanel;
