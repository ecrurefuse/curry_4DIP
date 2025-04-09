
# Lorenz Attractor - Practical and Theoretical Tier 5 Convergence Test

import numpy as np
import time

def log_lorenz_result(label, state, energy, iterations, t, start_time):
    print(f"\n--- Lorenz {label} ---")
    print(f"Final State: {state}")
    print(f"Final Energy: {energy:.14e}")
    print(f"Iterations: {iterations}")
    print(f"Simulated Time: {t:.6f} s")
    print(f"Runtime: {time.time() - start_time:.6f} s")
    print("------------------------------")

def lorenz_dynamics(state, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])

def energy(state):
    return np.sum(np.square(state))

def dE_dt(state):
    grad = 2 * state
    f = lorenz_dynamics(state)
    return np.dot(grad, f)

def run_lorenz_test(boosted=False):
    state = np.array([1.0, 1.0, 1.0])
    dt = 0.001
    t = 0.0
    iterations = 0
    max_iter = 200000
    precision_threshold = 1e-14
    energy_log = [energy(state)]
    start_time = time.time()

    while iterations < max_iter:
        prev_energy = energy_log[-1]
        dEdt = dE_dt(state)
        eta = max(0.0, dEdt / (prev_energy + 1e-12))
        if boosted:
            eta *= 2.0  # Practical mode: Boosted damping

        f = lorenz_dynamics(state) - eta * state
        state = state + f * dt
        t += dt
        iterations += 1

        curr_energy = energy(state)
        energy_log.append(curr_energy)
        if abs(curr_energy - prev_energy) < precision_threshold:
            break

    label = "Practical" if boosted else "Theoretical"
    log_lorenz_result(label, state, curr_energy, iterations, t, start_time)

# Run both versions
run_lorenz_test(boosted=True)
run_lorenz_test(boosted=False)
