import ccxt
import numpy as np
import time

def fetch_live_trades(symbol='ETH/USDT'):
    """
    Connects to Binance and pulls the most recent tick data.
    """
    exchange = ccxt.binanceus({'enableRateLimit': True})
    
    # Fetch a fixed count rather than a time window first
    # This ensures we have enough points for the C++ engine to chew on
    raw_trades = exchange.fetch_trades(symbol, limit=500)
    
    if not raw_trades:
        return None, None

    ms_timestamps = np.array([t['timestamp'] for t in raw_trades])
    seconds_timestamps = ms_timestamps / 1000.0
    
    # Calculate the actual T (time from first trade to last trade)
    t0 = seconds_timestamps[0]
    normalized_timestamps = seconds_timestamps - t0
    T = normalized_timestamps[-1]
    
    # Safety Check: If 500 trades took 5 hours, T will be huge. 
    # If 500 trades took 2 minutes, T will be small (High Density).
    print(f"Captured {len(normalized_timestamps)} trades over {T:.2f} seconds.")
    
    return normalized_timestamps, T