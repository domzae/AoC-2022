# Assumes the cube layout:
#  AB
#  C
# ED
# F

import numpy as np
import regex as re
from collections import deque

with open("inp.txt") as f:
    inp = f.read().splitlines()

instructions = [int(x) if x.isnumeric() else x for x in re.findall('\d+|[A-Z]', inp[-1])]

max_x = max((len(x) for x in inp[:-2]))
mmap = np.array([list(x.ljust(max_x)) for x in inp[:-2]])


class Face:
    def __init__(self, x, y, sides):
        self.offsets = x, y
        self.map = mmap[y:y+50, x:x+50]
        self.sides = sides

    def shift(self, dir, x, y):
        """Shift over an edge of the cube.
        Returns new face, newx/y, and new direction"""
        this = self.sides[dir]
        n_face = this[0]
        n_x, n_y = this[1](x, y)
        n_dir = this[2]

        return n_face, n_x, n_y, n_dir


# x, y offsets to split the cube into it's faces
A = 50, 0
B = 100, 0
C = 50, 50
D = 50, 100
E = 0, 100
F = 0, 150

# Hard-coding what happens at each edge, for each face (feelsbadman)
# current_direction: [new_face, new_(x,y), new_direction]
A_sides = {
    ">": ["B", lambda x, y: (0, y), ">"],
    "v": ["C", lambda x, y: (x, 0), "v"],
    "<": ["E", lambda x, y: (0, 49 - y), ">"],
    "^": ["F", lambda x, y: (0, x), ">"],
}

B_sides = {
    ">": ["D", lambda x, y: (49, 49 - y), "<"],
    "v": ["C", lambda x, y: (49, x), "<"],
    "<": ["A", lambda x, y: (49, y), "<"],
    "^": ["F", lambda x, y: (x, 49), "^"],
}

C_sides = {
    ">": ["B", lambda x, y: (y, 49), "^"],
    "v": ["D", lambda x, y: (x, 0), "v"],
    "<": ["E", lambda x, y: (y, 0), "v"],
    "^": ["A", lambda x, y: (x, 49), "^"]
}

D_sides = {
    ">": ["B", lambda x, y: (49, 49 - y), "<"],
    "v": ["F", lambda x, y: (49, x), "<"],
    "<": ["E", lambda x, y: (49, y), "<"],
    "^": ["C", lambda x, y: (x, 49), "^"],
}

E_sides = {
    ">": ["D", lambda x, y: (0, y), ">"],
    "v": ["F", lambda x, y: (x, 0), "v"],
    "<": ["A", lambda x, y: (0, 49 - y), ">"],
    "^": ["C", lambda x, y: (0, x), ">"],
}

F_sides = {
    ">": ["D", lambda x, y: (y, 49), "^"],
    "v": ["B", lambda x, y: (x, 0), "v"],
    "<": ["A", lambda x, y: (y, 0), "v"],
    "^": ["E", lambda x, y: (x, 49), "^"],
}

# Initialize our cube faces into a dictionary
faces = {
    "A": Face(*A, A_sides),
    "B": Face(*B, B_sides),
    "C": Face(*C, C_sides),
    "D": Face(*D, D_sides),
    "E": Face(*E, E_sides),
    "F": Face(*F, F_sides),
}

# Set up our directions
dirs = deque((">", "v", "<", "^"))

# Starting vars, keep track of our current face and relative y,x coords.
loc = ("A", (0, 0))
dir = ">"

# Main logic starts here
for instr in instructions:
    if isinstance(instr, int):

        # We count down our steps
        while instr > 0:
            instr -= 1
            face, (y, x) = loc

            # For each direction, check if we need to "shift" over the edge
            # If we hit a block, break out of our countdown loop
            # Otherwise move into our new space and set our new "loc"/"dir"
            if dir == ">":
                if x+1 == 50:
                    n_face, n_x, n_y, n_dir = faces[face].shift(dir, x, y)
                    if faces[n_face].map[n_y, n_x] == "#":
                        break
                    loc = (n_face, (n_y, n_x))
                    dir = n_dir
                else:
                    if faces[face].map[y, x+1] == "#":
                        break
                    loc = (face, (y, x+1))

            elif dir == "v":
                if y+1 == 50:
                    n_face, n_x, n_y, n_dir = faces[face].shift(dir, x, y)
                    if faces[n_face].map[n_y, n_x] == "#":
                        break
                    loc = (n_face, (n_y, n_x))
                    dir = n_dir
                else:
                    if faces[face].map[y+1, x] == "#":
                        break
                    loc = (face, (y+1, x))

            elif dir == "<":
                if x-1 == -1:
                    n_face, n_x, n_y, n_dir = faces[face].shift(dir, x, y)
                    if faces[n_face].map[n_y, n_x] == "#":
                        break
                    loc = (n_face, (n_y, n_x))
                    dir = n_dir
                else:
                    if faces[face].map[y, x-1] == "#":
                        break
                    loc = (face, (y, x-1))

            elif dir == "^":
                if y-1 == -1:
                    n_face, n_x, n_y, n_dir = faces[face].shift(dir, x, y)
                    if faces[n_face].map[n_y, n_x] == "#":
                        break
                    loc = (n_face, (n_y, n_x))
                    dir = n_dir
                else:
                    if faces[face].map[y-1, x] == "#":
                        break
                    loc = (face, (y-1, x))

    # Find the next direction to face
    else:
        while not dirs[0] == dir:
            dirs.rotate(1)
        if instr == "R":
            dirs.rotate(-1)
        else:
            dirs.rotate(1)
        dir = dirs[0]


# Scores for our ending direction
dir_score = {
    ">": 0,
    "v": 1,
    "<": 2,
    "^": 3
}

face, (y, x) = loc
print(f"Finished at: Face {face}. Row {y+1}. Column {x+1}. Direction {dir}.")

# Add our offsets from our current face to get the coords on the "monkey map"
x_offset, y_offset = faces[face].offsets
print(
    f"Password: {(1000 * (y+y_offset+1)) + (4 * (x+x_offset+1)) + dir_score[dir]}")
