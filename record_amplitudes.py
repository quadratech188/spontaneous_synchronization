from amplitudes import data
import sys
import csv
import numpy as np

writer = csv.writer(sys.stdout)

for M in range(20, 301, 20):
    print(M)
    records = data(M, 500)

    ts = [d[0] for i in range(2) for d in records[i]]
    positions = [[], []]
    ts.sort()

    tables = [{t[0]: t[1] for t in records[i]} for i in range(2)]

    for i, t in enumerate(ts):
        for k in range(2):
            if t in tables[k]:
                positions[k].append(tables[k][t])
                continue

            t1 = 0
            t2 = 0
            for j in range(i, -1, -1):
                if ts[j] in tables[k]:
                    t1 = ts[j]
                    break

            for j in range(i, len(ts)):
                if ts[j] in tables[k]:
                    t2 = ts[j]
                    break

            x = ((t2 - t) * tables[k][t1] + (t - t1) * tables[k][t2]) / (t2 - t1)
            positions[k].append(x)

    with open(f'output/{M}.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        for t, x1, x2 in zip(ts, positions[0], positions[1]):
            writer.writerow([t, x1, x2])

