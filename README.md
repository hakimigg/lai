# 🤖 CodeMaster AI - Termux Edition

Advanced Terminal-based AI Assistant optimized for Termux on Android devices. Powered by real AI APIs (OpenAI, Claude, Gemini, Groq) with web access capabilities.

## ✨ Features

- 🧠 **Multiple AI Providers**: OpenAI, Claude, Gemini, and Groq support
- 🌐 **Web Search**: Real-time web search and current information
- 💻 **Code Generation**: Dynamic code generation with syntax highlighting
- 📁 **File Management**: Complete file system operations with animations
- 🎨 **Beautiful UI**: Colorful terminal interface with progress animations
- 📱 **Termux Optimized**: Specifically designed for Android/Termux environment
- ⚡ **Fast & Efficient**: Lightweight and responsive

## 📦 Installation

### Prerequisites

Make sure you have Termux installed on your Android device. You can download it from F-Droid.

### Setup Steps

1. **Update Termux packages**:
```bash
pkg update && pkg upgrade
```

2. **Install required packages**:
```bash
pkg install python git
```

3. **Clone or copy this folder to your Termux storage**:
```bash
# If you have it on your device storage
cp -r /storage/emulated/0/path/to/termux\ ai ~/
cd ~/termux\ ai
```

4. **Make the run script executable**:
```bash
chmod +x run.sh
```

5. **Set up your API keys** (see API Setup section below)

6. **Run the application**:
```bash
./run.sh
```

Or run directly with Python:
```bash
python main.py
```

## 🔑 API Setup

You need at least one AI API key to use CodeMaster AI. Here's how to get them:

### 1. Groq (Recommended - Free & Fast)
- Visit: https://console.groq.com/keys
- Sign up and get your free API key
- Set in Termux:
```bash
export GROQ_API_KEY="your_key_here"
```

### 2. OpenAI
- Visit: https://platform.openai.com/api-keys
- Create account and get API key
- Set in Termux:
```bash
export OPENAI_API_KEY="your_key_here"
```

### 3. Google Gemini
- Visit: https://makersuite.google.com/app/apikey
- Get your API key
- Set in Termux:
```bash
export GOOGLE_API_KEY="your_key_here"
```

### 4. Anthropic Claude
- Visit: https://console.anthropic.com/
- Get your API key
- Set in Termux:
```bash
export ANTHROPIC_API_KEY="your_key_here"
```

### Making API Keys Persistent

To avoid setting API keys every time, add them to your `.bashrc`:

```bash
nano ~/.bashrc
```

Add these lines:
```bash
export GROQ_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
```

Save and reload:
```bash
source ~/.bashrc
```

Alternatively, create a `.env` file in the application directory:
```bash
nano .env
```

Add:
```
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## 🚀 Usage

### Basic Commands

```bash
help           # Show all commands
clear          # Clear screen
status         # Show API connection status
setup          # Show API setup instructions
history        # Show conversation history
exit           # Exit application
```

### File Management

```bash
save code      # Save code from last AI response
create <file>  # Create a new file
read <file>    # Read file content
delete <file>  # Delete a file
move <src> <dst>  # Move/rename file
mkdir <dir>    # Create directory
ls [dir]       # List directory contents
cd <dir>       # Change directory
pwd            # Show current directory
find <pattern> # Find files
analyze [dir]  # Analyze directory structure
project <name> # Create project structure
```

### AI Features

```bash
search <query>    # Web search
news              # Get latest news
weather [location] # Get weather info
unrestricted      # Activate unrestricted mode
```

### Natural Conversation

Just type naturally! Examples:
- "Create a Python web scraper"
- "Build a calculator app"
- "What's the latest in AI?"
- "Debug this code..."
- "Make a Discord bot"

## 📱 Termux-Specific Tips

### Storage Access

To access your phone's storage:
```bash
termux-setup-storage
```

Then you can access:
- `/storage/emulated/0/` - Internal storage
- `/storage/emulated/0/Download/` - Downloads folder
- `/storage/emulated/0/Documents/` - Documents folder

### Saving Code to Phone Storage

When the AI generates code, you can say:
- "save to storage"
- "put it in downloads"
- "save to /storage/emulated/0/MyProjects"

### Running in Background

To keep the app running when you close Termux:
```bash
nohup python main.py &
```

### Creating a Shortcut

Create a shortcut script in your home directory:
```bash
echo '#!/data/data/com.termux/files/usr/bin/bash' > ~/codemaster
echo 'cd ~/termux\ ai && python main.py' >> ~/codemaster
chmod +x ~/codemaster
```

Then run from anywhere:
```bash
~/codemaster
```

## 🎨 Features Showcase

### Code Generation with Syntax Highlighting
The AI generates code with beautiful syntax highlighting and line numbers.

### File Operations with Animations
All file operations show progress with smooth animations:
- Creating files: 📝
- Reading files: 📖
- Writing files: ✍️
- Deleting files: 🗑️
- Moving files: 📦

### Smart Code Saving
The AI can save generated code to files automatically. Just ask naturally:
- "save this to my projects folder"
- "create a file called calculator.py"
- "put it in downloads"

## 🔧 Troubleshooting

### Dependencies Installation Issues

If you encounter issues installing dependencies:
```bash
pkg install python python-pip
pip install --upgrade pip
pip install -r requirements.txt
```

### Permission Errors

If you get permission errors accessing storage:
```bash
termux-setup-storage
```

### API Connection Issues

Check your internet connection and API keys:
```bash
# In the app
status
```

### Clear Cache

If the app behaves strangely:
```bash
rm -rf __pycache__
```

## 📝 Configuration

Edit `config.py` to customize:
- Preferred AI provider
- Response length (MAX_TOKENS)
- Temperature (creativity level)
- Thinking animation delays

## 🌟 Tips for Best Experience

1. **Use Groq for speed**: It's free and very fast
2. **Enable storage access**: For saving files to your phone
3. **Set up .bashrc**: For persistent API keys
4. **Use natural language**: Just chat normally with the AI
5. **Try unrestricted mode**: For maximum AI capabilities

## 🤝 Support

If you encounter issues:
1. Check API keys are set correctly
2. Ensure internet connection is active
3. Update Termux packages: `pkg update && pkg upgrade`
4. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## 📄 License

This is a personal AI assistant tool. Use responsibly and in accordance with the terms of service of the AI providers you use.

## 🎉 Enjoy!

You now have a powerful AI assistant running on your Android device! Ask it anything, generate code, search the web, and manage files - all from your terminal.

Happy coding! 🚀
