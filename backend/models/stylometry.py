import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
import re

class StylometricAnalyzer:
    def __init__(self):
        # Download NLTK data if not already present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        self.stop_words = set(stopwords.words('english'))
        
    def extract_features(self, text):
        """Extract traditional stylometric features using NLTK only"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words_alpha = [w for w in words if w.isalpha()]
        words_lower = [w.lower() for w in words_alpha]
        
        if not words_alpha or not sentences:
            return self._empty_features()
        
        # Basic lexical features
        word_lengths = [len(w) for w in words_alpha]
        unique_words = set(words_lower)
        
        # POS approximation using simple rules (without spaCy)
        nouns = sum(1 for w in words_lower if w.endswith(('tion', 'ness', 'ment', 'ship', 'ity')))
        
        features = {
            # Lexical features
            'avg_word_length': np.mean(word_lengths),
            'type_token_ratio': len(unique_words) / len(words_lower),
            'hapax_legomena_ratio': sum(1 for count in Counter(words_lower).values() if count == 1) / len(words_lower),
            
            # Syntactic features
            'avg_sentence_length': len(words_alpha) / len(sentences),
            'sentence_length_variance': np.var([len(word_tokenize(s)) for s in sentences]),
            'avg_parse_tree_depth': 3.5,  # Placeholder - not needed for obfuscation detection
            
            # POS patterns (approximated)
            'noun_ratio': nouns / len(words_lower),
            'verb_ratio': 0.15,  # Placeholder
            'adj_ratio': 0.10,   # Placeholder
            'adv_ratio': 0.05,   # Placeholder
            
            # Function words
            'function_word_ratio': sum(1 for w in words_lower if w in self.stop_words) / len(words_lower),
            
            # Punctuation
            'comma_per_sentence': text.count(',') / len(sentences),
            'semicolon_per_sentence': text.count(';') / len(sentences),
            
            # Complexity
            'flesch_reading_ease': self._flesch_score(text, sentences, words_alpha),
        }
        
        return features
    
    def _empty_features(self):
        """Return empty feature dict"""
        return {
            'avg_word_length': 0,
            'type_token_ratio': 0,
            'hapax_legomena_ratio': 0,
            'avg_sentence_length': 0,
            'sentence_length_variance': 0,
            'avg_parse_tree_depth': 0,
            'noun_ratio': 0,
            'verb_ratio': 0,
            'adj_ratio': 0,
            'adv_ratio': 0,
            'function_word_ratio': 0,
            'comma_per_sentence': 0,
            'semicolon_per_sentence': 0,
            'flesch_reading_ease': 0,
        }
    
    def segment_text(self, text, segment_size=200):
        """Split text into segments for analysis"""
        words = word_tokenize(text)
        segments = []
        
        for i in range(0, len(words), segment_size):
            segment = ' '.join(words[i:i+segment_size])
            if len(segment.split()) >= 50:  # Minimum viable segment
                segments.append(segment)
        
        return segments
    
    def _flesch_score(self, text, sentences, words):
        """Calculate Flesch Reading Ease score"""
        syllables = sum(self._count_syllables(word) for word in words)
        
        if len(sentences) == 0 or len(words) == 0:
            return 0
        
        score = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))
        return score
    
    def _count_syllables(self, word):
        """Simple syllable counter"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel
        
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count = 1
        
        return count