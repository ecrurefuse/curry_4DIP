# Relativistic MHD symbolic system with 4DIP convergence using sympy and mpmath

from sympy import symbols, Function, Matrix, diff, simplify, diag, IndexedBase
from sympy.abc import t, x, y, z
from mpmath import mp

# Set precision to 50 digits
mp.dps = 50

# Coordinate list
coords = [t, x, y, z]

# Define physical symbols
rho, p, alpha = symbols('rho p alpha')  # density, pressure, nonlinearity strength
u = IndexedBase('u')       # 4-velocity u^mu
B = IndexedBase('B')       # magnetic field B^i (spatial only)
F = IndexedBase('F')       # electromagnetic tensor F^{mu nu}
J = IndexedBase('J')       # current density J^nu
epsilon = IndexedBase('epsilon')  # noise or fluctuation term ε^ν

# Minkowski metric tensor η^{μν} = diag(-1, 1, 1, 1)
eta = diag(-1, 1, 1, 1)

# Magnetic field squared norm B² = B^i B_i (spatial part only)
B_sq = sum(B[i] * B[i] for i in range(1, 4))  # i = 1, 2, 3

# Build energy-momentum tensor T^{μν}
T_expr = {}
for mu in range(4):
    for nu in range(4):
        term1 = (rho + p + B_sq) * u[mu] * u[nu]
        term2 = (p + 0.5 * B_sq) * eta[mu, nu]
        term3 = -B[mu] * B[nu] if mu in range(1, 4) and nu in range(1, 4) else 0
        T_expr[(mu, nu)] = simplify(term1 + term2 + term3)

# Compute divergence ∂_μ T^{μν}
div_T = []
for nu in range(4):
    result = sum(diff(T_expr[(mu, nu)], coords[mu]) for mu in range(4))
    div_T.append(simplify(result))

# Add nonlinear penalty (∇·B)^2
nonlinear_penalty = alpha * sum(diff(B[i], coords[i])**2 for i in range(1, 4))
div_T = [div_T[i] + nonlinear_penalty for i in range(4)]

# Compute divergence of F^{μν} - J^ν + ε^ν
div_F = []
for nu in range(4):
    result = sum(diff(F[mu, nu], coords[mu]) for mu in range(4))
    div_F.append(simplify(result - J[nu] + epsilon[nu]))

# Combine into full residual vector F_n
F_n = div_T + div_F  # 8-component vector

# Initialize G_0 with a 1% offset
G_n = [0.99 * f for f in F_n]

# Set contraction factor γ
gamma = mp.mpf('0.98')

# Run 5 symbolic iterations of 4DIP
print("=== 4DIP Iteration: Symbolic Relativistic MHD ===")
for step in range(5):
    R_n = [F_n[i] - G_n[i] for i in range(8)]
    G_n = [F_n[i] - gamma * R_n[i] for i in range(8)]

    print(f"\nIteration {step}")
    for i in range(8):
        print(f"  R[{i}] = {R_n[i]}")
