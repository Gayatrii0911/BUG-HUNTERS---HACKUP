import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import CyberHero from '../components/CyberHero';

const Home = () => {
  return (
    <div className="min-h-[90vh] flex flex-col items-center justify-center relative overflow-hidden">
      {/* Dynamic Background Glows */}
      <motion.div 
        animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.5, 0.3] }}
        transition={{ duration: 10, repeat: Infinity }}
        className="absolute top-1/4 left-1/4 w-[800px] h-[800px] bg-blue-600/10 rounded-full blur-[180px] pointer-events-none" 
      />
      <motion.div 
        animate={{ scale: [1, 1.3, 1], opacity: [0.2, 0.4, 0.2] }}
        transition={{ duration: 15, repeat: Infinity }}
        className="absolute bottom-1/4 right-1/4 w-[900px] h-[900px] bg-indigo-600/10 rounded-full blur-[220px] pointer-events-none" 
      />
      
      <div className="relative z-10 w-full grid lg:grid-cols-2 gap-24 items-center px-12 max-w-[1800px] mx-auto">
        
        {/* Intelligence Brief Section */}
        <motion.div 
           initial={{ x: -100, opacity: 0 }}
           animate={{ x: 0, opacity: 1 }}
           transition={{ duration: 1 }}
           className="space-y-16"
        >
           <div className="space-y-8">
              <motion.div 
                whileHover={{ scale: 1.05 }}
                className="inline-flex items-center space-x-4 px-8 py-3 bg-white/5 border border-white/10 rounded-full text-[10px] font-black uppercase tracking-[0.5em] text-blue-400 shadow-2xl backdrop-blur-md cursor-pointer"
              >
                  <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse shadow-[0_0_10px_#3b82f6]" />
                  <span>Sentinel Unit Active</span>
              </motion.div>

              <div className="space-y-4">
                 <h1 className="text-[7rem] font-display font-black text-white tracking-tighter leading-[0.85] italic">
                    Neural<br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 via-indigo-400 to-purple-500 drop-shadow-[0_0_30px_rgba(59,130,246,0.3)] pr-4">Forensics</span>
                 </h1>
                 <p className="text-sm text-slate-500 font-bold max-w-xl leading-relaxed uppercase tracking-[0.2em] italic opacity-60">
                    "Cognitive relationship tracking integrated with real-time fund-flow anomalies."
                 </p>
              </div>
           </div>

           <div className="flex items-center space-x-12">
              <Link to="/dashboard" className="group relative">
                 <div className="absolute inset-0 bg-blue-600 blur-2xl opacity-20 group-hover:opacity-40 transition-opacity" />
                 <div className="relative flex items-center space-x-6 px-14 py-8 bg-blue-600 text-white rounded-[2.5rem] font-black text-xs uppercase tracking-[0.3em] transition-all hover:scale-105 hover:shadow-[0_20px_50px_rgba(59,130,246,0.3)] shadow-2xl is-3d">
                    <span>Tactical Center</span>
                    <span className="text-xl rotate-12">→</span>
                 </div>
              </Link>
              
              <div className="flex flex-col space-y-1">
                 <span className="text-[10px] font-black text-white uppercase tracking-widest">v1.2.1 PROD</span>
                 <span className="text-[8px] font-black text-slate-600 uppercase tracking-widest">Build 912-ELITE</span>
              </div>
           </div>

           <div className="grid grid-cols-3 gap-8 pt-12 border-t border-white/5">
              {[
                { label: 'Latency', val: '12ms' },
                { label: 'Uptime', val: '99.9%' },
                { label: 'Nodes', val: '4.2k' }
              ].map((stat, i) => (
                <div key={i} className="space-y-2">
                   <div className="text-[9px] font-black text-slate-600 uppercase tracking-widest">{stat.label}</div>
                   <div className="text-xl font-black text-white font-mono italic">{stat.val}</div>
                </div>
              ))}
           </div>
        </motion.div>

        {/* Cinematic Neural Core */}
        <motion.div 
           initial={{ scale: 0.8, opacity: 0 }}
           animate={{ scale: 1, opacity: 1 }}
           transition={{ duration: 1.5, ease: "easeOut" }}
           className="relative flex justify-center items-center group"
        >
           <div className="absolute inset-0 bg-blue-500/5 rounded-full blur-[200px] pointer-events-none group-hover:bg-blue-500/10 transition-colors" />
           <div className="relative z-10 scale-[1.2]">
              <CyberHero />
           </div>
           
           {/* Floating HUD Elements */}
           <motion.div 
              animate={{ y: [0, -20, 0] }}
              transition={{ duration: 4, repeat: Infinity }}
              className="absolute -top-12 -right-12 p-6 glass-panel neo-glow is-3d"
           >
              <div className="text-[8px] font-black text-blue-400 uppercase tracking-widest mb-2">Neural Pulse</div>
              <div className="flex items-end space-x-2">
                 <div className="text-2xl font-black text-white italic">0.92</div>
                 <div className="text-[8px] text-slate-500 mb-1 font-bold">ALPHA</div>
              </div>
           </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Home;
