import pandas as pd
import numpy as np

def load_binance_ticks(csv_path):
    """
    Loads Binance trade CSV and returns normalized timestamps in seconds.
    """
    # Binance columns: trade_id, price, qty, quote_qty, time, is_buyer_maker
    df = pd.read_csv(csv_path, names=['id', 'price', 'qty', 'quote_qty', 'time', 'is_maker'])
    
    # 1. Convert ms to seconds
    raw_times = df['time'].values / 1000.0
    
    # 2. Normalize so the first trade is at time 0
    t0 = raw_times[0]
    timestamps = raw_times - t0
    
    # 3. Get total duration T
    T = timestamps[-1]
    
    print(f"Loaded {len(timestamps)} trades over {T/60:.2f} minutes.")
    return timestamps, T