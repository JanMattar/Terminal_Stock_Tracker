# Terminal Portfolio Tracker

A simple, fast terminal tool to manage a local stock portfolio, track live performance, and get AI-summarized market news. Built to be readable and resilient without needing a heavy database.

## The Architecture

I built this project to balance speed, privacy, and reliability:

**Local Event Ledger:** All BUY, SELL, and DIVIDEND transactions are saved locally within a dedicated data/ directory. The app dynamically calculates current holdings, average cost, and both realized and unrealized Profit/Loss (P&L) on the fly using this event history.

**Live Prices & Terminal Charts:** Uses yfinance to grab live market data and historical pricing. It integrates with plotext to draw clean, responsive ASCII line charts directly in your terminal window.

**News & AI Advisor (Gemini):** Bypasses web scrapers by pulling directly from Yahoo’s official RSS XML feed. Headlines are processed through Google's gemini-2.5-flash-lite model for a quick summary of why a stock is moving. It also features a Portfolio Advisor that analyzes live allocations to provide professional critiques on diversification and risk.

**Smart Token caching:** To protect API quotas and increase performance, the app implements an in-memory caching layer using Python's lru_cache. Identical news queries are served instantly from memory without consuming additional Gemini tokens.

**Containerized Environment:** Fully Dockerized for a seamless experience across any operating system without polluting your local Python environment.

## Quick Start

You can run this tracker instantly using the pre-built Docker image, or build it yourself from the source code.
(replace `your_api_key` with your actual Gemini API key)

#### Option 1: Run Instantly (Recommended)
```bash
docker run -it -v ./data:/app/data -e GEMINI_API_KEY="your_api_key" jeanmatar16/terminal-portfolio-tracker
```

#### Option 2: Build from Source
```bash
git clone https://github.com/JanMattar/Terminal-Portfolio-Tracker.git
cd Terminal-Portfolio-Tracker
echo "GEMINI_API_KEY=your_key_here" > .env
docker compose run tracker
```

## Available Commands

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
| `PORTFOLIO -VS` | View current holdings, average cost, and Profit + Compare vs S&P 500 | `PORTFOLIO -VS` |
| `EXPORT` | Export transaction history to CSV | `EXPORT` |
| `HISTORY` | View all past transactions | `HISTORY` |
| `HISTORY <Ticker> [<Ticker>...]` | Filter history by ticker(s) | `HISTORY VOO AAPL` |
| `REMOVE` | Undo the last transaction | `REMOVE` |
| `HELP` | Show the help menu | `HELP` |
