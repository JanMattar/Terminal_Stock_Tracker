# Terminal Stock Tracker

A simple, fast terminal tool to track US stocks, manage a local portfolio, and get AI-summarized market news. Built to be readable and resilient without needing a heavy database.

### The Architecture
I built this project to balance speed and reliability:

Prices (yfinance): Uses yfinance to grab live market data and historical charts. Fast and free.

Portfolio Ledger: All BUY and SELL transactions are saved locally to a Portfolio.json file. The app calculates your current holdings, average cost, and Profit/Loss (P&L) on the fly by reading this history.

News (Yahoo RSS + Gemini): Bypasses brittle web scrapers by pulling directly from Yahoo’s official RSS XML feed. The headlines are then streamed through Google's gemini-2.5-flash-lite model for a quick, character-by-character summary of why the stock is moving.

### Quick Start

Install dependencies: pip install yfinance google-genai python-dotenv

Add your key: Create a .env file and add GEMINI_API_KEY=your_key_here

Run it: python3 tracker.py

### Available Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `<Ticker>` | Get current price and historical performance | `VOO` |
| `<Ticker> -NEWS` | Get stock info + AI news summary | `VOO -NEWS` |
| `BUY` | Buy shares (saved to local ledger) | `BUY VOO 1.57 593.32` |
| `SELL` | Sell shares | `SELL VOO 0.50 615.10` |
| `PORTFOLIO` | View current holdings, average cost, and P&L | `PORTFOLIO` |
| `HISTORY` | View all past transactions | `HISTORY` |
| `HISTORY -<Ticker> [-<Ticker>...] | Filter history by ticker(s) | HISTORY -VOO -AAPL |
| `REMOVE` | Undo the last transaction | `REMOVE` |
| `HELP` | Show the help menu | `HELP` |