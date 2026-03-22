from data_loader import load_binance_ticks
from optimizer import fit_hawkes

# Load real BTC trades from a CSV you downloaded
timestamps, T = load_binance_ticks("BTCUSDT-trades-2026-03-01.csv")

# Fit the model to find the market's "DNA"
params = fit_hawkes(timestamps, T)

if params:
    print(f"Market Reflexivity (n): {params['alpha']/params['beta']:.4f}")
    if (params['alpha']/params['beta']) > 0.8:
        print("⚠️ WARNING: High self-excitation detected. Market is fragile.")