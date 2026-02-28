#!/usr/bin/env python3
"""
MomaCleaner - AI-Powered File Organizer
Now with REAL AI using MiniMax-M2.5
"""
import os
import requests
import json
from datetime import datetime
from pathlib import Path

# MiniMax API
API_KEY = "sk-api-t3NvNNPlbsqIFLbqGrhlwMNTzUyPk2fqbGEg25SWSNSjgUPb9bl797i8tf53yqZfFAbwFxL9-89ioQ2U0vpWk_MR3gsDPXWHRBM_EaKCCmjEZL6GduxIn0k"

class MomaCleanerAI:
    def __init__(self):
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.ppt', '.pptx'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Code': ['.py', '.js', '.ts', '.java', '.c', '.cpp', '.html', '.css'],
            'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'Data': ['.json', '.xml', '.csv', '.sql', '.db']
        }
        
    def ask_ai(self, prompt):
        """Ask MiniMax AI"""
        url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "MiniMax-M2.5",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        result = r.json()
        if 'choices' in result and result['choices']:
            return result['choices'][0]['message']['content']
        return "AI unavailable"
        
    def scan_folder(self, path):
        """Scan folder for files"""
        files = []
        
        for root, dirs, filenames in os.walk(path):
            for f in filenames:
                filepath = Path(root) / f
                try:
                    stat = filepath.stat()
                    files.append({
                        'name': f,
                        'path': str(filepath),
                        'size': stat.st_size,
                        'ext': filepath.suffix.lower(),
                        'modified': datetime.fromtimestamp(stat.st_mtime)
                    })
                except:
                    pass
                    
        return files
        
    def categorize_file(self, filepath):
        """Categorize a file"""
        ext = Path(filepath).suffix.lower()
        
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category
                
        return 'Other'
        
    def analyze_with_ai(self, files):
        """Use AI to analyze files and give recommendations"""
        # Build file summary
        by_category = {}
        for f in files:
            cat = self.categorize_file(f['path'])
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(f['name'])
        
        summary = "文件统计:\n"
        for cat, names in by_category.items():
            summary += f"- {cat}: {len(names)} 个文件\n"
        
        # Old files
        old_files = [f for f in files if (datetime.now() - f['modified']).days > 30]
        if old_files:
            summary += f"- 超过30天的文件: {len(old_files)} 个\n"
        
        # Large files
        large_files = [f for f in files if f['size'] > 100*1024*1024]  # > 100MB
        if large_files:
            summary += f"- 大文件(>100MB): {len(large_files)} 个\n"
        
        prompt = f"""你是一个文件管理专家。请分析以下文件夹的文件情况，给出整理建议:

{summary}

请用中文给出:
1. 文件分布分析
2. 整理建议 (哪些可以删除、哪些应该归档)
3. 存储优化建议

回答要实用，控制在150字以内。"""
        
        return self.ask_ai(prompt)
        
    def suggest_filename(self, filepath):
        """Use AI to suggest a better filename"""
        filename = Path(filepath).stem
        ext = Path(filepath).suffix
        
        prompt = f"""请为以下文件起一个更好的名字:

原始文件名: {filename}
文件类型: {ext}

请给出3个建议的名称（简洁的），只用中文回答，一行一个。"""
        
        result = self.ask_ai(prompt)
        return result
        
    def analyze_duplicate(self, files):
        """Analyze potential duplicates"""
        by_name = {}
        for f in files:
            name = Path(f['path']).stem.lower()
            if name not in by_name:
                by_name[name] = []
            by_name[name].append(f)
        
        duplicates = {k: v for k, v in by_name.items() if len(v) > 1}
        
        if duplicates:
            prompt = f"""以下文件可能是重复的:

"""
            for name, files_list in list(duplicates.items())[:5]:
                prompt += f"- {name}: {len(files_list)} 个版本\n"
            
            prompt += "\n请给出清理建议，哪些应该保留，哪些可以删除？用中文回答，50字以内。"
            return self.ask_ai(prompt)
        
        return "没有发现重复文件。"
        
    def run(self, path=None):
        """Run file organizer"""
        if not path:
            path = os.path.expanduser("~/Downloads")
        
        print("\n" + "="*70)
        print("🧹 MOMACLEANER - AI-POWERED FILE ORGANIZER")
        print("="*70)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🧠 Model: MiniMax-M2.5")
        print(f"📂 扫描路径: {path}")
        print("="*70)
        
        # Scan files
        print("\n📂 扫描文件...")
        files = self.scan_folder(path)
        
        print(f"   找到 {len(files)} 个文件")
        
        # Show categories
        by_category = {}
        for f in files:
            cat = self.categorize_file(f['path'])
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print("\n📊 文件分类:")
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            print(f"   - {cat}: {count}")
        
        # AI Analysis
        print("\n" + "="*70)
        print("🧠 AI 整理建议")
        print("="*70)
        
        analysis = self.analyze_with_ai(files)
        print(analysis)
        
        # Duplicate analysis
        print("\n" + "="*70)
        print("🔍 重复文件分析")
        print("="*70)
        
        dup_analysis = self.analyze_duplicate(files)
        print(dup_analysis)
        
        print("\n" + "="*70)


if __name__ == "__main__":
    cleaner = MomaCleanerAI()
    cleaner.run()
