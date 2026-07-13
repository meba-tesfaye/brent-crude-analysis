import React, { useState, useEffect } from 'react';
import DashboardKPI from './components/DashboardKPI';
import AnalyticsChart from './components/AnalyticsChart';

export default function App() {
  const [metrics, setMetrics] = useState(null);
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [categoryFilter, setCategoryFilter] = useState('All');

  useEffect(() => {
    Promise.all([
      fetch('http://127.0.0.1:5000/api/metrics').then(res => res.json()),
      fetch('http://127.0.0.1:5000/api/prices').then(res => res.json()),
      fetch('http://127.0.0.1:5000/api/events').then(res => res.json())
    ]).then(([metricsData, pricesData, eventsData]) => {
      setMetrics(metricsData);
      setPrices(pricesData);
      setEvents(eventsData);
    }).catch(err => console.error("API link exception:", err));
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <header className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-3xl font-black text-white tracking-tight">Brent Crude Oil Structural Analysis</h1>
        <p className="text-gray-400 text-sm mt-1">Decoupled React-Flask Production Change Point Infrastructure</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <DashboardKPI title="Structural Break Date" value={metrics ? metrics.inferred_break_date : "Loading..."} subtext={`MCMC Index: ${metrics ? metrics.inferred_tau_index : '...'}`} highlightColor="indigo" />
        <DashboardKPI title="Pre-Break Mean" value={metrics ? `$${metrics.mu_before.toFixed(2)}` : "Loading..."} subtext={`R-hat Check: ${metrics ? metrics.diagnostics.rhat_mu1.toFixed(2) : '...'}`} highlightColor="emerald" />
        <DashboardKPI title="Post-Break Mean" value={metrics ? `$${metrics.mu_after.toFixed(2)}` : "Loading..."} subtext={`R-hat Check: ${metrics ? metrics.diagnostics.rhat_mu2.toFixed(2) : '...'}`} highlightColor="rose" />
        <DashboardKPI title="Regime Shift" value={metrics ? `+${metrics.percentage_structural_shift.toFixed(1)}%` : "Loading..."} subtext="Statistically Significant" highlightColor="amber" />
      </div>

      <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
          <h3 className="text-lg font-bold text-white">Historical Time Series & Structural Thresholds</h3>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-400 font-medium">Filter Macro Context:</span>
            <select value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)} className="bg-gray-900 border border-gray-700 text-gray-200 px-4 py-2 rounded-lg text-sm outline-none focus:border-indigo-500">
              <option value="All">Show Full Series</option>
              <option value="Geopolitical">Geopolitical Milestones</option>
              <option value="Economic">Economic Shockwaves</option>
            </select>
          </div>
        </div>
        <AnalyticsChart priceData={prices} metrics={metrics} selectedCategory={categoryFilter} events={events} />
      </div>
    </div>
  );
}