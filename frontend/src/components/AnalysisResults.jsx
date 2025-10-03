import React from 'react';
import { AlertCircle, TrendingUp, BarChart3, Download } from 'lucide-react';
import { HeatMap } from './HeatMap';
import { FeatureBreakdown } from './FeatureBreakdown';

export const AnalysisResults = ({ results, onNewAnalysis }) => {
  const getRiskColor = (level) => {
    const colors = {
      'HIGH': 'bg-red-100 text-red-800 border-red-300',
      'MEDIUM': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      'LOW': 'bg-blue-100 text-blue-800 border-blue-300',
      'MINIMAL': 'bg-green-100 text-green-800 border-green-300'
    };
    return colors[level] || colors['MINIMAL'];
  };

  const getScoreColor = (score) => {
    if (score >= 0.7) return 'text-red-600';
    if (score >= 0.5) return 'text-yellow-600';
    if (score >= 0.3) return 'text-blue-600';
    return 'text-green-600';
  };

  const getScoreBarColor = (score) => {
    if (score >= 0.7) return 'bg-red-500';
    if (score >= 0.5) return 'bg-yellow-500';
    return 'bg-blue-500';
  };

  const exportReport = () => {
    const reportData = JSON.stringify(results, null, 2);
    const blob = new Blob([reportData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'obfuscation-analysis-report.json';
    a.click();
  };

  return (
    <div className="grid gap-6">
      {/* Overall Score Card */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-slate-900">Analysis Results</h2>
          <div className={`px-4 py-2 rounded-lg border-2 font-bold ${getRiskColor(results.risk_level)}`}>
            {results.risk_level} RISK
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Score Gauge */}
          <div className="flex flex-col items-center justify-center p-6 bg-slate-50 rounded-lg">
            <div className="relative w-48 h-48">
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="96"
                  cy="96"
                  r="80"
                  stroke="#e2e8f0"
                  strokeWidth="16"
                  fill="none"
                />
                <circle
                  cx="96"
                  cy="96"
                  r="80"
                  stroke={results.overall_score >= 0.7 ? '#dc2626' : results.overall_score >= 0.5 ? '#ca8a04' : '#2563eb'}
                  strokeWidth="16"
                  fill="none"
                  strokeDasharray={`${results.overall_score * 502.4} 502.4`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className={`text-4xl font-bold ${getScoreColor(results.overall_score)}`}>
                  {(results.overall_score * 100).toFixed(0)}%
                </span>
                <span className="text-sm text-slate-600 mt-1">Obfuscation Score</span>
              </div>
            </div>
            <p className="text-sm text-slate-600 text-center mt-4 max-w-xs">
              Higher scores indicate greater likelihood of deliberate stylistic manipulation
            </p>
          </div>

          {/* Component Scores */}
          <FeatureBreakdown scores={results.component_scores} />
        </div>
      </div>

      {/* AI Explanation */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-start gap-3">
          <div className="p-2 bg-indigo-100 rounded-lg flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-indigo-600" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-slate-900 mb-2">AI Analysis</h3>
            <p className="text-slate-700 leading-relaxed">
              {results.explanation}
            </p>
          </div>
        </div>
      </div>

      {/* Suspicious Segments */}
      {results.suspicious_segments && results.suspicious_segments.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-indigo-600" />
            <h3 className="font-semibold text-slate-900">Suspicious Text Segments</h3>
          </div>
          <div className="space-y-3">
            {results.suspicious_segments.map((segment, idx) => (
              <div key={idx} className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-slate-900">
                    Segment {segment.segment_index + 1}
                  </span>
                  <span className={`text-sm font-bold ${getScoreColor(segment.score)}`}>
                    Suspicion: {(segment.score * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${getScoreBarColor(segment.score)}`}
                    style={{ width: `${segment.score * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Heatmap */}
      <HeatMap segmentFeatures={results.segment_features} />

      {/* Export Options */}
      <div className="flex gap-3">
        <button 
          onClick={exportReport}
          className="flex-1 px-6 py-3 bg-white border-2 border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-colors flex items-center justify-center gap-2"
        >
          <Download className="w-4 h-4" />
          Export Report (JSON)
        </button>
        <button 
          onClick={onNewAnalysis}
          className="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors shadow-md"
        >
          Analyze New Text
        </button>
      </div>
    </div>
  );
};