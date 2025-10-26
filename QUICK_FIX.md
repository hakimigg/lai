# 🚨 QUICK FIX for Termux Installation Issues

If you're getting "failed to build pydantic-core" or "failed to build jiter" errors, follow this:

## ✅ Working Solution

```bash
# 1. Remove old installation
cd ~
rm -rf lai

# 2. Clone repository
git clone https://github.com/hakimigg/lai.git
cd lai

# 3. Install packages ONE BY ONE
pip install requests
pip install beautifulsoup4  
pip install colorama
pip install python-dotenv
pip install aiohttp

# 4. Try installing Groq (may fail - that's OK)
pip install groq

# 5. If Groq fails, use OpenAI with older version
pip install openai==0.28.1

# 6. Set your API key
# For Groq (if step 4 worked):
export GROQ_API_KEY="your_key_here"

# For OpenAI (if using step 5):
export OPENAI_API_KEY="your_key_here"

# 7. Run the app
python main.py
```

## 🎯 Why This Works

- Installing packages one by one avoids dependency conflicts
- Older versions (0.28.1) don't require pydantic v2
- No compilation needed

## 🔑 Get API Keys

**Groq (Free & Fast)**: https://console.groq.com/keys
**OpenAI**: https://platform.openai.com/api-keys

## ✅ Test Installation

```bash
# Test if packages installed
python -c "import requests; print('requests OK')"
python -c "import aiohttp; print('aiohttp OK')"

# Test if AI library works
python -c "import openai; print('OpenAI OK')"
# or
python -c "import groq; print('Groq OK')"
```

## 📞 Still Not Working?

Install ONLY the essentials and use the app without AI libraries:

```bash
pip install requests beautifulsoup4 colorama python-dotenv aiohttp
```

Then manually add API calls using requests library (the app will guide you).

## 🎉 Success!

Once installed, type `help` in the app to see all commands.
