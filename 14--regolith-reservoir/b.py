import sys
from itertools import tee


DOWN = (0, 1)
DOWN_AND_LEFT = (-1, 1)
DOWN_AND_RIGHT = (1, 1)

SOURCE = (500, 0)


def main(path):
    global grid, active_particle, floor_y
    grid = {}
    active_particle = SOURCE
    grid[active_particle] = 'o'

    for line in open(path).read().splitlines():
        vertices = [parse_vertex(each) for each in line.split(' -> ')]
        for v, w in pairwise(vertices):
            draw_line(grid, v, w)

    max_y = max(y for (x, y) in grid.keys())
    floor_y = max_y + 2

    while True:
        done = simulate_one_step()
        if done:
            break

    print(sum(1 for particle in grid.values() if particle == 'o'))


def simulate_one_step():
    '''
    Simulate one step, then return a boolean: True if the simulation is over,
    False otherwise.
    '''
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
        return False
    elif is_empty(SOURCE):  # Particle is at rest and a new particle can be spawned
        active_particle = SOURCE
        grid[active_particle] = 'o'
        return False
    else:  # Particle is at rest at the source
        assert active_particle == SOURCE
        return True


def is_empty(pos):
    x, y = pos
    return (
        grid.get(pos) is None
        and y != floor_y
    )


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
