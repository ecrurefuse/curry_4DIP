# 4DIP Convergence Test: Chaotic Triple Pendulum Using Lagrangian Symbolic Form

from sympy import symbols, Function, Matrix, diff, cos, simplify
from sympy.abc import t
from mpmath import mp, norm
import matplotlib.pyplot as plt

# High precision setup
mp.dps = 50

# Physical constants
m1, m2, m3 = 1, 1, 1
l1, l2, l3 = 1, 1, 1
g = 9.81

# Angles as time-dependent functions
th1 = Function('th1')(t)
th2 = Function('th2')(t)
th3 = Function('th3')(t)

# First and second derivatives
th1d, th2d, th3d = diff(th1, t), diff(th2, t), diff(th3, t)
th1dd, th2dd, th3dd = diff(th1d, t), diff(th2d, t), diff(th3d, t)

# Kinetic Energy (simplified Lagrangian)
T = (0.5 * m1 * l1**2 * th1d**2 +
     0.5 * m2 * (l1**2 * th1d**2 + l2**2 * th2d**2 + 2 * l1 * l2 * th1d * th2d * cos(th1 - th2)) +
     0.5 * m3 * (l1**2 * th1d**2 + l2**2 * th2d**2 + l3**2 * th3d**2 +
                2 * l1 * l2 * th1d * th2d * cos(th1 - th2) +
                2 * l1 * l3 * th1d * th3d * cos(th1 - th3) +
                2 * l2 * l3 * th2d * th3d * cos(th2 - th3)))

# Potential Energy
V = m1 * g * l1 * cos(th1) + m2 * g * (l1 * cos(th1) + l2 * cos(th2)) + m3 * g * (l1 * cos(th1) + l2 * cos(th2) + l3 * cos(th3))

# Lagrangian
L = T - V

# Euler-Lagrange equations
coords = [th1, th2, th3]
F_n = []
for q in coords:
    dL_dq = diff(L, q)
    dL_dqdot = diff(L, diff(q, t))
    d_dt = diff(dL_dqdot, t)
    F_n.append(simplify(d_dt - dL_dq))
F_n = Matrix(F_n)

# Chaotic initial condition substitution
subs = {
    th1: 0.1,
    th2: 0.1,
    th3: 0.1,
    th1d: 1.0,
    th2d: -1.5,
    th3d: 0.75,
    th1dd: 0,
    th2dd: 0,
    th3dd: 0
}

# Evaluate system
F_n_eval = F_n.subs(subs).evalf(mp.dps)
F_n_mp = Matrix([mp.mpf(str(val)) for val in F_n_eval])

# 4DIP setup
G_n = Matrix([0.99 * val for val in F_n_mp])
gamma = mp.mpf('0.98')
residuals = []

print("=== 4DIP: Chaotic Triple Pendulum ===")

for step in range(2000):
    R_n = F_n_mp - G_n
    res_norm = norm([float(r) for r in R_n])
    residuals.append(float(res_norm))
    print(f"Iteration {step}: Residual Norm = {float(res_norm):.6e}")
    if res_norm < 1e-14:
        print("Converged below 1e-14.")
        break
    G_n = F_n_mp - gamma * R_n

# Plot residual norm
plt.plot(residuals)
plt.xlabel("Iteration")
plt.ylabel("Residual Norm")
plt.title("4DIP Convergence: Chaotic Triple Pendulum")
plt.grid(True)
plt.savefig("convergence_plot.png", dpi=300)
plt.show()
