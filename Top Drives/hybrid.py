import matplotlib.pyplot as plt
import numpy as np
from itertools import product

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

tunes = [
    tup for tup in product([6, 7, 8, 9], repeat=3)
    if sum(tup) <= 24
]

engine = (0, 1, 1)
weight = (-0.866, -0.5, 1)
chassis = (0.855, -0.5, 1)

for tune in tunes:
    coords = [(0, 0, 0)]
    coords.extend([engine] * (tune[0] - 6))
    coords.extend([weight] * (tune[1] - 6))
    coords.extend([chassis] * (tune[2] - 6))
    coords = [sum(dir) for dir in list(zip(*coords))]
    ax.scatter(*coords, marker="o")

ax.plot([0, 0], [0, 6], zs=[0, 6])
ax.plot([0, -0.866 * 6], [0, -3], zs=[0, 6])
ax.plot([0, 0.866 * 6], [0, -3], zs=[0, 6])

plt.show()