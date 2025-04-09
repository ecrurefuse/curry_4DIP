# 2×2 Matrix System Simulation with Tier 5 Convergence

import numpy as np
import time

def log_matrix_result(matrix, energy, iterations, t, start_time):
    print(f"\n--- 2×2 Matrix System ---")
    print("Final Matrix State:")
    print(matrix)
    print(f"Final Energy: {energy:.14e}")
    print(f"Iterations: {iterations}")
    print(f"Simulated Time: {t:.6f} s")
    print(f"Runtime: {time.time() - start_time:.6f} s")
    print("------------------------------")

# Define the decay system: dM/dt = -kM (element-wise)
k = 0.1

def matrix_dynamics(M):
    return -k * M

def matrix_energy(M):
    return np.sum(M**2)

# Initialization
matrix = np.array([[1.0, 0.5], [0.5, 1.0]])
dt = 0.001
t = 0.0
iterations = 0
max_iter = 200000
precision_threshold = 1e-14
energy_log = [matrix_energy(matrix)]
start_time = time.time()

# Main simulation loop
while iterations < max_iter:
    prev_energy = energy_log[-1]
    dMdt = matrix_dynamics(matrix)
    matrix = matrix + dMdt * dt
    t += dt
    iterations += 1
    curr_energy = matrix_energy(matrix)
    energy_log.append(curr_energy)
    if abs(curr_energy - prev_energy) < precision_threshold:
        break

log_matrix_result(matrix, curr_energy, iterations, t, start_time)

