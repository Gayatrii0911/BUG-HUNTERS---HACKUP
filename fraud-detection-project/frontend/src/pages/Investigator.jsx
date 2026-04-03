import { useState, useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import { fetchTrace, fetchAccountSummary } from '../services/api';
import { motion } from 'framer-motion';

const Investigator = () => {
  const [accountId, setAccountId] = useState('BOSS');
  const [loading, setLoading] = useState(false);
  const [accountData, setAccountData] = useState(null);
  const containerRef = useRef(null);
  const cyRef = useRef(null);

  const [graphPayload, setGraphPayload] = useState(null);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await fetchTrace(accountId);
      const summary = await fetchAccountSummary(accountId);
      setAccountData(summary);
      if (data && data.status === "success") {
          setGraphPayload(data.graph_payload || { nodes: [], edges: [] });
      }
    } catch (err) {
      console.error("Pathfinder link fault:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch();
  }, []);

  useEffect(() => {
    if (graphPayload && containerRef.current) {
        initGraph(graphPayload);
    }
  }, [graphPayload]);

  const initGraph = (graphData) => {
    const nodes = (graphData.nodes || []).map(n => {
        const d = n.data || n;
        let color = '#3182ce';
        if (d.risk_score >= 70) color = '#ef4444';
        else if (d.risk_score >= 40) color = '#ecc94b';
        return { data: { ...d, color } };
    });

    const edges = (graphData.edges || []).map(e => ({ data: { ...(e.data || e) } }));

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: [...nodes, ...edges],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(color)',
            'label': 'data(label)',
            'color': '#fff',
            'font-size': '10px',
            'width': '40px',
            'height': '40px',
            'text-valign': 'center',
            'border-width': 4,
            'border-color': 'rgba(255,255,255,0.1)',
            'shape': 'ellipse',
            'text-margin-y': -25,
            'font-weight': 'bold'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': 'rgba(99,102,241,0.2)',
            'target-arrow-color': 'rgba(99,102,241,0.2)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '8px',
            'color': '#4a5568'
          }
        },
        {
            selector: 'node:selected',
            style: { 'border-color': '#fff', 'border-width': 6 }
        }
      ],
      layout: { name: 'cose', padding: 50, animate: true }
    });

    cyRef.current.on('tap', 'node', async (evt) => {
        const id = evt.target.id();
        setAccountId(id);
        const summ = await fetchAccountSummary(id);
        setAccountData(summ);
    });
  };

  return (
    <div className="space-y-12 max-w-[1800px] mx-auto px-6 py-6 fade-in">
       <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-8 border-b border-white/5 pb-10">
          <div className="space-y-1">
             <div className="text-[10px] uppercase font-black tracking-[0.6em] text-blue-500 mb-2 italic">Neural Network Investigator</div>
             <h2 className="text-5xl font-display font-black text-white italic tracking-tighter shadow-sm">
                Forensic <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-400">Pathfinder</span>
             </h2>
             <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-2 opacity-60">Visualizing Structural Laundering and Circular Nodal Synergies</p>
          </div>
          
          <div className="flex bg-white/[0.03] p-1.5 border border-white/10 rounded-2xl shadow-2xl">
             <input 
               type="text" 
               value={accountId}
               onChange={(e) => setAccountId(e.target.value)}
               className="bg-transparent px-6 py-3 text-sm text-white font-mono placeholder:text-slate-700 focus:outline-none w-64 uppercase"
               placeholder="TARGET_NODE_ID..."
             />
             <button 
               onClick={handleSearch} 
               className="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-black text-[10px] uppercase tracking-widest transition-all is-3d italic"
             >
                Trace Origin
             </button>
          </div>
       </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-10">
        {/* Graph Container */}
        <div className="xl:col-span-8 orca-card p-0 h-[700px] overflow-hidden relative shadow-[0_0_100px_rgba(30,58,138,0.1)] border-white/10 group">
          {loading && (
             <div className="absolute inset-0 bg-black/60 backdrop-blur-md flex flex-col items-center justify-center z-50 text-white space-y-4">
                <div className="w-16 h-16 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin shadow-[0_0_20px_#3b82f6]" />
                <div className="text-[10px] font-black uppercase tracking-[0.6em] italic animate-pulse">Running Neural Trace...</div>
             </div>
          )}
          <div ref={containerRef} className="w-full h-full cursor-crosshair" />
          <div className="absolute bottom-8 right-8 flex space-x-4">
             <div className="bg-black/50 backdrop-blur-xl border border-white/10 p-6 rounded-2xl flex space-x-8">
                <div className="flex items-center space-x-3">
                   <div className="w-3 h-3 rounded bg-blue-500 shadow-[0_0_10px_#3b82f6]" />
                   <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest italic">Stable</span>
                </div>
                <div className="flex items-center space-x-3">
                   <div className="w-3 h-3 rounded bg-yellow-500 shadow-[0_0_10px_#eab308]" />
                   <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest italic">Anomalous</span>
                </div>
                <div className="flex items-center space-x-3">
                   <div className="w-3 h-3 rounded bg-red-500 shadow-[0_0_10px_#ef4444]" />
                   <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest italic">Structural Risk</span>
                </div>
             </div>
          </div>
        </div>

        {/* Account Details / Stats */}
        <div className="xl:col-span-4 flex flex-col space-y-10">
           <div className="orca-card p-10 bg-gradient-to-tr from-white/[0.02] to-transparent border-white/10 group">
             <h3 className="text-[10px] uppercase font-black text-slate-500 mb-8 tracking-[0.4em] italic leading-none border-b border-white/5 pb-6">Account Behavioral Profile</h3>
             <div className="space-y-8">
                <div className="flex justify-between items-center">
                   <span className="text-[10px] text-slate-600 font-black uppercase italic tracking-widest">Nodal Signature</span>
                   <span className="font-mono text-lg text-white font-black italic tracking-tighter">[{accountData?.account_id || accountId}]</span>
                </div>
                <div className="flex justify-between items-center">
                   <span className="text-[10px] text-slate-600 font-black uppercase italic tracking-widest">Integrity Status</span>
                   <span className={`px-5 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest italic border ${accountData?.is_fraudulent ? 'bg-red-500/10 text-red-500 border-red-500/20 shadow-[0_0_20px_rgba(239,68,68,0.2)]' : 'bg-green-500/10 text-green-500 border-green-500/20 shadow-[0_0_20px_rgba(34,197,94,0.1)]'}`}>
                      {accountData?.is_fraudulent ? 'Suspicious Hub' : 'Verified Node'}
                   </span>
                </div>
                <div className="pt-6 border-t border-white/5">
                   <div className="text-[9px] text-slate-600 font-black uppercase mb-4 tracking-[0.3em] italic">ML Anomaly Intensity</div>
                   <div className="w-full h-2 bg-black/40 rounded-full border border-white/5 overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${(accountData?.recent_alerts?.[0]?.risk_score || 20)}%` }}
                        className={`h-full ${accountData?.is_fraudulent ? 'bg-red-500 shadow-[0_0_10px_#ef4444]' : 'bg-blue-500 shadow-[0_0_10px_#3b82f6]'}`}
                      />
                   </div>
                </div>
             </div>
             <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
           </div>

           <div className="orca-card p-10 flex-1 border-white/5 group relative overflow-hidden bg-white/[0.01]">
              <h3 className="text-[10px] uppercase font-black text-slate-500 mb-8 tracking-[0.4em] italic leading-none border-b border-white/5 pb-6">Pattern Recognition Engine</h3>
              <div className="space-y-4">
                 {accountData?.recent_alerts?.length > 0 ? accountData.recent_alerts.map((alert, i) => (
                    <div key={i} className="p-6 bg-red-400/[0.03] border border-red-400/10 rounded-2xl group/alert hover:bg-red-400/5 transition-all">
                       <div className="flex items-center space-x-4 mb-3">
                          <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse shadow-[0_0_10px_#ef4444]"></div>
                          <span className="text-[10px] font-black uppercase text-red-400 tracking-widest italic">{alert.pattern || 'Suspicious Outflow'}</span>
                       </div>
                       <p className="text-[11px] text-slate-500 font-bold italic leading-relaxed lowercase tracking-wider pl-6">
                           "{alert.reasons?.[0] || 'structural relationship risk exceeding 75% threshold based on modal flow analysis'}"
                       </p>
                    </div>
                 )) : <div className="p-12 text-center text-[10px] text-slate-700 font-black uppercase italic tracking-widest opacity-40">No network-based patterns detected for this node.</div>}
              </div>
              <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
           </div>
        </div>
      </div>
    </div>
  );
};

export default Investigator;
