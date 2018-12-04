import re
import datetime as dt
from collections import defaultdict, Counter

s = open('d04.txt').readlines()
s = [l.strip() for l in s]

d = []
for line in s:
    m = re.search('^\[(.+)\] (.+)', line)
    t = (dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M"), m.group(2))
    d.append(t)

g = None
hs = Counter()
hm = defaultdict(Counter)
for r in sorted(d):
    if r[1].startswith('Guard'):
        g = re.match('Guard #(\d+)', r[1]).group(1)
        #print(g)
    elif r[1] == 'falls asleep':
        start = r[0].minute
    elif r[1] == 'wakes up':
        #print('>>', start, (r[0].hour, r[0].minute))
        for m in range(start, r[0].minute):
            hs[g] += 1
            hm[g][m] += 1

# part 1

g = hs.most_common(1)[0][0]
#print(g)
#print(hm[g].most_common(1))
#print(int(g) * hm[g].most_common(1)[0][0])

# part 2

# g1 is asleep: 3 x m1, 2 x m2
# g2 is asleep: 4 x m1, 1 x m1

max_cmg = (0, 0, '')
for g, c in hm.items():
    minute, cnt = c.most_common(1)[0]
    max_cmg = max(max_cmg, (cnt, minute, g))
print(max_cmg)
