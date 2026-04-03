const BASE_URL = 'http://127.0.0.1:8000'

export async function submitTransaction(data) {
  const response = await fetch(`${BASE_URL}/transaction`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  if (!response.ok) {
    const err = await response.json()
    throw new Error(err.detail || 'Transaction failed')
  }
  return response.json()
}

export async function fetchAlerts() {
  const response = await fetch(`${BASE_URL}/alerts`)
  if (!response.ok) throw new Error('Failed to fetch alerts')
  return response.json()
}

export async function fetchTrace(account) {
  const response = await fetch(`${BASE_URL}/trace/${account}`)
  if (!response.ok) throw new Error('Failed to fetch trace')
  return response.json()
}

export async function fetchHealth() {
  const response = await fetch(`${BASE_URL}/health`)
  return response.json()
}