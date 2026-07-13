import React from 'react';

export default function DashboardKPI({ title, value, subtext, highlightColor }) {
  const colors = {
    indigo: 'text-indigo-400',
    emerald: 'text-emerald-400',
    rose: 'text-rose-400',
    amber: 'text-amber-400'
  };

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-md">
      <p className="text-sm font-semibold text-gray-400 uppercase tracking-wider">{title}</p>
      <p className={`text-2xl font-bold mt-2 ${colors[highlightColor] || 'text-white'}`}>
        {value}
      </p>
      {subtext && <p className="text-xs text-gray-500 mt-1">{subtext}</p>}
    </div>
  );
}