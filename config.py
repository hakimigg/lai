"""
Configuration file for CodeMaster AI - Termux Edition
Add your API keys here
"""

import os
from typing import Optional

class Config:
    # OpenAI API Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = 'gpt-3.5-turbo'  # Available with all OpenAI accounts
    
    # Anthropic Claude API Configuration  
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY', '')
    ANTHROPIC_MODEL: str = 'claude-3-sonnet-20240229'
    
    # Google Gemini API Configuration
    GOOGLE_API_KEY: Optional[str] = os.getenv('GOOGLE_API_KEY', '')
    
    # Groq API Configuration (Free and fast)
    GROQ_API_KEY: Optional[str] = os.getenv('GROQ_API_KEY', '')
    
    # Preferred AI Provider (openai, anthropic, google, groq)
    PREFERRED_PROVIDER: str = 'groq'
    
    # Web Search Configuration
    SERP_API_KEY: Optional[str] = os.getenv('SERP_API_KEY', '')
    
    # News API Configuration
    NEWS_API_KEY: Optional[str] = os.getenv('NEWS_API_KEY', '')
    
    # Weather API Configuration
    WEATHER_API_KEY: Optional[str] = os.getenv('WEATHER_API_KEY', '')
    
    # Response Configuration
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    THINKING_DELAY_MIN: float = 1.0  # Minimum thinking time in seconds
    THINKING_DELAY_MAX: float = 3.0  # Maximum thinking time in seconds
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available AI providers based on API keys"""
        providers = []
        if cls.OPENAI_API_KEY:
            providers.append('openai')
        if cls.ANTHROPIC_API_KEY:
            providers.append('anthropic')
        if cls.GOOGLE_API_KEY:
            providers.append('google')
        if cls.GROQ_API_KEY:
            providers.append('groq')
        return providers
    
    @classmethod
    def has_web_access(cls) -> bool:
        """Check if web access APIs are configured"""
        return bool(cls.SERP_API_KEY or cls.NEWS_API_KEY)

# Instructions for getting API keys
API_INSTRUCTIONS = """
🔑 API Key Setup Instructions for Termux:

1. OpenAI (Recommended):
   - Go to: https://platform.openai.com/api-keys
   - Create account and get API key
   - Set environment variable: export OPENAI_API_KEY=your_key_here
   - Add to ~/.bashrc for persistence

2. Anthropic Claude:
   - Go to: https://console.anthropic.com/
   - Get API key
   - Set environment variable: export ANTHROPIC_API_KEY=your_key_here

3. Groq (Free and Fast - Recommended for Termux):
   - Go to: https://console.groq.com/keys
   - Get free API key
   - Set environment variable: export GROQ_API_KEY=your_key_here

4. Google Gemini:
   - Go to: https://makersuite.google.com/app/apikey
   - Get API key
   - Set environment variable: export GOOGLE_API_KEY=your_key_here

5. Web Search (Optional):
   - SerpAPI: https://serpapi.com/
   - Set environment variable: export SERP_API_KEY=your_key_here

6. News API (Optional):
   - NewsAPI: https://newsapi.org/
   - Set environment variable: export NEWS_API_KEY=your_key_here

To set environment variables in Termux:
1. Edit your .bashrc file:
   nano ~/.bashrc

2. Add these lines:
   export OPENAI_API_KEY="your_api_key_here"
   export GROQ_API_KEY="your_api_key_here"

3. Save and reload:
   source ~/.bashrc

Or create a .env file in this directory with:
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
"""
