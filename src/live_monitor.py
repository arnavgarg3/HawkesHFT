import matplotlib.pyplot as plt
import numpy as np
from live_fetcher import fetch_live_trades
from optimizer import fit_hawkes_model

def run_live_monitor():
    # 1. Grab the latest 1,000 trades from Binance
    timestamps, T = fetch_live_trades('BTC/USDT')
    
    # 2. Run your C++ optimized solver
    print("Analyzing market DNA...")
    params = fit_hawkes_model(timestamps, T)
    
    if not params:
        print("Optimization failed. Market might be too quiet.")
        return

    mu, alpha, beta = float(params["mu"]), float(params["alpha"]), float(params["beta"])
    n = alpha / beta  # Our Branching Ratio
    
    # 3. Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Top Plot: The actual trade arrivals (The "Ticks")
    ax1.vlines(timestamps, 0, 1, colors='blue', alpha=0.5, label='Trade Events')
    ax1.set_title(f"Live BTC/USDT Trade Arrivals (Last {len(timestamps)} trades)")
    ax1.set_ylabel("Occurence")
    
    # Bottom Plot: The Intensity Calculation
    # We'll plot a simplified intensity curve to show the "clustering"
    t_plot = np.linspace(0, T, 1000)
    intensity = np.full_like(t_plot, mu)
    for t_i in timestamps:
        # Add the jump and decay for each trade
        mask = t_plot > t_i
        intensity[mask] += alpha * np.exp(-beta * (t_plot[mask] - t_i))
        
    ax2.plot(t_plot, intensity, color='red', label='Hawkes Intensity (λ)')
    ax2.fill_between(t_plot, mu, intensity, color='red', alpha=0.2)
    ax2.set_title(f"Market Reflexivity Score (n): {n:.4f}")
    ax2.set_xlabel("Seconds from start of window")
    ax2.set_ylabel("Intensity (λ)")
    
    

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_live_monitor()