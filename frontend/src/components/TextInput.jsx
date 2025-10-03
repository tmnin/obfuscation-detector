import React, { useState } from 'react';
import axios from 'axios';
import { Loader2 } from 'lucide-react';

export const TextInput = ({ onAnalysisComplete }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (text.split(/\s+/).filter(w => w).length < 100) {
      setError('Please enter at least 100 words');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        text: text,
        segment_size: 200
      });
      onAnalysisComplete(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste text here..."
        className="w-full h-64 p-4 border rounded-lg"
        disabled={loading}
      />
      {error && <p className="text-red-600 text-sm">{error}</p>}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="px-6 py-3 bg-indigo-600 text-white rounded-lg disabled:bg-gray-400"
      >
        {loading ? (
          <>
            <Loader2 className="animate-spin inline mr-2" />
            Analyzing...
          </>
        ) : (
          'Analyze Text'
        )}
      </button>
    </div>
  );
};