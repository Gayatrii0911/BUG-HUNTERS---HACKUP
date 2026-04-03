import { useState } from 'react';
import { runScenario, resetSystem } from '../services/api';

const SCENARIOS = [
  { id: 'normal_user', name: 'Normal Activity', desc: 'Legitimate behavioral baseline' },
  { id: 'new_device_anomaly', name: 'Identity Drift', desc: 'New device + unusual amount' },
  { id: 'cycle_fraud', name: 'Circular Laundering', desc: 'A → B → C → A pattern' },
  { id: 'mule_hub', name: 'Mule Hub', desc: 'One-to-many fan-out distribution' },
  { id: 'layering_chain', name: 'Layering Chain', desc: 'Multi-hop fund dispersal' },
  { id: 'account_takeover', name: 'Account Takeover', desc: 'Compromised access + abuse' },
  { id: 'coordinated_synergy', name: 'Elite Synergy', desc: 'Graph Pattern + AI Anomaly' },
  { id: 'repeated_suspicious', name: 'Adaptive History', desc: 'Escalation based on history' }
];

const Simulation = () => {
  const [running, setRunning] = useState(null);
  const [msg, setMsg] = useState('');

  const handleRun = async (id) => {
    setRunning(id);
    setMsg(`Executing scenario: ${id.toUpperCase()}...`);
    try {
      const res = await runScenario(id);
      setMsg(`Success: ${res.results.length} transactions processed. Decision: ${res.results[res.results.length-1].decision}`);
    } catch (err) {
      setMsg('Execution failed. Check backend console.');
    } finally {
      setRunning(null);
    }
  };

  const handleReset = async () => {
     if (!window.confirm("Reset entire system state?")) return;
     try {
       await resetSystem();
       setMsg('System Reset Successful. Graph and Profiles cleared.');
     } catch (err) {
       setMsg('Reset failed.');
     }
  };

  return (
    <div className="space-y-8 fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold font-display text-white">Scenario Simulation</h2>
          <p className="text-sm text-slate-500 mt-1">Replay and validate elite fraud patterns in real-time.</p>
        </div>
        <button onClick={handleReset} className="px-6 py-2 border border-red-500/30 text-red-400 rounded-xl font-bold hover:bg-red-500/10 transition-all">
          System Reset
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {SCENARIOS.map((s) => (
          <div key={s.id} className="card group relative overflow-hidden">
             <div className="relative z-10 space-y-2">
                <h3 className="font-bold text-white group-hover:text-[#3182ce] transition-colors">{s.name}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{s.desc}</p>
                <div className="pt-4">
                  <button 
                    disabled={running !== null}
                    onClick={() => handleRun(s.id)}
                    className={`text-xs font-bold px-4 py-2 rounded-lg bg-[#2d3748] text-white transition-all hover:bg-[#3182ce] ${running === s.id ? 'animate-pulse bg-blue-500' : ''}`}
                  >
                    {running === s.id ? 'Running...' : 'Execute Replay'}
                  </button>
                </div>
             </div>
             <div className="absolute right-0 bottom-0 opacity-5 group-hover:opacity-10 transition-opacity">
                <div className="w-20 h-20 bg-white rotate-12 transform translate-x-10 translate-y-10"></div>
             </div>
          </div>
        ))}
      </div>

      {msg && (
        <div className="p-4 bg-[#1a1c2e] border border-[#2d3748] rounded-xl font-mono text-xs text-[#3182ce] flex items-center space-x-3">
           <span className="w-1.5 h-1.5 rounded-full bg-[#3182ce] animate-ping"></span>
           <span>LOG: {msg}</span>
        </div>
      )}

      <div className="p-8 border-2 border-dashed border-[#2d3748] rounded-3xl text-center space-y-3">
         <h3 className="text-sm font-bold text-slate-500">Live Decision Stream</h3>
         <p className="text-xs text-slate-600">The dashboard will update automatically as scenarios are replayed.</p>
      </div>
    </div>
  );
}

export default Simulation;