import itertools
from math import *

def hypercube(origin=(0, 0, 0, 0), edge_offset=0):
    x, y, z, w = origin
    points = list(itertools.product((-1, 1), repeat=4))
    points = [(x2+x, y2+y, z2+z, w2+w) for x2, y2, z2, w2 in points]
    edges = []
    for i in range(16):
        for j in range(i, 16):
            if sum(1 for k in range(4) if points[i][k] == points[j][k]) == 3:
                edges.append((i+edge_offset, j+edge_offset))
    return points, edges

def simplex():
    points = [(1, 1, 1, -1/sqrt(5)), (1, -1, -1, -1/sqrt(5)), (-1, 1, -1, -1/sqrt(5)), (-1, -1, 1, -1/sqrt(5)), (0, 0, 0, sqrt(5)-1/sqrt(5))]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    return points, edges

def two_hypercubes():
    p1, e1 = hypercube(origin=(0, -1, 0, 0))
    p2, e2 = hypercube(origin=(0, 1, 0, 0), edge_offset=16)
    return p1 + p2, e1 + e2

def sixteencell(size=1):
    points = [(size, 0, 0, 0), (-size, 0, 0, 0), (0, size, 0, 0), (0, -size, 0, 0), (0, 0, size, 0), (0, 0, -size, 0), (0, 0, 0, size), (0, 0, 0, -size)]
    edges = []
    for i in range(8):
        for j in range(i+1, 8):
            edges.append((i, j))
    return points, edges