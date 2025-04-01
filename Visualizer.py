from Simulation import Simulation
from vpython import *
import numpy as np
import math

class Visualizer:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation

        self.deltas = np.linspace(-2, 2, simulation.n)

        self.rods = [cylinder(pos=vector(self.deltas[i], 0, 0),
                              axis = vector(simulation.r * math.sin(simulation.x.x[i]),
                                            -simulation.r * math.cos(simulation.x.x[i]), 0),
                              radius = 0.02)
                     for i in range(simulation.n)]

        self.ceiling = box(pos=vector(0, 0, 0), size = vector(5, 0.1, 0.5))

    def update(self):
        for i in range(self.simulation.n):
            self.rods[i].pos = vector(self.deltas[i] + self.simulation.x.X, 0, 0)
            self.rods[i].axis = vector(self.simulation.r * math.sin(self.simulation.x.x[i]),
                                       -self.simulation.r * math.cos(self.simulation.x.x[i]), 0)

        self.ceiling.pos.x = self.simulation.x.X
