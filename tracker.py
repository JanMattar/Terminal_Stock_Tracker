from stock_api import fetch_stock_history, calculate_changes
from ui import print_stock_info, print_error
from AI_News import print_news


def process_input(user_input):
    # Future enhancement: Look for flags like -NEWS here
    parts = user_input.split()
    symbol = parts[0]
    flags = parts[1:] if len(parts) > 1 else []
    
    print(f"Fetching stock price for {symbol}...")
    
    history = fetch_stock_history(symbol)
    if history is None or history.empty:
        print_error(f"No data found for {symbol.upper()}. Please check the symbol and try again.")
        return

    stock_data = calculate_changes(history)
    print_stock_info(symbol, stock_data)
    NEWS = "-NEWS" == flags[0] if flags else False
    print_news(NEWS, symbol)

if __name__ == "__main__":
    try:
        welcome = "WELCOME TO THE TERMINAL STOCK TRACKER!"
        help_hint = "TYPE 'HELP' FOR AVAILABLE COMMANDS"
        print(f"\n{welcome.center(50)}")
        print(f"{help_hint.center(50)}\n")
        while True:
            cmd = input("Enter a US stock ticker: ").strip()
            parts = cmd.split()
            symbol = parts[0]
            flags = parts[1:] if len(parts) > 1 else []

            if symbol.lower() in ['exit', 'quit', 'q']:
                print("Exiting the stock tracker. Goodbye!")
                break
            elif symbol == "help":
                header = "AVAILABLE COMMANDS"
                print(f"\n{header.center(50)}")
                print("=" * 50)
                print(f"{'<symbol>':<20} : Fetch stock information for a given symbol")
                print(f"{'<symbol> -NEWS':<20} : Fetch news related to the stock")
                print(f"{'exit/quit/q':<20} : Exit the stock tracker")
                print(f"{'help':<20} : Display this help message")
                print("=" * 50)
                print("\n")
            elif cmd:
                process_input(cmd)
    except KeyboardInterrupt:
        print("\nExiting the stock tracker. Goodbye!")
