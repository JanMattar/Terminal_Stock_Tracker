# Terminal Stock Tracker

A lightweight, high-speed terminal tool to track US stocks and get AI-powered news analysis. Built to be fast, readable, and resilient.

### The Architecture (A Hybrid Approach)
I built this project to balance speed and reliability by mixing two different data retrieval strategies:

Prices (yfinance): Uses an unofficial web scraper. It's the fastest, free way to get live market data, but it can be brittle.

News (Yahoo RSS): Bypasses web scraping entirely. Because news scrapers frequently break or get shadowbanned, I wrote a custom XML fetcher that pulls directly from Yahoo’s official RSS syndication.

Analysis (gemini-2.0-flash-lite): Uses Google's high-speed "Lite" model to summarize the RSS headlines. I implemented text streaming so the AI's thoughts print to the terminal instantly, character-by-character.

### Quick Start
Install dependencies: pip install yfinance google-genai python-dotenv

Add your key: Create a .env file and add GEMINI_API_KEY=your_key_here

Run it: python tracker.py

Example: Type NVDA -NEWS to see the live price followed by the AI market summary.