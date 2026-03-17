# Terminal Portfolio Tracker

A simple, fast terminal tool to manage a local stock portfolio, track live performance, and get AI-summarized market news. Built to be readable and resilient without needing a heavy database.

### The Architecture
I built this project to balance speed, privacy, and reliability:

Local Event Ledger: All BUY and SELL transactions are saved locally to a Portfolio.json file. The app calculates your current holdings, average cost, and Profit/Loss (P&L) on the fly by reading this transaction history.

Live Prices (yfinance): Uses yfinance to grab live market data and historical charts to calculate your portfolio's real-time value. Fast and free.

News (Yahoo RSS + Gemini): Bypasses web scrapers by pulling directly from Yahoo’s official RSS XML feed. The headlines are then streamed through Google's gemini-2.5-flash-lite model for a quick, character-by-character summary of why a stock is moving.

### Quick Start

Install dependencies: pip install yfinance google-genai python-dotenv

Add your key: Create a .env file and add GEMINI_API_KEY=your_key_here

Run it: python3 tracker.py

### Available Commands

|     Command      |                 Description                     |        Example        |
|                  |                                                 |                       |
|      `BUY`       |                  Buy shares                     | `BUY VOO 1.57 593.32` |
|      `SELL`      |                  Sell shares                    | `SELL VOO 0.50 615.10`|
|    `PORTFOLIO`   | View current holdings, average cost, and profit |      `PORTFOLIO`      |
|     `HISTORY`    |           View all past transactions            |       `HISTORY`       |
|     `REMOVE`     |            Undo the last transaction            |       `REMOVE`        |
|    `<Ticker>`    |   Get current price and historical performance  |         `VOO`         |
| `<Ticker> -NEWS` |      Get stock info + AI news summary           |      `VOO -NEWS`      |
|     `HELP`       |            Show the help menu                   |        `HELP`         |
