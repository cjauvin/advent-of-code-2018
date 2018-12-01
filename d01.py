# with open('d01.txt') as f:
#     vs = f.readlines()

# vs = list(map(int, [l.strip() for l in vs]))
# print(sum(vs))

vs_test = [1, -1]

freqs = {0}
curr_freq = 0
while True:
    for v in vs:
        curr_freq += v
        print(curr_freq)
        if curr_freq in freqs:
            print(curr_freq)
            break
        freqs.add(curr_freq)
    else:
        continue
    break