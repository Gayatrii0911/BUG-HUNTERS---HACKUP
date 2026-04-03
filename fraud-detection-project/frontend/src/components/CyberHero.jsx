const CyberHero = () => {
    return (
        <div className="relative w-full h-[600px] perspective flex items-center justify-center group">
            {/* The 3D Elements */}
            <div className="relative w-[500px] h-[350px] is-3d shadow-[0_0_100px_rgba(49,130,206,0.1)] rounded-[40px] overflow-hidden border border-white/5 hologram scanline">
               
               {/* Content Inside the 3D Hologram */}
               <div className="absolute inset-0 p-8 flex flex-col justify-between">
                  <div className="flex justify-between items-start">
                     <div className="space-y-1">
                        <div className="text-[10px] font-black text-[#3182ce] tracking-[0.3em] uppercase">Security Level 9</div>
                        <div className="text-xl font-display font-black text-white italic">CYBER SENTINEL</div>
                     </div>
                     <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-xl">
                        🛡️
                     </div>
                  </div>

                  <div className="space-y-4">
                     <div className="h-16 w-full bg-gradient-to-r from-[#3182ce]/10 to-transparent rounded-xl border-l-2 border-[#3182ce] p-3 flex flex-col justify-center">
                        <span className="text-[8px] font-bold text-slate-500 uppercase tracking-widest">Active Neural Patterns</span>
                        <div className="flex space-x-1 mt-1">
                           {[...Array(20)].map((_, i) => (
                              <div key={i} className="flex-1 bg-blue-400 h-2 rounded-full opacity-40 animate-pulse" style={{ animationDelay: `${i * 0.1}s`, height: `${Math.random() * 10 + 2}px` }} />
                           ))}
                        </div>
                     </div>
                     <div className="grid grid-cols-2 gap-4">
                        <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                           <div className="text-[8px] text-slate-500 font-bold uppercase mb-1">Graph Nodes</div>
                           <div className="text-xl font-black text-white">42,891</div>
                        </div>
                        <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                           <div className="text-[8px] text-slate-500 font-bold uppercase mb-1">Threat Score</div>
                           <div className="text-xl font-black text-red-500 tracking-tighter">0.02%</div>
                        </div>
                     </div>
                  </div>
               </div>

               {/* Grid Overlay */}
               <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-30 pointer-events-none" />
               <div className="absolute inset-0 bg-gradient-to-br from-transparent via-[#3182ce]/5 to-transparent pointer-events-none" />
            </div>

            {/* Orbiting Elements */}
            <div className="absolute w-[650px] h-[650px] border border-white/5 rounded-full animate-[spin_20s_linear_infinite] opacity-20 pointer-events-none" />
            <div className="absolute w-[450px] h-[450px] border border-white/5 rounded-full animate-[spin_15s_linear_reverse_infinite] opacity-10 pointer-events-none" />
        </div>
    );
};

export default CyberHero;
