import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function AnalyticsChart({ priceData, metrics, selectedCategory, events }) {
  if (!priceData.length || !metrics) return <div className="text-gray-400 text-center py-12">Loading data canvas...</div>;

  const filteredPrices = priceData.filter(d => {
    if (selectedCategory === 'All') return true;
    const matchingEvent = events.find(e => e.Date === d.date);
    return matchingEvent ? matchingEvent.Category === selectedCategory : true;
  });

  const labels = filteredPrices.map(d => d.date);
  const rawPrices = filteredPrices.map(d => d.price);
  const breakDateStr = metrics.inferred_break_date;
  const baselineModelLine = filteredPrices.map(d => {
    return d.date < breakDateStr ? metrics.mu_before : metrics.mu_after;
  });

  const dataSetStructure = {
    labels: labels,
    datasets: [
      { label: 'Actual Spot Price ($)', data: rawPrices, borderColor: 'rgba(99, 102, 241, 0.4)', borderWidth: 1.5, pointRadius: 0, fill: false },
      { label: 'Bayesian Mean Regimes', data: baselineModelLine, borderColor: '#f59e0b', borderWidth: 3, pointRadius: 0, borderDash: [5, 5], fill: false }
    ]
  };

  const chartOptions = {
    responsive: true, maintainAspectRatio: false,
    scales: {
      x: { grid: { color: '#374151' }, ticks: { color: '#9ca3af', maxTicksLimit: 10 } },
      y: { grid: { color: '#374151' }, ticks: { color: '#9ca3af' } }
    },
    plugins: { legend: { labels: { color: '#f3f4f6' } } }
  };

  return <div className="h-[450px] w-full"><Line data={dataSetStructure} options={chartOptions} /></div>;
}