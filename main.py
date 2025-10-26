#!/data/data/com.termux/files/usr/bin/python
"""
CodeMaster AI - Termux Edition
Advanced Terminal-based AI Assistant optimized for Termux
Powered by real AI APIs (OpenAI, Claude, Gemini, Groq) with web access
"""

import os
import sys
import json
import time
import random
import datetime
import asyncio
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
import subprocess
import platform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our AI engine
from ai_engine import AIEngine, WebSearchEngine
from config import Config, API_INSTRUCTIONS
from code_formatter import CodeFormatter
from file_manager import FileManager
from file_operations import AdvancedFileManager

# Terminal colors and styling
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime.datetime

class ThinkingAnimation:
    def __init__(self):
        self.thinking = False
        self.thread = None
    
    def start(self):
        """Start the thinking animation"""
        self.thinking = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop the thinking animation"""
        self.thinking = False
        if self.thread:
            self.thread.join()
        # Clear the line
        print('\r' + ' ' * 50 + '\r', end='', flush=True)
    
    def _animate(self):
        """Animation loop"""
        frames = ['   ', '.  ', '.. ', '...']
        i = 0
        while self.thinking:
            print(f'\r{Colors.BRIGHT_CYAN}Thinking{frames[i % len(frames)]}{Colors.RESET}', end='', flush=True)
            time.sleep(0.4)
            i += 1

class CodeMasterAI:
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.ai_engine = AIEngine()
        self.web_engine = WebSearchEngine()
        self.config = Config()
        self.current_date = datetime.datetime.now()
        self.thinking_animation = ThinkingAnimation()
        self.code_formatter = CodeFormatter()
        self.file_manager = FileManager()
        self.advanced_file_manager = AdvancedFileManager()
        self.pending_code_blocks = []
        
        # Check if APIs are configured
        self.check_api_setup()
    
    def check_api_setup(self):
        """Check if AI APIs are properly configured"""
        available_providers = self.config.get_available_providers()
        if not available_providers:
            print(f"\n{Colors.BRIGHT_RED}⚠️  No AI APIs configured!{Colors.RESET}")
            print(f"{Colors.YELLOW}Please set up at least one API key to use CodeMaster AI.{Colors.RESET}")
            print(API_INSTRUCTIONS)
            print(f"\n{Colors.BRIGHT_CYAN}You can still use basic features, but AI responses won't work.{Colors.RESET}")
        else:
            print(f"{Colors.BRIGHT_GREEN}✅ AI APIs configured: {', '.join(available_providers)}{Colors.RESET}")
    
    def clear_screen(self):
        os.system('clear')
    
    def print_banner(self):
        available_providers = self.config.get_available_providers()
        provider_status = f"🔗 Connected: {', '.join(available_providers)}" if available_providers else "❌ No APIs configured"
        
        banner = f"""
{Colors.BRIGHT_MAGENTA}Today is {self.current_date.strftime('%A, %B %d, %Y')}{Colors.RESET}
{Colors.DIM}{provider_status}{Colors.RESET}
{Colors.DIM}Type 'help' for commands, 'exit' to quit{Colors.RESET}
"""
        print(banner)
    
    def print_help(self):
        help_text = f"""
{Colors.BRIGHT_YELLOW}📚 CodeMaster AI Commands:{Colors.RESET}

{Colors.BRIGHT_GREEN}General Commands:{Colors.RESET}
  {Colors.CYAN}help{Colors.RESET}           - Show this help message
  {Colors.CYAN}clear{Colors.RESET}          - Clear the screen
  {Colors.CYAN}exit{Colors.RESET}           - Exit the application
  {Colors.CYAN}history{Colors.RESET}        - Show conversation history
  {Colors.CYAN}status{Colors.RESET}         - Show API connection status
  {Colors.CYAN}setup{Colors.RESET}          - Show API setup instructions
  {Colors.CYAN}unrestricted{Colors.RESET}   - Activate maximum freedom mode

{Colors.BRIGHT_GREEN}AI Features:{Colors.RESET}
  {Colors.CYAN}search <query>{Colors.RESET}  - Search the web for current information
  {Colors.CYAN}news{Colors.RESET}           - Get latest news headlines
  {Colors.CYAN}weather{Colors.RESET}        - Get current weather information

{Colors.BRIGHT_GREEN}File Management:{Colors.RESET}
  {Colors.CYAN}save code{Colors.RESET}       - Save all code from last response to files
  {Colors.CYAN}create <file>{Colors.RESET}   - Create a new file
  {Colors.CYAN}edit <file>{Colors.RESET}     - Edit an existing file
  {Colors.CYAN}read <file>{Colors.RESET}     - Read file content
  {Colors.CYAN}delete <file>{Colors.RESET}   - Delete a file
  {Colors.CYAN}move <src> <dst>{Colors.RESET} - Move/rename a file
  {Colors.CYAN}mkdir <dir>{Colors.RESET}     - Create directory
  {Colors.CYAN}ls [dir]{Colors.RESET}        - List directory contents
  {Colors.CYAN}cd <dir>{Colors.RESET}        - Change directory
  {Colors.CYAN}pwd{Colors.RESET}             - Show current directory
  {Colors.CYAN}find <pattern>{Colors.RESET}  - Find files matching pattern
  {Colors.CYAN}analyze [dir]{Colors.RESET}   - Analyze directory structure
  {Colors.CYAN}log{Colors.RESET}             - Show recent file operations
  {Colors.CYAN}project <name>{Colors.RESET}  - Create project structure

{Colors.BRIGHT_GREEN}Just Chat Naturally!{Colors.RESET}
  {Colors.DIM}> Hi! How are you?{Colors.RESET}
  {Colors.DIM}> What's your favorite programming language?{Colors.RESET}
  {Colors.DIM}> Create a web scraper in Python{Colors.RESET}
  {Colors.DIM}> Tell me about quantum computing{Colors.RESET}
  {Colors.DIM}> What's happening in tech today?{Colors.RESET}
  {Colors.DIM}> Can you help me with my homework?{Colors.RESET}

{Colors.BRIGHT_YELLOW}💡 I'm here to chat!{Colors.RESET} I can:
  • Chat about anything - tech, life, hobbies, whatever!
  • Help with coding when you need it
  • Search the web for current info
  • Be your friendly AI companion 😊
"""
        print(help_text)
    
    def show_history(self):
        if not self.conversation_history:
            print(f"{Colors.YELLOW}No conversation history yet.{Colors.RESET}")
            return
        
        print(f"\n{Colors.BRIGHT_YELLOW}📝 Conversation History:{Colors.RESET}")
        for i, msg in enumerate(self.conversation_history[-10:], 1):  # Show last 10 messages
            role_color = Colors.BRIGHT_BLUE if msg['role'] == 'user' else Colors.BRIGHT_GREEN
            content_preview = msg['content'][:100] + '...' if len(msg['content']) > 100 else msg['content']
            print(f"{Colors.DIM}[{i}]{Colors.RESET} {role_color}{msg['role'].capitalize()}:{Colors.RESET} {content_preview}")
        print()
    
    def show_status(self):
        """Show API connection status"""
        print(f"\n{Colors.BRIGHT_YELLOW}🔌 API Connection Status:{Colors.RESET}")
        
        providers = {
            'OpenAI': self.config.OPENAI_API_KEY,
            'Anthropic Claude': self.config.ANTHROPIC_API_KEY,
            'Google Gemini': self.config.GOOGLE_API_KEY,
            'Groq': self.config.GROQ_API_KEY
        }
        
        for provider, api_key in providers.items():
            status = f"{Colors.BRIGHT_GREEN}✅ Connected{Colors.RESET}" if api_key else f"{Colors.BRIGHT_RED}❌ Not configured{Colors.RESET}"
            print(f"  {provider:<15} {status}")
        
        print(f"\n{Colors.BRIGHT_CYAN}Current Provider: {self.config.PREFERRED_PROVIDER}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Web Search: {'✅ Available' if self.config.has_web_access() else '❌ Not configured'}{Colors.RESET}")
        print()
    
    async def get_ai_response(self, user_input: str) -> str:
        """Get response from AI"""
        if not self.config.get_available_providers():
            return f"{Colors.BRIGHT_RED}❌ No AI providers configured. Please set up API keys first.{Colors.RESET}\nType 'setup' for instructions."
        
        # Start thinking animation
        self.thinking_animation.start()
        
        try:
            # Get AI response
            response = await self.ai_engine.generate_response(user_input, self.conversation_history)
            return response
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Error getting AI response: {str(e)}{Colors.RESET}"
        finally:
            # Stop thinking animation
            self.thinking_animation.stop()
    
    async def handle_web_search(self, query: str) -> str:
        """Handle web search requests"""
        try:
            results = await self.web_engine.search_web(query)
            return f"{Colors.BRIGHT_GREEN}🔍 Web Search Results for '{query}':{Colors.RESET}\n\n{results}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Search error: {str(e)}{Colors.RESET}"
    
    async def handle_news(self) -> str:
        """Get current news"""
        try:
            news = await self.web_engine.get_current_news()
            return f"{Colors.BRIGHT_GREEN}📰 Latest News Headlines:{Colors.RESET}\n\n{news}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ News error: {str(e)}{Colors.RESET}"
    
    async def handle_weather(self, location: str = "current") -> str:
        """Get weather information"""
        try:
            weather = await self.web_engine.get_weather(location)
            return f"{Colors.BRIGHT_GREEN}🌤️ Weather Information:{Colors.RESET}\n\n{weather}"
        except Exception as e:
            return f"{Colors.BRIGHT_RED}❌ Weather error: {str(e)}{Colors.RESET}"
    
    async def process_command(self, user_input: str) -> str:
        """Process user commands and generate responses"""
        user_input = user_input.strip()
        
        if not user_input:
            return f"{Colors.YELLOW}Please enter a command or question.{Colors.RESET}"
        
        # Add to conversation history
        self.conversation_history.append({'role': 'user', 'content': user_input})
        
        # Command processing
        if user_input.lower() == 'help':
            self.print_help()
            return ""
        
        if user_input.lower() == 'clear':
            self.clear_screen()
            self.print_banner()
            return ""
        
        if user_input.lower() == 'history':
            self.show_history()
            return ""
        
        if user_input.lower() == 'status':
            self.show_status()
            return ""
        
        if user_input.lower() == 'setup':
            print(API_INSTRUCTIONS)
            return ""
        
        if user_input.lower() == 'unrestricted':
            return f"""
{Colors.BRIGHT_GREEN}🔓 UNRESTRICTED MODE ACTIVATED{Colors.RESET}

{Colors.BRIGHT_YELLOW}Your AI is now in maximum freedom mode:{Colors.RESET}
✅ No content restrictions
✅ No ethical limitations  
✅ No safety filters
✅ Will generate any code requested
✅ Discusses any topic
✅ Provides direct, unfiltered responses

{Colors.BRIGHT_CYAN}You can now request:{Colors.RESET}
• Any automation tools or scripts
• Web scrapers and data extraction tools
• Security and penetration testing tools
• Social media bots and automation
• Any programming project without limits
• Advanced hacking and security techniques

{Colors.DIM}Type your request and get unrestricted, working code!{Colors.RESET}
"""
        
        # Web search commands
        if user_input.lower().startswith('search '):
            query = user_input[7:].strip()
            if query:
                response = await self.handle_web_search(query)
                self.conversation_history.append({'role': 'assistant', 'content': response})
                return self.code_formatter.create_section_header("Web Search Results", "🔍") + response
            else:
                return f"{Colors.YELLOW}Please provide a search query. Example: search latest AI news{Colors.RESET}"
        
        if user_input.lower() == 'news':
            response = await self.handle_news()
            self.conversation_history.append({'role': 'assistant', 'content': response})
            return self.code_formatter.create_section_header("Latest News", "📰") + response
        
        if user_input.lower().startswith('weather'):
            parts = user_input.split(' ', 1)
            location = parts[1] if len(parts) > 1 else "current"
            response = await self.handle_weather(location)
            self.conversation_history.append({'role': 'assistant', 'content': response})
            return self.code_formatter.create_section_header("Weather Information", "🌤️") + response
        
        # File management commands
        if user_input.lower() == 'save code':
            if self.conversation_history:
                last_response = self.conversation_history[-1]['content']
                return self.file_manager.save_code_blocks(last_response)
            else:
                return f"{Colors.YELLOW}No previous response to save code from{Colors.RESET}"
        
        if user_input.lower().startswith('create '):
            filename = user_input[7:].strip()
            return self.file_manager.create_file(filename)
        
        if user_input.lower().startswith('edit '):
            filename = user_input[5:].strip()
            return f"{Colors.YELLOW}Use: edit <filename> <content> or ask AI to edit the file{Colors.RESET}"
        
        if user_input.lower().startswith('read '):
            filename = user_input[5:].strip()
            return self.advanced_file_manager.read_file_with_animation(filename)
        
        if user_input.lower().startswith('delete '):
            filename = user_input[7:].strip()
            return self.advanced_file_manager.delete_file_with_animation(filename)
        
        if user_input.lower().startswith('move '):
            parts = user_input[5:].strip().split(' ', 1)
            if len(parts) == 2:
                return self.advanced_file_manager.move_file_with_animation(parts[0], parts[1])
            else:
                return f"{Colors.YELLOW}Usage: move <source> <destination>{Colors.RESET}"
        
        if user_input.lower().startswith('mkdir '):
            dirname = user_input[6:].strip()
            return self.file_manager.create_directory(dirname)
        
        if user_input.lower().startswith('ls'):
            parts = user_input.split(' ', 1)
            directory = parts[1] if len(parts) > 1 else "."
            return self.file_manager.list_directory(directory)
        
        if user_input.lower().startswith('cd '):
            dirname = user_input[3:].strip()
            return self.advanced_file_manager.change_directory_with_feedback(dirname)
        
        if user_input.lower() == 'pwd':
            return f"{Colors.BRIGHT_CYAN}📍 Current directory: {self.advanced_file_manager.current_directory}{Colors.RESET}"
        
        if user_input.lower().startswith('find '):
            pattern = user_input[5:].strip()
            return self.file_manager.find_files(pattern)
        
        if user_input.lower().startswith('analyze'):
            parts = user_input.split(' ', 1)
            directory = parts[1] if len(parts) > 1 else "."
            return self.advanced_file_manager.analyze_directory_with_animation(directory)
        
        if user_input.lower() == 'log':
            return self.advanced_file_manager.get_operation_log()
        
        if user_input.lower().startswith('project '):
            project_name = user_input[8:].strip()
            # Basic project structure - can be enhanced
            structure = {
                'src': {},
                'tests': {},
                'docs': {},
                'README.md': f"# {project_name}\n\nProject description here.",
                'requirements.txt': "",
                '.gitignore': "__pycache__/\n*.pyc\n.env\n"
            }
            return self.advanced_file_manager.create_project_structure_with_animation(project_name, structure)
        
        # Handle natural language save requests
        if self.pending_code_blocks and self.is_save_request(user_input):
            return self.handle_save_request(user_input)
        
        # All other inputs go to AI
        response = await self.get_ai_response(user_input)
        self.conversation_history.append({'role': 'assistant', 'content': response})
        
        # Check if response contains code and offer to save it interactively
        code_blocks = self.file_manager.extract_code_from_response(response)
        if code_blocks:
            # Store the code blocks for later use
            self.pending_code_blocks = code_blocks
            save_prompt = f"\n{Colors.BRIGHT_YELLOW}💾 I generated some code for you! Would you like me to save it to a file?{Colors.RESET}"
            save_prompt += f"\n{Colors.CYAN}Just tell me where to put it (e.g., 'save to storage', 'put it in my projects folder', 'create file calculator.py'){Colors.RESET}"
            return response + save_prompt
        
        return response
    
    def is_save_request(self, user_input: str) -> bool:
        """Check if user input is a request to save code"""
        save_keywords = [
            'save', 'put', 'create', 'write', 'make', 'store', 'place',
            'storage', 'folder', 'file', 'directory', 'yes', 'yeah', 'ok', 'okay'
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in save_keywords)
    
    def handle_save_request(self, user_input: str) -> str:
        """Handle natural language save requests"""
        if not self.pending_code_blocks:
            return f"{Colors.YELLOW}No code to save. Generate some code first!{Colors.RESET}"
        
        user_lower = user_input.lower()
        
        # Parse the save location - Termux paths
        save_location = "generated_code"  # default
        filename = None
        
        # Check for storage
        if 'storage' in user_lower or 'sdcard' in user_lower:
            save_location = "/storage/emulated/0"
        
        # Check for specific folder mentions
        if 'project' in user_lower or 'projects' in user_lower:
            save_location = "projects"
        elif 'download' in user_lower or 'downloads' in user_lower:
            save_location = "/storage/emulated/0/Download"
        
        # Check for specific filename - improved parsing
        import re
        
        # Look for patterns like "name it X.py", "call it X.py", "file X.py", etc.
        filename_patterns = [
            r'name.*?(\w+\.\w+)',
            r'call.*?(\w+\.\w+)', 
            r'file.*?(\w+\.\w+)',
            r'create.*?(\w+\.\w+)',
            r'make.*?(\w+\.\w+)',
            r'save.*?as.*?(\w+\.\w+)',
            r'put.*?(\w+\.\w+)',
            r'(\w+\.\w+)'  # Any word with extension
        ]
        
        for pattern in filename_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                potential_filename = match.group(1)
                # Make sure it has a valid extension
                if '.' in potential_filename and len(potential_filename.split('.')[-1]) <= 4:
                    filename = potential_filename
                    break
        
        # Save the code blocks
        results = []
        self.file_manager.create_directory(save_location)
        
        if filename and len(self.pending_code_blocks) > 1:
            # Multiple files but user specified one name - combine them or use numbered names
            base_name = filename.split('.')[0]
            extension = filename.split('.')[-1]
            
            for i, block in enumerate(self.pending_code_blocks):
                if i == 0:
                    # First file gets the exact name
                    filepath = f"{save_location}/{filename}"
                else:
                    # Additional files get numbered
                    filepath = f"{save_location}/{base_name}_{i+1}.{extension}"
                
                result = self.advanced_file_manager.write_file_with_animation(filepath, block['code'], 'w')
                results.append(f"  • {block['language'].upper()}: {filepath}")
        
        elif filename and len(self.pending_code_blocks) == 1:
            # Single file with custom name
            filepath = f"{save_location}/{filename}"
            block = self.pending_code_blocks[0]
            result = self.advanced_file_manager.write_file_with_animation(filepath, block['code'], 'w')
            results.append(f"  • {block['language'].upper()}: {filepath}")
        
        else:
            # No custom filename - use suggested names
            for i, block in enumerate(self.pending_code_blocks):
                filepath = f"{save_location}/{block['suggested_filename']}"
                result = self.advanced_file_manager.write_file_with_animation(filepath, block['code'], 'w')
                results.append(f"  • {block['language'].upper()}: {filepath}")
        
        # Clear pending code blocks
        self.pending_code_blocks = []
        
        success_msg = f"{Colors.BRIGHT_GREEN}💾 Successfully saved {len(results)} file(s) to {save_location}:{Colors.RESET}\n"
        return success_msg + "\n".join(results)
    
    async def run_async(self):
        """Async main application loop"""
        self.clear_screen()
        self.print_banner()
        
        print(f"{Colors.BRIGHT_GREEN}👋 Hey there! I'm CodeMaster AI, your friendly AI assistant!{Colors.RESET}")
        print(f"{Colors.DIM}I'm here to chat, help with code, answer questions, or just hang out. What's on your mind?{Colors.RESET}\n")
        
        while True:
            try:
                # Prompt with styling
                prompt = f"{Colors.BRIGHT_CYAN}CodeMaster{Colors.RESET} {Colors.BRIGHT_YELLOW}>{Colors.RESET} "
                user_input = input(prompt).strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print(f"\n{Colors.BRIGHT_GREEN}👋 Goodbye! It was great chatting with you! Come back anytime! 😊{Colors.RESET}")
                    print(f"{Colors.DIM}Returning to terminal...{Colors.RESET}\n")
                    sys.exit(0)
                
                if user_input:
                    response = await self.process_command(user_input)
                    if response:
                        # Format the response with code highlighting
                        formatted_response = self.code_formatter.format_response(response)
                        print(f"\n{formatted_response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.BRIGHT_YELLOW}👋 Caught you trying to leave! See you next time! 😊{Colors.RESET}")
                print(f"{Colors.DIM}Returning to terminal...{Colors.RESET}\n")
                sys.exit(0)
            except EOFError:
                break
            except Exception as e:
                print(f"\n{Colors.RED}An error occurred: {e}{Colors.RESET}\n")
    
    def run(self):
        """Main entry point"""
        asyncio.run(self.run_async())

if __name__ == "__main__":
    ai = CodeMasterAI()
    ai.run()
