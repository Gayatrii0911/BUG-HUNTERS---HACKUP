import { motion } from 'framer-motion';

const FraudChainFlow = ({ chain }) => {
  if (!chain || chain.length === 0) return null;

  return (
    <div className="orca-card p-10 bg-gradient-to-br from-white/[0.02] to-transparent group overflow-hidden relative h-full">
      <div className="flex justify-between items-start mb-16">
         <div className="space-y-4">
            <h3 className="text-xs font-black uppercase text-indigo-500 tracking-[0.4em] italic mb-1">Fund Flow Lineage</h3>
            <div className="text-[10px] font-black text-slate-600 uppercase tracking-widest italic opacity-60">Verified Neural Cycle Trace [v2.4]</div>
         </div>
         <div className="flex items-center space-x-3 text-red-500 bg-red-500/10 border border-red-500/20 px-4 py-1.5 rounded-full animate-pulse shadow-[0_0_20px_rgba(239,68,68,0.2)]">
            <span className="w-2 h-2 rounded-full bg-red-500"></span>
            <span className="text-[9px] font-black uppercase tracking-[0.3em] italic">Cycle Detected</span>
         </div>
      </div>

      <div className="flex items-center justify-between px-16 relative h-40">
        {/* Continuous Flow Anim Line */}
        <div className="absolute inset-x-20 h-px bg-white/5 top-1/2 -translate-y-1/2 z-0" />
        <motion.div 
            initial={{ left: '0%' }}
            animate={{ left: '100%', opacity: [0, 0.4, 0] }}
            transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            className="absolute w-40 h-[2px] bg-gradient-to-r from-transparent via-indigo-500 to-transparent z-0 blur-[1px] top-1/2 -translate-y-1/2" 
        />

        {chain.map((node, i) => (
          <div key={i} className="relative z-10 flex flex-col items-center group/node mx-4">
            <motion.div 
               whileHover={{ scale: 1.15, rotate: -5 }}
               className={`w-16 h-16 rounded-[1.5rem] bg-black/60 border-2 flex items-center justify-center shadow-2xl transition-all duration-700 is-3d backdrop-blur-md cursor-pointer
                  ${node.isFraud ? 'border-red-500/60 shadow-[0_0_30px_rgba(239,68,68,0.2)]' : 'border-indigo-500/40 shadow-[0_0_20px_rgba(99,102,241,0.1)]'}
               `}
            >
               <span className="text-xs font-black text-white italic tracking-tighter shadow-sm">{node.label}</span>
            </motion.div>
            
            <div className="absolute -bottom-14 flex flex-col items-center w-max opacity-40 group-hover/node:opacity-100 transition-opacity duration-500">
                <span className="text-[8px] font-bold text-slate-500 uppercase tracking-[0.3em] italic leading-none mb-2">{node.role || 'Node'}</span>
                <span className="text-[10px] font-black text-white italic tabular-nums tracking-tighter">{node.id.slice(0, 10).toUpperCase()}</span>
            </div>

            {i < chain.length - 1 && (
               <div className="absolute left-[calc(100%+1rem)] top-1/2 -translate-y-1/2 z-20 pointer-events-none w-12 flex justify-center">
                  <motion.div 
                    animate={{ x: [0, 10, 0], opacity: [0.1, 1, 0.1] }}
                    transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.3 }}
                    className="text-indigo-500 text-2xl font-black italic shadow-lg"
                  >
                    ›
                  </motion.div>
               </div>
            )}
          </div>
        ))}
      </div>

      {/* Forensic Audit context footer */}
      <div className="mt-20 pt-8 border-t border-white/5 flex justify-between items-center text-[9px] font-black uppercase text-slate-600 tracking-[0.4em] italic group-hover:text-slate-400 transition-colors">
         <span>Forensic Nodal Context</span>
         <span className="text-indigo-400 opacity-60">Synthetic Cluster Match: High Confidence</span>
      </div>
      <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
    </div>
  );
};

export default FraudChainFlow;
