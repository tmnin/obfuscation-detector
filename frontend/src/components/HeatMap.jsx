import React, { useState } from 'react';
import { BarChart3 } from 'lucide-react';

export const HeatMap = ({ segmentFeatures }) => {
  const [hoveredSegment, setHoveredSegment] = useState(null);

  // Calculate intensity based on deviation from mean
  const calculateIntensities = () => {
    if (!segmentFeatures || segmentFeatures.length === 0) return [];
    
    const avgWordLengths = segmentFeatures.map(f => f.avg_word_length);
    const mean = avgWordLengths.reduce((a, b) => a + b, 0) / avgWordLengths.length;
    const std = Math.sqrt(
      avgWordLengths.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / avgWordLengths.length
    );
    
  return avgWordLengths.map(val => {
      const zScore = Math.abs((val - mean) / (std || 1));
      return Math.min(zScore / 2, 1); // Normalize to 0-1
    });
  };

  const intensities = calculateIntensities();

  const getColor = (intensity) => {
    if (intensity >= 0.7) return '#dc2626'; // red
    if (intensity >= 0.5) return '#ca8a04'; // yellow
    return '#3b82f6'; // blue
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="w-5 h-5 text-indigo-600" />
        <h3 className="font-semibold text-slate-900">Text Heatmap</h3>
        <span className="text-sm text-slate-600 ml-2">
          (Shows stylistic variation across segments)
        </span>
      </div>
      
      <div className="flex gap-1 h-16 relative">
        {intensities.map((intensity, idx) => (
          <div
            key={idx}
            className="flex-1 rounded transition-all hover:scale-105 cursor-pointer relative group"
            style={{
              backgroundColor: getColor(intensity),
              opacity: 0.3 + (intensity * 0.7)
            }}
            onMouseEnter={() => setHoveredSegment(idx)}
            onMouseLeave={() => setHoveredSegment(null)}
          >
            {hoveredSegment === idx && (
              <div className="absolute -top-20 left-1/2 transform -translate-x-1/2 bg-slate-900 text-white text-xs px-3 py-2 rounded shadow-lg z-10 whitespace-nowrap">
                <div className="font-semibold mb-1">Segment {idx + 1}</div>
                <div>Deviation: {(intensity * 100).toFixed(0)}%</div>
                <div>Avg word length: {segmentFeatures[idx].avg_word_length.toFixed(2)}</div>
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="flex justify-between mt-3 text-xs text-slate-600">
        <span>Start of text</span>
        <span>End of text</span>
      </div>
      
      <div className="flex items-center justify-center gap-4 mt-4 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#3b82f6', opacity: 0.5 }}></div>
          <span className="text-slate-600">Low variation</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#ca8a04', opacity: 0.7 }}></div>
          <span className="text-slate-600">Medium variation</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: '#dc2626', opacity: 0.9 }}></div>
          <span className="text-slate-600">High variation</span>
        </div>
      </div>
    </div>
  );
};