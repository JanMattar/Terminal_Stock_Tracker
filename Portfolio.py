import json
import os
from datetime import datetime
import yfinance as yf
from ui import print_error, RED, GREEN, RESET
import csv
from AI import analyze_portfolio

PORTFOLIO_FILE = "data/Portfolio.json"

def load_ledger():
    if not os.path.exists(PORTFOLIO_FILE):
        return []
    try:
        with open(PORTFOLIO_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            ledger = json.loads(content)
            # Normalize all tickers to uppercase and save if changed
            changed = False
            for tx in ledger:
                if tx['ticker'] != tx['ticker'].upper():
                    tx['ticker'] = tx['ticker'].upper()
                    changed = True
            if changed:
                save_ledger(ledger)
            return ledger
    except json.JSONDecodeError:
        return []

def save_ledger(ledger):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

def buy_stock(ticker, quantity, price):
    ledger = load_ledger()
    ledger.append({
        "timestamp": datetime.now().isoformat(),
        "action": "BUY",
        "ticker": ticker.upper(),
        "quantity": quantity,
        "price": price
    })
    save_ledger(ledger)
    print(f"{GREEN}Bought {quantity} shares of {ticker.upper()} at ${price:.2f} at a total cost of ${quantity * price:.2f}{RESET}.")

def sell_stock(ticker, quantity, price):
    ledger = load_ledger()
    holdings = {}
    for entry in ledger:
        holdings[entry['ticker']] = holdings.get(entry['ticker'], 0) + (entry['quantity'] if entry['action'] == 'BUY' else -entry['quantity'])
    if holdings.get(ticker.upper(), 0) < quantity:
        print_error(f"Not enough shares to sell. You currently hold {holdings.get(ticker.upper(), 0)} shares of {ticker.upper()}, enter 'PORTFOLIO' to view your holdings.")
        return
    ledger.append({
        "timestamp": datetime.now().isoformat(),
        "action": "SELL",
        "ticker": ticker.upper(),
        "quantity": quantity,
        "price": price
    }) 
    save_ledger(ledger)
    print(f"{RED}Sold {quantity} shares of {ticker.upper()} at ${price:.2f} for a total of ${quantity * price:.2f}.{RESET}")

def add_dividend(ticker, amount):
    ledger = load_ledger()
    ledger.append({
        "timestamp": datetime.now().isoformat(),
        "action": "DIVIDEND",
        "ticker": ticker.upper(),
        "quantity": 0.0,
        "price": amount
    })
    save_ledger(ledger)
    print(f"{GREEN}Dividend of ${amount} recorded for {ticker.upper()}{RESET}")


def remove_last():
    ledger = load_ledger()
    if not ledger:
        print_error("No transactions to remove.")
        return
    removed = ledger.pop()
    save_ledger(ledger)
    if removed['action'] == 'DIVIDEND':
        print(f"{RED}Removed last transaction: {removed['action']} ${removed['price']:.2f} for {removed['ticker']}{RESET}")
    else:
        print(f"{RED}Removed last transaction: {removed['action']} {removed['quantity']} shares of {removed['ticker']} at ${removed['price']:.2f} at a total of ${removed['quantity'] * removed['price']:.2f}.{RESET}")

def show_history(tickers=None):
    ledger = load_ledger()
    if not ledger:
        print("No transactions found.")
        return

    ticker_filter = {t.upper() for t in tickers} if tickers else None

    filtered = []
    for entry in ledger:
        entry_ticker = entry['ticker'].upper()
        if ticker_filter is None or entry_ticker in ticker_filter:
            filtered.append(entry)

    if not filtered:
        if ticker_filter:
            print_error(f"No transactions found for tickers: {', '.join(ticker_filter)}.")
        else:
            print("No transactions found.")
        return

    print(f"\n{'--- TRANSACTION HISTORY ---'.center(60)}")
    print(f" {'Date':^18} {'Action':^8}{'Ticker':^9} {'Shares':^5}  {'Price':^10} {'Total':^8}")
    print("-" * 64)

    for entry in filtered:
        date = datetime.fromisoformat(entry["timestamp"])
        nice_time = date.strftime("%Y-%m-%d %H:%M")
        total = entry['price'] if entry['action'] == 'DIVIDEND' else entry['quantity'] * entry['price']
        if entry['action'] != 'DIVIDEND':
            print(f" {nice_time:<20} {entry['action']:<7} {entry['ticker']:<7} {entry['quantity']:<7}  ${entry['price']:<8.2f} ${total:<10.2f}")
        elif entry['action'] == 'DIVIDEND':
            print(f" {nice_time:<18} {entry['action']:<9} {entry['ticker']:<7} {entry['quantity']:<7}  ${entry['price']:<8.2f} ${total:<10.2f}")
    print("\n")

def get_current_price(ticker):
    try:
        return yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
    except:
        return None

def show_portfolio(ai_analysis=False, benchmark=False):
    ledger = load_ledger()
    holdings = {}
    cost = {}
    dividends = {}

    avg_costs = {}
    realized_profits = {} 
    for entry in ledger:
        ticker = entry['ticker']
        if entry['action'] == 'BUY':
            current_qty = holdings.get(ticker, 0)
            current_avg = avg_costs.get(ticker, 0)
            
            new_total_cost = (current_qty * current_avg) + (entry['quantity'] * entry['price'])
            new_qty = current_qty + entry['quantity']
            
            avg_costs[ticker] = new_total_cost / new_qty if new_qty > 0 else 0
            holdings[ticker] = new_qty
            
        elif entry['action'] == 'SELL':
            holdings[ticker] -= entry['quantity']

            profit_on_sale = (entry['price'] - avg_costs[ticker]) * entry['quantity']
            realized_profits[ticker] = realized_profits.get(ticker, 0) + profit_on_sale
            
        elif entry['action'] == 'DIVIDEND':
            dividends[ticker] = dividends.get(ticker, 0) + entry['price']

    if not ledger:
        print("No transactions yet. Your portfolio is empty.")
        return
    
    current_holdings = {ticker: (qty, avg_costs[ticker]) for ticker, qty in holdings.items() if qty > 0}

    prices = {}
    total_value = 0
    for ticker, (qty, avg_cost) in current_holdings.items():
        price = get_current_price(ticker)
        prices[ticker] = price
        if price:
            total_value += price * qty

    print(f"\n{'--- PORTFOLIO ---'.center(120)}")
    if not current_holdings:
        print(f"{'No active positions. All holdings have been sold.':^120}\n")
    else:
        print(f" {'Ticker':^7} {'Shares':^6} {'Holdings':^10} {'Avg-Cost':^9} {'Current-Price':^13} {'Daily-gain':^12} {'Daily-change':^13} {'All-Time-gain':^14} {'All-Time-change':^16} {'Allocation':^11}")
        print ("-" * 125)
    total_profit = 0
    total_cost = 0
    total_daily_gain = 0
    ai_allocations_string = ""

    for ticker, (qty, avg_cost) in current_holdings.items():
        current_price = prices.get(ticker)
        if current_price:
            try:
                history_2d = yf.Ticker(ticker).history(period="2d") 
                yesterday_price = history_2d['Close'].iloc[-2] if len(history_2d) > 1 else current_price
                daily_gain = (current_price - yesterday_price) * qty
                daily_pct = ((current_price - yesterday_price) / yesterday_price) * 100 if yesterday_price > 0 else 0
            except:
                daily_gain = 0
                daily_pct = 0
            all_time_gain = (current_price - avg_cost) * qty + dividends.get(ticker, 0) + realized_profits.get(ticker, 0)
            all_time_pct = ((current_price - avg_cost) / avg_cost) * 100 if avg_cost > 0 else 0
            total_cost += avg_cost * qty
            total_profit += all_time_gain
            total_daily_gain += daily_gain
            pnl_color = GREEN if all_time_gain >= 0 else RED
            daily_color = GREEN if daily_gain >= 0 else RED
            allocation_pct = ((avg_cost * qty) / total_value) * 100 if total_value > 0 else 0
            ai_allocations_string += f"{ticker}: {allocation_pct:.2f}%, "
            print(f"  {ticker:<7}{qty:<7} ${avg_cost * qty:<7.2f}  ${avg_cost:<10.2f} ${current_price:<14.2f}{daily_color}${daily_gain:<12.2f}{RESET}{daily_color}{f'{daily_pct:.2f}%':<14}{RESET}{pnl_color}${all_time_gain:<8.2f}{RESET} {pnl_color}{all_time_pct:>12.2f}%{RESET} {allocation_pct:>12.2f}%")
        else:
            print(f"  {ticker:<6}  {qty:<8} ${avg_cost * qty:<8.2f} ${avg_cost:<8.2f} N/A       N/A          N/A             N/A             N/A             N/A")
    
    for ticker, qty in holdings.items():
        if qty == 0:
            total_profit += realized_profits.get(ticker, 0) + dividends.get(ticker, 0)

    total_color = GREEN if total_profit >= 0 else RED
    total_value = total_cost + total_profit
    total_pct = (total_profit / total_cost) * 100 if total_cost > 0 else 0
    total_daily_pct = (total_daily_gain / (total_value - total_daily_gain)) * 100 if (total_value - total_daily_gain) > 0 else 0
    total_daily_color = GREEN if total_daily_gain >= 0 else RED


    print(f"\nTotal Portfolio value : ${total_value:.2f}")
    print(f"     Daily Gain       : {total_daily_color}${total_daily_gain:.2f} {total_daily_pct:.2f}%{RESET}")
    print(f"    Total Profit      : {total_color}${total_profit:.2f} {total_pct:.2f}%{RESET}")
    print("\n")

    if benchmark and ledger:
        try:
            first_date = ledger[0]["timestamp"][:10] 
            
            voo_history = yf.Ticker("VOO").history(start=first_date)
            
            if not voo_history.empty:
                voo_old = voo_history['Close'].iloc[0]
                voo_now = voo_history['Close'].iloc[-1]
                voo_pct = ((voo_now - voo_old) / voo_old) * 100
                
                beat_market = total_pct > voo_pct
                color = GREEN if beat_market else RED
                result_text = "BEATING" if beat_market else "TRAILING"
                
                print(f"S&P 500 Return (Since {first_date}): {voo_pct:.2f}% | You are {color}{result_text}{RESET} the market.")
                print("\n")
            else:
                print_error("Not enough benchmark data.")
        except Exception as e:
            print_error(f"Failed to fetch benchmark data: {e}")

    if ai_analysis and total_value > 0:
        analyze_portfolio(ai_allocations_string)



def export_csv():
    ledger = load_ledger()
    if not ledger:
        print("No transactions to export.")
        return

    filename = f"portfolio_export_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "action", "ticker", "quantity", "price", "total"])
        writer.writeheader()
        for entry in ledger:
            writer.writerow({
                "timestamp": entry["timestamp"],
                "action": entry["action"],
                "ticker": entry["ticker"],
                "quantity": entry["quantity"],
                "price": entry["price"],
                "total": entry["price"] if entry["action"] == "DIVIDEND" else entry["quantity"] * entry["price"]
            })
    print(f"{GREEN}Exported {len(ledger)} transactions to {filename}{RESET}")



