"""
Code Formatter for CodeMaster AI - Termux Edition
Adds beautiful syntax highlighting and formatting for code blocks
"""

import re
from typing import Dict, List

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
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_DARK_GRAY = '\033[100m'
    BG_BLUE = '\033[44m'

class CodeFormatter:
    def __init__(self):
        self.language_keywords = {
            'python': ['def', 'class', 'import', 'from', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'return', 'yield', 'with', 'as', 'lambda', 'and', 'or', 'not', 'in', 'is'],
            'javascript': ['function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return', 'class', 'extends', 'import', 'export', 'async', 'await', 'try', 'catch'],
            'java': ['public', 'private', 'protected', 'class', 'interface', 'extends', 'implements', 'if', 'else', 'for', 'while', 'return', 'try', 'catch', 'finally'],
            'cpp': ['#include', 'using', 'namespace', 'class', 'struct', 'public', 'private', 'protected', 'if', 'else', 'for', 'while', 'return', 'try', 'catch'],
            'sql': ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'TABLE', 'INDEX', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER'],
            'html': ['<!DOCTYPE', '<html>', '<head>', '<body>', '<div>', '<span>', '<p>', '<h1>', '<h2>', '<h3>', '<script>', '<style>'],
            'css': ['color', 'background', 'margin', 'padding', 'border', 'width', 'height', 'display', 'position', 'font'],
        }
    
    def detect_language(self, code: str) -> str:
        """Detect programming language from code content"""
        code_lower = code.lower()
        
        # Check for specific patterns
        if 'def ' in code or 'import ' in code or 'print(' in code:
            return 'python'
        elif 'function ' in code or 'const ' in code or 'console.log' in code:
            return 'javascript'
        elif '#include' in code or 'std::' in code or 'cout' in code:
            return 'cpp'
        elif 'public class' in code or 'System.out' in code:
            return 'java'
        elif 'select ' in code_lower or 'from ' in code_lower:
            return 'sql'
        elif '<html>' in code or '<!doctype' in code_lower:
            return 'html'
        elif any(prop in code for prop in ['color:', 'background:', 'margin:']):
            return 'css'
        
        return 'text'
    
    def highlight_syntax(self, code: str, language: str) -> str:
        """Add syntax highlighting to code"""
        if language not in self.language_keywords:
            return code
        
        highlighted = code
        keywords = self.language_keywords[language]
        
        # Highlight keywords
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            highlighted = re.sub(pattern, f'{Colors.BRIGHT_BLUE}{keyword}{Colors.RESET}', highlighted, flags=re.IGNORECASE)
        
        # Highlight strings
        highlighted = re.sub(r'"([^"]*)"', f'{Colors.BRIGHT_GREEN}"\\1"{Colors.RESET}', highlighted)
        highlighted = re.sub(r"'([^']*)'", f"{Colors.BRIGHT_GREEN}'\\1'{Colors.RESET}", highlighted)
        
        # Highlight comments
        if language in ['python', 'bash']:
            highlighted = re.sub(r'#.*$', f'{Colors.DIM}\\g<0>{Colors.RESET}', highlighted, flags=re.MULTILINE)
        elif language in ['javascript', 'java', 'cpp']:
            highlighted = re.sub(r'//.*$', f'{Colors.DIM}\\g<0>{Colors.RESET}', highlighted, flags=re.MULTILINE)
            highlighted = re.sub(r'/\*.*?\*/', f'{Colors.DIM}\\g<0>{Colors.RESET}', highlighted, flags=re.DOTALL)
        
        # Highlight numbers
        highlighted = re.sub(r'\b\d+\.?\d*\b', f'{Colors.BRIGHT_YELLOW}\\g<0>{Colors.RESET}', highlighted)
        
        return highlighted
    
    def format_code_block(self, code: str, language: str = None) -> str:
        """Format a code block with beautiful styling"""
        if not language:
            language = self.detect_language(code)
        
        # Clean the code
        code = code.strip()
        lines = code.split('\n')
        
        # Apply syntax highlighting
        highlighted_code = self.highlight_syntax(code, language)
        highlighted_lines = highlighted_code.split('\n')
        
        # Create the formatted output
        result = []
        
        # Top border with language indicator
        lang_display = language.upper() if language != 'text' else 'CODE'
        border_length = max(60, len(max(lines, key=len)) + 10)
        
        result.append(f"{Colors.BRIGHT_CYAN}╭{'─' * (border_length - 2)}╮{Colors.RESET}")
        result.append(f"{Colors.BRIGHT_CYAN}│{Colors.BRIGHT_WHITE} 💻 {lang_display} CODE {Colors.BRIGHT_CYAN}{' ' * (border_length - len(lang_display) - 12)}│{Colors.RESET}")
        result.append(f"{Colors.BRIGHT_CYAN}├{'─' * (border_length - 2)}┤{Colors.RESET}")
        
        # Code lines with line numbers
        for i, line in enumerate(highlighted_lines, 1):
            line_num = f"{i:3d}"
            padding = ' ' * (border_length - len(line) - 8)
            if len(line) > border_length - 8:
                padding = ''
            result.append(f"{Colors.BRIGHT_CYAN}│{Colors.DIM}{line_num}{Colors.RESET} {line}{padding}{Colors.BRIGHT_CYAN}│{Colors.RESET}")
        
        # Bottom border
        result.append(f"{Colors.BRIGHT_CYAN}╰{'─' * (border_length - 2)}╯{Colors.RESET}")
        
        return '\n'.join(result)
    
    def format_response(self, response: str) -> str:
        """Format AI response with code blocks highlighted"""
        # Find code blocks (```language\ncode\n```)
        code_block_pattern = r'```(\w+)?\n(.*?)\n```'
        
        def replace_code_block(match):
            language = match.group(1) or 'text'
            code = match.group(2)
            return self.format_code_block(code, language)
        
        # Replace code blocks
        formatted = re.sub(code_block_pattern, replace_code_block, response, flags=re.DOTALL)
        
        # Find inline code (`code`)
        inline_code_pattern = r'`([^`]+)`'
        formatted = re.sub(inline_code_pattern, f'{Colors.BG_DARK_GRAY}{Colors.BRIGHT_WHITE} \\1 {Colors.RESET}', formatted)
        
        # Add chat styling for non-code parts
        lines = formatted.split('\n')
        result_lines = []
        
        for line in lines:
            # Skip lines that are part of code blocks
            if ('╭' in line or '╰' in line or '├' in line or '│' in line) and Colors.BRIGHT_CYAN in line:
                result_lines.append(line)
            elif line.strip():
                # Regular chat line - add subtle styling
                result_lines.append(f"{Colors.BRIGHT_WHITE}{line}{Colors.RESET}")
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def format_chat_message(self, message: str) -> str:
        """Format a regular chat message"""
        return f"{Colors.BRIGHT_WHITE}{message}{Colors.RESET}"
    
    def create_section_header(self, title: str, icon: str = "💬") -> str:
        """Create a beautiful section header"""
        border_length = max(50, len(title) + 10)
        return f"""
{Colors.BRIGHT_MAGENTA}╭{'─' * (border_length - 2)}╮{Colors.RESET}
{Colors.BRIGHT_MAGENTA}│{Colors.BRIGHT_WHITE} {icon} {title} {Colors.BRIGHT_MAGENTA}{' ' * (border_length - len(title) - 6)}│{Colors.RESET}
{Colors.BRIGHT_MAGENTA}╰{'─' * (border_length - 2)}╯{Colors.RESET}
"""
