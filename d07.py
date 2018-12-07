import re
from collections import defaultdict
import heapq

s = open('d07.txt').readlines()

# s = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.""".split('\n')

steps = []
nodes = set()
for line in s:
    st = re.findall('[A-Z]', line[1:])
    steps.append(st)
    nodes |= set(st)

# a -> [b, c, ..]

req = defaultdict(set)
parent = {}
roots = []

for a, b in steps:
    req[b].add(a)
    parent[b] = a

roots = nodes - set(parent.keys())

# Part 1

to_visit = list(roots)
heapq.heapify(to_visit)
done = set()
path = []
while True:
    a = heapq.heappop(to_visit)
    done.add(a)
    path.append(a)
    for a, b in req.items():
        if not (b - done) and a not in (set(to_visit) | done):
            heapq.heappush(to_visit, a)
    if not to_visit:
        break

print(''.join(path))

# Part 2

workers = defaultdict(int) # task -> n_seconds remaining to finish current work
n_workers = 5
base_time = 60
curr_time = 0

to_visit = list(roots)
heapq.heapify(to_visit)
done = set()
path = []

while True:

    while len(workers) < n_workers and to_visit:
        a = heapq.heappop(to_visit)
        workers[a] = base_time + ord(a) - 64

    # print(curr_time, workers)

    tasks_to_delete = []
    for a in workers:
        workers[a] -= 1
        if workers[a] == 0:
            done.add(a)
            path.append(a)
            tasks_to_delete.append(a)

    for a in tasks_to_delete:
        del workers[a]

    for a, b in req.items():
        reqs_satisfied = not (b - done)
        if reqs_satisfied and a not in (set(to_visit) | done) and a not in workers:
            heapq.heappush(to_visit, a)

    curr_time += 1

    if not to_visit and not workers:
        break

print(curr_time)
print(''.join(path))
