import { motion } from 'framer-motion';

const Navbar = () => {
    return (
        <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="h-20 px-12 border-b border-white/5 flex items-center justify-between sticky top-0 bg-[hsl(var(--bg-deep))] z-40 backdrop-blur-2xl"
        >
            <div className="flex items-center space-x-8">
                <div className="flex space-x-8 text-[11px] font-bold text-slate-500 uppercase tracking-widest cursor-pointer">
                    <span className="text-white">Executive</span>
                    <span className="hover:text-slate-300">Taxonomy</span>
                    <span className="hover:text-slate-300">Vulnerabilities</span>
                    <span className="hover:text-slate-300">Compliance</span>
                </div>
            </div>

            <div className="flex items-center space-x-10 text-slate-500">
                <div className="flex items-center space-x-3 px-4 py-2 bg-white/[0.03] border border-white/5 rounded-xl text-xs font-medium cursor-pointer hover:bg-white/[0.05] transition-colors">
                    🔍 <span className="opacity-60">Search for nodes, assets...</span>
                    <span className="px-1.5 py-0.5 bg-black/40 border border-white/10 rounded text-[9px] font-mono opacity-40 ml-2">⌘K</span>
                </div>
                <div className="flex items-center space-x-6 text-sm">
                    <span className="cursor-pointer hover:text-white transition-colors">⚙️ Settings</span>
                    <div className="w-8 h-8 rounded-full border border-white/10 bg-slate-800" />
                </div>
            </div>
        </motion.div>
    );
};

export default Navbar;