"""Quick sanity tests for lru_cache.py and event_scheduler.py."""

import threading
from lru_cache import LRUCache, ThreadSafeLRUCache
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms


def test_lru_cache():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                       # evicts key 2 (least recently used)
    assert c.get(2) == -1
    c.put(4, 4)                       # evicts key 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    print("LRUCache: all tests passed")


def test_event_scheduler():
    no_overlap = [(9, 10), (10, 11), (11, 12)]
    overlap = [(9, 11), (10, 12), (11, 13), (13, 14)]

    assert can_attend_all(no_overlap) is True
    assert can_attend_all(overlap) is False
    assert min_rooms_required(no_overlap) == 1
    assert min_rooms_required(overlap) == 2
    assert min_rooms_required([]) == 0

    print("Event scheduler: all tests passed")
    print("Room assignment for", overlap, "->")
    for ev, room in assign_rooms(overlap):
        print("   ", ev, "->", room)


def test_thread_safety():
    cache = ThreadSafeLRUCache(100)

    def worker():
        for i in range(2000):
            cache.put(i % 150, i)
            cache.get(i % 150)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert len(cache.map) == 100
    print("ThreadSafeLRUCache: no corruption under concurrent access")


if __name__ == "__main__":
    test_lru_cache()
    test_event_scheduler()
    test_thread_safety()
