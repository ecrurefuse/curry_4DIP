# Inverse-Square Gravity Force Test (Capped)

import numpy as np
import time

def log_gravity_result(force, energy, iterations, t, start_time):
    print(f"\n--- Gravity Test ---")
    print(f"Final Force: {force:.14e} N")
    print(f"Final Energy: {energy:.14e}")
    print(f"Iterations: {iterations}")
    print(f"Simulated Time: {t:.6f} s")
    print(f"Runtime: {time.time() - start_time:.6f} s")
    print("------------------------------")

# Constants
G = 6.67430e-11  # gravitational constant (m^3/kg/s^2)
M = 5.972e24  # mass of Earth (kg)
r = 1.0  # distance (m)

def gravity_force(G, M, r):
    return G * M / r**2

def gravity_energy(force, distance):
    return force * distance

# Initialization
force = gravity_force(G, M, r)
energy = gravity_energy(force, r)
iterations = 0
t = 0.0
max_iter = 200000
precision_threshold = 1e-14
energy_log = [energy]
start_time = time.time()

# Main loop
while iterations < max_iter:
    prev_energy = energy_log[-1]
    force = gravity_force(G, M, r)
    energy = gravity_energy(force, r)
    energy_log.append(energy)
    t += 0.01
    iterations += 1
    if abs(energy - prev_energy) < precision_threshold:
        break

log_gravity_result(force, energy, iterations, t, start_time)

