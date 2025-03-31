import math
import numpy as np

m = 1
M = 5
r = 1
n = 5
g = 9.8
fps = 100
dt = 1 / fps

class Data:
    def __init__(self, x: np.ndarray, X: float):
        self.x = x
        self.X = X

    def __add__(self, other: 'Data'):
        return Data(self.x + other.x, self.X + other.X)

    def __rmul__(self, other: float):
        return Data(other * self.x, other * self.X)

    def __str__(self):
        return f"{self.x}, {self.X}"

def acceleration(x: Data, v: Data) -> Data:
    dividend = m * r * sum(math.sin(x.x[i]) * v.x[i] ** 2 for i in range(n)) \
            + m * g * r * sum(math.sin(x.x[i]) * math.cos(x.x[i]) for i in range(n))

    divisor = (n * m + M) - m * sum(math.cos(x.x[i]) ** 2 for i in range(n))

    A = dividend / divisor

    a = np.fromiter((-g * math.sin(x.x[i]) - math.cos(x.x[i]) * A / r for i in range(n)), float, n)

    return Data(a, A)

def energy(x: Data, v: Data) -> float:
    result = 0
    for i in range(n):
        result += 0.5 * m * (vector(v.X, 0, 0) + vector(r * v.x[i], 0, 0).rotate(x.x[i])).mag2

    result += 0.5 * M * v.X ** 2

    for i in range(n):
        result += -m * g * r * math.cos(x.x[i])

    return result

def runge_kutta(x1: Data, v1: Data):
    a1 = acceleration(x1, v1)
    x2 = x1 + 0.5 * dt * v1
    v2 = v1 + 0.5 * dt * a1

    a2 = acceleration(x2, v2)

    x3 = x1 + 0.5 * dt * v2
    v3 = v1 + 0.5 * dt * a2

    a3 = acceleration(x3, v3)

    x4 = x1 + dt * v3
    v4 = v1 + dt * a3

    a4 = acceleration(x4, v4)

    return x1 + dt / 6 * (v1 + 2 * v2 + 2 * v3 + v4),\
           v1 + dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)

from vpython import *

x = Data(np.array([0, 0, 0, 0, 1]), 0)
v = Data(np.array([0, 0, 0, 0, 0]), 0)

deltas = np.linspace(-2, 2, n)

rods = [cylinder(pos=vector(deltas[i], 0, 0),
                 axis = vector(r * math.sin(x.x[i]), -r * math.cos(x.x[i]), 0),
                 radius = 0.02)
                 for i in range(n)]

ceiling = box(pos=vector(0, 0, 0), size = vector(5, 0.1, 0.5))

while True:
    rate(fps)

    x, v = runge_kutta(x, v)

    for i in range(n):
        rods[i].pos.x = deltas[i] + x.X
        rods[i].axis = vector(r * math.sin(x.x[i]), - r * math.cos(x.x[i]), 0)

    ceiling.pos.x = x.X

    print(energy(x, v))
