import { motion } from 'framer-motion';

const MetricCard = ({ label, value, icon, variant = 'blue' }) => {
  const getGlow = () => {
    switch(variant) {
      case 'red': return 'shadow-[0_0_20px_rgba(239,68,68,0.2)] border-red-500/20';
      case 'amber': return 'shadow-[0_0_20px_rgba(245,158,11,0.2)] border-amber-500/20';
      default: return 'shadow-[0_0_20px_rgba(99,102,241,0.2)] border-indigo-500/20';
    }
  };

  const getTextColor = () => {
    switch(variant) {
      case 'red': return 'text-red-500';
      case 'amber': return 'text-amber-500';
      default: return 'text-indigo-400';
    }
  };

  return (
    <motion.div 
      whileHover={{ scale: 1.02, y: -5 }}
      className={`orca-card h-full flex flex-col justify-between group overflow-hidden relative ${getGlow()}`}
    >
      <div className="flex justify-between items-start">
        <div className="space-y-4">
          <span className="text-[10px] font-black uppercase text-slate-500 tracking-[0.3em] italic group-hover:text-slate-300 transition-colors leading-none">{label}</span>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-black text-white italic tracking-tighter shadow-sm">{value}</span>
            {typeof value === 'number' && <span className="text-[8px] font-bold text-slate-600 uppercase tracking-widest">+12%</span>}
          </div>
        </div>
        <div className="w-10 h-10 rounded-xl bg-black/40 border border-white/5 flex items-center justify-center grayscale group-hover:grayscale-0 transition-all text-sm group-hover:shadow-[0_0_15px_rgba(255,255,255,0.1)]">
          {icon}
        </div>
      </div>

      <div className="w-full h-[2px] bg-white/5 rounded-full overflow-hidden mt-4">
         <motion.div 
            initial={{ width: 0 }}
            animate={{ width: '65%' }}
            className={`h-full opacity-60 ${variant === 'red' ? 'bg-red-500' : variant === 'amber' ? 'bg-amber-500' : 'bg-indigo-500'}`} 
         />
      </div>

      <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
    </motion.div>
  );
};

export default MetricCard;
