"""
Advanced File Operations with Animations for CodeMaster AI - Termux Edition
Provides real-time file system access with visual feedback
"""

import os
import time
import threading
from pathlib import Path
from typing import List, Dict, Optional

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

class FileOperationAnimation:
    def __init__(self):
        self.is_running = False
        self.animation_thread = None
    
    def start_animation(self, operation: str, filename: str = ""):
        """Start an animation for file operations"""
        self.is_running = True
        self.animation_thread = threading.Thread(
            target=self._animate, 
            args=(operation, filename)
        )
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def stop_animation(self):
        """Stop the current animation"""
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join(timeout=1)
        print()  # New line after animation
    
    def _animate(self, operation: str, filename: str):
        """Animation loop"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        operations = {
            'reading': f'{Colors.BRIGHT_BLUE}📖 Reading',
            'writing': f'{Colors.BRIGHT_GREEN}✍️  Writing',
            'creating': f'{Colors.BRIGHT_YELLOW}📝 Creating',
            'editing': f'{Colors.BRIGHT_CYAN}✏️  Editing',
            'deleting': f'{Colors.BRIGHT_RED}🗑️  Deleting',
            'moving': f'{Colors.BRIGHT_MAGENTA}📦 Moving',
            'analyzing': f'{Colors.BRIGHT_WHITE}🔍 Analyzing'
        }
        
        op_text = operations.get(operation, f'{Colors.WHITE}⚙️  Processing')
        
        i = 0
        while self.is_running:
            frame = frames[i % len(frames)]
            if filename:
                print(f'\r{op_text} {filename} {Colors.YELLOW}{frame}{Colors.RESET}', end='', flush=True)
            else:
                print(f'\r{op_text} {Colors.YELLOW}{frame}{Colors.RESET}', end='', flush=True)
            time.sleep(0.1)
            i += 1

class AdvancedFileManager:
    def __init__(self, base_directory: str = None):
        self.base_directory = Path(base_directory) if base_directory else Path.cwd()
        self.current_directory = self.base_directory
        self.animation = FileOperationAnimation()
        self.operation_log = []
    
    def log_operation(self, operation: str):
        """Log file operations"""
        timestamp = time.strftime("%H:%M:%S")
        self.operation_log.append(f"[{timestamp}] {operation}")
        print(f"{Colors.DIM}[{timestamp}] {operation}{Colors.RESET}")
    
    def read_file_with_animation(self, filepath: str) -> str:
        """Read file with animation"""
        try:
            full_path = self.current_directory / filepath
            
            self.animation.start_animation('reading', filepath)
            time.sleep(0.5)  # Simulate reading time
            
            if not full_path.exists():
                self.animation.stop_animation()
                self.log_operation(f"❌ File not found: {filepath}")
                return f"{Colors.YELLOW}⚠️  File doesn't exist: {filepath}{Colors.RESET}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.animation.stop_animation()
            self.log_operation(f"✅ Successfully read {filepath} ({len(content)} chars)")
            
            return f"{Colors.BRIGHT_BLUE}📄 Content of {filepath}:{Colors.RESET}\n\n{content}"
        except Exception as e:
            self.animation.stop_animation()
            self.log_operation(f"❌ Error reading {filepath}: {str(e)}")
            return f"{Colors.BRIGHT_RED}❌ Error reading file: {str(e)}{Colors.RESET}"
    
    def write_file_with_animation(self, filepath: str, content: str, mode: str = "w") -> str:
        """Write file with animation"""
        try:
            full_path = self.current_directory / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            operation = 'creating' if mode == 'w' and not full_path.exists() else 'editing'
            self.animation.start_animation(operation, filepath)
            
            # Simulate writing with progressive animation
            lines = content.split('\n')
            with open(full_path, mode, encoding='utf-8') as f:
                for i, line in enumerate(lines):
                    f.write(line + '\n')
                    if i % 10 == 0:  # Update animation every 10 lines
                        time.sleep(0.05)
            
            self.animation.stop_animation()
            action = "Created" if operation == 'creating' else "Updated"
            self.log_operation(f"✅ {action} {filepath} ({len(lines)} lines)")
            
            return f"{Colors.BRIGHT_GREEN}✅ {action} file: {filepath}{Colors.RESET}"
        except Exception as e:
            self.animation.stop_animation()
            self.log_operation(f"❌ Error writing {filepath}: {str(e)}")
            return f"{Colors.BRIGHT_RED}❌ Error writing file: {str(e)}{Colors.RESET}"
    
    def delete_file_with_animation(self, filepath: str) -> str:
        """Delete file with animation"""
        try:
            full_path = self.current_directory / filepath
            
            if not full_path.exists():
                self.log_operation(f"⚠️  File not found: {filepath}")
                return f"{Colors.YELLOW}⚠️  File doesn't exist: {filepath}{Colors.RESET}"
            
            self.animation.start_animation('deleting', filepath)
            time.sleep(0.3)  # Dramatic pause
            
            full_path.unlink()
            
            self.animation.stop_animation()
            self.log_operation(f"🗑️  Deleted {filepath}")
            
            return f"{Colors.BRIGHT_GREEN}✅ Deleted file: {filepath}{Colors.RESET}"
        except Exception as e:
            self.animation.stop_animation()
            self.log_operation(f"❌ Error deleting {filepath}: {str(e)}")
            return f"{Colors.BRIGHT_RED}❌ Error deleting file: {str(e)}{Colors.RESET}"
    
    def move_file_with_animation(self, source: str, destination: str) -> str:
        """Move file with animation"""
        try:
            src_path = self.current_directory / source
            dst_path = self.current_directory / destination
            
            if not src_path.exists():
                self.log_operation(f"⚠️  Source file not found: {source}")
                return f"{Colors.YELLOW}⚠️  Source file doesn't exist: {source}{Colors.RESET}"
            
            self.animation.start_animation('moving', f"{source} → {destination}")
            time.sleep(0.4)
            
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            src_path.rename(dst_path)
            
            self.animation.stop_animation()
            self.log_operation(f"📦 Moved {source} → {destination}")
            
            return f"{Colors.BRIGHT_GREEN}✅ Moved {source} → {destination}{Colors.RESET}"
        except Exception as e:
            self.animation.stop_animation()
            self.log_operation(f"❌ Error moving {source}: {str(e)}")
            return f"{Colors.BRIGHT_RED}❌ Error moving file: {str(e)}{Colors.RESET}"
    
    def analyze_directory_with_animation(self, directory: str = ".") -> str:
        """Analyze directory structure with animation"""
        try:
            target_path = self.current_directory / directory
            
            if not target_path.exists():
                self.log_operation(f"⚠️  Directory not found: {directory}")
                return f"{Colors.YELLOW}⚠️  Directory doesn't exist: {directory}{Colors.RESET}"
            
            self.animation.start_animation('analyzing', directory)
            time.sleep(0.6)
            
            # Analyze directory
            files = []
            dirs = []
            total_size = 0
            
            for item in target_path.rglob('*'):
                if item.is_file():
                    size = item.stat().st_size
                    total_size += size
                    files.append({
                        'name': str(item.relative_to(target_path)),
                        'size': size,
                        'ext': item.suffix
                    })
                elif item.is_dir():
                    dirs.append(str(item.relative_to(target_path)))
            
            self.animation.stop_animation()
            self.log_operation(f"🔍 Analyzed {directory}: {len(files)} files, {len(dirs)} directories")
            
            # Format results
            result = f"{Colors.BRIGHT_MAGENTA}📊 Directory Analysis: {directory}{Colors.RESET}\n"
            result += f"{Colors.CYAN}📁 Directories: {len(dirs)}{Colors.RESET}\n"
            result += f"{Colors.CYAN}📄 Files: {len(files)}{Colors.RESET}\n"
            result += f"{Colors.CYAN}💾 Total Size: {self._format_size(total_size)}{Colors.RESET}\n\n"
            
            # Show file types
            extensions = {}
            for file in files:
                ext = file['ext'] or 'no extension'
                extensions[ext] = extensions.get(ext, 0) + 1
            
            if extensions:
                result += f"{Colors.BRIGHT_YELLOW}📋 File Types:{Colors.RESET}\n"
                for ext, count in sorted(extensions.items()):
                    result += f"  {Colors.YELLOW}•{Colors.RESET} {ext}: {count} files\n"
            
            return result
        except Exception as e:
            self.animation.stop_animation()
            self.log_operation(f"❌ Error analyzing {directory}: {str(e)}")
            return f"{Colors.BRIGHT_RED}❌ Error analyzing directory: {str(e)}{Colors.RESET}"
    
    def create_project_structure_with_animation(self, project_name: str, structure: Dict) -> str:
        """Create a complete project structure with animation"""
        try:
            project_path = self.current_directory / project_name
            
            self.animation.start_animation('creating', f"project {project_name}")
            
            # Create project directory
            project_path.mkdir(exist_ok=True)
            self.log_operation(f"📁 Created project directory: {project_name}")
            
            # Create structure recursively
            self._create_structure_recursive(project_path, structure)
            
            self.animation.stop_animation()
            self.log_operation(f"🎉 Project {project_name} created successfully!")
            
            return f"{Colors.BRIGHT_GREEN}🎉 Created project: {project_name}{Colors.RESET}"
        except Exception as e:
            self.animation.stop_animation()
            self.log_operation(f"❌ Error creating project {project_name}: {str(e)}")
            return f"{Colors.BRIGHT_RED}❌ Error creating project: {str(e)}{Colors.RESET}"
    
    def _create_structure_recursive(self, base_path: Path, structure: Dict):
        """Recursively create directory structure"""
        for name, content in structure.items():
            item_path = base_path / name
            
            if isinstance(content, dict):
                # It's a directory
                item_path.mkdir(exist_ok=True)
                self.log_operation(f"📁 Created directory: {item_path.relative_to(self.current_directory)}")
                self._create_structure_recursive(item_path, content)
            else:
                # It's a file
                with open(item_path, 'w', encoding='utf-8') as f:
                    f.write(content or "")
                self.log_operation(f"📄 Created file: {item_path.relative_to(self.current_directory)}")
                time.sleep(0.1)  # Small delay for visual effect
    
    def get_operation_log(self) -> str:
        """Get recent operations log"""
        if not self.operation_log:
            return f"{Colors.DIM}No operations performed yet{Colors.RESET}"
        
        recent_ops = self.operation_log[-10:]  # Last 10 operations
        result = f"{Colors.BRIGHT_CYAN}📋 Recent Operations:{Colors.RESET}\n"
        for op in recent_ops:
            result += f"{op}\n"
        
        return result
    
    def _format_size(self, size: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    
    def change_directory_with_feedback(self, path: str) -> str:
        """Change directory with feedback"""
        try:
            if path == "..":
                new_path = self.current_directory.parent
            elif path == ".":
                new_path = self.current_directory
            else:
                new_path = self.current_directory / path
            
            if not new_path.exists():
                self.log_operation(f"⚠️  Directory not found: {path}")
                return f"{Colors.YELLOW}⚠️  Directory doesn't exist: {path}{Colors.RESET}"
            
            self.current_directory = new_path.resolve()
            self.log_operation(f"📍 Changed to: {self.current_directory}")
            
            return f"{Colors.BRIGHT_GREEN}📍 Now in: {self.current_directory}{Colors.RESET}"
        except Exception as e:
            self.log_operation(f"❌ Error changing directory: {str(e)}")
            return f"{Colors.BRIGHT_RED}❌ Error changing directory: {str(e)}{Colors.RESET}"
