# utils/priority_queue.py

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.entry_set = set()

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
        self.entry_set.add(tuple(item.state))

    def get(self):
        priority, item = heapq.heappop(self.elements)
        self.entry_set.remove(tuple(item.state))
        return item

    def contains(self, state):
        return tuple(state) in self.entry_set
