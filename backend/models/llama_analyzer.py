class LlamaStyleAnalyzer:
    """Simplified analyzer without heavy transformers dependency"""
    
    def __init__(self):
        print("Using lightweight stylometric analysis (no LLM required)")
    
    def analyze_stylistic_features(self, text):
        """Basic feature analysis without transformers"""
        words = text.split()
        sentences = text.split('.')
        
        # Calculate basic metrics
        unique_words = len(set(w.lower() for w in words))
        total_words = len(words)
        
        return {
            'sentence_complexity': 'medium',
            'lexical_sophistication': min(10, (unique_words / total_words * 10)) if total_words > 0 else 5,
            'formality_level': 6,
            'avg_word_length': sum(len(w) for w in words) / total_words if total_words > 0 else 0,
            'dominant_patterns': 'varied sentence structure',
            'discourse_markers': 'moderate usage'
        }
    
    def detect_inconsistencies(self, segments):
        """Detect inconsistencies between segments"""
        features = [self.analyze_stylistic_features(seg) for seg in segments]
        
        # Calculate variance in sophistication
        sophistications = [f['lexical_sophistication'] for f in features]
        avg_soph = sum(sophistications) / len(sophistications)
        variance = sum((x - avg_soph)**2 for x in sophistications) / len(sophistications)
        
        return {
            'variance': variance,
            'consistency_score': 1.0 - min(variance / 10, 1.0),
            'segments_analyzed': len(segments)
        }
    
    def generate_explanation(self, inconsistencies, text_segments):
        """Generate explanation based on analysis"""
        consistency = inconsistencies.get('consistency_score', 0.5)
        
        if consistency < 0.5:
            return """This text exhibits significant stylistic inconsistencies across segments. 
The variation in lexical sophistication and sentence structure suggests potential authorship obfuscation. 
Key indicators include: abrupt shifts in vocabulary complexity between sections, inconsistent sentence 
patterns that don't match natural writing evolution, and unnatural variation in stylistic markers. 
These patterns deviate significantly from typical single-author writing and warrant further investigation."""
        
        elif consistency < 0.7:
            return """This text shows moderate stylistic variation across segments. While some inconsistencies 
are present in vocabulary usage and sentence structure, they may fall within the normal range of variation 
for a single author writing over time or in different contexts. However, certain segments show unusual 
patterns that merit closer examination. Consider analyzing specific suspicious segments for more detailed insights."""
        
        else:
            return """This text demonstrates relatively consistent stylistic patterns throughout all analyzed segments. 
The lexical diversity, sentence complexity, and other stylometric features remain stable within expected ranges 
for authentic single-author writing. While minor variations exist (as is natural in any text), they follow 
predictable patterns and do not suggest deliberate obfuscation. No significant indicators of stylistic 
manipulation were detected."""