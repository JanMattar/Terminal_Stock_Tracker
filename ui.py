import plotext as plt

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
YELLOW = "\033[93m"

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

    print(f"\n{'--- ' + symbol.upper() + ' ---':^14}")
    print(f"{'Price: $' + f'{current_price:.2f}':<15} [{daily_change}]")

    for label, change in data["historical_changes"].items():
        if change is not None:
            formatted_change = format_percentage(change)
            print(f"{label:<9}: {formatted_change}")
        else:
            print_error(f"{label:<9}: Not enough historical data")
    print()

def draw_1y_chart(ticker, history):
    if history is None or history.empty:
        return

    recent_history = history.tail(252)
    dates = recent_history.index.strftime('%d/%m/%Y').tolist()
    prices = recent_history['Close'].tolist()

    plt.clf()
    plt.theme('clear')
    plt.plot(dates, prices, color='cyan')
    plt.title(f"{ticker.upper()} - 1 Year Performance")
    plt.plotsize(150, 25)

    print()
    plt.show()
    print()