import { useState, useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import { fetchTrace, fetchAccountSummary } from '../services/api';

const Investigator = () => {
  const [accountId, setAccountId] = useState('BOSS');
  const [loading, setLoading] = useState(false);
  const [accountData, setAccountData] = useState(null);
  const containerRef = useRef(null);
  const cyRef = useRef(null);

  useEffect(() => {
     handleSearch();
  }, []);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await fetchTrace(accountId);
      const summary = await fetchAccountSummary(accountId);
      setAccountData(summary);
      initGraph(data.graph_data);
    } catch (err) {
      console.error("Trace failed", err);
    } finally {
      setLoading(false);
    }
  };

  const initGraph = (graphData) => {
    if (!containerRef.current) return;

    // Convert backend edges/nodes into Cytoscape format
    const elements = [
      ...graphData.nodes.map(n => ({ data: { id: n.id, label: n.label } })),
      ...graphData.edges.map((e, idx) => ({ data: { id: `e${idx}`, source: e.source, target: e.target, label: `Rs. ${e.amount}` } }))
    ];

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#3182ce',
            'label': 'data(label)',
            'color': '#fff',
            'font-size': '10px',
            'width': '30px',
            'height': '30px',
            'text-valign': 'center',
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#4a5568',
            'target-arrow-color': '#4a5568',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '8px',
            'color': '#cbd5e0'
          }
        }
      ],
      layout: { name: 'breadthfirst', directed: true, padding: 10 }
    });
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold font-display text-white">Forensic Investigator</h2>
        <div className="flex space-x-2">
           <input 
             type="text" 
             value={accountId}
             onChange={(e) => setAccountId(e.target.value)}
             className="bg-[#1a1c2e] border border-[#2d3748] rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-[#3182ce]"
             placeholder="Search Account ID..."
           />
           <button onClick={handleSearch} className="px-6 py-2 bg-[#3182ce] text-white rounded-xl font-bold">Investigate</button>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* Graph Container */}
        <div className="col-span-8 bg-[#1a1c2e] rounded-2xl border border-[#2d3748] h-[500px] overflow-hidden relative shadow-2xl">
          {loading && <div className="absolute inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-10 text-white font-bold">Analysing Flow...</div>}
          <div ref={containerRef} className="w-full h-full" />
        </div>

        {/* Account Details / Stats */}
        <div className="col-span-4 bg-[#1a1c2e] p-6 rounded-2xl border border-[#2d3748] space-y-6 shadow-2xl">
           <div>
             <h3 className="text-xs uppercase font-bold text-[#718096] mb-3 tracking-widest">Account Forensic Profile</h3>
             <div className="space-y-4">
                <div className="flex justify-between items-center text-sm">
                   <span className="text-slate-500">Node ID</span>
                   <span className="font-mono text-white">{accountData?.account_id || accountId}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                   <span className="text-slate-500">Risk Profile</span>
                   <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${accountData?.is_fraudulent ? 'bg-red-400/20 text-red-500 border border-red-500/20' : 'bg-green-400/20 text-green-500 border border-green-500/20'}`}>
                      {accountData?.is_fraudulent ? 'Suspicious Hub' : 'Standard Node'}
                   </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                    <span className="text-slate-500">Transaction History</span>
                    <span className="text-white">{accountData?.history?.length || 0} Traces</span>
                </div>
             </div>
           </div>

           <div className="pt-6 border-t border-[#2d3748]">
              <h3 className="text-xs uppercase font-bold text-[#718096] mb-3 tracking-widest">Pattern Recognition</h3>
              <div className="space-y-2">
                 {accountData?.recent_alerts?.length > 0 ? accountData.recent_alerts.map((alert, i) => (
                    <div key={i} className="p-3 bg-red-400/5 border border-red-400/10 rounded-xl text-xs text-red-100 flex items-center space-x-2">
                       <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                       <span>{alert.pattern || 'Suspicious Outflow'}</span>
                    </div>
                 )) : <div className="text-xs text-slate-600">No network-based patterns detected for this node in current history.</div>}
              </div>
           </div>
        </div>
      </div>
    </div>
  );
}

export default Investigator;
