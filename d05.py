s = open('d05.txt').readlines()[0].strip()

#s = 'dabAcCaCBAcCcaDA'

def react(s):
    while True:
        found = False
        t = []
        for i in range(0, len(s), 2):
            ss = s[i:i+2]
            a = set(ss)
            b = set(ss.lower())
            if len(a) == 2 and len(b) == 1:
                # print('Remove:', ss)
                found = True
            else:
                t += ss
        s = ''.join(t)
        t = [s[0]]
        for i in range(1, len(s), 2):
            ss = s[i:i+2]
            a = set(ss)
            b = set(ss.lower())
            if len(a) == 2 and len(b) == 1:
                # print('Remove:', ss)
                found = True
            else:
                t += ss
        s = ''.join(t)
        #print(len(s))
        if not found:
            break
    return s

def remove(s, c):
    return ''.join(d for d in s if d not in {c, c.upper()})

# Part 1
#print(len(react(s)))

# Part 2
m = float('inf')
for c in set(s.lower()):
    t = remove(s, c)
    n = len(react(t))
    print(c, n)
    m = min(n, m)
print(m)
