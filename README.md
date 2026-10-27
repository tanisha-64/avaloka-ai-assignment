# Data Structures & Systems Design Assignment

AI / Multi-Agent Systems Intern — Avaloka (Guruvai Sciences)
Author: Tanisha Gupta

## Files

- `lru_cache.py` — `LRUCache` (O(1) get/put) and `ThreadSafeLRUCache`
- `event_scheduler.py` — `can_attend_all`, `min_rooms_required`, `assign_rooms`
- `test_solutions.py` — sanity tests for both problems

## Run

```bash
python test_solutions.py
```

## Summary

**Problem 1 (LRU Cache):** hash map (O(1) lookup) + doubly linked list
(O(1) reorder/evict) combined to get O(1) `get` and `put`.

**Problem 2 (Event Scheduler):** `can_attend_all` sorts events and checks
for any overlap between consecutive events. `min_rooms_required` uses a
min-heap of room end-times to track the maximum number of rooms needed at
once. `assign_rooms` extends this to return an actual room label per event.

Full write-up (approach, complexity analysis, trade-offs, concurrency) is
in the submitted PDF.
