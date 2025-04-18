# Triple Pendulum simulated with symbolic ODEs and 4DIP convergence using mpmath

from sympy import symbols, Function, diff, simplify, sin, cos, Matrix
from sympy.abc import t
from mpmath import mp, norm

# Set high precision for Tier 7+ convergence
mp.dps = 50

# Define physical parameters
m1, m2, m3 = 1, 1, 1       # masses
l1, l2, l3 = 1, 1, 1       # lengths
g = 9.81                  # gravity

# Angular positions (generalized coordinates)
th1 = Function('th1')(t)
th2 = Function('th2')(t)
th3 = Function('th3')(t)

# First and second derivatives
th1d = diff(th1, t)
th2d = diff(th2, t)
th3d = diff(th3, t)
th1dd = diff(th1d, t)
th2dd = diff(th2d, t)
th3dd = diff(th3d, t)

# Approximate symbolic equations of motion (simplified for testing)
F1 = m1 * l1**2 * th1dd + m2 * l1 * l2 * th2dd * cos(th1 - th2) + g * l1 * sin(th1)
F2 = m2 * l2**2 * th2dd + m3 * l2 * l3 * th3dd * cos(th2 - th3) + g * l2 * sin(th2)
F3 = m3 * l3**2 * th3dd + g * l3 * sin(th3)

# Residual vector F_n
F_n = Matrix([F1, F2, F3])

# Substitute numerical initial conditions for angles, velocities, accelerations
subs = {
    th1: 0.1, th2: 0.1, th3: 0.1,
    th1d: 0, th2d: 0, th3d: 0,
    th1dd: 0, th2dd: 0, th3dd: 0
}

# Evaluate F_n at initial state with high precision
F_n_evaluated = F_n.subs(subs).evalf(mp.dps)
F_n_mp = Matrix([mp.mpf(str(val)) for val in F_n_evaluated])

# Initialize guess G_0 = 0.99 * F_n
G_n = Matrix([0.99 * f for f in F_n_mp])
gamma = mp.mpf('0.98')

# Run 10 iterations of 4DIP with norm tracking
print("=== 4DIP Convergence: Triple Pendulum ===")

for step in range(10):
    R_n = F_n_mp - G_n
    R_norm = norm([float(r) for r in R_n])
    tier = int(-mp.floor(mp.log10(R_norm)))

    print("\nIteration", step)
    print("  Residual Norm =", float(R_norm), "  Tier", tier)

    for i in range(3):
        print("  R[{}] =".format(i), float(R_n[i]))

    G_n = F_n_mp - gamma * R_n
