import sys
from itertools import tee


DOWN = (0, 1)
DOWN_AND_LEFT = (-1, 1)
DOWN_AND_RIGHT = (1, 1)

SOURCE = (500, 0)


def main(path):
    global grid, active_particle
    grid = {}
    active_particle = SOURCE
    grid[active_particle] = 'o'

    for line in open(path).read().splitlines():
        vertices = [parse_vertex(each) for each in line.split(' -> ')]
        for v, w in pairwise(vertices):
            draw_line(grid, v, w)

    max_y = max(y for (x, y) in grid.keys())

    while True:
        simulate_one_step()
        if active_particle[1] > max_y:
            break

    print(sum(1 for particle in grid.values() if particle == 'o') - 1)


def simulate_one_step():
    global grid, active_particle
    assert grid.get(active_particle) == 'o'
    if (
        is_empty(new_pos := addvec(active_particle, DOWN))
        or is_empty(new_pos := addvec(active_particle, DOWN_AND_LEFT))
        or is_empty(new_pos := addvec(active_particle, DOWN_AND_RIGHT))
    ):
        del grid[active_particle]
        active_particle = new_pos
        grid[active_particle] = 'o'
    else:
        assert is_empty(SOURCE)
        active_particle = SOURCE
        grid[active_particle] = 'o'


def is_empty(pos):
    return grid.get(pos) is None


def draw_line(grid, start, end):
    direction = signvec(subvec(end, start))
    curr = start
    while curr != end:
        grid[curr] = '#'
        curr = addvec(curr, direction)
    grid[curr] = '#'


def parse_vertex(s):
    x, y = s.split(',')
    return (int(x), int(y))


def addvec(v, w):
    return (
        v[0] + w[0],
        v[1] + w[1],
    )


def subvec(v, w):
    return (
        v[0] - w[0],
        v[1] - w[1],
    )


def signvec(v):
    return (
        signum(v[0]),
        signum(v[1]),
    )


def signum(n):
    if n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return -1


# From https://docs.python.org/3/library/itertools.html#itertools.pairwise
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


if __name__ == '__main__':
    main(sys.argv[1])
