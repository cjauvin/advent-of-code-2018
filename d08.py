import re

#s = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
s = open('d08.txt').read()
s = list(map(int, re.findall('\d+', s)))

#print(s)

sum_entries = 0

def tree(t):
    global sum_entries
    n_children = t[0]
    n_entries = t[1]
    node = {'children': []}
    offset = 2
    for i in range(n_children):
        child, child_offset = tree(t[offset:])
        offset += child_offset
        node['children'].append(child)
    node['entries'] = t[offset:offset + n_entries]
    sum_entries += sum(node['entries'])
    node['value'] = 0
    if not node['children']:
        node['value'] = sum(node['entries'])
    else:
        for e in node['entries']:
            if e == 0:
                continue
            if e <= len(node['children']):
                node['value'] += node['children'][e - 1]['value']
    return node, offset + n_entries

root, offset = tree(s)

# tree: 2 3 0 3 .. (2 children, 3 entries)
#   tree 0 3 10 .. (0 children, 3 entries) -> offset=2+3
#   tree

# Part 1

print(sum_entries)

# Part 2

print(root['value'])
