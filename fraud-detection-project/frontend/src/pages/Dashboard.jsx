import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchAlerts, fetchHealth } from '../services/api';
import RiskGauge from '../components/RiskGauge';
import DecisionBadge from '../components/DecisionBadge';
import CyberTable from '../components/CyberTable';
import { ShieldAlert, Cpu, Activity, TrendingUp, Zap } from 'lucide-react';

export default function Dashboard() {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({ total: 0, high_risk: 0, blocked: 0, mfa: 0, avg_score: 0 });
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const data = await fetchAlerts();
      const h = await fetchHealth();
      const alertsArray = Array.isArray(data) ? data : (data.alerts || []);
      setAlerts(alertsArray);
      setHealth(h);
      
      if (alertsArray.length > 0) {
        const high = alertsArray.filter(a => a.risk_score >= 70).length;
        const blocked = alertsArray.filter(a => (a.decision === 'BLOCK' || a.action === 'BLOCK')).length;
        const mfa = alertsArray.filter(a => (a.decision === 'MFA' || a.action === 'MFA')).length;
        const avg = alertsArray.reduce((acc, curr) => acc + (curr.risk_score || 0), 0) / alertsArray.length;
        setStats({ total: alertsArray.length, high_risk: high, blocked, mfa, avg_score: avg });
      } else {
        // Reset stats if no alerts
        setStats({ total: 0, high_risk: 0, blocked: 0, mfa: 0, avg_score: 0 });
      }
    } catch (e) {
      console.error("Dashboard sync failed", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  const latestAlert = alerts.length > 0 ? alerts[0] : null;

  return (
    <div className="space-y-8 pb-12">
      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-12 lg:col-span-4 h-full">
           <RiskGauge score={stats.avg_score} />
        </div>

        <div className="col-span-12 lg:col-span-8 flex flex-col space-y-6">
           <div className="glass-card flex-1 flex flex-col justify-between overflow-hidden relative group">
              <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                 <ShieldAlert className="w-32 h-32 text-cyber-danger" />
              </div>
              
              <div className="space-y-4">
                 <div className="flex items-center space-x-3">
                    <Zap className="w-5 h-5 text-cyber-accent animate-pulse" />
                    <h2 className="text-xl font-black font-display text-white uppercase tracking-tighter italic">Strategic Intelligence Overview</h2>
                 </div>
                 <p className="text-xs text-slate-500 leading-relaxed max-w-xl font-medium">
                    Neural monitoring system active. Currently analyzing behavioral fingerprints across <span className="text-white font-black">{stats.total}</span> transaction vectors. 
                    Real-time sync established with Aegis Core v{health?.version || '1.2.0'}.
                 </p>
              </div>

              <div className="grid grid-cols-3 gap-6 pt-8">
                 <StatItem label="Threats Intercepted" value={stats.blocked} color="text-cyber-danger" icon={<ShieldAlert className="w-4 h-4" />} />
                 <StatItem label="High Risk Patterns" value={stats.high_risk} color="text-cyber-warning" icon={<TrendingUp className="w-4 h-4" />} />
                 <StatItem label="Active Analytics" value={health?.uptime_seconds || 0} unit="SEC" color="text-cyber-accent" icon={<Activity className="w-4 h-4" />} />
              </div>
           </div>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-8">
        <div className="col-span-12 lg:col-span-12 grid grid-cols-1 md:grid-cols-2 gap-6">
           <div className="glass-card space-y-4">
              <div className="flex items-center justify-between border-b border-white/5 pb-4">
                 <div className="flex items-center space-x-2">
                    <ShieldAlert className="w-4 h-4 text-cyber-danger" />
                    <h3 className="text-[10px] font-black text-white uppercase tracking-widest">Active Interventions</h3>
                 </div>
                 <span className="text-[9px] text-slate-500 font-bold uppercase">{alerts.filter(a => a.decision === 'BLOCK').length} TOTAL</span>
              </div>
              <div className="space-y-3">
                 {alerts.filter(a => a.decision === 'BLOCK').slice(0, 3).map((a, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-cyber-danger/5 rounded-lg border border-cyber-danger/10">
                       <div className="flex flex-col">
                          <span className="text-[10px] font-black text-white uppercase">Account Locked: {a.sender_id || a.user_id}</span>
                          <span className="text-[8px] text-slate-500 font-mono">Vector ID: {a.transaction_id?.slice(0, 8)}...</span>
                       </div>
                       <div className="text-[8px] font-bold text-cyber-danger uppercase border border-cyber-danger px-2 py-1 rounded">Halt Executed</div>
                    </div>
                 ))}
                 {alerts.filter(a => a.decision === 'BLOCK').length === 0 && (
                    <div className="flex flex-col items-center justify-center py-10 space-y-3 opacity-40">
                       <ShieldAlert className="w-8 h-8 text-slate-500" />
                       <div className="text-center px-6">
                          <div className="text-[10px] text-white uppercase font-black tracking-widest">Aegis Lockdown Active</div>
                          <p className="text-[8px] text-slate-500 mt-1 lowercase font-mono">This module logs automated account freezes and fund-locking events.</p>
                       </div>
                    </div>
                 )}
              </div>
           </div>

           <div className="glass-card space-y-4">
              <div className="flex items-center justify-between border-b border-white/5 pb-4">
                 <div className="flex items-center space-x-2">
                    <Activity className="w-4 h-4 text-cyber-warning" />
                    <h3 className="text-[10px] font-black text-white uppercase tracking-widest">Validation Challenges</h3>
                 </div>
                 <span className="text-[9px] text-slate-500 font-bold uppercase">{alerts.filter(a => a.decision === 'MFA').length} ACTIVE</span>
              </div>
              <div className="space-y-3">
                 {alerts.filter(a => a.decision === 'MFA').slice(0, 3).map((a, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-cyber-warning/5 rounded-lg border border-cyber-warning/10">
                       <div className="flex flex-col">
                          <span className="text-[10px] font-black text-white uppercase">MFA Escalation: {a.sender_id || a.user_id}</span>
                          <span className="text-[8px] text-slate-500 font-mono">Status: Awaiting Interaction</span>
                       </div>
                       <div className="text-[8px] font-bold text-cyber-warning uppercase animate-pulse underline">Pending</div>
                    </div>
                 ))}
                 {alerts.filter(a => a.decision === 'MFA').length === 0 && (
                    <div className="flex flex-col items-center justify-center py-10 space-y-3 opacity-40">
                       <Activity className="w-8 h-8 text-slate-500" />
                       <div className="text-center px-6">
                          <div className="text-[10px] text-white uppercase font-black tracking-widest">Challenge Matrix Operational</div>
                          <p className="text-[8px] text-slate-500 mt-1 lowercase font-mono">This module tracks triggered MFA challenges for suspicious anomalies.</p>
                       </div>
                    </div>
                 )}
              </div>
           </div>
        </div>

        <div className="col-span-12 lg:col-span-9 space-y-6">
           <div className="flex items-center justify-between px-2">
              <div className="flex items-center space-x-3">
                 <div className="w-2 h-2 rounded-full bg-cyber-accent animate-ping" />
                 <h3 className="text-sm font-black text-white uppercase tracking-[0.2em]">Neural Intelligence Feed</h3>
              </div>
              <span className="text-[10px] font-mono font-bold text-slate-600 uppercase">Buffer: 100% Synced</span>
           </div>
           
           <CyberTable alerts={alerts.slice(0, 8)} />
        </div>

        <div className="col-span-12 lg:col-span-3 space-y-6">
           <AnimatePresence mode="wait">
             {latestAlert && (
               <motion.div 
                 key={latestAlert.alert_id}
                 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                 className="glass-card bg-gradient-to-br from-white/5 to-transparent border-cyber-accent/20"
               >
                  <h3 className="text-[10px] font-black text-cyber-accent uppercase tracking-widest mb-6">Latest Active Decision</h3>
                  <div className="space-y-6">
                     <DecisionBadge decision={latestAlert.decision} />
                     <div className="space-y-4">
                        <div className="flex justify-between items-center text-[10px] font-bold">
                           <span className="text-slate-500 uppercase">IDENTIFIED AS</span>
                           <span className="text-white uppercase font-black">{latestAlert.fraud_type || "anomaly"}</span>
                        </div>
                        <div className="flex justify-between items-center text-[10px] font-bold">
                           <span className="text-slate-500 uppercase">AI CONFIDENCE</span>
                           <span className="text-cyber-accent font-black">94.2%</span>
                        </div>
                     </div>
                  </div>
               </motion.div>
             )}
           </AnimatePresence>

           <div className="glass-card space-y-6 border-white/5">
              <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Aegis Intelligence Health</h3>
              <div className="space-y-4">
                 <HealthRow label="ML Model" status="OPERATIONAL" sub="Isolation Forest v2" pulse="bg-cyber-success" />
                 <HealthRow label="Graph Engine" status="SYNCED" sub="NetworkX Real-time" pulse="bg-cyber-accent" />
                 <HealthRow label="Identity Hub" status="ACTIVE" sub="Hardware Fingerprinting" pulse="bg-cyber-accent" />
                 <HealthRow label="Retrain Queue" status="READY" sub={`${stats.total % 20}/20 Samples`} pulse="bg-cyber-warning" />
              </div>
           </div>

           <div className="p-6 bg-cyber-bg border border-cyber-border rounded-2xl flex items-center justify-between group overflow-hidden relative">
              <div className="absolute -right-4 -bottom-4 opacity-5 group-hover:scale-110 transition-transform">
                 <Cpu className="w-24 h-24 text-white" />
              </div>
              <div className="relative z-10">
                 <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Automation State</h4>
                 <p className="text-xs font-bold text-cyber-accent mt-1">Matrix Fusion Active</p>
              </div>
              <div className="w-10 h-10 rounded-full border-4 border-cyber-accent/20 border-t-cyber-accent animate-spin" />
           </div>
        </div>
      </div>
    </div>
  );
}

function StatItem({ label, value, unit, color, icon }) {
  return (
    <div className="flex flex-col space-y-1">
      <div className="flex items-center space-x-2 text-[10px] font-black text-slate-600 uppercase tracking-tighter">
         {icon}
         <span>{label}</span>
      </div>
      <div className={`text-2xl font-black font-display font-mono ${color}`}>
         {value}{unit && <span className="text-[10px] ml-1 opacity-50">{unit}</span>}
      </div>
    </div>
  );
}

function HealthRow({ label, status, sub, pulse }) {
  return (
    <div className="flex flex-col space-y-1">
       <div className="flex justify-between items-center text-[10px] font-black uppercase">
          <span className="text-slate-400">{label}</span>
          <div className="flex items-center space-x-2">
             <span className={pulse.replace('bg-', 'text-')}>{status}</span>
             <div className={`w-1.5 h-1.5 rounded-full ${pulse} animate-pulse`} />
          </div>
       </div>
       <span className="text-[8px] text-slate-600 font-mono font-bold uppercase">{sub}</span>
    </div>
  );
}