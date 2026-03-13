RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def format_percentage(value):
    if value >= 0:
        return f"{GREEN}+{value:.2f}%{RESET}"
    else:
        return f"{RED}{value:.2f}%{RESET}"

def print_error(message):
    print(f"{RED}{message}{RESET}")

def print_stock_info(symbol, data):
    if not data:
        print_error(f"Error fetching data for {symbol.upper()}. Please check the symbol and try again.")
        return

    current_price = data["current_price"]
    daily_change = format_percentage(data["daily_change"])

    print(f"\n--- {symbol.upper()} ---")
    print(f"Price: ${current_price:.2f}   [{daily_change}]")

    for label, change in data["historical_changes"].items():
        if change is not None:
            formatted_change = format_percentage(change)
            print(f"{label:<9}: {formatted_change}")
        else:
            print_error(f"{label:<9}: Not enough historical data")