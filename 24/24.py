import numpy as np
from collections import defaultdict

with open("inp.txt") as f:
    valley = np.array([list(x) for x in f.read().splitlines()])

# Store each coord in dict with a list of blizzards
orig_bliz_dict = {}
walls = set()
for y,row in enumerate(valley):
    for x,space in enumerate(row):
        if space in (">","v","<","^"):
            orig_bliz_dict[(x,y)] = [space]
        if space == "#":
            walls.add((x,y))

# Add extra walls so we don't leave the valley
walls.add((1,-1))
walls.add((valley.shape[1] - 2, valley.shape[0]))

directions = {
    ">": lambda x, y: (x+1, y),
    "v": lambda x, y: (x, y+1),
    "<": lambda x, y: (x-1, y),
    "^": lambda x, y: (x, y-1)}

def move_blizzards(bliz_dict):
    """Shifts the blizzards in their direction, wrapping around the valley"""
    new_bliz = defaultdict(list)
    for coords, blizzards in bliz_dict.items():
        for bliz in blizzards:
            x, y = directions[bliz](*coords)

            # Handle wall collisions
            if x == valley.shape[1] - 1:
                x = 1
            elif x == 0:
                x = valley.shape[1] - 2
            elif y == valley.shape[0] - 1:
                y = 1
            elif y == 0:
                y = valley.shape[0] - 2

            new_bliz[(x,y)].append(bliz)

    return new_bliz

def adjacent(coords, bliz_dict):
    """Returns a list of coords of available adjacent spaces"""
    global walls
    x, y = coords
    available = []
    for dx, dy in [(1, 0), (0, 1), (0, 0), (0, -1), (-1, 0)]:
        if (x+dx, y+dy) in bliz_dict or (x+dx, y+dy) in walls:
            continue
        else:
            available.append((x+dx,y+dy))

    return available


def expedition(mins, pos, end, offset):
    global seen, max_mins, t_blizzards

    # Check if we have been in this spot, at this time already
    hash = tuple([mins, pos])
    if hash in seen:
        return seen[hash]

    # Early stop if we have a better score already
    if len(seen) > 0 and mins > min(seen.values()):
        return np.inf

    # Early stop if we won't make it to the end before our arbitrary max minutes
    if abs(end[0] - pos[0]) + abs(end[1] - pos[1]) > max_mins - mins:
        return np.inf

    # Early stop if we reach our maximum minutes
    if mins == max_mins:
        return np.inf

    # We reached the end of this path!
    if pos == end:
        return mins

    mins += 1

    # Get possible moves
    possible = adjacent(pos, t_blizzards[mins+offset % len(t_blizzards)])

    result = np.inf
    if len(possible) > 0:
        # Move (or wait)
        for coords in possible:
            # Recursively explore next possible paths, finding the lowest result
            result = min(result, expedition(mins, coords, end, offset))

    # Add our best result from this location
    seen[hash] = result
    return result


# Pre-compute all possible blizzard at each minute
t_blizzards = defaultdict(set)
next = orig_bliz_dict.copy()
for i in range(valley.shape[0]*valley.shape[1]):
    next = move_blizzards(next)
    t_blizzards[i+1] = set(next.keys())


seen = {}
start = (1, 0)
end = (valley.shape[1] - 2, valley.shape[0] - 1)
max_mins = 300  # arbitrary, but has to be big enough to find at least 1 path

total_time = 0
total_time += expedition(0, start, end, 0)
print(f"Minutes to complete part 1: {total_time}")

seen = {}
time = expedition(0, end, start, total_time)
total_time += time
# print(f"Minutes to return: {time} (Total: {total_time})")

seen = {}
time = expedition(0, start, end, total_time)
total_time += time
# print(f"Minutes to end: {time}.")
print(f"Minutes to complete part 2: {total_time}.")
