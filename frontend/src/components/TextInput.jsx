import React, { useState } from 'react';
import axios from 'axios';
import { Loader2, Info, FileText } from 'lucide-react';

export const TextInput = ({ onAnalysisComplete }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sampleTexts = {
    authentic: `The development of renewable energy technologies has become increasingly important in recent years. Solar panels have seen dramatic improvements in efficiency, while wind turbines have become more cost-effective. These advancements represent significant progress in our efforts to combat climate change. The integration of these technologies into existing power grids presents both challenges and opportunities for energy companies. Many governments have implemented incentive programs to encourage adoption of renewable energy sources. Research continues to push the boundaries of what is possible in energy storage and distribution. The future of sustainable energy looks promising as innovation continues to accelerate. Investment in green technology has reached unprecedented levels across multiple sectors. Public awareness and support for environmental initiatives has grown substantially. These factors combined suggest a positive trajectory for renewable energy development.`,
    
    obfuscated: `Renewable energy tech development became very important lately. Solar panels got way more efficient, and wind turbines are cheaper now. This is big progress for fighting climate change! Integrating these technologies into power grids is challenging but also presents opportunities. Governments did incentive programs for renewable adoption. Research pushes energy storage boundaries continuously. Sustainable energy's future appears promising with accelerating innovation. Green tech investment reached unprecedented levels. Environmental initiative support grew substantially among the public. Combined, these factors indicate positive renewable energy trajectory.`,
    
    mixed: `The quantum computing revolution is transforming computational capabilities. Traditional silicon-based processors face fundamental limitations. Quantum bits enable parallel processing at unprecedented scales. Major technology companies invest billions in quantum research. IBM, Google, and Microsoft lead the development race. But like, quantum computers are super cool and stuff. They use qubits which are totally different from regular bits. The applications are gonna be amazing for cryptography and drug discovery. Scientists are working really hard on making them stable. Error correction remains a significant challenge tho. Decoherence and noise affect quantum states significantly.`
  };

  const handleAnalyze = async () => {
    const wordCount = text.split(/\s+/).filter(w => w).length;
    
    if (wordCount < 100) {
      setError('Please enter at least 100 words for reliable analysis');
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
      setError(err.response?.data?.detail || 'Analysis failed. Please check if the backend is running.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadSample = (key) => {
    setText(sampleTexts[key]);
    setError('');
  };

  const wordCount = text.split(/\s+/).filter(w => w).length;

  return (
    <div className="grid gap-6">
      {/* Instructions Card */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-start gap-3 mb-4">
          <Info className="w-5 h-5 text-indigo-600 mt-1 flex-shrink-0" />
          <div>
            <h3 className="font-semibold text-slate-900 mb-1">How it works</h3>
            <p className="text-sm text-slate-600">
              Paste text (minimum 100 words) to analyze for signs of deliberate stylistic manipulation. 
              Our AI examines lexical, syntactic, and stylistic patterns to detect inconsistencies that 
              suggest the author is trying to disguise their writing style.
            </p>
          </div>
        </div>
      </div>

      {/* Text Input Card */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-indigo-600" />
          <h3 className="font-semibold text-slate-900">Enter Text for Analysis</h3>
        </div>
        
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste the text you want to analyze here..."
          className="w-full h-64 p-4 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none font-mono text-sm"
          disabled={loading}
        />
        
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-4">
            <span className={`text-sm ${wordCount >= 100 ? 'text-green-600' : 'text-slate-600'}`}>
              Word count: {wordCount} {wordCount >= 100 && '✓'}
            </span>
            {wordCount < 100 && (
              <span className="text-xs text-slate-500">
                ({100 - wordCount} more needed)
              </span>
            )}
          </div>
          <button 
            onClick={handleAnalyze}
            disabled={loading || wordCount < 100}
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              'Analyze Text'
            )}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Sample Texts Card */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="font-semibold text-slate-900 mb-3">Try Sample Texts</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button 
            onClick={() => loadSample('authentic')}
            className="p-4 border-2 border-slate-200 rounded-lg hover:border-indigo-400 hover:bg-indigo-50 transition-all text-left"
          >
            <div className="font-medium text-sm text-slate-900 mb-1">Authentic Writing</div>
            <div className="text-xs text-slate-600">
              Natural, consistent style throughout
            </div>
          </button>
          <button 
            onClick={() => loadSample('obfuscated')}
            className="p-4 border-2 border-slate-200 rounded-lg hover:border-indigo-400 hover:bg-indigo-50 transition-all text-left"
          >
            <div className="font-medium text-sm text-slate-900 mb-1">Obfuscated Sample</div>
            <div className="text-xs text-slate-600">
              Deliberately manipulated style
            </div>
          </button>
          <button 
            onClick={() => loadSample('mixed')}
            className="p-4 border-2 border-slate-200 rounded-lg hover:border-indigo-400 hover:bg-indigo-50 transition-all text-left"
          >
            <div className="font-medium text-sm text-slate-900 mb-1">Mixed Authorship</div>
            <div className="text-xs text-slate-600">
              Multiple writing styles combined
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};