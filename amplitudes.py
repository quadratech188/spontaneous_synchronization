from Simulation import Simulation
import pandas as pd

def data(M, T):
    dt = 0.01

    simulation = Simulation(2, 1, M, 1, 0.01, 0, 0.01)

    simulation.x.x[0] = 1

    records = [[(0, 1)], [(0, 0)]]

    maximums = [(0.0, 0.0) for _ in range(2)]

    def update_maximums(i, dir):
        records[i].append(maximums[i])
        maximums[i] = (0.0, 0.0)

    simulation.add_escapement_hook(update_maximums)

    t = 0
    while t < T:
        simulation.step(dt)

        for i in range(2):
            if maximums[i][1] < abs(simulation.x.x[i]):
                maximums[i] = (t, abs(simulation.x.x[i]))

        t += dt

    return records
