export default function RiskBreakdown({ result }) {
  if (!result) return null
  const score = result.risk_score ?? result.score ?? 0
  const level = result.risk_level ?? result.level ?? 'low'
  const reasons = result.reasons || result.flags || []

  const barColor = level === 'high' ? 'bg-red-400' : level === 'medium' ? 'bg-orange-400' : 'bg-green-400'
  const textColor = level === 'high' ? 'text-red-400' : level === 'medium' ? 'text-orange-400' : 'text-green-400'

  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <span className="text-xs text-slate-400 uppercase tracking-wider">Risk Score</span>
        <span className={`text-2xl font-display font-black ${textColor}`}>{score}</span>
      </div>
      <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all duration-700 ${barColor}`}
          style={{ width: `${score}%` }} />
      </div>
      {reasons.length > 0 && (
        <div className="space-y-1 pt-1">
          {reasons.map((r, i) => (
            <div key={i} className={`flex items-start gap-2 text-xs text-slate-300`}>
              <span className={`${textColor} mt-0.5`}>›</span>{r}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}