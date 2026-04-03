const NAV_ITEMS = [
  {
    id: 'dashboard', label: 'Dashboard',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    )
  },
  {
    id: 'transaction', label: 'Analyze',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
    )
  },
  {
    id: 'alerts', label: 'Alerts',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    )
  },
  {
    id: 'trace', label: 'Trace',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    )
  },
  {
    id: 'simulation', label: 'Simulation',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    )
  }
]

export default function Sidebar({ activePage, setActivePage, isOpen, setIsOpen }) {
  return (
    <div className={`${isOpen ? 'w-48' : 'w-14'} transition-all duration-300 ease-in-out
                    bg-panel border-r border-white/5 flex flex-col shrink-0 overflow-hidden`}>

      {/* Logo */}
      <div className="h-14 flex items-center px-4 border-b border-white/5 shrink-0">
        <div className="w-2 h-2 rounded-full bg-accent animate-pulse shrink-0" />
        {isOpen && (
          <span className="ml-3 font-display font-bold text-white text-sm tracking-wider whitespace-nowrap">
            FRAUDSENTINEL
          </span>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 space-y-1 px-2">
        {NAV_ITEMS.map(item => (
          <button
            key={item.id}
            onClick={() => setActivePage(item.id)}
            className={`w-full flex items-center gap-3 px-2 py-2.5 rounded-lg transition-all duration-200 text-left
                        ${activePage === item.id
                          ? 'bg-accent/10 text-accent border border-accent/20'
                          : 'text-slate-400 hover:text-white hover:bg-white/5'}`}>
            <span className="shrink-0">{item.icon}</span>
            {isOpen && (
              <span className="text-sm font-mono whitespace-nowrap">{item.label}</span>
            )}
          </button>
        ))}
      </nav>

      {/* Bottom status */}
      {isOpen && (
        <div className="p-4 border-t border-white/5">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs text-slate-500 font-mono">System Online</span>
          </div>
        </div>
      )}
    </div>
  )
}