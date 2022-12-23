from collections import deque, Counter

with open("inp.txt") as f:
    inp = f.read().splitlines()

def move_north(x,y):
    if set(((x-1, y-1), (x, y-1), (x+1, y-1))).intersection(elves):
        return False
    return (x, y-1)

def move_south(x,y):
    if set(((x-1, y+1), (x, y+1), (x+1, y+1))).intersection(elves):
        return False
    return (x, y+1)

def move_west(x,y):
    if set(((x-1, y-1), (x-1, y), (x-1, y+1))).intersection(elves):
        return False
    return (x-1, y)

def move_east(x,y):
    if set(((x+1, y-1), (x+1, y), (x+1, y+1))).intersection(elves):
        return False
    return (x+1, y)


# Set up elf coordinates
elves = set()
for y, line in enumerate(inp):
    for x, char in enumerate(line):
        if char == "#":
            elves.add((x, y))
# Set up move order
moves = deque((move_north, move_south, move_west, move_east))

round_count = 0
while True:
    round_count += 1
    ### First half
    proposed = {}
    for elf in elves:
        next_coords = False
        directions = 0
        for move in moves:
            # For each direction, check if there are any overlaps with current elf positions
            new_coords = move(*elf)
            if new_coords:
                directions += 1
            # Only save the first possible move
            if not next_coords:
                next_coords = new_coords

        # Add proposition if 1-3 directions available. (0: Can't move. 4: Won't move)
        if 0 < directions < 4:
            proposed[elf] = next_coords

    ### Second half
    # Check for collisions
    to_remove = set()
    proposal_list = Counter(proposed.values())
    for k, v in proposed.items():
        if proposal_list[v] > 1:
            to_remove.add(k)

    # Remove collisions from proposal
    for k in to_remove:
        proposed.pop(k)

    ### Part 2 - No elf wants to move? We're done!
    if len(proposed) == 0:
        print(f"Part 2: {round_count} rounds.")
        break

    # Actually move
    for old_pos, new_pos in proposed.items():
        elves.discard(old_pos)
        elves.add(new_pos)

    # Shift move order
    moves.rotate(-1)

    ### Part 1 - End of round 10, how many empty tiles are there?
    if round_count == 10:
        min_y = max_y = min_x = max_x = 0
        for x, y in elves:
            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y
        empty = ((max_x+1 - min_x) * (max_y+1 - min_y)) - len(elves)
        print(f"Part 1: {empty} empty tiles.")
