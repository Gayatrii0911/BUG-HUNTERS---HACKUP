import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';

const Sidebar = () => {
    const navItems = [
        { name: 'Dashboard', path: '/', icon: '📡' },
        { name: 'Investigator', path: '/investigator', icon: '🔍' },
        { name: 'Simulation Lab', path: '/simulation', icon: '🧪' },
        { name: 'Telemetry', path: '/alerts', icon: '🚨' },
    ];

    return (
        <div className="w-80 bg-[hsl(var(--bg-deep))] h-screen p-6 flex flex-col border-r border-[hsl(var(--border-muted))] relative z-50">
            {/* Branding */}
            <div className="flex items-center space-x-3 mb-10 px-2 group cursor-pointer">
                <div className="w-10 h-10 bg-gradient-to-tr from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(37,99,235,0.3)] group-hover:shadow-[0_0_40px_rgba(37,99,235,0.6)] transition-all duration-500 is-3d">
                    <span className="text-xl font-black text-white italic">X</span>
                </div>
                <div className="flex flex-col">
                    <h1 className="text-2xl font-black font-display text-white tracking-tighter leading-none italic">Sentinel-<span className="text-blue-500">X</span></h1>
                    <span className="text-[8px] text-slate-500 font-black uppercase tracking-[0.4em] mt-1 italic">Forensic Intelligence</span>
                </div>
            </div>

            {/* Profile Brief */}
            <div className="bg-white/[0.03] border border-white/5 rounded-2xl p-4 mb-10 flex items-center space-x-4">
                <div className="w-10 h-10 rounded-full bg-slate-800 overflow-hidden border border-white/10">
                   <img src="https://ui-avatars.com/api/?name=Niko+Satrio&background=random" alt="Avatar" />
                </div>
                <div className="flex-1 overflow-hidden">
                   <div className="text-sm font-bold text-white truncate">Niko Satrio</div>
                   <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest truncate">Lead Product Design</div>
                </div>
                <div className="text-slate-600">⇵</div>
            </div>

            {/* Nav Menu */}
            <nav className="flex-1 space-y-1">
                {navItems.map((item) => (
                    <NavLink 
                        key={item.path} 
                        to={item.path}
                        className={({ isActive }) => `
                            sidebar-item
                            ${isActive 
                                ? 'sidebar-item-active' 
                                : 'text-slate-500 hover:bg-white/[0.03] hover:text-slate-300'}
                        `}
                    >
                        <span className="text-lg opacity-80">{item.icon}</span>
                        <span className="font-medium">{item.name}</span>
                    </NavLink>
                ))}
            </nav>

            {/* Bottom Section */}
            <div className="mt-auto space-y-8">
                <div className="sidebar-item text-slate-500 hover:text-white cursor-pointer">
                    <span className="text-lg">⚙️</span>
                    <span className="font-medium">Settings</span>
                </div>

                <div className="relative overflow-hidden bg-gradient-to-br from-indigo-500/10 to-purple-500/10 rounded-2xl p-6 border border-white/5 group">
                   <div className="text-xs font-bold text-white text-center mb-1">Trial period in 28 days</div>
                   <div className="text-[10px] text-indigo-400 font-black text-center uppercase tracking-widest group-hover:scale-110 transition-transform">Upgrade Plan</div>
                   <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-600 opacity-50" />
                </div>
            </div>
        </div>
    );
};

export default Sidebar;