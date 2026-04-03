import { useState, useEffect } from 'react';
import { fetchAlerts, fetchHealth } from '../services/api';
import AlertCard from '../components/AlertCard';

const Dashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({ total: 0, high_risk: 0, blocked: 0, mfa: 0 });
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchAlerts();
        const h = await fetchHealth();
        setAlerts(data);
        setHealth(h);
        
        // Compute stats
        const high = data.filter(a => a.risk_score >= 70).length;
        const blocked = data.filter(a => a.action === 'BLOCK').length;
        const mfa = data.filter(a => a.action === 'MFA').length;
        setStats({ total: data.length, high_risk: high, blocked, mfa });
      } catch (e) {
        console.error("Dashboard load failed", e);
      } finally {
        setLoading(false);
      }
    };
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-8 fade-in">
      
      {/* Header Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total Threats', value: stats.total, color: 'text-white' },
          { label: 'High Priority', value: stats.high_risk, color: 'text-red-400' },
          { label: 'Blocked Attacks', value: stats.blocked, color: 'text-red-500' },
          { label: 'MFA Challenges', value: stats.mfa, color: 'text-orange-400' }
        ].map((s, i) => (
          <div key={i} className="bg-[#1a1c2e] border border-[#2d3748] rounded-2xl p-6 shadow-lg">
             <div className="text-[10px] uppercase font-bold text-[#718096] tracking-widest mb-1">{s.label}</div>
             <div className={`text-3xl font-black font-display ${s.color}`}>{s.value}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Latest Activity Feed */}
        <div className="lg:col-span-2 space-y-4">
           <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">Live Suspicious Feed</h3>
              <div className="text-[10px] text-green-400 flex items-center space-x-1">
                 <span className="w-1 h-1 rounded-full bg-green-400 animate-ping"></span>
                 <span>Real-time Stream</span>
              </div>
           </div>
           
           <div className="space-y-3 max-h-[600px] overflow-auto pr-2">
              {alerts.length > 0 ? alerts.slice(0, 10).map((alert) => (
                <AlertCard key={alert.alert_id} alert={alert} />
              )) : <div className="text-xs text-slate-600 p-8 border border-dashed border-[#2d3748] rounded-2xl text-center">No security alerts detected in recent stream.</div>}
           </div>
        </div>

        {/* System Health / Intelligence Panel */}
        <div className="space-y-6">
           <div className="card space-y-4">
              <h3 className="text-xs font-bold text-[#718096] uppercase tracking-widest">Intelligence Health</h3>
              <div className="space-y-3">
                 <div className="flex justify-between items-center text-xs">
                    <span>Engine Version</span>
                    <span className="text-white font-mono">{health?.version || 'v1.2.1'}</span>
                 </div>
                 <div className="flex justify-between items-center text-xs">
                    <span>ML Outlier Detection</span>
                    <span className="text-green-400">ACTIVE</span>
                 </div>
                 <div className="flex justify-between items-center text-xs">
                    <span>Graph Engine</span>
                    <span className="text-green-400">SYNCED</span>
                 </div>
                 <div className="flex justify-between items-center text-xs">
                    <span>System Uptime</span>
                    <span className="text-white">{health?.uptime_seconds || 0}s</span>
                 </div>
              </div>
           </div>

           <div className="card bg-gradient-to-br from-[#3182ce]/5 to-transparent">
              <h3 className="text-xs font-bold text-[#3182ce] uppercase tracking-widest mb-3">Adaptive Intelligence</h3>
              <p className="text-[10px] text-slate-500 leading-relaxed mb-4">
                The core engine is currently processing <span className="text-white">{stats.total}</span> behavioral fingerprints. Retraining loop scheduled for next 20 anomalous samples.
              </p>
              <div className="h-1.5 w-full bg-[#0f111a] rounded-full overflow-hidden">
                 <div className="h-full bg-[#3182ce] w-[65%]" />
              </div>
           </div>
        </div>

      </div>
    </div>
  );
}

export default Dashboard;