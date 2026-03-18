from stock_api import fetch_stock_history, calculate_changes
from ui import print_stock_info, print_error, RESET, draw_1y_chart, YELLOW
from AI import print_news
from Portfolio import buy_stock, sell_stock, show_history, remove_last, show_portfolio, export_csv, add_dividend


def process_input(user_input):
    parts = user_input.split()
    symbol = parts[0].upper()


    flags = [f.upper() for f in parts[1:]] if len(parts) > 1 else []
    
    print(f"Fetching stock price for {symbol}...")
    
    history = fetch_stock_history(symbol)
    if history is None or history.empty:
        print_error(f"No data found for {symbol.upper()}. Please check the symbol and try again.")
        return

    stock_data = calculate_changes(history)
    print_stock_info(symbol, stock_data)
    if "-CH" in flags:
        draw_1y_chart(symbol, history)
    if "-NEWS" in flags:
        print_news(symbol)

if __name__ == "__main__":
    try:
        welcome = "WELCOME TO THE TERMINAL STOCK TRACKER!"
        help_hint = "TYPE 'HELP' FOR AVAILABLE COMMANDS"
        print(f"\n{welcome.center(50)}")
        print(f"{help_hint.center(50)}\n")
        while True:
            cmd = input("Enter a command or US stock ticker: ").strip()
            parts = cmd.split()

            if not parts:
                continue
            command = parts[0].lower()
            args = [f.upper() for f in parts[1:]] if len(parts) > 1 else []

            if command in ['exit', 'quit', 'q']:
                print("Exiting the stock tracker. Goodbye!")
                break

            elif command == "help":
                header = "AVAILABLE COMMANDS"
                print(f"\n{header.center(70)}")
                print("=" * 80)
                print(f"\n{YELLOW}    {'<Ticker>':<34}{RESET} : Fetch stock information\n")
                print(f"{YELLOW}    {'<Ticker> -NEWS':<34}{RESET} : Get stock info + AI news summary\n")
                print(f"{YELLOW}    {'<Ticker> -CH':<34}{RESET} : Get stock info + Plot 1Y chart\n")
                print(f"{YELLOW}    {'BUY <Ticker> <Amt> <Price> [Date]':<34}{RESET} : Add a BUY transaction (Date: YYYY-MM-DD, optional)\n")
                print(f"{YELLOW}    {'SELL <Ticker> <Amt> <Price> [Date]':<34}{RESET} : Add a SELL transaction (Date: YYYY-MM-DD, optional)\n")
                print(f"{YELLOW}    {'DIVIDEND <Ticker> <Amount>':<34}{RESET} : Record a dividend payment\n")
                print(f"{YELLOW}    {'PORTFOLIO':<34}{RESET} : View current holdings, average cost, and Profit\n")
                print(f"{YELLOW}    {'PORTFOLIO -AI':<34}{RESET} : View current holdings, average cost, and Profit + AI Portfolio Analysis\n")
                print(f"{YELLOW}    {'PORTFOLIO -VS':<34}{RESET} : View current holdings, average cost, and Profit + Compare vs S&P 500\n")
                print(f"{YELLOW}    {'EXPORT':<34}{RESET} : Export transaction history to CSV\n")
                print(f"{YELLOW}    {'HISTORY':<34}{RESET} : Show full transaction history\n")
                print(f"{YELLOW}    {'HISTORY <Ticker> [<Ticker>...]':<34}{RESET} : Filter history by ticker(s)\n")
                print(f"{YELLOW}    {'REMOVE':<34}{RESET} : Remove last transaction (undo)\n")
                print(f"{YELLOW}    {'HELP':<34}{RESET} : Show this help menu\n")
                print(f"{YELLOW}    {'EXIT / QUIT / Q':<34}{RESET} : Exit the program\n")
                print("-" * 80)
                print("\n    EXAMPLES:")
                print("      VOO")
                print("      VOO -CH -NEWS")
                print("      BUY VOO 1.57 593.32 2025-01-15")
                print("      SELL VOO 0.50 615.10")
                print("      SELL VOO 0.50 615.10 2025-06-01")
                print("      PORTFOLIO -AI -VS")
                print("      EXPORT")
                print("      HISTORY")
                print("      HISTORY VOO")
                print("      HISTORY VOO AAPL")
                print("      REMOVE\n")
                print("=" * 80)
                print()

            elif command == "buy":
                if len(args) not in [3, 4]:
                    print_error("Usage: BUY <Ticker> <Amount> <Price> [YYYY-MM-DD] | Example: BUY VOO 1.57 593.32 2025-01-15")
                    continue
                try:
                    ticker, qty, price = args[0], round(float(args[1]), 4), round(float(args[2]), 2)
                    date_str = args[3] if len(args) == 4 else None
                    buy_stock(ticker, qty, price, date_str)
                except ValueError:
                    print_error("Usage: BUY <Ticker> <Amount> <Price> [YYYY-MM-DD] | Example: BUY VOO 1.57 593.32 2025-01-15")

            elif command == "sell":
                if len(args) not in [3, 4]:
                    print_error("Usage: SELL <Ticker> <Amount> <Price> [YYYY-MM-DD] | Example: SELL VOO 0.50 615.10 2025-06-01")
                    continue
                try:
                    ticker, qty, price = args[0], round(float(args[1]), 4), round(float(args[2]), 2)
                    date_str = args[3] if len(args) == 4 else None
                    sell_stock(ticker, qty, price, date_str)
                except ValueError:
                    print_error("Usage: SELL <Ticker> <Amount> <Price> [YYYY-MM-DD] | Example: SELL VOO 0.50 615.10 2025-06-01")

            elif command == "dividend":
                if len(args) not in [2, 3]:
                    print_error("Invalid input for DIVIDEND command. Usage: DIVIDEND <Ticker> <Amount> [YYYY-MM-DD] | Example: DIVIDEND VOO 1.57 2025-01-15")
                    continue
                try:
                    ticker, amount = args[0].upper(), round(float(args[1]), 2)
                    date_str = args[2] if len(args) == 3 else None
                    add_dividend(ticker, amount, date_str)
                except ValueError:
                    print_error("Invalid input for DIVIDEND command. Usage: DIVIDEND <Ticker> <Amount> [YYYY-MM-DD] | Example: DIVIDEND VOO 1.57 2025-01-15")

            elif command == "history":
                if not args:
                    show_history()
                else:
                    tickers = [a.upper() for a in args]
                    show_history(tickers)

            elif command == "remove":
                remove_last()

            elif command == "portfolio":
                show_portfolio(ai_analysis="-AI" in args, benchmark="-VS" in args)
            
            elif command == "export":
                export_csv()

            elif cmd:
                process_input(cmd)
    except KeyboardInterrupt:
        print("\nExiting the stock tracker. Goodbye!")
