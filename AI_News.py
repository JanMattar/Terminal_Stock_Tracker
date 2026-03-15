import os
import urllib.request
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from google import genai as ai
from ui import print_error

load_dotenv()

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

def print_news(NEWS, symbol=None):
    if not NEWS or not symbol:
        return
    
    try:
        client = ai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        news = get_news_rss(symbol)
        
        news_summary = "\n".join([
            f"• {item.get('title')}: {item.get('summary')[:100]}..." 
            for item in news 
            if item.get('title')
        ])

        if news_summary:
            prompt = f"Based on this recent news for {symbol.upper()}:\n{news_summary}\n\nProvide a brief, concise explanation (under 100 words) why the stock is moving today."
            response = client.models.generate_content_stream(model="gemini-2.5-flash-lite", contents=prompt)
            
            print(f"\n--- {symbol.upper()} NEWS ---")
            for chunk in response:
                print(chunk.text, end="", flush=True) 
            print() 

        else:
            print(f"\n--- {symbol.upper()} NEWS ---")
            print("No recent news headlines available to analyze.")
            
    except Exception as e:
        print_error(f"Error fetching news for {symbol.upper()}: {e}")