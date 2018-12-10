import re
from collections import defaultdict

s = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

s = open('d10.txt').readlines()

d = defaultdict(lambda: defaultdict(list))
#for l in s.split('\n'):
for l in s:
    vs = list(map(int, re.findall('[-\d]+', l)))
    d[vs[0]][vs[1]].append(vs[2:])

def get_bounding_box(d):
    xs = [float('inf'), float('-inf')]
    ys = [float('inf'), float('-inf')]
    for i in d:
        for j in d[i]:
            xs[0] = min(i - 1, xs[0])
            xs[1] = max(i + 1, xs[1])
            ys[0] = min(j - 1, ys[0])
            ys[1] = max(j + 1, ys[1])
    return xs + ys

#print(get_bounding_box())

def print_grid(d, b=None):
    if b is None:
        b = get_bounding_box(d)
    print()#get_bounding_box())
    for j, y in enumerate(range(b[2], b[3])):
        for i, x in enumerate(range(b[0], b[1])):
            print('#' if x in d and y in d[x] else '.', end='')
        print()
    print()

def evolve(d):
    d2 = defaultdict(lambda: defaultdict(list))
    for i in d:
        for j in d[i]:
            # print(i, j, d[i][j])
            #p = d[i][j]
            for p in d[i][j]:
                d2[i + p[0]][j + p[1]].append(p)
    return d2

m = [float('inf'), float('inf')]

for i in range(100000):
    b = get_bounding_box(d)
    xb, yb = b[1] - b[0], b[3] - b[2]
    m[0] = min(xb, m[0])
    m[1] = min(yb, m[1])
    if i % 1000 == 0:
        print(m)
    if xb < 64:
        print(i)
        print_grid(d)
        break
    d = evolve(d)

#print_grid(d, b)
# for _ in range(3):
#     d = evolve(d)
# print_grid(d, b)
