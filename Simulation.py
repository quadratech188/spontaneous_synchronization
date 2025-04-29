import math
import numpy as np
from vpython import vector

g = 9.8

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

class Simulation:
    def __init__(self, n: int, m: float, M: float, r: float, b: float, angle_threshold: float, impulse: float):
        self.n = n
        self.m = m
        self.M = M
        self.r = r
        self.b = b
        self.angle_threshold = angle_threshold
        self.impulse = impulse
        self.x = Data(np.zeros(n), 0)
        self.v = Data(np.zeros(n), 0)
        self.forces = np.zeros(n)

        self.escapement_hooks = []

    def acceleration(self, x: Data, v: Data, f: np.ndarray) -> Data:

        dividend = self.m * self.r * np.sum(np.sin(x.x) * v.x ** 2) \
                + self.m * g * np.sum(np.sin(x.x) * np.cos(x.x)) \
                + self.b * self.m * self.r * np.sum(np.cos(x.x) * v.x) \
                - np.sum(f * np.cos(x.x) ** 2)

        divisor = (self.n * self.m + self.M) - self.m * np.sum(np.cos(x.x))

        A = dividend / divisor

        a = -g * np.sin(x.x) / self.r \
            - np.cos(x.x) * A / self.r \
            - self.b * v.x \
            + f * np.cos(x.x) / self.m / self.r 

        return Data(a, A)

    def energy(self) -> float:
        result = 0
        for i in range(self.n):
            result += 0.5 * self.m * (vector(self.v.X, 0, 0) \
                    + vector(self.r * self.v.x[i], 0, 0).rotate(self.x.x[i])).mag2

        result += 0.5 * self.M * self.v.X ** 2

        for i in range(self.n):
            result += -self.m * g * self.r * math.cos(self.x.x[i])

        return result

    def runge_kutta(self, x1: Data, v1: Data, f: np.ndarray, dt: float):
        a1 = self.acceleration(x1, v1, f)
        x2 = x1 + 0.5 * dt * v1
        v2 = v1 + 0.5 * dt * a1

        a2 = self.acceleration(x2, v2, f)

        x3 = x1 + 0.5 * dt * v2
        v3 = v1 + 0.5 * dt * a2

        a3 = self.acceleration(x3, v3, f)

        x4 = x1 + dt * v3
        v4 = v1 + dt * a3

        a4 = self.acceleration(x4, v4, f)

        return x1 + dt / 6 * (v1 + 2 * v2 + 2 * v3 + v4),\
               v1 + dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)

    def step(self, dt: float):
        x_next, v_next = self.runge_kutta(self.x, self.v, self.forces, dt)

        self.forces = np.zeros(self.n)

        for i in range(self.n):
            if self.x.x[i] < -self.angle_threshold and x_next.x[i] > -self.angle_threshold:
                self.forces[i] += self.impulse / dt
                for hook in self.escapement_hooks:
                    hook(i, 1)

            if self.x.x[i] > self.angle_threshold and x_next.x[i] < self.angle_threshold:
                self.forces[i] += -self.impulse / dt
                for hook in self.escapement_hooks:
                    hook(i, -1)

        self.x, self.v = x_next, v_next

    def add_escapement_hook(self, hook):
        self.escapement_hooks.append(hook)
