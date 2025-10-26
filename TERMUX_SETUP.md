# 📱 Termux Setup Guide for CodeMaster AI

Complete step-by-step guide to set up CodeMaster AI on your Android device using Termux.

## 🎯 Quick Start (5 Minutes)

### Step 1: Install Termux
1. Download Termux from **F-Droid** (NOT Google Play Store)
   - Visit: https://f-droid.org/packages/com.termux/
   - Or search "Termux" in F-Droid app

### Step 2: Initial Termux Setup
Open Termux and run these commands:

```bash
# Update packages
pkg update && pkg upgrade -y

# Install Python and Git
pkg install python git -y

# Setup storage access (important!)
termux-setup-storage
```

When prompted, **allow storage access** - this lets you save files to your phone.

### Step 3: Get CodeMaster AI

If you have the folder on your phone storage:
```bash
# Copy from Downloads (adjust path if needed)
cp -r /storage/emulated/0/Download/termux\ ai ~/
cd ~/termux\ ai
```

Or if starting fresh, create the directory:
```bash
mkdir -p ~/termux\ ai
cd ~/termux\ ai
```

### Step 4: Setup API Key

Get a **free Groq API key** (fastest option):
1. Visit: https://console.groq.com/keys (on your phone browser)
2. Sign up with email
3. Copy your API key

Set it in Termux:
```bash
export GROQ_API_KEY="paste_your_key_here"
```

### Step 5: Install Dependencies

```bash
# Install Python packages
pip install requests beautifulsoup4 colorama rich openai anthropic google-generativeai groq python-dotenv aiohttp lxml
```

### Step 6: Run!

```bash
python main.py
```

🎉 **Done!** You should see the CodeMaster AI welcome screen.

---

## 🔧 Detailed Setup

### Making API Keys Permanent

To avoid setting the API key every time:

```bash
# Edit your bash profile
nano ~/.bashrc
```

Add this line at the end:
```bash
export GROQ_API_KEY="your_key_here"
```

Save: `Ctrl + X`, then `Y`, then `Enter`

Reload:
```bash
source ~/.bashrc
```

### Alternative: Using .env File

```bash
cd ~/termux\ ai
nano .env
```

Add:
```
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

Save and exit.

### Creating a Quick Launch Command

Make it easy to start:

```bash
# Create launcher script
echo '#!/data/data/com.termux/files/usr/bin/bash' > ~/ai
echo 'cd ~/termux\ ai && python main.py' >> ~/ai
chmod +x ~/ai
```

Now you can just type `~/ai` from anywhere to launch!

---

## 📂 File Locations in Termux

### Important Paths

- **Termux Home**: `~` or `/data/data/com.termux/files/home/`
- **Phone Storage**: `/storage/emulated/0/`
- **Downloads**: `/storage/emulated/0/Download/`
- **Documents**: `/storage/emulated/0/Documents/`

### Saving Code to Phone Storage

When AI generates code, tell it:
- "save to /storage/emulated/0/MyProjects"
- "put it in downloads"
- "save to storage"

---

## 🎨 Customization

### Change AI Provider

Edit `config.py`:
```bash
nano config.py
```

Change line:
```python
PREFERRED_PROVIDER: str = 'groq'  # or 'openai', 'google', 'anthropic'
```

### Adjust Response Length

In `config.py`:
```python
MAX_TOKENS: int = 2000  # Increase for longer responses
```

### Change Colors

Edit the `Colors` class in any file to customize the color scheme.

---

## 🚀 Advanced Usage

### Running in Background

Keep it running when you close Termux:
```bash
nohup python main.py > output.log 2>&1 &
```

Check if it's running:
```bash
ps aux | grep python
```

Kill it:
```bash
pkill -f main.py
```

### Auto-start on Termux Launch

Add to `~/.bashrc`:
```bash
# Auto-start CodeMaster AI
cd ~/termux\ ai && python main.py
```

### Using with Termux:Widget

Create a widget shortcut:
```bash
mkdir -p ~/.shortcuts
echo '#!/data/data/com.termux/files/usr/bin/bash' > ~/.shortcuts/CodeMaster
echo 'cd ~/termux\ ai && python main.py' >> ~/.shortcuts/CodeMaster
chmod +x ~/.shortcuts/CodeMaster
```

Install Termux:Widget from F-Droid, then add the widget to your home screen.

---

## 🔍 Troubleshooting

### "Command not found: python"
```bash
pkg install python -y
```

### "No module named 'X'"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x run.sh
termux-setup-storage
```

### API Key Not Working
```bash
# Check if it's set
echo $GROQ_API_KEY

# Re-export it
export GROQ_API_KEY="your_key_here"
```

### Can't Access Phone Storage
```bash
termux-setup-storage
# Allow permission when prompted
```

### App Crashes
```bash
# Clear cache
rm -rf __pycache__

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Slow Performance
- Use Groq (fastest free option)
- Reduce MAX_TOKENS in config.py
- Close other apps

---

## 💡 Tips & Tricks

### 1. Use Tab Completion
Press `Tab` to auto-complete file names and commands.

### 2. Access Command History
Press `↑` to cycle through previous commands.

### 3. Copy/Paste in Termux
- Long press to select text
- Volume Up + Q = Show keyboard
- Volume Up + V = Paste

### 4. Split Screen
Use Android's split-screen feature to have Termux and a browser open simultaneously.

### 5. External Keyboard
Connect a Bluetooth keyboard for easier typing.

### 6. Keep Screen On
In Termux, run:
```bash
termux-wake-lock
```

To release:
```bash
termux-wake-unlock
```

---

## 🌟 Getting the Most Out of It

### Best Practices

1. **Start with Groq**: It's free and fast
2. **Enable storage access**: Essential for saving files
3. **Use natural language**: Just chat normally
4. **Try different commands**: Explore all features
5. **Save important code**: Use the save commands

### Example Workflows

**Creating a Python Script:**
```
You: Create a Python script that downloads YouTube videos
AI: [generates code]
You: save to /storage/emulated/0/MyScripts/youtube_downloader.py
```

**Web Research:**
```
You: search latest Python frameworks
AI: [shows search results]
You: tell me more about FastAPI
```

**File Management:**
```
You: analyze /storage/emulated/0/Documents
AI: [shows directory analysis]
You: create a backup folder
```

---

## 📞 Need Help?

### Common Questions

**Q: Which AI provider should I use?**
A: Start with Groq - it's free, fast, and works great on mobile.

**Q: Can I use this offline?**
A: No, it requires internet to connect to AI APIs.

**Q: Is my data safe?**
A: Your conversations are sent to the AI provider you choose. Read their privacy policies.

**Q: Can I use multiple API keys?**
A: Yes! Set multiple keys and switch between providers.

**Q: Does this drain battery?**
A: Minimal impact. The app is lightweight and only uses data when you send requests.

---

## 🎓 Learning Resources

### Termux Basics
- Official Wiki: https://wiki.termux.com/
- Termux Commands: `pkg list-all`

### Python in Termux
- Install packages: `pip install package_name`
- Python version: `python --version`

### File System
- List files: `ls -la`
- Change directory: `cd path`
- Create directory: `mkdir name`
- Remove file: `rm filename`

---

## 🎉 You're All Set!

Enjoy your powerful AI assistant on Android! 

Type `help` in the app to see all available commands.

Happy coding! 🚀📱
