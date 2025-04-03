import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

for filepath in sys.argv[1:]:
    file = open(filepath)
    f = csv.reader(file)

    intersections = []

    prev_x0 = 0
    prev_x1 = 0
    for row in f:
        if (float(row[1]) - float(row[2])) * (prev_x0 - prev_x1) < 0:
            intersections.append(float(row[0]))

        prev_x0 = float(row[1])
        prev_x1 = float(row[2])

    plt.plot(np.arange(len(intersections)), intersections)
    plt.show()

    m, b = np.polyfit(np.arange(len(intersections)), intersections, 1)

    print(f"{filepath.split('/')[-1].split('.')[:-1]},{m}")
