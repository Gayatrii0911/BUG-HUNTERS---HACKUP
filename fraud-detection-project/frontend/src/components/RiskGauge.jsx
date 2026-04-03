import React from 'react';
import { motion } from 'framer-motion';

const RiskGauge = ({ score }) => {
  const getLevelColor = (s) => {
    if (s >= 70) return 'text-cyber-danger';
    if (s >= 40) return 'text-cyber-warning';
    return 'text-cyber-low';
  };

  const getGlowColor = (s) => {
    if (s >= 70) return 'rgba(255, 0, 60, 0.4)';
    if (s >= 40) return 'rgba(255, 204, 0, 0.4)';
    return 'rgba(16, 185, 129, 0.4)';
  };

  return (
    <div className="relative flex flex-col items-center justify-center p-8 glass-card">
      <h3 className="absolute top-4 left-6 text-[10px] uppercase font-bold tracking-[0.2em] text-slate-500">
        Risk Assessment Meter
      </h3>
      
      <div className="relative w-48 h-48 flex items-center justify-center">
        {/* Glow Background */}
        <motion.div 
          className="absolute inset-0 rounded-full blur-2xl opacity-20"
          animate={{ backgroundColor: getGlowColor(score) }}
        />
        
        {/* SVG Circle */}
        <svg className="w-full h-full transform -rotate-90">
          <circle
            cx="96"
            cy="96"
            r="88"
            stroke="currentColor"
            strokeWidth="12"
            fill="transparent"
            className="text-cyber-border"
          />
          <motion.circle
            cx="96"
            cy="96"
            r="88"
            stroke="currentColor"
            strokeWidth="12"
            fill="transparent"
            strokeDasharray="552.92"
            initial={{ strokeDashoffset: 552.92 }}
            animate={{ strokeDashoffset: 552.92 - (552.92 * score) / 100 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            className={getLevelColor(score)}
            style={{ filter: `drop-shadow(0 0 8px ${getGlowColor(score)})` }}
          />
        </svg>

        {/* Score Value */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span 
            className="text-5xl font-black font-display text-white"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            {score.toFixed(1)}
          </motion.span>
          <span className="text-[10px] uppercase font-bold text-slate-500 tracking-widest mt-1">
            Global Risk
          </span>
        </div>
      </div>
      
      {/* Risk Level Tag */}
      <motion.div 
        className={`mt-6 px-4 py-1 rounded-full border text-[10px] font-black uppercase tracking-widest
                    ${score >= 70 ? 'border-cyber-danger/30 text-cyber-danger bg-cyber-danger/10' : 
                      score >= 40 ? 'border-cyber-warning/30 text-cyber-warning bg-cyber-warning/10' : 
                      'border-cyber-low/30 text-cyber-low bg-cyber-low/10'}`}
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        {score >= 70 ? 'CRITICAL THREAT' : score >= 40 ? 'ELEVATED RISK' : 'LOW CLEARANCE'}
      </motion.div>
    </div>
  );
};

export default RiskGauge;
