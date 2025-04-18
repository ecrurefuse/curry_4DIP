# 4DIP Convergence Test: Relativistic Magnetohydrodynamics (MHD)

from sympy import symbols, IndexedBase, Matrix, diff, simplify
from mpmath import mp, norm

# Set high precision
mp.dps = 50

# Define spacetime and index range
coords = symbols('t x y z')
mu = range(4)  # 0=t, 1=x, 2=y, 3=z

# Define fields
T = IndexedBase('T')   # Energy-momentum tensor T^{mu nu}
F = IndexedBase('F')   # Electromagnetic tensor F^{mu nu}
J = IndexedBase('J')   # Four-current J^nu

# Create symbolic divergence of T^{mu nu} and F^{mu nu}
div_T = []
div_F = []
for nu in mu:
    div_T_expr = 0
    div_F_expr = -J[nu]  # ∂_μ F^{μν} = J^ν
    for mu_idx in mu:
        coord = coords[mu_idx]
        div_T_expr += diff(T[mu_idx, nu], coord)
        div_F_expr += diff(F[mu_idx, nu], coord)
    div_T.append(div_T_expr)
    div_F.append(div_F_expr)

# Full target field vector F_n (symbolic form)
F_n_sym = Matrix(div_T + div_F)  # 8 components: 4 from T, 4 from F

# Substitute sample numerical values
subs = {}
for mu_idx in mu:
    for nu_idx in mu:
        T_idx = (mu_idx, nu_idx)
        F_idx = (mu_idx, nu_idx)
        subs[T[T_idx]] = 1.0 + 0.1 * mu_idx + 0.01 * nu_idx
        subs[F[F_idx]] = 0.5 - 0.02 * mu_idx + 0.005 * nu_idx
    subs[J[mu_idx]] = 0.1 * mu_idx

# Evaluate F_n numerically
F_n_eval = F_n_sym.subs(subs).evalf(mp.dps)
F_n_mp = Matrix([mp.mpf(str(val)) for val in F_n_eval])

# Initialize 4DIP
G_n = Matrix([0.99 * val for val in F_n_mp])
gamma = mp.mpf('0.98')
residuals = []

print("=== 4DIP: Relativistic MHD ===")

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
