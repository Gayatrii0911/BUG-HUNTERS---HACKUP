import { useState } from 'react'
import { fetchTrace } from '../services/api'

export default function Trace() {
  const [account, setAccount] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleTrace(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await fetchTrace(account)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 fade-in-up">
      <div>
        <h1 className="font-display text-2xl font-bold text-white">Account Trace</h1>
        <p className="text-slate-500 text-sm mt-1">Trace transaction flow for any account</p>
      </div>

      <form onSubmit={handleTrace} className="flex gap-3">
        <input
          value={account}
          onChange={e => setAccount(e.target.value)}
          placeholder="Enter account ID (e.g. A101)"
          className="flex-1 bg-panel border border-white/10 rounded-lg px-4 py-2.5 text-sm text-white
                     placeholder:text-slate-600 focus:border-accent focus:outline-none transition-colors"
        />
        <button type="submit" disabled={loading}
          className="bg-accent hover:bg-cyan-400 text-black font-bold px-6 py-2.5 rounded-lg
                     transition-all duration-200 hover:scale-105 active:scale-95 text-sm uppercase font-mono">
          {loading ? 'Tracing...' : 'Trace'}
        </button>
      </form>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-sm">
          ⚠ {error}
        </div>
      )}

      {result && (
        <div className="bg-panel border border-white/5 rounded-xl p-6 space-y-4 slide-in-right">
          <h2 className="font-display text-white font-semibold">Trace Result</h2>
          <pre className="text-xs text-slate-300 bg-black/20 rounded-lg p-4 overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}