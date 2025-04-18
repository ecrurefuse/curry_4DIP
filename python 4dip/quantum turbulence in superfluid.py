# 4DIP Convergence Test: Quantum Turbulence in Superfluids (Gross-Pitaevskii Equation with Noise)

from sympy import symbols, Function, I, Abs, Matrix, simplify, diff
from mpmath import mp, mpc, norm
import random

# Set high precision
mp.dps = 50

# Define variables
x, t = symbols('x t')
psi = Function('psi')(t, x)

# Parameters
V = symbols('V')  # interaction strength

# Gross-Pitaevskii equation with stochastic noise term
# i * d/dt psi = -1/2 * d^2/dx^2 psi + V * |psi|^2 * psi + epsilon(t, x)
psi_t = diff(psi, t)
psi_xx = diff(psi, x, x)
abs_psi_squared = Abs(psi)**2
noise_term = Function('epsilon')(t, x)

# Define the field equation
F_n_sym = I * psi_t + (1/2) * psi_xx - V * abs_psi_squared * psi - noise_term

# Substitution dictionary (simulate psi and epsilon numerically)
subs = {
    psi: 1 + I*0.5,               # complex wavefunction
    diff(psi, t): 0.1 + I*0.05,
    diff(psi, x, x): -0.2 + I*0.1,
    V: 1.0,
    noise_term: random.gauss(0, 0.001) + I * random.gauss(0, 0.001)
}

# Evaluate F_n
F_n_eval = F_n_sym.subs(subs).evalf(mp.dps)
F_n_mp = mpc(F_n_eval.evalf())

# 4DIP setup
G_n = 0.99 * F_n_mp
gamma = mp.mpf('0.98')
residuals = []

print("=== 4DIP: Quantum Turbulence in Superfluid ===")

# Iterate until convergence
for step in range(2000):
    R_n = F_n_mp - G_n
    res_norm = abs(R_n)
    residuals.append(float(res_norm))
    print(f"Iteration {step}: Residual Norm = {float(res_norm):.6e}")
    if res_norm < 1e-14:
        print("Converged below 1e-14.")
        break
    G_n = F_n_mp - gamma * R_n
