import os
from groq import Groq

class LlamaStyleAnalyzer:
    """Analyzer using Meta Llama via Groq API"""
    
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=api_key)
                print("Llama analyzer initialized with Groq API")
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
                self.client = None
    
    def analyze_stylistic_features(self, text):
        """Analyze stylistic features using Llama"""
        if not self.client:
            return self._fallback_analysis(text)
        
        try:
            prompt = f"""Analyze the writing style of this text. Provide scores (1-10) for:
1. Sentence complexity
2. Lexical sophistication
3. Formality level

Text: {text[:500]}

Respond in JSON format:
{{"sentence_complexity": <score>, "lexical_sophistication": <score>, "formality_level": <score>}}"""

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse response - handle potential JSON parsing issues
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Llama API error: {e}")
            return self._fallback_analysis(text)
    
    def _fallback_analysis(self, text):
        """Fallback analysis if API unavailable"""
        words = text.split()
        sentences = text.split('.')
        unique_words = len(set(w.lower() for w in words))
        total_words = len(words)
        
        return {
            'sentence_complexity': 5,
            'lexical_sophistication': min(10, (unique_words / total_words * 10)) if total_words > 0 else 5,
            'formality_level': 6
        }
    
    def detect_inconsistencies(self, segments):
        """Detect inconsistencies between segments using Llama"""
        if not self.client or len(segments) < 2:
            return self._fallback_inconsistencies(segments)
        
        try:
            # Analyze first two segments for comparison
            segment_texts = "\n\n---SEGMENT---\n\n".join(segments[:3])
            
            prompt = f"""Compare the writing style across these text segments. Look for:
- Changes in vocabulary sophistication
- Shifts in sentence structure
- Inconsistent formality levels
- Unusual stylistic variations

Rate the consistency from 0.0 (completely inconsistent) to 1.0 (perfectly consistent).

{segment_texts}

Respond with just a number between 0.0 and 1.0."""

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.3,
                max_tokens=50
            )
            
            consistency_score = float(response.choices[0].message.content.strip())
            
            return {
                'consistency_score': max(0.0, min(1.0, consistency_score)),
                'segments_analyzed': len(segments),
                'variance': 1.0 - consistency_score
            }
            
        except Exception as e:
            print(f"Llama inconsistency detection error: {e}")
            return self._fallback_inconsistencies(segments)
    
    def _fallback_inconsistencies(self, segments):
        """Fallback inconsistency detection"""
        features = [self._fallback_analysis(seg) for seg in segments]
        sophistications = [f['lexical_sophistication'] for f in features]
        avg_soph = sum(sophistications) / len(sophistications)
        variance = sum((x - avg_soph)**2 for x in sophistications) / len(sophistications)
        
        return {
            'variance': variance,
            'consistency_score': 1.0 - min(variance / 10, 1.0),
            'segments_analyzed': len(segments)
        }
    
    def generate_explanation(self, inconsistencies, text_segments):
        """Generate explanation using Llama"""
        if not self.client:
            return self._fallback_explanation(inconsistencies)
        
        try:
            consistency = inconsistencies.get('consistency_score', 0.5)
            sample_text = text_segments[0][:300] if text_segments else ""
            
            prompt = f"""You are analyzing text for signs of authorship obfuscation (deliberate attempts to disguise writing style).

Consistency Score: {consistency:.2f} (1.0 = consistent, 0.0 = highly inconsistent)
Number of Segments: {inconsistencies.get('segments_analyzed', 0)}

Sample text: {sample_text}

Provide a 3-4 sentence analysis explaining:
1. What the consistency score indicates
2. Whether obfuscation is likely
3. Key stylistic patterns observed

Be specific and professional."""

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Llama explanation generation error: {e}")
            return self._fallback_explanation(inconsistencies)
    
    def _fallback_explanation(self, inconsistencies):
        """Fallback explanation generation"""
        consistency = inconsistencies.get('consistency_score', 0.5)
        
        if consistency < 0.5:
            return """This text exhibits significant stylistic inconsistencies across segments. The variation in lexical sophistication and sentence structure suggests potential authorship obfuscation. Key indicators include abrupt shifts in vocabulary complexity and inconsistent sentence patterns."""
        elif consistency < 0.7:
            return """This text shows moderate stylistic variation across segments. While some inconsistencies are present, they may fall within the normal range for a single author. However, certain patterns merit closer examination."""
        else:
            return """This text demonstrates relatively consistent stylistic patterns throughout. The lexical diversity and sentence complexity remain stable within expected ranges for authentic single-author writing. No significant indicators of manipulation were detected."""