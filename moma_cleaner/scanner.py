"""File Scanner - Scans directories for files"""
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)


class FileScanner:
    """Scans directories for files"""
    
    def __init__(self, config):
        self.config = config
        self.exclude_dirs = config.get('exclude_dirs', [
            '.git', '.svn', 'node_modules', '__pycache__', '.DS_Store'
        ])
        self.exclude_exts = config.get('exclude_exts', [
            '.tmp', '.temp', '.lock', '.log'
        ])
        
    def scan(self, path: Path) -> List[Path]:
        """Scan directory for files"""
        files = []
        
        for root, dirs, filenames in os.walk(path):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for filename in filenames:
                # Skip excluded extensions
                if any(filename.endswith(ext) for ext in self.exclude_exts):
                    continue
                    
                filepath = Path(root) / filename
                
                # Skip directories
                if filepath.is_file():
                    # Get file info
                    stat = filepath.stat()
                    file_info = {
                        'path': filepath,
                        'name': filename,
                        'stem': filepath.stem,
                        'suffix': filepath.suffix,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime),
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'extension': filepath.suffix.lower()
                    }
                    files.append(file_info)
                    
        logger.info(f"Scanned {len(files)} files")
        return files
        
    def scan_by_date(self, path: Path, days: int = 30) -> dict:
        """Scan files by modification date"""
        files = self.scan(path)
        
        now = datetime.now()
        result = {
            'today': [],
            'this_week': [],
            'this_month': [],
            'older': []
        }
        
        for f in files:
            age = (now - f['modified']).days
            
            if age == 0:
                result['today'].append(f)
            elif age <= 7:
                result['this_week'].append(f)
            elif age <= 30:
                result['this_month'].append(f)
            else:
                result['older'].append(f)
                
        return result
        
    def scan_by_size(self, path: Path) -> dict:
        """Scan files by size"""
        files = self.scan(path)
        
        result = {
            'tiny': [],     # < 1KB
            'small': [],   # 1KB - 1MB
            'medium': [],  # 1MB - 100MB
            'large': [],   # > 100MB
            'huge':        # > 1GB
        }
        
        for f in files:
            size = f['size']
            
            if size < 1024:
                result['tiny'].append(f)
            elif size < 1024 * 1024:
                result['small'].append(f)
            elif size < 100 * 1024 * 1024:
                result['medium'].append(f)
            elif size < 1024 * 1024 * 1024:
                result['large'].append(f)
            else:
                result['huge'].append(f)
                
        return result
