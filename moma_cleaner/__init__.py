#!/usr/bin/env python3
"""
MomaCleaner - AI-Powered File Organizer
Main entry point
"""
import os
import argparse
import logging
from datetime import datetime
from pathlib import Path

from cleaner.scanner import FileScanner
from cleaner.categorizer import FileCategorizer
from cleaner.namer import AINamer
from cleaner.deduplicator import Deduplicator
from cleaner.config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MomaCleaner:
    """AI-Powered File Organizer"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = Config(config_path)
        self.scanner = FileScanner(self.config)
        self.categorizer = FileCategorizer(self.config)
        self.namer = AINamer(self.config)
        self.dedup = Deduplicator(self.config)
        
    def organize(self, path: str, dry_run: bool = False, ai_name: bool = False):
        """Organize files in a directory"""
        path = Path(path).resolve()
        
        if not path.exists():
            logger.error(f"Path does not exist: {path}")
            return
            
        logger.info(f"🧹 Starting MomaCleaner on: {path}")
        logger.info(f"Dry run: {dry_run}")
        
        # Scan files
        logger.info("📂 Scanning files...")
        files = self.scanner.scan(path)
        logger.info(f"Found {len(files)} files")
        
        # Categorize
        logger.info("🏷️ Categorizing files...")
        categorized = self.categorizer.categorize(files)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 ORGANIZATION SUMMARY")
        print("="*60)
        
        for category, file_list in categorized.items():
            if file_list:
                print(f"\n{category}: {len(file_list)} files")
                for f in file_list[:5]:  # Show first 5
                    print(f"  - {f.name}")
                if len(file_list) > 5:
                    print(f"  ... and {len(file_list) - 5} more")
        
        # AI naming
        if ai_name:
            logger.info("🤖 AI naming files...")
            for category, file_list in categorized.items():
                for f in file_list:
                    new_name = self.namer.suggest_name(f)
                    if new_name and new_name != f.stem:
                        print(f"  📝 {f.name} → {new_name}{f.suffix}")
        
        # Deduplication
        logger.info("🔍 Checking for duplicates...")
        duplicates = self.dedup.find_duplicates(files)
        
        if duplicates:
            print(f"\n⚠️ Found {len(duplicates)} duplicate groups:")
            for group in duplicates[:5]:
                print(f"  - {group[0].name} ({len(group)} copies)")
        
        # Execute or preview
        if dry_run:
            print("\n🔍 Dry run complete. Use without --dry-run to actually organize.")
        else:
            logger.info("📁 Organizing files...")
            self._organize_files(categorized)
            logger.info("✅ Organization complete!")
            
    def _organize_files(self, categorized: dict):
        """Actually move files to their categories"""
        # Implementation would move files to category folders
        pass
        
    def clean_duplicates(self, path: str, keep: str = "newest"):
        """Remove duplicate files"""
        path = Path(path)
        
        logger.info("🔍 Scanning for duplicates...")
        files = self.scanner.scan(path)
        
        duplicates = self.dedup.find_duplicates(files)
        
        if not duplicates:
            logger.info("No duplicates found!")
            return
            
        logger.info(f"Found {len(duplicates)} duplicate groups")
        
        # Remove duplicates
        removed = self.dedup.remove_duplicates(duplicates, keep=keep)
        
        logger.info(f"Removed {removed} duplicate files")


def main():
    parser = argparse.ArgumentParser(description="MomaCleaner - AI File Organizer")
    parser.add_argument('--path', type=str, help='Path to organize')
    parser.add_argument('--dry-run', action='store_true', help='Preview only')
    parser.add_argument('--ai-name', action='store_true', help='AI rename files')
    parser.add_argument('--dedup', action='store_true', help='Remove duplicates')
    parser.add_argument('--config', default='config.yaml', help='Config file')
    parser.add_argument('--schedule', choices=['hourly', 'daily', 'weekly'],
                       help='Schedule automatic cleaning')
    
    args = parser.parse_args()
    
    cleaner = MomaCleaner(args.config)
    
    if args.dedup and args.path:
        cleaner.clean_duplicates(args.path)
    elif args.path:
        cleaner.organize(args.path, dry_run=args.dry_run, ai_name=args.ai_name)
    elif args.schedule:
        logger.info(f"Scheduling {args.schedule} cleaning...")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
