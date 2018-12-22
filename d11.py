import numpy as np
from collections import defaultdict


def get_digit(num, n=3):
    if n == 1:
        return num % 10
    else:
        return get_digit(num // 10, n - 1)

def get_grid(serial):

    g = defaultdict(lambda: defaultdict(int))
    h = np.empty((300, 300))

    for x in range(1, 301):
        for y in range(1, 301):
            rack_id = x + 10
            pl = rack_id * y
            pl += serial
            pl *= rack_id
            g[x][y] = get_digit(pl) - 5
            h[y-1][x-1] = g[x][y]

    return g, h

# assert get_grid(8)[3][5] == 4
# assert get_grid(57)[122][79] == -5
# assert get_grid(39)[217][196] == 0
# assert get_grid(71)[101][153] == 4

g, _ = get_grid(3214)

# best = (float('-inf'), (-1, -1))

# for x in range(1, 301 - 3):
#     for y in range(1, 301 - 3):
#         tot = 0
#         for i in range(3):
#             for j in range(3):
#                 tot += g[x+i][y+j]
#         best = max(best, (tot, (x, y)))

# print(best)

# _, h = get_grid(3214)

# np.set_printoptions(threshold=np.nan, linewidth=2000)
# print(h[:50, :50])

s = defaultdict(lambda: defaultdict(int))

for x in range(1, 301):
    for y in range(1, 301):
        s[x][y] = s[x-1][y] + g[x][y]

def sum_between(x1, x2, y):
    return s[x2][y] - s[x1 - 1][y]

# print(g[189][300])

# for j in range(298, 301):
#     for i in range(188, 192):
#         print(f'{g[i][j]: >4}', end=' ')
#     print()

# exit()

best_sum = (float('-inf'), (-1, -1, -1))
for x1 in range(1, 301):
    for x2 in range(x1, 301):
        curr_sum = 0
        curr_best_sum = (float('-inf'), (-1, -1, -1))
        for y in range(1, 301):
            curr_sum += sum_between(x1, x2, y)
            curr_best_sum = max(curr_best_sum, (curr_sum, (x1, y, x2 - x1)))
            if curr_sum < 0:
                curr_sum = 0
        best_sum = max(best_sum, curr_best_sum)

print(best_sum)

# for i in range(10):
#     for j in range(10):
#         print(f'{g[i][j]: >4}', end=' ')
#     print()

# print('\n')

# for i in range(10):
#     for j in range(10):
#         print(f'{s[j][i]: >4}', end=' ')
#     print()

# print('--')

# print(s[6][2])
# print(s[3][2])
# print(sum_between(3, 6, 2))
