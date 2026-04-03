import { motion } from 'framer-motion';

const DeviceIntelligenceCard = ({ signals }) => {
  if (!signals) return null;

  return (
    <div className="cyber-card p-10 space-y-10 group/device relative bg-gradient-to-bl from-blue-500/[0.05] to-transparent overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-white/5 to-transparent rounded-bl-full pointer-events-none" />
      
      <div className="relative z-10 space-y-8">
        <div className="text-[11px] uppercase font-black text-blue-500 tracking-[0.5em] flex items-center space-x-3 mb-6 italic border-b border-white/5 pb-6 leading-none">
            <span className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_10px_#3b82f6] animate-pulse" />
            <span>Biometric Hardware Audit</span>
        </div>

        <div className="space-y-6">
          <div className="flex flex-col space-y-3">
             <div className="flex justify-between items-end">
                <span className="text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em] italic">Linked Identity Count</span>
                <span className={`text-4xl font-black italic tracking-tighter drop-shadow-[0_0_20px_rgba(255,255,255,0.2)] ${signals.identity_count > 0 ? 'text-orange-400' : 'text-green-500'}`}>
                    {signals.identity_count}
                </span>
             </div>
             <div className="h-[2px] w-full bg-white/5 relative overflow-hidden rounded-full">
                <motion.div 
                    initial={{ x: '-100%' }}
                    animate={{ x: '100%' }}
                    transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                    className="absolute inset-y-0 w-1/3 bg-gradient-to-r from-transparent via-blue-500/50 to-transparent shadow-[0_0_10px_#3b82f6]" 
                />
             </div>
             <p className="text-[10px] text-slate-500 leading-loose italic opacity-60 group-hover/device:opacity-100 transition-opacity">
                "unique behavioral fingerprints detected originating from common hardware indices."
             </p>
          </div>

          <div className="pt-8 border-t border-white/5 space-y-4">
             <div className="text-[9px] uppercase font-black text-slate-600 tracking-[0.3em] italic">Associated Neural Signatures</div>
             <div className="flex flex-wrap gap-3">
                {signals.shared_hardware_users?.length > 0 ? signals.shared_hardware_users.map((uid, i) => (
                   <span key={uid} className="px-4 py-2 bg-black/40 text-blue-400 text-[10px] font-mono font-bold rounded-2xl border border-white/10 hover:border-blue-500/50 hover:bg-blue-500/10 transition-all cursor-pointer shadow-inner">
                      {uid}
                   </span>
                )) : (
                   <div className="text-[10px] text-slate-600 italic tracking-widest leading-none">NO_ASSOCIATIONS_DETECTED</div>
                )}
             </div>
          </div>
        </div>
      </div>
      <div className="hologram-overlay opacity-5 group-hover/device:opacity-10 transition-opacity" />
    </div>
  );
};

export default DeviceIntelligenceCard;
