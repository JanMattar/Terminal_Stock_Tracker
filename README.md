# Terminal Portfolio Tracker

A simple, fast terminal tool to manage a local stock portfolio, track live performance, and get AI-summarized market news. Built to be readable and resilient without needing a heavy database.

### The Architecture

I built this project to balance speed, privacy, and reliability:

Local Event Ledger: All BUY, SELL, and DIVIDEND transactions are saved locally to a Portfolio.json file. The app calculates your current holdings, average cost, and Profit/Loss (P&L) on the fly using this event history.

Live Prices & Terminal Charts: Uses yfinance to grab live market data and historical pricing. It integrates with plotext to draw clean, responsive ASCII line charts directly in your terminal window. Fast and free.

News & AI Advisor (Gemini): Bypasses web scrapers by pulling directly from Yahoo’s official RSS XML feed. Headlines are streamed through Google's gemini-2.5-flash-lite model for a quick summary of why a stock is moving. It also features a Portfolio Advisor that analyzes your live allocations to provide instant, professional critiques on diversification and risk.

### Quick Start

Install dependencies: pip install yfinance google-genai python-dotenv plotext

Add your key: Create a .env file and add GEMINI_API_KEY=your_key_here

Run it: python3 tracker.py

### Available Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `<Ticker>` | Get current price and historical performance | `VOO` |
| `<Ticker> -NEWS` | Get stock info + AI news summary | `VOO -NEWS` |
| `<Ticker> -CH` | Get stock info + Plot 1Y Chart | `VOO -CH` |
| `BUY` | Buy shares (saved to local ledger) | `BUY VOO 1.57 593.32` |
| `SELL` | Sell shares | `SELL VOO 0.50 615.10` |
| `DIVIDEND` | Record a dividend payment | `DIVIDEND VOO 3.50` |
| `PORTFOLIO` | View current holdings, average cost, and Profit | `PORTFOLIO` |
| `PORTFOLIO -AI` | View current holdings, average cost, and Profit + AI Portfolio Analysis | `PORTFOLIO -AI` |
| `EXPORT` | Export transaction history to CSV | `EXPORT` |
| `HISTORY` | View all past transactions | `HISTORY` |
| `HISTORY -<Ticker> [-<Ticker>...]` | Filter history by ticker(s) | `HISTORY -VOO -AAPL` |
| `REMOVE` | Undo the last transaction | `REMOVE` |
| `HELP` | Show the help menu | `HELP` |
