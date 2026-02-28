"""AI Namer - Suggests better names for files"""
import logging
import hashlib
from typing import Dict

logger = logging.getLogger(__name__)


class AINamer:
    """AI-powered file naming"""
    
    def __init__(self, config):
        self.config = config
        
    def suggest_name(self, file: Dict) -> str:
        """Suggest a better name for a file"""
        # Simple rule-based naming
        # In production, use AI/LLM for better suggestions
        
        original = file.get('stem', '')
        suffix = file.get('suffix', '')
        
        # Clean up the name
        new_name = self._clean_name(original)
        
        # Add date if missing
        if file.get('modified'):
            date_str = file['modified'].strftime('%Y%m%d')
            if date_str not in new_name:
                new_name = f"{date_str}_{new_name}"
                
        return new_name
        
    def _clean_name(self, name: str) -> str:
        """Clean up a messy filename"""
        import re
        
        # Remove common junk
        junk_patterns = [
            r'\s*-\s*\d+\s*$',  # Trailing numbers
            r'\s*\(.*\)\s*$',    # Parentheses content
            r'\s*\[.*\]\s*$',    # Brackets content
            r'_+',               # Multiple underscores
            r'\s+',              # Multiple spaces
        ]
        
        cleaned = name
        for pattern in junk_patterns:
            cleaned = re.sub(pattern, '', cleaned)
            
        # Replace spaces with underscores
        cleaned = cleaned.strip().replace(' ', '_')
        
        # Lowercase
        cleaned = cleaned.lower()
        
        return cleaned
        
    def batch_suggest(self, files: list) -> Dict[str, str]:
        """Suggest names for multiple files"""
        result = {}
        
        for file in files:
            path = file.get('path')
            if path:
                new_name = self.suggest_name(file)
                result[str(path)] = new_name
                
        return result
