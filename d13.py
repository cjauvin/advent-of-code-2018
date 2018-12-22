from collections import defaultdict

s = r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """

#g = list(map(list, s.split("\n")[1:]))
g = list(map(list, open('d13.txt').read().split('\n')))

ts = {}
tid = 0
for i, row in enumerate(g):
    for j, col in enumerate(row):
        if col in '<>v^':
            ts[(tid, i, j)] = (col, 0) # choice=0,1,2
            g[i][j] = '-' if col in '<>' else '|'
            tid += 1

#choice = 0

def show(ts):
    for i, row in enumerate(g):
        for j, col in enumerate(row):
            if (i, j) in ts:
                print(ts[(i, j)][0], end='')
            else:
                print(g[i][j], end='')
        print()
    print()

def tick(ts):
    #global g, choice
    new_ts = {}
    crash = None
    for tid, i, j in sorted(ts):
        #curr, choice = ts[pos]
        pos = (i, j)
        # print(pos, curr)
        if curr == '>':
            new_pos = (pos[0], pos[1] + 1)
        elif curr == '<':
            new_pos = (pos[0], pos[1] - 1)
        elif curr == 'v':
            new_pos = (pos[0] + 1, pos[1])
        elif curr == '^':
            new_pos = (pos[0] - 1, pos[1])

        nxt_cell = g[new_pos[0]][new_pos[1]]
        assert nxt_cell in '<>v^+\\/-|', nxt_cell

        if new_pos in new_ts:
            print('!!')
            crash = new_pos

        # print(pos, curr, new_pos, nxt_cell)

        if curr == '>':
            if nxt_cell == '+':
                if choice == 0:
                    nxt = '^'
                elif choice == 1:
                    nxt = '>'
                else:
                    nxt = 'v'
                choice += 1
                choice %= 3
            elif nxt_cell == '\\':
                nxt = 'v'
            elif nxt_cell == '/':
                nxt = '^'
            else:
                nxt = curr

        elif curr == '<':
            if nxt_cell == '+':
                if choice == 0:
                    nxt = 'v'
                elif choice == 1:
                    nxt = '<'
                else:
                    nxt = '^'
                choice += 1
                choice %= 3
            elif nxt_cell == '\\':
                nxt = '^'
            elif nxt_cell == '/':
                nxt = 'v'
            else:
                nxt = curr

        elif curr == 'v':
            if nxt_cell == '+':
                if choice == 0:
                    nxt = '>'
                elif choice == 1:
                    nxt = 'v'
                else:
                    nxt = '<'
                choice += 1
                choice %= 3
            elif nxt_cell == '\\':
                nxt = '>'
            elif nxt_cell == '/':
                nxt = '<'
            else:
                nxt = curr
        elif curr == '^':
            if nxt_cell == '+':
                if choice == 0:
                    nxt = '<'
                elif choice == 1:
                    nxt = '^'
                else:
                    nxt = '>'
                choice += 1
                choice %= 3
            elif nxt_cell == '\\':
                nxt = '<'
            elif nxt_cell == '/':
                nxt = '>'
            else:
                nxt = curr

        # print(new_pos, nxt, choice)
        new_ts[new_pos] = (nxt, choice)

    return new_ts, crash

#for i in range(14):
i = 0
while True:
    print(i)
    i += 1
    # if i > 3:
    #     break
    # show(ts)
    ts, crash = tick(ts)
    if crash:
        print(crash)
        break
