from collections import Counter

s = '459 players; last marble is worth 71790 points'

# Thanks: https://www.sanfoundry.com/python-program-implement-circular-doubly-linked-list/

class Node:
    def __init__(self, data):
       self.data = data
       self.next = None
       self.prev = None


class CircularDoublyLinkedList:
    def __init__(self):
        self.first = None

    def get_node(self, index):
        current = self.first
        for i in range(index):
            current = current.next
            if current == self.first:
                return None
        return current

    def insert_after(self, ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    def insert_before(self, ref_node, new_node):
        self.insert_after(ref_node.prev, new_node)

    def insert_at_end(self, new_node):
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.first.prev, new_node)

    def insert_at_beg(self, new_node):
        self.insert_at_end(new_node)
        self.first = new_node

    def remove(self, node):
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next

    def display(self):
        if self.first is None:
            return
        current = self.first
        while True:
            print(current.data, end = ' ')
            current = current.next
            if current == self.first:
                break

    def as_list(self):
        if self.first is None:
            return []
        lst = []
        curr = self.first
        while True:
            lst.append(curr.data)
            curr = curr.next
            if curr == self.first:
                break
        return lst


def play(n_players, n_marbles):

    player = 0
    score = Counter()

    ll = CircularDoublyLinkedList()
    ll.insert_at_end(Node(0))
    curr = ll.first

    for i in range(1, n_marbles + 1):

        if i % 23 == 0:
            score[player + 1] += i
            for j in range(7):
                curr = curr.prev
            # print('stop:', curr.data)
            ll.remove(curr)
            score[player + 1] += curr.data
            curr = curr.next
            # print('new:', curr.data)
            #print(f'> {player + 1}: ', ll.as_list())
        else:
            ni = Node(i)
            ll.insert_after(curr.next, ni)
            curr = ni
        # print(f'{player + 1}: ', ll.as_list())
        player += 1
        player %= n_players

    return score.most_common(1)[0][1]

assert play(9, 25) == 32
assert play(10, 1618) == 8317
assert play(13, 7999) == 146373
assert play(17, 1104) == 2764
assert play(21, 6111) == 54718
assert play(30, 5807) == 37305

#print(play(459, 71790))
print(play(459, 7179000))
