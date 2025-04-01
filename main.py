import math
import numpy as np

m = 1
M = 10
r = 1
b = 0.1
n = 5

angle_threshold = 0.1
impulse = 0.1
initial_amplitude = 1

g = 9.8
fps = 100
timescale = 1
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

def acceleration(x: Data, v: Data, f: np.ndarray) -> Data:
    dividend = m * r * sum(math.sin(x.x[i]) * v.x[i] ** 2 for i in range(n)) \
            + m * g * sum(math.sin(x.x[i]) * math.cos(x.x[i]) for i in range(n)) \
            + b * m * r * sum(math.cos(x.x[i]) * v.x[i] for i in range(n)) \
            - sum(f[i] * math.cos(x.x[i]) ** 2 for i in range(n))

    divisor = (n * m + M) - m * sum(math.cos(x.x[i]) ** 2 for i in range(n))

    A = dividend / divisor

    a = np.fromiter((-g * math.sin(x.x[i]) \
                     - math.cos(x.x[i]) * A / r - b * v.x[i] \
                     + f[i] * math.cos(x.x[i]) / m / r for i in range(n)), float, n)

    return Data(a, A)

def energy(x: Data, v: Data) -> float:
    result = 0
    for i in range(n):
        result += 0.5 * m * (vector(v.X, 0, 0) + vector(r * v.x[i], 0, 0).rotate(x.x[i])).mag2

    result += 0.5 * M * v.X ** 2

    for i in range(n):
        result += -m * g * r * math.cos(x.x[i])

    return result

def runge_kutta(x1: Data, v1: Data, f: np.ndarray):
    a1 = acceleration(x1, v1, f)
    x2 = x1 + 0.5 * dt * v1
    v2 = v1 + 0.5 * dt * a1

    a2 = acceleration(x2, v2, f)

    x3 = x1 + 0.5 * dt * v2
    v3 = v1 + 0.5 * dt * a2

    a3 = acceleration(x3, v3, f)

    x4 = x1 + dt * v3
    v4 = v1 + dt * a3

    a4 = acceleration(x4, v4, f)

    return x1 + dt / 6 * (v1 + 2 * v2 + 2 * v3 + v4),\
           v1 + dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)

from vpython import *

x = Data(np.zeros(n), 0)
v = Data(np.zeros(n), 0)
forces = np.zeros(n)
t = 0

deltas = np.linspace(-2, 2, n)

rods = [cylinder(pos=vector(deltas[i], 0, 0),
                 axis = vector(r * math.sin(x.x[i]), -r * math.cos(x.x[i]), 0),
                 radius = 0.02)
                 for i in range(n)]

ceiling = box(pos=vector(0, 0, 0), size = vector(5, 0.1, 0.5))

angle_graph = graph(title='x - t', xtitle='t(s)', ytitle='x(m)', xmin=-5, xmax=0, scroll=True)

angle_curves = [gcurve(color=color.hsv_to_rgb(vector(i / n, 1, 1))) for i in range(n)]

scene.caption = 'Spontaneous Synchronization\n\n'
timescale_text = wtext(text=f'Time Factor: {timescale}x\n')

def timescale_slider_callback(evt):
    global timescale, timescale_text
    timescale = int(evt.value)
    timescale_text.text = f'Time Factor: {timescale}x\n'

timescale_slider = slider(bind=timescale_slider_callback, min=1, max=10, step=1)
scene.append_to_caption('\n\n')

def left_callback(evt):
    x.x[evt.id] = -initial_amplitude

def right_callback(evt):
    x.x[evt.id] = initial_amplitude

for i in range(n):
    button(text='<', bind=left_callback, id=i)
    scene.append_to_caption(f' {i} ')
    button(text='>', bind=right_callback, id=i)
    scene.append_to_caption(f'    ')

scene.append_to_caption('\n')

new_n = None
new_m = None
new_M = None

while True:
    rate(fps)

    for i in range(timescale):
        x_next, v_next = runge_kutta(x, v, forces)

        forces = np.zeros(n)

        for i in range(n):
            if x.x[i] < -angle_threshold and x_next.x[i] > -angle_threshold:
                forces[i] = impulse / dt

            if x.x[i] > angle_threshold and x_next.x[i] < angle_threshold:
                forces[i] = -impulse / dt

        x, v = x_next, v_next

    for i in range(n):
        rods[i].pos.x = deltas[i] + x.X
        rods[i].axis = vector(r * math.sin(x.x[i]), - r * math.cos(x.x[i]), 0)
        angle_curves[i].plot(t, x.x[i])

    ceiling.pos.x = x.X

    t += dt * timescale

    # print(m * r * sum(math.sin(x.x[i]) for i in range(n)) + (M + n * m) * x.X)
    # print(energy(x, v))
