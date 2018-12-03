import re
from collections import defaultdict

s = open('d03.txt').readlines()
s = [l.strip() for l in s]

coords = []
max_i = 0
max_j = 0
for r in s:
    m = re.match('#\d+ @ (\d+),(\d+): (\d+)x(\d+)', r)
    coords.append(list(map(int, m.groups())))
    max_i = max(max_i, coords[-1][0] + coords[-1][2])
    max_j = max(max_j, coords[-1][1] + coords[-1][3])

g = defaultdict(lambda: defaultdict(int))

for c in coords:
    for i in range(c[2]):
        for j in range(c[3]):
            g[c[0] + i][c[1] + j] += 1

# part 1
n = 0
for i in range(1100):
    for j in range(1100):
        n += 1 if g[i][j] > 1 else 0

print(n)

# part 2

for ci, c in enumerate(coords):
    is_intact = True
    for i in range(c[2]):
        for j in range(c[3]):
            if g[c[0] + i][c[1] + j] > 1:
                is_intact = False
                break
        if not is_intact:
            break
    if is_intact:
        print(ci + 1)
        break
