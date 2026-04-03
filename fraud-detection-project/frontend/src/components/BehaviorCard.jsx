import { motion } from 'framer-motion';

const BehaviorCard = ({ label, data }) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="cyber-card p-10 space-y-8 group/behavior relative bg-gradient-to-tr from-white/[0.02] to-transparent overflow-hidden">
      <div className="text-[11px] uppercase font-black text-slate-500 tracking-[0.4em] flex items-center space-x-3 mb-6 italic border-b border-white/5 pb-6 leading-none">
        <span className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_10px_#3b82f6]" />
        <span>{label}</span>
      </div>
      <div className="space-y-6">
        {data.slice(0, 5).map(([item, count], i) => (
          <div key={i} className="space-y-3 group/item">
            <div className="flex justify-between text-[10px] items-center italic">
              <span className="text-slate-400 font-bold tracking-widest font-mono truncate mr-2 uppercase group-hover/item:text-slate-200 transition-colors">{item}</span>
              <span className="text-white font-black tabular-nums">{count} NODES</span>
            </div>
            <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden border border-white/5 shadow-inner">
               <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(100, (count / Math.max(...data.map(d => d[1]))) * 100)}%` }} 
                  transition={{ duration: 1.5, delay: i * 0.1 }}
                  className={`h-full bg-blue-600 shadow-[0_0_10px_rgba(59,130,246,0.3)] opacity-60 group-hover/item:opacity-100 transition-all`} 
               />
            </div>
          </div>
        ))}
      </div>
      <div className="hologram-overlay opacity-5 group-hover/behavior:opacity-10 transition-opacity" />
    </div>
  );
};

export default BehaviorCard;
