"""
LRU (Least Recently Used) Cache
--------------------------------
get(key) and put(key, value) both run in O(1) time.

Approach:
A hash map gives O(1) lookup of a key but has no sense of usage order.
A doubly linked list keeps nodes ordered by recency and lets us move /
remove / insert any node in O(1) because each node holds direct pointers
to its neighbours. Combining the two gives O(1) for both operations:
  - map:  key -> Node   (O(1) access to the node object)
  - list: head (most recently used) ... tail (least recently used)
"""


class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key, self.val, self.prev, self.next = key, val, None, None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.cap = capacity
        self.map = {}                                   # key -> Node
        self.head, self.tail = Node(), Node()            # sentinels
        self.head.next, self.tail.prev = self.tail, self.head
        # head.next = most recently used, tail.prev = least recently used

    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_front(node)                            # mark as recently used
        return node.val

    def put(self, key, value):
        if key in self.map:                              # update existing key
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) == self.cap:                     # evict LRU item
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)


class ThreadSafeLRUCache(LRUCache):
    """Thread-safe variant: a single lock guards get() and put()."""

    def __init__(self, capacity: int):
        import threading
        super().__init__(capacity)
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            return super().get(key)

    def put(self, key, value):
        with self._lock:
            super().put(key, value)
