import { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

const GraphView = ({ graphData, loading }) => {
    const containerRef = useRef(null);
    const cyRef = useRef(null);
    
    // Normalize data: Backend returns { nodes: [{ data: { id, label, ...} }], edges: [...] }
    const actualData = graphData?.graph_payload || graphData;

    useEffect(() => {
        if (!containerRef.current || !actualData) return;

        // Cytoscape expects elements in a specific format. 
        // Our backend already provides them in [ { data: {...} } ] format.
        const elements = [
            ...(actualData.nodes || []).map(n => n.data ? n : { data: n }),
            ...(actualData.edges || []).map(e => e.data ? e : { data: e })
        ];

        cyRef.current = cytoscape({
            container: containerRef.current,
            elements: elements,
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#0C1021',
                        'label': 'data(id)',
                        'color': '#cbd5e0',
                        'font-size': '10px',
                        'width': '50px',
                        'height': '50px',
                        'text-valign': 'bottom',
                        'text-margin-y': 8,
                        'font-weight': 'bold',
                        'border-width': 2,
                        'border-color': '#6366f1', // Indigo
                        'box-shadow': '0 0 15px #6366f1',
                        'transition-property': 'background-color, border-color, width, height',
                        'transition-duration': '0.5s'
                    }
                },
                {
                    selector: 'node[?is_fraudulent]',
                    style: {
                        'background-color': '#450a0a',
                        'border-color': '#ef4444',
                        'color': '#ef4444',
                        'width': '60px',
                        'height': '60px',
                        'border-width': 4,
                        'box-shadow': '0 0 30px #ef4444'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 2,
                        'line-color': '#312e81', // Deep Indigo
                        'target-arrow-color': '#312e81',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        'label': 'data(amount)',
                        'font-size': '8px',
                        'color': '#6366f1',
                        'text-rotation': 'autorotate',
                        'text-margin-y': -10,
                        'line-style': 'dashed',
                        'arrow-scale': 1.2
                    }
                },
                {
                    selector: 'edge[?is_fraudulent]',
                    style: {
                        'line-color': '#ef4444',
                        'target-arrow-color': '#ef4444',
                        'width': 4,
                        'line-style': 'solid',
                        'opacity': 0.8
                    }
                }
            ],
            layout: { 
                name: 'cose', 
                animate: true,
                padding: 50,
                componentSpacing: 100,
                nodeRepulsion: 4000,
                edgeElasticity: 100,
                nestingFactor: 5
            }
        });

        // Nodal Interaction: Click to investigate
        cyRef.current.on('tap', 'node', (evt) => {
            const nodeId = evt.target.id();
            if (onNodeClick) onNodeClick(nodeId);
        });

        // Edge Flow Animation
        let offset = 0;
        const animateEdges = () => {
             offset -= 0.5;
             if (cyRef.current) {
                 cyRef.current.edges().style('line-dash-offset', offset);
                 requestAnimationFrame(animateEdges);
             }
        };
        requestAnimationFrame(animateEdges);

        return () => {
            if (cyRef.current) cyRef.current.destroy();
        };
    }, [actualData]);

    return (
        <div className="bg-[hsl(var(--bg-deep))] rounded-2xl border border-white/5 h-full overflow-hidden relative group">
            {loading && (
                <div className="absolute inset-0 bg-black/60 backdrop-blur-2xl flex items-center justify-center z-20">
                    <div className="flex flex-col items-center space-y-6">
                        <div className="w-16 h-16 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin shadow-[0_0_20px_rgba(99,102,241,0.2)]" />
                        <span className="text-indigo-400 font-black tracking-[0.4em] text-[11px] uppercase italic animate-pulse">Deciphering Nodal Fabric...</span>
                    </div>
                </div>
            )}
            <div ref={containerRef} className="w-full h-full" />
            
            {(!loading && (!actualData || (!actualData.nodes?.length && !actualData.edges?.length))) && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <div className="text-center space-y-4 opacity-20">
                        <div className="text-6xl">🧬</div>
                        <div className="text-[12px] font-black uppercase tracking-[0.5em] text-slate-500 italic">Neural Ingress Awaiting Signal</div>
                    </div>
                </div>
            )}
            
            {/* Visual Legend */}
            <div className="absolute bottom-8 left-8 p-6 bg-black/40 backdrop-blur-2xl border border-white/5 rounded-2xl space-y-3 shadow-2xl">
                <div className="flex items-center space-x-4">
                    <div className="w-3 h-3 rounded-full bg-indigo-500 shadow-[0_0_10px_#6366f1]" />
                    <span className="text-slate-300 font-bold text-[10px] uppercase tracking-widest italic leading-none">Verified Identity Node</span>
                </div>
                <div className="flex items-center space-x-4">
                    <div className="w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_#ef4444] animate-pulse" />
                    <span className="text-red-500 font-black text-[10px] uppercase tracking-widest italic leading-none">Suspicious Neural Cluster</span>
                </div>
                <div className="pt-2 border-t border-white/5">
                   <div className="flex items-center space-x-4">
                      <div className="w-6 h-0.5 bg-indigo-900 border-t border-dashed border-indigo-500" />
                      <span className="text-slate-500 font-bold text-[9px] uppercase tracking-widest italic leading-none">Routine Nodal Flow</span>
                   </div>
                </div>
            </div>

            <div className="hologram-overlay opacity-5 group-hover:opacity-10 transition-opacity" />
        </div>
    );
};

export default GraphView;
