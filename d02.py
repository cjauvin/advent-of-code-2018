from collections import Counter

s2 = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""

n2 = 0
n3 = 0

#for line in s.split('\n'):
for line in open('d02.txt'):
    line = line.strip()
    vs = set(Counter(line).values())
    n2 += 1 if 2 in vs else 0
    n3 += 1 if 3 in vs else 0

print(n2, n3)
print(n2 * n3)

s = [l.strip() for l in open('d02.txt')]

# part 2

def diff(a, b):
    return ''.join([a[i] for i in range(len(a)) if a[i] == b[i]])

print(diff('abcde', 'axcye'))
print(diff('fghij', 'fguij'))

ss = sorted(s)
for i, t in enumerate(ss[1:], 1):
    d = diff(t, ss[i-1])
    # print(len(t), len(d))
    if len(d) == len(t) - 1:
        print(t, ss[i-1], d)


