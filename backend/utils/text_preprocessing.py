import re
from typing import List

class TextPreprocessor:
    def __init__(self):
        self.min_word_length = 2
        
    def clean_text(self, text: str) -> str:
        """Basic text cleaning while preserving style"""
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\'\"]', '', text)
        
        return text.strip()
    
    def split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = re.split(r'\n\n+', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace"""
        return ' '.join(text.split())
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs if needed"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def preprocess(self, text: str, remove_urls: bool = False) -> str:
        """Full preprocessing pipeline"""
        if remove_urls:
            text = self.remove_urls(text)
        
        text = self.clean_text(text)
        text = self.normalize_whitespace(text)
        
        return text