import { useState, useEffect } from 'react'
import { fetchAlerts } from '../services/api'
import AlertCard from '../components/AlertCard'

export default function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    loadAlerts()
    const interval = setInterval(loadAlerts, 5000)
    return () => clearInterval(interval)
  }, [])

  async function loadAlerts() {
    try {
      const data = await fetchAlerts()
      const list = Array.isArray(data) ? data : (data.alerts || [])
      setAlerts(list)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const filtered = alerts.filter(a => {
    if (filter === 'all') return true
    if (filter === 'high') return (a.risk_level || a.level) === 'high'
    if (filter === 'block') return a.decision === 'BLOCK'
    if (filter === 'mfa') return a.decision === 'MFA'
    return true
  })

  const filters = [
    { id: 'all', label: 'All' },
    { id: 'high', label: 'High Risk' },
    { id: 'block', label: 'Blocked' },
    { id: 'mfa', label: 'MFA' }
  ]

  return (
    <div className="space-y-6 fade-in-up">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-bold text-white">Alerts</h1>
          <p className="text-slate-500 text-sm mt-1">{alerts.length} total alerts detected</p>
        </div>
        <button onClick={loadAlerts}
          className="text-xs text-accent border border-accent/30 px-3 py-1.5 rounded-lg hover:bg-accent/10 transition-colors font-mono">
          ↻ Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        {filters.map(f => (
          <button key={f.id} onClick={() => setFilter(f.id)}
            className={`text-xs px-3 py-1.5 rounded-lg font-mono transition-colors
                        ${filter === f.id
                          ? 'bg-accent/10 text-accent border border-accent/30'
                          : 'text-slate-400 border border-white/10 hover:text-white'}`}>
            {f.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-slate-500 text-sm font-mono">Loading...</div>
      ) : filtered.length === 0 ? (
        <div className="bg-panel border border-white/5 rounded-xl p-8 text-center">
          <div className="text-slate-500 text-sm font-mono">No alerts match this filter</div>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {filtered.slice().reverse().map((alert, i) => (
            <AlertCard key={i} alert={alert} />
          ))}
        </div>
      )}
    </div>
  )
}