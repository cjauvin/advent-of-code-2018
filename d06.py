import sys
import re
from collections import defaultdict
import numpy as np

coords = []
for line in open('d06.txt'):
    a = map(int, re.findall('\d+', line))
    coords.append(tuple(a))

m = [0, 0]
for c in coords:
    m[0] = max(m[0], c[0])
    m[1] = max(m[1], c[1])

N = 360

# coords = [
#     (1, 1),
#     (1, 6),
#     (8, 3),
#     (3, 4),
#     (5, 5),
#     (8, 9)
# ]
# N = 10

g = defaultdict(lambda: {'idx': -1, 'dist': float('inf')})

def dist(c, d):
    return abs(c[0] - d[0]) + abs(c[1] - d[1])

visited = set()

def visit(i):

    to_visit = set([coords[i]])
    n_visited = 0

    while to_visit:

        n_visited += 1

        c = to_visit.pop()
        d = dist(c, coords[i])

        if g[c]['dist'] == d and g[c]['idx'] != i:
            g[c]['idx'] = -1
        else:
            g[c] = {'idx': i, 'dist': d}

        visited.add((c, i))

        left = (c[0] - 1, c[1])
        if c[0] > 0 and d + 1 <= g[left]['dist']:
            if (left, i) not in visited:
                to_visit.add(left)
        right = (c[0] + 1, c[1])
        if c[0] < N and d + 1 <= g[right]['dist']:
            if (right, i) not in visited:
                to_visit.add(right)
        up = (c[0], c[1] - 1)
        if c[1] > 0 and d + 1 <= g[up]['dist']:
            if (up, i) not in visited:
                to_visit.add(up)
        down = (c[0], c[1] + 1)
        if c[1] < N and d + 1 <= g[down]['dist']:
            if (down, i) not in visited:
                to_visit.add(down)

    return n_visited

# for i in range(len(coords)):
#     print(i, visit(i))
#     sys.stdout.flush()
# print('--')

# is_infinite = set()

# G = np.zeros((N, N), dtype=int)
# for i in range(N):
#     for j in range(N):
#         G[i, j] = g[(i, j)]['dist']
#         if g[(i, j)]['idx'] != -1 and (i in {0, N-1} or j in {0, N-1}):
#             is_infinite.add(g[(i, j)]['idx'])

# print()
# print(G.T)
# print(is_infinite)

# m = 0
# for i in range(len(coords)):
#     if i in is_infinite:
#         continue
#     m = max(len(G[G == i]), m)

# print(m)


def visit2(i):

    g = defaultdict(lambda: {'idx': -1, 'dist': float('inf')})

    visited = set()
    to_visit = set([coords[i]])

    while to_visit:

        c = to_visit.pop()
        d = dist(c, coords[i])

        g[c] = {'idx': i, 'dist': d}

        visited.add(c)

        left = (c[0] - 1, c[1])
        if c[0] > 0 and d + 1 < g[left]['dist']:
            if left not in visited:
                to_visit.add(left)
        right = (c[0] + 1, c[1])
        if c[0] < N and d + 1 < g[right]['dist']:
            if right not in visited:
                to_visit.add(right)
        up = (c[0], c[1] - 1)
        if c[1] > 0 and d + 1 < g[up]['dist']:
            if up not in visited:
                to_visit.add(up)
        down = (c[0], c[1] + 1)
        if c[1] < N and d + 1 < g[down]['dist']:
            if down not in visited:
                to_visit.add(down)

    G = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            G[i, j] = g[(i, j)]['dist']

    return G

G = np.zeros((N, N))
for i in range(len(coords)):
    G += visit2(i)
    print(i)
#print(G.T)
print(len(G[G < 10000]))
