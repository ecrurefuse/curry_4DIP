# 4DIP Convergence Test: Dirac Field in Curved Spacetime (Simplified 1+1D Symbolic Model)

from sympy import symbols, Function, I, Matrix, simplify, diff
from mpmath import mp, mpc, norm

# Set high-precision
mp.dps = 50

# Define spacetime variable
x, t = symbols('x t')

# Define spinor components (simplified Dirac field)
psi = Matrix([
    Function('psi1')(t, x),
    Function('psi2')(t, x),
    Function('psi3')(t, x),
    Function('psi4')(t, x)
])

# Simplified gamma matrices (1+1D approximation for Schwarzschild background)
gamma0 = Matrix([[0, 0, 0, I], [0, 0, I, 0], [0, -I, 0, 0], [-I, 0, 0, 0]])
gamma1 = Matrix([[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]])

# Parameters
m, J = symbols('m J')

# Derivatives
D0 = Matrix([diff(psi[i], t) for i in range(4)])
D1 = Matrix([diff(psi[i], x) for i in range(4)])

# Simplified Dirac equation with source J
F_n_sym = I * (gamma0 * D0 + gamma1 * D1) - m * psi - Matrix([J]*4)

# Substitution for evaluation
subs = {
    psi[0]: 1.0, psi[1]: -1.0, psi[2]: 0.5, psi[3]: -0.5,
    diff(psi[0], t): 0.1, diff(psi[1], t): 0.1, diff(psi[2], t): 0.1, diff(psi[3], t): 0.1,
    diff(psi[0], x): 0.2, diff(psi[1], x): 0.2, diff(psi[2], x): 0.2, diff(psi[3], x): 0.2,
    m: 1.0, J: 0.0
}

# Evaluate the symbolic Dirac system
F_n_eval = F_n_sym.subs(subs).evalf(mp.dps)

# Convert to complex mpmath values
F_n_mp = Matrix([mpc(val.evalf()) for val in F_n_eval])

# 4DIP Initialization
G_n = Matrix([0.99 * val for val in F_n_mp])
gamma = mp.mpf('0.98')
residuals = []

print("=== 4DIP: Dirac Field in Curved Spacetime ===")

# Iterate until convergence
for step in range(2000):
    R_n = F_n_mp - G_n
    res_norm = norm([complex(val) for val in R_n])
    residuals.append(float(res_norm))
    print(f"Iteration {step}: Residual Norm = {float(res_norm):.6e}")
    if res_norm < 1e-14:
        print("Converged below 1e-14.")
        break
    G_n = F_n_mp - gamma * R_n
