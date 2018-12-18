import re
from collections import defaultdict


def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def and_(a, b):
    return a & b

def or_(a, b):
    return a | b

def set_(a, b):
    return a

def gt(a, b):
    return 1 if a > b else 0

def eq(a, b):
    return 1 if a == b else 0

opcodes = {
    'addr': (add, False, False), # is_value
    'addi': (add, False, True),
    'mulr': (mul, False, False),
    'muli': (mul, False, True),
    'banr': (and_, False, False),
    'bani': (and_, False, True),
    'borr': (or_, False, False),
    'bori': (or_, False, True),
    'setr': (set_, False, True),
    'seti': (set_, True, True),

    'gtir': (gt, True, False),
    'gtri': (gt, False, True),
    'gtrr': (gt, False, False),

    'eqir': (eq, True, False),
    'eqri': (eq, False, True),
    'eqrr': (eq, False, False)
}

def execute(inst, before):
    op, a, b, c = inst
    after = before[:]
    func, a_is_value, b_is_value = opcodes[op]
    after[c] = func(a if a_is_value else before[a], b if b_is_value else before[b])
    return after

# print(execute(('mulr', 2, 1, 2), [3, 2, 1, 1]))
# print(execute(('addi', 2, 1, 2), [3, 2, 1, 1]))
# print(execute(('seti', 2, 1, 2), [3, 2, 1, 1]))

def n_similar(inst, before, after):
    _, a, b, c = inst
    n = 0
    for op, impl in opcodes.items():
        aft = execute([op] + [a, b, c], before)
        func, a_is_value, b_is_value = impl
        n += 1 if aft == after else 0
    return n

def get_similar(inst, before, after):
    _, a, b, c = inst
    s = set()
    for op, impl in opcodes.items():
        aft = execute([op] + [a, b, c], before)
        func, a_is_value, b_is_value = impl
        s |= {op} if aft == after else set()
    return s

befores = []
insts = []
afters = []
in_prog = False
prog = []
for line in open('d16.txt'):
    line = line.strip()
    if not line:
        continue
    if line == '===':
        # in_prog = True
        #continue
        break
    # if not in_prog:
    #     continue
    # prog.append(list(map(int, re.findall('\d+', line))))
    if line.startswith('Before:'):
        befores.append(list(map(int, re.findall('\d+', line))))
    elif line.startswith('After:'):
        afters.append(list(map(int, re.findall('\d+', line))))
    else:
        insts.append(list(map(int, re.findall('\d+', line))))

#print(n_similar(('mulr', 2, 1, 2), [3, 2, 1, 1], [3, 2, 2, 1]))

assert len(befores) == len(afters) == len(insts)

# n = 0
# for i in range(len(befores)):
#     n += 1 if n_similar(insts[i], befores[i], afters[i]) >= 3 else 0
# print(n)

# A = {
#     0: 'muli',
#     6: 'addi',
#     10: 'addr',
#     9: 'mulr',
#     11: 'borr',
#     1: 'seti',
#     12: 'bori',
#     15: 'setr',
#     2: 'bani',
#     14: 'banr',
#     7: 'gtir',
#     13: 'eqri',
#     5: 'eqrr',
#     8: 'eqir',
#     4: 'gtrr',
#     3: 'gtri'
# }

opi_to_op = {}

while len(opi_to_op) < len(opcodes):

    d = defaultdict(set)

    for i in range(len(befores)):
        opi = insts[i][0]
        for op in get_similar(insts[i], befores[i], afters[i]):
            if opi not in opi_to_op:
                d[op].add(opi)

    for op, opis in d.items():
        if len(opis) == 1:
            opi = list(opis)[0]
            print(f'{opi} -> {op}')
            opi_to_op[opi] = op

# regs = [0, 0, 0, 0]

# for inst in prog:
#     opi, a, b, c = inst
#     func, a_is_value, b_is_value = opcodes[A[opi]]
#     regs[c] = func(a if a_is_value else regs[a], b if b_is_value else regs[b])

# print(regs)
