const SimulationCard = ({ scenario, onRun, running }) => {
  const isRunning = running === scenario.id;

  return (
    <div className="perspective h-full">
      <div className={`bg-[#1a1c2e] border border-[#2d3748] rounded-2xl p-6 shadow-xl relative overflow-hidden group hover:border-[#3182ce]/50 transition-all flex flex-col h-full is-3d ${isRunning ? 'ring-2 ring-blue-500/50' : ''}`}>
        <div className="absolute top-0 right-0 w-16 h-16 bg-[#3182ce]/5 rounded-bl-full group-hover:bg-[#3182ce]/10 transition-colors" />
      
        <div className="relative z-10 space-y-4 flex-1">
          <div className="flex justify-between items-start">
             <h3 className="font-bold text-white group-hover:text-[#3182ce] transition-colors">{scenario.name}</h3>
             <div className={`p-1.5 rounded-lg bg-[#0f111a] border border-[#2d3748] text-[10px] ${isRunning ? 'text-blue-400 animate-pulse' : 'text-slate-600'}`}>
                {isRunning ? '•••' : 'IDLE'}
             </div>
          </div>
          <p className="text-[10px] text-slate-500 leading-relaxed italic border-l border-[#3182ce]/30 pl-3">
            {scenario.desc}
          </p>
        </div>

        <div className="mt-6 relative z-10">
          <button 
            disabled={running !== null}
            onClick={() => onRun(scenario.id)}
            className={`w-full text-[10px] font-black uppercase tracking-widest px-4 py-3 rounded-xl transition-all border
              ${isRunning 
                ? 'bg-blue-500 text-white border-blue-400 animate-pulse' 
                : 'bg-[#2d3748]/50 text-slate-300 border-[#2d3748] hover:bg-[#3182ce] hover:text-white hover:border-[#3182ce] hover:shadow-lg hover:shadow-[#3182ce]/20'
              }`}
          >
            {isRunning ? 'Processing Intelligence...' : 'Execute Replay'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SimulationCard;
