"""Configuration Module"""
import yaml
from typing import Any


class Config:
    """Configuration manager"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._config = {}
        self._load()
        
    def _load(self):
        """Load config from file"""
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            self._config = self._default()
            
    def _default(self) -> dict:
        """Default configuration"""
        return {
            # Directories to exclude
            'exclude_dirs': [
                '.git', '.svn', 'node_modules', '__pycache__', 
                '.DS_Store', '.Trash'
            ],
            
            # Extensions to exclude
            'exclude_exts': [
                '.tmp', '.temp', '.lock', '.log', '.part'
            ],
            
            # Category mappings
            'categories': {
                'Images': ['.jpg', '.png', '.gif', '.webp'],
                'Videos': ['.mp4', '.avi', '.mkv'],
                'Documents': ['.pdf', '.doc', '.txt'],
            },
            
            # Organization settings
            'organize_by': 'category',  # category, date, size
            
            # Deduplication
            'dedup_enabled': True,
            
            # AI naming
            'ai_name_enabled': False,
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        return self._config.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set config value"""
        self._config[key] = value
