from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from models.llama_analyzer import LlamaStyleAnalyzer
from models.stylometry import StylometricAnalyzer
from models.obfuscation_scorer import ObfuscationScorer

app = FastAPI(title="Authorship Obfuscation Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://obfuscationdetector.netlify.app",
    "http://localhost:3000",
    "http://localhost:3001",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llama_analyzer = LlamaStyleAnalyzer()
stylometric_analyzer = StylometricAnalyzer()
obfuscation_scorer = ObfuscationScorer()

class TextInput(BaseModel):
    text: str
    segment_size: int = 200

@app.post("/analyze")
async def analyze_text(input_data: TextInput):
    """Main analysis endpoint"""
    try:
        text = input_data.text
        
        if len(text.split()) < 100:
            raise HTTPException(400, "Text too short. Need at least 100 words.")
        
        segments = stylometric_analyzer.segment_text(text, input_data.segment_size)
        
        if len(segments) < 3:
            raise HTTPException(400, "Text too short for reliable analysis. Need at least 3 segments.")
        
        segment_features = [stylometric_analyzer.extract_features(seg) for seg in segments]
        
        obfuscation_results = obfuscation_scorer.calculate_obfuscation_score(segment_features)
        
        llama_inconsistencies = llama_analyzer.detect_inconsistencies(segments)
        explanation = llama_analyzer.generate_explanation(
            obfuscation_results,
            segments
        )
        
        return {
            'overall_score': obfuscation_results['overall_score'],
            'risk_level': obfuscation_results['risk_level'],
            'component_scores': obfuscation_results['component_scores'],
            'suspicious_segments': obfuscation_results['suspicious_segments'],
            'explanation': explanation,
            'llama_analysis': llama_inconsistencies,
            'num_segments': len(segments),
            'segment_features': segment_features
        }
        
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)