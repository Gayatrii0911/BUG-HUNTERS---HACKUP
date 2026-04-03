import { motion } from 'framer-motion';

const NeuralRiskMeter = ({ score = 0, status = "SAFE" }) => {
  const radius = 80;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;
  
  const getSeverityColor = (s) => {
    if (s >= 75) return '#ef4444'; // Red
    if (s >= 40) return '#f59e0b'; // Amber
    return '#6366f1'; // Indigo
  };

  const color = getSeverityColor(score);

  return (
    <div className="relative flex flex-col items-center justify-center group h-fit">
      <svg className="w-64 h-64 transform -rotate-90 drop-shadow-[0_0_15px_rgba(99,102,241,0.2)]">
        {/* Background Track */}
        <circle
          cx="128"
          cy="128"
          r={radius}
          stroke="currentColor"
          strokeWidth="12"
          fill="transparent"
          className="text-white/[0.05]"
        />
        {/* Progress Circle */}
        <motion.circle
          cx="128"
          cy="128"
          r={radius}
          stroke={color}
          strokeWidth="14"
          fill="transparent"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: circumference - progress }}
          transition={{ duration: 2, ease: "easeOut" }}
          strokeLinecap="round"
          className="filter drop-shadow-[0_0_10px_var(--tw-shadow-color)]"
          style={{ '--tw-shadow-color': color }}
        />
        
        {/* Glowing Pulse Effect for high risk */}
        {score >= 70 && (
          <circle
            cx="128"
            cy="128"
            r={radius}
            stroke={color}
            strokeWidth="20"
            fill="transparent"
            className="animate-ping opacity-20"
          />
        )}
      </svg>

      {/* Central Stats Panel */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.span 
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="text-[10px] font-black uppercase text-slate-500 tracking-[0.4em] mb-2 italic"
        >
          Neural Risk
        </motion.span>
        <div className="flex items-baseline">
            <motion.span 
              className="text-5xl font-black text-white italic tabular-nums pr-1 leading-none shadow-sm"
              animate={{ color: ['#fff', color, '#fff'] }}
              transition={{ duration: 4, repeat: Infinity }}
            >
              {score.toFixed(0)}
            </motion.span>
            <span className="text-xl font-bold text-slate-600">%</span>
        </div>
        <div className={`mt-4 px-4 py-1.5 rounded-full border border-white/5 bg-black/40 backdrop-blur-md transition-all duration-500
            ${score >= 70 ? 'border-red-500/30' : 'border-indigo-500/20'}
        `}>
            <span className="text-[9px] font-black uppercase tracking-[0.3em] italic" style={{ color }}>
                {status}
            </span>
        </div>
      </div>

      {/* Auxiliary Metadata HUD */}
      <div className="mt-8 flex justify-between w-full px-6 text-[8px] font-black uppercase text-slate-600 tracking-widest italic group-hover:text-slate-400 transition-colors">
         <div className="flex flex-col items-center">
            <span className="mb-1">Confidence</span>
            <span className="text-white">99.82%</span>
         </div>
         <div className="w-px h-6 bg-white/5 mx-4" />
         <div className="flex flex-col items-center">
            <span className="mb-1">Momentum</span>
            <span className={score > 50 ? 'text-red-500' : 'text-emerald-500'}>
                {score > 50 ? 'ACCELERATING' : 'STABLE'}
            </span>
         </div>
      </div>

      {/* Hologram Overlay */}
      <div className="hologram-overlay opacity-5 pointer-events-none" />
    </div>
  );
};

export default NeuralRiskMeter;
