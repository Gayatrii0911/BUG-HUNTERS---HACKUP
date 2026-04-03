import { motion } from 'framer-motion';

const RiskBreakdown = ({ components }) => {
  if (!components) return (
     <div className="flex flex-col items-center justify-center p-20 opacity-20 italic font-black uppercase text-[10px] tracking-[0.4em] text-slate-500">
        Neural Ingress Inactive
     </div>
  );

  const factors = [
    { label: 'Network Graph Cluster', value: components.graph_risk, color: 'bg-indigo-500', icon: '🌐' },
    { label: 'Ensemble ML Anomaly', value: components.ml_risk, color: 'bg-indigo-600', icon: '🧠' },
    { label: 'Behavioral Baseline', value: components.behavior_risk, color: 'bg-indigo-700', icon: '👤' },
    { label: 'Identity Hardware', value: components.device_risk, color: 'bg-indigo-800', icon: '📱' },
  ];

  return (
    <div className="space-y-12 h-full flex flex-col justify-between">
      <div className="text-[10px] uppercase font-black text-slate-500 tracking-[0.4em] flex items-center justify-between border-b border-white/5 pb-6 italic">
         <div className="flex items-center space-x-3">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 shadow-[0_0_8px_#6366f1]" />
            <span>Neural Fusion Breakdown</span>
         </div>
         <span className="text-indigo-400 opacity-60">Matrix Weight 2.4</span>
      </div>

      <div className="space-y-10 flex-1">
        {factors.map((f, i) => (
          <div key={i} className="space-y-4 group/factor">
            <div className="flex justify-between text-xs font-medium items-end">
              <span className="text-slate-500 flex items-center space-x-4 opacity-60 group-hover/factor:opacity-100 transition-opacity">
                 <span className="text-sm grayscale group-hover/factor:grayscale-0 transition-grayscale">{f.icon}</span>
                 <span className="uppercase tracking-[0.2em] font-black text-[9px] italic leading-none">{f.label}</span>
              </span>
              <span className="text-white font-mono text-[11px] tabular-nums italic">{f.value.toFixed(1)}%</span>
            </div>
            <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden flex shadow-inner border border-white/5 relative">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${f.value}%` }} 
                transition={{ duration: 1.5, delay: i * 0.1 }}
                className={`h-full ${f.color} shadow-[0_0_15px_rgba(99,102,241,0.3)] transition-all ease-out`} 
              />
            </div>
          </div>
        ))}
      </div>

      <div className="pt-8 border-t border-white/5 text-center flex flex-col items-center">
         <span className="text-[9px] text-slate-600 uppercase tracking-[0.6em] font-black group-hover:text-white transition-colors cursor-default italic mb-4">Intelligence Fusion Fabric</span>
         <div className="flex items-center space-x-2 text-[8px] font-mono text-indigo-500 opacity-40">
            <span>[ COORDINATED_SIG: READY ]</span>
            <span>[ ADAPTIVE_RETRAIN: 99% ]</span>
         </div>
      </div>
      
      <div className="hologram-overlay opacity-5 pointer-events-none" />
    </div>
  );
};

export default RiskBreakdown;