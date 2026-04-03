import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldCheck, ShieldAlert, ShieldX } from 'lucide-react';

const DecisionBadge = ({ decision }) => {
  const isBlock = decision === 'BLOCK';
  
  const config = {
    BLOCK: {
      color: 'bg-cyber-danger/20 border-cyber-danger text-cyber-danger',
      icon: <ShieldX className="w-5 h-5" />,
      text: 'SYSTEM BLOCKED',
      glow: 'shadow-[0_0_20px_rgba(255,0,60,0.4)]',
      pulse: 'pulse-red'
    },
    MFA: {
      color: 'bg-cyber-warning/20 border-cyber-warning text-cyber-warning',
      icon: <ShieldAlert className="w-5 h-5" />,
      text: 'MFA REQUIRED',
      glow: 'shadow-[0_0_20px_rgba(255,204,0,0.4)]',
      pulse: ''
    },
    APPROVE: {
      color: 'bg-cyber-success/20 border-cyber-success text-cyber-success',
      icon: <ShieldCheck className="w-5 h-5" />,
      text: 'CLEAN PASS',
      glow: 'shadow-[0_0_20px_rgba(57,255,20,0.4)]',
      pulse: ''
    }
  };

  const current = config[decision] || config.APPROVE;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={decision}
        initial={{ opacity: 0, x: -20, scale: 0.9 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        exit={{ opacity: 0, x: 20, scale: 0.9 }}
        className={`flex items-center space-x-3 px-6 py-3 rounded-xl border-2 font-black tracking-tighter
                    ${current.color} ${current.glow} ${current.pulse}`}
      >
        <motion.div
          animate={isBlock ? { scale: [1, 1.2, 1] } : {}}
          transition={{ repeat: Infinity, duration: 1.5 }}
        >
          {current.icon}
        </motion.div>
        <span className="text-sm uppercase">{current.text}</span>
      </motion.div>
    </AnimatePresence>
  );
};

export default DecisionBadge;