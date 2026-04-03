import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';

const Sidebar = () => {
    const navItems = [
        { name: 'Dashboard', path: '/', icon: '📊' },
        { name: 'Discovery', path: '/discovery', icon: '🔍' },
        { name: 'API Security', path: '/dashboard', icon: '🛡️' },
        { name: 'Cloud Infra', path: '/cloud', icon: '☁️' },
        { name: 'Inventory', path: '/behavior', icon: '🧬' },
        { name: 'Attack Paths', path: '/investigator', icon: '🏹' },
        { name: 'Vulnerability', path: '/alerts', icon: '⚠️' },
        { name: 'Compliance', path: '/compliance', icon: '📝' },
    ];

    return (
        <div className="w-80 bg-[hsl(var(--bg-deep))] h-screen p-6 flex flex-col border-r border-[hsl(var(--border-muted))] relative z-50">
            {/* Branding */}
            <div className="flex items-center space-x-3 mb-10 px-2">
                <div className="w-8 h-8 bg-gradient-to-tr from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg">
                    <span className="text-sm font-bold text-white italic">O</span>
                </div>
                <h1 className="text-xl font-bold font-display text-white tracking-tight">Orca</h1>
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