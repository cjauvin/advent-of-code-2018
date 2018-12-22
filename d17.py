from collections import defaultdict
import random
import re
import sys

s = """
......+.......
............#.
.#..#.......#.
.#..#..#......
.#..#..#......
.#.....#......
.#.....#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
"""

# s = """
# .....+.....
# ..#.#.#.#..
# ..#.#.#.#..
# ..#.#.#.#..
# ..#######..
# ...........
# """

t = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""

s = """
...............+...............
...............................
............#.....#............
............#.....#............
............#######............
...............................
......#........................
......#.................#......
......#.................#......
......#.................#......
......#.................#......
......#.................#......
......###################......
...............................
...............................
"""

def get_grid(t):
    dims = [float('inf'), float('-inf'), float('inf'), float('-inf')]  # min_y, max_y, min_x, max_x
    specs = []
    for line in t.split('\n') if isinstance(t, str) else t.readlines():
        line = line.strip()
        if not line: continue
        m = re.match('(.)=(.+), (.)=(.+)', line)
        xs = list(map(int, re.findall('\d+', m.group(2) if m.group(1) == 'x' else m.group(4))))
        ys = list(map(int, re.findall('\d+', m.group(4) if m.group(1) == 'x' else m.group(2))))
        dims[0] = min(dims[0], min(ys))
        dims[1] = max(dims[1], max(ys))
        dims[2] = min(dims[2], min(xs))
        dims[3] = max(dims[3], max(xs))
        specs.append((ys, xs))

    print(dims)
    # print(specs)

    g = []
    for _ in range(dims[0], dims[1] + 1):
        g.append(['.'] * (dims[3] - dims[2] + 3))

    print(len(g), len(g[0]))

    for ys, xs in specs:
        for y in range(ys[0], ys[-1] + 1):
            for x in range(xs[0], xs[-1] + 1):
                i, j = (y - dims[0]), (x - dims[2])
                g[i][j + 1] = '#'

    g[0][500 - dims[2] + 1] = '+'

    return g

# g = []
# for line in s.strip().split('\n'):
#     g.append(list(line))

with open('d17.txt') as f:
    g = get_grid(f)

# g = get_grid(t)

def print_grid(g):
    print('\n' + '\n'.join(''.join(c for c in row) for row in g))

go_left = True

dird = defaultdict(bool)

def drop():

    global go_left, dird
    visited = set()

    to_visit = [(1, g[0].index('+'))]

    while to_visit:
        i, j = to_visit.pop()
        visited.add((i, j))
        g[i][j] = '|'
        #go_left = random.choice([True, False])
        go_left = dird[(i, j)]

        is_moving = False

        if i + 1 >= len(g):
            is_moving = True # stop!
        # if can go down..
        elif g[i + 1][j] in '.|':
            to_visit.append((i + 1, j))
            is_moving = True

        # if can go left and never went
        else:
            if g[i][j - 1] in '.|' and (i, j - 1) not in visited:
                to_visit.append((i, j - 1))
                is_moving = True

            if g[i][j + 1] in '.|' and (i, j + 1) not in visited:
                to_visit.append((i, j + 1))
                is_moving = True

        if not is_moving:
            left = j
            left_open = True
            while g[i][left] != '#':
                left -= 1
                if left < 0:
                    left = None
                    break
            if left:
                assert g[i][left] == '#'
            if left and g[i + 1][left + 1] in '~#':
                left_open = False

            right = j
            right_open = True
            while g[i][right] != '#':
                right += 1
                if right >= len(g[0]):
                    right = None
                    break
            if right:
                assert g[i][right] == '#'
            if right and g[i + 1][right - 1] in '~#':
                right_open = False

            # right = j
            # right_open = False
            # while g[i][right] != '#':
            #     right += 1
            #     if g[i + 2][right] in '.|':
            #         right_open = True
            #         break
            # if not left_open and not right_open:
            #     g[i][j] = '~'


            # left = j
            # left_open = False
            # while g[i][left] != '#':
            #     left -= 1
            #     if g[i + 2][left] in '.|':
            #         left_open = True
            #         break
            # right = j
            # right_open = False
            # while g[i][right] != '#':
            #     right += 1
            #     if g[i + 2][right] in '.|':
            #         right_open = True
            #         break

            if not left_open and not right_open:
                g[i][j] = '~'

    #go_left = not go_left

for _ in range(int(sys.argv[1])):
#for _ in range(150):
    drop()

# print_grid(g)
# print()

# n = 0
# for r in g:
#     for c in r:
#         n += 1 if c in '~|' else 0
# print(n)
