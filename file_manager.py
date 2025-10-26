"""
File Manager for CodeMaster AI - Termux Edition
Provides file and directory management capabilities
"""

import os
import shutil
import json
import re
from pathlib import Path
from typing import List, Dict, Optional

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RED = '\033[31m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_RED = '\033[91m'

class FileManager:
    def __init__(self, base_directory: str = None):
        self.base_directory = Path(base_directory) if base_directory else Path.cwd()
        self.current_directory = self.base_directory
        
    def create_file(self, filepath: str, content: str = "", overwrite: bool = False) -> str:
        """Create a new file with content"""
        try:
            full_path = self.current_directory / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if full_path.exists() and not overwrite:
                return f"{Colors.YELLOW}⚠️  File already exists: {filepath}. Use overwrite=True to replace.{Colors.RESET}"
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"{Colors.BRIGHT_GREEN}✅ Created file: {filepath}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error creating file: {str(e)}{Colors.RESET}"
    
    def edit_file(self, filepath: str, content: str, mode: str = "replace") -> str:
        """Edit an existing file"""
        try:
            full_path = self.current_directory / filepath
            
            if not full_path.exists():
                return f"{Colors.YELLOW}⚠️  File doesn't exist: {filepath}. Creating new file.{Colors.RESET}\n" + self.create_file(filepath, content)
            
            if mode == "replace":
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                action = "Replaced content in"
            elif mode == "append":
                with open(full_path, 'a', encoding='utf-8') as f:
                    f.write(content)
                action = "Appended to"
            elif mode == "prepend":
                with open(full_path, 'r', encoding='utf-8') as f:
                    existing = f.read()
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content + existing)
                action = "Prepended to"
            
            return f"{Colors.BRIGHT_GREEN}✅ {action} file: {filepath}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error editing file: {str(e)}{Colors.RESET}"
    
    def read_file(self, filepath: str) -> str:
        """Read file content"""
        try:
            full_path = self.current_directory / filepath
            if not full_path.exists():
                return f"{Colors.YELLOW}⚠️  File doesn't exist: {filepath}{Colors.RESET}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return f"{Colors.BRIGHT_BLUE}📄 Content of {filepath}:{Colors.RESET}\n\n{content}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error reading file: {str(e)}{Colors.RESET}"
    
    def delete_file(self, filepath: str) -> str:
        """Delete a file"""
        try:
            full_path = self.current_directory / filepath
            if not full_path.exists():
                return f"{Colors.YELLOW}⚠️  File doesn't exist: {filepath}{Colors.RESET}"
            
            full_path.unlink()
            return f"{Colors.BRIGHT_GREEN}✅ Deleted file: {filepath}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error deleting file: {str(e)}{Colors.RESET}"
    
    def move_file(self, source: str, destination: str) -> str:
        """Move/rename a file"""
        try:
            src_path = self.current_directory / source
            dst_path = self.current_directory / destination
            
            if not src_path.exists():
                return f"{Colors.YELLOW}⚠️  Source file doesn't exist: {source}{Colors.RESET}"
            
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            
            return f"{Colors.BRIGHT_GREEN}✅ Moved {source} → {destination}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error moving file: {str(e)}{Colors.RESET}"
    
    def copy_file(self, source: str, destination: str) -> str:
        """Copy a file"""
        try:
            src_path = self.current_directory / source
            dst_path = self.current_directory / destination
            
            if not src_path.exists():
                return f"{Colors.YELLOW}⚠️  Source file doesn't exist: {source}{Colors.RESET}"
            
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src_path), str(dst_path))
            
            return f"{Colors.BRIGHT_GREEN}✅ Copied {source} → {destination}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error copying file: {str(e)}{Colors.RESET}"
    
    def create_directory(self, dirpath: str) -> str:
        """Create a directory"""
        try:
            full_path = self.current_directory / dirpath
            full_path.mkdir(parents=True, exist_ok=True)
            return f"{Colors.BRIGHT_GREEN}✅ Created directory: {dirpath}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error creating directory: {str(e)}{Colors.RESET}"
    
    def delete_directory(self, dirpath: str) -> str:
        """Delete a directory"""
        try:
            full_path = self.current_directory / dirpath
            if not full_path.exists():
                return f"{Colors.YELLOW}⚠️  Directory doesn't exist: {dirpath}{Colors.RESET}"
            
            shutil.rmtree(str(full_path))
            return f"{Colors.BRIGHT_GREEN}✅ Deleted directory: {dirpath}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error deleting directory: {str(e)}{Colors.RESET}"
    
    def list_directory(self, dirpath: str = ".") -> str:
        """List directory contents"""
        try:
            full_path = self.current_directory / dirpath
            if not full_path.exists():
                return f"{Colors.YELLOW}⚠️  Directory doesn't exist: {dirpath}{Colors.RESET}"
            
            items = []
            for item in sorted(full_path.iterdir()):
                if item.is_dir():
                    items.append(f"{Colors.BRIGHT_BLUE}📁 {item.name}/{Colors.RESET}")
                else:
                    size = item.stat().st_size
                    size_str = self._format_size(size)
                    items.append(f"{Colors.BRIGHT_CYAN}📄 {item.name} ({size_str}){Colors.RESET}")
            
            if not items:
                return f"{Colors.YELLOW}📂 Directory is empty: {dirpath}{Colors.RESET}"
            
            return f"{Colors.BRIGHT_MAGENTA}📂 Contents of {dirpath}:{Colors.RESET}\n" + "\n".join(items)
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error listing directory: {str(e)}{Colors.RESET}"
    
    def change_directory(self, dirpath: str) -> str:
        """Change current working directory"""
        try:
            if dirpath == "..":
                new_path = self.current_directory.parent
            elif dirpath == ".":
                new_path = self.current_directory
            else:
                new_path = self.current_directory / dirpath
            
            if not new_path.exists():
                return f"{Colors.YELLOW}⚠️  Directory doesn't exist: {dirpath}{Colors.RESET}"
            
            self.current_directory = new_path.resolve()
            return f"{Colors.BRIGHT_GREEN}✅ Changed directory to: {self.current_directory}{Colors.RESET}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error changing directory: {str(e)}{Colors.RESET}"
    
    def get_current_directory(self) -> str:
        """Get current working directory"""
        return f"{Colors.BRIGHT_CYAN}📍 Current directory: {self.current_directory}{Colors.RESET}"
    
    def find_files(self, pattern: str, directory: str = ".") -> str:
        """Find files matching a pattern"""
        try:
            search_path = self.current_directory / directory
            if not search_path.exists():
                return f"{Colors.YELLOW}⚠️  Directory doesn't exist: {directory}{Colors.RESET}"
            
            matches = []
            for item in search_path.rglob(pattern):
                if item.is_file():
                    relative_path = item.relative_to(self.current_directory)
                    matches.append(f"{Colors.BRIGHT_CYAN}📄 {relative_path}{Colors.RESET}")
            
            if not matches:
                return f"{Colors.YELLOW}🔍 No files found matching: {pattern}{Colors.RESET}"
            
            return f"{Colors.BRIGHT_MAGENTA}🔍 Files matching '{pattern}':{Colors.RESET}\n" + "\n".join(matches)
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error finding files: {str(e)}{Colors.RESET}"
    
    def _format_size(self, size: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def extract_code_from_response(self, response: str) -> List[Dict]:
        """Extract code blocks from AI response"""
        code_blocks = []
        
        # Find code blocks with language specification
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        for i, (language, code) in enumerate(matches):
            if not language:
                language = self._detect_language(code)
            
            code_blocks.append({
                'index': i,
                'language': language,
                'code': code.strip(),
                'suggested_filename': self._suggest_filename(code, language)
            })
        
        return code_blocks
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language from code"""
        code_lower = code.lower()
        
        if 'def ' in code or 'import ' in code or 'print(' in code:
            return 'python'
        elif 'function ' in code or 'const ' in code or 'console.log' in code:
            return 'javascript'
        elif '#include' in code or 'std::' in code:
            return 'cpp'
        elif 'public class' in code or 'System.out' in code:
            return 'java'
        elif '<html>' in code or '<!doctype' in code_lower:
            return 'html'
        elif any(prop in code for prop in ['color:', 'background:', 'margin:']):
            return 'css'
        
        return 'text'
    
    def _suggest_filename(self, code: str, language: str) -> str:
        """Suggest a filename based on code content"""
        # Try to find function/class names
        if language == 'python':
            class_match = re.search(r'class\s+(\w+)', code)
            if class_match:
                return f"{class_match.group(1).lower()}.py"
            
            func_match = re.search(r'def\s+(\w+)', code)
            if func_match:
                return f"{func_match.group(1).lower()}.py"
            
            return "script.py"
        
        elif language == 'javascript':
            func_match = re.search(r'function\s+(\w+)', code)
            if func_match:
                return f"{func_match.group(1).lower()}.js"
            return "script.js"
        
        elif language == 'html':
            return "index.html"
        
        elif language == 'css':
            return "styles.css"
        
        elif language == 'java':
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            if class_match:
                return f"{class_match.group(1)}.java"
            return "Main.java"
        
        elif language == 'cpp':
            return "main.cpp"
        
        return f"code.{language}"
    
    def save_code_blocks(self, response: str, directory: str = "generated_code") -> str:
        """Extract and save all code blocks from AI response"""
        code_blocks = self.extract_code_from_response(response)
        
        if not code_blocks:
            return f"{Colors.YELLOW}⚠️  No code blocks found in response{Colors.RESET}"
        
        # Create directory for generated code
        self.create_directory(directory)
        
        results = []
        for block in code_blocks:
            filename = f"{directory}/{block['suggested_filename']}"
            result = self.create_file(filename, block['code'], overwrite=True)
            results.append(f"  • {block['language'].upper()}: {filename}")
        
        return f"{Colors.BRIGHT_GREEN}💾 Saved {len(code_blocks)} code files:{Colors.RESET}\n" + "\n".join(results)
