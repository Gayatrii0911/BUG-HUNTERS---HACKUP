import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Alerts from './pages/Alerts'
import Trace from './pages/Trace'
import Simulation from './pages/Simulation'
import TransactionForm from './components/TransactionForm'

export default function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const pages = {
    dashboard: <Dashboard />,
    transaction: <TransactionForm />,
    alerts: <Alerts />,
    trace: <Trace />,
    simulation: <Simulation />
  }

  return (
    <div className="flex h-screen bg-base overflow-hidden">
      <Sidebar activePage={activePage} setActivePage={setActivePage} isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Navbar onMenuClick={() => setSidebarOpen(o => !o)} activePage={activePage} />
        <main className="flex-1 overflow-y-auto p-6">
          {pages[activePage]}
        </main>
      </div>
    </div>
  )
}