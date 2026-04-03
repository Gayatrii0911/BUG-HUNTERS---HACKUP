import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, 
  ShieldAlert, 
  Search, 
  Zap, 
  Cpu, 
  Terminal,
  Activity,
  Menu,
  ChevronRight
} from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Alerts from './pages/Alerts';
import Investigator from './pages/Investigator';
import Simulation from './pages/Simulation';
import './styles/index.css';

// StatusBadge must be defined BEFORE Sidebar to avoid ReferenceError
const StatusBadge = ({ label, status, color }) => (
  <div className="flex items-center justify-between">
    <span className="text-[9px] font-black text-slate-600 uppercase tracking-tighter">{label}</span>
    <div className="flex items-center space-x-2">
       <span className="text-[9px] font-bold text-slate-500 uppercase">{status}</span>
       <div className={`w-1.5 h-1.5 rounded-full ${color} animate-pulse`} />
    </div>
  </div>
);

const Sidebar = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Command Center', icon: <LayoutDashboard size={18} />, color: 'group-hover:text-cyber-accent' },
    { path: '/alerts', label: 'Security Alerts', icon: <ShieldAlert size={18} />, color: 'group-hover:text-cyber-danger' },
    { path: '/investigator', label: 'Node Tracing', icon: <Search size={18} />, color: 'group-hover:text-cyber-accent' },
    { path: '/simulation', label: 'Matrix Simulator', icon: <Zap size={18} />, color: 'group-hover:text-cyber-warning' },
  ];

  return (
    <nav className="w-64 bg-cyber-bg border-r border-cyber-border flex flex-col p-6 space-y-8 z-50">
      {/* Brand */}
      <div className="flex items-center space-x-3 group cursor-pointer">
        <div className="w-10 h-10 bg-cyber-accent rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(0,245,255,0.4)] group-hover:scale-110 transition-transform">
          <Cpu className="text-cyber-bg w-6 h-6" />
        </div>
        <div>
          <h1 className="text-xl font-black font-display text-white tracking-tighter leading-none italic">AEGIS</h1>
          <span className="text-[10px] font-mono font-bold text-cyber-accent uppercase tracking-[0.2em]">Matrix v1.2</span>
        </div>
      </div>

      {/* Nav Links */}
      <div className="flex flex-col space-y-2 flex-1">
        <div className="text-[10px] uppercase font-black text-slate-600 tracking-widest mb-4 px-2">Navigation Console</div>
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link 
              key={item.path}
              to={item.path} 
              className={`group flex items-center justify-between px-4 py-3 rounded-xl transition-all relative overflow-hidden
                         ${isActive ? 'bg-white/5 text-white' : 'text-slate-500 hover:text-white'}`}
            >
              <div className="flex items-center space-x-3 z-10">
                <div className={`transition-colors duration-300 ${isActive ? 'text-cyber-accent' : item.color}`}>
                  {item.icon}
                </div>
                <span className="text-xs font-bold uppercase tracking-tight">{item.label}</span>
              </div>
              {isActive && (
                <motion.div 
                  layoutId="active-nav"
                  className="absolute left-0 w-1 h-6 bg-cyber-accent rounded-r-full"
                />
              )}
              <ChevronRight size={14} className={`opacity-0 group-hover:opacity-100 transition-all ${isActive ? 'translate-x-0 opacity-100 text-cyber-accent' : 'translate-x-[-10px]'}`} />
            </Link>
          );
        })}
      </div>

      {/* System Status Container */}
      <div className="pt-6 border-t border-cyber-border space-y-4">
        <div className="flex flex-col space-y-2 px-2">
           <StatusBadge label="Uplink" status="Stable" color="bg-cyber-success" />
           <StatusBadge label="Neural" status="Syncing" color="bg-cyber-accent" />
           <StatusBadge label="Matrix" status="Active" color="bg-cyber-warning" />
        </div>
        <div className="flex items-center space-x-2 text-[9px] font-mono text-slate-700 bg-black/30 p-3 rounded-lg border border-white/5">
           <Terminal size={10} />
           <span>KERN: OK | PID: 1042</span>
        </div>
      </div>
    </nav>
  );
};

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-cyber-bg text-slate-400 font-sans overflow-hidden">
        
        <Sidebar />

        {/* Main Content Area */}
        <main className="flex-1 flex flex-col min-w-0 bg-[#080a12] relative">
          
          {/* Header */}
          <header className="h-20 border-b border-cyber-border flex items-center px-10 justify-between z-40 bg-[#080a12]/80 backdrop-blur-md">
            <div className="flex items-center space-x-4">
                <Menu size={20} className="lg:hidden text-slate-500" />
                <div className="flex flex-col">
                  <h2 className="text-sm font-black text-white uppercase tracking-widest font-display">Command HUD</h2>
                  <div className="text-[9px] text-slate-600 font-mono flex items-center space-x-1 uppercase">
                     <span className="text-cyber-accent font-bold">SYSLOG:</span>
                     <span>Processing anomaly fingerprints...</span>
                  </div>
                </div>
            </div>

            <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-3 px-4 py-2 bg-cyber-panel border border-cyber-border rounded-xl">
                   <Activity size={14} className="text-cyber-accent animate-pulse" />
                   <span className="text-[10px] font-black text-white uppercase tracking-widest">Neural Sync: 98%</span>
                </div>
                <div className="w-10 h-10 rounded-full bg-cyber-purple/10 border border-cyber-purple/20 flex items-center justify-center text-cyber-purple shadow-[0_0_10px_rgba(188,19,254,0.2)]">
                   <ShieldAlert size={18} />
                </div>
            </div>
          </header>

          {/* Sub-Header / Breadcrumbs (Cyber Style) */}
          <div className="px-10 py-4 bg-white/5 border-b border-white/5 flex items-center justify-between">
             <div className="flex items-center space-x-2 text-[9px] font-black uppercase text-slate-500 tracking-[0.2em]">
                <span className="hover:text-cyber-accent cursor-pointer transition-colors">ROOT</span>
                <ChevronRight size={10} />
                <span className="text-white hover:text-cyber-accent cursor-pointer transition-colors">MATRIX</span>
                <ChevronRight size={10} />
                <span className="text-cyber-accent">LIVE_FEED</span>
             </div>
             <div className="font-mono text-[9px] text-slate-700">
                LTC: {new Date().toISOString().slice(11, 19)} UTC
             </div>
          </div>

          <div className="p-10 flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/investigator" element={<Investigator />} />
              <Route path="/simulation" element={<Simulation />} />
            </Routes>
          </div>
          
          {/* Global UI Decoration (Brutalist Lines) */}
          <div className="absolute top-0 right-0 w-px h-full bg-gradient-to-b from-transparent via-cyber-border to-transparent opacity-30" />
          <div className="absolute left-0 bottom-0 w-full h-px bg-gradient-to-r from-transparent via-cyber-border to-transparent opacity-30" />
        </main>
      </div>
    </Router>
  );
}

export default App;