import yfinance as yf
import os
from contextlib import redirect_stdout, redirect_stderr

def fetch_stock_history(symbol):
    ticker = yf.Ticker(symbol)
    with open(os.devnull, 'w') as devnull:
        with redirect_stderr(devnull), redirect_stdout(devnull):
            history = ticker.history(period="5y")
    return history

def calculate_changes(history):
    if history.empty:
        return None

    try:
        current_price = history['Close'].iloc[-1]
        prev_close = history['Close'].iloc[-2]
    except Exception:
        return None

    daily_percent_change = ((current_price - prev_close) / prev_close) * 100

    time_frames = {
        "1 Week": 6, 
        "1 Month": 22,
        "6 Months": 127,
        "1 Year": 253,
        "5 Years": 1265
    }

    historical_changes = {}
    for label, days in time_frames.items():
        if len(history) >= days:
            old_price = history['Close'].iloc[-days]
            percent_change = ((current_price - old_price) / old_price) * 100
            historical_changes[label] = percent_change
        else:
            historical_changes[label] = None

    return {
        "current_price": current_price,
        "daily_change": daily_percent_change,
        "historical_changes": historical_changes
    }