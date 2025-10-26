# 📱 Termux Installation Guide

Quick guide to install CodeMaster AI on Android using Termux.

## 🚀 Quick Install

```bash
# Update Termux
pkg update && pkg upgrade -y

# Install dependencies
pkg install python git -y

# Setup storage access
termux-setup-storage

# Clone repository
git clone https://github.com/hakimigg/lai.git
cd lai

# Install packages (DO NOT upgrade pip in Termux!)
pip install -r requirements.txt

# Set API key (get free key from https://console.groq.com/keys)
export GROQ_API_KEY="your_key_here"

# Run
python main.py
```

## 🔧 If Installation Fails

### Problem: jiter build error

If you see errors about "Failed to build jiter", use the minimal installation:

```bash
# Install minimal requirements
pip install -r requirements-minimal.txt

# Or install manually:
pip install requests beautifulsoup4 colorama python-dotenv aiohttp groq
```

### Problem: Package conflicts

Install packages one by one:

```bash
pip install requests beautifulsoup4 colorama python-dotenv aiohttp
pip install groq
```

**IMPORTANT**: Never run `pip install --upgrade pip` in Termux - it will break your installation!

### Problem: Permission errors

```bash
termux-setup-storage
# Allow permission when prompted
```

## ✅ Verify Installation

```bash
python -c "import groq; print('Success!')"
```

If you see "Success!", you're ready to go!

## 🎯 Recommended: Use Groq Only

Groq is:
- ✅ Free
- ✅ Fast
- ✅ Easy to install
- ✅ Works great on mobile

Get your free API key: https://console.groq.com/keys

## 📞 Still Having Issues?

1. Make sure Termux is from F-Droid (not Play Store)
2. Update all packages: `pkg upgrade`
3. Try minimal installation
4. Use only Groq API

## 🚀 After Installation

```bash
# Make it permanent
echo 'export GROQ_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc

# Create shortcut
echo 'alias lai="cd ~/lai && python main.py"' >> ~/.bashrc
source ~/.bashrc

# Now just type:
lai
```

Happy coding! 🎉
