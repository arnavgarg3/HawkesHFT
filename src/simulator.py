import numpy as np

def simulate_hawkes(mu, alpha, beta, T):
    """
    Generates a sequence of timestamps for a Hawkes Process.
    ogata thinning algorithm
    mu:    The baseline intensity (how often trades happen randomly)
    alpha: The jump size (how much one trade excites the others)
    beta:  The decay rate (how fast the excitement fades)
    T:     The total time duration to simulate (in seconds)
    """
    t = 0
    timestamps = []
    
    # We start with the maximum possible intensity, which is just mu
    # This is our 'ceiling' for generating candidate events
    lambda_upper = mu
    
    while t < T:
        # 1. Generate a candidate time step from a Poisson process
        u1 = np.random.uniform(0, 1)
        dt = -np.log(u1) / lambda_upper
        t += dt
        
        if t >= T:
            break
            
        # 2. Calculate the ACTUAL intensity at this exact moment
        # lambda(t) = mu + sum( alpha * exp(-beta * (t - ti)) )
        actual_lambda = mu
        for ti in timestamps:
            actual_lambda += alpha * np.exp(-beta * (t - ti))
            
        # 3. Acceptance/Rejection step (Thinning)
        u2 = np.random.uniform(0, 1)
        if u2 <= actual_lambda / lambda_upper:
            # We accept the event!
            timestamps.append(t)
            # After a jump, the new intensity 'ceiling' increases by alpha
            lambda_upper = actual_lambda + alpha
        else:
            # We reject the event, but we lower our ceiling for the next step
            # to make the simulation more efficient
            lambda_upper = actual_lambda
            
    return np.array(timestamps)