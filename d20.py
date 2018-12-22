from collections import defaultdict


class Node:
    def __init__(self, elems=None):
        self.elems = elems if elems else []

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        return f'{type(self).__name__}: {self.elems}'


class AndNode(Node):
    def __init__(self, elems=None):
        if type(elems) is str:
            elems = list(elems)
        super().__init__(elems)

    def __str__(self):
        return ''.join(str(e) for e in self.elems)

    @staticmethod
    def create(s):
        node = AndNode()
        i = 0
        while i < len(s):
            c = s[i]
            if c == '(':
                or_node = OrNode.create(s[i + 1:])
                node.elems.append(or_node)
                i += len(or_node)
            elif c == '|':
                return node
            elif c == ')':
                return node
            elif c in '^$':
                i += 1
            else:
                node.elems.append(c)  # xxx
                i += 1
        return node


class OrNode(Node):
    def __init__(self, elems=None):
        super().__init__(elems)

    def __str__(self):
        s = '|'.join(str(e) for e in self.elems)
        return f'({s})'

    @staticmethod
    def create(s):
        node = OrNode()
        i = 0
        while i < len(s):
            if s[i] == ')':
                return node
            elif s[i] == '|':
                i += 1
            # elif s[i] == '(':
            #     assert False
            and_node = AndNode.create(s[i:])
            node.elems.append(and_node)
            i += len(and_node)
        return node


def follow(node, i=0, j=0):
    if isinstance(node, AndNode):
        for e in node.elems:
            if isinstance(e, str):
                g[(i, j)].add(e)
                if e == 'S':
                    i += 1
                    g[(i, j)].add('N')
                elif e =='N':
                    i -= 1
                    g[(i, j)].add('S')
                elif e == 'W':
                    j -= 1
                    g[(i, j)].add('E')
                else:
                    j += 1
                    g[(i, j)].add('W')
            else:
                follow(e, i, j)
    elif isinstance(node, OrNode):
        for e in node.elems:
            follow(e, i, j)
    else:
        assert False


def print_grid(g):
    ijs = g.keys()
    dims = (min([x[0] for x in ijs]), max([x[0] for x in ijs]),
            min([x[1] for x in ijs]), max([x[1] for x in ijs]))
    # print(dims)
    h = []
    for i in range(dims[0], dims[1] + 1):
        r0 = []
        r1 = ['#']
        r2 = []
        for j in range(dims[2], dims[3] + 1):
            # print(f'({i},{j}) -> {g[(i,j)]}')
            r0.append('-' if 'N' in g[(i, j)] else '#')
            r1 += ['X' if (i, j) == (0, 0) else '.', '|' if 'E' in g[(i, j)] else '#']
            r2.append('-' if 'S' in g[(i, j)] else '#')
        r0 = '#' + '#'.join(r0) + '#'
        r2 = '#' + '#'.join(r2) + '#'
        if i == dims[0]:
            h.extend([r0, r1, r2])
        else:
            h.extend([r1, r2])
    print()
    for r in h:
        print(''.join(r))


def furthest_room_dist(g, part=1):

    def f(p, e):
        if e == 'E': return (p[0], p[1] + 1)
        elif e == 'W': return (p[0], p[1] - 1)
        elif e == 'S': return (p[0] + 1, p[1])
        elif e == 'N': return (p[0] - 1, p[1])

    d = defaultdict(lambda: float('inf'))  # (i, j) -> dist
    to_visit = [((0, 0), 0)]
    while to_visit:
        p, dist = to_visit.pop()
        d[p] = dist
        for e in 'EWSN':
            q = f(p, e)
            if e in g[p] and dist + 1 < d[q]:
                to_visit.append((q, dist + 1))

    if part == 1:
        return max(d.values())
    else:
        return len([v for v in d.values() if v >= 1000])


#a = AndNode.create('^ENWWW(NEEE|SSE(EE|N))$')
#a = AndNode.create('^ENWWW$')
#follow(AndNode.create('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'))
#follow(AndNode.create('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'))
#follow(AndNode.create('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'))

#  ^ENWWW(NEEE|SSE(EE|N))$
#  ENWWW--> NEEE
#       |-> SSE  --> EE
#                |-> N

import sys
sys.setrecursionlimit(10000)

s = open('d20.txt').read().strip()

g = defaultdict(set)  # (i, j) -> {E, W, S, N}

follow(AndNode.create(s))
print_grid(g)
print()
print(furthest_room_dist(g, 1))
print(furthest_room_dist(g, 2))
