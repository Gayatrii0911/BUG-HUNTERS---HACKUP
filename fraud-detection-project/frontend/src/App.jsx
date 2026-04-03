import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Alerts from './pages/Alerts';
import Investigation from './pages/Investigation';
import Behavior from './pages/Behavior';
import Simulation from './pages/Simulation';
import './styles/theme.css';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-[hsl(var(--bg-deep))] text-[hsl(var(--text-muted))] font-sans selection:bg-[hsl(var(--accent-primary)/0.2)] selection:text-white relative overflow-hidden">
        {/* Subtle Background Glow */}
        <div className="absolute top-0 right-0 w-[1000px] h-[1000px] bg-[hsl(var(--accent-primary)/0.03)] rounded-full blur-[200px] pointer-events-none" />
        <div className="absolute bottom-0 left-80 w-[600px] h-[600px] bg-[hsl(var(--accent-secondary)/0.03)] rounded-full blur-[150px] pointer-events-none" />
        
        <Sidebar />
        <main className="flex-1 overflow-auto bg-transparent scrollbar-thin scrollbar-thumb-slate-700 relative z-10">
          <Navbar />
          <div className="p-8 pb-32 relative">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/investigator" element={<Investigation />} />
              <Route path="/behavior" element={<Behavior />} />
              <Route path="/simulation" element={<Simulation />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;