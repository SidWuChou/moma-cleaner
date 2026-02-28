"""File Categorizer - Categorizes files by type"""
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)


class FileCategorizer:
    """Categorizes files by type"""
    
    def __init__(self, config):
        self.config = config
        
        # Category definitions
        self.categories = {
            'Images': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', 
                              '.svg', '.ico', '.tiff', '.psd', '.raw', '.heic', '.heif'],
                'folders': ['Images', 'Photos', 'Pictures', 'Screenshots']
            },
            'Videos': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
                              '.webm', '.m4v', '.mpeg', '.mpg', '.3gp'],
                'folders': ['Videos', 'Movies', 'Films', 'Video']
            },
            'Audio': {
                'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', 
                              '.m4a', '.opus', '.aiff'],
                'folders': ['Music', 'Audio', 'Sounds']
            },
            'Documents': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', 
                              '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.md'],
                'folders': ['Documents', 'Docs', 'Papers']
            },
            'Archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', 
                              '.xz', '.iso', '.dmg'],
                'folders': ['Archives', 'Compressed', 'Zip']
            },
            'Code': {
                'extensions': ['.py', '.js', '.ts', '.java', '.c', '.cpp', '.h',
                              '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt',
                              '.html', '.css', '.json', '.xml', '.yaml', '.yml',
                              '.sql', '.sh', '.bat', '.ps1'],
                'folders': ['Code', 'Projects', 'Src', 'Scripts']
            },
            'Executables': {
                'extensions': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm',
                              '.apk', '.ipa'],
                'folders': ['Programs', 'Applications', 'Apps', 'Software']
            },
            'Data': {
                'extensions': ['.db', '.sqlite', '.sqlite3', '.json', '.xml',
                              '.csv', '.dat', '.sql', '.bak'],
                'folders': ['Data', 'Database', 'Backups']
            }
        }
        
    def categorize(self, files: List[Dict]) -> Dict[str, List]:
        """Categorize files into categories"""
        result = {category: [] for category in self.categories.keys()}
        result['Other'] = []
        
        for file in files:
            category = self._get_category(file)
            
            if category:
                result[category].append(file)
            else:
                result['Other'].append(file)
                
        # Remove empty categories
        result = {k: v for k, v in result.items() if v}
        
        return result
        
    def _get_category(self, file: Dict) -> str:
        """Get category for a file"""
        ext = file.get('extension', '').lower()
        
        for category, info in self.categories.items():
            if ext in info['extensions']:
                return category
                
        # Also check folder name
        path = file.get('path', '')
        path_str = str(path)
        
        for category, info in self.categories.items():
            for folder in info['folders']:
                if folder.lower() in path_str.lower():
                    return category
                    
        return None
        
    def suggest_folder(self, file: Dict) -> str:
        """Suggest folder for a file"""
        category = self._get_category(file)
        
        if category:
            # Map to common folder names
            folder_map = {
                'Images': 'Images',
                'Videos': 'Videos', 
                'Audio': 'Music',
                'Documents': 'Documents',
                'Archives': 'Archives',
                'Code': 'Code',
                'Executables': 'Applications',
                'Data': 'Data'
            }
            return folder_map.get(category, category)
            
        return 'Misc'
        
    def get_stats(self, categorized: Dict) -> Dict:
        """Get statistics about categorized files"""
        stats = {}
        
        for category, files in categorized.items():
            total_size = sum(f.get('size', 0) for f in files)
            stats[category] = {
                'count': len(files),
                'size': total_size,
                'size_mb': round(total_size / (1024 * 1024), 2)
            }
            
        return stats
