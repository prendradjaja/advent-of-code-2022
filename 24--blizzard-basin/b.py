import sys
import collections
import math


DIRECTIONS = {
    '>': ( 0,  1),
    '<': ( 0, -1),
    'v': ( 1,  0),
    '^': (-1,  0),
}


def main(path):
    # Parse
    text = open(path).read()
    room_grid_2d, blizzards = parse(text)

    exit_pos_2d = (-1, -2)
    assert getindex(room_grid_2d, exit_pos_2d) == '.'
    start_pos_2d = (0, 1)
    assert getindex(room_grid_2d, start_pos_2d) == '.'

    # Find the "loop duration" (After enough steps, the blizzard pattern repeats)
    inner_height = len(room_grid_2d) - 2
    inner_width = len(room_grid_2d[0]) - 2
    loop_duration = math.lcm(inner_height, inner_width)

    # Simulate and create a 3D maze (The extra dimension is time)
    print(f'Simulating {loop_duration} timesteps...')
    raw_grid_3d = [make_slice(room_grid_2d, blizzards)]
    for _ in range(loop_duration - 1):  # Exclude the last iteration because that slice is the same as the first slice
        blizzards = simulate_one_timestep(room_grid_2d, blizzards)
        raw_grid_3d.append(make_slice(room_grid_2d, blizzards))
    grid_3d = InfiniteGrid3D(raw_grid_3d)

    # Solve
    depth = 0
    depth = find_shortest_path_length(grid_3d, depth, start_pos_2d, exit_pos_2d)
    depth = find_shortest_path_length(grid_3d, depth, exit_pos_2d, start_pos_2d)
    depth = find_shortest_path_length(grid_3d, depth, start_pos_2d, exit_pos_2d)
    print(depth)


def find_shortest_path_length(grid_3d, start_depth, start_pos_2d, exit_pos_2d):
    loop_duration = len(grid_3d._grid)

    for depth in range(loop_duration):
        setindex(grid_3d._grid, (depth, *start_pos_2d), '.')
        setindex(grid_3d._grid, (depth, *exit_pos_2d), 'X')

    start = (start_depth, *start_pos_2d)
    return bfs(start, grid_3d)


def bfs(node, grid_3d):
    def neighbors(node):
        for offset in [
            (1,  0,  0),
            (1,  0,  1),
            (1,  0, -1),
            (1,  1,  0),
            (1, -1,  0),
        ]:
            neighbor = addvec(node, offset)
            if grid_3d[neighbor] != '#':
                yield neighbor
    def is_exit(node):
        return grid_3d[node] == 'X'

    visited = set()
    q = collections.deque([node])
    while q:
        node = q.popleft()
        if is_exit(node):
            time = node[0]
            return time
        for v in neighbors(node):
            if v not in visited:
                visited.add(v)
                q.append(v)


class InfiniteGrid3D:
    def __init__(self, grid):
        self._grid = grid

    def __getitem__(self, key):
        time, r, c = key
        time = time % len(self._grid)
        return getindex(self._grid, (time, r, c))


def make_slice(room_grid_2d, blizzards):
    """ Create one 2-dimensional 'time slice' of the 3D maze. """
    outer_height = len(room_grid_2d)
    outer_width = len(room_grid_2d[0])
    result = []
    for r in range(outer_height):
        row = []
        result.append(row)
        for c in range(outer_width):
            pos = r, c
            ch = getindex(room_grid_2d, pos)
            if blizzards[pos]:
                ch = '#'
            row.append(ch)
    return result


def simulate_one_timestep(room_grid_2d, blizzards):
    new_blizzards = collections.defaultdict(list)
    for pos in blizzards:
        for direction in blizzards[pos]:
            offset = DIRECTIONS[direction]
            new_pos = addvec(pos, offset)
            if getindex(room_grid_2d, new_pos) == '.':
                new_blizzards[new_pos].append(direction)
            elif getindex(room_grid_2d, new_pos) == '#':
                new_pos = wrap(pos, direction, room_grid_2d)
                new_blizzards[new_pos].append(direction)
            else:
                raise Exception('Unreachable case')
    return new_blizzards


def wrap(pos, direction, room_grid_2d):
    offset = DIRECTIONS[direction]
    offset = mulvec(offset, -1)
    while getindex(room_grid_2d, addvec(pos, offset)) != '#':
        pos = addvec(pos, offset)
    return pos


def parse(text):
    room_grid_2d = [list(line) for line in text.splitlines()]

    blizzards = collections.defaultdict(list)

    for r, row in enumerate(room_grid_2d):
        for c, ch in enumerate(row):
            pos = r, c
            if ch in ['>', '<', '^', 'v']:
                blizzards[pos].append(ch)
                setindex(room_grid_2d, pos, '.')

    return room_grid_2d, blizzards


def getindex(grid, pos):
    for x in pos:
        grid = grid[x]
    return grid


def setindex(grid, pos, value):
    for x in pos[:-1]:
        grid = grid[x]
    grid[pos[-1]] = value


def addvec(a, b):
    return tuple(x+y for x,y in zip(a,b))


def mulvec(vec, s):
    return tuple(x*s for x in vec)


if __name__ == '__main__':
    main(sys.argv[1])
