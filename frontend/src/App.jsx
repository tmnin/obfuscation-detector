import React, { useState } from 'react';
import { TextInput } from './components/TextInput';
import { AnalysisResults } from './components/AnalysisResults';
import { FileText } from 'lucide-react';

function App() {
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('input');

  const handleAnalysisComplete = (data) => {
    setResults(data);
    setActiveTab('results');
  };

  const handleNewAnalysis = () => {
    setResults(null);
    setActiveTab('input');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-indigo-600 rounded-lg">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">
                  Authorship Obfuscation Detector
                </h1>
                <p className="text-sm text-slate-600">Powered by Meta Llama</p>
              </div>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-indigo-50 rounded-lg border border-indigo-200">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium text-indigo-900">System Ready</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('input')}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'input'
                ? 'bg-white text-indigo-600 shadow-md'
                : 'bg-white/50 text-slate-600 hover:bg-white'
            }`}
          >
            1. Input Text
          </button>
          <button
            onClick={() => results && setActiveTab('results')}
            disabled={!results}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'results'
                ? 'bg-white text-indigo-600 shadow-md'
                : 'bg-white/50 text-slate-600 hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed'
            }`}
          >
            2. Analysis Results
          </button>
        </div>

        {/* Content */}
        {activeTab === 'input' && (
          <TextInput onAnalysisComplete={handleAnalysisComplete} />
        )}

        {activeTab === 'results' && results && (
          <AnalysisResults results={results} onNewAnalysis={handleNewAnalysis} />
        )}
      </div>
    </div>
  );
}

export default App;