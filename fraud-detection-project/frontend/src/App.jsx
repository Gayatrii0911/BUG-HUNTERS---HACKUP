import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Alerts from './pages/Alerts';
import Investigator from './pages/Investigator';
import Simulation from './pages/Simulation';
import './styles/index.css';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-[#0f111a] text-[#a0aec0]">
        
        {/* Sidebar */}
        <nav className="w-64 bg-[#1a1c2e] border-r border-[#2d3748] flex flex-col p-6 space-y-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-[#3182ce] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">FG</span>
            </div>
            <h1 className="text-xl font-bold text-white tracking-tight">FraudGuard</h1>
          </div>

          <div className="flex flex-col space-y-2">
            <Link to="/" className="flex items-center space-x-3 px-4 py-3 rounded-xl transition-all hover:bg-[#2d3748] hover:text-white">
              <span>Overview</span>
            </Link>
            <Link to="/alerts" className="flex items-center space-x-3 px-4 py-3 rounded-xl transition-all hover:bg-[#2d3748] hover:text-white">
              <span>Alerts</span>
            </Link>
            <Link to="/investigator" className="flex items-center space-x-3 px-4 py-3 rounded-xl transition-all hover:bg-[#2d3748] hover:text-white">
              <span>Investigator</span>
            </Link>
            <Link to="/simulation" className="flex items-center space-x-3 px-4 py-3 rounded-xl transition-all hover:bg-[#2d3748] hover:text-white">
              <span>Simulation</span>
            </Link>
          </div>

          <div className="mt-auto pt-6 border-t border-[#2d3748]">
            <div className="flex items-center space-x-2 text-xs font-mono text-[#718096]">
              <div className="w-2 h-2 rounded-full bg-green-400"></div>
              <span>Backend Online: v1.2.1</span>
            </div>
          </div>
        </nav>

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto bg-[#0f111a]">
          <header className="h-16 border-b border-[#2d3748] flex items-center px-8 bg-[#1a1c2e] justify-between">
            <div className="text-sm font-medium">Dashboard / {location.pathname}</div>
            <div className="flex items-center space-x-4">
                <span className="text-xs font-semibold px-3 py-1 rounded-full bg-[#2d3748] text-[#3182ce]">Member 1 & 2 Integrated</span>
            </div>
          </header>

          <div className="p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/investigator" element={<Investigator />} />
              <Route path="/simulation" element={<Simulation />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;