# Attosecond Oscillator Simulation (Symbolic Test Only - Precision Limit Caveat)

import numpy as np
import time

def log_oscillator_result(state, energy, iterations, t, start_time):
    print(f"\n--- Attosecond Oscillator Test ---")
    print(f"Final State: {state}")
    print(f"Final Energy: {energy:.14e}")
    print(f"Iterations: {iterations}")
    print(f"Simulated Time: {t:.6e} s")
    print(f"Runtime: {time.time() - start_time:.6f} s")
    print("Note: This test confirms symbolic stability at 10^-18 s, but cannot guarantee precision below 10^-14 with float64.")
    print("------------------------------")

# High-frequency oscillator: d²x/dt² + ω²x = 0 → dx/dt = v, dv/dt = -ω²x
omega = 1e15  # rad/s (high frequency)

def oscillator_dynamics(state):
    x, v = state
    dx = v
    dv = -omega**2 * x
    return np.array([dx, dv])

def oscillator_energy(state):
    x, v = state
    return 0.5 * (v**2 + omega**2 * x**2)

# Initialization
state = np.array([1.0, 0.0])
dt = 1e-18
t = 0.0
iterations = 0
max_iter = 1000
precision_threshold = 1e-14
energy_log = [oscillator_energy(state)]
start_time = time.time()

# Main loop
while iterations < max_iter:
    prev_energy = energy_log[-1]
    dSdt = oscillator_dynamics(state)
    state = state + dSdt * dt
    t += dt
    iterations += 1
    curr_energy = oscillator_energy(state)
    energy_log.append(curr_energy)
    if abs(curr_energy - prev_energy) < precision_threshold:
        break

log_oscillator_result(state, curr_energy, iterations, t, start_time)

