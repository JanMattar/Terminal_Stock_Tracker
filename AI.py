import os
import urllib.request
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from google import genai as ai
from ui import print_error
from functools import lru_cache

load_dotenv()

@lru_cache(maxsize=32)
def get_cached_ai_summary(symbol, news_summary):
    client = ai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"Based on this recent news for {symbol.upper()}:\n{news_summary}\n\nProvide a brief, concise explanation (under 100 words) why the stock is moving today."
    
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    return response.text

def get_news_rss(symbol):
    url = f"https://finance.yahoo.com/rss/headline?s={symbol}"
    try:
        # Disguise the Python script as a normal web browser
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        news_items = []
        
        for item in root.findall('.//item')[:3]:
            title_node = item.find('title')
            desc_node = item.find('description')
            
            news_items.append({
                'title': title_node.text if title_node is not None else "No Title",
                'summary': desc_node.text if desc_node is not None else ""
            })
        return news_items
    except Exception as e:
        print_error(f"RSS fetch failed: {e}")
        return []

def print_news(symbol=None):
    if not symbol:
        return
    
    try:
        news = get_news_rss(symbol)
        
        news_summary = "\n".join([
            f"• {item.get('title')}: {item.get('summary')[:100]}..." 
            for item in news 
            if item.get('title')
        ])

        if news_summary:
            print(f"--- {symbol.upper()} NEWS ---".center(150))
            
            analysis = get_cached_ai_summary(symbol, news_summary)
            print(analysis)
            print() 

        else:
            print(f"--- {symbol.upper()} NEWS ---".center(150))
            print("No recent news headlines available to analyze.")
            
    except Exception as e:
        print_error(f"Error fetching news for {symbol.upper()}: {e}")


def analyze_portfolio(portfolio_summary):
    if not portfolio_summary:
        return

    try: 
        client = ai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = f"Here is my current stock portfolio allocation:\n{portfolio_summary}\n\nAct as a blunt, professional financial advisor. Provide a brief, concise analysis (under 3 sentences) of this portfolio, focusing purely on diversification and risk and then provide advices if needed (maximum 3)."
        response = client.models.generate_content_stream(model="gemini-2.5-flash-lite", contents=prompt)

        print(f"\n{'--- AI PORTFOLIO ANALYSIS ---'.center(120)}")
        for chunk in response:
            print(chunk.text, end="", flush=True)
        print()
    
    except Exception as e:
        print_error(f"Error fetching AI analysis: {e}")