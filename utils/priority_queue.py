# utils/priority_queue.py

import heapq

class PriorityQueue:
    "Reference: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes"
    REMOVED = "<removed-item>"
    
    
    def __init__(self):
        self.pq = []  # Store entries (including outdated ones) as priority queue 
        self.entries = {}  # Map item and entry. Used to access entries in priority queue
        self.counter = 0  # Handle entries with equal priority


    def __contains__(self, entry_key):
        return entry_key in self.entries
    
    
    def __len__(self):
        return len(self.entries)
    
    
    def add(self, item, priority):
        "Add new item or update the priority of the current item."
        if tuple(item.state) in self.entries:
            self.remove(item)
        entry = [priority, self.counter, item]
        self.entries[tuple(item.state)] = entry
        heapq.heappush(self.pq, entry)
        self.counter += 1
        

    def remove(self, item):
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        outdated_entry = self.entries.pop(tuple(item.state))
        outdated_entry[-1] = self.REMOVED


    def pop(self):
        "Remove and return the lowest priority item. Raise KeyError if empty."
        while self.entries:
            priority, _, item = heapq.heappop(self.pq)
            if item is not self.REMOVED:
                del self.entries[tuple(item.state)]
                return item, priority
        raise KeyError("pop from an empty priority queue")

    
    def get_priority(self, entry_key):
        "Return priority of existing item. Raise KeyError if not found."
        return self.entries[entry_key][0]