const CONFIG = {
  APPROVE: { color: 'text-green-400', bg: 'bg-green-400/10 border-green-400/30', label: '✓ APPROVE' },
  MFA:     { color: 'text-orange-400', bg: 'bg-orange-400/10 border-orange-400/30', label: '⚠ MFA' },
  BLOCK:   { color: 'text-red-400', bg: 'bg-red-400/10 border-red-400/30', label: '✕ BLOCK' }
}

export default function DecisionBadge({ decision }) {
  const config = CONFIG[decision] || CONFIG.APPROVE
  return (
    <span className={`text-xs px-2 py-1 rounded-full border font-mono uppercase tracking-wider ${config.bg} ${config.color}`}>
      {config.label}
    </span>
  )
}