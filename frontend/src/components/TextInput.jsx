import React, { useState } from 'react';
import axios from 'axios';
import { Loader2, Info, FileText } from 'lucide-react';

export const TextInput = ({ onAnalysisComplete }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sampleTexts = {
    authentic: `The development of renewable energy technologies has become increasingly important in recent years as nations worldwide grapple with the pressing challenges of climate change and energy security. Solar panels have seen dramatic improvements in efficiency, with modern photovoltaic cells achieving conversion rates that were unimaginable just a decade ago. Similarly, wind turbines have become more cost-effective through advances in materials science and aerodynamic design, allowing them to generate power even in areas with moderate wind conditions. These advancements represent significant progress in our collective efforts to combat climate change and transition away from fossil fuel dependency. The integration of these technologies into existing power grids presents both substantial challenges and remarkable opportunities for energy companies and utilities. Engineers must develop sophisticated systems to manage the intermittent nature of renewable sources while maintaining grid stability and reliability. Many governments have implemented comprehensive incentive programs to encourage adoption of renewable energy sources, including tax credits, feed-in tariffs, and renewable portfolio standards. Research continues to push the boundaries of what is possible in energy storage and distribution, with battery technology and smart grid systems showing particular promise. The future of sustainable energy looks increasingly promising as innovation continues to accelerate across multiple fronts. Investment in green technology has reached unprecedented levels across multiple sectors, driven by both environmental concerns and economic opportunities. Public awareness and support for environmental initiatives has grown substantially over the past decade, creating political momentum for bold climate action. These factors combined suggest a positive trajectory for renewable energy development and deployment in the coming years.`,
    
    obfuscated: `Renewable energy tech development became very important lately. Nations deal with climate change problems everywhere now. Solar panels got way more efficient recently! Modern photovoltaic cells do conversion rates that were totally unimaginable before. Wind turbines are cheaper now through better materials and design stuff. They generate power even with moderate wind which is cool. This is big progress for fighting climate change and moving away from fossil fuels basically. Integrating these technologies into power grids is challenging but also presents opportunities, you know? Engineers gotta develop systems for managing intermittent renewable sources while keeping grids stable. Governments did incentive programs for renewable adoption - tax credits, feed-in tariffs, portfolio standards, all that. Research pushes energy storage boundaries continuously. Battery tech and smart grids show promise particularly. Sustainable energy's future appears promising with accelerating innovation happening. Green tech investment reached unprecedented levels. It's driven by environmental concerns plus economic opportunities simultaneously. Environmental initiative support grew substantially among the public lately. Political momentum for climate action exists now. Combined, these factors indicate positive renewable energy trajectory going forward into future years ahead.`,
    
    mixed: `The quantum computing revolution is fundamentally transforming computational capabilities across scientific and commercial domains. Traditional silicon-based processors face fundamental physical limitations as transistor sizes approach atomic scales. Quantum bits, or qubits, enable parallel processing at unprecedented scales by exploiting quantum superposition and entanglement phenomena. Major technology companies including IBM, Google, and Microsoft are investing billions of dollars in quantum research and development. These corporations lead the global race to achieve quantum supremacy and practical quantum advantage. But like, quantum computers are super cool and totally different from regular computers, right? They use qubits which are way more powerful than normal bits. The applications are gonna be absolutely amazing for stuff like cryptography and drug discovery and optimization problems. Scientists are working really hard on making quantum systems more stable and reliable. Error correction remains a significant technical challenge though, since quantum states are fragile. Decoherence and environmental noise affect quantum coherence significantly, limiting computation time. Research teams worldwide are developing novel approaches to quantum error correction using topological qubits and other innovative architectures. The timeline for practical quantum computers remains uncertain but progress accelerates rapidly. Some experts predict commercial viability within the next decade while others remain more skeptical about near-term applications.`
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
        const response = await axios.post('https://obfuscation-detector.onrender.com/analyze', {        text: text,
        segment_size: 50
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