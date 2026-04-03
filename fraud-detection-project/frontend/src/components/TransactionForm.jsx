import { useState } from 'react'
import { submitTransaction } from '../services/api'

const INITIAL = {
  user_id: '',
  from_account: '',
  to_account: '',
  amount: '',
  timestamp: new Date().toISOString().slice(0, 16),
  device_id: '',
  channel: 'mobile',
  location: ''
}

const DECISION_CONFIG = {
  APPROVE: { color: 'text-green-400', bg: 'bg-green-400/10 border-green-400/30', glow: 'glow-green', label: '✓ APPROVED' },
  MFA:     { color: 'text-orange-400', bg: 'bg-orange-400/10 border-orange-400/30', glow: 'glow-orange', label: '⚠ MFA REQUIRED' },
  BLOCK:   { color: 'text-red-400', bg: 'bg-red-400/10 border-red-400/30', glow: 'glow-red', label: '✕ BLOCKED' }
}

export default function TransactionForm() {
  const [form, setForm] = useState(INITIAL)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  function handleChange(e) {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const payload = {
        ...form,
        amount: parseFloat(form.amount),
        timestamp: new Date(form.timestamp).toISOString()
      }
      const data = await submitTransaction(payload)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const decision = result ? DECISION_CONFIG[result.decision] : null

  return (
    <div className="min-h-screen bg-base flex items-center justify-center p-6">
      <div className="w-full max-w-2xl space-y-6">

        {/* Header */}
        <div className="fade-in-up">
          <div className="flex items-center gap-3 mb-1">
            <div className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            <span className="text-accent text-xs font-mono tracking-widest uppercase">FraudSentinel</span>
          </div>
          <h1 className="font-display text-3xl font-bold text-white">
            Transaction Analysis
          </h1>
          <p className="text-slate-500 text-sm mt-1">Submit a transaction for real-time fraud evaluation</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit}
          className="bg-panel border border-white/5 rounded-2xl p-6 space-y-4 fade-in-up"
          style={{ animationDelay: '0.1s' }}>

          <div className="grid grid-cols-2 gap-4">
            <Field label="User ID" name="user_id" value={form.user_id} onChange={handleChange} placeholder="U101" />
            <Field label="Amount (₹)" name="amount" value={form.amount} onChange={handleChange} placeholder="5000" type="number" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Field label="From Account" name="from_account" value={form.from_account} onChange={handleChange} placeholder="A101" />
            <Field label="To Account" name="to_account" value={form.to_account} onChange={handleChange} placeholder="B202" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Field label="Device ID" name="device_id" value={form.device_id} onChange={handleChange} placeholder="D01" />
            <Field label="Location" name="location" value={form.location} onChange={handleChange} placeholder="Mumbai" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-400 uppercase tracking-wider mb-1 block">Channel</label>
              <select name="channel" value={form.channel} onChange={handleChange}
                className="w-full bg-base border border-white/10 rounded-lg px-3 py-2.5 text-sm text-white focus:border-accent focus:outline-none transition-colors">
                <option value="mobile">Mobile</option>
                <option value="web">Web</option>
                <option value="api">API</option>
                <option value="atm">ATM</option>
              </select>
            </div>
            <Field label="Timestamp" name="timestamp" value={form.timestamp} onChange={handleChange} type="datetime-local" />
          </div>

          <button type="submit" disabled={loading}
            className="w-full mt-2 bg-accent hover:bg-cyan-400 text-black font-display font-bold py-3 rounded-xl
                       transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed
                       tracking-wide text-sm uppercase glow-cyan">
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                Analyzing...
              </span>
            ) : 'Analyze Transaction'}
          </button>
        </form>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-sm fade-in-up">
            ⚠ {error}
          </div>
        )}

        {/* Result */}
        {result && decision && (
          <div className={`border rounded-2xl p-6 space-y-4 slide-in-right ${decision.bg} ${decision.glow}`}>

            {/* Decision badge */}
            <div className="flex items-center justify-between">
              <span className={`font-display text-2xl font-bold ${decision.color}`}>
                {decision.label}
              </span>
              <div className="text-right">
                <div className={`text-4xl font-display font-black ${decision.color}`}>
                  {result.risk_score}
                </div>
                <div className="text-xs text-slate-400 uppercase tracking-wider">Risk Score</div>
              </div>
            </div>

            {/* Risk level bar */}
            <div>
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Risk Level</span>
                <span className="uppercase">{result.risk_level}</span>
              </div>
              <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    result.risk_level === 'high' ? 'bg-red-400' :
                    result.risk_level === 'medium' ? 'bg-orange-400' : 'bg-green-400'
                  }`}
                  style={{ width: `${result.risk_score}%` }}
                />
              </div>
            </div>

            {/* Reasons */}
            <div>
              <div className="text-xs text-slate-400 uppercase tracking-wider mb-2">Detection Signals</div>
              <div className="space-y-1.5">
                {result.reasons.map((r, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className={`mt-0.5 ${decision.color}`}>›</span>
                    {r}
                  </div>
                ))}
              </div>
            </div>

            {/* Alert flag */}
            {result.alert && (
              <div className="flex items-center gap-2 text-xs text-red-400 border-t border-white/5 pt-3">
                <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse" />
                Alert generated — flagged for investigation
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function Field({ label, name, value, onChange, placeholder, type = 'text' }) {
  return (
    <div>
      <label className="text-xs text-slate-400 uppercase tracking-wider mb-1 block">{label}</label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required
        className="w-full bg-base border border-white/10 rounded-lg px-3 py-2.5 text-sm text-white
                   placeholder:text-slate-600 focus:border-accent focus:outline-none transition-colors"
      />
    </div>
  )
}