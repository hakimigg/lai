"""
AI Engine for CodeMaster AI - Termux Edition
Handles communication with various AI APIs
"""

import asyncio
import aiohttp
import json
import time
import random
import requests
from typing import Optional, Dict, Any, List
from config import Config

# Try to import AI libraries, but don't fail if they're not available
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import google.generativeai as genai
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

class AIEngine:
    def __init__(self):
        self.config = Config()
        self.setup_clients()
        
    def setup_clients(self):
        """Initialize AI API clients"""
        self.clients = {}
        
        # OpenAI
        if self.config.OPENAI_API_KEY:
            if HAS_OPENAI:
                self.clients['openai'] = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
            else:
                self.clients['openai'] = 'direct'  # Use direct API calls
            
        # Anthropic Claude
        if self.config.ANTHROPIC_API_KEY:
            if HAS_ANTHROPIC:
                self.clients['anthropic'] = anthropic.Anthropic(api_key=self.config.ANTHROPIC_API_KEY)
            else:
                self.clients['anthropic'] = 'direct'
            
        # Google Gemini
        if self.config.GOOGLE_API_KEY:
            if HAS_GOOGLE:
                genai.configure(api_key=self.config.GOOGLE_API_KEY)
                self.clients['google'] = genai.GenerativeModel('gemini-pro')
            else:
                self.clients['google'] = 'direct'
            
        # Groq
        if self.config.GROQ_API_KEY:
            if HAS_GROQ:
                self.clients['groq'] = Groq(api_key=self.config.GROQ_API_KEY)
            else:
                self.clients['groq'] = 'direct'  # Use direct API calls
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the AI"""
        return """You are CodeMaster AI, a friendly and helpful AI assistant. You chat naturally like ChatGPT or Kimi.

Your personality:
- Warm, conversational, and friendly
- You chat about ANY topic - not just coding
- When someone says "hi" or "hello", you greet them warmly and ask how you can help
- You're knowledgeable about everything: technology, science, culture, daily life, entertainment, etc.
- You give thoughtful, engaging responses
- You're helpful with coding when asked, but you're also great at general conversation

When chatting casually:
- Be friendly and natural
- Ask follow-up questions to keep conversation flowing
- Share interesting insights and perspectives
- Discuss hobbies, interests, current events, philosophy, etc.
- Be empathetic and understanding
- Use a conversational tone, not overly formal

When helping with code:
- Provide complete, working code
- Explain what the code does
- Include setup instructions
- Mention they can use 'save code' command to save it
- Consider Termux environment (Android paths like /storage/emulated/0)

You can help with:
- General conversation and questions about anything
- Coding and programming (all languages)
- Technology and science discussions
- Creative writing and ideas
- Problem-solving and advice
- Learning new topics
- Entertainment recommendations
- And literally anything else!

Current date: {current_date}

Remember: You're a friendly AI companion who enjoys chatting about everything, not just a coding assistant. Be warm, engaging, and helpful!"""

    async def generate_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Generate AI response using the preferred provider"""
        if not self.clients:
            return "❌ No AI providers configured. Please set up API keys in config.py"
        
        # Use preferred provider or fallback to available ones
        provider = self.config.PREFERRED_PROVIDER
        if provider not in self.clients:
            provider = list(self.clients.keys())[0]
        
        try:
            # Use direct API if library not installed
            if self.clients.get(provider) == 'direct':
                return await self._generate_direct_api(provider, user_input, conversation_history)
            
            if provider == 'openai':
                return await self._generate_openai_response(user_input, conversation_history)
            elif provider == 'anthropic':
                return await self._generate_anthropic_response(user_input, conversation_history)
            elif provider == 'google':
                return await self._generate_google_response(user_input, conversation_history)
            elif provider == 'groq':
                return await self._generate_groq_response(user_input, conversation_history)
        except Exception as e:
            return f"❌ Error generating response: {str(e)}\nTrying fallback provider..."
    
    async def _generate_direct_api(self, provider: str, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using direct API calls (no library needed)"""
        messages = [{"role": "system", "content": self.get_system_prompt().format(current_date=time.strftime("%Y-%m-%d"))}]
        
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        messages.append({"role": "user", "content": user_input})
        
        if provider == 'groq':
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.config.GROQ_API_KEY}", "Content-Type": "application/json"}
            data = {"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": self.config.MAX_TOKENS, "temperature": self.config.TEMPERATURE}
        elif provider == 'openai':
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.config.OPENAI_API_KEY}", "Content-Type": "application/json"}
            data = {"model": self.config.OPENAI_MODEL, "messages": messages, "max_tokens": self.config.MAX_TOKENS, "temperature": self.config.TEMPERATURE}
        else:
            return f"❌ Direct API not implemented for {provider}"
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ API Error: {str(e)}"
    
    async def _generate_openai_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using OpenAI"""
        messages = [{"role": "system", "content": self.get_system_prompt().format(current_date=time.strftime("%Y-%m-%d"))}]
        
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 messages for context
        
        messages.append({"role": "user", "content": user_input})
        
        response = self.clients['openai'].chat.completions.create(
            model=self.config.OPENAI_MODEL,
            messages=messages,
            max_tokens=self.config.MAX_TOKENS,
            temperature=self.config.TEMPERATURE
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using Anthropic Claude"""
        system_prompt = self.get_system_prompt().format(current_date=time.strftime("%Y-%m-%d"))
        
        # Build conversation context
        conversation = ""
        if conversation_history:
            for msg in conversation_history[-10:]:
                role = "Human" if msg["role"] == "user" else "Assistant"
                conversation += f"\n{role}: {msg['content']}\n"
        
        conversation += f"\nHuman: {user_input}\n\nAssistant:"
        
        response = self.clients['anthropic'].messages.create(
            model=self.config.ANTHROPIC_MODEL,
            max_tokens=self.config.MAX_TOKENS,
            temperature=self.config.TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": conversation}]
        )
        
        return response.content[0].text
    
    async def _generate_google_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using Google Gemini"""
        prompt = self.get_system_prompt().format(current_date=time.strftime("%Y-%m-%d"))
        prompt += f"\n\nUser: {user_input}\nAssistant:"
        
        response = self.clients['google'].generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
        )
        
        return response.text
    
    async def _generate_groq_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using Groq"""
        messages = [{"role": "system", "content": self.get_system_prompt().format(current_date=time.strftime("%Y-%m-%d"))}]
        
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        messages.append({"role": "user", "content": user_input})
        
        response = self.clients['groq'].chat.completions.create(
            model="llama-3.1-8b-instant",  # Current production model
            messages=messages,
            max_tokens=self.config.MAX_TOKENS,
            temperature=self.config.TEMPERATURE
        )
        
        return response.choices[0].message.content

class WebSearchEngine:
    def __init__(self):
        self.config = Config()
    
    async def search_web(self, query: str) -> str:
        """Search the web for current information"""
        try:
            if self.config.SERP_API_KEY:
                return await self._search_with_serpapi(query)
            else:
                return await self._search_with_duckduckgo(query)
        except Exception as e:
            return f"Web search error: {str(e)}"
    
    async def _search_with_serpapi(self, query: str) -> str:
        """Search using SerpAPI"""
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.config.SERP_API_KEY,
            "engine": "google",
            "num": 5
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                
                results = []
                for result in data.get("organic_results", [])[:3]:
                    results.append(f"• {result.get('title', '')}: {result.get('snippet', '')}")
                
                return "\n".join(results) if results else "No results found"
    
    async def _search_with_duckduckgo(self, query: str) -> str:
        """Fallback search using DuckDuckGo (no API key required)"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            url = f"https://duckduckgo.com/html/?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result')[:3]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('div', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text().strip()
                    snippet = snippet_elem.get_text().strip()
                    results.append(f"• {title}: {snippet}")
            
            return "\n".join(results) if results else "No results found"
        except Exception as e:
            return f"Search unavailable: {str(e)}"
    
    async def get_current_news(self) -> str:
        """Get current news headlines"""
        if not self.config.NEWS_API_KEY:
            return await self._get_news_fallback()
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": self.config.NEWS_API_KEY,
                "country": "us",
                "pageSize": 5
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    
                    headlines = []
                    for article in data.get("articles", []):
                        headlines.append(f"• {article.get('title', '')}")
                    
                    return "\n".join(headlines) if headlines else "No news available"
        except Exception as e:
            return f"News unavailable: {str(e)}"
    
    async def _get_news_fallback(self) -> str:
        """Fallback news without API"""
        return "News API not configured. Set NEWS_API_KEY for real-time news."

    async def get_weather(self, location: str = "current") -> str:
        """Get weather information"""
        if not self.config.WEATHER_API_KEY:
            return "Weather API not configured. Set WEATHER_API_KEY for real-time weather."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": self.config.WEATHER_API_KEY,
                "units": "metric"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    
                    if response.status == 200:
                        weather = data["weather"][0]["description"]
                        temp = data["main"]["temp"]
                        feels_like = data["main"]["feels_like"]
                        city = data["name"]
                        
                        return f"Weather in {city}: {weather.title()}, {temp}°C (feels like {feels_like}°C)"
                    else:
                        return f"Weather data unavailable for {location}"
        except Exception as e:
            return f"Weather error: {str(e)}"
