"""Deduplicator - Finds and removes duplicate files"""
import logging
import hashlib
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

logger = logging.getLogger(__name__)


class Deduplicator:
    """Finds and removes duplicate files"""
    
    def __init__(self, config):
        self.config = config
        
    def find_duplicates(self, files: List[Dict]) -> List[List[Dict]]:
        """Find duplicate files based on content hash"""
        logger.info("Finding duplicates...")
        
        # Group by size first (quick filter)
        size_groups = defaultdict(list)
        for f in files:
            size = f.get('size', 0)
            if size > 0:  # Skip empty files
                size_groups[size].append(f)
                
        # Only check files with same size
        duplicates = []
        
        for size, file_group in size_groups.items():
            if len(file_group) < 2:
                continue
                
            # Hash files of same size
            hash_groups = defaultdict(list)
            
            for f in file_group:
                file_hash = self._hash_file(f.get('path'))
                if file_hash:
                    hash_groups[file_hash].append(f)
                    
            # Add to duplicates
            for file_hash, files_with_hash in hash_groups.items():
                if len(files_with_hash) > 1:
                    duplicates.append(files_with_hash)
                    
        logger.info(f"Found {len(duplicates)} duplicate groups")
        return duplicates
        
    def _hash_file(self, filepath: Path, chunk_size: int = 8192) -> str:
        """Calculate hash of file content"""
        try:
            hasher = hashlib.md5()
            
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
                    
            return hasher.hexdigest()
            
        except Exception as e:
            logger.warning(f"Failed to hash {filepath}: {e}")
            return None
            
    def remove_duplicates(self, duplicates: List[List[Dict]], 
                         keep: str = "newest") -> int:
        """Remove duplicate files"""
        removed = 0
        
        for group in duplicates:
            # Sort by date
            if keep == "newest":
                group.sort(key=lambda x: x.get('modified', 0), reverse=True)
            elif keep == "oldest":
                group.sort(key=lambda x: x.get('modified', 0))
            elif keep == "shortest":
                group.sort(key=lambda x: len(str(x.get('path', ''))))
                
            # Keep first, remove rest
            for f in group[1:]:
                try:
                    path = f.get('path')
                    if path and path.exists():
                        path.unlink()
                        logger.info(f"Removed duplicate: {path}")
                        removed += 1
                except Exception as e:
                    logger.error(f"Failed to remove {f}: {e}")
                    
        return removed
        
    def find_similar_names(self, files: List[Dict], threshold: float = 0.8) -> List:
        """Find files with similar names"""
        from difflib import SequenceMatcher
        
        similar = []
        names = [(f, f.get('name', '')) for f in files]
        
        for i, (f1, name1) in enumerate(names):
            for f2, name2 in names[i+1:]:
                ratio = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
                
                if ratio >= threshold:
                    similar.append({
                        'file1': f1,
                        'file2': f2,
                        'similarity': ratio
                    })
                    
        return similar
