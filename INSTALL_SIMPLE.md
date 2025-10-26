# 🚀 Simple Installation for Termux (NO BUILD ERRORS!)

This method works 100% on Termux without any compilation issues.

## ✅ Installation Steps

```bash
# 1. Remove old installation
cd ~
rm -rf lai

# 2. Clone repository
git clone https://github.com/hakimigg/lai.git
cd lai

# 3. Install ONLY these packages (no compilation needed!)
pip install requests
pip install beautifulsoup4
pip install colorama
pip install aiohttp

# 4. Use the simple AI engine (no pydantic needed)
mv ai_engine.py ai_engine_original.py
mv ai_engine_simple.py ai_engine.py

# 5. Get a FREE API key from Groq
# Visit: https://console.groq.com/keys
# Sign up and copy your key

# 6. Set your API key
export GROQ_API_KEY="paste_your_key_here"

# 7. Run the app
python main.py
```

## 🎉 That's It!

No build errors, no pydantic, no compilation. Just pure Python!

## 🔑 Make API Key Permanent

```bash
# Add to your bash profile
echo 'export GROQ_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

## 📱 Create Shortcut

```bash
# Create easy launcher
echo 'alias lai="cd ~/lai && python main.py"' >> ~/.bashrc
source ~/.bashrc

# Now just type:
lai
```

## ✅ What Works

- ✅ Full AI chat with Groq or OpenAI
- ✅ Code generation
- ✅ Web search
- ✅ File management
- ✅ All app features
- ✅ NO compilation errors!

## 🔧 Using OpenAI Instead

If you prefer OpenAI:

```bash
export OPENAI_API_KEY="sk-your-key-here"
python main.py
```

## 📞 Troubleshooting

### "No module named 'requests'"
```bash
pip install requests
```

### "No module named 'beautifulsoup4'"
```bash
pip install beautifulsoup4
```

### "API key not found"
```bash
# Make sure you exported it:
export GROQ_API_KEY="your_key_here"

# Check if it's set:
echo $GROQ_API_KEY
```

## 🌟 Why This Works

- Uses direct API calls with `requests` library
- No pydantic or complex dependencies
- No compilation needed
- Works on any Termux installation
- Same features as full version!

Happy coding! 🎉
