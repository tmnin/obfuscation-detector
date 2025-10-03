import numpy as np
from collections import Counter
from typing import Dict, List
import re

class FeatureExtractor:
    """Additional feature extraction utilities"""
    
    def __init__(self):
        self.common_function_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'if', 'of', 'at', 'by', 'for',
            'with', 'about', 'as', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
            'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
            'when', 'where', 'why', 'how', 'all', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
            'don', 'should', 'now'
        }
    
    def extract_ngram_features(self, words: List[str], n: int = 2) -> Dict:
        """Extract n-gram features"""
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)
        
        ngram_counts = Counter(ngrams)
        total_ngrams = len(ngrams)
        
        return {
            f'{n}gram_diversity': len(ngram_counts) / total_ngrams if total_ngrams > 0 else 0,
            f'most_common_{n}grams': ngram_counts.most_common(10)
        }
    
    def extract_punctuation_features(self, text: str) -> Dict:
        """Extract punctuation usage patterns"""
        punctuation_marks = {
            ',': 'comma',
            '.': 'period',
            '!': 'exclamation',
            '?': 'question',
            ';': 'semicolon',
            ':': 'colon',
            '-': 'dash',
            '(': 'parenthesis',
            '"': 'quote'
        }
        
        features = {}
        total_chars = len(text)
        
        for mark, name in punctuation_marks.items():
            count = text.count(mark)
            features[f'{name}_frequency'] = count / total_chars if total_chars > 0 else 0
        
        return features
    
    def extract_readability_features(self, text: str, sentences: List, words: List) -> Dict:
        """Extract various readability metrics"""
        if not sentences or not words:
            return {
                'avg_words_per_sentence': 0,
                'avg_chars_per_word': 0,
                'long_word_ratio': 0
            }
        
        total_chars = sum(len(word) for word in words)
        long_words = sum(1 for word in words if len(word) > 6)
        
        return {
            'avg_words_per_sentence': len(words) / len(sentences),
            'avg_chars_per_word': total_chars / len(words),
            'long_word_ratio': long_words / len(words)
        }
    
    def extract_function_word_profile(self, words: List[str]) -> Dict:
        """Detailed function word analysis"""
        words_lower = [w.lower() for w in words]
        total_words = len(words_lower)
        
        function_word_counts = {}
        for fw in self.common_function_words:
            count = words_lower.count(fw)
            function_word_counts[fw] = count / total_words if total_words > 0 else 0
        
        # Get top 10 most used function words
        sorted_fw = sorted(function_word_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'function_word_profile': dict(sorted_fw[:10]),
            'function_word_diversity': len([fw for fw, freq in function_word_counts.items() if freq > 0]) / len(self.common_function_words)
        }
    
    def extract_lexical_richness(self, words: List[str]) -> Dict:
        """Calculate various lexical richness metrics"""
        words_lower = [w.lower() for w in words]
        word_counts = Counter(words_lower)
        
        #Hapax legomena 
        hapax = sum(1 for count in word_counts.values() if count == 1)
        
        #Hapax dislegomena 
        dis = sum(1 for count in word_counts.values() if count == 2)
        
        #Yule's K 
        M1 = len(words_lower)
        M2 = sum([freq ** 2 for freq in word_counts.values()])
        
        yules_k = 10000 * (M2 - M1) / (M1 ** 2) if M1 > 0 else 0
        
        return {
            'hapax_legomena': hapax,
            'hapax_dislegomena': dis,
            'yules_k': yules_k,
            'unique_word_ratio': len(word_counts) / len(words_lower) if words_lower else 0
        }
    
    def extract_sentence_variety(self, sentences: List) -> Dict:
        """Analyze sentence structure variety"""
        if not sentences:
            return {
                'sentence_length_variance': 0,
                'sentence_length_std': 0,
                'length_coefficient_variation': 0
            }
        
        lengths = [len(sent.split()) for sent in sentences]
        
        mean_length = np.mean(lengths)
        std_length = np.std(lengths)
        
        return {
            'sentence_length_variance': np.var(lengths),
            'sentence_length_std': std_length,
            'length_coefficient_variation': std_length / mean_length if mean_length > 0 else 0,
            'min_sentence_length': min(lengths),
            'max_sentence_length': max(lengths)
        }