import { useState, useEffect } from 'react'
import { fetchAlerts } from '../services/api'

export default function Navbar({ onMenuClick, activePage }) {
  const [alertCount, setAlertCount] = useState(0)
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetchAlerts()
      .then(data => {
        const alerts = Array.isArray(data) ? data : (data.alerts || [])
        setAlertCount(alerts.length)
      })
      .catch(() => {})

    const interval = setInterval(() => {
      fetchAlerts()
        .then(data => {
          const alerts = Array.isArray(data) ? data : (data.alerts || [])
          setAlertCount(alerts.length)
        })
        .catch(() => {})
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const pageNames = {
    dashboard: 'Dashboard',
    transaction: 'Transaction Analysis',
    alerts: 'Alerts',
    trace: 'Account Trace',
    simulation: 'Simulation'
  }

  return (
    <div className="h-14 bg-panel border-b border-white/5 flex items-center px-4 gap-4 shrink-0">
      <button onClick={onMenuClick}
        className="text-slate-400 hover:text-white transition-colors p-1">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <span className="font-display text-white font-semibold text-sm">
        {pageNames[activePage] || 'FraudSentinel'}
      </span>

      <div className="flex-1 max-w-md mx-auto">
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search account or transaction ID..."
          className="w-full bg-base border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white
                     placeholder:text-slate-600 focus:border-accent focus:outline-none transition-colors"
        />
      </div>

      <div className="ml-auto flex items-center gap-3">
        {/* Alert bell */}
        <div className="relative">
          <button className="text-slate-400 hover:text-white transition-colors p-1">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>
          {alertCount > 0 && (
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-xs flex items-center justify-center text-white animate-pulse">
              {alertCount > 9 ? '9+' : alertCount}
            </span>
          )}
        </div>

        {/* Avatar */}
        <div className="w-7 h-7 rounded-full bg-accent/20 border border-accent/40 flex items-center justify-center text-accent text-xs font-bold">
          F
        </div>
      </div>
    </div>
  )
}