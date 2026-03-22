import numpy as np
import time
from simulator import simulate_hawkes
from optimizer import fit_hawkes_model

def run_calibration():
    # 1. SET THE 'TRUE' PARAMETERS
    # mu (baseline), alpha (impact), beta (decay)
    true_mu = 0.2
    true_alpha = 0.5
    true_beta = 0.8  # Branching ratio n = 0.625 (Stable)
    T = 2000         # Simulate 2000 seconds of trading
    
    print(f"--- Starting Calibration Test ---")
    print(f"Targeting: mu={true_mu}, alpha={true_alpha}, beta={true_beta}")
    
    # 2. GENERATE SYNTHETIC DATA
    start_sim = time.time()
    timestamps = simulate_hawkes(true_mu, true_alpha, true_beta, T)
    sim_duration = time.time() - start_sim
    
    print(f"Generated {len(timestamps)} events in {sim_duration:.2f}s")
    
    # 3. RUN THE OPTIMIZER (THE BLIND GUESS)
    print("Fitting model to data...")
    start_fit = time.time()
    estimates = fit_hawkes_model(timestamps, T)
    fit_duration = time.time() - start_fit
    
    # 4. SHOW THE RESULTS
    if estimates:
        print(f"\n--- Results (Solved in {fit_duration:.2f}s) ---")
        print(f"MU:    True: {true_mu:<6} | Estimated: {estimates['mu']:.4f}")
        print(f"ALPHA: True: {true_alpha:<6} | Estimated: {estimates['alpha']:.4f}")
        print(f"BETA:  True: {true_beta:<6} | Estimated: {estimates['beta']:.4f}")
        
        # Check the Branching Ratio
        true_n = true_alpha / true_beta
        print(f"N (Reflexivity): True: {true_n:.3f} | Estimated: {estimates['n']:.3f}")
        
        # Calculate Error
        error = np.abs(estimates['n'] - true_n) / true_n
        if error < 0.1: # Within 10%
            print("\n✅ CALIBRATION SUCCESS: The engine recovered the parameters!")
        else:
            print("\n⚠️ CALIBRATION TOLERANCE: The estimate is off. Consider a longer simulation time (T).")
    else:
        print("❌ CALIBRATION FAILED: Optimizer could not find a solution.")

if __name__ == "__main__":
    run_calibration()