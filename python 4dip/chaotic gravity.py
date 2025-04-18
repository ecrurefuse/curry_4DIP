# 4DIP Convergence Test: Chaotic 3-Body Gravitational System with Lorentz-like Perturbation

from sympy import symbols, Matrix, diff, simplify
from mpmath import mp, norm
import numpy as np

# Set high-precision
mp.dps = 50

# Constants and parameters
G = mp.mpf('1.0')   # Gravitational constant
epsilon = mp.mpf('0.01')  # Lorentz perturbation strength
B = Matrix([0, 0, 1])  # Magnetic field vector (z direction)

# Masses and initial positions/velocities for 3 bodies
m = [mp.mpf('1.0'), mp.mpf('1.0'), mp.mpf('1.0')]

r = [Matrix([mp.mpf('1.0'), mp.mpf('0.0'), mp.mpf('0.0')]),
     Matrix([mp.mpf('-0.5'), mp.mpf('0.866'), mp.mpf('0.0')]),
     Matrix([mp.mpf('-0.5'), mp.mpf('-0.866'), mp.mpf('0.0')])]

v = [Matrix([mp.mpf('0.0'), mp.mpf('1.0'), mp.mpf('0.0')]),
     Matrix([mp.mpf('-0.866'), mp.mpf('-0.5'), mp.mpf('0.0')]),
     Matrix([mp.mpf('0.866'), mp.mpf('-0.5'), mp.mpf('0.0')])]

# Compute acceleration due to gravity + Lorentz-like force
a = []
for i in range(3):
    a_i = Matrix([0, 0, 0])
    for j in range(3):
        if i != j:
            delta = r[i] - r[j]
            r_norm = mp.sqrt(sum(float(comp)**2 for comp in delta)) + 1e-8  # avoid singularity
            a_i += -G * m[j] * delta / (r_norm**3)
    # Add Lorentz-like force: epsilon * (v_i x B)
    a_i += epsilon * v[i].cross(B)
    a.append(simplify(a_i))

# Flatten all components into a residual vector F_n
F_n_vec = Matrix([comp for vec in a for comp in vec])

# Evaluate numerically
F_n_mp = Matrix([mp.mpf(str(val)) for val in F_n_vec])

# 4DIP initialization
G_n = Matrix([0.99 * val for val in F_n_mp])
gamma = mp.mpf('0.98')
residuals = []

print("=== 4DIP: Chaotic 3-Body Gravitational System ===")

# Run iteration
for step in range(2000):
    R_n = F_n_mp - G_n
    res_norm = norm([float(val) for val in R_n])
    residuals.append(float(res_norm))
    print(f"Iteration {step}: Residual Norm = {float(res_norm):.6e}")
    if res_norm < 1e-14:
        print("Converged below 1e-14.")
        break
    G_n = F_n_mp - gamma * R_n