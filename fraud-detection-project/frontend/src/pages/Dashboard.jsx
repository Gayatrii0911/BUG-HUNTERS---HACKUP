import { useState, useEffect } from 'react'
import { fetchAlerts } from '../services/api'
import AlertCard from '../components/AlertCard'
import DecisionBadge from '../components/DecisionBadge'

export default function Dashboard() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({ total: 0, high: 0, blocked: 0, mfa: 0 })

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
      setStats({
        total: list.length,
        high: list.filter(a => (a.risk_level || a.level) === 'high').length,
        blocked: list.filter(a => a.decision === 'BLOCK').length,
        mfa: list.filter(a => a.decision === 'MFA').length
      })
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    { label: 'Total Alerts', value: stats.total, color: 'text-accent', border: 'border-accent/20' },
    { label: 'High Risk', value: stats.high, color: 'text-red-400', border: 'border-red-400/20' },
    { label: 'Blocked', value: stats.blocked, color: 'text-red-400', border: 'border-red-400/20' },
    { label: 'MFA Triggered', value: stats.mfa, color: 'text-orange-400', border: 'border-orange-400/20' }
  ]

  return (
    <div className="space-y-6 fade-in-up">

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        {statCards.map((s, i) => (
          <div key={i} className={`bg-panel border ${s.border} rounded-xl p-4`}>
            <div className="text-xs text-slate-400 uppercase tracking-wider mb-1">{s.label}</div>
            <div className={`text-3xl font-display font-black ${s.color}`}>{s.value}</div>
          </div>
        ))}
      </div>

      {/* Recent alerts */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-display text-white font-semibold">Recent Suspicious Activity</h2>
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs text-slate-500 font-mono">Live</span>
          </div>
        </div>

        {loading ? (
          <div className="text-slate-500 text-sm font-mono">Loading alerts...</div>
        ) : alerts.length === 0 ? (
          <div className="bg-panel border border-white/5 rounded-xl p-8 text-center">
            <div className="text-slate-500 text-sm font-mono">No alerts yet</div>
            <div className="text-slate-600 text-xs mt-1">Submit suspicious transactions to generate alerts</div>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {alerts.slice().reverse().map((alert, i) => (
              <AlertCard key={i} alert={alert} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}