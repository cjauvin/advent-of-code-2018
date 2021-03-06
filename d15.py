from collections import defaultdict
import pprint

# s = """
# #########
# #G..G..G#
# #.......#
# #.......#
# #G..E..G#
# #.......#
# #.......#
# #G..G..G#
# #########
# """

# s = """
# #########
# #.G...G.#
# #...G...#
# #...E..G#
# #.G.....#
# #.......#
# #G..G..G#
# #.......#
# #########
# """

# s = """
# #######
# #E..G.#
# #...#.#
# #.G.#G#
# #######
# """

# 47, 27730
# s = """
# #######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######
# """

# 37 * 982 = 36334
# s = """
# #######
# #G..#E#
# #E#E.E#
# #G.##.#
# #...#E#
# #...E.#
# #######
# """

# 46 * 859 = 39514
# s = """
# #######
# #E..EG#
# #.#G.E#
# #E.##E#
# #G..#.#
# #..E#.#
# #######
# """

# 35 * 793 = 27755
# s = """
# #######
# #E.G#.#
# #.#G..#
# #G.#.G#
# #G..#.#
# #...E.#
# #######
# """

# 54 * 536 = 28944
# s = """
# #######
# #.E...#
# #.#..G#
# #.###.#
# #E#G#G#
# #...#G#
# #######
# """

# 20 * 937 = 18740
# s = """
# #########
# #G......#
# #.E.#...#
# #..##..G#
# #...##..#
# #...#...#
# #.G...G.#
# #.....G.#
# #########
# """

# s = """
# ################################
# ###########...G...#.##..########
# ###########...#..G#..G...#######
# #########.G.#....##.#GG..#######
# #########.#.........G....#######
# #########.#..............#######
# #########.#...............######
# #########.GG#.G...........######
# ########.##...............##..##
# #####.G..##G.......E....G......#
# #####.#..##......E............##
# #####.#..##..........EG....#.###
# ########......#####...E.##.#.#.#
# ########.#...#######......E....#
# ########..G.#########..E...###.#
# ####.###..#.#########.....E.####
# ####....G.#.#########.....E.####
# #.........#G#########......#####
# ####....###G#########......##..#
# ###.....###..#######....##..#..#
# ####....#.....#####.....###....#
# ######..#.G...........##########
# ######...............###########
# ####.....G.......#.#############
# ####..#...##.##..#.#############
# ####......#####E...#############
# #.....###...####E..#############
# ##.....####....#...#############
# ####.########..#...#############
# ####...######.###..#############
# ####..##########################
# ################################
# """

# s = """
# ################################
# ##########################..####
# #########################...####
# #########################..#####
# ########################G..#####
# #####################.#.....##.#
# #####################..........#
# ##############.#####...........#
# ########G...G#.####............#
# #######......G....#.....#......#
# #######...G....GG.#............#
# #######G.G.............####....#
# #######.#.....#####....E.....###
# #######......#######.G.......###
# #..####..G..#########.###..#####
# #........G..#########.##########
# #..#..#G....#########.##########
# #.###...E...#########.##########
# #####...G.G.#########.##########
# ########G....#######..##########
# ####..........#####...##########
# ####......E........G..##########
# #.G..................###########
# #G...................###########
# ###.....##E.......E..###########
# ###....#............############
# ###.................############
# ##G.....#.............##########
# ###########...#E..##..##########
# ###########.E...###.E.EE.#######
# ###########......#.......#######
# ################################
# """

s = """
################################
###########....#################
###########......G##############
############.G......############
############........############
########..G#.............#######
#########.G.G................#.#
######..#.......G..............#
#######...G.....G.....#........#
########..............E....##.##
###....G##GG........G.....######
###.###.##............##.#######
###G##.....G..#####...#######..#
##........#..#######..#######..#
#...........#########.##.#....##
#...........#########.......####
#.......E...#########.##......##
#G...G...#..#########.###......#
#...G.......#########E#.#.....##
#....#.....E.#######.......E..##
###.###.......#####...#.E....###
######................#.E....###
#######G.#...#..##.####.......##
#######..E.........######.E.####
#######.##...G.....######..#####
#######..#.G......#######.######
#####....#.#.....#######..######
#####.E..###..##########.#######
#####..######.##########.#######
#####..######..######....#######
######.#######.#####.....#######
################################
"""

# s = """
# ####
# ##E#
# #GG#
# ####
# """

# s = """
# #######
# #E..G.#
# #...#.#
# #.G.#G#
# #######
# """

def get_grid(s):
    g = []
    for line in s.split('\n'):
        if not line.strip():
            continue
        row = []
        for c in line.strip():
            if c in 'EG':
                row.append([c, 200])
            else:
                row.append(c)
        g.append(row)
    return g

# unit: (E|G, i, j, hp)
def get_units(g):
    us = []
    for i in range(len(g)):
        for j in range(len(g[0])):
            if isinstance(g[i][j], list):
                us.append((g[i][j][0], i, j, g[i][j][1]))
    return us

def is_blocked(c):
    return isinstance(c, list) or c == '#'

def get_paths(g, src, dest):
    p = [[float('inf')] * len(g[0]) for _ in range(len(g))]

    def f(i, j, d):
        p[i][j] = d
        if (i, j) == dest:
            return
        for a, b in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ni, nj = i + a, j + b
            if d + 1 < p[ni][nj] and not is_blocked(g[ni][nj]):
                f(ni, nj, d + 1)

    f(src[0], src[1], 0)
    return p

def print_paths(p):
    print('\n'.join(''.join(str(v if v != float('inf') else '.') for v in row) for row in p))

def print_grid(g):
    print()
    for row in g:
        for c in row:
            print(c[0] if isinstance(c, list) else c, end='')
        print('   ' + ', '.join(f'{c[0]}({c[1]})' for c in row if isinstance(c, list)))
    print()

def print_grid2(g):
    print('\n'.join(''.join(c[0] if isinstance(c, list) else c for c in row) for row in g))

# move: (dist, hp, i, j)
def get_step(g, p, i, j):
    ms = []
    for a, b in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        ni, nj = i + a, j + b
        if p[ni][nj] != float('inf'):
            #hp = g[ni][nj][1] if isinstance(g[ni][nj], list) else -1
            #assert p[ni][nj] >= 1
            ms.append((p[ni][nj], -1, ni, nj))
    return min(ms) if ms else None

def get_reachable(g, ut):
    rs = set()
    for u in get_units(g):
        if u[0] == ut:
            continue
        for a, b in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ri, rj = u[1] + a, u[2] + b
            if not is_blocked(g[ri][rj]):
                rs.add((ri, rj))
    return rs

def get_in_range(g, u):
    gs = []
    for a, b in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        ri, rj = u[1] + a, u[2] + b
        if isinstance(g[ri][rj], list) and g[ri][rj][0] != u[0]:
            # (0, hp, i, j)
            gs.append((0, g[ri][rj][1], ri, rj))
    return gs

def try_attack(g, u):
    gs = get_in_range(g, u)
    return (min(gs), do_attack) if gs else None

def get_best_move2(g, u):
    gs = try_attack(g, u)
    if gs:
        return gs
    rs = get_reachable(g, u[0])
    ms = []
    for r in rs:
        p = get_paths(g, r, u[1:3])
        m = get_step(g, p, u[1], u[2])
        if m:
            ms.append(m)

    return (min(ms), do_step) if ms else None

def do_step(g, u, m):
    g[u[1]][u[2]] = '.'
    g[m[2]][m[3]] = [u[0], u[3]]
    return g, (u[0], m[2], m[3], u[3])

def do_attack(g, u, m):
    assert g[m[2]][m[3]][0] != u[0]
    g[m[2]][m[3]][1] -= 3
    if g[m[2]][m[3]][1] <= 0:
        print(f'{g[m[2]][m[3]][0]} KILLED!')
        g[m[2]][m[3]] = '.'
    return g, u

def get_enemy_count(g, ut):
    n = 0
    for u in get_units(g):
        if u[0] != ut:
            n += 1
    return n

def print_units(g):
    for u in get_units(g):
        print(f'{u[0]} r={u[1]} c={u[2]} hp={u[3]}')

#################################

s = """
########
#..E..G#
#G######
########
"""

g = get_grid(s)

print_grid(g)

us = get_units(g)
u = us[0]
print(u)
m = get_best_move2(g, u)
print(m)

# round = 0

# print(f'==== {round} =====')
# print_units(g)
# print_grid2(g)
# print('=======================')

# while True:

#     print(f'==== {round} =====')

#     for u in get_units(g):
#         # if u[0] != 'E':
#         #     continue
#         if g[u[1]][u[2]] == '.':
#             # is already dead
#             continue

#         if get_enemy_count(g, u[0]) == 0:
#             print('DONE>>', round)
#             break

#         m = get_best_move2(g, u)
#         # print(u, m, 'move' if m[0] else 'attack')
#         if m:
#             f = m[1]
#             g, v = f(g, u, m[0])
#             #if move_type == 'step':
#             if f == do_step:
#                 m = try_attack(g, v)
#                 if m:
#                     assert m[1] == do_attack
#                     g, _ = do_attack(g, v, m[0])
#                     #assert mt == 'attack'

#             print(f'{v[0]} r={v[1]} c={v[2]} hp={v[3]}')

#         else:
#             print(f'{u[0]} r={u[1]} c={u[2]} hp={u[3]}')

#     print_grid2(g)
#     print('=======================')

#     # print(f'Round {round}')
#     # print_grid(g)
#     us = get_units(g)
#     # pprint.pprint(us)

#     if len({u[0] for u in us}) == 1:
#         print(f'done in {round}')
#         print(us)
#         print(round * sum(u[3] for u in us))
#         break

#     round += 1

#     if round > 5:
#         break
