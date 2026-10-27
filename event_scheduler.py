"""
Event Scheduler
----------------
can_attend_all(events)     -> True if no two events overlap
min_rooms_required(events) -> minimum simultaneous rooms needed
assign_rooms(events)       -> (event, room_name) pairs (future-proofing)

Input format: [(start, end), ...], e.g. [(9, 10), (10, 11), (11, 12)]
Adjacent events (end == start) are NOT considered overlapping.
"""

import heapq


def can_attend_all(events):
    events = sorted(events)                              # sort by start time
    return all(events[i][0] >= events[i - 1][1] for i in range(1, len(events)))


def min_rooms_required(events):
    end_times = []                        # min-heap: end times of rooms in use
    for start, end in sorted(events):
        if end_times and end_times[0] <= start:          # earliest room is free
            heapq.heapreplace(end_times, end)             # reuse that room
        else:                                             # all rooms busy
            heapq.heappush(end_times, end)                # open a new room
    return len(end_times)


def assign_rooms(events):
    """Extends min_rooms_required to return which room each event gets."""
    free, busy, room_of, count = [], [], {}, 0            # busy: (end, room_id)
    for i, (start, end) in sorted(enumerate(events), key=lambda x: x[1]):
        while busy and busy[0][0] <= start:                # release finished rooms
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)                     # lowest-numbered free room
        else:
            room, count = count, count + 1                 # open a brand new room
        heapq.heappush(busy, (end, room))
        room_of[i] = room

    def name(r):
        return f"Room {chr(65 + r)}" if r < 26 else f"Room {r + 1}"

    return [(events[i], name(room_of[i])) for i in range(len(events))]
