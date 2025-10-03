import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np

class LlamaStyleAnalyzer:
    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    
    def analyze_stylistic_features(self, text):
        """Extract stylistic features using Llama"""
        prompt = f"""Analyze this text's writing style. Provide:
1. Sentence complexity (simple/compound/complex ratio)
2. Lexical sophistication level (1-10)
3. Formality level (1-10)
4. Dominant syntactic patterns
5. Discourse markers frequency

Text: {text}

Respond in JSON format."""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=500)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return self._parse_llama_response(response)
    
    def detect_inconsistencies(self, segments):
        """Compare stylistic features across text segments"""
        features_per_segment = [self.analyze_stylistic_features(seg) for seg in segments]
        
        inconsistencies = self._calculate_feature_variance(features_per_segment)
        
        return inconsistencies
    
    def generate_explanation(self, inconsistencies, text_segments):
        """Use Llama to generate human-readable explanation"""
        prompt = f"""You are a forensic linguistics expert. Explain why this text shows signs of authorship obfuscation.

Detected inconsistencies:
{inconsistencies}

Text segments:
{text_segments[:2]}  # Show first two segments

Provide a clear, non-technical explanation of what seems suspicious."""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=300)
        explanation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return explanation
    
    def _parse_llama_response(self, response):
        pass
    
    def _calculate_feature_variance(self, features_list):
        pass