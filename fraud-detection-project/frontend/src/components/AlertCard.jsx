const LEVEL_CONFIG = {
  high:   { color: 'text-red-400',    bg: 'bg-red-400/10 border-red-400/20',    dot: 'bg-red-400' },
  medium: { color: 'text-orange-400', bg: 'bg-orange-400/10 border-orange-400/20', dot: 'bg-orange-400' },
  low:    { color: 'text-green-400',  bg: 'bg-green-400/10 border-green-400/20',  dot: 'bg-green-400' }
}

export default function AlertCard({ alert }) {
  const level = alert.risk_level || alert.level || 'low'
  const config = LEVEL_CONFIG[level] || LEVEL_CONFIG.low

  const reasons = alert.reasons || alert.flags || []
  const score = alert.risk_score ?? alert.score ?? '—'
  const decision = alert.decision || '—'
  const timestamp = alert.timestamp || alert.created_at || ''
  const account = alert.sender_id || alert.from_account || alert.account || '—'

  return (
    <div className={`border rounded-xl p-4 space-y-3 transition-all duration-200 hover:scale-[1.01] ${config.bg}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${config.dot} animate-pulse`} />
          <span className={`text-xs font-mono uppercase tracking-wider ${config.color}`}>{level} risk</span>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-lg font-display font-black ${config.color}`}>{score}</span>
          <span className={`text-xs px-2 py-0.5 rounded-full border ${config.bg} ${config.color}`}>
            {decision}
          </span>
        </div>
      </div>

      <div className="text-xs text-slate-400 font-mono">
        Account: <span className="text-white">{account}</span>
      </div>

      {reasons.length > 0 && (
        <div className="space-y-1">
          {reasons.slice(0, 3).map((r, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-slate-300">
              <span className={`${config.color} mt-0.5`}>›</span>
              {r}
            </div>
          ))}
        </div>
      )}

      {timestamp && (
        <div className="text-xs text-slate-600 font-mono border-t border-white/5 pt-2">
          {new Date(timestamp).toLocaleString()}
        </div>
      )}
    </div>
  )
}