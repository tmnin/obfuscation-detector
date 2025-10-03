import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import numpy as np
import spacy

class StylometricAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        nltk.download('punkt', quiet=True)
        
    def extract_features(self, text):
        """Extract traditional stylometric features"""
        doc = self.nlp(text)
        sentences = list(doc.sents)
        tokens = [token for token in doc if not token.is_punct]
        
        features = {
            # Lexical features
            'avg_word_length': np.mean([len(token.text) for token in tokens]),
            'type_token_ratio': len(set([t.text.lower() for t in tokens])) / len(tokens),
            'hapax_legomena_ratio': sum(1 for count in Counter([t.text.lower() for t in tokens]).values() if count == 1) / len(tokens),
            
            # Syntactic features
            'avg_sentence_length': np.mean([len(list(sent)) for sent in sentences]),
            'sentence_length_variance': np.var([len(list(sent)) for sent in sentences]),
            'avg_parse_tree_depth': self._avg_tree_depth(doc),
            
            # POS patterns
            'noun_ratio': sum(1 for t in tokens if t.pos_ == 'NOUN') / len(tokens),
            'verb_ratio': sum(1 for t in tokens if t.pos_ == 'VERB') / len(tokens),
            'adj_ratio': sum(1 for t in tokens if t.pos_ == 'ADJ') / len(tokens),
            'adv_ratio': sum(1 for t in tokens if t.pos_ == 'ADV') / len(tokens),
            
            # Function words
            'function_word_ratio': sum(1 for t in tokens if t.is_stop) / len(tokens),
            
            # Punctuation
            'comma_per_sentence': len([t for t in doc if t.text == ',']) / len(sentences),
            'semicolon_per_sentence': len([t for t in doc if t.text == ';']) / len(sentences),
            
            # Complexity
            'flesch_reading_ease': self._flesch_score(text),
        }
        
        return features
    
    def segment_text(self, text, segment_size=200):
        """Split text into segments for analysis"""
        words = word_tokenize(text)
        segments = []
        
        for i in range(0, len(words), segment_size):
            segment = ' '.join(words[i:i+segment_size])
            if len(segment.split()) >= 50:  #minimum viable segment
                segments.append(segment)
        
        return segments
    
    def _avg_tree_depth(self, doc):
        """Calculate average parse tree depth"""
        depths = []
        for sent in doc.sents:
            for token in sent:
                depth = 0
                current = token
                while current.head != current:
                    depth += 1
                    current = current.head
                depths.append(depth)
        return np.mean(depths) if depths else 0
    
    def _flesch_score(self, text):
        """Calculate Flesch Reading Ease score"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
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