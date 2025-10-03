import React from 'react';

export const FeatureBreakdown = ({ scores }) => {
  const getScoreColor = (score) => {
    if (score >= 0.7) return 'text-red-600';
    if (score >= 0.5) return 'text-yellow-600';
    if (score >= 0.3) return 'text-blue-600';
    return 'text-green-600';
  };

  const getBarColor = (score) => {
    if (score >= 0.7) return 'bg-red-500';
    if (score >= 0.5) return 'bg-yellow-500';
    return 'bg-blue-500';
  };

  const formatLabel = (key) => {
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="space-y-4">
      <h3 className="font-semibold text-slate-900 mb-4">Component Analysis</h3>
      {Object.entries(scores).map(([key, value]) => (
        <div key={key}>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-slate-700">
              {formatLabel(key)}
            </span>
            <span className={`text-sm font-bold ${getScoreColor(value)}`}>
              {(value * 100).toFixed(0)}%
            </span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${getBarColor(value)}`}
              style={{ width: `${value * 100}%` }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
};