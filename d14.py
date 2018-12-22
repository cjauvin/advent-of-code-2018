def f(n):
    recipes = [3, 7]
    elves = [0, 1] # 0 is (), 1 is []
    i = 0
    while True:
        r0, r1 = recipes[elves[0]], recipes[elves[1]]
        rec = r0 + r1
        a = rec // 10
        b = rec % 10
        recipes += [a, b] if a else [b]
        elves = [(elves[0] + r0 + 1) % len(recipes), (elves[1] + r1 + 1) % len(recipes)]
        #print(i, recipes, elves)
        if len(recipes) >= n + 10:
            print(recipes)
            return ''.join(map(str, recipes[n:n + 10]))
        i += 1

def g(n):
    recipes = [3, 7]
    elves = [0, 1] # 0 is (), 1 is []
    i = 0
    while True:
        r0, r1 = recipes[elves[0]], recipes[elves[1]]
        rec = r0 + r1
        a = rec // 10
        b = rec % 10
        recipes += [a, b] if a else [b]
        elves = [(elves[0] + r0 + 1) % len(recipes), (elves[1] + r1 + 1) % len(recipes)]
        if recipes[-len(n):] == n:
            return len(recipes) - len(n)
        if recipes[-len(n)-1:-1] == n:
            return len(recipes) - len(n) - 1
        i += 1


# print(f(9))
# print(f(5))
# print(f(18))
#print(f(2018))
#print(f(157901))

#print(g([5,1,5,8,9]))
# print(g([0,1,2,4,5]))
#print(g([9,2,5,1,0]))
#print(g([5,9,4,1,4]))
print(g([1,5,7,9,0,1]))
#print(g([1,5,8,9,1]))
