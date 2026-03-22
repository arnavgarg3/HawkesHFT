import numpy as np
from scipy.optimize import minimize
import hawkes_engine

def fit_hawkes_model(timestamps, T):
    """
    Finds the best mu, alpha, and beta for a given set of trade times.
    """
    def objective_function(params):
        mu, alpha, beta = params
      
        r_vec = hawkes_engine.compute_r_vector(timestamps, beta)
        obj = hawkes_engine.log_likelihood(T, mu, alpha, beta, r_vec, timestamps)
        return obj

    # 2. THE BOUNDS: mu, alpha, and beta must be positive (> 0)
    # We use 1e-6 instead of 0 to prevent division-by-zero errors
    bounds = [(1e-6, 1.0), (1e-6, 0.9), (0.1, 5)]

    # 3. THE STABILITY CONSTRAINT: alpha < beta (so n < 1)
    # This ensures the market doesn't "explode" to infinity
    def stability_constraint(params):
        mu, alpha, beta = params
        return beta - alpha  # SciPy keeps this >= 0

    constraints = {'type': 'ineq', 'fun': stability_constraint}

    initial_guess = [len(timestamps)/T, 0.5, 1.0]

    result = minimize(
        objective_function, 
        initial_guess, 
        method='SLSQP', 
        bounds=bounds, 
        constraints=constraints
    )

    if result.success:
        return {
            'mu': result.x[0],
            'alpha': result.x[1],
            'beta': result.x[2],
            'n': result.x[1] / result.x[2]  # The Branching Ratio
        }
    else:
        print("Optimization failed:", result.message)
        return None