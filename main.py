from vpython import *
import math

g = 9.8
L = 1.0
n = 5
dt = 0.01
M = 30.0
m = 1.0
k = g / L
gamma = 0.1  # damping
kick = 0.01

# Set initial phases and convert to x, v
A = 0.3
omega = math.sqrt(k / m)
offset = 1.3
phases = [0, 0, 0, 0, offset]  # or use any offset you want, must be len = n

x = [A * math.cos(phi) for phi in phases]
x_prev = x[:]
v = [-A * omega * math.sin(phi) for phi in phases]

X = 0.0
V = 0.0

# Cancel net momentum
s = sum(v)
for i in range(n):
    v[i] -= s / n

base = box(pos=vector(0, 0, 0), size=vector(3, 0.05, 0.5))

deltas = [-1.2 + 2.4 * i / (n - 1) for i in range(n)]
pivots = []

for i in range(n):
    pivots.append(cylinder(pos=vector(deltas[i], 0, 0),
                           axis=vector(L * math.sin(x[i] / L), -L * math.cos(x[i] / L), 0),
                           radius=0.02))

# Graph setup
energy_graph = graph(title="Total Energy vs Time", xtitle="Time (s)", ytitle="Energy (J)")
energy_curve = gcurve(color=color.green)

# Displacement (x) graph setup
x_graph = graph(title="x[i] vs Time", xtitle="Time (s)", ytitle="x (displacement)", fast=False, scroll=True, xmin=-5, xmax=0)
x_curves = [gcurve(color=color.hsv_to_rgb(vector(i/n, 1, 1))) for i in range(n)]
x_graph = graph(title="X vs Time", xtitle="Time (s)", ytitle="X (displacement)", fast=False)
X_curve = gcurve()

t = 0

# Van der Pol acceleration
def acceleration(xi, vi, X, V):
  mu = 1.0  # nonlinear damping strength
  return -k * (xi - X) / m - gamma * vi

def base_acceleration(x_list, X, V):
    force_sum = sum(k * (xi - X) for xi in x_list)
    return force_sum / M - gamma * V

while True:
    rate(1 / dt)
    t += dt

    # RK4 for each x[i] and v[i]
    x1 = x[:]
    v1 = v[:]
    X1 = X
    V1 = V

    a1 = [acceleration(x1[i], v1[i], X1, V1) for i in range(n)]
    A1 = base_acceleration(x1, X1, V1)

    x2 = [x1[i] + 0.5 * dt * v1[i] for i in range(n)]
    v2 = [v1[i] + 0.5 * dt * a1[i] for i in range(n)]
    X2 = X1 + 0.5 * dt * V1
    V2 = V1 + 0.5 * dt * A1

    a2 = [acceleration(x2[i], v2[i], X2, V2) for i in range(n)]
    A2 = base_acceleration(x2, X2, V2)

    x3 = [x1[i] + 0.5 * dt * v2[i] for i in range(n)]
    v3 = [v1[i] + 0.5 * dt * a2[i] for i in range(n)]
    X3 = X1 + 0.5 * dt * V2
    V3 = V1 + 0.5 * dt * A2

    a3 = [acceleration(x3[i], v3[i], X3, V3) for i in range(n)]
    A3 = base_acceleration(x3, X3, V3)

    x4 = [x1[i] + dt * v3[i] for i in range(n)]
    v4 = [v1[i] + dt * a3[i] for i in range(n)]
    X4 = X1 + dt * V3
    V4 = V1 + dt * A3

    a4 = [acceleration(x4[i], v4[i], X4, V4) for i in range(n)]
    A4 = base_acceleration(x4, X4, V4)

    for i in range(n):
        x[i] += dt / 6 * (v1[i] + 2*v2[i] + 2*v3[i] + v4[i])
        v[i] += dt / 6 * (a1[i] + 2*a2[i] + 2*a3[i] + a4[i])

    X += dt / 6 * (V1 + 2*V2 + 2*V3 + V4)
    V += dt / 6 * (A1 + 2*A2 + 2*A3 + A4)

    base.pos = vector(X, 0, 0)

    for i in range(n):
        if x_prev[i] * x[i] < 0:  # crossed zero
            if v[i] > 0:
                v[i] += kick / m
                V -= kick / M
            else:
                v[i] -= kick / m
                V += kick / M

    x_prev = x[:]

    for i in range(n):
        pivots[i].pos.x = deltas[i] + X
        pivots[i].axis = vector(L * math.sin((x[i] - X) / L), -L * math.cos((x[i] - X) / L), 0)

    # Energy calculation
    total_energy = 0.5 * M * V**2
    for i in range(n):
        ke = 0.5 * m * v[i]**2
        pe = 0.5 * k * (x[i] - X)**2
        total_energy += ke + pe

    # Plot x[i] vs time
    for i in range(n):
        x_curves[i].plot(t, x[i])

    energy_curve.plot(t, total_energy)
    X_curve.plot(t, X)
