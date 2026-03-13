from stock_api import fetch_stock_history, calculate_changes
from ui import print_stock_info, print_error

def process_input(user_input):
    # Future enhancement: Look for flags like -NEWS here
    parts = user_input.split()
    symbol = parts[0]
    
    print(f"Fetching stock price for {symbol}...")
    
    history = fetch_stock_history(symbol)
    if history is None or history.empty:
        print_error(f"No data found for {symbol.upper()}. Please check the symbol and try again.")
        return

    stock_data = calculate_changes(history)
    print_stock_info(symbol, stock_data)

if __name__ == "__main__":
    try:
        while True:
            cmd = input("Enter a US stock ticker (or 'exit' to quit): ").strip()
            if cmd.lower() == 'exit':
                print("Exiting the stock tracker. Goodbye!")
                break
            if cmd:
                process_input(cmd)
    except KeyboardInterrupt:
        print("\nExiting the stock tracker. Goodbye!")
